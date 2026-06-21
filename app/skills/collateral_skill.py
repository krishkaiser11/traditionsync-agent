import json


class CollateralSkill:
    """
    Skill for generating client-facing collateral like receipts or WhatsApp summaries
    from structured order data.
    """

    @staticmethod
    def generate_receipt(order_json_str: str) -> str:
        """
        Takes structured JSON order data and formats a polished markdown receipt.

        Args:
            order_json_str (str): JSON string containing processed order data.

        Returns:
            str: Formatted markdown string.
        """
        try:
            data = json.loads(order_json_str)
        except json.JSONDecodeError:
            return "Error: Invalid order data format."

        client_name = data.get("client", {}).get("name", "Valued Client")
        item_type = data.get("order", {}).get("item_type", "Item")
        dimensions = (
            data.get("order", {}).get("specifications", {}).get("dimensions", "N/A")
        )
        pricing = data.get("order", {}).get("pricing", {})

        quantity = pricing.get("quantity", 1)
        total_price = pricing.get("total_price", 0.0)
        currency = pricing.get("currency", "USD")

        receipt = (
            f"# Order Receipt\n"
            f"**Client:** {client_name}\n\n"
            f"## Order Details\n"
            f"- **Item:** {item_type}\n"
            f"- **Dimensions:** {dimensions}\n"
            f"- **Quantity:** {quantity}\n\n"
            f"## Pricing Summary\n"
            f"**Total Amount Due:** {total_price:.2f} {currency}\n\n"
            f"*Thank you for your business!*\n"
        )
        return receipt

    @staticmethod
    def generate_whatsapp_summary(order_json_str: str) -> str:
        """
        Takes structured JSON order data and formats a WhatsApp-friendly summary template.
        """
        try:
            data = json.loads(order_json_str)
        except json.JSONDecodeError:
            return "Error: Invalid order data format."

        client_name = data.get("client", {}).get("name", "Valued Client")
        item_type = data.get("order", {}).get("item_type", "Item")
        pricing = data.get("order", {}).get("pricing", {})

        total_price = pricing.get("total_price", 0.0)
        currency = pricing.get("currency", "USD")

        message = (
            f"Hello {client_name}! 👋\n\n"
            f"Here is a quick summary of your order:\n"
            f"🛒 *Item:* {item_type}\n"
            f"💰 *Total:* {total_price:.2f} {currency}\n\n"
            f"Let us know if you have any questions! Thank you! ✨"
        )
        return message
