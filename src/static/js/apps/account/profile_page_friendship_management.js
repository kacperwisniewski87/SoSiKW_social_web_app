$(document).ready(function() {
    var urlSendFriendRequest = $('.urlDataContainer').data('send-friend-request');
    var urlFriendshipRequests = $('.urlDataContainer').data('friendship-requests');
    var urlBlockUserAdd = $('.urlDataContainer').data('block-user-add');
    var urlRemoveFriend = $('.urlDataContainer').data('remove-friend');
    var urlAvatarMale = $('.urlDataContainer').data('url-avatar-male');
    var urlAvatarFemale = $('.urlDataContainer').data('url-avatar-female');
    var urlAvatarDefault = $('.urlDataContainer').data('url-avatar-default');

    var csrftoken = $('meta[name="csrf-token"]').attr('content');
    var userSiteUrlNew = $('#block-hud-open-btn').data('site-url');

    // Invite friend request button click event handler
    $(document).on('click', '#invite-button', function() {

        $.ajax({
            url: urlSendFriendRequest,
            method: "POST",
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response.success) {
                    $("#friendship-btns-section").html("<button title='Manage requests' onclick=\"location.href='" + urlFriendshipRequests + "'\" class='px-3 py-2 rounded-md bg-amber-200 hover:bg-amber-500'>Friendship request sent!</button>");
                } else {
                    alert("Error: " + response.error);
                }
            },
            error: function(xhr, status, error) {
                console.log("An error occurred: " + error);
            }
        });
    });

    // Block user hud open request button click event handler
    $(document).on('click', '#block-hud-open-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#hud-message');
        var userSiteUrl = $(this).data('site-url');

        $.ajax({
            url: '/' + userSiteUrl + '/hud_data',
            type: 'get',
            dataType: 'json',
            success: function(response) {
                if (response && response.success) {
                    $curtainDiv.removeClass('hidden');
                    $removeUserConfirmMessage.removeClass('hidden');
                    $removeUserConfirmMessage.append(
                        '<div class="flex flex-col px-2 text-center items-center">' +
                          '<div class="aspect-square size-60">' +
                            '<img src="' + response.profile_picture_url + '" class="size-fit aspect-square rounded-full object-cover">' +
                          '</div>' +
                          '<p class="font-bold text-lg">Do you really want to block ' + response.first_name + ' ' + response.last_name + '?</p>' +
                        '</div>' +
                        '<div class="flex pt-4 justify-center">' +
                          '<button id="block-user-btn" data-id="' + response.user_id + '" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Block</button>' +
                          '<button id="cancel-block-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Cancel</button>' +
                        '</div>'
                    );
                } else {
                    console.error('Failed to get user data from database:', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to open block hud:', error);
                console.log(xhr.responseText);
            }
        });
    });

    // Friend deletion hud open button click event handler
    $(document).on('click', '#delete-hud-open-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#hud-message');

        var userSiteUrl = $(this).data('site-url');

        $.ajax({
            url: '/' + userSiteUrl + '/hud_data',
            type: 'get',
            dataType: 'json',
            success: function(response) {
                if (response && response.success) {
                    $curtainDiv.removeClass('hidden');
                    $removeUserConfirmMessage.removeClass('hidden');
                    $removeUserConfirmMessage.append(
                        '<div class="flex flex-col px-2 text-center items-center">' +
                          '<div class="aspect-square size-60">' +
                            '<img src="' + response.profile_picture_url + '" class="size-fit aspect-square rounded-full object-cover">' +
                          '</div>' +
                          '<p class="font-bold text-lg">Do you really want to remove ' + response.first_name + ' ' + response.last_name + ' from your friends?</p>' +
                        '</div>' +
                        '<div class="flex pt-4 justify-center">' +
                          '<button id="remove-user-btn" data-id="' + response.user_id + '" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Remove</button>' +
                          '<button id="cancel-delete-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Cancel</button>' +
                        '</div>'
                    );
                } else {
                    console.error('Failed to get user data from database:', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to open block hud:', error);
                console.log(xhr.responseText);
            }
        });
    });

    // Close hud button click event handler
    $(document).on('click', '#cancel-delete-btn, #cancel-block-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#hud-message');

        $curtainDiv.addClass('hidden');
        $removeUserConfirmMessage.addClass('hidden');
        $removeUserConfirmMessage.empty();
    });

    // Confirm blocking user button click event handler
    $(document).on('click', '#block-user-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#hud-message');

        var userId = $(this).data('id');

        $.ajax({
            url: urlBlockUserAdd + userId + '/',
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    setTimeout(() => {
                        var redirectUrl = "/";
                        window.location.href = redirectUrl;
                    }, 500)
                } else {
                    console.error('Failed to block user:', response.message);
                };
            },
            error: function(xhr, status, error) {
                console.error('Failed to delete friend and remove container:', error);
            }
        });
    });

    // Confirm delete friend button click event handler
    $(document).on('click', '#remove-user-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#hud-message');
        var $dropdownMenuDeleteBtn = $('#delete-hud-open-btn');
        var $friendshipBtnsSection = $('#friendship-btns-section');
        var $separatingHr = $('#separating-hr');

        var userId = $(this).data('id');

        $.ajax({
            url: urlRemoveFriend + userId + '/',
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $dropdownMenuDeleteBtn.remove();
                    $separatingHr.remove();
                    $curtainDiv.addClass('hidden');
                    $removeUserConfirmMessage.addClass('hidden');
                    $removeUserConfirmMessage.empty();

                    $friendshipBtnsSection.append(
                        '<button id="invite-button" class="px-3 h-10 rounded-md text-white bg-sky-950 hover:bg-sky-800">Invite to Friends</button>'
                    );
                } else {
                    console.error('Failed to delete friend:', response.message);
                };
            },
            error: function(xhr, status, error) {
                console.error('Failed to delete friend and remove container:', error);
            }
        });
    });
});