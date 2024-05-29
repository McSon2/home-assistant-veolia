"""Sensor platform for Veolia."""

import logging
from homeassistant.components.sensor import SensorStateClass
from .const import DAILY, DOMAIN, HISTORY, MONTHLY
from .entity import VeoliaEntity
from veolia_client import VeoliaClient

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    client = VeoliaClient(email=username, password=password)
    client.login()

    add_entities([VeoliaDailyConsumptionSensor(client), VeoliaMonthlyConsumptionSensor(client)], True)

class VeoliaLastIndexSensor(VeoliaEntity):
    """Monitors the last index."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return "veolia_last_index"

    @property
    def state_class(self):
        """Return the state_class of the sensor."""
        _LOGGER.debug(f"state_class = {SensorStateClass.TOTAL_INCREASING}")
        return SensorStateClass.TOTAL_INCREASING

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data['last_index']}")
        state = self.coordinator.data["last_index"]
        if state > 0:
            return state
        return None

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        return self._base_extra_state_attributes()


class VeoliaDailyConsumptionSensor(VeoliaEntity):
    """Monitors the daily water usage."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return "veolia_daily_consumption_test"

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data[DAILY]}")
        state = self.coordinator.data[DAILY][HISTORY][0][1]
        if state > 0:
            return state
        return None

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        _LOGGER.debug(f"Daily : self.coordinator.data = {self.coordinator.data[DAILY]}")
        attrs = self._base_extra_state_attributes() | {
            "historyConsumption": self.coordinator.data[DAILY][HISTORY],
        }
        return attrs


class VeoliaMonthlyConsumptionSensor(VeoliaEntity):
    """Monitors the monthly water usage."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return "veolia_monthly_consumption_test"

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data[MONTHLY]}")
        state = self.coordinator.data[MONTHLY][HISTORY][0][1]
        if state > 0:
            return state
        return None

    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        _LOGGER.debug(f"Monthly : self.coordinator.data = {self.coordinator.data[MONTHLY]}")
        attrs = self._base_extra_state_attributes() | {
            "historyConsumption": self.coordinator.data[MONTHLY][HISTORY],
        }
        return attrs
