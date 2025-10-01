import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

_logger = logging.getLogger("__main__")


def _info(msg: str):
    _logger.info(msg)


def _warning(msg: str):
    _logger.warning(msg)


def _fatal(msg: str):
    _logger.critical(msg)
    sys.exit(1)


def _error(msg: str):
    _logger.error(msg)


def _debug(msg: str):
    _logger.debug(msg)


def _exception(e: Exception, msg: str = None):
    _logger.exception(f"{msg if msg else 'Exception raised'}: {str(e)}")
