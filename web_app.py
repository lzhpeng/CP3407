from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app import Chatbot, Event, EventDatabase
import json
import uvicorn
import traceback
import sys

# 创建FastAPI应用
app = FastAPI(title="CP3407-group4")

# 设置模板和静态文件
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化事件数据库和聊天机器人
try:
    event_database = EventDatabase()  # 创建EventDatabase实例
    chatbot = Chatbot(event_database)  # 传递EventDatabase实例给Chatbot
    print("Chatbot initialized successfully")
except Exception as e:
    print(f"Error initializing chatbot: {str(e)}")
    print(traceback.format_exc())
    sys.exit(1)

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        # 处理用户消息
        user_message = message.message.strip()
        if not user_message:
            return {
                "response": {
                    "main_response": "请输入消息。\nPlease enter a message.",
                    "follow_up_questions": []
                }
            }

        print(f"Processing message: {user_message}")  # 调试信息

        # 获取chatbot的响应
        response = chatbot.process_query(user_message)
        print(f"Chatbot response: {response}")  # 调试信息

        # 确保响应格式正确
        if isinstance(response, str):
            response = {
                "main_response": response,
                "follow_up_questions": []
            }
        elif not isinstance(response, dict):
            response = {
                "main_response": str(response),
                "follow_up_questions": []
            }

        return {"response": response}
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # 打印详细错误信息
        return {
            "response": {
                "main_response": f"抱歉，处理您的请求时出现错误：{str(e)}\nSorry, there was an error processing your request: {str(e)}",
                "follow_up_questions": []
            }
        }

if __name__ == "__main__":
    uvicorn.run("web_app:app", host="127.0.0.1", port=8000, reload=True) 