document.addEventListener('DOMContentLoaded', function() {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    let isBotTyping = false;

    function createLoadingIndicator() {
        const container = document.createElement('div');
        container.className = 'loading-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            dot.className = 'loading-dot';
            container.appendChild(dot);
        }
        
        return container;
    }

    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = text;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
        return messageDiv;
    }

    function showTypingIndicator() {
        if (isBotTyping) return;
        
        isBotTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message bot-typing';
        typingDiv.textContent = 'Digitando';
        typingDiv.appendChild(createLoadingIndicator());
        chatbox.appendChild(typingDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
        
        return typingDiv;
    }

    function hideTypingIndicator(typingElement) {
        if (typingElement && typingElement.parentNode) {
            typingElement.remove();
        }
        isBotTyping = false;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message || isBotTyping) return;

        addMessage(message, true);
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;

        const typingElement = showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            hideTypingIndicator(typingElement);
            addMessage(data.response, false);
        } catch (error) {
            hideTypingIndicator(typingElement);
            addMessage("Desculpe, ocorreu um erro ao tentar responder.", false);
        }

        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});