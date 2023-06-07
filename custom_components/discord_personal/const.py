"""Constants for discord_personal."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

################################
# Do not change! Will be set by release workflow
INTEGRATION_VERSION = "main"  # git tag will be used
MIN_REQUIRED_HA_VERSION = "0.0.0"  # set min required version in hacs.json
################################

NAME = "Discord Personal"
DOMAIN = "discord_personal"
ATTRIBUTION = "Data provided by Discord"

PY_DISCORD_BOT = DOMAIN + "_bot"

CONF_BOT_TOKEN = "bot_token"
CONF_USER_ID = "user_id"
CONF_GUILD_ID = "guild_id"
