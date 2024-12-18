# -*- coding: utf-8 -*-
"""
File Name: service.py
Description: This script creates a FastAPI web service that interacts with the OpenAI API. 
             It handles user messages, processes them through an OpenAI assistant,
             and returns the assistant's response.
Author: MathTeixeira
Date: June 28, 2024
Version: 1.0.0
License: MIT License
Contact Information: mathteixeira55
"""

# ### Imports ###
from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from openai import OpenAI
import os
import time
import logging

# ### Constants ###
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

# Initialize the OpenAI client
# You need to set the OPENAI_API_KEY environment variable with your API key
client = OpenAI()

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)


# ### Data Models ###
class MessageRequest(BaseModel):
    """Data model for the incoming message request."""
    message: str


# ### API Endpoints ###


@app.post("/message")
async def read_message(request: Request,
                       message_request: MessageRequest = Body(...)):
    """
    Endpoint to handle incoming messages and get a response from the OpenAI assistant.

    Args:
        request (Request): The HTTP request object.
        message_request (MessageRequest): The request body containing the user message.

    Returns:
        dict: A dictionary containing the assistant's response message.
    """
    # Retrieve conversation ID from headers
    conversation_id = request.headers.get("Openai-Conversation-Id")
    if conversation_id:
        logging.info(f"Using conversation ID: {conversation_id}")
    else:
        logging.info("No conversation ID provided.")

    # Retrieve the user message from the request body
    message = message_request.message
    if not message:
        return {"message": "No message provided."}

    # Create a new thread for the conversation
    thread = client.beta.threads.create()

    # Retrieve the assistant
    assistant = client.beta.assistants.retrieve(assistant_id)

    # Add the user message to the thread
    client.beta.threads.messages.create(thread.id,
                                        role="user",
                                        content=message)

    # Start a new run with the assistant
    run = client.beta.threads.runs.create(thread_id=thread.id,
                                          assistant_id=assistant.id)

    # Poll for the completion of the run
    still_running = True
    while still_running:
        latest_run = client.beta.threads.runs.retrieve(thread_id=thread.id,
                                                       run_id=run.id)
        still_running = latest_run.status != "completed"
        if still_running:
            time.sleep(2)

    # Retrieve and return the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    result = messages.data[0].content

    return {"message": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, reload=True)
