import json
import logging
from typing import List, NamedTuple, Optional

_logger = logging.getLogger(__name__)

Config = NamedTuple(
    'Config', [
        ('my_ip_url', str),
        ('my_ip_attr', Optional[str]),
        ('dns_token', str),
        ('dns_domain', str),
        ('dns_record_ids', List[int]),
    ]
)


def get_config(config_fd) -> Config:
    _logger.debug('Reading config')

    raw_config = json.load(config_fd)
    config = Config(**raw_config)

    if _logger.isEnabledFor(logging.DEBUG):
        _logger.debug('Current config is: {}'.format(config))

    return config
