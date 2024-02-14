# GPT2Notion

> Notion Management with OpenAI API

## Introduction

GPT2Notion provides an API to simplify the process of submitting to-do items to Notion. 

It automates the task of filling in details such as:
* Start/end time,
* Title,
* Details,
* and more.

By leveraging the power of OpenAI's GPT-3.5 language model, GPT2Notion enables users to generate comprehensive to-do items effortlessly.

## Installation and Setup

# Notion Setup

1. Go to https://www.notion.so/my-integrations

2. Create and new integration. Select the workplace you are integrating. Copy and Save the integration key (secret_xxxxxxxxx...) for ".env".

3. Go to the database page you would like to connect. Find your database key in the url. https://www.notion.so/**xxxxxxxxxxxa**?v=... Save it up for ".env" .

4. In the database page, go to more option in the top-right-hand corner and find "Add connections". Find the integration you added previously.

# Script Setup

To set up GPT2Notion locally, follow these steps:

1. Install Poetry: GPT2Notion uses Poetry as a dependency manager. Start by installing Poetry using the following command:
   ```
   pip install poetry
   ```

2. Install project dependencies: Once Poetry is installed, navigate to the project directory and execute the following command to install the required dependencies:
   ```
   poetry install
   ```
   
3. Populate `.env`: Fill in the appropriate API keys and make `.env` in the same directory of `gpt2notion.py`
   
   Use `template.env` as a sample. 

5. Run the application: After installing the dependencies, run the GPT2Notion application using the following command:
   ```
   poetry run python gpt2notion.py
   ```


**Steps to securely host the server over the internet using self-hosting / cloud hosting will be added soon.**

## Usage

To submit a to-do item to Notion using GPT2Notion, interact with the application's endpoint API. 

You need to send a POST request to `/assistant` with a JSON payload containing a `"prompt"` key. 

The value of the `"prompt"` key should be the task description for which you want GPT2Notion to generate the to-do item. The endpoint will return the response from ChatGPT summarizing what has been done. 

## Testing ChatGPT API only

Since integration with Notion proves to be tricky, to separate variables, use `NOTION_DRYRUN=1` to bypass Notion integration. 

What would otherwise be submitted to Notion will be printed to console instead. 

Manually inspect for any errors before enabling Notion integration. 

## Issues with incompatible ChatGPT models

**Only new OpenAI API version support to use `tools` parameter for calling Notion API.**

**Only new ChatGPT models supports to use `tools` parameter for calling Notion API.**

If you see `openai.NotFoundError: Error code: 404 - {'error': {'message': 'Unrecognized request argument supplied: tools', 'type': 'invalid_request_error', 'param': None, 'code': None}}`, the model and/or the API does not implement the `tools` parameter. 

Try something else. 

Important note for HKUST Azure OpenAI API users:

> From [the official documentation](https://itsc.hkust.edu.hk/services/it-infrastructure/azure-openai-api-service), "Supported OpenAI API Models and Versions" does NOT support specifying model version such as `gpt-35-turbo-1106` unlike other API endpoints!
>
> It just occurs that `gpt-35-turbo-16k` supports to use `tools` parameter, but not `gpt-35-turbo`.
>
> In an ideal world, HKUST should allow specifying model version. However, the current arrangement may be due to insurmountable limitations. 

---

This is a personal project initiated because I wanted to do voice control for my Notion eco-system.
This Read Me will be updated soon. 
