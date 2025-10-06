import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
import json
from transformers import pipeline
# Loading the variables or API key  from .env
load_dotenv()

# Read the token from the environment variable
# hf_token = os.getenv("HUGGING_FACE_API_TOKEN")
# Load a Hugging face model

# generator = pipeline(
#     "text-generation",
#     model="bigscience/bloom-560m",  # public, no token needed
#     use_auth_token=hf_token
# )

# Intialize client with the env var
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Defing the pydantic model for validating normalized addresses


class Address(BaseModel):
    street: str
    city: str
    postcode: str
    coutry: str
    notes: str = " "


# Creating a prompt to use few shot prompting
few_shot_prompt = """
You are a JSON-only address normalizer. For each input, output ONLY one JSON object
with keys: street, city, postcode, country, notes.
Use empty string for missing fields. No explanations, no markdown, only JSON.

Example 1
Input: "221b baker st, london nw1"
Output:
{"street":"221B Baker Street","city":"London","postcode":"NW1","country":"United Kingdom","notes":""}

Example 2
Input: "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
Output:
{"street":"1600 Amphitheatre Parkway","city":"Mountain View","postcode":"94043","country":"United States","notes":"state CA present"}

Now normalize the following address and output only the JSON:
Input: "10 Downing St, SW1A 2AA, London"
"""

######################################################################
# Helper function to call HF model


# def call_hf_model(prompt: str) -> str:
#     """
#     Calls Hugging Face text-generation pipeline
#     Returns generated text (still a string)
#     """
#     result = generator(prompt, max_new_tokens=200)
#     # The model returns a list of dicts with 'generated_text'
#     return result[0]['generated_text']

####################################################################


def normalize_address(address: str) -> Address:
    """ Normalize a freeform mailing address using OpenAI Model .
    Return a pydantic Address object ,
    It implements 
    Model Call
    Json Parsing
    Validation
    Retry once if with clarifying promot if parse fails 
    """

    # Building trhe initial prompt
    prompt = few_shot_prompt+f'Input:{address}"\nOutput:'

    for attempt in range(2):
        try:
            resp = client.responses.create(
                model="gpt-4o",
                instructions="You are a helpful assistant return json only output",
                input=prompt,
                temperature=0  # to get the determinstic output
            )
            # plain_text = call_hf_model(prompt).strip()
            # print("Model output:", plain_text)
            # To get the plain text output
           # resp.output_text flattens all the model’s text output into a single string.
            plain_text = resp.output_text.strip()
            print(plain_text)

            # To get the JSON
            # json.loads() converts the JSON string into a Python dictionary.
            parsed_json = json.loads(plain_text)

            # Validate the dictionary using pydantic
            normalize_address = Address(**parsed_json)

            return normalize_address

        except (json.JSONDecodeError, ValidationError) as e:
            # if first attempt fials ,retry with a clarifying promt
            if attempt == 0:
                # Modify the promt
                prompt = few_shot_prompt+f'Input:"{address}"\nOutput:'
                prompt += "\nIMPORTANT:Return valid JSON ONly.DO not Include any text or markdown"
                continue
            else:
                # second attempt failed ,return with the note
                return Address(street=" ", city=" ", postcode=" ", coutry=" ", notes=f"Failed to parse address: {address}")


if __name__ == "__main__":
    sample_addresses = [
        "221b baker st, london nw1",
        "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
        "P.O. Box 123, Sydney NSW 2000"
    ]

    for addr in sample_addresses:
        normalized = normalize_address(addr)
        print(normalized.json())
