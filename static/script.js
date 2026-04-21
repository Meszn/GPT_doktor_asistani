const initModal = document.getElementById('init-modal');
const appContainer = document.getElementById('app-container');
const startBtn = document.getElementById('start-btn');
const userNameInput = document.getElementById('user-name');
const userAgeInput = document.getElementById('user-age');

const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');

let userName = '';
let userAge = 0;

// API URL - since the app is served via /ui on same port, the API is at /chat
const API_URL = '/chat';

// Start Chat
startBtn.addEventListener('click', () => {
    const name = userNameInput.value.trim();
    const age = parseInt(userAgeInput.value);

    // Basic validation
    if (name && age > 0) {
        userName = name;
        userAge = age;
        
        // Hide modal
        initModal.style.opacity = '0';
        setTimeout(() => {
            initModal.classList.add('hidden');
            appContainer.classList.remove('hidden');
            messageInput.focus();
            
            // Welcome message
            addBotMessage(`Merhaba ${userName}! Ben Doktor Asistanınızım. Size nasıl yardımcı olabilirim?`);
        }, 300);
    } else {
        alert("Lütfen geçerli bir isim ve yaş giriniz.");
    }
});

function addMessage(text, isUser = false) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(isUser ? 'user' : 'bot');
    
    if (isUser) {
        msgDiv.textContent = text;
    } else {
        // Parse markdown to HTML for bot messages
        msgDiv.innerHTML = marked.parse(text);
    }
    
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'bot', 'typing-indicator-container');
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function addBotMessage(text) {
    addMessage(text, false);
}

function addUserMessage(text) {
    addMessage(text, true);
}

async function sendMessage() {
    const text = messageInput.value.trim();
    if (!text) return;
    
    // UI Update
    addUserMessage(text);
    messageInput.value = '';
    messageInput.focus();
    
    // Show typing...
    showTypingIndicator();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: userName,
                age: userAge,
                message: text
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        removeTypingIndicator();
        addBotMessage(data.response);
        
    } catch (error) {
        console.error("Error communicating with API:", error);
        removeTypingIndicator();
        addBotMessage("Üzgünüm, sisteme bağlanırken bir hata oluştu. Lütfen servislerin çalıştığından emin olun.");
    }
}

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
