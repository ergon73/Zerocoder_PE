
import json
import requests
import os
from openai import OpenAI
from prompts import assistant_instructions

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Отправка данных о потенциальном клиенте в Make
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

# Создать или загрузить ассистента
def create_assistant(client):
    assistant_file_path = 'assistant.json'

    # Если ассистент уже создан — загружаем его ID
    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # Создание нового ассистента
        assistant = client.beta.assistants.create(
            instructions=assistant_instructions,
            model="gpt-4o",
            tools=[
                {
                    "type": "file_search"
                },
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
                                    "description": "Client's full name."
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "Client's phone number."
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Preferred appointment date and time."
                                },
                                "service": {
                                    "type": "string",
                                    "description": "Requested tattoo or piercing service."
                                }
                            },
                            "required": ["name", "phone", "date", "service"]
                        }
                    }
                }
            ]
        )

        # Сохраняем assistant_id для будущего использования
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
