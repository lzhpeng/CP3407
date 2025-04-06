document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // 添加消息到聊天界面
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // 滚动到底部
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // 处理表单提交
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;
        
        // 添加用户消息
        addMessage(message, true);
        userInput.value = '';
        
        try {
            // 发送请求到服务器
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            // 添加机器人回复
            addMessage(data.response);
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('抱歉，发生了一些错误。请稍后再试。');
        }
    });

    // 按Enter发送消息
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
}); 