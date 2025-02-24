// WebSocket connection
const chatSocket = new WebSocket(
    `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws/chat/${roomId}/`
);

const messagesContainer = document.querySelector('.messages-container');
const messageForm = document.getElementById('message-form');

document.addEventListener('DOMContentLoaded', function() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
});

const textarea = document.querySelector(".message-input");
textarea.addEventListener("input", function () {
    this.style.height = "40px";
    this.style.height = this.scrollHeight + "px";
});

function handleReplyClick() {
    const replyId = this.getAttribute('data-reply-id');
    document.getElementById('id_replied_msg').value = replyId;
    const messageCard = this.closest('.message-card');
    const messageText = messageCard.querySelector('.message-content p').innerText;
    document.getElementById('reply-text').innerText = messageText;
    document.getElementById('reply-banner').style.display = 'flex';
}

function attachReplyListeners() {
    document.querySelectorAll('.reply-btn').forEach(function(btn) {
        btn.removeEventListener('click', handleReplyClick);
        btn.addEventListener('click', handleReplyClick);
    });
}

attachReplyListeners();

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateParticipants(participants) {
    const participantsList = document.querySelector('.participants-list');
    participantsList.innerHTML = '';
    participants.forEach(function(participant) {
        participantsList.insertAdjacentHTML('beforeend', `
            <a href="/profile/${participant.id}" class="participant">
                <span class="participant-name">💠 ${participant.username}</span>
            </a>
        `);
    });
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.participants) {
        updateParticipants(data.participants);
        return;
    }
    const isOwner = data.user_id == currentUserId;
    const messageHtml = `
        <div id="message-${data.id}" class="message-card" data-msg-id="${data.id}">
            <div class="message-header">
                <a href="/profile/${data.user_id}" class="message-author">
                    @${data.user}
                </a>
                <time class="message-time">
                    Sent at: <b>just now</b>
                </time>
            </div>
            <div class="message-content">
                ${data.replied_to ? `
                    <a href="#message-${data.replied_to.id}" class="reply-link">
                        <div class="reply-preview">
                            <span class="reply-label">Replied to:</span>
                            <span class="reply-text">${data.replied_to.body}</span>
                        </div>
                    </a>
                ` : ''}
                <p>${data.body}</p>
                <div class="message-actions">
                    <button class="reply-btn" data-reply-id="${data.id}" type="button">
                        <svg class="reply-icon" viewBox="0 0 24 24">
                            <path d="M10 9V5l-7 7 7 7v-4.1c5 0 8 1.7 11 5.1-1-5-4-10-11-10z"></path>
                        </svg>
                        Reply
                    </button>
                    ${isOwner ? `
                        <a href="/update-message/${data.id}">
                            <button class="update-message" type="button">
                                <svg class="edit-icon" viewBox="0 0 24 24">
                                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a1.003 1.003 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"></path>
                                </svg>
                                Edit
                            </button>
                        </a>
                        <a href="/delete-message/${data.id}">
                            <button class="delete-message" type="button">
                                <svg class="delete-icon" viewBox="0 0 24 24">
                                    <path d="M16 9v10H8V9h8m-1.5-6h-5l-1 1H5v2h14V4h-4.5l-1-1z"></path>
                                </svg>
                                Delete
                            </button>
                        </a>
                    ` : ''}
                </div>
            </div>
        </div>
    `;

    messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
    scrollToBottom();
    attachReplyListeners();
    attachReplyLinkListeners();
};

messageForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const messageInput = document.querySelector('.message-input');
    const replyId = document.getElementById('id_replied_msg').value;
    const message = messageInput.value;

    if (message.trim()) {
        chatSocket.send(JSON.stringify({
            'message': message,
            'replied_to': replyId || null
        }));
        messageInput.value = '';
        messageInput.style.height = '40px';
        document.getElementById('reply-banner').style.display = 'none';
        document.getElementById('id_replied_msg').value = '';
        scrollToBottom();
    }
});

document.getElementById('cancel-reply').addEventListener('click', function () {
    document.getElementById('id_replied_msg').value = '';
    document.getElementById('reply-banner').style.display = 'none';
});

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".reply-link").forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: "smooth", block: "center" });
                targetElement.classList.add("highlight");
                setTimeout(() => targetElement.classList.remove("highlight"), 1500);
            }
        });
    });
});

function attachReplyLinkListeners() {
    document.querySelectorAll(".reply-link").forEach(link => {
        link.removeEventListener("click", replyLinkClickHandler);
        link.addEventListener("click", replyLinkClickHandler);
    });
}

function replyLinkClickHandler(event) {
    event.preventDefault();
    const targetId = this.getAttribute("href").substring(1);
    const targetElement = document.getElementById(targetId);
    if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth", block: "center" });
        targetElement.classList.add("highlight");
        setTimeout(() => targetElement.classList.remove("highlight"), 1500);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    attachReplyLinkListeners();
});


