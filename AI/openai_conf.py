# Python packages
import os
from openai import OpenAI
from dotenv import load_dotenv

# load .env file
load_dotenv()

# openai instance
"""
we are going to use the client instance to send messages and get responses from openai APIs
"""
openai_client = OpenAI(
    api_key=os.getenv("open_ai_key"),
)




