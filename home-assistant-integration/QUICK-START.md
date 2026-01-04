# ⚡ Quick Start - AI Assistant in Home Assistant

Guida rapida per iniziare in 5 minuti.

## 🚀 Installazione Rapida

### 1. Copia il Componente

```bash
# Windows (PowerShell)
Copy-Item -Path "custom_components\ai_assistant" -Destination "C:\config\custom_components\" -Recurse

# Linux/Mac
cp -r custom_components/ai_assistant ~/.homeassistant/custom_components/

# Docker
# Monta il volume e copia nella cartella /config/custom_components/
```

### 2. Riavvia Home Assistant

- Vai su **Impostazioni** → **Sistema** → **Riavvia**

### 3. Aggiungi Integrazione

1. **Impostazioni** → **Dispositivi e servizi**
2. **+ Aggiungi integrazione**
3. Cerca **"AI Assistant"**
4. Configura e salva

## ✅ Verifica

Dovresti vedere queste entità:

- `sensor.ai_assistant_status`
- `sensor.ai_assistant_conversation_count`
- `sensor.ai_assistant_last_response`

## 🎯 Primo Test

Vai su **Impostazioni** → **Automazioni e scene** → **Servizi**:

1. Seleziona `ai_assistant.ask_question`
2. Inserisci: `"Ciao, funzioni?"`
3. Clicca **Chiama servizio**
4. Controlla `sensor.ai_assistant_last_response`

## 📚 Prossimi Passi

- 📖 Leggi la [Guida Completa](./GUIDA-INSTALLAZIONE.md)
- 🔌 Estendi con [API OpenAI](./examples/openai-integration-example.py)
- 🤖 Crea [Automazioni](./examples/automazioni.yaml)
- 🎨 Aggiungi [Card Dashboard](./examples/dashboard-card.yaml)

---

**Nota:** L'implementazione base è un template. Per usare un vero AI, estendi il codice con un'API reale.

