

import api
import ai
import asyncio
import uvicorn
from typing import Dict, Any

class EventBus:
    def __init__(self):
        self.event_queue = asyncio.Queue()
        self.response_queues: Dict[str, asyncio.Queue] = {}
        self.ai_handler = ai.AIHandler()
    
    async def publish(self, event_type: str, kwargs: dict, request_id: str):
        await self.event_queue.put({
            'type': event_type,
            'kwargs': kwargs,
            'request_id': request_id
        })
        self.response_queues[request_id] = asyncio.Queue()
    
    async def process_events(self):
        while True:
            event = await self.event_queue.get()
            response = await self.ai_handler.handle_event(event['type'], event['kwargs'])
            await self.response_queues[event['request_id']].put(response)
            del self.response_queues[event['request_id']]

# Initialize components
event_bus = EventBus()
app = api.create_app(event_bus)

def run_server():
    asyncio.create_task(event_bus.process_events())
    uvicorn.run(app, host="127.0.0.1", port=2474)