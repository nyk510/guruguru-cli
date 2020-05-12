from typing import Union
from urllib.parse import urljoin

import requests

from . import constance


class BaseUrlSession(requests.Session):
    def __init__(self, base_url: Union[None, str] = None):
        self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def get_auth_headers(self):
        token = constance.config.get_token()
        if token is None:
            return {}

        return {
            'authorization': f'JWT {token}'
        }

    def request(self, method: str, url: str, use_auth=True, headers: Union[None, dict] = None, **kwargs):
        if self.base_url is not None:
            url = urljoin(self.base_url, url)
        headers = {} if headers is None else headers
        if use_auth:
            auth_header = self.get_auth_headers()
            headers.update(auth_header)
        return super(BaseUrlSession, self).request(method, url, headers=headers, **kwargs)


guruguru_session = BaseUrlSession(base_url=constance.BASE_URL)
