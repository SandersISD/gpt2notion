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

4. Run the application: After installing the dependencies, run the GPT2Notion application using the following command:
   ```
   poetry run python gpt2notion.py
   ```

**Steps to securely host the server over the internet using self-hosting / cloud hosting will be added soon.**

## Usage

To submit a to-do item to Notion using GPT2Notion, interact with the application's endpoint API. 

You need to send a POST request to `/assistant` with a JSON payload containing a `"prompt"` key. 

The value of the `"prompt"` key should be the task description for which you want GPT2Notion to generate the to-do item. The endpoint will return the response from ChatGPT summarizing what has been done. 

---

This is a personal project initiated because I wanted to do voice control for my Notion eco-system.
This Read Me will be updated soon. 
