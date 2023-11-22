from typing import Callable
from django.http import HttpRequest, HttpResponse, QueryDict
from django.http.multipartparser import MultiPartParser
from django.utils.datastructures import MultiValueDict

GetResponseCallable = Callable[[HttpRequest], HttpResponse]


def rest_middleware(get_response: GetResponseCallable):
    """This creates request.PUT and request.DELETE"""

    def parse_request(request: HttpRequest) -> tuple[QueryDict, MultiValueDict]:
        if request.content_type.startswith("multipart"):
            parser = MultiPartParser(
                request.META,
                request,
                request.upload_handlers,
            )
            return parser.parse()
        else:
            return QueryDict(request.body), MultiValueDict()

    def middleware(request: HttpRequest):
        # Populate PUT and DELETE with empty dicts for now
        request.PUT = QueryDict("")
        request.DELETE = QueryDict("")

        # Parse request and load data
        if request.method == "PUT":
            request.PUT, request._files = parse_request(request)
        elif request.method == "DELETE":
            request.DELETE, request._files = parse_request(request)

        return get_response(request)

    return middleware
