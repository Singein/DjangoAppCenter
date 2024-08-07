import logging

from django.http import HttpResponseBadRequest, JsonResponse

logger = logging.getLogger("exception")


class BaseException(Exception):
    pass


class ExceptionHandler(object):
    def process_exception(self, request, exception):
        logger.exception(exception)

        if isinstance(exception, BaseException):
            # 记录日志
            return JsonResponse({"msg": "System Error"}, status=500)

        else:
            return HttpResponseBadRequest()
