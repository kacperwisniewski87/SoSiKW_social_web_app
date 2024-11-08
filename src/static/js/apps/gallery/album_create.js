$(document).ready(function() {
    var urlUpload = $('.urlDataContainer').data('url-upload');
    var urlDeleteOneTemp = $('.urlDataContainer').data('url-delete-one-temp');
    var urlDeleteAllTemp = $('.urlDataContainer').data('url-delete-all-temp');

    var csrftoken = $('meta[name="csrf-token"]').attr('content');


    // Handle image upload
    $('#id_image').change(function() {
        event.preventDefault();
        var formData = new FormData();
        $.each($(this)[0].files, function(i, file) {
            formData.append('images', file);
        });

        $.ajax({
            url: urlUpload,
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                $.each(data, function(i, image) {
                    $('#image-section').append(
                        '<div class="temp-image-container w-full min-w-70 h-[500px] bg-white">' +
                        '<div class="h-[390px] bg-white relative">' +
                        '<div class="grid size-fit h-full justify-items-center items-center">' +
                        '<img src="' + image.image_url + '" class="border-b max-h-[390px]">' +
                        '</div>' +
                        '<button title="Delete temporary image" data-id="' + image.image_id + '" class="delete-temp-image-btn p-1 text text-sm font-bold rounded-lg bg-red-500 border border-2 border-black absolute top-2 right-2">' +
                        'Delete' +
                        '</button>' +
                        '</div>' +
                        '<div class="p-2">' +
                        '<textarea name="temp_img_description_' + image.image_id + '" placeholder="Image description (optional)" class="temp-img-description p-2 w-full min-h-24 max-h-16 bg-gray-100 rounded-2xl text-gray-800 resize-none"></textarea>' +
                        '</div>' +
                        '</div>'
                    );
                    $('#hidden-inputs-container').append(
                        '<input type="hidden" name="temp_img_description_' + image.image_id + '" value="">'
                    );
                });
            },
            error: function(xhr, status, error) {
                console.error('Failed to upload image:', xhr.responseText, status, error);
            }
        });
    });

    // Delete image button click event handler
    $(document).on('click', '.delete-temp-image-btn', function() {
        var image_id = $(this).data('id');
        var $imageContainer = $(this).closest('.temp-image-container');

        $.ajax({
            url: urlDeleteOneTemp + image_id,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $imageContainer.remove();
                    $('input[name="temp_img_description_' + image_id + '"]').remove();
                } else {
                    console.error('Failed to delete image:', response.message); }
                },
            error: function(xhr, status, error) {
                console.error('Failed to delete image:', error);
            }
        });
    });

    // Remove all temp images button click event handler
    $('#remove-all-temp-images-btn').click(function() {
        $.ajax({
            url: urlDeleteAllTemp,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function() {
                $('#image-section').empty();
            },
            error: function(xhr, status, error) { console.error('Failed to cancel:', error); }
        });
    });

    // Before submitting the form, copy the textarea values to the hidden inputs
    $('#albumForm').submit(function(event) {
        var submitButtonName = $(document.activeElement).attr('name');
        if (submitButtonName === 'create_album') {
            $('.temp-img-description').each(function() {
                var desc = $(this).val();
                var name = $(this).attr('name');
                $('input[name="' + name + '"]').val(desc);
            });
        } else {
            console.log('Form submitted with cancel button.');
        }
    });
});