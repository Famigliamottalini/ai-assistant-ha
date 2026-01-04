# 🤖 AI Assistant Integration per Home Assistant

Integrazione personalizzata per aggiungere un assistente AI a Home Assistant.

## 📦 Cosa Include

- ✅ Componente personalizzato completo
- ✅ Config flow per setup guidato
- ✅ Sensori per stato e statistiche
- ✅ Servizi per interagire con l'AI
- ✅ Eventi per automazioni
- ✅ Esempi di automazioni e dashboard

## 🚀 Quick Start

### 1. Installazione

Copia la cartella `custom_components/ai_assistant` nella tua installazione Home Assistant:

```bash
# Per Home Assistant OS/Supervised
cp -r custom_components/ai_assistant /config/custom_components/

# Riavvia Home Assistant
```

### 2. Configurazione

1. Vai su **Impostazioni** → **Dispositivi e servizi**
2. Clicca **+ Aggiungi integrazione**
3. Cerca **"AI Assistant"**
4. Configura e salva

### 3. Utilizzo Base

```yaml
# Chiedi una domanda
service: ai_assistant.ask_question
data:
  question: "Qual è la temperatura attuale?"
```

## 📚 Documentazione Completa

Vedi [GUIDA-INSTALLAZIONE.md](./GUIDA-INSTALLAZIONE.md) per:
- Installazione dettagliata
- Estensione con API AI reali (OpenAI, ecc.)
- Esempi avanzati
- Troubleshooting

## 📁 Struttura

```
home-assistant-integration/
├── custom_components/
│   └── ai_assistant/          # Componente principale
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── manifest.json
│       ├── sensor.py
│       └── services.yaml
├── examples/                   # Esempi pratici
│   ├── automazioni.yaml
│   ├── dashboard-card.yaml
│   └── script.yaml
├── GUIDA-INSTALLAZIONE.md     # Guida completa
└── README.md                  # Questo file
```

## 🎯 Funzionalità

### Servizi

- `ai_assistant.ask_question` - Fai una domanda all'AI
- `ai_assistant.reset` - Reset contatore conversazioni

### Sensori

- `sensor.ai_assistant_status` - Stato dell'assistente
- `sensor.ai_assistant_conversation_count` - Numero conversazioni
- `sensor.ai_assistant_last_response` - Ultima risposta

### Eventi

- `ai_assistant_response` - Emesso quando l'AI risponde

## 🔌 Estensione con API Reale

L'implementazione attuale è un template. Per usare un'API AI reale:

1. Modifica `manifest.json` per aggiungere le dipendenze
2. Aggiorna `coordinator.py` con la logica API
3. Aggiungi l'API key in `config_flow.py`

Vedi la [Guida Completa](./GUIDA-INSTALLAZIONE.md#estensione-api) per dettagli.

## 📝 Esempi

Vedi la cartella `examples/` per:
- Automazioni pronte all'uso
- Card dashboard personalizzate
- Script interattivi

## 🐛 Problemi?

Consulta la sezione [Troubleshooting](./GUIDA-INSTALLAZIONE.md#troubleshooting) nella guida completa.

## 📄 Licenza

Questo progetto è fornito "così com'è" per scopi educativi e personali.

---

**Nota:** Questa è un'implementazione base. Per usare un vero assistente AI, devi estendere il codice con un'API reale (OpenAI, Anthropic, ecc.).

