import logging
import sys

from mcp.server.fastmcp import FastMCP

# Configure logging to write to stderr to avoid breaking MCP stdio protocol
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp_server")

# Initialize a standard FastMCP server
mcp = FastMCP("traditionsync-db-server")


@mcp.tool()
def execute_inventory_query(item_category: str) -> str:
    """
    Simulate a secure, parameterized SQL-like local relational query over an asset dataset.

    Args:
        item_category (str): The category of items to query.
    """
    logger.info(f"Executing secure inventory query for category: {item_category}")

    # Simulating a secure parameterized query
    # e.g., cursor.execute("SELECT id, name, stock FROM inventory WHERE category = ?", (item_category,))

    mock_database = {
        "furniture": [
            {"id": 101, "name": "Oak Dining Table", "stock": 12},
            {"id": 102, "name": "Leather Sofa", "stock": 5},
            {"id": 103, "name": "Ergonomic Office Chair", "stock": 34},
        ],
        "electronics": [
            {"id": 201, "name": "4K Monitor", "stock": 50},
            {"id": 202, "name": "Mechanical Keyboard", "stock": 120},
        ],
        "decor": [
            {"id": 301, "name": "Ceramic Vase", "stock": 85},
            {"id": 302, "name": "Wall Art - Abstract", "stock": 15},
        ],
    }

    # Parameterized lookup mock
    normalized_category = item_category.strip().lower()
    results = mock_database.get(normalized_category, [])

    if results:
        logger.info(f"Query returned {len(results)} items for '{normalized_category}'.")
        return f"Inventory query results for '{normalized_category}':\n{results}"
    else:
        logger.info(f"No items found matching category: '{normalized_category}'.")
        return f"No items found for the category: '{normalized_category}'."


if __name__ == "__main__":
    logger.info("Starting 'traditionsync-db-server' FastMCP server...")
    mcp.run()
