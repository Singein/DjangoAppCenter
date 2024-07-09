import logging

from django.http import HttpResponseBadRequest, JsonResponse

logger = logging.getLogger("exception")


class CustomException(Exception):
    pass


class GlobalExceptionHandler(object):
    def process_exception(self, request, exception):
        logger.exception(exception)

        if isinstance(exception, CustomException):
            logger.error(f"CustomException: {exception}")
            return JsonResponse({'msg': str(exception), 'code': -1})
        else:
            logger.error(f"GlobalExceptionHandler: {exception}")
            return HttpResponseBadRequest()
