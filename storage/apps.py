import time

from django.apps import AppConfig

from storage.store import StorageCSVRecords
from storage.settings import DOCSHEETS_URL


class StorageConfig(AppConfig):
    name = 'storage'
    storage = None

    def ready(self):
        t0 = time.time()
        self.storage = StorageCSVRecords(url=DOCSHEETS_URL)
        print("Boot time", time.time() - t0)

    def get_storage(self):
        return self.storage
