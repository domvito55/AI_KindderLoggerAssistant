import glob
import whatsapp_utils
from openai import OpenAI

client = OpenAI()
pattern = "audios\\*.ogg"
opus_files = glob.glob(pattern)

for file_name in opus_files:
  file_datetime = whatsapp_utils.extract_date_time_from_filename(file_name)
  print(f"Processing {file_name}")
  audio_file = open(file_name, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1",
    response_format="text",
    file=audio_file,
    temperature=0.2,
    prompt="Matheus"
  )

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assitant."},
      {"role": "user", "content": f"""Translate into Portuguese the following text that I surrounded by 3 stars (***).
        Create a JSON document with the following elements:
       - {file_datetime.date()}. Put the traslated text here.
       - audiofile_datetime. The value must be: {file_datetime}
       ***
       {transcription}
       ***
       """
      }
    ], response_format={"type": "json_object"}
  )

  with open(f"{file_datetime.date()}.json", "w", encoding="utf-8") as json_file:
    json_file.write(completion.choices[0].message.content)
  
  print("Done!")
