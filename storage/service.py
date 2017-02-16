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


def get_content_type(iostream):
    try:
        image = Image.open(iostream)
    except IOError:
        image_content_type = None
    else:
        image_content_type = 'image/%s' % image.format.lower()
    return image_content_type


def load_image(url: str, session=None) -> tuple:
    if not url:
        logger.debug("Skip loading. Url is empty.")
        return [None] * 2

    if not session:
        session = CacheControl(requests.session(), cache=http_cache)

    try:
        response = session.get(url=url, stream=True)
    except requests.exceptions.RequestException as e:
        logger.error(str(e))
        return [None] * 2

    if response.from_cache:
        content_type = get_content_type(io.BytesIO(response.content))
        logger.debug("Result `%s` fetched from cache. Content-Type `%s`", url,
                     content_type)
        return response, content_type

    content_type = get_content_type(io.BytesIO(response.content))
    logger.debug("Loaded file `%s`. HTTP Status `%s`. Content-Type `%s`.", url,
                 response.status_code, content_type)

    return response, content_type


def load_csv(url=None) -> tuple:
    """
    :raises ServiceException
        - raises when requests can't connect to CSV file OR
            returned file has a wrong `content-type`

    :return: tuple of :io.String: and :response: object
    """
    content_type_csv = 'text/csv'
    url = url or DOCSHEETS_URL

    cached_sess = CacheControl(requests.session(), cache=http_cache)

    t0 = time.time()
    try:
        response = cached_sess.get(url=url, stream=True)
    except requests.exceptions.RequestException as e:
        logger.exception("Check connect to %s, Detail (%s)", url, str(e))
        raise ServiceException("Something went wrong")

    if response.headers['content-type'] != content_type_csv:
        message = (
            "Wrong content-type `%s` of file by address %s. Expected `%s`" % (
                response.headers['content-type'], url, content_type_csv
            )
        )
        logger.error(message)
        raise ServiceException(message)

    logger.debug("CSV loaded by address `%s`. From cache %s. Time %s", url,
                 response.from_cache, time.time() - t0)

    return io.StringIO(response.text), response
