import asyncio
import csv
import logging

from PIL import Image

from cachecontrol import caches

from django.core.cache import cache

from storage.service import load_image, load_csv

logger = logging.getLogger(__name__)

http_cache = caches.FileCache('cache')
Image.preinit()


def async_init_caches():
    async def main(urls, loop):
        coroutines = [asyncio.coroutine(load_image)(url)
                      for url in urls]
        completed, pending = await asyncio.wait(coroutines, timeout=5000,
                                                loop=loop)
        return completed

    def load_images(urls):
        loop = asyncio.new_event_loop()
        future_task = main(urls, loop)
        res = loop.run_until_complete(future_task)
        return res

    csvfile = load_csv()
    reader = csv.DictReader(csvfile)
    urls_images = [row['image'] for row in reader]
    images = load_images(urls_images)

    for image in images:
        response, image_content_type, url = image.result()
        if response and image_content_type:
            cache.set(url, (image_content_type, response.content))


def init_caches():
    csvfile = load_csv()
    reader = csv.DictReader(csvfile)
    for row in reader:
        image_url = row['image']

        response, image_content_type, _ = load_image(url=image_url)

        content = None
        if response:
            content = response.content

        cache.set(image_url, (image_content_type, content))


def cache_control_max_age(response):
    cc = response.connection.controller.parse_cache_control(response.headers)
    if (cc and 'max-age' in cc and cc['max-age'].isdigit()
            and int(cc['max-age']) > 0):
        return int(cc['max-age'])
    return None


def get_or_set_image(url):
    res = cache.get(url)

    if not res:
        response, image_content_type, _ = load_image(url=url)

        if response and image_content_type:
            res = (image_content_type, response.content)
            cache.set(url, res)
        else:
            res = None, None

    return res
