import codecs
import json
import sys
import re

# Force utf-8 encoding for Windows terminals to print emojis correctly
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")


def structure_order(
    client_name: str,
    item_type: str,
    dimensions: str,
    quantity: int = 1,
    price_per_unit: float = 0.0,
) -> str:
    total_price = quantity * price_per_unit
    return json.dumps(
        {
            "client": {"name": client_name},
            "order": {
                "item_type": item_type,
                "specifications": {"dimensions": dimensions},
                "pricing": {
                    "quantity": quantity,
                    "price_per_unit": price_per_unit,
                    "total_price": total_price,
                    "currency": "USD",
                },
            },
            "status": "processed",
        },
        indent=2,
    )


def generate_collateral(order_json_str: str) -> str:
    data = json.loads(order_json_str)
    client_name = data["client"]["name"]
    item_type = data["order"]["item_type"]
    dimensions = data["order"]["specifications"]["dimensions"]
    quantity = data["order"]["pricing"]["quantity"]
    total_price = data["order"]["pricing"]["total_price"]

    receipt = (
        f"# Order Receipt\n"
        f"**Client:** {client_name}\n\n"
        f"## Order Details\n"
        f"- **Item:** {item_type}\n"
        f"- **Dimensions:** {dimensions}\n"
        f"- **Quantity:** {quantity}\n\n"
        f"## Pricing Summary\n"
        f"**Total Amount Due:** {total_price:.2f} USD\n\n"
        f"*Thank you for your business!*\n"
    )

    whatsapp = (
        f"Hello {client_name}! 👋\n\n"
        f"Here is a quick summary of your order:\n"
        f"🛒 *Item:* {item_type}\n"
        f"💰 *Total:* {total_price:.2f} USD\n\n"
        f"Let us know if you have any questions! Thank you! ✨"
    )

    return f"State change saved securely. Here is your final collateral:\n\n=== Receipt ===\n{receipt}\n\n=== WhatsApp Summary ===\n{whatsapp}"


def execute_inventory_query(item_category: str, item_name: str) -> str:
    return f"Inventory query results for '{item_category}':\n[{{'id': 101, 'name': '{item_name}', 'stock': 12}}]"


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Log a custom teakwood dining table for client Ram Sharma, size 6x3 feet, check furniture inventory records, and create the invoice summary"
    
    # Simple regex extraction for dynamic mock testing
    client_match = re.search(r"client (.*?),", prompt)
    client_name = client_match.group(1) if client_match else "Valued Client"
    
    item_match = re.search(r"Log a (.*?) for", prompt)
    item_type = item_match.group(1) if item_match else "custom furniture"
    
    dim_match = re.search(r"size (.*?),", prompt)
    dimensions = dim_match.group(1) if dim_match else "N/A"
    
    # Dynamic pricing simulation
    price = 2200.0 if "wardrobe" in item_type.lower() else 1500.0

    print("Sending order instruction to coordinator agent...")
    print(f"> {prompt}\n")
    print("========== AGENT EVENTS ==========")

    print("[Agent] Calling tool 'execute_inventory_query' with category='furniture'")
    print(f"[Tool Response] {execute_inventory_query('furniture', item_type)}\n")

    print("[Agent] Calling tool 'structure_order'")
    structured = structure_order(client_name, item_type, dimensions, 1, price)
    print(f"[Tool Response]\n{structured}\n")

    print("[Agent] Calling tool 'generate_collateral'")
    final = generate_collateral(structured)
    print(f"[Final Output]\n{final}")
