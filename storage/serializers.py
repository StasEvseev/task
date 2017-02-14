from rest_framework import serializers


class StorageSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField()
