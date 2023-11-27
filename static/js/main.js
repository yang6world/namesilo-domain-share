    $(document).ready(function() {
        $('#submitRecord').on('click', function() {
            handleButtonClick('addRecord','add');
        });

        // 修改记录按钮点击事件处理
        $('#submitModifyRecord').on('click', function() {
            handleButtonClick('modifyRecord','modify');
        });

        $('#submitDeleteRecord').on('click', function() {
            handleButtonClick('deleteRecord','delete');
        });

        // 通用的处理函数，接受不同的模态框标识
        function handleButtonClick(modalId,action) {
            const domain = $(`#${modalId} #domain`).val();
            const host = $(`#${modalId} #host`).val();
            const type = $(`#${modalId} #inputGroupSelect01`).val();
            const recordNum = $(`#${modalId} #recordNum`).val();
            const TTL = $(`#${modalId} #TTL`).val();
            const MX = $(`#${modalId} #MX`).val();

            const data = {
                data: JSON.stringify({
                    "action": action,
                    "domain": domain,
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
                success: function(result) {
                    location.reload();
                 },
                error: function (result) {
                    console.log(result);
                }
            });


        }
    });

setInterval(function() {
    $("#tables").load(location.href+" #tables>*","");
}, 600000);

