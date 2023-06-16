from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 全てのオリジンからのアクセスを許可（本番環境では具体的なオリジンを指定）
    allow_credentials=True,
    allow_methods=["*"],  # 全てのHTTPメソッドを許可
    allow_headers=["*"],  # 全てのHTTPヘッダーを許可
)
class LineMessage(BaseModel):
    type: str
    replyToken: str
    source: dict
    timestamp: int
    message: dict
    app_type: Optional[str] = None

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

@app.post("/test_line_user")
async def test_line_user(msg: LineMessage):
    """
        この関数はテスト用です。
        このエンドポイントへLINEメッセージを転送してもDynamoDBへ保存できます。
        curl -X POST -H "Content-Type: application/json" -d @data.json http://localhost:8000/test_line_user
    """
    data = {
    "user_id": msg.source['userId'],
    "created_at": datetime.now().isoformat(),
    "message_id": msg.message['id'],
    "text": msg.message['text'],
    "type": msg.type,
    # "app_type": "line",
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

    # return f"{msg.type}, {msg.replyToken}, {msg.source['userId']}, {msg.source['type']}, {msg.timestamp}, {msg.message['type']}, {msg.message['id']}, {msg.message['text']}"