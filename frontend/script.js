const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
let hasSentMessage = false;

let thread_id = Math.random().toString(36).substring(7);

function hideWelcomeScreen() {
    const welcomeScreen = document.getElementById('welcome-screen');
    if (welcomeScreen && !hasSentMessage) {
        welcomeScreen.style.display = 'none';
        hasSentMessage = true;
    }
}

function resetChat() {
    // Remove all dynamically added messages
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => msg.remove());
    
    // Show welcome screen again
    const welcomeScreen = document.getElementById('welcome-screen');
    if (welcomeScreen) {
        welcomeScreen.style.display = 'flex';
    }
    
    // Reset state
    hasSentMessage = false;
    
    // Generate new thread ID to clear the AI's memory context
    thread_id = Math.random().toString(36).substring(7);
}

function addMessage(text, sender) {
    hideWelcomeScreen();
    
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    
    messageDiv.innerHTML = `
        <div class="message-content">
            ${text}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    hideWelcomeScreen();
    
    const indicator = document.createElement('div');
    indicator.classList.add('message', 'assistant', 'typing');
    indicator.id = 'typing-indicator';
    indicator.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

// Function triggered by clicking the Quick Action suggestion pills
function insertAndSend(text) {
    userInput.value = text;
    sendMessage();
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Clear input
    userInput.value = '';
    
    // Add user message to UI
    addMessage(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();

    // Determine the backend URL based on the current environment
    const BACKEND_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://localhost:8000' 
        : 'https://multi-agent-tool.onrender.com';

    try {
        const response = await fetch(`${BACKEND_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                thread_id: thread_id
            }),

        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        removeTypingIndicator();
        addMessage(data.response, 'assistant');
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Sorry, something went wrong. Please check if the backend server is running.', 'assistant');
    }
}

sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
