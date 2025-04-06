let currentLanguage = 'zh';

// 显示登录界面
function showLoginSection() {
    document.getElementById('registerSection').classList.add('d-none');
    document.getElementById('loginSection').classList.remove('d-none');
    document.getElementById('chatSection').classList.add('d-none');
}

// 显示注册界面
function showRegisterSection() {
    document.getElementById('loginSection').classList.add('d-none');
    document.getElementById('registerSection').classList.remove('d-none');
    document.getElementById('chatSection').classList.add('d-none');
}

// 显示聊天界面
function showChatSection() {
    document.getElementById('loginSection').classList.add('d-none');
    document.getElementById('registerSection').classList.add('d-none');
    document.getElementById('chatSection').classList.remove('d-none');
}

// 添加消息到聊天界面
function addMessage(message, type = 'bot') {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    if (typeof message === 'object') {
        // 处理带有主回复和后续问题的消息对象
        if (message.main_response) {
            const mainResponseDiv = document.createElement('div');
            mainResponseDiv.textContent = message.main_response;
            messageDiv.appendChild(mainResponseDiv);
        }
        
        if (message.follow_up_questions && message.follow_up_questions.length > 0) {
            const followUpDiv = document.createElement('div');
            followUpDiv.className = 'follow-up';
            followUpDiv.innerHTML = message.follow_up_questions.map(q => 
                `<button class="btn btn-link" onclick="handleFollowUp('${q}')">${q}</button>`
            ).join('<br>');
            messageDiv.appendChild(followUpDiv);
        }
    } else {
        messageDiv.textContent = message;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 显示错误消息
function showError(zhMessage, enMessage) {
    alert(`${zhMessage}\n${enMessage}`);
}

// 登录处理
async function login(event) {
    event.preventDefault();
    const studentId = document.getElementById('loginStudentId').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${studentId}&password=${password}`
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            showChatSection();
            showWelcomeMessage();
        } else {
            const error = await response.json();
            showError(
                '登录失败：' + error.detail,
                'Login failed: ' + error.detail
            );
        }
    } catch (error) {
        console.error('Error:', error);
        showError(
            '登录时发生错误',
            'Error during login'
        );
    }
}

// 验证密码复杂度
function validatePassword(password) {
    if (password.length < 8) return false;
    if (!/[A-Z]/.test(password)) return false;
    if (!/[a-z]/.test(password)) return false;
    if (!/[0-9]/.test(password)) return false;
    return true;
}

// 注册处理
async function register(event) {
    event.preventDefault();
    const studentId = document.getElementById('registerStudentId').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // 验证密码
    if (!validatePassword(password)) {
        showError(
            '密码必须包含至少8个字符，包括大写字母、小写字母和数字',
            'Password must contain at least 8 characters, including uppercase letters, lowercase letters, and numbers'
        );
        return;
    }

    if (password !== confirmPassword) {
        showError(
            '两次输入的密码不匹配',
            'Passwords do not match'
        );
        return;
    }

    // 验证邮箱格式
    if (!email.endsWith('@my.jcu.edu.au')) {
        showError(
            '请使用JCU邮箱',
            'Please use a JCU email address'
        );
        return;
    }

    try {
        const response = await fetch('/users/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: studentId,
                email: email,
                password: password
            })
        });

        if (response.ok) {
            showError(
                '注册成功！请登录',
                'Registration successful! Please login'
            );
            showLoginSection();
        } else {
            const error = await response.json();
            showError(
                '注册失败：' + error.detail,
                'Registration failed: ' + error.detail
            );
        }
    } catch (error) {
        console.error('Error:', error);
        showError(
            '注册时发生错误',
            'Error during registration'
        );
    }
}

// 退出登录
function logout() {
    localStorage.removeItem('token');
    showLoginSection();
}

// 检查是否已登录
function checkAuth() {
    const token = localStorage.getItem('token');
    if (token) {
        showChatSection();
    } else {
        showLoginSection();
    }
}

// 发送消息
async function sendMessage(event) {
    event.preventDefault();
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) return;

    // 显示用户消息
    addMessage(message, 'user');
    messageInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                message: message,
                language: currentLanguage
            })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.response) {
                let formattedResponse = '';
                
                // 处理不同类型的响应
                if (typeof data.response === 'object') {
                    if (data.response.name && data.response.hours) {
                        // 设施信息
                        formattedResponse = `${data.response.name}\n营业时间：${data.response.hours}`;
                    } else if (Array.isArray(data.response)) {
                        // 课程列表
                        formattedResponse = data.response.join('\n');
                    } else {
                        // 其他对象类型响应
                        formattedResponse = Object.entries(data.response)
                            .map(([key, value]) => {
                                if (Array.isArray(value)) {
                                    return `${key}:\n${value.join('\n')}`;
                                }
                                return `${key}: ${value}`;
                            })
                            .join('\n');
                    }
                } else {
                    formattedResponse = data.response;
                }
                
                addMessage(formattedResponse, 'bot');
            }
        } else {
            const error = await response.json();
            showError(
                '发送消息失败：' + error.detail,
                'Failed to send message: ' + error.detail
            );
        }
    } catch (error) {
        console.error('Error:', error);
        showError(
            '发送消息时发生错误',
            'Error while sending message'
        );
    }
}

// 显示欢迎消息
function showWelcomeMessage() {
    const welcomeMessage = {
        main_response: currentLanguage === 'zh'
            ? '登录成功! 欢迎使用JCU校园助手。'
            : 'Login successful! Welcome to JCU Campus Assistant.',
        follow_up_questions: currentLanguage === 'zh'
            ? [
                '校园设施和开放时间',
                '课程和专业信息',
                '学生服务和支持',
                '校园活动和社团'
            ]
            : [
                'Campus facilities and opening hours',
                'Courses and program information',
                'Student services and support',
                'Campus activities and clubs'
            ]
    };
    addMessage(welcomeMessage, 'bot');
}

// 处理后续问题
function handleFollowUp(question) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = question;
    document.getElementById('chatForm').dispatchEvent(new Event('submit'));
}

// 切换语言
function toggleLanguage() {
    const newLanguage = currentLanguage === 'zh' ? 'en' : 'zh';
    const confirmMessage = newLanguage === 'zh' 
        ? 'Are you sure you want to switch to Chinese?\nThis will affect the language of your questions and answers.' 
        : '确定要切换到英文模式吗？\n这将影响您的提问和回答的语言。';
    
    if (confirm(confirmMessage)) {
        currentLanguage = newLanguage;
        const langButton = document.getElementById('langButton');
        langButton.textContent = currentLanguage === 'zh' ? 'English' : '中文';
        
        // 显示语言切换提示消息
        const message = currentLanguage === 'zh' 
            ? '已切换到中文模式。请用中文提问，我会用中文回答。'
            : 'Switched to English mode. Please ask in English, I will respond in English.';
        addMessage(message, 'bot');
        
        // 显示欢迎消息
        showWelcomeMessage();
        
        // 更新输入框占位符
        const messageInput = document.getElementById('messageInput');
        messageInput.placeholder = currentLanguage === 'zh' 
            ? '请输入您的问题...' 
            : 'Enter your question...';
            
        // 更新按钮文本
        document.querySelector('#chatForm button[type="submit"]').textContent = 
            currentLanguage === 'zh' ? '发送' : 'Send';
        document.getElementById('clearChat').textContent = 
            currentLanguage === 'zh' ? '清空聊天' : 'Clear Chat';
        document.querySelector('button[onclick="logout()"]').textContent = 
            currentLanguage === 'zh' ? '退出登录' : 'Logout';
    }
}

// 清空聊天记录
function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = '';
    showWelcomeMessage();
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    
    // 添加事件监听器
    document.getElementById('loginForm').addEventListener('submit', login);
    document.getElementById('registerForm').addEventListener('submit', register);
    document.getElementById('chatForm').addEventListener('submit', sendMessage);
    document.getElementById('logoutButton').addEventListener('click', logout);
    document.getElementById('langButton').addEventListener('click', toggleLanguage);
}); 