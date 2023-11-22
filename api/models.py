from decimal import Decimal
from django.db import models
from userauth.models import User
from datetime import datetime
import pytz


class Item(models.Model):
    """This represent an item"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")

    title = models.TextField()
    desc = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True)
    starting_price = models.DecimalField(decimal_places=2, max_digits=32)
    bid_price = models.DecimalField(
        decimal_places=2, max_digits=32, blank=True, null=True
    )
    bid_user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_items"
    )
    end_date = models.DateTimeField()
    mail_sent = models.BooleanField(default=False)

    def to_dict(self):
        """Convert an item to a JSON-serializable dictionary"""
        return {
            "id": self.id,
            "owner": self.owner.to_dict(),
            "title": self.title,
            "desc": self.desc,
            "photo_path": self.photo.url if self.photo else None,
            "starting_price": self.starting_price,
            "bid_price": self.bid_price,
            "bid_user": self.bid_user.to_dict() if self.bid_user else None,
            "end_date": self.end_date,
            # the price to be displayed publicly
            "current_price": self.current_price(),
            # whether this item has any bids
            "has_bids": self.bid_price is not None,
            # whether bidding for this item has ended
            "has_ended": self.has_ended(),
        }

    def current_price(self) -> Decimal:
        """Return the current price of this item"""
        if not self.bid_price:
            return self.starting_price

        if self.starting_price > self.bid_price:
            return self.starting_price
        else:
            return self.bid_price

    def has_ended(self) -> bool:
        """Return whether this item has ended, intended for the frontend"""
        return self.end_date < datetime.now(pytz.UTC) or self.mail_sent


class ItemQuery(models.Model):
    """This represent query for an item"""

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="queries",
    )

    question = models.TextField()
    answer = models.TextField(null=True)

    asked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="queries",
    )

    def to_dict(self):
        """Convert a query to a JSON-serializable dictionary"""
        return {
            "id": self.id,
            "question": self.question,
            "asked_by": self.asked_by.to_dict(),
            "answer": self.answer,
        }
