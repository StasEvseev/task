import io
import logging

import requests
import time

from PIL import Image

from cachecontrol import CacheControl, caches

from storage.exceptions import ServiceException
from storage.settings import DOCSHEETS_URL

logger = logging.getLogger(__name__)

http_cache = caches.FileCache('cache')
Image.preinit()


def load_image(url: str, session=None) -> tuple:
    if not url:
        return [None] * 2

    if not session:
        session = CacheControl(requests.session(), cache=http_cache)

    try:
        response = session.get(url=url, stream=True)
    except requests.exceptions.RequestException as e:
        logger.error(str(e))
        return [None] * 2

    if response.from_cache:
        return response, response.headers['content-type']

    try:
        image = Image.open(io.BytesIO(response.content))
    except IOError:
        image_content_type = None
    else:
        image_content_type = 'image/%s' % image.format.lower()

    logger.debug("Image %s", url)
    logger.debug("HTTP Status %s", response.status_code)
    logger.debug("Content-Type %s", image_content_type)
    logger.debug("")

    return response, image_content_type


def load_csv(url=None) -> tuple:
    url = url or DOCSHEETS_URL
    sess = requests.session()
    cached_sess = CacheControl(sess, cache=http_cache)

    t0 = time.time()
    try:
        response = cached_sess.get(url=url)
    except requests.exceptions.RequestException as e:
        logger.exception(str(e))
        raise ServiceException("Something went wrong")

    logger.debug("CSV %s", DOCSHEETS_URL)
    logger.debug("Used cache %s", response.from_cache)
    logger.debug("Time %s", time.time() - t0)
    logger.debug("")

    return io.StringIO(response.text), response
