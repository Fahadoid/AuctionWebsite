from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "api"
urlpatterns = [
    path("items/", views.list_items, name="items"),
    path("items/<int:item_id>/", views.show_item, name="item"),
    path("items/<int:item_id>/bid/", views.bid_item, name="bid_item"),
    path("items/<int:item_id>/queries/", views.list_item_queries, name="item_queries"),
    path(
        "items/<int:item_id>/queries/<int:query_id>/",
        views.show_item_query,
        name="item_query",
    ),
    path(
        "items/<int:item_id>/queries/<int:query_id>/answer/",
        views.answer_item_query,
        name="answer_item_query",
    ),
    path("users/<int:user_id>/", views.show_user, name="users"),
    path("profile/", views.profile, name="profile"),
]
