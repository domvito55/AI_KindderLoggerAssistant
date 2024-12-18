# AI_KindderLoggerAssistant

This is just a *small example* on how to use RAG with OpenAI API.
We are also using whisper-1 to transcript the audios in the audios folder
and completions service to create a json file with the transcripts.

To use this code you will need:
- Step 1: set an OpenAI account
- Step 2: set the OPENAI_API_KEY enviroment key
- Step 3: run pip install -r requirements.txt
- Step 4: upload new files to the audios folder, if you will.
- Step 5: run the transcription.py script to create the audio json files.
- Step 6: run the assistants.py script to test the assistant locally
- Step 7: Once the files, vectors, and assistant is created, you can expose it using uvicorn and the service.py script

It was also provided a dockerfile and a .circleci config to create a container and automatically deploy it using AWS ECS, but I am currently not watching this repo to save costs, this is a demo only.

