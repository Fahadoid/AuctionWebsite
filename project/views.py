from django.http import HttpResponse, HttpRequest


def health(request: HttpRequest) -> HttpResponse:
    """/health endpoint for deploying in OpenShift"""
    return HttpResponse()
