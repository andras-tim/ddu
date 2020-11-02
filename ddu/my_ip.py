import logging
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

_logger = logging.getLogger(__name__)


class MyIp:
    def __init__(self, url: str, arg_name: Optional[str]):
        self.__url = url
        self.__arg_name = arg_name

        adapter = HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=0.5))
        self.__session = requests.Session()
        self.__session.mount('http://', adapter)
        self.__session.mount('https://', adapter)

    def get(self) -> Optional[str]:
        _logger.debug('Getting current IP')

        try:
            response = self.__session.get(self.__url)
            response.raise_for_status()
        except requests.RequestException as e:
            _logger.error('Error caused while getting current IP: {}'.format(e))
            return None

        result = response.json()
        if self.__arg_name:
            result = result[self.__arg_name]

        _logger.info('Current IP is {!r}'.format(result))

        return result
