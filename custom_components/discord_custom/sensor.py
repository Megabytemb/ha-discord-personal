"""Sensor platform for discord_custom."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity

from .const import ACTIVITY_ICON_MAP, DOMAIN
from .coordinator import DiscordDataUpdateCoordinator
from .entity import DiscordEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            DiscordActivitySensor(coordinator=coordinator),
            DiscordStatusSensor(coordinator=coordinator),
        ]
    )


class DiscordStatusSensor(DiscordEntity, SensorEntity):
    """discord_custom Sensor class."""

    def __init__(self, coordinator: DiscordDataUpdateCoordinator) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_name = f"{self.coordinator.data.name.capitalize()} Discord Status"

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        if member := self.coordinator.data:
            return member.status.value
        return None

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture to use in the frontend, if any."""
        if display_avatar := self.coordinator.data.display_avatar:
            return display_avatar.url
        return None

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        if member := self.coordinator.data:
            data = {
                "desktop_status": member.desktop_status.value,
                "mobile_status": member.mobile_status.value,
            }
            return data

        return {}

    @property
    def icon(self):
        """Return icon."""
        return "mdi:account"


class DiscordActivitySensor(DiscordEntity, SensorEntity):
    """discord_custom Sensor class."""

    def __init__(self, coordinator: DiscordDataUpdateCoordinator) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_name = f"{self.coordinator.data.name.capitalize()} Discord Activity"

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        if activity := self.coordinator.data.activity:
            return activity.name
        return None

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        if activity := self.coordinator.data.activity:
            data = activity.to_dict()

            if activity.type:
                data["type_str"] = activity.type.name
            return data

        return {}

    @property
    def icon(self):
        """Return iron."""
        if activity := self.coordinator.data.activity:
            return ACTIVITY_ICON_MAP.get(activity.type, "mdi:pencil")

        return "mdi:sleep"
