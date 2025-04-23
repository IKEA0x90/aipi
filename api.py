import uuid
from fastapi import FastAPI, Body, Query
from pydantic import BaseModel
from typing import Optional

class MessageModel(BaseModel):
    message: str

class StructureModel(BaseModel):
    structure: dict

def create_app(event_bus):
    app = FastAPI()
    
    @app.post("/assistants")
    async def create_assistant(
        uid: str = Query(..., description="User ID"), 
        aid: Optional[str] = Query(None, description="Assistant ID")
    ):
        request_id = str(uuid.uuid4())
        await event_bus.publish("create_user_assistant", {"uid": uid, "aid": aid}, request_id)
        return await event_bus.response_queues[request_id].get()

    @app.post("/message")
    async def send_single_message(
        message_data: MessageModel = Body(...),
        uid: str = Query(..., description="User ID"),
        aid: Optional[str] = Query(None, description="Assistant ID")
    ):
        request_id = str(uuid.uuid4())
        await event_bus.publish("send_single_message",
            {
                "uid": uid,
                "aid": aid,
                "message": message_data.message
            }, request_id)
        
        return await event_bus.response_queues[request_id].get()

    @app.post("/structure")
    async def request_structure(
        structure_data: StructureModel = Body(...),
        uid: str = Query(..., description="User ID"),
        aid: Optional[str] = Query(None, description="Assistant ID")
    ):
        request_id = str(uuid.uuid4())
        await event_bus.publish("request_structure",
            {
                "uid": uid,
                "aid": aid,
                "structure": structure_data.structure
            }, request_id)
        
        return await event_bus.response_queues[request_id].get()

    return app