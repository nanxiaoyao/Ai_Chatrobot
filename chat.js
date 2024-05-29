// 清空聊天记录的函数
function clearChatHistory() {
    // 获取聊天框元素
    const chatBox = document.getElementById('chat-box');
    // 清空聊天框的内容
    chatBox.innerHTML = '';
}

// 选择模型并清空聊天记录的函数
function selectModel(model) {
    // 设置当前模型为传入的模型
    currentModel = model;
    // 清空聊天记录
    clearChatHistory();
}

// 发送消息的函数
function sendMessage() {
    // 获取用户输入的内容
    const userInput = document.getElementById('user-input').value;
    // 构建请求数据对象
    const requestData = {
        message: userInput,
        model: currentModel
    };

    // 发送POST请求到聊天API
    fetch('http://localhost:18889/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // 获取AI的回复
        const reply = data.reply;
        // 显示用户和AI的消息
        displayMessage('user', userInput);
        displayMessage('ai', reply);
        // 清空用户输入框
        document.getElementById('user-input').value = '';
    })
    .catch(error => {
        // 输出错误信息到控制台
        console.error('Error:', error);
    });
}

// 显示消息的函数
function displayMessage(sender, message) {
    // 获取聊天框元素
    const chatBox = document.getElementById('chat-box');
    // 创建一个消息元素
    const messageElement = document.createElement('div');
    // 为消息元素添加样式类
    messageElement.classList.add('message', `${sender}-message`);

    // 创建一个头像元素
    const avatarElement = document.createElement('div');
    avatarElement.classList.add('avatar');
    // 根据发送者设置头像
    if (sender === 'ai') {
        avatarElement.innerHTML = `<img src="image/bot.png" alt="AI Avatar">`;
    } else if (sender === 'user') {
        avatarElement.innerHTML = `<img alt="User Avatar" src="image/user.png">`;
    }
    // 将头像元素添加到消息元素中
    messageElement.appendChild(avatarElement);

    // 创建一个文本元素
    const textElement = document.createElement('div');
    textElement.classList.add('message-text');
    // 设置文本元素的内容为传入的消息
    textElement.textContent = message;
    // 将文本元素添加到消息元素中
    messageElement.appendChild(textElement);
    // 将消息元素添加到聊天框中
    chatBox.appendChild(messageElement);
    // 滚动聊天框到底部以显示最新消息
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 监听模型选择下拉框变化的函数
document.getElementById('model-select').addEventListener('change', function() {
    // 当选项变化时，调用selectModel函数并传入当前选中的值
    selectModel(this.value);
});

// 初始化页面时执行的函数
document.addEventListener('DOMContentLoaded', function () {
    // 获取模型选择下拉框元素
    var modelSelect = document.getElementById('model-select');
    // 设置默认选中的模型为空
    modelSelect.value = ' ';
    // 初始化模型并清空聊天记录
    selectModel(modelSelect.value);
});