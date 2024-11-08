const friendsData = $('#friends_data_json').data('friends-data-json');
const urlAvatarMale = $('#friends_data_json').data('url-avatar-male');
const urlAvatarFemale = $('#friends_data_json').data('url-avatar-female');
const urlAvatarDefault = $('#friends_data_json').data('url-avatar-default');

const input = document.getElementById('friend_search')
const allFriendsContainer = document.getElementById('all_friends_container');

let filteredArr = []

input.addEventListener('keyup', (e)=>{
    const searchText = e.target.value.toLowerCase();
    allFriendsContainer.innerHTML = '';

    filteredArr = friendsData.filter(info=>
      info['fields']['first_name'].toLowerCase().startsWith(searchText.toLowerCase()) ||
      info['fields']['last_name'].toLowerCase().startsWith(searchText.toLowerCase())
    );

    if (filteredArr.length > 0) {
        filteredArr.map(info => {
            const friendLink = document.createElement('a');
            friendLink.id = info.pk;
            friendLink.href = '/' + info['fields']['site_url'];
            friendLink.className = 'w-full hover:underline hover:underline-offset-2';

            let profileImageUrl;
            if (info['fields']['profile_image_url']) {
                profileImageUrl = info['fields']['profile_image_url'];
            } else {
                if (info['fields']['gender'] === 'male') {
                  profileImageUrl = urlAvatarMale;
                } else if (info['fields']['gender'] === 'female') {
                  profileImageUrl = urlAvatarFemale;
                } else {
                  profileImageUrl = urlAvatarDefault;
                }
            }

            friendLink.innerHTML = `
                <div class="aspect-square rounded-xl border-2">
                  <img src="${profileImageUrl}" alt="${info['fields']['first_name']} ${info['fields']['last_name']}" class="object-cover w-full h-full rounded-xl">
                </div>
                <p class="p-1 font-bold">${info['fields']['first_name']} ${info['fields']['last_name']}</p>
            `;

            if (!allFriendsContainer.classList.contains('grid')) {
                allFriendsContainer.classList.add('grid');
            };
            allFriendsContainer.appendChild(friendLink);
        });
    } else {
        allFriendsContainer.classList.remove('grid');
        allFriendsContainer.innerHTML = `
            <div class="p-4 text lg:text-xl text-center bg-gray-300 rounded-xl">
            <p>There is no such person.</p>
            </div>
        `;
    }
});