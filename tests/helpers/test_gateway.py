"""Define tests for the gateway local API helpers."""

from __future__ import annotations

import json
from typing import Any

import pytest
from aiohttp import ClientResponseError
from aresponses import ResponsesMockServer

from ecowitt2mqtt.helpers.gateway import async_get_soil_channel_names

TEST_GATEWAY_HOST = "192.168.1.2"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "live_data,soil_channel_names",
    [
        # Named channels from both soil sensor types (unnamed ones are omitted):
        (
            {
                "ch_soil": [{"channel": "1", "name": "", "humidity": "40%"}],
                "ch_ec": [
                    {"channel": "2", "name": "Trees", "ec": "680 uS/cm"},
                    {"channel": "4", "name": "", "ec": "60 uS/cm"},
                    {"channel": "5", "name": "Frontyard/Right", "ec": "40 uS/cm"},
                ],
            },
            {"2": "Trees", "5": "Frontyard/Right"},
        ),
        (
            {"ch_soil": [{"channel": "1", "name": "Garden", "humidity": "40%"}]},
            {"1": "Garden"},
        ),
        # A gateway with no soil sensors:
        ({"common_list": [], "rain": []}, {}),
    ],
)
async def test_get_soil_channel_names(
    aresponses: ResponsesMockServer,
    live_data: dict[str, Any],
    soil_channel_names: dict[str, str],
) -> None:
    """Test getting soil channel names from a gateway.

    Args:
        aresponses: An aresponses server.
        live_data: The gateway's live data response.
        soil_channel_names: The expected soil channel names.
    """
    aresponses.add(
        TEST_GATEWAY_HOST,
        "/get_livedata_info",
        "get",
        # The gateway labels its JSON as text/html:
        aresponses.Response(text=json.dumps(live_data), content_type="text/html"),
    )
    assert await async_get_soil_channel_names(TEST_GATEWAY_HOST) == soil_channel_names


@pytest.mark.asyncio
async def test_get_soil_channel_names_http_error(
    aresponses: ResponsesMockServer,
) -> None:
    """Test that an HTTP error from the gateway is raised.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        TEST_GATEWAY_HOST,
        "/get_livedata_info",
        "get",
        aresponses.Response(text="Not Found", status=404),
    )
    with pytest.raises(ClientResponseError):
        await async_get_soil_channel_names(TEST_GATEWAY_HOST)
