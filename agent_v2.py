import os
import anthropic

client = anthropic.Anthropic()

def get_weather(city):
    return f"It is sunny, 85F in {city}"

get_weather_tool = {
    "name" : "get_weather",
    "description" : "Get the weather of the given city",
    "input_schema":{
        "type" : "object",
        "properties" : {
            "city" : {
                "type" : "string",
                "description" : "the city to get weather for"
            }
        },
        "required" : ["city"]
    }
}


while True:
    user_input = input("Ask me anything . . .")
    
    if user_input == "quit":
        break
    
    
    message = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 1024,
    messages = [
        {
        "role" : "user",
        "content" : user_input
    }
    ],
    tools = [get_weather_tool]
)

    while message.stop_reason == "tool_use":
        tool_uses = [block for block in message.content if block.type == 'tool_use']
        
        tool_results = []
        for tool_use in tool_uses:
            result = get_weather(tool_use.input['city'])
            tool_results.append({
                "type" : "tool_result",
                "tool_use_id" : tool_use.id,
                "content" : result
            })
        
        # tooluseblock = message.content[1]
        # name = tooluseblock.name
        # input_params = tooluseblock.input
        # tool_id = tooluseblock.id
        
        # result = get_weather(input_params['city'])
        # print(f'tool called {name}')
        # print(f'result : {result}')
        
        message = client.messages.create(
            model = "claude-sonnet-4-6",
            max_tokens = 1024,
            messages = [
                {
                    "role" : "user",
                    "content" : user_input
                },
                {
                    "role" : "assistant",
                    "content" : message.content
                },
                {
                    "role" : "user",
                    "content" : tool_results
                }
            ],
            tools = [get_weather_tool]
        )

    print(message.content[0].text)