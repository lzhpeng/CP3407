import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import reset_db

def main():
    print("正在重置数据库...")
    if reset_db():
        print("数据库重置成功！")
    else:
        print("数据库重置失败！")

if __name__ == "__main__":
    main() 