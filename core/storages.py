from django.conf import settings

from storages.backends.azure_storage import AzureStorage


class AzureStaticStorage(AzureStorage):
    azure_container = settings.AZURE_STATIC_CONTAINER
    location = settings.AZURE_STATIC_LOCATION


class AzureMediaStorage(AzureStorage):
    azure_container = settings.AZURE_MEDIA_CONTAINER
    location = settings.AZURE_MEDIA_LOCATION
