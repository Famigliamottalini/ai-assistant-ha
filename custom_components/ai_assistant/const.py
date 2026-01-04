"""Constants for AI Assistant integration."""
from typing import Final

DOMAIN: Final = "ai_assistant"
NAME: Final = "AI Assistant"

PLATFORMS: Final = ["sensor", "switch", "button"]

# Attributes
ATTR_STATUS: Final = "status"
ATTR_LAST_RESPONSE: Final = "last_response"
ATTR_CONVERSATION_COUNT: Final = "conversation_count"
ATTR_AVAILABLE: Final = "available"

# Services
SERVICE_ASK_QUESTION: Final = "ask_question"
SERVICE_RESET: Final = "reset"

# Defaults
DEFAULT_UPDATE_INTERVAL = 30  # seconds

