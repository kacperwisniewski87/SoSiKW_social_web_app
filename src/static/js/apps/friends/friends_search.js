const urlSearchResult = $('.urlDataContainer').data('url-search-result');
const urlAvatarMale = $('.urlDataContainer').data('url-avatar-male');
const urlAvatarFemale = $('.urlDataContainer').data('url-avatar-female');
const urlAvatarDefault = $('.urlDataContainer').data('url-avatar-default');
const urlSendFriendRequest = $('.urlDataContainer').data('send-friend-request');
const urlFriendshipRequests = $('.urlDataContainer').data('friendship-requests');

const searchForm = document.getElementById('friends-search-form');
const searchInput = document.getElementById('friends-search-input');
const resultsBox = document.getElementById('results-box');

const csrftoken = $('meta[name="csrf-token"]').attr('content');


// Function for searching users
const sendSearchData = (userData) => {
    $.ajax({
        type: 'POST',
        url: urlSearchResult,
        headers: { 'X-CSRFToken': csrftoken },
        data: {'userData': userData},
        success: (response)=> {
            const responseData = response.foundUsers;
            if (Array.isArray(responseData)) {
                resultsBox.innerHTML = '';
                responseData.forEach(user=> {

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

                    let friendRequestInfo
                    if (user['request_info'] === 'sent') {
                        friendRequestInfo = 'Request was sent';
                    } else if (user['request_info'] === 'received') {
                        friendRequestInfo = 'Request was received';
                    } else {
                        friendRequestInfo = '';
                    }

                    resultsBox.innerHTML += `
                        <a href="/${user['site_url']}" class="flex justify-between items-center p-2 max-h-20 rounded-xl border-2 hover:bg-gray-100 hover:underline hover:underline-offset-2">
                          <div class="flex space-x-4 items-center">
                            <div class="size-16 border rounded-full hover:contrast-75">
                              <img src="${profileImageUrl}" class="size-fit aspect-square rounded-full object-cover">
                            </div>
                            <p class="text font-bold">${user['first_name']} ${user['last_name']}</p>
                          </div>
                          <p class="text text-gray-700">${friendRequestInfo}</p>
                        </a>
                    `
                });
            } else {
                if (searchInput.value.length > 0) {
                    resultsBox.innerHTML = `<p class='flex h-16 p-2 text-xl font-bold items-center justify-center'>${responseData}</b>`
                } else {
                    resultsBox.classList.add('hidden');
                }
            }
        },
        error: (error)=> {
            console.log(error);
        }
    })
};


// Function for clearing and closing input field and result bux hud
function escapePress() {
    searchInput.value = '';
    searchInput.blur()
    resultsBox.innerHTML = '';
    resultsBox.classList.add('hidden');
}


// Event for clicking outside friend search input and result box
searchInput.addEventListener('keyup', function(event) {
    const searchText = event.target.value.toLowerCase();

    resultsBox.classList.remove('hidden');
    sendSearchData(searchText);
});


// Event for preventing search form submission
searchForm.addEventListener('submit', function(event) {
    event.preventDefault();
});


// Event listener for closing hud upon pressing ESC outside of input fields
document.addEventListener('keyup', function(event) {
    if (event.key === 'Escape') {
        escapePress();
    }
});


// Event for clicking outside friend search input and result box
document.addEventListener('click', function(event) {

    var isClickInsideInputField = searchInput.contains(event.target);
    var isClickInsideResultBox = resultsBox.contains(event.target);

    if (!isClickInsideInputField && !isClickInsideResultBox) {
        escapePress();
    }
});

$(document).on('click', '.send-request-btn', function() {
    var userId = $(this).data('user-id');
    var $buttonContainer = $(this).closest('.request-btn-container');

    $.ajax({
        url: urlSendFriendRequest + userId + '/',
        method: "POST",
        headers: { 'X-CSRFToken': csrftoken },
        success: function(response) {
            if (response.success) {
                $buttonContainer.html("<button onclick=\"location.href='" + urlFriendshipRequests + "'\" title='Manage requests' class='w-full p-2 bg-orange-700 rounded-md font-bold text-white hover:bg-orange-800'>Request was sent</button>");
            } else {
                alert("Error: " + response.error);
            }
        },
        error: function(xhr, status, error) {
            console.log("An error occurred: " + error);
        }
    });
});