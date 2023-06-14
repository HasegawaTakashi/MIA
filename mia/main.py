from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/index", response_class=HTMLResponse)
async def read_items():
    with open('Index.html', 'r') as f:
        html_content = f.read()
    return html_content

@app.get("/dynamodb")
async def get_api_gw():
    host_url = os.getenv('API_GW_URL')
    environment = os.getenv('DEVELOPMENT_ENVIRONMENT')
    url = host_url + environment

    params = {
        'message_id': os.getenv('MESSAGE_ID'),
        'user_id': os.getenv('USER_ID')
    }

    response = requests.get(url, params=params)

    return response.json()

@app.get("/line_message")
async def post_line_message():
    data = {
    "message_id": "4",
    "user_id": "1",
    "type": "text",
    "text": "you are shock !!!"
    }

    host_url = os.getenv('API_GW_URL')
    environment = os.getenv('DEVELOPMENT_ENVIRONMENT')
    url = host_url + environment

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to post message to API Gateway"}

    return response.json()