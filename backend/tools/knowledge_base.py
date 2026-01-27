import json
from langchain_core.tools import Tool


with open("data/company.json") as f:
    company_data = json.load(f)


def company_info_tool(query: str) -> str:
    for key, value in company_data.items():
        if key in query.lower():
            return f"{key}: {value}"
    return str(company_data)

knowledge_tool = Tool(
name="KnowledgeBaseTool",
func=company_info_tool,
description="Fetch company details like address, phone, services, pricing"
)