import qrcode
import os

def generate_qr_code():
    # Vercel部署后的URL
    url = "https://jcu-assistant.vercel.app"  # 这个URL会在部署后更新
    
    # 创建二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 创建图像
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # 确保static目录存在
    if not os.path.exists("static"):
        os.makedirs("static")
    
    # 保存二维码图片
    qr_image.save("static/app_qr.png")
    print(f"二维码已生成！扫描二维码可访问：{url}")
    print("注意：此二维码可以使用手机流量或任何网络环境访问")

if __name__ == "__main__":
    generate_qr_code() 