from typing import Any, Dict
from django.forms import ModelForm
from .models import Item, ItemQuery
from userauth.models import User
from .models import ItemQuery


class UserForm(ModelForm):
    """This is a User Form template"""

    class Meta:
        model = User
        fields = ["email", "password", "dob", "avatar"]


class ItemForm(ModelForm):
    """This is a Item Form template"""

    class Meta:
        model = Item
        exclude = ["bid_price", "bid_user"]


class BidForm(ModelForm):
    """This is a Bid Form template"""

    class Meta:
        model = Item
        fields = ["bid_user", "bid_price"]

    def clean(self):
        """Validate fields, this checks if bid_price is an invalid value"""
        # return all fields of the form, converted and validated to the correct types
        cleaned_data = super().clean()

        starting_price = self.instance.starting_price
        old_bid_price = self.instance.bid_price
        new_bid_price = cleaned_data["bid_price"]

        if new_bid_price is None:
            self.add_error("bid_price", "Bid price must be provided")
        elif old_bid_price is not None and new_bid_price <= old_bid_price:
            self.add_error(
                "bid_price", "New bid price must be higher than previous pid price"
            )
        elif new_bid_price < starting_price:
            self.add_error("bid_price", "Bid price cannot be less than starting price")


class QueryAnswerForm(ModelForm):
    """This is a Query answer Form template"""

    class Meta:
        model = ItemQuery
        fields = ["answer"]


class QueryQuestionForm(ModelForm):
    """This is a query question Form template"""

    class Meta:
        model = ItemQuery
        fields = ["item", "question", "asked_by"]
