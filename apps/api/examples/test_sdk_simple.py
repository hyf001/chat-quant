import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["THS_TIER"] = "dev"

from app.services.tools.sql_validator import validate_sql_tool
print(f"Tool name: {validate_sql_tool.name}")
print(f"Tool description: {validate_sql_tool.description}")
print("Test file created successfully!")
