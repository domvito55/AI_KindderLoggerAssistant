# -*- coding: utf-8 -*-
"""
File Name: assistants.py
Description: This script uses the OpenAI API to create a virtual assistant named
             "KinderLogger" that can process JSON transcript files, create vector
             stores, and interact with the user through a command-line interface.
             This is a test script to demonstrate the capabilities of the OpenAI API.
             Not necessaire to run this script, it is just a demonstration.
Author: MathTeixeira
Date: June 28, 2024
Version: 1.0.0
License: MIT License
Contact Information: mathteixeira55
"""

# ### Imports ###
import time
import glob
from openai import OpenAI

# ### Constants ###
MODEL = "gpt-3.5-turbo"
PATTERN = "*.json"

# Initialize the OpenAI client
# You need to set the OPENAI_API_KEY environment variable with your API key
client = OpenAI()

# Create the assistant with specific tools and model
assistant = client.beta.assistants.create(
    name="KinderLogger",
    instructions="You are a helpful assistant.",
    tools=[{
        "type": "file_search"
    }, {
        "type": "code_interpreter"
    }],
    model=MODEL)

# Pattern to match JSON files in the current directory
json_files = glob.glob(PATTERN)

# Create a vector store named "Transcripts"
vector_store = client.beta.vector_stores.create(name="Transcripts")

# Process each JSON file and add it to the vector store
for file_name in json_files:
    print(f"Processing {file_name}")

    # Create a transcript file in the OpenAI client
    transcript_file = client.files.create(file=open(file_name, "rb"),
                                          purpose="assistants")

    # Add the transcript file to the vector store and wait for completion
    file = client.beta.vector_stores.files.create_and_poll(
        vector_store_id=vector_store.id, file_id=transcript_file.id)

# Update the assistant to include the vector store for file search
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {
        "vector_store_ids": [vector_store.id]
    }})

# Create a new thread for interaction
thread = client.beta.threads.create()


def display_main_menu():
    """Displays the main menu and handles user input."""
    print("\n[KinderLogger Assistant]")
    prompt = input("\nEnter your prompt: ")
    handle_main_menu_option(prompt)


def handle_main_menu_option(prompt):
    """Handles the user's prompt and retrieves the response from the assistant."""
    # Create a new message in the thread
    client.beta.threads.messages.create(thread_id=thread.id,
                                        role="user",
                                        content=prompt)

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

    # Retrieve and display the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.data[0].content[0].text.value)


# Main loop to keep the assistant running and accepting user input
while True:
    display_main_menu()
