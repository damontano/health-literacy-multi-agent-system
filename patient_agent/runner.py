from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from patient_agent.agent import root_agent

memory_service = InMemoryMemoryService()
session_service = InMemorySessionService()

runner = InMemoryRunner(
    app_name="patient_agent",
    agent=root_agent,
    memory_service=memory_service,
    session_service=session_service
)


