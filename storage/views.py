import logging

from django.apps import apps
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseServerError

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from storage.exceptions import BaseStoreException
from storage.serializers import StorageSerializer

logger = logging.getLogger(__name__)

storage = apps.get_app_config('storage').get_storage()


class StorageViewSet(ViewSet):
    def list(self, request):
        try:
            data = storage.get_csv()
        except BaseStoreException as e:
            logger.exception(str(e))
            raise exceptions.APIException()

        serializer = StorageSerializer(data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            index = int(pk)
        except ValueError:
            raise exceptions.ValidationError(None)

        if index <= 0:
            raise exceptions.ValidationError(None)

        index -= 1
        try:
            data = storage.get_csv()
        except BaseStoreException as e:
            logger.exception(str(e))
            raise exceptions.APIException()

        try:
            row = data[index]
        except IndexError:
            raise exceptions.NotFound()

        serializer = StorageSerializer(row)
        return Response(serializer.data)


def image(request):
    signurl = request.GET.get('url', '')

    if not signurl:
        return HttpResponse()

    try:
        image_url = storage.unwrap_url(signurl=signurl)
    except BaseStoreException as e:
        logger.exception(str(e), signurl)
        return HttpResponseServerError()

    is_valid = storage.is_valid(image_url=image_url)

    if not is_valid:
        raise Http404()

    return HttpResponsePermanentRedirect(image_url)
