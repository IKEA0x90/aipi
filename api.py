import uuid
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

class MessageModel(BaseModel):
    message: str

def create_app(event_bus):
    app = FastAPI()
    
    @app.post("/assistants/{uid}")
    async def create_assistant(uid: str):
        request_id = str(uuid.uuid4())
        await event_bus.publish("create_user_assistant", {"uid":uid}, request_id)
        return await event_bus.response_queues[request_id].get()
    
    # {uid} will be a mandatory path parameter, {aid:str?} marks an optional url parameter.
    @app.post("/assistants/{uid}")
    async def send_single_message(
        uid: str, 
        message: str,
        # this line of code not only defines AID, it also tells FastAPI to check for url parameter ?aid.
        aid: Optional[str] = None
    ):
        request_id = str(uuid.uuid4())
        await event_bus.publish("send_single_message",
                {
                    "uid": uid,
                    "aid": aid,
                    "message": message
                }, 
            request_id
        )
        return await event_bus.response_queues[request_id].get()
    	
    return app
