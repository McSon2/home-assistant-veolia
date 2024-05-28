import logging
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.entity import Entity

from .veolia_client import VeoliaClient

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]

    client = VeoliaClient(email=username, password=password)
    client.login()

    add_entities([VeoliaWaterSensor(client)], True)

class VeoliaWaterSensor(Entity):
    def __init__(self, client):
        self._client = client
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "Veolia Water Consumption"

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self._attributes

    def update(self):
        data_daily = self._client.update(month=False)
        self._state = data_daily["history"][0][1] if data_daily["history"] else None
        self._attributes["daily_consumption"] = data_daily["history"]
