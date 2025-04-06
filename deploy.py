import os
import shutil
import subprocess

def prepare_deployment():
    print("准备部署文件...")
    
    # 确保必要的目录存在
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    # 检查并创建必要的文件
    required_files = [
        "main.py",
        "requirements.txt",
        "vercel.json",
        "static/chat.js",
        "templates/chat.html"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 缺少必要文件 {file}")
            return False
    
    print("所有必要文件已准备就绪")
    
    # 生成二维码
    try:
        subprocess.run(["python", "scripts/generate_qr.py"], check=True)
        print("二维码生成成功")
    except subprocess.CalledProcessError:
        print("警告: 二维码生成失败，但这不会影响部署")
    
    print("\n部署说明:")
    print("1. 访问 https://vercel.com/new")
    print("2. 选择 'Import Git Repository'")
    print("3. 在 'Import Git Repository' 页面中:")
    print("   - Framework Preset: 选择 Other")
    print("   - Build Command: 留空")
    print("   - Output Directory: 留空")
    print("   - Install Command: pip install -r requirements.txt")
    print("4. 点击 'Deploy' 开始部署")
    print("\n部署完成后:")
    print("1. 复制Vercel提供的域名")
    print("2. 更新 scripts/generate_qr.py 中的URL")
    print("3. 重新运行此脚本生成新的二维码")
    
    return True

if __name__ == "__main__":
    if prepare_deployment():
        print("\n文件准备完成！请按照上述说明进行部署。") 