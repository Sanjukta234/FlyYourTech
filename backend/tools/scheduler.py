#from langchain.tools import Tool
from langchain_core.tools import Tool



def schedule_meeting(query: str) -> str:
 return "Meeting scheduled successfully for tomorrow at 11 AM."


scheduler_tool = Tool(
name="SchedulerTool",
func=schedule_meeting,
description="Schedule meetings or appointments"
)