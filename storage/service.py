import csv
import io
import logging

import requests
import time

from PIL import Image

from cachecontrol import CacheControl, caches
from django.core import signing
from django.core.cache import cache
from django.urls import reverse

from storage.settings import DOCSHEETS_URL

logger = logging.getLogger(__name__)

http_cache = caches.FileCache('cache')
Image.preinit()


def load_image(url: str, session=None) -> tuple:
    if not url:
        return [None] * 3

    if not session:
        session = CacheControl(requests.session(), cache=http_cache)

    t0 = time.time()

    t000 = time.time()
    response = session.get(url=url, stream=True)
    logger.debug("time requests %s", time.time() - t000)

    if response.from_cache:
        return response, response.headers['content-type'], url

    try:
        t00 = time.time()

        image = Image.open(io.BytesIO(response.content))

        logger.debug('time to image open %s', time.time() - t00)
    except IOError:
        url = None
        image_content_type = None
    else:
        image_content_type = 'image/%s' % image.format.lower()

    logger.debug("Image %s", url)
    logger.debug("HTTP Status %s", response.status_code)
    logger.debug("Used cache %s", response.from_cache)
    logger.debug("Time %s", time.time() - t0)
    logger.debug("Content-Type %s", image_content_type)
    logger.debug("")

    return response, image_content_type, url


def load_csv() -> io.StringIO:
    sess = requests.session()
    cached_sess = CacheControl(sess, cache=http_cache)

    t0 = time.time()
    response = cached_sess.get(url=DOCSHEETS_URL)

    logger.debug("CSV %s", DOCSHEETS_URL)
    logger.debug("Used cache %s", response.from_cache)
    logger.debug("Time %s", time.time() - t0)
    logger.debug("")

    return io.StringIO(response.text)


def parse_csv(file) -> list:
    reader = csv.DictReader(file)

    for row in reader:
        image_url_inner = None
        image_url = row['image']
        if image_url:
            ct, _ = cache.get(image_url)
            if ct:
                image_url_inner = wrap_url(image_url)

        row['image'] = image_url_inner

        yield row


def wrap_url(image_url):
    url = reverse('image-proxy')
    signurl = signing.dumps(image_url)
    return "%s?url=%s" % (url, signurl)
