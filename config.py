# API key and model configuration

import os 
from dotenv import load_dotenv

load_dotenv()

# Hugging Face API Key
HF_API_KEY = os.getenv("HF_TOKEN")

# Hugging Face Model ID
MODEL_ID = "microsoft/Phi-3-mini-4k-instruct"

# Ensure API key is set
if HF_API_KEY is None:
    raise ValueError("Hugging Face API key is missing. Set the HF_TOKEN environment variable.")