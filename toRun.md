# How to Run — A2A Multi-Agent System

## Prerequisites

- Python 3.13 (required — Python 3.14 is not compatible with LangChain/Pydantic)
- [Ollama](https://ollama.com) running locally with the `mistral` model

---

## Step 1 — Install Ollama and Pull mistral

```bash
# Install Ollama (macOS)
brew install ollama

# Pull the mistral model
ollama pull mistral
```

---

## Step 2 — Create a Virtual Environment using Python 3.13

```bash
cd A2A

# Use python3.13 explicitly — do NOT use python3 (may point to 3.14)
python3.13 -m venv venv
```

Activate it:

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Verify .env File

A `.env` file should already exist in the `A2A` directory with:

```env
OLLAMA_BASE_URL=http://localhost:11434
```

No API key needed — everything runs locally.

---

## Step 5 — Start Ollama (Terminal 1)

```bash
ollama serve
```

---

## Step 6 — Start All Three Agent Servers (3 more terminals)

Each agent runs as an independent HTTP server. Open **3 terminals** from the `A2A` directory.

### Terminal 2 — Equipment Monitoring Agent (port 40002)

```bash
cd A2A
source venv/bin/activate        # Windows: venv\Scripts\activate
python3 -m agents.equipment_monitoring_agent
```

### Terminal 3 — Material Calculating Agent (port 40003)

```bash
cd A2A
source venv/bin/activate        # Windows: venv\Scripts\activate
python3 -m agents.material_calculating_agent
```

### Terminal 4 — Orchestrator Agent (port 40004)

```bash
cd A2A
source venv/bin/activate        # Windows: venv\Scripts\activate
python3 -m agents.orchestrator_agent
```

Wait until all three servers print that they are running before proceeding.

---

## Step 7 — Run the CLI Client (Terminal 5)

```bash
cd A2A
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### Talk to the Orchestrator (recommended)

```bash
python3 -m app.cmd --agent http://localhost:40004
```

### Talk directly to the Equipment Monitoring Agent

```bash
python3 -m app.cmd --agent http://localhost:40002
```

### Talk directly to the Material Calculating Agent

```bash
python3 -m app.cmd --agent http://localhost:40003
```

---

## Example Queries

```
Can I produce 100 batches of Product A?
Is it possible to produce 10 batches of Product B?
What is the current material availability and machine states?
Calculate materials needed for 5 batches of Product C
```

---

## Agent Ports Summary

| Agent                    | Port  | Description                                             |
| ------------------------ | ----- | ------------------------------------------------------- |
| EquipmentMonitoringAgent | 40002 | Reads tank levels and machine states                    |
| MaterialCalculatingAgent | 40003 | Calculates material requirements from recipes           |
| OrchestratorAgent        | 40004 | Routes queries to child agents and synthesizes response |

---

## Dummy Files (no real hardware needed)

| File                                                 | Replaces            |
| ---------------------------------------------------- | ------------------- |
| `agents/equipment_monitoring_agent/dummy_opc_ua.py`  | Real OPC UA server  |
| `agents/material_calculating_agent/dummy_storage.py` | PostgreSQL database |

To switch to real infrastructure, update the import comments in each agent's `tools.py`.

---

## Agent Registry

The orchestrator discovers child agents via [shared/a2a/agent_registry.json](shared/a2a/agent_registry.json):

```json
["http://localhost:40002", "http://localhost:40003"]
```

Update this file if your agents run on different hosts or ports.
