import logging

from django.http import HttpResponseBadRequest, JsonResponse

from DjangoAppCenter.dtos.ret import BaseRet
from settings.profile import SettingsLoaderError

logger = logging.getLogger("exception")


class CustomException(object):
    def process_exception(self, request, exception):
        logger.exception(exception)

        if isinstance(exception, SettingsLoaderError):
            return JsonResponse(BaseRet.fail(exception.message))

        else:
            return HttpResponseBadRequest()
