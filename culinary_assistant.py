from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Initialziing the model
try:
    client = genai.Client()

except Exception as e:
    print(f"Error in intialzing the model {e}")


def generate_recipe(ingredients_list):
    prompt = f'''You are a helpful culinary assistant. Your task is to generate a creative and delicious recipe based ONLY on the ingredients provided by the user.

    Please follow these rules:
    1. The recipe title should be catchy and descriptive.
    2. List all the necessary ingredients under an "Ingredients" heading.
    3. Provide clear, step-by-step instructions under an "Instructions" heading.
    4. If the ingredients aren't enough for a proper meal, suggest a simple snack or state that a full recipe isn't possible.

    User's Ingredients: {ingredients_list}'''
    try:
        res = client.models.generate_content(model='gemini-2.5-flash',
                                             contents=prompt,
                                             )

        print("\n"+"="*50)
        print("Created Recipe")
        print("="*50)
        print(res.text)
    except Exception as e:
        print(f"\n An error occured during api call {e}")


while True:
    task = input(
        "Enter your task (type 'recipe' to generate or 'exit' to quit)").strip().lower()

    if task == 'exit':
        print("\n Exiting the culinary Assistant Good bye !!!")
        break

    elif task == 'recipe':
        ingredients = input(
            "Enter the ingredients with the coma separated :").strip()

        if not ingredients:
            print("You must enter the ingredients with comma ")
            continue

        generate_recipe(ingredients_list=ingredients)

    else:
        print(f"❓ Invalid task '{task}'. Please enter 'recipe' or 'exit'.")
