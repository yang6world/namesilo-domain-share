$(document).ready(function () {
    $('#submitRecord').on('click', function () {
        handleButtonClick('addRecord', 'add');
    });

    // 修改记录按钮点击事件处理
    $('#submitModifyRecord').on('click', function () {
        handleButtonClick('modifyRecord', 'modify');
    });

    $('#submitDeleteRecord').on('click', function () {
        handleButtonClick('deleteRecord', 'delete');
    });

    // 通用的处理函数，接受不同的模态框标识
    function handleButtonClick(modalId, action) {
        const domain = $(`#${modalId} #domain`).val();
        const host = $(`#${modalId} #host`).val();
        const record_id = $(`#${modalId} #selectHost`).val();
        const type = $(`#${modalId} #inputGroupSelect01`).val();
        const recordNum = $(`#${modalId} #recordNum`).val();
        const TTL = $(`#${modalId} #TTL`).val();
        const MX = $(`#${modalId} #MX`).val();

        const data = {
            data: JSON.stringify({
                "action": action,
                "domain": domain,
                "record_id": record_id,
                "host": host,
                "type": type,
                "value": recordNum,
                "ttl": TTL,
                "mx": MX
            })
        };
        $("#loading").addClass("active");

        // 延迟5秒钟刷新页面
        //setTimeout(function() {
        //    location.reload();
        //}, 7000);
        //window.location.reload();
        //console.log(data);

        $(`#${modalId}`).modal('hide');
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/manage",
            data: data,
            success: function (result) {
                $("#loading").removeClass("active");
                var toast = new bootstrap.Toast(document.getElementById('toast'));
                if (result.status == 200) {
                    location.reload();
                }
                if (result.status == 400) {
                    document.getElementById("toastTitle").innerHTML = "警告";
                    document.getElementById("toastBody").innerHTML = "操作失败,请检查是否有重复记录,或输入参数";
                } else {
                    document.getElementById("toastTitle").innerHTML = "警告";
                    document.getElementById("toastBody").innerHTML = "未知错误";
                }
                toast.show();
            },
            error: function (result) {
                console.log(result);
                $("#loading").removeClass("active");
                document.getElementById("toastTitle").innerHTML = "警告";
                document.getElementById("toastBody").innerHTML = "操作失败";
            }
        });


    }
});


setInterval(function () {
    $("#tables").load(location.href + " #tables>*", "");
}, 600000);

