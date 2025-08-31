from dotenv import load_dotenv
import os
import json
# Load env variables from the .env file.
load_dotenv()

# Azure openai credentials
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_API_KEY =  os.getenv("AZURE_API_KEY")

# Google vertex credentials
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_VERTEX_PROJECT_ID = os.getenv("GOOGLE_VERTEX_PROJECT_ID")
GOOGLE_VERTEX_PROJECT_LOCATION = os.getenv("GOOGLE_VERTEX_PROJECT_LOCATION")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PROXY_API_KEY = os.getenv("PROXY_API_KEY")
PROXY_API_BASE = os.getenv("PROXY_API_BASE")