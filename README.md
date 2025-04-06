# JCU Assistant

一个基于FastAPI的智能校园助手聊天机器人，提供校园设施信息查询等功能。

## 功能特点

- 双语支持（中文/英文）
- 校园设施信息查询
- 实时语言切换
- 清空聊天记录
- 响应式设计
- PWA支持（可安装为本地应用）
- 支持扫码访问

## 项目结构

```
.
├── main.py                 # FastAPI主应用
├── static/                 # 静态资源
│   ├── chat.js            # 聊天界面逻辑
│   ├── styles.css         # 样式文件
│   └── manifest.json      # PWA配置
├── templates/             # HTML模板
│   └── chat.html         # 聊天界面
├── scripts/              # 工具脚本
│   ├── generate_icons.py # 生成PWA图标
│   └── generate_qr.py    # 生成访问二维码
└── requirements.txt      # 项目依赖
```

## 安装和运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行服务器：
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5500
```

3. 访问应用：
- 浏览器访问：http://localhost:5500
- 或扫描生成的二维码访问

## 开发团队

- Li Zhipeng
- Jiang Zhonghao
- Zhang Yiwen

## 技术栈

- Backend: FastAPI, Python
- Frontend: HTML5, CSS3, JavaScript
- PWA: Service Worker, Web Manifest
- 部署: Vercel
