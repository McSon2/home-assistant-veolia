from homeassistant.helpers.entity import Entity

class VeoliaEntity(Entity):
    """Base class for Veolia sensors."""

    def __init__(self, coordinator, entry):
        self.coordinator = coordinator
        self.entry = entry
        self._state = None
        self._attributes = {}

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.entry.entry_id}_{self.name}"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    def _base_extra_state_attributes(self):
        """Return base state attributes."""
        return {
            "attribution": "Data provided by Veolia",
        }

    async def async_update(self):
        """Update the entity."""
        await self.coordinator.async_request_refresh()
