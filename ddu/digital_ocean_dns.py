import logging
import os
from typing import Any, Dict, Generator
from urllib.parse import urljoin

import requests

_logger = logging.getLogger(__name__)


class DigitalOceanDns:
    def __init__(self, token: str, domain: str):
        self.__domain = domain
        self.__records_url = 'https://api.digitalocean.com/v2/domains/{domain}/records/'.format(domain=domain)

        self.__session = requests.Session()
        self.__session.headers.update({
            'Authorization': 'Bearer {}'.format(token),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        })

    def __request(self, method: str, url: str, *args, **kwargs):
        result = self.__session.request(method, url, *args, **kwargs)
        result.raise_for_status()

        return result

    def iterate_records(self) -> Generator[Dict[str, Any], None, None]:
        _logger.info('Enumerating records of {!r} domain'.format(self.__domain))

        records_url = self.__records_url
        while True:
            response = self.__request('GET', records_url).json()
            for record in response['domain_records']:
                yield record

            records_url = response['links']['pages'].get('next')
            if not records_url:
                return

    def update_record_by_id(self, record_id: int, record_data: str, ttl: int):
        _logger.info('Updating record; record_id={!r}, new_data={!r}'.format(record_id, record_data))

        self.__request(
            'PUT',
            urljoin(self.__records_url, str(record_id)),
            json={
                'data': record_data,
                'ttl': ttl
            }
        )

    def print_records(self):
        records = sorted(self.iterate_records(), key=self.__record_printer_order_key)

        line_template = '{id:>9}  {name:<30}  {type:<5}  {data:<60}  {ttl}'

        lines = [
            line_template.format(id='ID', name='RECORD', type='TYPE', data='DATA', ttl='TTL'),
            '-' * 120,
        ]

        for record in records:
            lines.append(line_template.format(**record))

        print(os.linesep.join(lines))

    def __record_printer_order_key(self, record: Dict[str, Any]) -> str:
        return '{name}_{type}_{data}'.format(**record)
