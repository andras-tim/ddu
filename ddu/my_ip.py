import logging
from typing import Optional

import requests

_logger = logging.getLogger(__name__)


def get_my_ip(url: str, arg_name: Optional[str]) -> str:
    _logger.debug('Getting current IP')

    response = requests.get(url)
    response.raise_for_status()

    result = response.json()
    if arg_name:
        result = result[arg_name]

    _logger.info('Current IP is {!r}'.format(result))

    return result
