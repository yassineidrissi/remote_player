class TournamentSocket {
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
        console.log(data.message);
        if (data.status === 'joined') {
            const userExist = document.querySelector('.' + data.username);
            if (userExist) {
                userExist.remove();
            }
            const userBox = document.getElementById('user-box');
            const userDiv = document.createElement('div');
            userDiv.classList.add('user', data.username);

            const roomContent = `
                <h2> ${data.message} </h2>
            `;
            
            userDiv.innerHTML = roomContent;
            userBox.appendChild(userDiv);
            userBox.scrollTop = userBox.scrollHeight;
        }
        else if (data.status === 'left') {
            document.querySelector('.' + data.username).remove();
        }
    }

    handleClose(event) {
        console.error('Tournament socket closed unexpectedly');
    }

    sendMessage(username) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                'username': username
            }));
        } else {
            console.error('WebSocket is not open. Cannot send message.');
        }
    }

}

document.addEventListener('DOMContentLoaded', () => {
    const roomName = localStorage.getItem('roomName');
    // console.log('roomName' + roomName);
    const tournamentSocket = new TournamentSocket('ws://' + window.location.host + '/tournament/' + roomName + '/');
    tournamentSocket.sendMessage('test');
});

