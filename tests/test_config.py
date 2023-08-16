import pytest
from pytest_mock import MockerFixture

from camerametrics.utils.config import Context, configure_logging

from .responses import (
    MOCK_TOML_DATA_DEV,
    MOCK_TOML_DATA_MISSING_KEYS,
    MOCK_TOML_DATA_PROD,
)

# Combine all the mock data for easier access
ALL_MOCK_DATA = {"Dev": MOCK_TOML_DATA_DEV, "Prod": MOCK_TOML_DATA_PROD}


@pytest.fixture
def mock_toml_load(mocker: MockerFixture):
    return mocker.patch("camerametrics.utils.config.tomllib.load")


def test_read_config_with_missing_keys(mocker):
    # Simulate missing keys in the toml data
    mocker.patch("camerametrics.utils.config.tomllib.load", return_value=MOCK_TOML_DATA_MISSING_KEYS)

    with pytest.raises(KeyError):
        Context.read_config()


def test_read_config_with_defaults(mocker: MockerFixture):
    # Mock the tomllib.load method
    mocked_load = mocker.patch("camerametrics.utils.config.tomllib.load", return_value=MOCK_TOML_DATA_DEV)

    # Test the function
    ctx = Context.read_config()

    # Assert
    assert ctx.api_host == "localhost"
    mocked_load.assert_called_once()


@pytest.mark.parametrize("env,expected_api_host", [("Dev", "localhost"), ("Prod", "mock.production.host")])
def test_read_config_parameterized(env, expected_api_host, mock_toml_load):
    if env == "Dev":
        mock_toml_load.return_value = MOCK_TOML_DATA_DEV
    elif env == "Prod":
        mock_toml_load.return_value = MOCK_TOML_DATA_PROD

    ctx = Context.read_config(env=env)
    assert ctx.api_host == expected_api_host


def test_configure_logging_with_defaults(mocker):
    mock_basic_config = mocker.patch("camerametrics.utils.config.logging.basicConfig")
    mock_get_logger = mocker.patch("camerametrics.utils.config.logging.getLogger")

    configure_logging()

    mock_basic_config.assert_called_once()
    mock_get_logger.assert_called_once_with("")
