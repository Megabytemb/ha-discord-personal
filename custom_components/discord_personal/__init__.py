"""Custom integration to integrate discord_personal with Home Assistant.

For more details about this integration, please refer to
https://github.com/Megabytemb/ha-discord-personal
"""
from __future__ import annotations

import logging

import discord

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, Platform
from homeassistant.core import HomeAssistant

from .const import CONF_BOT_TOKEN, CONF_USER_ID, DOMAIN, PY_DISCORD_BOT
from .discord_client import DiscordClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    intents = discord.Intents.default()
    intents.members = True
    intents.presences = True

    token = entry.data[CONF_BOT_TOKEN]
    user_id = int(entry.data[CONF_USER_ID])
    discordBot = hass.data[PY_DISCORD_BOT] = DiscordClient(intents=intents)

    # await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    async def async_stop_server(event):
        await discordBot.close()

    entry.async_create_background_task(
        hass, discordBot.start(token), "Discord Websocket"
    )
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, async_stop_server)

    async def on_member_update(before, after: discord.Member, *args, **kwargs):
        if after.id == user_id:
            _LOGGER.info(after)

    async def on_presence_update(before, after: discord.Member, *args, **kwargs):
        if after.id == user_id:
            _LOGGER.info(after.activity)

    discordBot.bind("presence_update", on_presence_update)
    discordBot.bind("member_update", on_member_update)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
