from PIL import Image
import os

def generate_icons(input_icon, output_dir):
    """Generate icons of different sizes from the input icon."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    img = Image.open(input_icon)

    for size in sizes:
        resized = img.resize((size, size), Image.LANCZOS)
        output_path = os.path.join(output_dir, f'icon-{size}x{size}.png')
        resized.save(output_path, 'PNG')
        print(f'Generated {output_path}')

if __name__ == '__main__':
    # 确保static/icons目录存在
    icons_dir = os.path.join('static', 'icons')
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    # 生成图标
    input_icon = 'app_icon.png'  # 请将此替换为您的源图标
    generate_icons(input_icon, icons_dir) 