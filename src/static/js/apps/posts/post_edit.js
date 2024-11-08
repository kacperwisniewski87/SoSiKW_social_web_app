$(document).ready(function() {
    var urlUpload = $('.urlDataContainer').data('url-upload');
    var urlDeleteOneTemp = $('.urlDataContainer').data('url-delete-one-temp');
    var urlDeleteAllTemp = $('.urlDataContainer').data('url-delete-all-temp');
    var urlToggleImageStatus = $('.urlDataContainer').data('url-toggle-image-status');

    var csrftoken = $('meta[name="csrf-token"]').attr('content');


    // Handle image upload
    $('#id_image').change(function() {
        var formData = new FormData();
        $.each($(this)[0].files, function(i, file) {
            formData.append('images', file);
        });

        $.ajax({
            url: urlUpload,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                $('#message-section').empty();
                $.each(data, function(i, image) {
                    $('#image-section').append(
                        '<div class="temp-image-container place-content-center flex relative border border-gray-400 bg-gray-400" data-id="' + image.image_id + '">' +
                        '<img src="' + image.image_url + '" class="max-h-60 ">' +
                        '<button title="Delete temporary image" data-id="' + image.image_id + '" class="delete-temp-image-btn p-1 text text-sm font-bold rounded-lg bg-red-500 border border-2 border-black absolute top-2 right-2">' +
                        'Delete' +
                        '</button>' +
                        '</div>'
                    );
                });
            },
          error: function(xhr, status, error) { console.error('Failed to upload image:', error); }
      });
    });

    // Delete image button click event handler
    $(document).on('click', '.delete-temp-image-btn', function() {
        var imageId = $(this).data('id');
        var $imageContainer = $(this).closest('.temp-image-container');

        $.ajax({
            url: urlDeleteOneTemp + imageId,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response && response.success) {
                    $imageContainer.remove();
                    var $image = $imageContainer.find('img');
                    $image.attr('src', $image.attr('src') + '?' + new Date().getTime());
                } else {
                    console.error('Failed to delete image:', response.message);
                }
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
            success: function(data) {
                $('#image-section .temp-image-container').each(function() {
                    $(this).remove();
                });
            },
            error: function(xhr, status, error) {
                console.error('Failed to cancel:', error);
            }
        });
    });

    // Handle image delete/keep button click
    $(document).on('click', '.delete-post-image-btn, .keep-post-image-btn', function() {
        var $button = $(this);
        var imageId = $button.data('id');

        $.ajax({
            url: urlToggleImageStatus + imageId,
            type: 'post',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                if (response.success) {
                    var $imageContainer = $button.closest('.image-container');
                    var $image = $imageContainer.find('img');

                    if (response.edit_to_delete) {
                        $image.addClass('opacity-40');
                        $button.removeClass('delete-post-image-btn')
                            .addClass('keep-post-image-btn')
                            .text('Keep')
                            .removeClass('bg-red-500')
                            .addClass('bg-green-500');
                    } else {
                        $image.removeClass('opacity-40');
                        $button.removeClass('keep-post-image-btn')
                            .addClass('delete-post-image-btn')
                            .text('Delete')
                            .removeClass('bg-green-500')
                            .addClass('bg-red-500');
                    }
                } else {
                    console.error('Failed to toggle image status:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to toggle image status:', error);
            }
        });
    });

    $('#description-input-field').keyup(function () {
        $('#message-section').empty();
    });
});