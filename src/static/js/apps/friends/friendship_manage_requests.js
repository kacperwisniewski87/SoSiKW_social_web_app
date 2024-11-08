$(document).ready(function() {
    var urlFriendRequestAccept = $('.urlDataContainer').data('friend-request-accept');
    var urlFriendRequestReject = $('.urlDataContainer').data('friend-request-reject');
    var urlFriendRequestCancel = $('.urlDataContainer').data('friend-request-cancel');
    var urlBlockUserAdd = $('.urlDataContainer').data('block-user-add');
    var urlBlockUserRemove = $('.urlDataContainer').data('block-user-remove');
    var urlRemoveFriend = $('.urlDataContainer').data('remove-friend');
    var urlAvatarMale = $('.urlDataContainer').data('url-avatar-male');
    var urlAvatarFemale = $('.urlDataContainer').data('url-avatar-female');
    var urlAvatarDefault = $('.urlDataContainer').data('url-avatar-default');
    var friendsDataJson = $('.urlDataContainer').data('friends-data-json');

    var csrftoken = $('meta[name="csrf-token"]').attr('content');

    // Accept request button click event handler
    $(document).on('click', '#request-accept-btn', function() {
        var requestId = $(this).data('user-id');
        var $requestContainer = $(this).closest('.friend-request-container');
        var $requestsListSection = $(this).closest('#requests-list-section');


        $.ajax({
            url: urlFriendRequestAccept + requestId,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $requestContainer.remove();

                    var $requestCountElement = $('#requests-count-tag');
                    var newCount = response.awaiting_requests_count;

                    if (newCount > 0) {
                        $requestCountElement.text(newCount);
                    } else {
                        $requestCountElement.remove();
                        $requestsListSection.append(
                            '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                            '<p>There are no pending invitations.</p>' +
                            '</div>'
                        );
                    }

                } else {
                    console.error('Failed to accept request and delete container:', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to accept request and delete container:', error);
            }
        });
    });

    // Reject request button click event handler
    $(document).on('click', '#request-reject-btn', function() {
        var requestId = $(this).data('user-id');
        var $requestContainer = $(this).closest('.friend-request-container');
        var $requestsListSection = $(this).closest('#requests-list-section');

        $.ajax({
            url: urlFriendRequestReject + requestId,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $requestContainer.remove();

                    var $requestCountElement = $('#requests-count-tag');
                    var newCount = response.awaiting_requests_count;

                    if (newCount > 0) {
                        $requestCountElement.text(newCount);
                    } else {
                        $requestCountElement.remove();
                        $requestsListSection.append(
                            '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                            '<p>There are no pending invitations.</p>' +
                            '</div>'
                        );
                    }

                } else {
                    console.error('Failed to reject request and delete container:', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to reject request and delete container:', error);
            }
        });
    });

    // Cancel request button click event handler
    $(document).on('click', '#request-cancel-btn', function() {
        var requestId = $(this).data('user-id');
        var $requestContainer = $(this).closest('.friend-request-container');
        var $requestsListSection = $(this).closest('#requests-list-section');

        $.ajax({
            url: urlFriendRequestCancel + requestId,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $requestContainer.remove();

                    var sentCount = response.sent_requests_count;

                    if (sentCount == 0) {
                        $requestsListSection.append(
                            '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                            '<p>There are no pending invitations.</p>' +
                            '</div>'
                        )
                    }
                } else {
                    console.error('Failed to cancel request and delete container:', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to cancel request and delete container:', error);
            }
        });
    });

    // Block user request button click event handler
    $(document).on('click', '#block-user-btn, .block-user-confirm-btn', function() {
        var userId = $(this).data('user-id');
        var $requestContainer = $(this).closest('.friend-request-container');
        var $requestsListSection = $(this).closest('#requests-list-section');
        var $friendsListSection = $(this).closest('#friends-list-section');

        $.ajax({
            url: urlBlockUserAdd + userId + '/',
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $requestContainer.remove();

                    var $requestCountElement = $('#requests-count-tag');
                    var newCount = response.awaiting_requests_count;

                    if (newCount > 0) {
                        $requestCountElement.text(newCount);
                    } else {
                        $requestCountElement.remove();
                        if ($requestsListSection !== undefined && response.requests_count == 0) {
                            $requestsListSection.append(
                                '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                                '<p>There are no pending invitations.</p>' +
                                '</div>'
                            );
                        };
                        if ($friendsListSection !== undefined && response.friends_count == 0) {
                            $friendsListSection.append(
                                '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                                '<p>You do not have friends.</p>' +
                                '</div>'
                            );
                        }
                    }
                } else {
                    console.error('Failed to block user and delete container (success):', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to block user and delete container (error):', error);
            }
        });
    });

    // Unblock user request button click event handler
    $(document).on('click', '#unblock-user-btn', function() {
        var userId = $(this).data('user-id');
        var $blockedUserContainer = $(this).closest('.blocked-user-container');
        var $blockedListSection = $(this).closest('#blocked-list-section');

        $.ajax({
            url: urlBlockUserRemove + userId + '/',
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $blockedUserContainer.remove();

                    if (response.blocked_users_count == 0) {
                        $blockedListSection.append(
                            '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                            '<p>You did not blocked anyone.</p>' +
                            '</div>'
                        );
                    };

                    var $requestCountMainElement = $('#requests-count-main-tag');
                    var newCount = response.awaiting_requests_count;

                    if (newCount == 1 && ($('#requests-count-inner-tag').length == 0)) {
                        $requestCountMainElement.append('<p id="requests-count-inner-tag" class="size-9 p-1 bg-red-600 rounded-full text-center text-white content-center absolute right-1" title="Unanswered friend requests">' + newCount + '</p>');
                    } else if (newCount > 1) {
                        var $requestCountInnerElement = $('#requests-count-inner-tag');
                        $requestCountInnerElement.text(newCount);
                    }
                } else {
                    console.error('Failed to block user and delete container:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to unblock user and delete container:', error);
            }
        });
    });

    // Friend deletion hud open button click event handler
    $(document).on('click', '.delete-user-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#remove-user-confirm-message');

        var userId = $(this).data('user-id');
        var selectedFriend = friendsDataJson.filter(function(item) { return item.pk === userId; })[0];

        let profileImageUrl;
        if (selectedFriend["fields"]["profile_image_url"] !== null) {
            profileImageUrl = selectedFriend["fields"]["profile_image_url"];
        } else {
            if (selectedFriend["fields"]["gender"] === 'male') {
              profileImageUrl = urlAvatarMale;
            } else if (selectedFriend["fields"]["gender"] === 'female') {
              profileImageUrl = urlAvatarFemale;
            } else {
              profileImageUrl = urlAvatarDefault;
            }
        };

        $curtainDiv.removeClass('hidden');
        $removeUserConfirmMessage.removeClass('hidden');
        $removeUserConfirmMessage.append(
            '<div class="flex flex-col px-2 text-center items-center">' +
              '<div class="aspect-square size-60">' +
                '<img src="' + profileImageUrl + '" class="size-fit aspect-square rounded-full object-cover">' +
              '</div>' +
              '<p class="font-bold text-lg">Do you really want to remove ' + selectedFriend["fields"]["first_name"] + ' ' + selectedFriend["fields"]["last_name"] + ' from your friends?</p>' +
            '</div>' +
            '<div class="flex pt-4 justify-center">' +
              '<button id="delete-user-confirm-btn" data-user-id="' + userId + '" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Remove</button>' +
              '<button id="cancel-hud-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Cancel</button>' +
            '</div>'
        );
    });

    // Friend block hud open button click event handler
    $(document).on('click', '.block-user-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#remove-user-confirm-message');

        var userId = $(this).data('user-id');
        var selectedFriend = friendsDataJson.filter(function(item) { return item.pk === userId; })[0];

        let profileImageUrl;
        if (selectedFriend["fields"]["profile_image_url"] !== null) {
            profileImageUrl = selectedFriend["fields"]["profile_image_url"];
        } else {
            if (selectedFriend["fields"]["gender"] === 'male') {
              profileImageUrl = urlAvatarMale;
            } else if (selectedFriend["fields"]["gender"] === 'female') {
              profileImageUrl = urlAvatarFemale;
            } else {
              profileImageUrl = urlAvatarDefault;
            }
        };

        $curtainDiv.removeClass('hidden');
        $removeUserConfirmMessage.removeClass('hidden');
        $removeUserConfirmMessage.append(
            '<div class="flex flex-col px-2 text-center items-center">' +
              '<div class="aspect-square size-60">' +
                '<img src="' + profileImageUrl + '" class="size-fit aspect-square rounded-full object-cover">' +
              '</div>' +
              '<p class="font-bold text-lg">Do you really want to block ' + selectedFriend["fields"]["first_name"] + ' ' + selectedFriend["fields"]["last_name"] + '?</p>' +
            '</div>' +
            '<div class="flex pt-4 justify-center">' +
              '<button id="block-user-confirm-btn" data-user-id="' + userId + '" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Block</button>' +
              '<button id="cancel-hud-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Cancel</button>' +
            '</div>'
        );
    });

    // Cancel friend deletion hud button click event handler
    $(document).on('click', '#cancel-hud-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#remove-user-confirm-message');

        $curtainDiv.addClass('hidden');
        $removeUserConfirmMessage.addClass('hidden');
        $removeUserConfirmMessage.empty();
    });

    // Confirm delete friend button click event handler
    $(document).on('click', '#delete-user-confirm-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#remove-user-confirm-message');
        var $friendsListSection = $('#friends-list-section');

        var userId = $(this).data('user-id');

        $.ajax({
            url: urlRemoveFriend + userId + '/',
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    var $friendContainer = $('#friend-container-' + userId);
                    $friendContainer.remove();
                    $curtainDiv.addClass('hidden');
                    $removeUserConfirmMessage.addClass('hidden');
                    $removeUserConfirmMessage.empty();

                    var newCount = response.friends_count;
                    if ($friendsListSection !== undefined && response.friends_count == 0) {
                        $friendsListSection.append(
                            '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                            '<p>You do not have friends.</p>' +
                            '</div>'
                        );
                    };
                } else {
                    console.error('Failed to delete user and container:', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to delete friend and remove container:', error);
            }
        });
    });

    // Block user request button click event handler
    $(document).on('click', '#block-user-confirm-btn', function() {
        var $curtainDiv = $('#curtain-screen');
        var $removeUserConfirmMessage = $('#remove-user-confirm-message');
        var $friendsListSection = $('#friends-list-section');

        var userId = $(this).data('user-id');

        $.ajax({
            url: urlBlockUserAdd + userId + '/',
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    var $friendContainer = $('#friend-container-' + userId);
                    $friendContainer.remove();
                    $curtainDiv.addClass('hidden');
                    $removeUserConfirmMessage.addClass('hidden');
                    $removeUserConfirmMessage.empty();

                    var newCount = response.friends_count;
                    if ($friendsListSection !== undefined && response.friends_count == 0) {
                        $friendsListSection.append(
                            '<div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">' +
                            '<p>You do not have friends.</p>' +
                            '</div>'
                        );
                    };
                } else {
                    console.error('Failed to delete user and container:', response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to block user and delete container (error):', error);
            }
        });
    });
});
