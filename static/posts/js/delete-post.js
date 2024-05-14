$("#delete-post").click(function () {
    let postId = $(this).attr("data-post-id");

    let data = {
        "postId": postId
    }

    $.ajax({
        url: "/delete-post/",
        type: "DELETE",
        data: JSON.stringify(data),
        processData: false,
        contentType: false,
        success: () => {
            console.log("Пост был успешно удален");
            window.location.href = "/posts/"
        },
        error: (xhr, status, error) => {
            console.error("Ошибка при удалении поста:", error);
        }
    });
})