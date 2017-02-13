import time
from django.apps import AppConfig

from storage.cache import init_caches, async_init_caches


class StorageConfig(AppConfig):
    name = 'storage'

    def ready(self):
        t0 = time.time()
        init_caches()
        print("Boot times", time.time() - t0)
