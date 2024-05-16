let originalStatus;

const createErrorMessage = (field, message) => {
    let errorMessage = "<b>" + field + "</b>: " + message;
    let errorElement = $("<p>").html(errorMessage);
    $("#error-messages-js").append(errorElement);
}

$("#edit-profile-js").click(function (e) {
    e.preventDefault();
    $("#error-messages-js").empty();
    originalStatus = $("#user-status-js").text();
    $("#user-status-js").hide();
    $("#edit-profile-js").hide();
    $("#status-input-js").val(originalStatus);
    $("#status-input-container-js").show();

    autosize($("#status-input-js"));
});

$("#cancel-save-status-button-js").click(function (e) {
    $("#error-messages-js").empty();
    $("#status-input-js").val(originalStatus);
    $("#user-status-js").show();
    $("#edit-profile-js").show();
    $("#status-input-container-js").hide();

    autosize.destroy($("#status-input-js"));
})

$("#save-status-button-js").click(function (event) {
    event.preventDefault();
    let newStatus = $("#status-input-js").val();
    $("#user-status-js").show();
    $("#edit-profile-js").show();
    $("#status-input-container-js").hide();

    autosize.destroy($("#status-input-js"));

    let data = {
        "status": newStatus
    }
    console.log(data);

    $.ajax({
        url: "/update-profile-status/",
        type: "PATCH",
        data: JSON.stringify(data),
        processData: false,
        contentType: false,
        success: function (response) {
            console.log("Статус был успешно изменен");
            $("#user-status-js").text(newStatus);
            $("#error-messages-js").empty();
        },
        error: function (xhr, status, error) {
            console.error("Ошибка при смене статуса:", error);
            let errors = xhr.responseJSON.errors;
            $("#error-messages-js").empty();

            if (errors.hasOwnProperty("status")) {
                $.each(errors.status, (index, message) => {
                    createErrorMessage("Статус", message);
                });
            }

        }
    });
});