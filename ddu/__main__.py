#!/usr/bin/env python3

__doc__ = 'DigitalOcean DNS Updater for Dynamic IP'

import argparse
import logging
from pathlib import Path
from time import sleep

from ddu.cache import get_cache
from ddu.config import Config, get_config
from ddu.digital_ocean_dns import DigitalOceanDns
from ddu.my_ip import MyIp

BASE_DIR = Path(__file__).parent


def main():
    args = parse_args()
    logging.basicConfig(
        level=[logging.WARNING, logging.INFO, logging.DEBUG][args.verbose],
        format='%(asctime)s{} %(message)s'.format('' if args.verbose < 2 else ' %(name)-25s %(levelname)-7s'),
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    config = get_config(args.config)
    dns = DigitalOceanDns(config.dns_token, config.dns_domain)

    if args.list_records:
        dns.print_records()
        exit()

    with get_cache(BASE_DIR.joinpath('.cache.json')) as cache:
        try:
            main_loop(config, cache, dns)
        except KeyboardInterrupt:
            pass


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '-l',
        '--list-records',
        action='store_true',
        help='List records for getting record ID'
    )
    parser.add_argument(
        '--config',
        metavar='PATH',
        type=argparse.FileType(),
        default=str(BASE_DIR.joinpath('config.json')),
        help='Json config file path (default: %(default)s)'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Increase verbosity (max verbosity: -vv)'
    )

    args = parser.parse_args()
    if args.verbose is None:
        args.verbose = 0
    elif args.verbose > 2:
        args.verbose = 2

    return args


def main_loop(config: Config, cache: dict, dns: DigitalOceanDns):
    my_ip = MyIp(config.my_ip_url, config.my_ip_attr)

    while True:
        current_ip = my_ip.get()
        if current_ip and current_ip != cache.get('last_ip'):
            for record_id in config.dns_record_ids:
                dns.update_record_by_id(record_id, current_ip)

            cache['last_ip'] = current_ip

        sleep(config.check_freq_s)


if __name__ == '__main__':
    main()
