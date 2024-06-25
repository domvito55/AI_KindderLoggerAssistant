import time
import glob
from openai import OpenAI

MODEL = "gpt-3.5-turbo"

client = OpenAI()

assistant = client.beta.assistants.create(
  name = "KinderLogger",
  instructions = "You are a helpful assistant.",
  tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
  model=MODEL
)

pattern = "*.json"
json_files = glob.glob(pattern)

# Create a vector store caled "Financial Statements"
vector_store = client.beta.vector_stores.create(name="Transcripts")

for file_name in json_files:
  print(f"Processing {file_name}")
  transcript_file = client.files.create(
    file=open(file_name, "rb"),
    purpose="assistants"
  )

  file = client.beta.vector_stores.files.create_and_poll(
    vector_store_id=vector_store.id,
    file_id=transcript_file.id
  )

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

thread = client.beta.threads.create()

def display_main_menu():
  print("\n[KinderLogger Assistant]")
  prompt = input("\nEnter your prompt: ")
  handle_main_menu_option(prompt)

def handle_main_menu_option(prompt):
  client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=prompt
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
  print(messages.data[0].content)


while True:
  display_main_menu()
