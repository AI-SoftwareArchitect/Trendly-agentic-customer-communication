document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chatInput');
    const sendMessageButton = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    const prompt1 = document.getElementById('prompt1');
    const prompt2 = document.getElementById('prompt2');
    const prompt3 = document.getElementById('prompt3');

    sendMessageButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('bl-input', (e) => {
        if (e.target.value.trim() !== '') {
            sendMessageButton.disabled = false;
        } else {
            sendMessageButton.disabled = true;
        }
    });

    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    prompt1.addEventListener('click', () => {
        chatInput.value = 'iPhone 15 Pro Max hakkında bilgi al';
        sendMessage();
    });

    prompt2.addEventListener('click', () => {
        chatInput.value = 'Playstation 5 Slim stok durumu';
        sendMessage();
    });

    prompt3.addEventListener('click', () => {
        chatInput.value = 'MacBook Pro M3 Max fiyatı nedir?';
        sendMessage();
    });

    function sendMessage() {
        const messageText = chatInput.value.trim();
        if (messageText) {
            displayMessage(messageText, 'user');
            chatInput.value = '';
            sendMessageButton.disabled = true;

            showLoading(true);

            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: messageText }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    displayMessage(data.response, 'agent');
                } else if (data.error) {
                    showError(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('Error connecting to the server.');
            })
            .finally(() => {
                showLoading(false);
            });
        }
    }

    function displayMessage(message, sender) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message', sender);

        const avatar = document.createElement('bl-avatar');
        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble');

        if (message.includes('<product>')) {
            const productName = message.match(/<product>(.*?)<\/product>/)[1];
            message = message.replace(/<product>.*?<\/product>/, '');
            messageBubble.innerHTML = message;

            const productContainer = document.createElement('div');
            productContainer.classList.add('product-container');
            productContainer.textContent = productName;
            messageBubble.appendChild(productContainer);
        } else {
            messageBubble.textContent = message;
        }

        if (sender === 'user') {
            avatar.innerHTML = 'ME';
            messageWrapper.appendChild(messageBubble);
            messageWrapper.appendChild(avatar);
        } else {
            avatar.src = 'https://www.trendyol.com/favicon.ico';
            avatar.alt = 'Trendyol Assistant';
            messageWrapper.appendChild(avatar);
            messageWrapper.appendChild(messageBubble);
        }

        chatMessages.appendChild(messageWrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
    }

    function showLoading(show) {
        if (show) {
            loadingSpinner.style.display = 'block';
        } else {
            loadingSpinner.style.display = 'none';
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.style.display = 'block';
    }
});