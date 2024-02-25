# Importing packages.
import os
import json
import httpx
from dotenv import find_dotenv, load_dotenv
from datetime import datetime, timezone
from openai import OpenAI, AzureOpenAI
from flask import Flask, request, jsonify

from setup_notion import NotionDatabase
from setup_callables import CallablesProps
from setup_callables import Callables
from setup_callables import callable_list

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

NOTION_INTEGRATION_1_KEY = os.getenv("NOTION_INTEGRATION_1_KEY")
NOTION_INTEGRATION_2_KEY = os.getenv("NOTION_INTEGRATION_2_KEY")
NOTION_DATABASE_1_ID = os.getenv("NOTION_DATABASE_1_ID")
NOTION_DATABASE_2_ID = os.getenv("NOTION_DATABASE_2_ID")
NOTION_DATABASE_3_ID = os.getenv("NOTION_DATABASE_3_ID")

my_notion_task_database = NotionDatabase(
    NOTION_INTEGRATION_1_KEY, 
    NOTION_DATABASE_2_ID,
    name = "Tasks",
    dry_run = NOTION_DRYRUN
    )

print(my_notion_task_database.query_pages(True)[0])