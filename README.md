# Unifi-Video Controller Metrics Collector

This is a utility that fetches camera metrics from the UnifiVideo Controller and exposes them as Prometheus metrics.

The metrics generated are:
- name: The camera's name as configured on the NVR
- model: The model reported by the camera
- cpu_load: Camera's CPU load as reported by the controller
- memory_used: Camera's memory usage as reported by the controller
- memory_total: Camera's total memory available as reported by the controller
- host: Camera's IP address
- mac: Camera's MAC address
- firmware_version: Firmware version as reported by the camera
- managed: Is the camera managed by this controller? 0 = No, 1 = Yes
- last_seen: When the camera was last seen by the controller. 
- state: Camera state as reported by the controller
- last_recording_start_time: When the last recording of this camera's footage started

## Prerequisites

- Python 3.8+
- A Unifi-Video Controller running at least v3.10 to fetch metrics from.

### Optional
- [Poetry](https://python-poetry.org/docs/): Python packaging and dependency management tool.

## Installation and Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/kobuskc/unifi-video-metrics-collector.git
   cd unifi-video-metrics-collector
   ```

2. Install the project dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment created by Poetry:
   ```bash
   poetry shell
   ```

## Usage

1. Configure the application using a [TOML](https://toml.io/en/) file. Set your environment, API host, ports, and other necessary configurations.

### Configuration file example
```toml
[dev]
api_host = "123.123.123.123"
api_port = 7443
api_key = "your_api_key_goes_here"
http_port = 8088
refresh_rate = 10
push = true
gateway = "your_prometheus_push.gateway.address"
gateway_port = 443
job = "your_prometheus_job"
```

2. Run the metrics collector:
   ```bash
   poetry run python main.py
   ```
> Note, if you don't pass a config file using `--config` when you run main.py, it will expect to find a valid `.config.toml` in the current directory

### Optional Arguments

- `--config`: Specify a different config file to use (default is `.config.toml`).
- `--env`: Specify which environment to load from the config file (default is `Prod`).
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR). Default is the level specified in `constants.py`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## Running Tests

Tests ensure that the functionality of the collector remains consistent with expectations. We strongly recommend running tests after making any changes.

### Using Poetry

If you're using `poetry` to manage your project (recommended), you can run tests using:

```bash
poetry run pytest
```

This ensures that tests run within the virtual environment managed by `poetry`, using the dependencies specified in `pyproject.toml`.

### Using Python's -m flag

Alternatively, if you have `pytest` installed globally or in your current environment, you can use Python's `-m` flag to run the `pytest` module:

```bash
python -m pytest
```

### Expected output
If you're using the included `pyproject.toml` file, you can expect output similar to this for a successful test run:

```bash
========================================================================================================================================================================== test session starts ==========================================================================================================================================================================
platform darwin -- Python 3.11.4, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/kobusc/work/code/python/CameraMetrics
configfile: pyproject.toml
testpaths: tests
plugins: asyncio-0.21.1, mock-3.11.1, anyio-3.7.1
asyncio: mode=Mode.STRICT
collected 7 items

tests/test_config.py::test_read_config_with_missing_keys PASSED                                                                                                                         [ 14%]
tests/test_config.py::test_read_config_with_defaults PASSED                                                                                                                             [ 28%]
tests/test_config.py::test_read_config_parameterized[Dev-localhost] PASSED                                                                                                              [ 42%]
tests/test_config.py::test_read_config_parameterized[Prod-mock.production.host] PASSED                                                                                                  [ 57%]
tests/test_config.py::test_configure_logging_with_defaults PASSED                                                                                                                       [ 71%]
tests/test_main.py::test_get_cameras PASSED                                                                                                                                             [ 85%]
tests/test_main.py::test_extract_and_update_camera_metrics PASSED                                                                                                                       [100%]

========================================================================================================================================================================== 7 passed in 0.06s ==========================================================================================================================================================================
```
### Test Coverage

To check the test coverage, you can use `pytest-cov`. First, ensure you have it installed (it's likely specified in your `pyproject.toml` if you're using this repo as-is). Then, run:

```bash
poetry run pytest --cov=camerametrics
```

The result should be similar to:
```bash
========================================================================================================================================================================== test session starts ==========================================================================================================================================================================
platform darwin -- Python 3.11.4, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/kobusc/work/code/python/CameraMetrics
configfile: pyproject.toml
testpaths: tests
plugins: cov-4.1.0, asyncio-0.21.1, mock-3.11.1, anyio-3.7.1
asyncio: mode=Mode.STRICT
collected 7 items

tests/test_config.py::test_read_config_with_missing_keys PASSED                                                                                                                         [ 14%]
tests/test_config.py::test_read_config_with_defaults PASSED                                                                                                                             [ 28%]
tests/test_config.py::test_read_config_parameterized[Dev-localhost] PASSED                                                                                                              [ 42%]
tests/test_config.py::test_read_config_parameterized[Prod-mock.production.host] PASSED                                                                                                  [ 57%]
tests/test_config.py::test_configure_logging_with_defaults PASSED                                                                                                                       [ 71%]
tests/test_main.py::test_get_cameras PASSED                                                                                                                                             [ 85%]
tests/test_main.py::test_extract_and_update_camera_metrics PASSED                                                                                                                       [100%]

---------- coverage: platform darwin, python 3.11.4-final-0 ----------
Name                               Stmts   Miss  Cover
------------------------------------------------------
camerametrics/__init__.py              0      0   100%
camerametrics/main.py                115     56    51%
camerametrics/utils/__init__.py        0      0   100%
camerametrics/utils/config.py         29      2    93%
camerametrics/utils/constants.py       8      0   100%
------------------------------------------------------
TOTAL                                152     58    62%


========================================================================================================================================================================== 7 passed in 0.11s ==========================================================================================================================================================================
```

## License

[MIT](https://choosealicense.com/licenses/mit/)