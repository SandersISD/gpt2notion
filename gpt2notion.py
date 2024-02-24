# Importing packages.
import os
import requests
import json
import httpx
from dotenv import find_dotenv, load_dotenv
from datetime import datetime, timezone
from openai import OpenAI, AzureOpenAI
from flask import Flask, request, jsonify

# Obtaining values in .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Please create your own .env file for the script.
USE_AZURE = int(os.getenv("USE_AZURE"))

OPENAI_API_URL = os.getenv("OPENAI_API_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")

NOTION_DRYRUN = int(os.getenv("NOTION_DRYRUN"))

NOTION_INTEGRATION_KEY = os.getenv("NOTION_INTEGRATION_KEY")
NOTION_DATABASE_1_ID = os.getenv("NOTION_DATABASE_1_ID")
NOTION_VERSION = os.getenv("NOTION_VERSION")
NOTION_CREATE_URL = os.getenv("NOTION_CREATE_URL")
NOTION_DATABASE_1_QUERY_URL = os.getenv("NOTION_DATABASE_1_QUERY_URL")

if NOTION_DRYRUN:
    print("Notion running in dry-run mode...")
else:
    print("Notion running in Normal mode...")

if USE_AZURE:
    print("Use AZURE")
    # Setup OpenAI Client
    openai_client = AzureOpenAI(
    api_key=OPENAI_API_KEY,  
    api_version=OPENAI_API_VERSION,
    azure_endpoint=OPENAI_API_URL
    )
else:
    print("Use OPENAI")
    # Setup OpenAI Client
    openai_client = OpenAI(
        base_url = OPENAI_API_URL,
        api_key = OPENAI_API_KEY,
        http_client=httpx.Client(
                base_url = OPENAI_API_URL,
                follow_redirects=True,
        ),
    )

from setup_notion import NotionDatabase
from setup_callables import *

#Setting up database
MyNotionEvents = NotionDatabase(
    NOTION_INTEGRATION_KEY, 
    NOTION_DATABASE_1_ID,
    name = "Event",
    dry_run = NOTION_DRYRUN
    )

# Preparing Sendable page data for creating a event
# Please Modify Your own structure of the properties in order for the page to be successfully create
def notionCreateEvent(event="", start=None, end=None, details=""):

    # Please refer to the prompt about creating the event
    if end == 'n': 
        end=None

    print("Preparing An Event...")

    data = {
        "Date": {
            "date": {
                "start": start,
                "end": end,
                "time_zone": None
            }
        },
        "Description": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": details,
                        "link": None
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
                        "link": None
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": event,
                    "href": None
                }
            ]
        }
    }

    print("Created Data:\t")
    print(data)
    print("-------------")

    MyNotionEvents.createPage(data)

    return True

Call_notionCreateEvent = Callables(
    notionCreateEvent,
    "Create an event in notion",
    Callables_Props(
        "event",
        "string", 
        "The name of the event.", 
        True
    ),
    Callables_Props(
        "start",
        "string", 
        "The start time of the event. e.g. 2024-02-02T13:00:00.000+08:00. \
            The current time is " + datetime.now().isoformat(), 
        True
    ),
    Callables_Props(
        "end",
        "string", 
        "The end time of the event. e.g. 2024-02-02T18:00:00.000+08:00. \
            The current time is " + datetime.now().isoformat() + \
                ". Return 'n' if there is no ending time for the event.", 
        True
    ),
    Callables_Props(
        "details",
        "string", 
        "The extra details of the event. Return nothing if there is no detail for the event", 
        True
    )
)

tool_list = CallableList(
    Call_notionCreateEvent
)

def openaiChatCompletionRequest(messages, tools=None, tool_choice=None, model=OPENAI_API_MODEL):
    if tools:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools, 
            tool_choice="auto"
            # tool_choice is auto, check docs
        )
    else:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
        )
    return response

def humanified_finished_functions_list(finished_functions_list):
    return ". ".join(f"Function name: ```{func_name}```, function paramaters: ```{';'.join(f'{k}={v}' for k,v in json.loads(func_args).items())}```" for func_name, func_args in finished_functions_list.values())

# Input the prompt to run the function defined in the script. Output a natural language message concluding the functions the model have done.
def openaiRunFunction(prompt, humanify_input_for_summarization=True, json_out=False):
    print("humanify_input_for_summarization:", humanify_input_for_summarization)
    print("json_out:", json_out)
    messages = []
    finished_functions_list = {}

    messages.append({"role": "system", "content": "You are a assitant to do tasks by plugging values into function. \
                     Determine tasks you need to do by the input prompt of the user. Don't make assumptions about what values to plug into functions."})
    messages.append({"role": "user", "content": prompt})
    print(tool_list)
    chat_response = openaiChatCompletionRequest(
        messages, tools= CallableList(
            Call_notionCreateEvent
        )   
    )
    assistant_message = chat_response.choices[0].message

    print(assistant_message)

    for call in assistant_message.tool_calls:
        chosen_function = eval(call.function.name)
        function_paramas = json.loads(call.function.arguments)
        chosen_function(**function_paramas)
        finished_functions_list[call.id] = [call.function.name, call.function.arguments]

    print(finished_functions_list)

    ai_summation_input = humanified_finished_functions_list(finished_functions_list)
    messages = []
    messages.append({"role": "system", "content": "Another AI have done tasks with functions and the Finished functions list given.\
                      Make an conclusion message replying the user listing the tasks done. Make it short and simple. Details can be ignored."})
    messages.append({"role": "user", "content": ai_summation_input if humanify_input_for_summarization else str(finished_functions_list)})
    reply_response = openaiChatCompletionRequest(
        messages
    )
    reply_message = reply_response.choices[0].message.content

    output_json = {"message":reply_message, "function_calls": list(finished_functions_list.values()), "ai_summation_input": ai_summation_input}
        
    return json.dumps(output_json) if json_out else reply_message

# Creating Flask. I have port-forward the access of the port 5000  
app = Flask(__name__)

@app.route("/assistant", methods=['POST']) # past was assitant
def obtain_payload():
    payload = request.get_data()
    payload = json.loads(payload)
    prompt = payload["prompt"]
    humanify2 = payload.get('humanify2', True)
    json_out = payload.get('json', False)
    if prompt:   
        reply = openaiRunFunction(prompt, humanify2, json_out)
    else:
        reply = "No Data was inputed."
    return reply

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)


