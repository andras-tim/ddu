#!/usr/bin/env python3

__doc__ = 'DigitalOcean DNS Updater for Dynamic IP'

import argparse
import logging

from ddu.config import get_config
from ddu.digital_ocean_dns import DigitalOceanDns
from ddu.my_ip import get_my_ip


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.INFO,  # logging.WARNING, logging.DEBUG
        format='%(asctime)s %(levelname)-7s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    config = get_config(args.config)
    dns = DigitalOceanDns(config.dns_token, config.dns_domain)

    if args.list_records:
        dns.print_records()
        exit()

    my_ip = get_my_ip(config.my_ip_url, config.my_ip_attr)
    for record_id in config.dns_record_ids:
        dns.update_record_by_id(record_id, my_ip)


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
        default='config.json',
        help='Json config file path (default: %(default)s)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
