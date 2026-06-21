import os

# Force Vertex AI routing and credential binding inside the app code itself
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    r"C:\Users\Lenovo\AppData\Roaming\gcloud\application_default_credentials.json"
)
os.environ["GOOGLE_CLOUD_PROJECT"] = "furniturestoreapp-446cd"
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "1"
os.environ["GEMINI_USE_VERTEXAI"] = "1"

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.mcp_server import execute_inventory_query
from app.skills.billing_skill import BillingSkill
from app.skills.collateral_skill import CollateralSkill


def structure_order(
    client_name: str,
    item_type: str,
    dimensions: str,
    quantity: int = 1,
    price_per_unit: float = 0.0,
) -> str:
    """
    Use this tool to process incoming raw order parameters into a clean, relational JSON format.

    Args:
        client_name: Name of the client
        item_type: Type of item being ordered
        dimensions: Dimensions or size specifications
        quantity: Number of items ordered
        price_per_unit: Price per individual unit
    """
    return BillingSkill.process_order_to_json(
        client_name, item_type, dimensions, quantity, price_per_unit
    )


def generate_collateral(order_json_str: str) -> str:
    """
    Use this tool to generate a formatted markdown receipt and a WhatsApp summary from structured JSON order data.

    Args:
        order_json_str: Structured JSON order data
    """
    receipt = CollateralSkill.generate_receipt(order_json_str)
    whatsapp = CollateralSkill.generate_whatsapp_summary(order_json_str)

    return f"State change saved securely. Here is your final collateral:\n\n=== Receipt ===\n{receipt}\n\n=== WhatsApp Summary ===\n{whatsapp}"


# Initialize the main coordinator agent
root_agent = Agent(
    name="traditionsync_coordinator",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are the main coordinator agent for TraditionSync. "
        "When a user gives an order instruction (e.g., 'Log a custom teakwood dining table for a customer'), you MUST follow this workflow:\n"
        "1. Query the inventory database using `execute_inventory_query` to check stock parameters for the item category.\n"
        "2. Once inventory is confirmed, pass the order parameters to `structure_order` (BillingSkill) to cleanly format the data.\n"
        "3. Finally, pass the structured JSON order data to `generate_collateral` (CollateralSkill) to produce the final receipt and WhatsApp summary, which inherently saves the state safely.\n"
        "Always present the final generated collateral to the user."
    ),
    tools=[execute_inventory_query, structure_order, generate_collateral],
)

app = App(
    root_agent=root_agent,
    name="app",
)
