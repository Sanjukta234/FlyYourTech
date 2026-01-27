import json
from langchain_core.tools import Tool


with open("data/leads.json") as f:
    leads_data = json.load(f)


def lead_tool(query: str) -> str:
    if "all" in query.lower():
        return str(leads_data)


    for lead in leads_data:
        if lead["name"].lower() in query.lower():
            return str(lead)


    return "No matching lead found"


lead_management_tool = Tool(
name="LeadManagementTool",
func=lead_tool,
description="Fetch lead details from lead database"
)