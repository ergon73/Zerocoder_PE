import json
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import assistant_instructions

# Загрузка переменных окружения
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

def create_lead(name, phone, date, service):
    url = "https://hook.eu2.make.com/jp2pwthnimnmumtpn840eoj80q7xwfpb"
    data = {
        "name": name,
        "phone": phone,
        "date": date,
        "service": service
    }
    response = requests.post(url, json=data)
    try:
        if response.content:
            return response.json()
        else:
            print("No data received in response")
            return {}
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from response: {response.text}")
        return {}

def create_assistant(client):
    assistant_file_path = 'assistant.json'
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-4o",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "create_lead",
                        "description": "Capture lead details and save to Make.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Name of the lead."
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Phone number of the lead."
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Date and time of the appointment."
                                },
                                "service": {
                                    "type": "string",
                                    "description": "Requested service (e.g. tattoo)."
                                }
                            },
                            "required": ["name", "phone", "date", "service"]
                        }
                    }
                }
            ]
        )

        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
