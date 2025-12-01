from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from ..config import config
from ..tools import reminder_tool

reminder_agent = LlmAgent(
    name="reminder_agent",
    model=Gemini(model=config.worker_model),
    tools=[reminder_tool],
    instruction="""You are an assistant that schedules reminders.
"""
)
