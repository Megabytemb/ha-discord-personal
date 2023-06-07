"""Discord client module."""
import asyncio
from collections import defaultdict
import logging

import discord

_LOGGER = logging.getLogger(__name__)


class DiscordClient(discord.Client):
    """A client for interacting with Discord API."""

    def __init__(self, *args, **kwargs):
        """Initialize the DiscordClient."""
        super().__init__(*args, **kwargs)
        self.future_ready = asyncio.Future()
        self.event_handlers = defaultdict(list)
        self._ready_fired = False

    async def on_ready(self):
        """Event handler for the client's 'ready' event."""
        _LOGGER.info(f"Logged in as {self.user} (ID: {self.user.id})")
        _LOGGER.info("------")

    def dispatch(self, event, *args, **kwargs):
        """Dispatch an event and call its associated event handlers."""
        super().dispatch(event, *args, **kwargs)
        _LOGGER.debug(f"Dispatching event {event}")
        method = "on_" + event

        if event == "ready" and not self._ready_fired:
            self.future_ready.set_result(True)
            self._ready_fired = True

        for coro in self.event_handlers[event]:
            self._schedule_event(coro, method, *args, **kwargs)

    def bind(self, event: str, coro):
        """Bind an event to a coroutine as its event handler."""

        self.event_handlers[event].append(coro)
