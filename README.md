# aipi
## Huh?
API for AI. AI API. AIPI.
## So..?
<b>Only three scripts shall be used. They must follow the rules.</b></br>
* AI is the only script allowed to interact with, well, AI. Be that processing user messages or implementing Assistant functionality - the world is your oyster. 
* AIPI is the connection point between AI and API. It can implement _anything_ except AI and API functionality. It is also the script that will be executed.
* API must provide API functionality. And <b>yes</b>, that includes both incoming and outgoing calls.
## Cool..
To connect the services, the application uses events. AIPI is the event bus, sending calls between API and AI. 
<br> First, an incoming call is received in API. It adds a request to AIPI, the bus, which is then processed in AI.
<br> However, AI can't send API calls. It processes the event in a local Assistant object. It then sends the Assistant to back to API via AIPI.
<br> Another catch! API doesn't know what an Assistant is and is not allowed to. So, AI actually sends a json object that is then processed in API.
## Why?
AIPI is a really cool name - just admit. In fact, such a name deserves special treatment instead of being another boring project.
<br> So, the only logical thing to do is introduce these unique limitations.
<br> This thing is absolutely not practical - API ended up doing most of the work. 
