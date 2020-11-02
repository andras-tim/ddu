import json
import logging
from contextlib import contextmanager
from pathlib import Path

_logger = logging.getLogger(__name__)


@contextmanager
def get_cache(persist_file: Path):
    data = {}
    if persist_file.is_file():
        _logger.debug('Opening cache persist file {}'.format(persist_file))
        with persist_file.open() as fd:
            data = json.load(fd)
    try:
        yield data
    finally:
        _logger.debug('Writing cache persist file {}'.format(persist_file))
        with persist_file.open('w') as fd:
            json.dump(data, fd, ensure_ascii=False, indent=4, sort_keys=True)
            fd.write('\n')
