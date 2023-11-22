from functools import wraps
from typing import Callable, TypeVar

from django.contrib.auth import get_user_model, login
from django.db.models import Q
from django.http import HttpRequest, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from userauth.models import User

from .forms import BidForm, ItemForm, QueryAnswerForm, QueryQuestionForm, UserForm
from .models import Item, ItemQuery

TCallable = TypeVar("TCallable", bound=Callable)


def require_login(func: TCallable) -> TCallable:
    """Decorator to only permit authenticated users"""

    @wraps(func)
    def wrapped(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "You must be authenticated to perform this action.",
                },
                status=401,  # unauthorized
            )
        return func(request, *args, **kwargs)

    return wrapped


@require_http_methods(["GET", "PUT"])
@csrf_exempt
def profile(request: HttpRequest):
    """Return/Update information about the currently-logged-in user, or None if not logged in."""
    user: User = request.user

    if request.method == "GET":
        if request.user.is_authenticated:
            return JsonResponse({"status": "OK", "value": user.to_dict()})
        else:
            return JsonResponse({"status": "OK", "value": None})
    else:
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "You must be authenticated to perform this action.",
                },
                status=401,  # unauthorized
            )

        form = UserForm(request.PUT, request.FILES, instance=user)

        if form.is_valid():
            form.save()

            # Bugfix - Password should be encrypted before saving
            user.set_password(request.PUT.get("password", ""))
            user.save()

            login(request, user)
            return JsonResponse({"status": "OK"})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "Failed to save changes to user",
                    "errors": errors,
                },
                status=400,  # bad request
            )


@require_http_methods(["GET", "PUT"])
@require_login
@csrf_exempt
def show_user(request: HttpRequest, user_id: int):
    """This method will show/update one user"""
    is_own_user = request.user.id == user_id

    if request.method == "GET":
        # GET any user
        user: User = get_user_model().objects.get(id=user_id)

        return JsonResponse({"status": "OK", "value": user.to_dict()})
    else:
        # PUT, only allow editing the own user
        if not is_own_user:
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "You can only edit your own user profile",
                },
                status=403,  # forbidden
            )

        user: User = get_user_model().objects.get(id=user_id)
        form = UserForm(request.PUT, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return JsonResponse({"status": "OK"})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "Failed to save changes to user",
                    "errors": errors,
                },
                status=400,  # bad request
            )


@require_http_methods(["GET", "POST"])
@require_login
@csrf_exempt
def list_items(request: HttpRequest):
    """Show or search list of all items, or create a new item"""
    if request.method == "GET":
        search = request.GET.get("q", None)
        if search:
            items = Item.objects.filter(
                Q(title__icontains=search) | Q(desc__icontains=search)
            )
        else:
            items = Item.objects.all()

        return JsonResponse({"status": "OK", "value": [i.to_dict() for i in items]})
    else:
        item_params = request.POST.copy()
        item_params["owner"] = request.user

        form = ItemForm(item_params, request.FILES)
        if form.is_valid():
            item: Item = form.save()
            return JsonResponse({"status": "OK", "value": item.to_dict()})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "Failed to create the item",
                    "errors": errors,
                },
                status=400,  # bad request
            )


@require_http_methods(["GET", "PUT"])
@require_login
@csrf_exempt
def show_item(request: HttpRequest, item_id: int):
    """Show/update one item"""
    item = Item.objects.get(id=item_id)
    is_own_item = item.owner == request.user

    if request.method == "GET":
        # GET any item
        return JsonResponse({"status": "OK", "value": item.to_dict()})
    else:
        # PUT, only allow editing own items
        if not is_own_item:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "You can only edit your own items",
                    "errors": errors,
                },
                status=401,  # unauthorized
            )

        item_params = request.PUT.copy()
        item_params["owner"] = request.user

        form = ItemForm(item_params, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            item.refresh_from_db()
            return JsonResponse({"status": "OK", "value": item.to_dict()})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "Failed to update the item",
                    "errors": errors,
                },
                status=400,  # bad request
            )


@require_http_methods(["PUT"])
@require_login
@csrf_exempt
def bid_item(request: HttpRequest, item_id: int):
    """update one bid item"""
    item = Item.objects.get(id=item_id)
    is_own_item = item.owner == request.user

    if is_own_item:
        return JsonResponse(
            {"status": "FAILED", "message": "You cannot bid on your own items."},
            status=401,  # unauthorized
        )

    if item.has_ended():
        return JsonResponse(
            {"status": "FAILED", "message": "Item auction has ended."},
            status=403,  # forbidden
        )

    # get parameters in the form of a mutable QueryDict using copy()
    item_params = request.PUT.copy()
    # bid user must be the current user
    item_params["bid_user"] = request.user

    form = BidForm(item_params, instance=item)
    if form.is_valid():
        form.save()
        item.refresh_from_db()
        return JsonResponse({"status": "OK", "value": item.to_dict()})
    else:
        errors = form.errors.get_json_data()
        return JsonResponse(
            {
                "status": "FAILED",
                "message": "Failed to place bid on the item",
                "errors": errors,
            },
            status=400,  # bad request
        )


@require_http_methods(["GET", "POST"])
@require_login
@csrf_exempt
def list_item_queries(request: HttpRequest, item_id: int):
    """show all queries of one item, or create a new query"""
    item = Item.objects.get(id=item_id)

    if request.method == "GET":
        # list all item queries for this item
        return JsonResponse(
            {"status": "OK", "value": [q.to_dict() for q in item.queries.all()]}
        )
    else:
        # create an item query for this item
        # the answer field should remain blank

        # get parameters in the form of a mutable QueryDict using copy()
        query_params = request.POST.copy()
        # asker user must be the current user
        query_params["asked_by"] = request.user
        # set the item of this query
        query_params["item"] = item

        form = QueryQuestionForm(query_params)
        if form.is_valid():
            query: ItemQuery = form.save()
            return JsonResponse({"status": "OK", "value": query.to_dict()})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "Failed to create an item query",
                    "errors": errors,
                },
                status=400,  # bad request
            )


@require_http_methods(["PUT"])
@require_login
@csrf_exempt
def answer_item_query(request: HttpRequest, item_id: int, query_id: int):
    """answer to question about a query"""
    item = Item.objects.get(id=item_id)
    is_own_item = item.owner == request.user

    if not is_own_item:
        return JsonResponse(
            {
                "status": "FAILED",
                "message": "You can only answer queries on your own items.",
            },
            status=401,  # unauthorized
        )

    query: ItemQuery = item.queries.get(id=query_id)
    query_params = request.PUT.copy()

    form = QueryAnswerForm(query_params, instance=query)
    if form.is_valid():
        form.save()
        query.refresh_from_db()
        return JsonResponse({"status": "OK", "value": query.to_dict()})
    else:
        errors = form.errors.get_json_data()
        return JsonResponse(
            {
                "status": "FAILED",
                "message": "Failed to answer the query.",
                "errors": errors,
            },
            status=400,  # bad request
        )


@require_http_methods(["GET", "PUT"])
@require_login
@csrf_exempt
def show_item_query(request: HttpRequest, item_id: int, query_id: int):
    """show/update one query of an item"""
    item = Item.objects.get(id=item_id)
    query: ItemQuery = item.queries.get(id=query_id)
    is_own_query = query.asked_by == request.user

    if request.method == "GET":
        # show a single query
        return JsonResponse({"status": "OK", "value": query.to_dict()})
    else:
        # update a single query
        if not is_own_query:
            return JsonResponse(
                {"status": "FAILED", "message": "You can only edit your own queries."},
                status=401,  # unauthorized
            )

        # get parameters in the form of a mutable QueryDict using copy()
        query_params = request.PUT.copy()
        # asker user must be the current user
        query_params["asked_by"] = request.user
        # set the item of this query
        query_params["item"] = item

        form = QueryQuestionForm(query_params, instance=query)
        if form.is_valid():
            form.save()
            query.refresh_from_db()
            return JsonResponse({"status": "OK", "value": query.to_dict()})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {
                    "status": "FAILED",
                    "message": "Failed to update the query",
                    "errors": errors,
                },
                status=400,  # bad request
            )
