import logging
import time

from django.core import signing
from django.http import HttpResponse

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from storage.serializers import StorageSerializer
from storage.service import load_csv, parse_csv
from storage.cache import get_or_set_image

logger = logging.getLogger(__name__)


class MyViewSet(ViewSet):
    def list(self, request):
        t0 = time.time()

        csvfile = load_csv()
        data = parse_csv(csvfile)
        serializer = StorageSerializer(data, many=True)
        resp = Response(serializer.data)

        logger.debug("Time %s.%s %s", self.__class__.__name__,
                     self.action, time.time() - t0)

        return resp

    def retrieve(self, request, pk=None):
        t0 = time.time()

        try:
            index = int(pk)
        except ValueError:
            raise exceptions.ValidationError(None)

        csv = load_csv()
        data = parse_csv(csv)
        data = list(data)

        try:
            row = data[index]
        except IndexError:
            raise exceptions.NotFound()

        serializer = StorageSerializer(row)
        response = Response(serializer.data)

        logger.debug("Time %s.%s %s", self.__class__.__name__,
                     self.action, time.time() - t0)

        return response


def image(request):
    signurl = request.GET.get('url', '')

    if signurl:
        image_url = signing.loads(signurl)
        content_type, image_bytes = get_or_set_image(url=image_url)
        if content_type and image_bytes:
            return HttpResponse(image_bytes, content_type=content_type)

    return HttpResponse(signurl)
