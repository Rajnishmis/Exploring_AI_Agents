from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

# defining the model
client = OpenAI(api_key="Your api key ")

# Defing the prompt
prompt = "Return a json with keys :name,age, city ,values"

# Calling the model
resp = client.responses.create(
    model='codex-mini-latest', input=prompt, temperature=0)


parsed = json.loads(resp.output_text)
