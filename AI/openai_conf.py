# Python packages
import os
from openai import OpenAI

# openai instance
"""
we are going to use the client instance to send messages and get responses from openai APIs
"""
openai_client = OpenAI(
    api_key=os.environ.get("open_ai_key"),
)




