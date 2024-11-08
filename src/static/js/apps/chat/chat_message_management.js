const roomUuid = JSON.parse(document.getElementById('json-room_uuid').textContent);
const roomName = JSON.parse(document.getElementById('json-room_name').textContent);
const userId = JSON.parse(document.getElementById('json-userid').textContent);
const userFirstName = JSON.parse(document.getElementById('json-userfirstname').textContent);
const userLastName = JSON.parse(document.getElementById('json-userlastname').textContent);
const userName = userFirstName + " " + userLastName;

const navbarRoomsSection = document.getElementById('navbar-rooms-section');

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + '/'    + roomUuid

);


chatSocket.onmessage = function(e) {
    console.log('onmessage')
    const data = JSON.parse(e.data);
    var navbarRoomContainer = document.getElementById('navbar-room-container-' + roomId);
    var roomImageUrl = $('#navbar-room-container-' + roomId).data('room-img');

    if (data.message) {
        if (data.user_id == document.getElementById('json-userid').textContent) {
            let html = '<div class="p-2 pl-4 pr-4 rounded-xl text-right border border-gray-300 bg-gray-100">';
                html += '<p class="font-semibold underline underline-offset-2">' + data.user_full_name + '</p>';
                html += '<p>' + data.message + '</p></div>';

            document.querySelector('#chat-messages').innerHTML += html;
            scrollToBottom();
        } else {
            let html = '<div class="p-2 pl-4 pr-4 rounded-xl border border-gray-300">';
                html += '<p class="font-semibold underline underline-offset-2">' + data.user_full_name + '</p>';
                html += '<p>' + data.message + '</p></div>';

          document.querySelector('#chat-messages').innerHTML += html;
          scrollToBottom();
        };

        let roomNameShort
        if (roomName.length > 25) {
            roomNameShort = roomName.substring(0,25) + '...';
        } else {
            roomNameShort = roomName
        }

        let messageUser
        if (data.user_id == document.getElementById('json-userid').textContent) {
            messageUser = 'You'
        } else {
            messageUser = data.user_name
        }

        let messageShort
        if (data.message.length > 25) {
            messageShort = data.message.substring(0,25) + '...';
        } else {
            messageShort = data.message
        }

        navbarRoomContainer.remove();
        navbarRoomsSection.insertAdjacentHTML('afterbegin',
            `
            <a id="navbar-room-container-${roomId}" href="/chat/${roomUuid}/" data-room-id="${roomId}" class="flex space-x-2 w-full py-2 px-3 rounded-xl border bg-amber-400">
              <div class="size-12 min-w-12">
                <img src="${roomImageUrl}" class="size-fit aspect-square rounded-full object-cover">
              </div>
              <div class="w-full">
                <div class="flex justify-between">
                  <p id="navbar-room-container-${roomId}-name" title="${roomName}" class="text-lg font-bold">${roomNameShort}</p>
                </div>
                <p class="text-sm font-bold">[${messageUser}] ${messageShort}</p>
              </div>
            </a>
            `
        );
        scrollToChat(roomId);
    };
}

chatSocket.onclose = function(e) {
    console.log('onclose')
}


document.querySelector('#chat-message-submit').onclick = function(e) {
    e.preventDefault();

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'message': message,
        'user_id': userId,
        'user_name': userFirstName,
        'user_full_name': userName,
        'room_uuid': roomUuid,
    }));

    messageInputDom.value = '';

    return false;
}

document.getElementById('chat-message-input').addEventListener('keydown', function(event) {
    if (event.keyCode == 27) {
        event.target.blur();
    }
})
