let token = localStorage.getItem('token');

// 添加基础URL
const API_BASE_URL = 'http://127.0.0.1:5500';

// 显示/隐藏表单
function showLoginForm() {
    document.getElementById('loginForm').classList.remove('d-none');
    document.getElementById('registerForm').classList.add('d-none');
    document.getElementById('eventList').classList.add('d-none');
    document.getElementById('createEventForm').classList.add('d-none');
}

function showRegisterForm() {
    document.getElementById('loginForm').classList.add('d-none');
    document.getElementById('registerForm').classList.remove('d-none');
    document.getElementById('eventList').classList.add('d-none');
    document.getElementById('createEventForm').classList.add('d-none');
}

function showEventList() {
    document.getElementById('loginForm').classList.add('d-none');
    document.getElementById('registerForm').classList.add('d-none');
    document.getElementById('eventList').classList.remove('d-none');
    document.getElementById('createEventForm').classList.add('d-none');
    loadEvents();
}

function showCreateEventForm() {
    document.getElementById('loginForm').classList.add('d-none');
    document.getElementById('registerForm').classList.add('d-none');
    document.getElementById('eventList').classList.add('d-none');
    document.getElementById('createEventForm').classList.remove('d-none');
}

// 认证相关函数
async function login(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': username,
                'password': password,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            localStorage.setItem('token', token);
            updateAuthUI();
            showEventList();
        } else {
            const errorData = await response.json();
            alert('登录失败：' + (errorData.detail || '请检查用户名和密码'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('登录时发生错误，请重试');
    }
}

async function register(event) {
    event.preventDefault();
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    // 基本验证
    if (username.length < 3) {
        alert('用户名至少需要3个字符');
        return;
    }
    if (password.length < 6) {
        alert('密码至少需要6个字符');
        return;
    }
    if (!email.includes('@')) {
        alert('请输入有效的电子邮箱地址');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            alert('注册成功，请登录');
            showLoginForm();
        } else {
            let errorMessage = '注册失败：';
            if (data.detail) {
                if (typeof data.detail === 'string') {
                    errorMessage += data.detail;
                } else if (Array.isArray(data.detail)) {
                    errorMessage += data.detail.map(err => err.msg).join(', ');
                }
            } else {
                errorMessage += '未知错误';
            }
            alert(errorMessage);
            console.error('Registration error:', data);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('注册时发生错误，请重试');
    }
}

function logout() {
    token = null;
    localStorage.removeItem('token');
    updateAuthUI();
    showLoginForm();
}

// 事件相关函数
async function loadEvents() {
    try {
        const response = await fetch(`${API_BASE_URL}/events/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const events = await response.json();
            const eventsContainer = document.getElementById('events');
            eventsContainer.innerHTML = '';

            events.forEach(event => {
                const eventCard = createEventCard(event);
                eventsContainer.appendChild(eventCard);
            });
        } else {
            const errorData = await response.json();
            alert('加载事件失败：' + (errorData.detail || '未知错误'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('加载事件时发生错误，请重试');
    }
}

function createEventCard(event) {
    const div = document.createElement('div');
    div.className = 'event-card';
    div.innerHTML = `
        <h3>${event.event_name}</h3>
        <div class="event-date">${new Date(event.event_date).toLocaleString()}</div>
        <div class="event-location">📍 ${event.location}</div>
        <div class="event-description">${event.description}</div>
        <div class="event-actions">
            <button class="btn btn-sm btn-primary" onclick="editEvent(${event.id})">编辑</button>
            <button class="btn btn-sm btn-danger" onclick="deleteEvent(${event.id})">删除</button>
        </div>
    `;
    return div;
}

async function createEvent(event) {
    event.preventDefault();
    const eventData = {
        event_name: document.getElementById('eventName').value,
        event_date: document.getElementById('eventDate').value,
        location: document.getElementById('eventLocation').value,
        description: document.getElementById('eventDescription').value,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/events/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(eventData),
        });

        if (response.ok) {
            alert('事件创建成功');
            showEventList();
        } else {
            const errorData = await response.json();
            alert('创建事件失败：' + (errorData.detail || '未知错误'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('创建事件时发生错误，请重试');
    }
}

async function deleteEvent(eventId) {
    if (!confirm('确定要删除这个事件吗？')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            alert('事件删除成功');
            loadEvents();
        } else {
            const errorData = await response.json();
            alert('删除事件失败：' + (errorData.detail || '未知错误'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('删除事件时发生错误，请重试');
    }
}

// 更新认证UI
function updateAuthUI() {
    const loginNav = document.getElementById('loginNav');
    const registerNav = document.getElementById('registerNav');
    const logoutNav = document.getElementById('logoutNav');

    if (token) {
        loginNav.classList.add('d-none');
        registerNav.classList.add('d-none');
        logoutNav.classList.remove('d-none');
    } else {
        loginNav.classList.remove('d-none');
        registerNav.classList.remove('d-none');
        logoutNav.classList.add('d-none');
    }
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    if (token) {
        showEventList();
    } else {
        showLoginForm();
    }
}); 