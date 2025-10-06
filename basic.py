from openai import OpenAI
from dotenv import load_dotenv

# Load the API key
load_dotenv()
# Defining LLM model
client = OpenAI(api_key="Open_AI_Key")

# calling the model
resp = client.responses.create(
    model="chatgpt-4o-latest",
    instructions="You are a helpful assistant",
    temperature=0,
    input="Ask ur question here")

# giving output
print(resp.output_text)
