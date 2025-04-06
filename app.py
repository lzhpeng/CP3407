import json
from datetime import datetime

class Event:
    """Event class"""
    def __init__(self, event_name, event_date, location, description):
        self.event_name = event_name
        self.event_date = event_date
        self.location = location
        self.description = description

    def __str__(self):
        return f"{self.event_name} on {self.event_date} at {self.location}. Description: {self.description}"


class EventDatabase:
    """Event database management class"""
    def __init__(self, json_file="events.json"):
        self.json_file = json_file
        self.events = self.load_events()

    def load_events(self):
        """Load events data, create sample data if file doesn't exist"""
        try:
            with open(self.json_file, "r") as file:
                data = json.load(file)
                return [Event(**event) for event in data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Event data not found or corrupted. Creating new event data.")
            return self.create_sample_events()

    def create_sample_events(self):
        """Create sample event data"""
        events = [
            Event("Welcome Speech", "2025-03-01", "JCU Auditorium",
                  "An introductory speech to kick off the orientation program."),
            Event("Campus Tour", "2025-03-01", "Campus Grounds",
                  "A guided tour of the campus to help new students get familiar."),
            Event("Networking Lunch", "2025-03-01", "Student Center",
                  "A chance to meet and connect with fellow students and faculty.")
        ]
        self.save_events(events)
        return events

    def save_events(self, events):
        """Save events data to JSON file"""
        with open(self.json_file, "w") as file:
            json.dump([event.__dict__ for event in events], file, indent=4)

    def get_event_by_date(self, date):
        """Query events by date"""
        return [event for event in self.events if event.event_date == date]

    def get_event_by_name(self, name):
        """Query event by name"""
        return next((event for event in self.events if event.event_name.lower() == name.lower()), None)


class Chatbot:
    """Chatbot class"""
    def __init__(self, event_database):
        self.event_database = event_database
        self.context = {"language": "zh"}
        
        # JCU Singapore 校园信息
        self.campus_info = {
            "locations": {
            "address": {
                    "zh": "149 Sims Drive, Singapore 387380",
                    "en": "149 Sims Drive, Singapore 387380"
                }
            },
            "academic": {
                "faculties": {
                    "business": {
                        "name": {
                            "zh": "商学院",
                            "en": "Business School"
                        },
                        "programs": {
                            "zh": [
                                "会计学",
                                "商业管理",
                                "旅游酒店管理",
                                "商务"
                            ],
                            "en": [
                                "Accounting",
                                "Business",
                                "Hospitality and Tourism Management",
                                "Commerce"
                            ]
                        }
                    },
                    "it": {
                        "name": {
                            "zh": "信息技术学院",
                            "en": "School of Information Technology"
                        },
                        "programs": {
                "zh": [
                                "信息技术",
                                "游戏设计"
                            ],
                "en": [
                                "Information Technology",
                                "Games Design"
                            ]
                        }
                    },
                    "science": {
                        "name": {
                            "zh": "理学院",
                            "en": "School of Science"
                        },
                        "programs": {
                "zh": [
                                "环境科学",
                                "心理学",
                                "理学"
                            ],
                "en": [
                                "Environmental Science",
                                "Psychology",
                                "Science"
                            ]
                        }
                    }
                }
            },
            "student_services": {
                "academic_support": {
                    "services": {
                "zh": [
                            "学习中心",
                            "心理诊所",
                            "校园IT服务",
                            "职业服务"
                        ],
                "en": [
                            "Learning Centre",
                            "Psychology Clinic",
                            "IT on Campus",
                            "Career Services"
                        ]
                    }
                }
            },
            "rankings": {
                "zh": [
                    "世界大学排名前2%*",
                    "新加坡首个获得EduTrust Star认证的机构（2015年）",
                    "2024年学生来自70多个国家",
                    "*2024年上海软科世界大学学术排名"
                ],
                "en": [
                    "Ranked in the Top 2% of Universities in the World*",
                    "First Organisation to achieve EduTrust Star in Singapore in 2015",
                    "Student Enrolments from more than 70 countries in 2024",
                    "*2024 ShanghaiRanking Academic Ranking of World Universities"
                ]
            }
        }

    def process_query(self, query):
        response = {
            "main_response": "",
            "follow_up_questions": []
        }

        lang = self.context["language"]
        
        # 职业服务查询
        if "职业" in query or "career" in query.lower():
            if lang == "en":
                response["main_response"] = "Career Services at JCU Singapore provides:\n- Career counseling and planning\n- Resume and interview workshops\n- Industry networking events\n- Internship opportunities"
            else:
                response["main_response"] = "JCU新加坡校区职业服务提供：\n- 职业规划咨询\n- 简历和面试辅导\n- 行业交流活动\n- 实习机会"

        # 课程信息查询
        elif any(word in query.lower() for word in ["course", "program", "major", "study"]) or \
             any(word in query for word in ["课程", "专业", "学习"]):
            faculty_info = []
            for faculty in self.campus_info["academic"]["faculties"].values():
                programs = ", ".join(faculty["programs"][lang])
                faculty_info.append(f"{faculty['name'][lang]}: {programs}")
            
            if lang == "en":
                response["main_response"] = "JCU Singapore offers the following programs:\n" + "\n".join(faculty_info)
            else:
                response["main_response"] = "JCU新加坡校区提供以下专业课程：\n" + "\n".join(faculty_info)

        # 学生服务查询
        elif any(word in query.lower() for word in ["service", "support", "help"]) or \
             any(word in query for word in ["服务", "支持", "帮助"]):
            services = self.campus_info["student_services"]["academic_support"]["services"][lang]
            if lang == "en":
                response["main_response"] = "JCU provides the following student services:\n- " + "\n- ".join(services)
            else:
                response["main_response"] = "JCU提供以下学生服务：\n- " + "\n- ".join(services)

        # 排名和认证查询
        elif any(word in query.lower() for word in ["rank", "recognition", "achievement"]) or \
             any(word in query for word in ["排名", "认证", "成就"]):
            rankings = self.campus_info["rankings"][lang]
            if lang == "en":
                response["main_response"] = "JCU Singapore achievements:\n- " + "\n- ".join(rankings)
            else:
                response["main_response"] = "JCU新加坡校区成就：\n- " + "\n- ".join(rankings)

        # 默认回复
        else:
            if lang == "en":
                response["main_response"] = "Please ask about specific topics such as courses, student services, or university achievements."
            else:
                response["main_response"] = "请询问具体的主题，例如课程信息、学生服务或大学成就。"
        
        return response


# Create global chatbot instance
event_database = EventDatabase()
chatbot = Chatbot(event_database)

def main():
    """主函数"""
    print("欢迎使用JCU校园助手！")
    print("Welcome to JCU Campus Assistant!")
    print("你可以询问我关于校园活动、设施、服务等问题。")
    print("You can ask me about campus activities, facilities, services, etc.")
    print("输入'exit'或'quit'结束程序。")
    print("Type 'exit' or 'quit' to end the program.")
    print("-" * 50)

    # 初始化事件数据库和聊天机器人
    try:
        event_database = EventDatabase()
        chatbot = Chatbot(event_database)
        print("聊天机器人初始化成功！")
        print("Chatbot initialized successfully!")
    except Exception as e:
        print(f"初始化聊天机器人时出错：{str(e)}")
        print(f"Error initializing chatbot: {str(e)}")
        return

    while True:
        # 根据当前语言显示输入提示
        if chatbot.context["language"] == "en":
            user_input = input("\nPlease enter your question: ").strip()
        else:
            user_input = input("\n请输入你的问题：").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            print("\n感谢使用JCU校园助手。再见！")
            print("\nThank you for using JCU Campus Assistant. Goodbye!")
            break
            
        if not user_input:
            continue
            
        try:
            response = chatbot.process_query(user_input)
            print("\n" + response["main_response"])
            if response["follow_up_questions"]:
                print("\n你可能还想了解：")
                print("You might also want to know:")
                print("\n".join(response["follow_up_questions"][:2]))
            print("-" * 50)
        except Exception as e:
            print(f"\n处理请求时出错：{str(e)}")
            print(f"Error processing request: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    main()