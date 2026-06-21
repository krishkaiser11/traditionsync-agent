import json
from typing import Dict, Any

class BillingSkill:
    """
    Skill for processing raw order parameters into a structured JSON order object.
    """
    
    @staticmethod
    def process_order_to_json(
        client_name: str, 
        item_type: str, 
        dimensions: str, 
        quantity: int = 1, 
        price_per_unit: float = 0.0
    ) -> str:
        """
        Takes incoming user parameters and structures them into a clean relational JSON object for processing.
        
        Args:
            client_name (str): Name of the client.
            item_type (str): The type of item being ordered.
            dimensions (str): Dimensions or size specifications of the item.
            quantity (int): Number of items ordered. Defaults to 1.
            price_per_unit (float): The cost of a single unit. Defaults to 0.0.
            
        Returns:
            str: A JSON string representing the structured order data.
        """
        total_price = quantity * price_per_unit
        
        order_data = {
            "client": {
                "name": client_name
            },
            "order": {
                "item_type": item_type,
                "specifications": {
                    "dimensions": dimensions
                },
                "pricing": {
                    "quantity": quantity,
                    "price_per_unit": price_per_unit,
                    "total_price": total_price,
                    "currency": "USD"
                }
            },
            "status": "processed"
        }
        
        return json.dumps(order_data, indent=2)
