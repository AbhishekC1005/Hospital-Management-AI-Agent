// Global variables
let isProcessing = false;
let currentSessionId = localStorage.getItem('crewai_session_id') || null;

// DOM elements
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const loadingOverlay = document.getElementById('loadingOverlay');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const charCount = document.getElementById('charCount');

// Initialize the application
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

async function initializeApp() {
    document.getElementById('welcomeTime').textContent = getCurrentTime();
    messageInput.addEventListener('keypress', handleKeyPress);
    messageInput.addEventListener('input', updateCharCount);
    messageInput.focus();
    updateStatus('ready', 'Ready');

    // Create session if one doesn't exist in local storage
    if (!currentSessionId) {
        await createNewSession();
    } else {
        console.log('App initialized with existing session:', currentSessionId);
    }
}

async function createNewSession() {
    try {
        updateStatus('processing', 'Creating session...');
        const response = await fetch('/new-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            const data = await response.json();
            currentSessionId = data.session_id;
            localStorage.setItem('crewai_session_id', currentSessionId);
            console.log('New session created and stored:', currentSessionId);
            updateStatus('ready', 'Ready');
        } else {
            throw new Error('Failed to create session');
        }
    } catch (error) {
        console.error('Error creating session:', error);
        updateStatus('error', 'Session error');
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function updateCharCount() {
    const count = messageInput.value.length;
    charCount.textContent = count;

    if (count > 450) {
        charCount.style.color = '#ef4444';
    } else if (count > 400) {
        charCount.style.color = '#f59e0b';
    } else {
        charCount.style.color = '#718096';
    }
}

function updateStatus(type, message) {
    statusText.textContent = message;

    switch (type) {
        case 'ready':
            statusDot.style.background = '#48bb78';
            break;
        case 'processing':
            statusDot.style.background = '#f59e0b';
            break;
        case 'error':
            statusDot.style.background = '#ef4444';
            break;
    }
}

async function sendMessage() {
    const message = messageInput.value.trim();

    if (!message || isProcessing) {
        return;
    }

    // Ensure we have a session
    if (!currentSessionId) {
        console.log('No session ID, creating a new one...');
        await createNewSession();
        // If session creation fails, stop
        if (!currentSessionId) {
            addMessage('Sorry, I couldnt start a conversation. Please refresh the page.', 'assistant', true);
            return;
        }
    }

    console.log('=== SENDING MESSAGE ===');
    console.log('Message:', message);
    console.log('Session ID:', currentSessionId);
    console.log('======================');

    addMessage(message, 'user');
    messageInput.value = '';
    updateCharCount();
    await processMessage(message);
}

function sendQuickQuery(query) {
    if (isProcessing) {
        return;
    }

    messageInput.value = query;
    sendMessage();
}

async function processMessage(message) {
    isProcessing = true;
    showLoading(true);
    updateStatus('processing', 'Processing...');

    try {
        const response = await fetch('/ask-reception', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_query: message,
                session_id: currentSessionId // Send the correct session ID
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // IMPORTANT: Update session ID if the server assigned a new one
        // This handles the case where the session was null or expired on the server
        if (data.session_id && data.session_id !== currentSessionId) {
            currentSessionId = data.session_id;
            localStorage.setItem('crewai_session_id', currentSessionId);
            console.log('Session ID updated by server:', currentSessionId);
        }

        addMessage(data.response, 'assistant');
        updateStatus('ready', 'Ready');

    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error while processing your request. Please try again.', 'assistant', true);
        updateStatus('error', 'Error occurred');

        setTimeout(() => {
            updateStatus('ready', 'Ready');
        }, 3000);
    } finally {
        isProcessing = false;
        showLoading(false);
        messageInput.focus();
    }
}

function addMessage(text, sender, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';

    if (sender === 'user') {
        avatarDiv.innerHTML = '<i class="fas fa-user"></i>';
    } else {
        avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
    }

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';

    if (isError) {
        textDiv.style.background = 'rgba(239, 68, 68, 0.1)';
        textDiv.style.color = '#ef4444';
        textDiv.style.border = '1px solid rgba(239, 68, 68, 0.3)';
    }

    textDiv.innerHTML = formatMessage(text);

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = getCurrentTime();

    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(text) {
    // Basic formatting for newlines and emphasis
    let formatted = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    
    formatted = formatted.replace(/\n/g, '<br>');
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // More robust list formatting
    // Unordered lists
    formatted = formatted.replace(/^[ \t]*[-•*]\s+(.*)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    // Fix nested or adjacent lists
    formatted = formatted.replace(/<\/ul>\s*<br>\s*<ul>/g, '');

    // Ordered lists
    formatted = formatted.replace(/^[ \t]*\d+\.\s+(.*)$/gm, '<li>$1</li>');
    formatted = formatted.replace(/(<li>.*<\/li>)/s, (match, p1) => {
        // Only wrap in <ol> if it's not already in a <ul>
        if (match.includes('<ul>')) return match;
        return `<ol>${p1}</ol>`;
    });
    // Fix nested or adjacent lists
    formatted = formatted.replace(/<\/ol>\s*<br>\s*<ol>/g, '');

    return formatted;
}


function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
    sendButton.disabled = show;
    messageInput.disabled = show;
}

async function clearChat() {
    if (!currentSessionId) {
        console.log('No session to clear.');
        return;
    }

    try {
        // Tell the server to clear this specific session
        const response = await fetch('/clear-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ session_id: currentSessionId }) // Send the session ID
        });

        if (response.ok) {
            showNotification('Conversation cleared - starting fresh!', 'success');
            console.log('Session cleared on server:', currentSessionId);
        } else {
            throw new Error('Failed to clear session on server');
        }
    } catch (error) {
        console.error('Error clearing session:', error);
        showNotification('Could not clear session on server, clearing locally.', 'warning');
    }

    // Clear local state
    const welcomeMessage = chatMessages.querySelector('.message');
    chatMessages.innerHTML = '';
    chatMessages.appendChild(welcomeMessage);
    document.getElementById('welcomeTime').textContent = getCurrentTime();
    messageInput.focus();
    
    // We create a new session right away
    await createNewSession();
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 20px',
        borderRadius: '8px',
        color: 'white',
        fontWeight: '500',
        zIndex: '1001',
        animation: 'slideInRight 0.3s ease',
        maxWidth: '300px'
    });

    switch (type) {
        case 'success':
            notification.style.background = '#48bb78';
            break;
        case 'error':
            notification.style.background = '#ef4444';
            break;
        case 'warning':
            notification.style.background = '#f59e0b';
            break;
        default:
            notification.style.background = '#667eea';
    }

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

window.addEventListener('online', () => {
    updateStatus('ready', 'Ready');
    showNotification('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    updateStatus('error', 'Offline');
    showNotification('Connection lost', 'error');
});
