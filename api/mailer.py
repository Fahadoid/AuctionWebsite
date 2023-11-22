from django.conf import settings
from django.core.mail import send_mail
from userauth.models import User
from api.models import Item
import textwrap
import re


def print_mail(subject: str, message: str, email: str):
    """Print the email in console"""
    print("---------------------------------------------")
    print(f"Sending email to: {email}")
    print(f"Subject: {subject}\n")
    print(message)
    print("---------------------------------------------")


def send_or_print_mail(subject: str, message: str, email: str):
    """Send an email to a user. If PRINT_EMAILS is set to true, then just print the email in console and skip sending"""
    if settings.PRINT_EMAILS:
        for allowed_regex in settings.PRINT_PERMITTED_EMAILS_REGEX:
            match = re.search(allowed_regex, email)
            if match:
                # email permitted, send email
                send_mail(subject, message, None, [email], fail_silently=False)
                return

        print_mail(subject, message, email)
    else:
        send_mail(subject, message, None, [email], fail_silently=False)


def highest_bidder(item: Item):
    """Send an "auction ended" email to the highest bidder of an item"""
    user = item.bid_user
    if user is None:
        raise RuntimeError("Item does not have a bidder!")

    subject = f"Auction ended - You are the highest bidder for {item.title}"

    message = textwrap.dedent(
        f"""\
        Congratulations! You are the highest bidder in the recent auction for {item.title}. Your final bid amount was £{item.bid_price}.

        You can proceed to purchase the item. Please contact the seller at: {item.owner.email}

        Sincerely,
        fBay
        """
    )

    send_or_print_mail(subject, message, user.email)


def auction_ended(item: Item):
    """Send an "auction ended" email to the owner of an item"""
    if item.bid_user is None:
        # no one bid on the item
        subject = f"Auction ended - There were no bidders on your item {item.title}"
        message = textwrap.dedent(
            f"""\
            Unfortunately, there were no bidders in your recent auction for {item.title}.

            Sincerely,
            fBay
            """
        )
    else:
        # someone bit on the item
        subject = f"Auction ended - you are the highest bidder for {item.title}"
        message = textwrap.dedent(
            f"""\
            Congratulations! Your recent auction for {item.title} ended with a £{item.bid_price} bid by {item.bid_user.email}.

            Sincerely,
            fBay
            """
        )

    send_or_print_mail(subject, message, item.owner.email)


def welcome_user(user: User):
    """Send a welcome email to a user"""
    subject = f"Welcome to fBay!"

    message = textwrap.dedent(
        f"""\
        Thank you for registering on fBay!

        Sincerely,
        fBay
        """
    )

    send_or_print_mail(subject, message, user.email)
