from datetime import datetime

import api.mailer as mailer
from api.models import Item


def end_item_auction(item: Item):
    """Send emails to item owner and bidder, and mark the item as ended"""
    # Send email to bidder if there is one
    if item.bid_user:
        mailer.highest_bidder(item)

    # Send email to owner no matter what
    mailer.auction_ended(item)

    item.mail_sent = True
    item.save()


def ended_items():
    """Return all items that have ended but haven't sent emails"""
    return Item.objects.filter(end_date__lte=datetime.now(), mail_sent=False)


def run():
    """Check if any items have ended, and send emails to items' owners and bidders"""
    for i in ended_items():
        end_item_auction(i)
