"""Test the main entrypoint."""

from __future__ import annotations

import os
from unittest.mock import patch

from ecowitt2mqtt.__main__ import get_cli_arguments, get_env_vars, main
from ecowitt2mqtt.const import (
    CONF_GATEWAY_HOST,
    CONF_MQTT_BROKER,
    CONF_MQTT_TOPIC,
    CONF_SENSOR_NAME_MAP,
    CONF_VERBOSE,
    ENV_SENSOR_NAME_MAP,
    ENV_VERBOSE,
)


def test_get_cli_arguments() -> None:
    """Test getting all set CLI arguments."""
    cli_arguments = get_cli_arguments(
        [
            "--mqtt-broker",
            "127.0.0.1",
            "--mqtt-topic",
            "Test",
            "--gateway-host",
            "192.168.1.2",
        ]
    )
    assert cli_arguments == {
        CONF_GATEWAY_HOST: "192.168.1.2",
        CONF_MQTT_BROKER: "127.0.0.1",
        CONF_MQTT_TOPIC: "Test",
    }


def test_get_env_vars() -> None:
    """Test getting all set environment variables."""
    os.environ[ENV_VERBOSE] = "TRUE"
    os.environ[ENV_SENSOR_NAME_MAP] = "tempin=Indoor Temp"
    env_vars = get_env_vars()
    assert env_vars == {
        CONF_SENSOR_NAME_MAP: "tempin=Indoor Temp",
        CONF_VERBOSE: "TRUE",
    }
    os.environ.pop(ENV_VERBOSE)
    os.environ.pop(ENV_SENSOR_NAME_MAP)


def test_main() -> None:
    """Test the main entrypoint.

    This is effectively a quick sanity check to ensure that the CLI doesn't blow up.
    """
    with patch(
        "sys.argv",
        [
            "ecowitt2mqtt",
            "--mqtt-broker",
            "127.0.0.1",
            "--mqtt-topic",
            "Test",
            "--diagnostics",
        ],
    ), patch("ecowitt2mqtt.core.Ecowitt.async_start"):
        main()
