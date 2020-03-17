from urllib.parse import urljoin

import requests

from . import constance


class BaseUrlSession(requests.Session):
    def __init__(self, base_url):
        self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def request(self, method, url, **kwargs):
        url = urljoin(self.base_url, url)
        return super(BaseUrlSession, self).request(method, url, **kwargs)


guruguru_session = BaseUrlSession(base_url=constance.BASE_URL)
