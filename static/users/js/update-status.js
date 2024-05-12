let originalStatus;

$("#edit-profile-js").click(function (e) {
    e.preventDefault();
    originalStatus = $("#user-status-js").text();
    $("#user-status-js").hide();
    $("#edit-profile-js").hide();
    $("#status-input-js").val(originalStatus);
    $("#status-input-container-js").show();
    autosize($("#status-input-js"));
});

$("#cancel-save-status-button-js").click(function (e) {
    $("#status-input-js").val(originalStatus);
    $("#user-status-js").show();
    $("#edit-profile-js").show();
    $("#status-input-container-js").hide();
    autosize.destroy($("#status-input-js"));
})

$("#save-status-button-js").click(function (event) {
    event.preventDefault();
    let newStatus = $("#status-input-js").val();
    $("#user-status-js").text(newStatus);
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
        type: "POST",
        data: JSON.stringify(data),
        processData: false,
        contentType: false,
        success: function (response) {
            console.log("Статус был успешно изменен");
        },
        error: function (xhr, status, error) {
            console.error("Ошибка при смене статуса:", error);
        }
    });
});