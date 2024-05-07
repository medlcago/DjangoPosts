$(".save-photo").click(function () {
    $("#no-photo").remove();
    let input = $("#formFile")[0];

    if (input.files && input.files[0]) {
        $(".upload-photo").next("small.text-danger").remove();

        let fileData = new FormData();
        fileData.append("file", input.files[0]);
        $.ajax({
            url: "/update-profile-photo/",
            type: "POST",
            data: fileData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log("Файл успешно загружен на сервер");
            },
            error: function (xhr, status, error) {
                console.error("Ошибка при загрузке файла на сервер:", error);
            }
        });
        setTimeout(function () {
            location.reload();
        }, 2000);
    } else {
        let errorMessage = $('<small class="text-danger" id="no-photo">Пожалуйста, выберите фото</small>');
        $(".upload-photo").after(errorMessage);
    }
});