import json
import os
from homeassistant.helpers.entity import Entity
from veolia_client import VeoliaClient

def setup_platform(hass, config, add_entities, discovery_info=None):
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    client = VeoliaClient(email=username, password=password)
    client.login()

    add_entities([VeoliaDailyConsumptionSensor(client), VeoliaMonthlyConsumptionSensor(client)], True)

class VeoliaDailyConsumptionSensor(Entity):
    def __init__(self, client):
        self._client = client
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return 'Veolia Daily Consumption'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self._attributes

    def update(self):
        data = self._client.update(month=False)
        if data:
            self._state = data['history'][0][1] if data['history'] else None
            self._attributes = {"history": data['history']}

class VeoliaMonthlyConsumptionSensor(Entity):
    def __init__(self, client):
        self._client = client
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return 'Veolia Monthly Consumption'

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        return self._attributes

    def update(self):
        data = self._client.update(month=True)
        if data:
            self._state = data['history'][0][1] if data['history'] else None
            self._attributes = {"history": data['history']}
