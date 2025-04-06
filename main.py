from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
import database
from models import init_db, Base, UserCreate, UserRead, User, Event, EventCreate, EventRead
import os
import re

class EventDatabase:
    def __init__(self):
        self.events = []
        self.campus_info = {
            "address": {
                "zh": "新加坡实必道149号，邮编387380",
                "en": "149 Sims Drive, Singapore 387380"
            },
            "facilities": {
                "library": {
                    "name": {
                        "zh": "图书馆",
                        "en": "Learning Commons"
                    },
                    "hours": {
                        "zh": "周一至周五: 8:00-22:00, 周末: 9:00-18:00",
                        "en": "Monday to Friday: 8:00-22:00, Weekend: 9:00-18:00"
                    }
                },
                "computer_labs": {
                    "name": {
                        "zh": "电脑实验室",
                        "en": "Computer Labs"
                    },
                    "hours": {
                        "zh": "24小时开放",
                        "en": "Open 24 Hours"
                    }
                },
                "cafeteria": {
                    "name": {
                        "zh": "食堂",
                        "en": "Food Court"
                    },
                    "hours": {
                        "zh": "周一至周五: 7:00-19:00, 周末: 8:00-15:00",
                        "en": "Monday to Friday: 7:00-19:00, Weekend: 8:00-15:00"
                    }
                }
            },
            "faculties": {
                "business": {
                    "zh": {
                        "name": "商学院",
                        "programs": ["工商管理学士", "工商管理硕士"]
                    },
                    "en": {
                        "name": "Faculty of Business",
                        "programs": ["Bachelor of Business", "Master of Business Administration"]
                    }
                },
                "it": {
                    "zh": {
                        "name": "信息技术学院",
                        "programs": ["信息技术学士", "信息技术硕士"]
                    },
                    "en": {
                        "name": "Faculty of Information Technology",
                        "programs": ["Bachelor of Information Technology", "Master of Information Technology"]
                    }
                },
                "science": {
                    "zh": {
                        "name": "理学院",
                        "programs": ["理学学士", "理学硕士"]
                    },
                    "en": {
                        "name": "Faculty of Science",
                        "programs": ["Bachelor of Science", "Master of Science"]
                    }
                }
            },
            "student_services": {
                "academic_support": {
                    "zh": "学术支持服务",
                    "en": "Academic Support Services"
                },
                "career_services": {
                    "zh": "就业指导服务",
                    "en": "Career Services"
                },
                "student_life": {
                    "zh": "学生生活服务",
                    "en": "Student Life Services"
                },
                "health_services": {
                    "zh": "健康服务",
                    "en": "Health Services"
                }
            },
            "important_dates": {
                "semester_1": {
                    "zh": "2月至6月",
                    "en": "February to June"
                },
                "semester_2": {
                    "zh": "7月至11月",
                    "en": "July to November"
                },
                "holidays": {
                    "zh": ["新年", "春节", "开斋节", "国庆日"],
                    "en": ["New Year", "Chinese New Year", "Hari Raya", "National Day"]
                }
            }
        }

class Chatbot:
    def __init__(self, event_database):
        self.event_database = event_database
        self.context = {"language": "zh"}

    def get_facility_response(self, facility, lang):
        name = facility['name'][lang]
        hours = facility['hours'][lang]
        if lang == 'zh':
            return f"{name}\n营业时间：{hours}"
        else:
            return f"{name}\nOpening Hours: {hours}"

    def is_chinese_query(self, query):
        # 检查是否包含中文字符
        return any('\u4e00' <= char <= '\u9fff' for char in query)

    def is_english_query(self, query):
        # 检查是否只包含英文字符和基本标点
        return all(ord(char) < 128 for char in query)

    def process_query(self, query):
        lang = self.context.get("language", "zh")
        
        # 检查查询语言是否匹配当前模式
        if lang == 'zh' and not self.is_chinese_query(query):
            return {
                "response": {
                    "main_response": "已切换到中文模式。请用中文提问，我会用中文回答。",
                    "follow_up_questions": [
                        "登录成功！欢迎使用JCU校园助手。",
                        "校园设施和开放时间",
                        "课程和专业信息",
                        "学生服务和支持",
                        "校园活动和社团"
                    ]
                }
            }
        elif lang == 'en' and not self.is_english_query(query):
            return {
                "response": {
                    "main_response": "Switched to English mode. Please ask in English, I will respond in English.",
                    "follow_up_questions": [
                        "Login successful! Welcome to JCU Campus Assistant.",
                        "Campus facilities and opening hours",
                        "Courses and program information",
                        "Student services and support",
                        "Campus activities and clubs"
                    ]
                }
            }
        
        # 中文模式
        if lang == 'zh':
            if any(word in query for word in ["图书馆", "阅览室", "自习"]):
                facility = self.event_database.campus_info["facilities"]["library"]
                return {"response": self.get_facility_response(facility, 'zh')}
            elif any(word in query for word in ["电脑", "计算机", "机房"]):
                facility = self.event_database.campus_info["facilities"]["computer_labs"]
                return {"response": self.get_facility_response(facility, 'zh')}
            elif any(word in query for word in ["食堂", "餐厅", "吃饭"]):
                facility = self.event_database.campus_info["facilities"]["cafeteria"]
                return {"response": self.get_facility_response(facility, 'zh')}
            elif any(word in query for word in ["课程", "专业", "学习", "学科"]):
                faculties = self.event_database.campus_info["faculties"]
                response = "可选专业课程：\n"
                for faculty_key, faculty_info in faculties.items():
                    faculty_data = faculty_info['zh']
                    response += f"\n{faculty_data['name']}：\n"
                    response += "\n".join(f"- {program}" for program in faculty_data['programs'])
                return {"response": response}
            elif any(word in query for word in ["服务", "帮助", "支持"]):
                services = self.event_database.campus_info["student_services"]
                response = "学生服务：\n" + "\n".join(f"- {service['zh']}" for service in services.values())
                return {"response": response}
            elif any(word in query for word in ["时间", "日期", "假期", "放假"]):
                dates = self.event_database.campus_info["important_dates"]
                response = "重要日期：\n"
                response += f"\n第一学期：{dates['semester_1']['zh']}"
                response += f"\n第二学期：{dates['semester_2']['zh']}"
                response += f"\n\n节假日：\n" + "\n".join(f"- {date}" for date in dates['holidays']['zh'])
                return {"response": response}
            else:
                return {"response": "抱歉，我不太理解您的问题。您可以询问：\n- 图书馆开放时间\n- 电脑实验室使用\n- 食堂营业时间\n- 专业课程信息\n- 学生服务\n- 校历和重要日期"}
        
        # 英文模式
        else:
            if any(word in query.lower() for word in ["library", "reading", "study room"]):
                facility = self.event_database.campus_info["facilities"]["library"]
                return {"response": self.get_facility_response(facility, 'en')}
            elif any(word in query.lower() for word in ["computer", "lab", "pc"]):
                facility = self.event_database.campus_info["facilities"]["computer_labs"]
                return {"response": self.get_facility_response(facility, 'en')}
            elif any(word in query.lower() for word in ["food", "cafeteria", "dining", "eat"]):
                facility = self.event_database.campus_info["facilities"]["cafeteria"]
                return {"response": self.get_facility_response(facility, 'en')}
            elif any(word in query.lower() for word in ["course", "program", "study", "major"]):
                faculties = self.event_database.campus_info["faculties"]
                response = "Available Programs:\n"
                for faculty_key, faculty_info in faculties.items():
                    faculty_data = faculty_info['en']
                    response += f"\n{faculty_data['name']}:\n"
                    response += "\n".join(f"- {program}" for program in faculty_data['programs'])
                return {"response": response}
            elif any(word in query.lower() for word in ["service", "help", "support"]):
                services = self.event_database.campus_info["student_services"]
                response = "Student Services:\n" + "\n".join(f"- {service['en']}" for service in services.values())
                return {"response": response}
            elif any(word in query.lower() for word in ["date", "time", "holiday", "break"]):
                dates = self.event_database.campus_info["important_dates"]
                response = "Important Dates:\n"
                response += f"\nSemester 1: {dates['semester_1']['en']}"
                response += f"\nSemester 2: {dates['semester_2']['en']}"
                response += f"\n\nHolidays:\n" + "\n".join(f"- {date}" for date in dates['holidays']['en'])
                return {"response": response}
            else:
                return {"response": "Sorry, I don't quite understand your question. You can ask about:\n- Library hours\n- Computer lab access\n- Cafeteria hours\n- Academic programs\n- Student services\n- Academic calendar and important dates"}

# 初始化数据库和聊天机器人
init_db()
event_database = EventDatabase()
chatbot = Chatbot(event_database)

app = FastAPI()

# 确保目录存在
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 设置模板
templates = Jinja2Templates(directory="templates")

# 安全配置
SECRET_KEY = "your-secret-key"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic模型
class UserBase(BaseModel):
    username: str = Field(..., pattern=r'^\d{8}$', description="8位数字学号")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9_.+-]+@my\.jcu\.edu\.au$', description="JCU邮箱地址")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    event_name: str
    event_date: datetime
    location: str
    description: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime
    creator_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# 辅助函数
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = database.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# 聊天机器人路由
class ChatMessage(BaseModel):
    message: str
    language: str = "zh"

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(message: ChatMessage):
    chatbot.context["language"] = message.language
    response = chatbot.process_query(message.message)
    return response

# 路由
@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = database.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误 | Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    if len(user.username) != 8 or not user.username.isdigit():
        raise HTTPException(
            status_code=400,
            detail="学号必须是8位数字 | Student ID must be 8 digits"
        )
        
    if not user.email.endswith("@my.jcu.edu.au"):
        raise HTTPException(
            status_code=400,
            detail="请使用JCU邮箱 | Please use JCU email"
        )
        
    if not validate_password(user.password):
        raise HTTPException(
            status_code=400,
            detail="密码必须包含大小写字母和数字 | Password must contain uppercase, lowercase letters and numbers"
        )
        
    db_user = database.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="邮箱已被注册 | Email already registered"
        )
    
    db_user = database.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="学号已被注册 | Student ID already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    return database.create_user(db, user.username, user.email, hashed_password)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/events/", response_model=Event)
def create_event(
    event: EventCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    return database.create_event(
        db,
        event.event_name,
        event.event_date,
        event.location,
        event.description,
        current_user.id
    )

@app.get("/events/", response_model=List[Event])
def read_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    events = database.get_events_by_creator(db, current_user.id)
    return events[skip : skip + limit]

@app.get("/events/{event_id}", response_model=Event)
def read_event(
    event_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = database.get_event_by_id(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this event")
    return db_event

@app.put("/events/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    event: EventCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = database.get_event_by_id(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this event")
    return database.update_event(
        db,
        event_id,
        event.event_name,
        event.event_date,
        event.location,
        event.description
    )

@app.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = database.get_event_by_id(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    if database.delete_event(db, event_id):
        return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=500, detail="Error deleting event")

# 验证密码复杂度
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True 
    return True 