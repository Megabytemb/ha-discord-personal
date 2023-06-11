"""DataUpdateCoordinator for integration_blueprint."""
from __future__ import annotations

from datetime import timedelta
import logging

import discord

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_GUILD_ID, CONF_USER_ID, DOMAIN, LOGGER
from .discord_client import DiscordClient

_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class DiscordDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry
    data: discord.Member

    def __init__(
        self,
        hass: HomeAssistant,
        client: DiscordClient,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

        self.user_id = int(self.config_entry.data[CONF_USER_ID])
        self.guild_id = int(self.config_entry.data[CONF_GUILD_ID])
        self.app_info = {}

    async def on_member_update(self, before, after: discord.Member, *args, **kwargs):
        """Handle member update event."""
        if after.id == self.user_id:
            _LOGGER.info(after)
            self.data = after
            self.async_update_listeners()

    async def on_presence_update(self, before, after: discord.Member, *args, **kwargs):
        """Handle presence update event."""

        if after.id == self.user_id:
            _LOGGER.info(after.activity)
            self.data = after
            self.async_update_listeners()

    async def setup_listeners(self):
        """Set up event listeners."""

        self.client.bind("presence_update", self.on_presence_update)
        self.client.bind("member_update", self.on_member_update)

    async def _async_update_data(self):
        """Update data manually."""
        guild = self.client.get_guild(self.guild_id)
        member = guild.get_member(self.user_id)

        self.app_info = await self.client.get_detectable_applications()

        return member

    def async_get_icon_for_activity(self, activity: discord.Activity) -> str | None:
        """Get the app icon URL for a given Discord activity."""

        def get_icon_url(app):
            """Generate the URL for the app icon."""
            return f"https://cdn.discordapp.com/app-icons/{app['id']}/{app['icon']}.png"

        if hasattr(activity, "application_id"):
            app_id = activity.application_id
            discord_app = next(
                (app for app in self.app_info if app["id"] == str(app_id)), None
            )
            if discord_app:
                _LOGGER.debug("FOUND discord app by application_id = %s", discord_app)
                return get_icon_url(discord_app)

        discord_app_by_name = next(
            (app for app in self.app_info if app["name"] == str(activity.name)), None
        )
        if discord_app_by_name:
            _LOGGER.debug("FOUND discord app by name = %s", discord_app_by_name)
            return get_icon_url(discord_app_by_name)

        if hasattr(activity, "album_cover_url"):
            return activity.album_cover_url

        return None
