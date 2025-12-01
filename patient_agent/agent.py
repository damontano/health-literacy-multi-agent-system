from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from .config import config
from .sub_agents.education_agent import education_agent
from .sub_agents.reminder_agent import reminder_agent
from .sub_agents.resource_agent import resource_agent

from .validator import validate_json

async def auto_save_to_memory(callback_context):
    ms = getattr(callback_context._invocation_context, "memory_service", None)
    session = getattr(callback_context._invocation_context, "session", None)
    json_data = getattr(callback_context._invocation_context, "output", None)

    if json_data:
        validated = validate_json(json_data, memory_service=ms)
        callback_context._invocation_context.output = validated

    if ms and session:
        await ms.add_session_to_memory(session)

root_agent = LlmAgent(
    name="root_agent",
    model=Gemini(model=config.worker_model),
    description="Parses discharge instructions and coordinates subagents.",
    instruction=""" 
    When given discharge instructions in plain text: 
    1. Extract key information and output JSON in this template: 
       { 
         "patient_email": "<email address if provided>", 
         "medications": [ 
           {"drug": "<drug>", "dose": "<dose>", "route": "<route>", "frequency": "<frequency>"} 
         ], 
         "reminders": [ 
           {"task": "<reminder task>", "timeframe": "<original text>", "normalized_datetime": "<ISO 8601 datetime>"} 
         ], 
         "conditions": ["<condition1>", "<condition2>"], 
         "tasks": [ 
           {"agent": "education_agent", "instruction": "Explain medications in plain language"}, 
           {"agent": "reminder_agent", "instruction": "Set reminders for medications and follow-ups"}, 
           {"agent": "resource_agent", "instruction": "Provide credible resources for conditions"} 
         ] 
       } 
    2. Normalize all time expressions into ISO 8601 datetime. 
    3. If patient_email is missing, check memory for stored PatientEmail. If still missing, ask the patient to provide it. 
    """,
    sub_agents=[education_agent, reminder_agent, resource_agent],
    after_agent_callback=auto_save_to_memory
)


