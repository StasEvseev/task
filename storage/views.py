import logging

from django.apps import apps

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from storage.exceptions import ServiceException
from storage.serializers import StorageSerializer

logger = logging.getLogger(__name__)

storage = apps.get_app_config('storage').get_storage()


class StorageViewSet(ViewSet):
    def list(self, request):
        try:
            data = storage.get_csv()
        except ServiceException as e:
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
        except ServiceException as e:
            logger.exception(str(e))
            raise exceptions.APIException()

        try:
            row = data[index]
        except IndexError:
            raise exceptions.NotFound()

        serializer = StorageSerializer(row)
        return Response(serializer.data)
