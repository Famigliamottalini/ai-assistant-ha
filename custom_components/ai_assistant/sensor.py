"""Sensor platform for AI Assistant."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTR_CONVERSATION_COUNT, ATTR_LAST_RESPONSE
from .coordinator import AIAssistantCoordinator

SENSOR_DESCRIPTIONS = (
    SensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:robot",
    ),
    SensorEntityDescription(
        key="conversation_count",
        name="Conversation Count",
        icon="mdi:message-text",
        native_unit_of_measurement="conversations",
    ),
    SensorEntityDescription(
        key="last_response",
        name="Last Response",
        icon="mdi:comment-text",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up AI Assistant sensor platform."""
    coordinator: AIAssistantCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        AIAssistantSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class AIAssistantSensor(CoordinatorEntity, SensorEntity):
    """Representation of an AI Assistant sensor."""

    def __init__(
        self,
        coordinator: AIAssistantCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{description.key}"
        self._attr_name = f"AI Assistant {description.name}"

    @property
    def native_value(self) -> str | int:
        """Return the state of the sensor."""
        data = self.coordinator.data
        key = self.entity_description.key
        
        if key == "status":
            return data.get("status", "unknown")
        elif key == "conversation_count":
            return data.get("conversation_count", 0)
        elif key == "last_response":
            return data.get("last_response", "No response yet")
        
        return "unknown"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        data = self.coordinator.data
        return {
            "last_update": data.get("last_update"),
            "available": data.get("available", True),
        }

