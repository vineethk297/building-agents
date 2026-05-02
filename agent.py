import os
import anthropic
from dotenv import load_dotenv

# 1. Load your .env file and get the key
load_dotenv()
api_key = os.environ.get("ANTHROPIC_API_KEY")
print("Key loaded:", api_key[:10] if api_key else "NOT FOUND")


client = anthropic.Anthropic()

def get_weather(city):
    return f"Sunny, 85F in {city}"

def calculate(expression):
    return eval(expression)

get_weather_tool = {
    "name" : "get_weather",
    "description" : "Get the current weather for a given city",
    "input_schema" :{
        "type" : "object",
        "properties" : {
            "city" : {
                "type" : "string",
                "description" : "city to get weather for.."
            }
        },
        "required" : ["city"]
    }
}

calculate_tool = {
    "name" : "calculate",
    "description" : "solve the mathematical expression",
    "input_schema" : {
        "type" : "object",
        "properties" : {
            "expression" : {
                "type" : "string",
                "description" : "Solve the expression"
            }
        },
        "required" : ["expression"]
    }
}

while True:
    user_input = input("Askk me anything...")
    
    if user_input.lower() == "quit":
        break

    message = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages = [{
            "role" : "user",
            "content" : user_input
        }],
        tools = [get_weather_tool, calculate_tool]
    )
    # print(message)
    # print(message.content[0].input)


    while message.stop_reason == 'tool_use':
        name = message.content[0].name
        input_city = message.content[0].input
        tool_id = message.content[0].id
        tool_type = message.content[0].type
        
        if name == "get_weather":
            result = get_weather(input_city['city'])
        elif name == "calculate":
            result = str(calculate(input_city['expression']))
            
        
        message = client.messages.create(
            model = "claude-sonnet-4-6",
            max_tokens = 1024,
            messages = [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": message.content},
                {"role": "user", "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result
                }]}
            ]
        )
        
    print(message.content[0].text)