from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# defining the model

client = OpenAI(api_key="daddedf")

# Calling rhe model
resp = client.responses.create(model='codex-mini-latest',
                               input='Summerze this text '+"AI is bad for health "*100)

# To know the number of total_tokens
print("token used :", resp.usage.total_tokens)
