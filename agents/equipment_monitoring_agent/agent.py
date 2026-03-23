import asyncio
import json
from typing import Dict, List
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from agents.equipment_monitoring_agent.tools import material_availability_sync, machine_states_sync

load_dotenv()


class ProductionAssistantResponse(BaseModel):
    machine_states: Dict[str, str]
    material_availability: Dict[str, float]
    tools_used: List[str]


class EquipmentMonitoringAgent:
    """Returns material availability and machine states by calling tools directly."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self, model: str = "mistral", verbose: bool = False):
        self.llm = ChatOllama(model=model)

    async def invoke(self, query: str) -> str:
        """Call tools directly and return structured JSON."""
        loop = asyncio.get_running_loop()
        materials_str = await loop.run_in_executor(None, material_availability_sync)
        machines_str  = await loop.run_in_executor(None, machine_states_sync)

        try:
            materials = json.loads(materials_str)
            machines  = json.loads(machines_str)
        except Exception:
            materials, machines = {}, {}

        result = {
            "machine_states": machines,
            "material_availability": materials,
            "tools_used": ["get_material_availability", "get_machine_states"],
        }
        try:
            return ProductionAssistantResponse(**result).model_dump_json()
        except Exception:
            return json.dumps(result)

    def __repr__(self) -> str:
        return f"EquipmentMonitoringAgent(model='{self.llm.model}')"
