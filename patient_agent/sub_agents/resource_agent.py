from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from ..config import config
from ..tools import resource_tool

resource_agent = LlmAgent(
    name="resource_agent",
    model=Gemini(model=config.worker_model),
    tools=[resource_tool],
    instruction="""You are an assistant that provides resources.
"""
)
