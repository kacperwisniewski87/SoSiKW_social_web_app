const urlSearchResult = $('.urlDataContainer').data('url-search-result');
const urlCreateGroupChat = $('.urlDataContainer').data('url-create-group-chat');
const urlAvatarMale = $('.urlDataContainer').data('url-avatar-male');
const urlAvatarFemale = $('.urlDataContainer').data('url-avatar-female');
const urlAvatarDefault = $('.urlDataContainer').data('url-avatar-default');
const urlRemoveButtonImg = $('.urlDataContainer').data('url-remove-button-img');
const roomUuidUrl = $('.urlDataContainer').data('room-uuid-url');
const roomId = $('.urlDataContainer').data('room-id');
const roomsDataJson = $('.urlDataContainer').data('rooms-data-json');

var csrftoken = $('meta[name="csrf-token"]').attr('content');

const isWhitespaceString = str => !str.replace(/\s/g, '').length;

let chatRoomsFilteredArr = []

function scrollToBottom() {
    const objDiv = document.querySelector('#chat-messages');
    if (objDiv) {
        objDiv.scrollTop = objDiv.scrollHeight;
    }
}

function scrollToChat(chatId) {
    const chatElement = document.getElementById(`navbar-room-container-${chatId}`);
    if (chatElement) {
        chatElement.scrollIntoView({ behavior: 'instant', block: 'end' });
    }
}

scrollToBottom();
scrollToChat(roomId);

// Chat search bar function
document.getElementById('chat-room-search-input').onkeyup = function (event) {
    const chatRoomsNavbarContainer = document.getElementById('navbar-rooms-container');
    const searchChatName = event.target.value.toLowerCase();
    chatRoomsNavbarContainer.innerHTML = '';

    chatRoomsFilteredArr = roomsDataJson.filter(info=>
      info['chat_name'].toLowerCase().includes(searchChatName.toLowerCase())
    );
    console.log(chatRoomsFilteredArr);
    if (chatRoomsFilteredArr.length > 0) {
        chatRoomsFilteredArr.map(info => {
            const chatRoomLink = document.createElement('a');
            chatRoomLink.id = 'navbar-room-container-' + info['chat_id'];
            chatRoomLink.href = '/chat/' + info['chat_uuid_url'];

            if (roomUuidUrl === info['chat_uuid_url']) {
                chatRoomLink.className = 'flex space-x-2 w-full py-2 px-3 rounded-xl border bg-amber-400';
            } else {
                chatRoomLink.className = 'flex space-x-2 w-full py-2 px-3 rounded-xl border bg-gray-100 hover:bg-gray-300';
            };

            if (info['chat_is_user_deleted'] === 'True') {
                chatNameHtml = `<p id="navbar-room-container-${info['chat_id']}-name" class="text-lg text-gray-600">${info['chat_name']} <span class="text-sm">[Deleted]</span></p>`
            } else {
                chatNameHtml = `<p id="navbar-room-container-${info['chat_id']}-name" class="text-lg font-bold">${info['chat_name']}</p>`
            };

            if (info['chat_date_last_message'] !== '') {
                if (info['is_new_message'] === 'True') {
                    chatMessageHtml = `<p class="text-sm font-bold">[${info['chat_last_message_user_name']}] ${info['chat_last_message_content']}</p>`
                } else {
                    chatMessageHtml = `<p class="text-sm text-gray-700">[${info['chat_last_message_user_name']}] ${info['chat_last_message_content']}</p>`
                }
            } else {
                chatMessageHtml = `<p class="text-sm text-gray-700">Start conversation</p>`
            };

            chatRoomLink.innerHTML = `
                <div class="size-12 min-w-12">
                  <img src="${info['chat_image_url']}" class="size-fit aspect-square rounded-full object-cover">
                  </div>
                  <div class="w-full">
                  <div class="flex justify-between">
                    ${chatNameHtml}
                  </div>
                  ${chatMessageHtml}
                </div>
            `;

            chatRoomsNavbarContainer.appendChild(chatRoomLink);
        });
    } else {
        chatRoomsNavbarContainer.innerHTML = `<p class="flex w-full py-2 justify-center text-center rounded-xl border bg-red-200 ">No matching chats</p>`;
    }
}


// Group chat creation functions
// Functions to populate hud upon pressing create group chat button
document.addEventListener('DOMContentLoaded', function() {
    const hudMessage = document.getElementById('hud-message');
    const curtainScreen = document.getElementById('curtain-screen');

    // HTML content for the Create Group Chat form
    const groupChatFormHTML = `
      <form id="create-group-chat-form" class="items-center">
        <p class="pb-4 text-3xl text-center text-sky-950 font-bold">Create group chat</p>
        <div class="flex w-full items-center pb-4">
          <p class="w-20 font-bold text-lg">Name:</p>
          <input type="text" id="new-chat-name" placeholder="Chat Name" autocomplete="off" class="w-full h-10 px-2 border border-gray-500 rounded-2xl bg-gray-100">
        </div>
        <div  id="chat-name-error-message" class="hidden mt-2 ml-20 p-2 bg-red-200 text text-red-600 font-bold border border-red-600 rounded-2xl">
        </div>
        <div class="flex w-full items-center">
          <p class="w-60 font-bold text-lg">Add friend to chat:</p>
          <div id="search-content" class="relative w-full">
            <input type="text" id="new-chat-friends-search-input" placeholder="Add friend to chat" autocomplete="off" class="w-full h-10 px-2 border border-gray-500 rounded-2xl bg-gray-100">
            <div id="user-results-box" class="hidden ml-2 w-[450px] max-h-60 bg-white shadow-xl shadow-sky-950 absolute top-14 overflow-auto">
            </div>
          </div>
        </div>
        <p class="my-2 font-bold text-lg">Chat members:</p>
        <div id="chat-members-box" class="w-full grid grid-cols-2 gap-y-2 gap-x-4 max-h-40 overflow-y-auto">
        </div>
      </form>
      <div id="chat-rename-error-message" class="hidden mt-2 mx-4 p-2 bg-red-200 text text-red-600 font-bold border border-red-600 rounded-2xl"></div>
      <div class="flex pt-4 justify-center">
        <button id="create-group-chat-btn" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Save</button>
        <button id="close-hud-btn" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Cancel</button>
      </div>
    `;

    // Function to populate the HUD and show it
    function populateHudMessage() {
        hudMessage.innerHTML = groupChatFormHTML;
        hudMessage.classList.remove('hidden');
        curtainScreen.classList.remove('hidden');

        // Attach functionality to the save button
        document.getElementById('create-group-chat-btn').addEventListener('click', function() {
            submitGroupChatForm();
        });

        // Attach functionality to the form submission)
        document.getElementById('create-group-chat-form').addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                submitGroupChatForm();
            }
        });

        // Attach the search functionality again
        const searchInput = document.getElementById('new-chat-friends-search-input');
        const userResultsBox = document.getElementById('user-results-box');

        document.body.addEventListener('keyup', function(event) {
            if (event.target.tagName === 'INPUT' && event.target.id === 'new-chat-friends-search-input') {
                if (event.keyCode == 27) {

                    event.target.value = '';
                    event.target.blur();
                    userResultsBox.innerHTML = '';
                } else {
                    const searchText = event.target.value.toLowerCase();

                    if (userResultsBox.classList.contains('hidden')) {
                        userResultsBox.classList.remove('hidden');
                    }

                    sendSearchData({userData: searchText, newChat: 'True', chatUuid: null, inputTagId: 'new-chat-friends-search-input'});
                }
            }
        });

        // Event for removing focus from input field
        document.body.addEventListener('keyup', function(event) {
            if (event.target.tagName === 'INPUT' && event.target.id === 'new-chat-name' && event.keyCode == 27) {
                event.target.blur();
            }
        });

    }

    // Attach the function to the button
    document.getElementById('create-group-chat').addEventListener('click', populateHudMessage);
});


// Submit group chat creation function
const submitGroupChatForm = () => {
    const chatNameInput = document.getElementById('new-chat-name');
    var chatName = chatNameInput.value;

    if (chatName == null || chatName == '' || isWhitespaceString(chatName)) {
        var $nameErrorMessage = $('#chat-name-error-message');

        $nameErrorMessage.removeClass('hidden');
        $nameErrorMessage.append('<p>Chat name is empty.</p>');
    } else {
        var addedUsersList = document.querySelectorAll(".chat-user-container");
        var addedUsersIdList = []

        addedUsersList.forEach(user=> {
            addedUsersIdList.push(user.dataset.addedId);
        });

        $.ajax({
            type: 'POST',
            url: urlCreateGroupChat,
            headers: { 'X-CSRFToken': csrftoken },
            data: {'chat_name': chatName, 'added_users_id': JSON.stringify(addedUsersIdList)},
            success: (response)=> {
                if (response && response.success) {
                    setTimeout(() => {
                        window.location.href = '/' + response.redirect_url;
                    }, 100)
                } else {
                    console.error('Failed to create chat:', response.error_message);

                    if (response.error_message == 'Too long') {

                        var $nameErrorMessage = $('#chat-name-error-message');

                        $nameErrorMessage.removeClass('hidden');
                        $nameErrorMessage.append('<p>New name for chat is too long. Try new name with max 255 characters.</p>');
                    }
                }
            },
            error: (error)=> {
                console.log(error);
            }
        })
    }
};


// Friends search result show function
const sendSearchData = ({userData, newChat, chatUuid, inputTagId}) => {
    const userResultsBox = document.getElementById('user-results-box');
    const searchInput = document.getElementById(inputTagId);
    $.ajax({
        type: 'POST',
        url: urlSearchResult,
        headers: { 'X-CSRFToken': csrftoken },
        data: {'userData': userData, 'newChat': newChat, 'chatUuid': chatUuid},
        success: (response)=> {
            const responseData = response.foundUsers;
            if (Array.isArray(responseData)) {
                userResultsBox.innerHTML = '';
                responseData.forEach(user=> {

                    if (!document.querySelector(`[data-added-id="${user.pk}"]`)) {
                        let profileImageUrl;
                        if (user['profile_image_url']) {
                            profileImageUrl = user['profile_image_url'];
                        } else {
                            if (user['gender'] === 'male') {
                              profileImageUrl = urlAvatarMale;
                            } else if (user['gender'] === 'female') {
                              profileImageUrl = urlAvatarFemale;
                            } else {
                              profileImageUrl = urlAvatarDefault;
                            }
                        }

                        const escapedUser = JSON.stringify(user).replace(/'/g, '&#39;').replace(/"/g, '&quot;');

                        userResultsBox.innerHTML += `
                            <div id="search-result-user-${user.pk}" class="user-container flex justify-between items-center h-12 border px-1">
                              <div class="flex items-center space-x-1">
                                <div class="size-10 border rounded-full">
                                  <img src="${profileImageUrl}" class="size-fit aspect-square rounded-full object-cover">
                                </div>
                                <p title="${user.full_name}" class="pl-2 text-sky-950">${user.full_name_truncate}</p>
                              </div>
                              <button title="Add to chat" data-id="${user.pk}" data-user="${escapedUser}" data-user_pic="${profileImageUrl}" class="add-friend-to-chat-btn w-16 h-10 rounded-lg bg-gray-200 hover:bg-gray-400">
                                Add
                              </button>
                            </div>
                        `
                    }
                })
            } else {
                userResultsBox.innerHTML = "";
                userResultsBox.classList.add('hidden');
            }
        },
        error: (error)=> {
            console.log(error);
        }
    })
};


// Event delegation for dynamically added buttons to add friend chat creation form
document.body.addEventListener('click', function(event) {
    if (event.target.tagName === 'BUTTON' &&
        (event.target.classList.contains('add-friend-to-chat-btn'))) {

        const addedUserData = JSON.parse(event.target.dataset.user);
        const addedUserPic = event.target.dataset.user_pic;

        const chatMembersBox = document.getElementById('chat-members-box');

        var userSearchResultsContainer = document.querySelector(`[id="search-result-user-${addedUserData.pk}"]`)

        if (!document.querySelector(`[data-added-id="${addedUserData.pk}"]`)) {
            chatMembersBox.insertAdjacentHTML('beforeend',
                `
                <div class="chat-user-container flex justify-between items-center h-10 border rounded-full" data-added-id="${addedUserData.pk}">
                    <div class="flex items-center space-x-1">
                        <div class="size-10 border rounded-full">
                            <img src="${addedUserPic}" class="size-fit aspect-square rounded-full object-cover">
                        </div>
                        <p title="${addedUserData.full_name}"  class="pl-2 text-sky-950">${addedUserData.full_name_truncate}</p>
                    </div>
                    <button title="Remove" class="remove-chat-member-btn size-10 border rounded-full" data-id="${addedUserData.pk}">
                        <img src="${urlRemoveButtonImg}" data-id="${addedUserData.pk}" class="remove-chat-member-btn size-fit aspect-square rounded-full object-cover">
                    </button>
                </div>
                `
            );
            userSearchResultsContainer.remove();
        } else {
            console.log("User already added to chat.");
        }
    }
});


// Event listener to remove the user from the chat members list
document.body.addEventListener('click', function(event) {
    if (event.target.tagName === 'IMG' &&
        event.target.classList.contains('remove-chat-member-btn')) {

        const userId = event.target.dataset.id;
        const memberElement = document.querySelector(`[data-added-id="${userId}"]`);

        if (memberElement) {
            memberElement.remove();
        }
    }
});


// Event delegation for dynamically added cancel/close buttons
document.body.addEventListener('click', function(event) {

    if (event.target.tagName === 'BUTTON' &&
        (event.target.id === 'cancel-hud-btn' ||
         event.target.id === 'close-hud-btn')) {

        var $curtainDiv = $('#curtain-screen');
        var $hudMessage = $('#hud-message');

        $curtainDiv.addClass('hidden');
        $hudMessage.addClass('hidden');
        $hudMessage.empty();
    }
});


// Event for clicking outside friend search input and result box
document.addEventListener('click', function(event) {
    const searchInput = document.getElementById('new-chat-friends-search-input');
    if (searchInput) {
        const userResultsBox = document.getElementById('user-results-box');

        var isClickInsideInputField = searchInput.contains(event.target);
        var isClickInsideResultBox = userResultsBox.contains(event.target);

        if (!isClickInsideInputField && !isClickInsideResultBox) {
            userResultsBox.classList.add('hidden');
            userResultsBox.innerHTML = "";
            searchInput.value = "";
        }
    }
});


// Event listener for closing hud upon pressing ESC outside of input fields
document.body.addEventListener('keyup', function(event) {
    if (event.target.tagName !== 'INPUT' && event.keyCode == 27) {
        var $curtainDiv = $('#curtain-screen');
        var $hudMessage = $('#hud-message');

        $curtainDiv.addClass('hidden');
        $hudMessage.addClass('hidden');
        $hudMessage.empty();
    }
});