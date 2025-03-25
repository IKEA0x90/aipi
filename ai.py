import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

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
            case "default":
                return await self._send_single_message(**kwargs)
            case _:
                return None
    
    async def _create_user_assistant(self, uid, aid):
        assistant = Assistant(aid)

        if uid in self.assistants:
            if isinstance(self.assistants[uid], dict):

                # sser already has an assistants dictionary
                assistant_dict = self.assistants[uid]
                if aid not in assistant_dict:
                    assistant_dict[aid] = assistant

            else:

                # convert single assistant to dictionary of assistants
                existing_assistant = self.assistants[uid]
                self.assistants[uid] = {
                    existing_assistant.aid: existing_assistant,
                    aid: assistant
                }
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
                return assistant
        
        return assistant