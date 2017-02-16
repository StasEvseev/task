import csv
import logging

from django.core import signing
from django.core.cache import cache
from django.core.signing import BadSignature
from django.urls import reverse

from storage.exceptions import StoreException
from storage.service import load_image, load_csv

logger = logging.getLogger(__name__)


class StorageCSVRecords(object):
    """
    Object which responsibility is keep csv records in cache and actualizing it
    when it required.
    Checks corrections of image urls into CSV by demand.
    """
    def __init__(self, url):
        self.url = url

    def is_valid(self, image_url: str) -> bool:
        is_valid = cache.get(image_url)

        if is_valid is None:
            response, content_type = load_image(url=image_url)

            is_valid = content_type is not None
            cache.set(image_url, is_valid)

        return is_valid

    def get_csv(self):
        csvfile, response = load_csv(url=self.url)

        if response.from_cache and cache.get(self.url):
            return cache.get(self.url)
        else:
            rows = list(self.parse_csv(csvfile))
            cache.set(self.url, rows)
            return rows

    @classmethod
    def unwrap_url(cls, signurl: str) -> str:
        try:
            image_url = signing.loads(signurl)
        except BadSignature as e:
            logger.error(str(e))
            raise StoreException('Bad signature')

        return image_url

    @classmethod
    def wrap_url(cls, image_url: str) -> str:
        url = reverse('image-proxy')
        signurl = signing.dumps(image_url)

        return "%s?url=%s" % (url, signurl)

    def parse_csv(self, file):
        reader = csv.DictReader(file)

        for row in reader:
            image_url = row['image']
            if image_url:
                image_url = self.wrap_url(image_url)

            row['image'] = image_url
            yield row
