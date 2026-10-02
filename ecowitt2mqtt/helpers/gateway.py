"""Define helpers to query an Ecowitt gateway's local API."""

from __future__ import annotations

from aiohttp import ClientSession, ClientTimeout

DEFAULT_TIMEOUT = 10

# The live data lists whose sensors share the soil channel space:
SOIL_CHANNEL_LISTS = ("ch_soil", "ch_ec")


async def async_get_soil_channel_names(host: str) -> dict[str, str]:
    """Get the names assigned to soil channels on a gateway.

    Args:
        host: The hostname or IP address of the gateway.

    Returns:
        A dictionary of channel numbers to names (unnamed channels are omitted).
    """
    async with ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT)) as session:
        async with session.get(f"http://{host}/get_livedata_info") as response:
            response.raise_for_status()
            # The gateway labels its JSON as text/html:
            data = await response.json(content_type=None)

    return {
        sensor["channel"]: sensor["name"]
        for channel_list in SOIL_CHANNEL_LISTS
        for sensor in data.get(channel_list, [])
        if sensor["name"]
    }
