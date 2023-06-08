"""Constants for discord_custom."""
from logging import Logger, getLogger

from discord import ActivityType

LOGGER: Logger = getLogger(__package__)

################################
# Do not change! Will be set by release workflow
INTEGRATION_VERSION = "main"  # git tag will be used
MIN_REQUIRED_HA_VERSION = "0.0.0"  # set min required version in hacs.json
################################

NAME = "Discord Custom"
DOMAIN = "discord_custom"
ATTRIBUTION = "Data provided by Discord"

PY_DISCORD_BOT = DOMAIN + "_bot"

CONF_BOT_TOKEN = "bot_token"
CONF_USER_ID = "user_id"
CONF_GUILD_ID = "guild_id"

ACTIVITY_ICON_MAP = {
    ActivityType.competing: "mdi:football",
    ActivityType.playing: "mdi:controller",
    ActivityType.streaming: "mdi:twitch",
    ActivityType.listening: "mdi:music",
    ActivityType.watching: "mdi:youtube-tv",
    ActivityType.custom: "mdi:pencil",
}
