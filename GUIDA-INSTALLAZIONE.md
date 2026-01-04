# 🤖 Guida Completa: Integrazione AI Assistant in Home Assistant

Questa guida ti spiega come installare e configurare l'integrazione AI Assistant in Home Assistant.

## 📋 Indice

1. [Installazione del Componente Personalizzato](#installazione)
2. [Configurazione Iniziale](#configurazione)
3. [Estensione con API AI Reale](#estensione-api)
4. [Utilizzo e Servizi](#utilizzo)
5. [Automazioni e Esempi](#automazioni)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Installazione del Componente Personalizzato

### Metodo 1: Installazione Manuale (Raccomandato)

1. **Accedi alla cartella Home Assistant:**
   - Se usi Home Assistant OS/Supervised: `/config/custom_components/`
   - Se usi Home Assistant Core: `~/.homeassistant/custom_components/`
   - Se usi Docker: monta il volume e accedi a `/config/custom_components/`

2. **Copia la cartella del componente:**
   ```bash
   # Copia l'intera cartella ai_assistant
   cp -r home-assistant-integration/custom_components/ai_assistant /config/custom_components/
   ```

3. **Verifica la struttura:**
   ```
   /config/custom_components/ai_assistant/
   ├── __init__.py
   ├── config_flow.py
   ├── const.py
   ├── coordinator.py
   ├── manifest.json
   ├── sensor.py
   └── services.yaml
   ```

4. **Riavvia Home Assistant:**
   - Vai su **Impostazioni** → **Sistema** → **Riavvia**

### Metodo 2: Via HACS (Home Assistant Community Store)

**⚠️ Nota:** Per usare HACS, devi prima pubblicare questo componente su un repository GitHub pubblico.

1. **Crea un repository GitHub:**
   - Crea un nuovo repository su GitHub (es: `ai-assistant-ha`)
   - Carica tutti i file della cartella `custom_components/ai_assistant/`
   - Assicurati che la struttura sia: `custom_components/ai_assistant/...`

2. **Installa HACS** (se non l'hai già):
   - Segui la guida: https://hacs.xyz/docs/setup/download

3. **Aggiungi come repository personalizzato:**
   - Vai su **HACS** → **Integrazioni** → **⋮** (menu) → **Repository personalizzati**
   - Aggiungi l'URL del tuo repository GitHub (es: `https://github.com/TUO-USERNAME/ai-assistant-ha`)
   - Categoria: **Integrazione**

4. **Installa:**
   - Cerca "AI Assistant" in HACS
   - Clicca **Installa**

**💡 Raccomandazione:** Per un uso immediato, usa il **Metodo 1 (Installazione Manuale)** che non richiede un repository GitHub.

---

## ⚙️ Configurazione Iniziale

1. **Aggiungi l'integrazione:**
   - Vai su **Impostazioni** → **Dispositivi e servizi**
   - Clicca **+ Aggiungi integrazione**
   - Cerca **"AI Assistant"**

2. **Configurazione base:**
   - **Nome:** AI Assistant (o un nome personalizzato)
   - **Intervallo aggiornamento:** 30 secondi (default)
   - Clicca **Invia**

3. **Verifica l'installazione:**
   - Dovresti vedere le seguenti entità:
     - `sensor.ai_assistant_status` - Stato dell'assistente
     - `sensor.ai_assistant_conversation_count` - Numero di conversazioni
     - `sensor.ai_assistant_last_response` - Ultima risposta

---

## 🔌 Estensione con API AI Reale

L'implementazione attuale è un template. Per usare un vero assistente AI, modifica i file seguenti:

### Opzione 1: Integrazione OpenAI (ChatGPT)

#### 1. Aggiorna `manifest.json`:

```json
{
  "domain": "ai_assistant",
  "name": "AI Assistant Integration",
  "version": "1.0.0",
  "requirements": ["openai>=1.0.0"],
  "dependencies": [],
  "codeowners": [],
  "documentation": "https://github.com/home-assistant/core",
  "iot_class": "local_polling",
  "config_flow": true
}
```

#### 2. Modifica `coordinator.py`:

```python
"""Data update coordinator for AI Assistant."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from openai import OpenAI

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class AIAssistantCoordinator(DataUpdateCoordinator):
    """Class to manage fetching AI Assistant data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_UPDATE_INTERVAL,
        )
        self.entry = entry
        self.conversation_count = 0
        self.last_response = "Ready"
        self.status = "online"
        self.available = True
        
        # Inizializza OpenAI client
        api_key = entry.data.get("api_key")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            _LOGGER.warning("OpenAI API key not configured")

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from AI Assistant."""
        try:
            data = {
                "status": self.status,
                "last_response": self.last_response,
                "conversation_count": self.conversation_count,
                "available": self.available,
                "last_update": datetime.now().isoformat(),
            }
            
            return data
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with AI Assistant: {err}")

    async def ask_question(self, question: str) -> str:
        """Ask a question to the AI assistant."""
        if not self.client:
            return "API key not configured"
        
        try:
            response = await self.hass.async_add_executor_job(
                self._call_openai, question
            )
            self.conversation_count += 1
            self.last_response = response
            self.async_update_listeners()
            return response
        except Exception as err:
            _LOGGER.error(f"Error calling OpenAI: {err}")
            return f"Error: {str(err)}"
    
    def _call_openai(self, question: str) -> str:
        """Call OpenAI API (runs in executor)."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant integrated with Home Assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
```

#### 3. Aggiorna `config_flow.py` per richiedere l'API key:

```python
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="AI Assistant"): str,
        vol.Required("api_key"): str,  # Aggiungi questo
        vol.Optional("update_interval", default=30): int,
    }
)
```

#### 4. Aggiorna `__init__.py` per usare il metodo async:

```python
async def handle_ask_question(call: ServiceCall) -> None:
    """Handle the ask question service."""
    question = call.data.get("question", "")
    _LOGGER.info(f"Question received: {question}")
    
    # Chiama l'API AI reale
    response = await coordinator.ask_question(question)
    
    hass.bus.async_fire(
        "ai_assistant_response",
        {"question": question, "response": response}
    )
```

### Opzione 2: Integrazione con API REST Personalizzata

Se preferisci usare un'altra API AI, modifica il metodo `ask_question` in `coordinator.py`:

```python
async def ask_question(self, question: str) -> str:
    """Ask a question to the AI assistant."""
    import aiohttp
    
    api_url = self.entry.data.get("api_url", "https://api.example.com/chat")
    api_key = self.entry.data.get("api_key")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": question,
        "context": "home_assistant"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                answer = data.get("response", "No response")
                self.conversation_count += 1
                self.last_response = answer
                self.async_update_listeners()
                return answer
            else:
                error = f"API error: {response.status}"
                _LOGGER.error(error)
                return error
```

---

## 🎯 Utilizzo e Servizi

### Servizi Disponibili

L'integrazione fornisce due servizi:

#### 1. `ai_assistant.ask_question`

Chiedi una domanda all'assistente AI.

**Parametri:**
- `question` (obbligatorio): La domanda da fare

**Esempio in YAML:**
```yaml
service: ai_assistant.ask_question
data:
  question: "Qual è la temperatura attuale in casa?"
```

**Esempio in Developer Tools:**
1. Vai su **Impostazioni** → **Automazioni e scene** → **Servizi**
2. Seleziona `ai_assistant.ask_question`
3. Inserisci nel campo `question`: `"Che tempo fa oggi?"`
4. Clicca **Chiama servizio**

#### 2. `ai_assistant.reset`

Resetta il contatore delle conversazioni.

**Esempio:**
```yaml
service: ai_assistant.reset
```

### Eventi

L'integrazione emette eventi quando riceve una risposta:

**Evento:** `ai_assistant_response`

**Dati:**
```json
{
  "question": "La tua domanda",
  "response": "La risposta dell'AI"
}
```

**Esempio di listener:**
```yaml
automation:
  - alias: "Log AI Responses"
    trigger:
      - platform: event
        event_type: ai_assistant_response
    action:
      - service: system_log.write
        data:
          message: "AI risposta: {{ trigger.event.data.response }}"
```

---

## 🤖 Automazioni e Esempi

### Esempio 1: Assistente Vocale con Assist

```yaml
automation:
  - alias: "AI Assistant via Assist"
    trigger:
      - platform: conversation
        command: 
          - "chiedi all'assistente"
          - "domanda all'AI"
    action:
      - service: ai_assistant.ask_question
        data:
          question: "{{ trigger.slots.question }}"
      - service: tts.google_say
        data:
          entity_id: media_player.speaker
          message: "{{ states('sensor.ai_assistant_last_response') }}"
```

### Esempio 2: Risposta Automatica a Domande su Sensori

```yaml
automation:
  - alias: "AI risponde su temperatura"
    trigger:
      - platform: conversation
        command: "qual è la temperatura"
    action:
      - service: ai_assistant.ask_question
        data:
          question: >
            La temperatura attuale è {{ states('sensor.temperatura_soggiorno') }} gradi.
            Spiega questo valore in modo semplice.
      - delay: "00:00:02"
      - service: notify.mobile_app
        data:
          message: "{{ states('sensor.ai_assistant_last_response') }}"
```

### Esempio 3: Dashboard con Chat

Crea una card personalizzata per interagire con l'AI:

```yaml
type: entities
title: AI Assistant
entities:
  - entity: sensor.ai_assistant_status
  - entity: sensor.ai_assistant_conversation_count
  - type: button
    name: "Fai una domanda"
    tap_action:
      action: call-service
      service: ai_assistant.ask_question
      service_data:
        question: "Come posso risparmiare energia oggi?"
```

### Esempio 4: Script Interattivo

```yaml
script:
  chiedi_all_ai:
    alias: "Chiedi all'AI Assistant"
    sequence:
      - service: ai_assistant.ask_question
        data:
          question: "{{ question }}"
      - wait_template: "{{ states('sensor.ai_assistant_last_response') != 'Ready' }}"
      - service: notify.telegram
        data:
          message: >
            Domanda: {{ question }}
            Risposta: {{ states('sensor.ai_assistant_last_response') }}
```

---

## 🔧 Troubleshooting

### Problema: L'integrazione non appare

**Soluzione:**
1. Verifica che la cartella sia in `/config/custom_components/ai_assistant/`
2. Controlla i log: **Impostazioni** → **Sistema** → **Log**
3. Cerca errori di sintassi Python
4. Riavvia Home Assistant

### Problema: I servizi non funzionano

**Soluzione:**
1. Verifica che l'integrazione sia configurata correttamente
2. Controlla i log per errori
3. Verifica che `services.yaml` sia presente

### Problema: L'API AI non risponde

**Soluzione:**
1. Verifica che l'API key sia corretta
2. Controlla la connessione internet
3. Verifica i log per dettagli sull'errore
4. Testa l'API manualmente (curl, Postman, ecc.)

### Problema: Le entità non si aggiornano

**Soluzione:**
1. Verifica l'intervallo di aggiornamento nella configurazione
2. Controlla che il coordinator funzioni correttamente
3. Forza un refresh: **Impostazioni** → **Dispositivi e servizi** → **AI Assistant** → **Aggiorna**

---

## 📚 Risorse Aggiuntive

- [Documentazione Home Assistant Custom Components](https://developers.home-assistant.io/docs/creating_component_index/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## 🎉 Prossimi Passi

1. ✅ Installa il componente personalizzato
2. ✅ Configura l'integrazione
3. ✅ Estendi con un'API AI reale
4. ✅ Crea automazioni personalizzate
5. ✅ Aggiungi al tuo dashboard

Buon divertimento con il tuo AI Assistant in Home Assistant! 🚀

