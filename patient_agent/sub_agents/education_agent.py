from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from ..config import config
from ..tools import education_tool

education_agent = LlmAgent(
    name="education_agent",
    model=Gemini(model=config.worker_model),
    tools=[education_tool],
    instruction="""You are an assistant that explains medications.
"""
)
