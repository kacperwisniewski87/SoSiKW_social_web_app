var csrftoken = $('meta[name="csrf-token"]').attr('content');

var urlAddFriendToChat = $('.groupUrlDataContainer').data('add-friend-to-chat-url');
var urlLeaveChat = $('.groupUrlDataContainer').data('leave-group-chat-url');
var urlRenameChat = $('.groupUrlDataContainer').data('rename-group-chat-url');
var chatUuidUrl = $('.groupUrlDataContainer').data('chat-uuid');


// App people to group chat functions
// Add people to group chat hud open request button click event handler
document.querySelector('#add-person-hud-open-btn').onclick = function() {
    var $curtainDiv = $('#curtain-screen');
    var $addPersonMessage = $('#hud-message');

    $curtainDiv.removeClass('hidden');
    $addPersonMessage.removeClass('hidden');
    $addPersonMessage.append(
        '<div class="text-center items-center">' +
          '<p class="pb-4 text-3xl text-sky-950 font-bold">Add friend to chat</p>' +
          '<div class="flex w-full items-center">' +
            '<p class="w-40 font-bold text-lg">Find friend:</p>' +
            '<div id="search-content-existing-chat" class="relative w-full">' +
              '<input type="text" id="friends-search-input" placeholder="Add friend to chat" autocomplete="off" class="w-full h-10 px-2 border border-gray-500 rounded-2xl bg-gray-100">' +
              '<div id="user-results-box" class="hidden ml-2 w-[450px] max-h-60 bg-white shadow-xl shadow-sky-950 absolute top-12 overflow-auto">' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div id="chat-members-box" class="w-full my-2 grid grid-cols-2 gap-y-2 gap-x-4 max-h-40 overflow-y-auto">' +
          '</div>' +
        '</div>' +
        '<div class="flex pt-4 justify-center">' +
          '<button id="add-friends-to-chat-btn" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Add</button>' +
          '<button id="close-hud-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Close</button>' +
        '</div>'
    );
};

document.body.addEventListener('keyup', function(event) {
    if (event.target.tagName === 'INPUT' && event.target.id === 'friends-search-input') {
        if (event.keyCode == 27) {
            const userResultsBox = document.getElementById('user-results-box');

            event.target.value = '';
            event.target.blur();
            userResultsBox.innerHTML = '';
        } else {
            const searchText = event.target.value.toLowerCase();
            const friendsResultsBox = document.getElementById('user-results-box');

            if (friendsResultsBox.classList.contains('hidden')) {
                friendsResultsBox.classList.remove('hidden');
            }

            sendSearchData({userData: searchText, newChat: 'False', chatUuid: chatUuidUrl, inputTagId: 'friends-search-input'});
        }
    }
});

// Attach functionality to the save button
document.body.addEventListener('click', function(event) {
    if (event.target.tagName === 'BUTTON' &&
        (event.target.id === 'add-friends-to-chat-btn')) {

        addNewFriendsToGroupChat();
    }
});


const addNewFriendsToGroupChat = () => {
    var addedUsersList = document.querySelectorAll(".chat-user-container");
    var addedUsersIdList = []

    addedUsersList.forEach(user=> {
        addedUsersIdList.push(user.dataset.addedId);
    });

    $.ajax({
        type: 'POST',
        url: '/' + urlAddFriendToChat,
        headers: { 'X-CSRFToken': csrftoken },
        data: {'added_users_id': JSON.stringify(addedUsersIdList)},
        success: (response)=> {
            if (response && response.success) {
                console.log('Friends added to chat.');
                var membersSection = document.getElementById('group-chat-members-section');
                var responseData = response.usersToAdd;

                if (Array.isArray(responseData)) {
                    responseData.forEach(user=> {
                        if (!document.getElementById('chat-member-${user.pk}')) {
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
                            };
                            membersSection.insertAdjacentHTML('beforeend',
                                `
                                <a href="${user.profile_page_url}" class="flex space-x-1 items-center hover:text-sky-900">
                                  <div class="size-8 min-w-8 rounded-full border border-gray-300">
                                  <img src="${profileImageUrl}" class="size-fit aspect-square rounded-full object-cover">
                                  </div>
                                  <p class="font-bold max-w-80 text-sky-950">${user.full_name} <span class="font-normal text-black">(Is Friend)</span></p>
                                </a>
                                `
                            );
                        }
                    });
                };

                var $curtainDiv = $('#curtain-screen');
                var $hudMessage = $('#hud-message');
                $curtainDiv.addClass('hidden');
                $hudMessage.addClass('hidden');
                $hudMessage.empty();
            } else {
                console.error('Failed to create chat:', response.error_message);
            }
        },
        error: (error)=> {
            console.log(error);
        }
    })

};


// Rename group chat functions
// Rename group chat hud open request button click event handler
document.querySelector('#rename-chat-hud-open-btn').onclick = function() {
    var $curtainDiv = $('#curtain-screen');
    var $renameChatFormMessage = $('#hud-message');

    $curtainDiv.removeClass('hidden');
    $renameChatFormMessage.removeClass('hidden');
    $renameChatFormMessage.append(
        '<form id="rename-form" class="text-center items-center">' +
          '<p class="pb-4 text-3xl text-sky-950 font-bold">Rename chat</p>' +
          '<div class="flex w-full items-center">' +
            '<p class="w-60 font-bold text-lg">Set new name:</p>' +
            '<input type="text" id="new-chat-name" class="w-full h-10 px-2 border border-gray-500 rounded-2xl bg-gray-100">' +
          '</div>' +
        '</form>' +
        '<div id="chat-rename-error-message" class="hidden mt-2 p-2 bg-red-200 text text-red-600 font-bold border border-red-600 rounded-2xl">' +
        '</div>' +
        '<div class="flex pt-4 justify-center">' +
          '<button id="save-new-chat-name-btn" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Save</button>' +
          '<button id="close-hud-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Cancel</button>' +
        '</div>'
    );
};

function renameGroupChat() {
    const isWhitespaceString = str => !str.replace(/\s/g, '').length;
    var newName = $('#new-chat-name').val();

    if (newName == null || newName == '' || isWhitespaceString(newName)) {
        console.log('New name is too short');
        var $errorMessage = $('#chat-rename-error-message');

        $errorMessage.removeClass('hidden');
        $errorMessage.append('<p>New name for chat is too short.</p>');
    } else {
        $.ajax({
            url: '/' + urlRenameChat,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'new_name' : newName},
            success: function(response) {
                if (response && response.success) {
                    var $curtainDiv = $('#curtain-screen');
                    var $hudMessage = $('#hud-message');
                    $curtainDiv.addClass('hidden');
                    $hudMessage.addClass('hidden');
                    $hudMessage.empty();

                    var chatNameInfoSection = $('#info-chat-name');
                    var chatNameNavbarSection = $('#navbar-room-container-' + response.room_id + '-name');
                    chatNameInfoSection.text(newName);
                    chatNameNavbarSection.text(newName);
                } else {
                    console.error('Failed to change name:', response.error_message);
                    if (response.error_message == 'Too long') {
                        console.log('New name is too long');
                        var $errorMessage = $('#chat-rename-error-message');

                        $errorMessage.removeClass('hidden');
                        $errorMessage.append('<p>New name for chat is too long. Try new name with max 255 characters.</p>');
                    }
                };
            },
            error: function(xhr, status, error) {
                console.error('Failed to change name:', error);
            }
        });
    };
};

// Event delegation for dynamically added rename chat submit button
document.body.addEventListener('submit', function(event) {

    if (event.target.tagName === 'FORM' &&
        (event.target.id === 'rename-form')) {

        event.preventDefault();
        renameGroupChat();
    }
});

// Event delegation for dynamically added rename chat submit button
document.body.addEventListener('click', function(event) {

    if (event.target.tagName === 'BUTTON' &&
        (event.target.id === 'save-new-chat-name-btn')) {

        renameGroupChat();
    }
});

// Event delegation for removing name error warning upon keypress
document.body.addEventListener('keypress', function(event) {
    if (event.target.tagName === 'INPUT' &&
        (event.target.id === 'new-chat-name')) {

        var $errorMessage = $('#chat-rename-error-message');

        $errorMessage.addClass('hidden');
        $errorMessage.empty();
    }
});

// Event for removing focus from input field
document.body.addEventListener('keyup', function(event) {
    if (event.target.tagName === 'INPUT' && event.target.id === 'new-chat-name' && event.keyCode == 27) {
        event.target.blur();
    }
});



// Leave group chat functions
// Leave group chat hud open request button click event handler
document.querySelector('#leave-chat-hud-open-btn').onclick = function() {
    var $curtainDiv = $('#curtain-screen');
    var $leaveChatConfirmMessage = $('#hud-message');

    $curtainDiv.removeClass('hidden');
    $leaveChatConfirmMessage.removeClass('hidden');
    $leaveChatConfirmMessage.append(
        '<div class="text-center items-center">' +
          '<p class="pb-4 text-3xl text-sky-950 font-bold">Leave chat</p>' +
          '<p class="font-bold text-lg">Do you really want to leave this chat?</p>' +
        '</div>' +
        '<div class="flex pt-4 justify-center">' +
          '<button id="leave-chat-btn" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Yes, leave</button>' +
          '<button id="close-hud-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">No, stay</button>' +
        '</div>'
    );
};

// Event delegation for dynamically added leave group chat button
document.body.addEventListener('click', function(event) {

    if (event.target.tagName === 'BUTTON' &&
        (event.target.id === 'leave-chat-btn')) {
        $.ajax({
            url: '/' + urlLeaveChat,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    console.log(response);
                    setTimeout(() => {
                        window.location.href = '/' + response.redirect_url;
                    }, 500)
                } else {
                    console.error('Failed to leave chat:', response.message);
                };
            },
            error: function(xhr, status, error) {
                console.error('Failed to leave chat:', error);
            }
        });
    }
});
