const isWhitespaceString = str => !str.replace(/\s/g, '').length;

$(document).on('click', '#send-message-hud-btn', function() {
    var $curtainDiv = $('#curtain-screen');
    var $sendMessageScreen = $('#hud-message');

    $curtainDiv.removeClass('hidden');
    $sendMessageScreen.removeClass('hidden');
    $sendMessageScreen.append(
        '<form id="send-message-form" class="text-center items-center">' +
          '<p class="pb-4 text-3xl text-sky-950 font-bold">Send message</p>' +
            '<textarea id="new-message-content-textarea" placeholder="Message..." class="w-full min-h-24 max-h-40 p-2 border border-gray-500 rounded-2xl bg-gray-100"></textarea>' +
        '</form>' +
        '<div id="message-error-container" class="hidden mt-2 p-2 bg-red-200 text text-red-600 font-bold border border-red-600 rounded-2xl">' +
        '</div>' +
        '<div class="flex pt-4 justify-center">' +
          '<button id="send-message-confirm-btn" class="w-1/2 py-2 px-3 text-white font-bold bg-sky-700 hover:bg-sky-800 rounded-2xl">Send</button>' +
          '<button id="close-hud-btn" name="cancel" class="w-1/2 ml-2 py-2 px-3 text-white text-center font-bold bg-red-600 hover:bg-red-700 rounded-2xl">Cancel</button>' +
        '</div>'
    );
});


$(document).on('click', '#send-message-confirm-btn', function() {
    var messageContentContainer = $('#new-message-content-textarea');
    var messageContentValue =  messageContentContainer.val();

    if (messageContentValue == null || messageContentValue == '' || isWhitespaceString(messageContentValue)) {
        console.log('Message is empty.');
        var $errorMessage = $('#message-error-container');

        $errorMessage.removeClass('hidden');
        $errorMessage.append('<p>Message is empty.</p>');
        messageContentContainer.val('');
    } else {
        console.log('message sent: ', messageContentValue);
        var csrftoken = $('meta[name="csrf-token"]').attr('content');
        var dataUserId = $('.urlDataContainer').data('user-id');
        var urlSendMessage = $('.urlDataContainer').data('send-message-url');


        $.ajax({
            url: urlSendMessage,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            data: { 'message_content': messageContentValue, 'user_id': dataUserId},
            success: function(response) {
                console.log(response);
                if (response && response.success) {
                    window.location.href = '/' + response.chat_redirect_url;
                } else {
                    console.error('Failed send message:', response.message);
                };
            },
            error: function(xhr, status, error) {
                console.error('Failed send message:', error);
            }
        });
    };
});


$(document).on('keypress', '#new-message-content-textarea', function() {
    var $errorMessage = $('#message-error-container');

    $errorMessage.addClass('hidden');
    $errorMessage.empty();
});


$(document).on('click', '#close-hud-btn', function() {
    var $curtainDiv = $('#curtain-screen');
    var $hudMessage = $('#hud-message');

    $curtainDiv.addClass('hidden');
    $hudMessage.addClass('hidden');
    $hudMessage.empty();
});
