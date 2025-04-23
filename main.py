from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
from logic import get_caddy_response

app = FastAPI()

@app.post("/bot")
async def bot(request: Request):
    form = await request.form()
    user_input = form.get("Body")
    response = MessagingResponse()
    reply = get_caddy_response(user_input)
    response.message(reply)
    return str(response)
