
// const chatSocket = new WebSocket(
//     'ws://' + window.location.host + '/app/'
// );

// chatSocket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     const chatBox = document.getElementById('chat-box');
    
//     const messageDiv = document.createElement('div');
//     messageDiv.classList.add('message', 'received');

//     const messageContent = `
//         <p>${data.message}</p>
//         <span class="timestamp">${new Date().toLocaleTimeString()}</span>
//         <span class="username">user: ${data.username}</span>
//     `;

//     messageDiv.innerHTML = messageContent;
//     chatBox.appendChild(messageDiv);

//     chatBox.scrollTop = chatBox.scrollHeight;
// };

// chatSocket.onclose = function(e) {
//     console.error('Chat socket closed unexpectedly');
// };

// // var username = getElementById('username').value;

// document.getElementById('send-button').onclick = function(e) {
//     const messageInput = document.getElementById('message-input');
//     const message = messageInput.value;
//     const usernameInput = document.getElementById('username');
//     const username = usernameInput.value;

//     chatSocket.send(JSON.stringify({
//         'message': message,
//         'username': username
//     }));

//     messageInput.value = '';
// };
