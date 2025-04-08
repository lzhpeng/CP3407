# JCU校园助手 | JCU Campus Assistant

访问网站 | Visit Website: [https://lzhpeng.github.io/CP3407-group4/](https://lzhpeng.github.io/CP3407-group4/)

## 功能特点 | Features

### 1. 用户管理 | User Management
- 注册功能 | Registration
  - 支持8位学号验证 | 8-digit student ID validation
  - JCU邮箱验证 (@my.jcu.edu.au) | JCU email validation
  - 实时检查学号是否已被注册 | Real-time student ID availability check
  - 实时检查邮箱是否已被使用 | Real-time email availability check
  - 密码确认功能 | Password confirmation

- 登录功能 | Login
  - 学号和密码验证 | Student ID and password verification
  - 实时提示学号状态 | Real-time student ID status feedback

### 2. 聊天功能 | Chat Features
- 支持中英双语 | Bilingual support (Chinese/English)
- 一键切换语言 | One-click language switch
- 常见问题快速回复 | Quick responses for common questions:
  - 校园设施和开放时间 | Campus facilities and opening hours
  - 课程和专业信息 | Courses and program information
  - 学生服务和支持 | Student services and support
  - 校历和重要日期 | Academic calendar and important dates
- 清空聊天记录 | Clear chat history

### 3. 数据管理 | Data Management
- 本地数据存储 | Local data storage
  - 使用浏览器的 localStorage 作为数据库 | Using browser's localStorage as database
  - 数据格式：用户信息（学号、邮箱、密码）| Data format: User info (student ID, email, password)
  - 数据持久化：关闭浏览器后数据仍然保留 | Data persistence: Data remains after browser closes
- 一键重置所有数据 | One-click data reset
- 自动保存用户信息 | Automatic user information saving

### 4. 界面特性 | UI Features
- 响应式设计 | Responsive design
- 用户友好的提示信息 | User-friendly tooltips
- 实时反馈信息 | Real-time feedback messages
- 简洁现代的界面设计 | Clean and modern interface

## 使用说明 | Usage Instructions

### 注册新用户 | Register New User
1. 点击"注册"链接 | Click "Register" link
2. 输入8位学号 | Enter 8-digit student ID
3. 输入JCU邮箱 | Enter JCU email
4. 设置密码 | Set password
5. 确认密码 | Confirm password

### 登录系统 | Login System
1. 输入学号 | Enter student ID
2. 输入密码 | Enter password
3. 点击登录按钮 | Click login button

### 使用聊天功能 | Using Chat
1. 选择语言（中文/英文）| Choose language (Chinese/English)
2. 点击预设问题或输入自定义问题 | Click preset questions or enter custom questions
3. 查看系统回复 | View system responses

### 重置数据 | Reset Data
1. 登录后点击"重置数据"按钮 | Click "Reset Data" button after login
2. 确认重置操作 | Confirm reset operation
3. 系统将清除所有用户数据 | All user data will be cleared

## 技术说明 | Technical Details
- 纯前端应用 | Frontend-only application
- 数据存储 | Data Storage
  - 使用浏览器的 localStorage 作为轻量级数据库 | Using browser's localStorage as lightweight database
  - 数据以 JSON 格式存储 | Data stored in JSON format
  - 支持数据的增删改查操作 | Support CRUD operations
  - 数据在浏览器清除缓存前一直保留 | Data persists until browser cache is cleared
- 基于 Bootstrap 5 构建 | Built with Bootstrap 5
- 支持PWA | PWA supported
