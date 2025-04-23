import os
import openai
from pydantic import BaseModel, create_model
from typing import Any

openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_structure_from_json(json_data: dict) -> type:
    fields = {}
    for key, value in json_data.items():
        if isinstance(value, str):
            fields[key] = (str, ...)
        elif isinstance(value, int):
            fields[key] = (int, ...)
        elif isinstance(value, float):
            fields[key] = (float, ...)
        elif isinstance(value, bool):
            fields[key] = (bool, ...)
        elif isinstance(value, list):
            fields[key] = (list[Any], ...)
        elif isinstance(value, None):
            fields.pop(key)
        elif isinstance(value, dict):
            nested_model = generate_structure_from_json(f"{key.lower()}", value)
            fields[key] = (nested_model, ...)
        else:
            fields[key] = (Any, ...)
    return create_model("Structures", **fields)

class Assistant:
    def __init__(self, aid: str, messages: list = []):
        self.aid = aid
        self.messages = messages

class Message:
    def __init__(self, type, content, tool, embedding):
        self.type = type
        self.content = content
        self.tool = tool
        self.embedding = embedding

class AIHandler:
    def __init__(self):
        self._openai = None  # Lazy load OpenAI client
        self.assistants = dict()

    async def _get_response(self, assistant):
        completion = self._openai.chat.completions.create(
            model="gpt-4o",
            messages=assistant.messages,
            tools=assistant.tools,
        )
        return completion.choices[0].message.content
        
    async def _ensure_client(self):
        if not self._openai:
            self._openai = openai.AsyncClient()
    
    async def handle_event(self, event_type: str, kwargs):
        await self._ensure_client()
        
        match event_type:
            case "create_user_assistant":
                return await self._create_user_assistant(**kwargs)
            case "send_single_message":
                return await self._create_user_assistant(**kwargs)
            case "request_structure":
                return await self._create_structure(**kwargs)
            case "default":
                return await self._send_single_message(**kwargs)
            case _:
                return None
            
    async def _create_structure(self, uid, structure, aid):
        assistants = self.assistants.get(uid)
        if assistants and isinstance(assistants, dict):
            assistant = assistants.get(aid)
            if assistant:
                message = structure.get("message")
                if message:
                    structure['message'] = None
                else:
                    return {}

                # Create a new model based on the structure
                s = generate_structure_from_json(f"{structure}")
                
                completion = self._openai.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Create a custom json object based on the provided structure and the message. If a field is missing, make it yourself based on context."},
                    {"role": "user", "content": f"{message}"}
                ],
                response_format=s
)
                return completion.choices[0].message.parsed
        return {}
    
    async def _create_user_assistant(self, uid, aid):
        assistant = Assistant(aid)

        if uid in self.assistants:
            # user already has an assistants dictionary
            assistant_dict = self.assistants[uid]
            if aid not in assistant_dict:
                assistant_dict[aid] = assistant

        else:
            # first assistant for this user
            self.assistants[uid] = {aid: assistant}

        return assistant
    
    async def _send_single_message(self, uid, aid, message):
        assistants = self.assistants.get(uid)
        if assistants and isinstance(assistants, dict):
            assistant = assistants.get(aid)
            if assistant:
                assistant.messages.append(message)

                self._get_response(assistant)