import logging
import tomllib
from dataclasses import dataclass, field
from typing import Optional

from .constants import (
    DEFAULT_CONFIG_FILE,
    DEFAULT_ENV,
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_FORMAT,
)


@dataclass(frozen=False)
class ContextData:
    api_host: str
    api_port: int
    api_key: str
    http_port: int
    refresh_rate: int
    push: bool
    gateway: str
    gateway_port: int
    job: str

    # def __post_init__(self):
    #     print(self)


class Context:
    @staticmethod
    def read_config(config_file: Optional[str] = DEFAULT_CONFIG_FILE, env: Optional[str] = DEFAULT_ENV) -> ContextData:
        """Parse the config and returns a populated dataclass"""
        with open(config_file, "rb") as f:
            data = tomllib.load(f)
        ctx = ContextData(
            api_host=data[env]["api_host"],
            api_port=data[env]["api_port"],
            api_key=data[env]["api_key"],
            http_port=data[env]["http_port"],
            refresh_rate=data[env]["refresh_rate"],
            push=data[env]["push"],
            gateway=data[env]["gateway"],
            gateway_port=data[env]["gateway_port"],
            job=data[env]["job"],
        )
        return ctx


def configure_logging(log_level: int = logging.INFO) -> None:
    """
    Set up standard logging.

    Parameters:
    - log_level str: The log level to use. Should be one of "DEBUG, INFO, WARNING, or ERROR"
    """
    logging.basicConfig(level=log_level, filename=DEFAULT_LOG_FILE, filemode="a", format=DEFAULT_LOG_FORMAT)
    logging.getLogger("").addHandler(logging.StreamHandler())


if __name__ == "__main__":
    ctx = Context.read_config()
    print(ctx)
