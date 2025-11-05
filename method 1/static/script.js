// Global variables
let isProcessing = false;
let currentSessionId = localStorage.getItem('hospital_session_id') || 'persistent_session';

// DOM elements
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const loadingOverlay = document.getElementById('loadingOverlay');
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const charCount = document.getElementById('charCount');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set welcome message time
    document.getElementById('welcomeTime').textContent = getCurrentTime();
    
    // Add event listeners
    messageInput.addEventListener('keypress', handleKeyPress);
    messageInput.addEventListener('input', updateCharCount);
    
    // Focus on input
    messageInput.focus();
    
    // Update status
    updateStatus('ready', 'Ready');
    
    // Update session info
    updateSessionInfo();
}

function updateSessionInfo() {
    const sessionInfo = document.getElementById('sessionInfo');
    if (currentSessionId === 'persistent_session') {
        sessionInfo.textContent = 'Persistent Session';
    } else {
        sessionInfo.textContent = `Session: ${currentSessionId.substring(0, 8)}...`;
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
    
    switch(type) {
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
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    updateCharCount();
    
    // Send to API
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
                session_id: currentSessionId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update session ID if provided
        if (data.session_id) {
            currentSessionId = data.session_id;
            localStorage.setItem('hospital_session_id', currentSessionId);
            updateSessionInfo();
        }
        
        // Add assistant response to chat
        addMessage(data.response, 'assistant');
        
        updateStatus('ready', 'Ready');
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error while processing your request. Please try again.', 'assistant', true);
        updateStatus('error', 'Error occurred');
        
        // Reset status after 3 seconds
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
    
    // Format the text (handle lists, line breaks, etc.)
    textDiv.innerHTML = formatMessage(text);
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = getCurrentTime();
    
    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    
    // Add feedback buttons for assistant messages with recommendations
    if (sender === 'assistant' && (text.includes('recommend') || text.includes('suggest') || text.includes('👍') || text.includes('👎'))) {
        const feedbackDiv = document.createElement('div');
        feedbackDiv.className = 'feedback-buttons';
        feedbackDiv.style.marginTop = '8px';
        
        const likeBtn = document.createElement('button');
        likeBtn.innerHTML = '👍 Like';
        likeBtn.className = 'feedback-btn like-btn';
        likeBtn.onclick = () => submitFeedback(text, 'like', likeBtn, dislikeBtn);
        
        const dislikeBtn = document.createElement('button');
        dislikeBtn.innerHTML = '👎 Dislike';
        dislikeBtn.className = 'feedback-btn dislike-btn';
        dislikeBtn.onclick = () => submitFeedback(text, 'dislike', likeBtn, dislikeBtn);
        
        feedbackDiv.appendChild(likeBtn);
        feedbackDiv.appendChild(dislikeBtn);
        contentDiv.appendChild(feedbackDiv);
    }
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(text) {
    // Convert line breaks to <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Convert **bold** to <strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert numbered lists
    formatted = formatted.replace(/^\d+\.\s(.+)$/gm, '<li>$1</li>');
    if (formatted.includes('<li>')) {
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ol>$1</ol>');
    }
    
    // Convert bullet points
    formatted = formatted.replace(/^[-•]\s(.+)$/gm, '<li>$1</li>');
    if (formatted.includes('<li>') && !formatted.includes('<ol>')) {
        formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
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
    try {
        // Create a new session
        const response = await fetch('/new-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            currentSessionId = data.session_id;
            localStorage.setItem('hospital_session_id', currentSessionId);
            updateSessionInfo();
            
            showNotification('New conversation started', 'success');
        }
    } catch (error) {
        console.error('Error creating new session:', error);
        showNotification('Error starting new conversation', 'error');
    }
    
    // Keep only the welcome message
    const welcomeMessage = chatMessages.querySelector('.message');
    chatMessages.innerHTML = '';
    chatMessages.appendChild(welcomeMessage);
    
    // Update welcome time
    document.getElementById('welcomeTime').textContent = getCurrentTime();
    
    // Focus input
    messageInput.focus();
}

// Utility functions for enhanced UX
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
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
    
    // Set background color based on type
    switch(type) {
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
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add CSS animations for notifications
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

// Feedback functionality
async function submitFeedback(recommendation, feedback, likeBtn, dislikeBtn) {
    try {
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                recommendation: recommendation,
                feedback: feedback,
                session_id: currentSessionId
            })
        });
        
        if (response.ok) {
            // Disable both buttons and show feedback
            likeBtn.disabled = true;
            dislikeBtn.disabled = true;
            
            if (feedback === 'like') {
                likeBtn.style.background = '#48bb78';
                likeBtn.style.color = 'white';
                showNotification('Feedback recorded! I\'ll learn from this.', 'success');
            } else {
                dislikeBtn.style.background = '#ef4444';
                dislikeBtn.style.color = 'white';
                showNotification('Feedback recorded! I\'ll adjust future recommendations.', 'success');
            }
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        showNotification('Error recording feedback', 'error');
    }
}

// Handle connection errors
window.addEventListener('online', () => {
    updateStatus('ready', 'Ready');
    showNotification('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    updateStatus('error', 'Offline');
    showNotification('Connection lost', 'error');
});

// Prevent form submission on Enter in input
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.shiftKey) {
        // Allow Shift+Enter for new lines
        return;
    }
});