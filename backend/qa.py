import os
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

def get_response(messages):

    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_ENDPOINT"),
    )
    response = client.chat.completions.create(
        messages = messages,
        model = os.getenv("OPENAI_DEPLOYMENT_NAME"),
    )

    return response.choices[0].message.content
    