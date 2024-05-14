let originalPostTitle;
let originalPostDescription;

const createErrorMessage = (field, message) => {
    let errorMessage = "<b>" + field + "</b>: " + message;
    let errorElement = $("<p>").html(errorMessage);
    $("#error-messages-js").append(errorElement);
}


$("#post-edit-js").click(function () {
    $("#error-messages-js").empty();
    $("#post-container-js").hide();
    $("#edit-post-container-js").show();

    originalPostTitle = $("#edit-post-title-js").text();
    originalPostDescription = $("#edit-post-description-js").text();

    autosize($("#edit-post-title-js"));
    autosize($("#edit-post-description-js"));
});

$("#post-cancel-js").click(function () {
    $("#error-messages-js").empty();
    $("#edit-post-container-js").hide();
    $("#post-container-js").show();

    $("#post-title-js").val(originalPostTitle);
    $("#post-description-js").val(originalPostDescription);

    $("#edit-post-title-js").val(originalPostTitle);
    $("#edit-post-description-js").val(originalPostDescription);

    autosize.destroy($("#edit-post-title-js"));
    autosize.destroy($("#edit-post-description-js"));
})

$("#post-save-js").click(function () {
    autosize.destroy($("#edit-post-title-js"));
    autosize.destroy($("#edit-post-description-js"));

    $("#edit-post-container-js").hide();
    $("#post-container-js").show();

    let postId = $(this).attr("data-post-id");
    let newPostTitle = $("#edit-post-title-js").val();
    let newPostDescription = $("#edit-post-description-js").val();
    let newPostStatus = $("#edit-post-status-js").val();

    let data = {
        "postId": postId,
        "postTitle": newPostTitle,
        "postDescription": newPostDescription,
        "postStatus": newPostStatus
    }

    $.ajax({
        url: "/update-post/",
        type: "POST",
        data: JSON.stringify(data),
        processData: false,
        contentType: false,
        success: function (response) {
            console.log("Пост был успешно обновлен");
            $("#post-title-js").html(newPostTitle);
            $("#post-description-js").html(newPostDescription);
            $("#error-messages-js").empty();
        },
        error: function (xhr, status, error) {
            console.error("Ошибка при обновлении поста:", error);
            let errors = xhr.responseJSON.errors;
            console.log(errors);
            $("#error-messages-js").empty();

            if (errors.hasOwnProperty("title")) {
                $.each(errors.title, (index, message) => {
                    createErrorMessage("Заголовок", message);
                });
            }

            if (errors.hasOwnProperty("description")) {
                $.each(errors.description, (index, message) => {
                    createErrorMessage("Описание", message);
                });
            }
        }
    });
})