
# # Rules for defining a function
# {
#     "type": "function",
#     "name": "get_wheather",
#     "description": "Retrives current weather for the given location ",
#     "parameters":
#         {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "City and country e.g Bogota ,Columbia"},
#                 "units": {
#                     "type": "string",
#                     "enum": ["celsius", "fahrenhite"],
#                     "description": "Units the temperature will be returned in ."}
#             },
#             "required": ["location", "units"],
#             "additionalProperties": False
#         },
#         "strict": True
# }

# import google.generativeai as genai
# from google.generativeai.types import FunctionDeclaration, Tool

# # difing a function for horoscope
# horoscope_tool = Tool(
#     function_declerations=[
#         FunctionDeclaration(
#             name="get_horoscope",
#             description="Get the today's horoscope for the astrological sign ",
#             parameters={
#                 "type": "object",
#                 "properties": {
#                         "astrological_sign": {
#                             "type": "string",
#                             "description": "An astrological sign something like taurous or Aquarius "
#                         },
#                 },
#                 "required": ["astrological_sign"],
#             },
#         )
#     ]
# )

# # Intializing the model
# model = genai.GenerativeModel(
#     model_name='gemini-1.5-flash',
#     tools=[horoscope_tool]

# )

# # giving prompt to the model
# chat = model.start_chat(
#     history=[]
# )

# # prompting
# prompt = "What is horoscope for taurus today ?"

# # passing prompt to the model
# response = chat.send_message(prompt)

# # Printing the output
# print(response.candidates[0].content_parts[0].to_dict())


import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool

# Manually define the function declaration using your JSON schema
horoscope_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="get_horoscope",
            description="Get the today's horoscope for the astrological sign",
            parameters={
                "type": "object",
                "properties": {
                    "astrological_sign": {
                        "type": "string",
                        "description": "An astrological sign something like Taurus or Aquarius"
                    },
                },
                "required": ["astrological_sign"],
            },
        )
    ]
)

# Initialize the Gemini model with your tool
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[horoscope_tool],
    # Correct way to set tool configuration
    tool_config={
        "function_calling_config": {
            "mode": "ANY"  # 'ANY' forces the model to predict a function call from the list of provided tools
        }
    }
)

# A sample conversation to demonstrate how the model can use your tool
chat = model.start_chat(
    history=[]
)

# Example user prompt
prompt = "What is the horoscope for Taurus today?"

# Send the prompt to the model and observe the function call
response = chat.send_message(prompt)

# Print the model's response, which will contain the function call
print(response.candidates[0].content.parts[0].to_dict())
