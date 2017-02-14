import asyncio
import logging
import time

from django.core.cache import cache

from storage.service import load_image, load_csv, rows_of_csv

logger = logging.getLogger(__name__)


class StorageCSVRecords(object):
    """
    Object which responsibility is keep csv records in cache and actualizing it
    when it required.
    """
    def __init__(self, url):
        self.url = url

    def init_cache(self, csvfile=None):
        logger.debug("Initialization of cache.")
        t0 = time.time()

        if not csvfile:
            csvfile, response = load_csv(url=self.url)

        rows = rows_of_csv(csvfile)
        logger.debug("CSV file has a `%s` lines", len(rows))

        result = []
        for row in rows:
            image_url = row['image']
            response, image_content_type = load_image(url=image_url)

            if not image_content_type:
                row['image'] = None

            result.append(row)
        cache.set(self.url, result)

        logger.debug("Initialization take `%s`", time.time() - t0)

    def get_csv(self):
        csvfile, response = load_csv(url=self.url)

        if response.from_cache and cache.get(self.url):
            return cache.get(self.url)
        else:
            self.init_cache(csvfile=csvfile)
            return cache.get(self.url)


class AsyncStorageCSVRecords(StorageCSVRecords):
    """
    Asyncronous version of StorageCSVRecords
    """
    def init_cache(self, csvfile=None):
        async def main(urls, loop):
            coroutines = [asyncio.coroutine(load_image)(url) for url in urls]
            completed, pending = await asyncio.wait(coroutines, timeout=5000,
                                                    loop=loop)
            return completed

        def load_images(urls):
            loop = asyncio.new_event_loop()
            future_task = main(urls, loop)
            res = loop.run_until_complete(future_task)
            return res

        logger.debug("Initialization of cache.")
        t0 = time.time()

        if not csvfile:
            csvfile, response = load_csv(url=self.url)

        rows = rows_of_csv(csvfile)
        logger.debug("CSV file has a `%s` lines", len(rows))

        urls_images = [row['image'] for row in rows]
        images = load_images(urls_images)

        result = []
        for image, row in zip(images, rows):
            response, image_content_type = image.result()

            if not image_content_type:
                row['image'] = None

            result.append(row)
        cache.set(self.url, result)

        logger.debug("Initialization take `%s`", time.time() - t0)
