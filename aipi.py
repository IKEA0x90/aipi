

import api
import ai
import asyncio
import uvicorn
from typing import Dict

class EventBus:
    '''
    Class used for passing events between API and AI
    '''
    def __init__(self):
        self.event_queue = asyncio.Queue() # queue for incoming events
        # we are using typing Dict instead of built-in to specify key and value types
        self.response_queues: Dict[str, asyncio.Queue] = {} # a dict of all queues
        self.ai_handler = ai.AIHandler() # AI class that is listening to the calls 
        self.api_handler = api.APIHandler() # API class that is listening to the calls

    async def add_request(self, event_type: str, kwargs: dict, request_id: str):
        '''
        add event to bus.
        takes event_type: str, kwargs: dict, request_id: str
        '''
        # add new event to the queue
        await self.event_queue.put({
            'type': event_type,
            'kwargs': kwargs,
            'request_id': request_id
        })
        # add it to the map
        self.response_queues[request_id] = asyncio.Queue()
    
    async def process_events(self):
        '''
        a loop that will be ran for processing all events
        '''
        while True:
            event = await self.event_queue.get()
            # send the event to AI
            response = await self.ai_handler.handle_event(event['type'], event['kwargs'])

            await self.response_queues[event['request_id']].put(response)
            del self.response_queues[event['request_id']]

# Initialize components
event_bus = EventBus()
app = api.create_app(event_bus)

def run_server():
    asyncio.create_task(event_bus.process_events())
    uvicorn.run(app, host="127.0.0.1", port=2474)