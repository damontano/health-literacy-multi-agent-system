import os
from dataclasses import dataclass
from google.genai import types

os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "False")  # run locally

@dataclass
class Configuration:
    worker_model: str = "gemini-2.5-flash-lite"

config = Configuration()

