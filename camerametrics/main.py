import argparse
import asyncio
import logging
import signal
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import httpx
import prometheus_client as prom
from prometheus_client import (
    GC_COLLECTOR,
    PLATFORM_COLLECTOR,
    PROCESS_COLLECTOR,
    REGISTRY,
    CollectorRegistry,
    Gauge,
    Info,
    push_to_gateway,
    start_http_server,
)
from utils.config import Context, configure_logging
from utils.constants import (
    API_URL_TEMPLATE,
    DEFAULT_LOG_LEVEL,
    MAX_RETRIES,
    RETRY_DELAY,
)


def extract_and_update_camera_metrics(
    camera_data: List[Dict[str, Any]], metrics: Dict[str, Any], ctx: Context, registry: CollectorRegistry
) -> None:
    """
    Extracts metric data from the json response received when calling the camera api.

    Parameters:
    - camera_data: Array of JSON objects, one per camera
    - metrics (dict): A dictionary containing the metrics we want to update
    - ctx (Context): Context containing config parameters
    - registry (CollectorRegistry): Prometheus collector registry to which metrics will be registered.
    """
    for camera in camera_data:
        name = camera.get("name", "")
        model = camera.get("model", "")
        cpu_load = camera.get("systemInfo", {}).get("cpuLoad", 0.0)
        memory_used = camera.get("systemInfo", {}).get("memory", {}).get("used", 0)
        memory_total = camera.get("systemInfo", {}).get("memory", {}).get("total", 0)

        host = camera.get("host", "")
        mac = camera.get("mac", "")
        firmware_version = camera.get("firmwareVersion", "")
        managed = str(camera.get("managed", "")).lower()
        last_seen = camera.get("lastSeen", "")
        state = camera.get("state", "")
        last_recording_start_time = camera.get("lastRecordingStartTime", "")

        # Update Prometheus metrics for each camera
        metrics["g_name"].labels(name=name).set(1 if name else 0)
        metrics["g_model"].labels(name=name).info({"camera_model": model})
        metrics["g_cpu_load"].labels(name=name).set(cpu_load)
        metrics["g_memory_used"].labels(name=name).set(memory_used)
        metrics["g_memory_total"].labels(name=name).set(memory_total)
        metrics["g_host"].labels(name=name).info({"camera_host": host})
        metrics["g_mac"].labels(name=name).info({"camera_mac": mac})
        metrics["g_firmware_version"].labels(name=name).info({"camera_firmware_version": firmware_version})
        metrics["g_managed"].labels(name=name).set(1 if managed else 0)
        metrics["g_last_seen"].labels(name=name).set(last_seen)
        metrics["g_state"].labels(name=name, state=state).set(1 if str.upper(state) == "CONNECTED" else 0)
        metrics["g_last_recording_start_time"].labels(name=name).set(last_recording_start_time)
        logging.info(f"Updated metrics for camera: {name}")

        # do we need to push metrics?
        if ctx.push:
            logging.info(f"Trying to push metrics to {ctx.gateway} on port {ctx.gateway_port} - job: {ctx.job}")
            try:
                push_to_gateway(gateway=f"{ctx.gateway}:{ctx.gateway_port}", job=ctx.job, registry=registry)
            except Exception as e:
                logging.error(f"Error: {e}")


async def fetch_and_update(ctx: Context, metrics: Dict[str, Any], registry: CollectorRegistry) -> None:
    """
    Calls get_cameras() to get a JSON response containing camera metrics, then sends that to be processed into
    updated metrics.

    This function loops until shutdown is requested.

    Parameters:
    - ctx (Context): Context containing config parameters.
    - metrics (dict): A dictionary containing the metrics we want to update.
    - registry (CollectorRegistry): Prometheus collector registry to which metrics will be registered.
    """
    while not shutdown_requested:
        response = await get_cameras(ctx)

        if "data" in response:
            extract_and_update_camera_metrics(response["data"], metrics, ctx, registry)

        await asyncio.sleep(ctx.refresh_rate)


async def get_cameras(ctx: Context) -> Union[Dict[str, Any], None]:
    """
    Makes the API call to the Unifi Video host. If the response doesn't contain camera data, it will retry up to
    MAX_RETRIES, waiting RETRY_DELAY seconds between each attemps. These are defined as constants - constants.py

    Parameters:
    - ctx (Context): Context containing config parameters.

    Returns:
    - dict: Dictionary containing created metrics.
    """
    url = API_URL_TEMPLATE.format(host=ctx.api_host, port=ctx.api_port, key=ctx.api_key)
    retries = 0

    while retries < MAX_RETRIES:
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logging.error(f"HTTP error while fetching camera data: {e}. Retrying in {RETRY_DELAY} seconds...")
            retries += 1
            await asyncio.sleep(RETRY_DELAY)

    logging.error(f"Failed to fetch camera data after {MAX_RETRIES} retries.")
    return None


def main() -> None:
    """
    Calls a function to process cli arguments, creates the configuration context and then kicks off the process
    based on the parameters provided.
    """
    global shutdown_requested  # We make it global so that the signal handler can modify it
    shutdown_requested = False  # This is set to True when SIGINT is received

    args = parse_args()
    log_level = getattr(logging, args.log_level.upper())
    configure_logging(log_level)
    ctx = Context().read_config(args.config, args.env)

    #  Create, and set up a single registry for all metrics
    registry = CollectorRegistry()
    metrics = setup_metrics(registry)

    # Are we going to push metrics to a push_gateway?
    if ctx.push:
        logging.info(f"Configured to push metrics to {ctx.gateway}:{ctx.gateway_port}")
        # Do we need a custom session with an HTTP proxy?
    else:
        logging.info(f"Starting web service on port {ctx.http_port}")
        start_http_server(ctx.http_port, registry=registry)

    loop = asyncio.get_event_loop()

    # Set up a signal handler for Ctrl+C (SIGINT)
    # This is a bit unconventional, but defining the funcion here in main() has some Pros:
    #  - we're encaptulating the logic related to signal handling within the context it is being used in
    #  - the sigint_handler has access to main's scope, should it be required
    def sigint_handler(signum, frame):
        global shutdown_requested
        logging.info(f"Signal {signum} detected. ")
        shutdown_requested = True

    signal.signal(signal.SIGINT, sigint_handler)

    try:
        logging.info(f"Fetching metrics from {ctx.api_host}")
        logging.info(f"Refreshing metrics every {ctx.refresh_rate} seconds")

        loop.run_until_complete(fetch_and_update(ctx, metrics, registry))

    except Exception as e:
        logging.exception(f"Error encountered: {e}")
    finally:
        shutdown(loop)


def parse_args() -> argparse.Namespace:
    """
    Processes command-line arguments, and provide defaults where required.

    Returns:
    - (argparse.Namespace): Dictionary containing created metrics.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="config file to use", default=".config.toml")
    parser.add_argument("--env", help="which environment to load from the config file", default="Prod")
    parser.add_argument("--log-level", help="logging level (DEBUG, INFO, WARNING, ERROR)", default=DEFAULT_LOG_LEVEL)
    return parser.parse_args()


def setup_metrics(registry: CollectorRegistry) -> Dict[str, Any]:
    """
    Set up Prometheus metrics and register them to the provided registry.

    Parameters:
    - registry (CollectorRegistry): Prometheus collector registry to which metrics will be registered.

    Returns:
    - dict: Dictionary containing created metrics.
    """

    REGISTRY.unregister(GC_COLLECTOR)
    REGISTRY.unregister(PLATFORM_COLLECTOR)
    REGISTRY.unregister(PROCESS_COLLECTOR)

    # Create Prometheus metrics with label 'name' to differentiate metrics for each camera
    metrics = {
        "g_name": Gauge("camera_name_available", "Is Camera Name available", ["name"], registry=registry),
        "g_model": Info("camera_model", "Camera Model", ["name"], registry=registry),
        "g_cpu_load": Gauge("camera_cpu_load", "Camera CPU Load Percentage", ["name"], registry=registry),
        "g_memory_used": Gauge("camera_memory_used_bytes", "Camera Memory Used in Bytes", ["name"], registry=registry),
        "g_memory_total": Gauge(
            "camera_memory_total_bytes", "Camera Total Memory in Bytes", ["name"], registry=registry
        ),
        "g_host": Info("camera_host", "Camera Host", ["name"], registry=registry),
        "g_mac": Info("camera_mac", "Camera MAC address", ["name"], registry=registry),
        "g_firmware_version": Info("camera_firmware_version", "Camera Firmware Version", ["name"], registry=registry),
        "g_managed": Gauge("camera_managed", "Is Camera Managed", ["name"], registry=registry),
        "g_last_seen": Gauge("camera_last_seen_timestamp", "Camera Last Seen Timestamp", ["name"], registry=registry),
        "g_state": Gauge("camera_state", "Camera State", ["name", "state"], registry=registry),
        "g_last_recording_start_time": Gauge(
            "camera_last_recording_start_time", "Camera Last Recording Start Time", ["name"], registry=registry
        ),
    }

    return metrics


def shutdown(loop: asyncio.AbstractEventLoop) -> None:
    """
    Performs a clean shutdown of the Event Loop.

    Parameters:
    - loop (asyncio.AbstractEventLoop): The Event Loop.
    """
    logging.info("Initiating graceful shutdown...")

    # Cancel all tasks in the event loop
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()

    # Run the event loop until all tasks are cancelled
    try:
        loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop=loop), return_exceptions=True))
    except asyncio.CancelledError:
        pass
    logging.info("Shutting down gracefully...")
    loop.stop()


if __name__ == "__main__":
    main()
