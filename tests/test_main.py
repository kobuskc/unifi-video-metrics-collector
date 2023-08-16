import pytest
from pytest_mock import MockerFixture

from camerametrics.main import extract_and_update_camera_metrics, get_cameras
from camerametrics.utils.config import Context

from .responses import CAMERA_VALID_RESPONSE, MOCK_METRICS, MOCK_TOML_DATA_DEV


@pytest.fixture
def mock_context(mocker: MockerFixture):
    # Mock the tomllib.load method
    mocked_load = mocker.patch("camerametrics.utils.config.tomllib.load", return_value=MOCK_TOML_DATA_DEV)

    return Context.read_config()


@pytest.fixture
async def mock_camera_data(mocker: MockerFixture, mock_context):
    # Mock the get_cameras function
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = CAMERA_VALID_RESPONSE

    # Use an async mock for the client's get function
    mock_client = mocker.MagicMock()
    mock_client.get = mocker.AsyncMock(return_value=mock_response)

    # Mock the __aenter__ and __aexit__ methods for the async context manager
    mock_async_context_manager = mocker.MagicMock()
    mock_async_context_manager.__aenter__.return_value = mock_client
    mock_async_context_manager.__aexit__ = mocker.AsyncMock(return_value=None)

    # Patch httpx.AsyncClient to return the mock_async_context_manager
    mocker.patch("httpx.AsyncClient", return_value=mock_async_context_manager)

    response = await get_cameras(mock_context)
    return response["data"]


@pytest.mark.asyncio
async def test_get_cameras(mocker, mock_context):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = CAMERA_VALID_RESPONSE

    # Use an async mock for the client's get function
    mock_client = mocker.MagicMock()
    mock_client.get = mocker.AsyncMock(return_value=mock_response)

    # Mock the __aenter__ and __aexit__ methods for the async context manager
    mock_async_context_manager = mocker.MagicMock()
    mock_async_context_manager.__aenter__.return_value = mock_client
    mock_async_context_manager.__aexit__ = mocker.AsyncMock(return_value=None)

    # Patch httpx.AsyncClient to return the mock_async_context_manager
    mocker.patch("httpx.AsyncClient", return_value=mock_async_context_manager)

    response = await get_cameras(mock_context)
    assert response == CAMERA_VALID_RESPONSE


@pytest.mark.asyncio
async def test_extract_and_update_camera_metrics(mocker, mock_camera_data, mock_context):
    camera_data = await mock_camera_data

    mock_registry = mocker.MagicMock()
    mock_metrics = {
        "g_name": mocker.MagicMock(),
        "g_model": mocker.MagicMock(),
        "g_cpu_load": mocker.MagicMock(),
        "g_memory_used": mocker.MagicMock(),
        "g_memory_total": mocker.MagicMock(),
        "g_host": mocker.MagicMock(),
        "g_mac": mocker.MagicMock(),
        "g_firmware_version": mocker.MagicMock(),
        "g_managed": mocker.MagicMock(),
        "g_last_seen": mocker.MagicMock(),
        "g_state": mocker.MagicMock(),
        "g_last_recording_start_time": mocker.MagicMock(),
    }

    # Mock the Prometheus metric updating functions
    for mock_metric in mock_metrics.values():
        mock_metric.labels.return_value = mock_metric
        mock_metric.info.return_value = None
        mock_metric.set.return_value = None

    # Mock logging
    mocker.patch("logging.info")
    mocker.patch("camerametrics.main.push_to_gateway", return_value=None)

    extract_and_update_camera_metrics(camera_data, mock_metrics, mock_context, mock_registry)

    # Assert the mock functions were called with the correct values
    for metric_name, (args, value) in MOCK_METRICS.items():
        mock_metrics[metric_name].labels.assert_called_with(**args[0])
        if isinstance(value, dict):
            mock_metrics[metric_name].info.assert_called_with(value)
        else:
            mock_metrics[metric_name].set.assert_called_with(value)
