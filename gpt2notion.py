# Importing packages.
import os
import requests
import json
import httpx
from dotenv import find_dotenv, load_dotenv
from datetime import datetime, timezone
from openai import OpenAI
from flask import Flask, request, jsonify

# Obtaining values in .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Please create your own .env file for the script.
OPENAI_API_URL = os.getenv("OPENAI_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")
NOTION_INTEGRATION_KEY = os.getenv("NOTION_INTEGRATION_KEY")
NOTION_DATABASE_1_ID = os.getenv("NOTION_DATABASE_1_ID")
NOTION_VERSION = os.getenv("NOTION_VERSION")
NOTION_CREATE_URL = os.getenv("NOTION_CREATE_URL")
NOTION_DATABASE_1_QUERY_URL = os.getenv("NOTION_DATABASE_1_QUERY_URL")

# Obtain the Current time for prompting the model
current_time = datetime.now().isoformat()
print(current_time)


# Initialise Headers for requests. Required by Notion 
notion_headers = {
    "Authorization": "Bearer " + NOTION_INTEGRATION_KEY,
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

# Define values for python to successfully interpret "null", "true", and "false" in the dictionary below. 
# I am not sure if theres other way but it is needed for now to make things work.
null = None
true = True
false = False

# Creating Page in Notion by sending the page data
def notionCreatePage(page_prop: dict, database):
    
    print("Creating a Page in Notion with:\t" + database)

    create_url = NOTION_CREATE_URL

    page_data = {
        "parent": {
            "database_id": database
        },
        "properties": page_prop
    }

    res = requests.post(create_url, headers=notion_headers, json=page_data)
    print(res.status_code)
    return res

# Preparing Sendable page data for creating a event
# Please Modify Your own structure of the properties in order for the page to be successfully create
def notionCreateEvent(event="", start=null, end=null, details=""):

    # Please refer to the prompt about creating the event
    if end == 'n': 
        end=null

    print("Preparing An Event...")

    data = {
        "Date": {
            "date": {
                "start": start,
                "end": end,
                "time_zone": null
            }
        },
        "Description": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": details,
                        "link": null
                    },
                }
            ]
        },
        "Name": {
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": event,
                        "link": null
                    },
                    "annotations": {
                        "bold": false,
                        "italic": false,
                        "strikethrough": false,
                        "underline": false,
                        "code": false,
                        "color": "default"
                    },
                    "plain_text": event,
                    "href": null
                }
            ]
        }
    }

    print("Created Data:\t")
    print(data)
    print("-------------")

    notionCreatePage(data, NOTION_DATABASE_1_ID)

    return True

# Setup OpenAI Client
openai_client = OpenAI(
    base_url = OPENAI_API_URL,
    api_key = OPENAI_API_KEY,
    http_client=httpx.Client(
            base_url = OPENAI_API_URL,
            follow_redirects=True,
    ),
)

# Define the tools/functions list for the model to use. Make sure the functions' names is exactly the same with the ones you define in the script.
# In my case, e.g. notionCreateEvent was defined above and put in the list.
openai_tools_list = [
    {
        "type": "function",
        "function": {
            "name": "notionCreateEvent",
            "description": "create an event in notion",
            "parameters": {
                "type": "object",
                "properties": {
                    "event": {
                        "type": "string",
                        "description": "The name of the event.",
                    },
                    "start": {
                        "type": "string",
                        "description": "The start time of the event. e.g. 2024-02-02T13:00:00.000+08:00. The current time is " + current_time,
                    },
                    "end": {
                        "type": "string",
                        "description": "The end time of the event. e.g. 2024-02-02T18:00:00.000+08:00. The current time is " + current_time + \
                            ". Return 'n' if there is no ending time for the event.",
                    },
                    "details": {
                        "type": "string",
                        "description": "The extra details of the event. Return nothing if there is no detail for the event",
                    },
                },
                "required": ["event", "start","end","details"],
            },
        }
    },
]

def openaiChatCompletionRequest(messages, tools=None, tool_choice=None, model=OPENAI_API_MODEL):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
    )
    return response

# Input the prompt to run the function defined in the script. Output a natural language message concluding the functions the model have done.
def openaiRunFunction(prompt):
    messages = []
    finished_functions_list = {}

    messages.append({"role": "system", "content": "You are a assitant to do tasks by plugging values into function. \
                     Determine tasks you need to do by the input prompt of the user. Don't make assumptions about what values to plug into functions."})
    messages.append({"role": "user", "content": prompt})
    chat_response = openaiChatCompletionRequest(
        messages, tools=openai_tools_list
    )
    assistant_message = chat_response.choices[0].message

    print(assistant_message)

    for call in assistant_message.tool_calls:
        chosen_function = eval(call.function.name)
        function_paramas = json.loads(call.function.arguments)
        chosen_function(**function_paramas)
        finished_functions_list[call.id] = [call.function.name, call.function.arguments]

    messages = []
    messages.append({"role": "system", "content": "Another AI have done tasks with functions and the Finished functions list given.\
                      Make an conclusion message replying the user listing the tasks done. Make it short and simple. Details can be ignored."})
    messages.append({"role": "user", "content": str(finished_functions_list)})
    reply_response = openaiChatCompletionRequest(
        messages
    )
    reply_message = reply_response.choices[0].message.content
        
    return reply_message

# Creating Flask. I have port-forward the access of the port 5000  
app = Flask(__name__)

@app.route("/assitant", methods=['POST'])
def obtain_payload():
    payload = request.get_data()
    payload = json.loads(payload)
    prompt = payload["prompt"]
    if prompt:     
        reply = openaiRunFunction(prompt)
    else:
        reply = "No Data was inputed."
    return reply

if __name__ == "__main__":
    app.run("0.0.0.0")


