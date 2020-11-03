import logging
import socket
from contextlib import contextmanager
from typing import Generator, Optional

_logger = logging.getLogger(__name__)

_BUFFER_SIZE = 100
_MAGIC_COMMAND = 'get-my-ip'


@contextmanager
def get_my_ip(host: str, port: int, command: Optional[str] = None) -> Generator[Optional[str], None, None]:
    _logger.debug('Getting current IP')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            if command:
                sent = sock.sendall(command.encode())
                if sent == 0:
                    raise RuntimeError('Socket connection broken')
        except Exception as e:
            _logger.error('Error caused while getting current IP: {}'.format(e))
            yield None
            return

        public_ip = sock.recv(_BUFFER_SIZE).decode().rstrip('\n')
        _logger.info('Current public IP is {!r}'.format(public_ip))

        try:
            yield public_ip

            _logger.debug('Waiting for connection termination')
            __set_keepalive(sock)
            if sock.recv(_BUFFER_SIZE) != b'':
                _logger.warning('Unwanted data received')

        except TimeoutError:
            pass

        finally:
            _logger.debug('Closing connection')


def __set_keepalive(sock: socket.SocketType, after_idle_sec: int = 1, interval_sec: int = 3, max_fails: int = 5):
    _logger.debug('Enable TCP keep-alive')
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)
