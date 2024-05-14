$(".save-photo").click(function () {
    $("#failed-upload-photo").remove();
    $("#unsupported-extension").remove();
    let input = $("#formFile")[0];

    if (input.files && input.files[0]) {
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
                let successMessage = $('<small class="text-success" id="success-upload-photo">Фотография успешно загружена</small>');
                $(".upload-photo").after(successMessage);
            },
            error: function (xhr, status, error) {
                console.error("Ошибка при загрузке файла на сервер:", error);
                let unsupportedExtensionMessage = $('<small class="text-danger" id="unsupported-extension">Невозможно обработать данное изображение</small>');
                $(".upload-photo").after(unsupportedExtensionMessage);
            }
        });
        setTimeout(function () {
            location.reload();
        }, 2000);
    } else {
        let errorMessage = $('<small class="text-danger" id="failed-upload-photo">Пожалуйста, выберите фотографию</small>');
        $(".upload-photo").after(errorMessage);
    }
});