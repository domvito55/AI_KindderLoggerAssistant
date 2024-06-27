from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from openai import OpenAI
import os
import time
import logging

assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI()

app = FastAPI()

logging.basicConfig(level=logging.INFO)

class MessageRequest(BaseModel):
    message: str

@app.post("/message")
async def read_message(request: Request, message_request: MessageRequest = Body(...)):
    conversation_id = request.headers.get("Openai-Conversation-Id")
    if conversation_id:
        logging.info(f"Using conversation ID: {conversation_id}")
    else:
        logging.info("No conversation ID provided.")

    message = message_request.message
    if not message:
        return {"message": "No message provided."}
  
    thread = client.beta.threads.create()
    assistant = client.beta.assistants.retrieve(assistant_id)
  
    client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    still_running = True
    while still_running:
        latest_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        still_running = latest_run.status != "completed"
        if still_running:
            time.sleep(2)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    result = messages.data[0].content

    return {"message": result}