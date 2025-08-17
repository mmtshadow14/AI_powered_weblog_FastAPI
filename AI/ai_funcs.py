# Python packages
import os
from dotenv import load_dotenv

# AI
from AI.openai_conf import openai_client

# loading .env file
load_dotenv()


# get keywords from AI
def get_keywords(description):
    """
    with this function we will send request to openai APIs and the AI will return us the keywords which is stored
    in the post description of the post which the user just made, and we will return the keywords as list
    """
    response = openai_client.responses.create(
        model="gpt-5",
        messages=[
            {"role": "system",
             "content": "Extract 2-3 keywords from the text, return them as a comma-separated list."},
            {"role": "user", "content": description}
        ]
    )
    keywords = response.output_text
    return [k.strip() for k in keywords.split(",")]
