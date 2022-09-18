from rest_framework.views import exception_handler
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


def core_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        "Http404": _handle_not_found_error,
        "Not Found": _handle_not_found_error,
        "ValidationError": _handle_validation_error,
    }
    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](response)
    return response


def _handle_validation_error(response):
    response.data = {"code": HTTP_400_BAD_REQUEST, "message": "Validation Failed"}
    return response


def _handle_not_found_error(response):
    response.data = {"code": HTTP_404_NOT_FOUND, "message": "Item not found"}
    return response
