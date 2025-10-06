from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Defining the model
client = OpenAI(api_key="Your api key ")

# Creating a prompt for the model
prompt = "Your task is to help me in my task by assisting me in my faily task like generating the code and then decoding them "

# Calling the model
resp = client.responses.create(model='o1',
                               input=prompt,
                               temperature=0.7)

print(resp.output_text)
