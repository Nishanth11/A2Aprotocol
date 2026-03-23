import json
import re
from typing import Dict, List
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from agents.material_calculating_agent.dummy_storage import get_product_details

load_dotenv()


class ProductionAssistantResponse(BaseModel):
    material_requirements: Dict[str, float]
    tools_used: List[str]


class MaterialCalculatingAgent:
    """Calculates total material requirements from recipe + batch count."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self, model: str = "mistral", verbose: bool = False):
        self.llm = ChatOllama(model=model)

    async def invoke(self, query: str) -> str:
        """Extract product + batch count from query, compute requirements directly."""
        product_match = re.search(r'product\s+([A-Za-z0-9]+)', query, re.IGNORECASE)
        product_name  = f"Product {product_match.group(1).upper()}" if product_match else "Product A"

        batch_match = re.search(r'(\d+)\s*batch', query, re.IGNORECASE)
        num_batches = int(batch_match.group(1)) if batch_match else 1

        recipe_json = get_product_details(product_name)
        if not recipe_json:
            return json.dumps({"material_requirements": {}, "tools_used": ["get_product_details"]})

        recipe = json.loads(recipe_json).get("recipe", [])
        material_requirements = {
            f"tank{item['tank_number']}_{item['material_name'].lower().replace(' ', '_')}": item["quantity"] * num_batches
            for item in recipe
        }

        result = {"material_requirements": material_requirements, "tools_used": ["get_product_details"]}
        try:
            return ProductionAssistantResponse(**result).model_dump_json()
        except Exception:
            return json.dumps(result)

    def __repr__(self) -> str:
        return f"MaterialCalculatingAgent(model='{self.llm.model}')"
