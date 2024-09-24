class RoomSocket {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.initSocket();
    }

    initSocket() {
        this.socket = new WebSocket(this.url);

        this.socket.onmessage = (e) => {
            this.handleMessage(e);
        };

        this.socket.onclose = (e) => {
            this.handleClose(e);
        };
    }

    handleMessage(event) {
        const data = JSON.parse(event.data);
        // console.log(data.message);
        console.log(data.room_name);

        const roomBox = document.getElementById('room-box');
        const roomDiv = document.createElement('div');
        roomDiv.classList.add('user');

        const roomContent = `
            <input type="text" id="{data.room_name}" value="${data.room_name}" readonly>
            <h2>welcome to ${data.room_name}</h2>
            <p> nbr of players: ${data.nbr_of_players}</p>
            <button class="join" id="join" data-room-count="${data.nbr_of_players}">Join</button>
        `;

        roomDiv.innerHTML = roomContent;
        roomBox.appendChild(roomDiv);
        roomBox.scrollTop = roomBox.scrollHeight;
    }

    handleClose(event) {
        console.error('Tournament socket closed unexpectedly');
    }

    sendMessage(room_name) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                'room_name': room_name
            }));
        } else {
            console.error('WebSocket is not open. Cannot send message.');
        }
    }

}

// document.addEventListener('DOMContentLoaded', () => {
//     // const roomName = localStorage.getItem('roomName');
//     // console.log('roomName' + roomName);
//     // const roomSocket = new RoomSocket('ws://' + window.location.host + '/tournament/');
//     // roomSocket.sendMessage(room_name);
// });
const roomSocket = new RoomSocket('ws://' + window.location.host + '/tournament/');

document.getElementById('create').addEventListener('click', function() {
    const room_name = document.querySelector('#room_name').value;
    if (room_name === '') {
        alert('Please enter a room name');
        return;
    }
    localStorage.setItem('roomName', room_name);
    roomSocket.sendMessage(room_name);
    window.location.pathname = `/tournament/${room_name}/`;
});

// document.getElementById('join').addEventListener('click', function() {
//     console.log('join');
//     const room_name = document.querySelector('#room_name').value;
//     localStorage.setItem('roomName', room_name);
//     window.location.pathname = `/tournament/${room_name}/`;
// });


const joins_btns = document.querySelectorAll('.join');


joins_btns.forEach(btn => {

    btn.addEventListener('click', function() {
        const roomName = btn.parentElement.querySelector('input').value;
        const roomCount = btn.getAttribute('data-room-count');
        if (roomCount >= 4) {
            return;
        }
        console.log(roomName);
        localStorage.setItem('roomName', roomName);
        window.location.pathname = `/tournament/${roomName}/`;
    });
});