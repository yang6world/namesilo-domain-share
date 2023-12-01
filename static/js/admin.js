//不怎么会js先用着，后面再改
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

    $('#submitModifyUser').on('click', function () {
        handleButtonClick('modifyUser', 'modifyUser');
    });

    // 修改记录按钮点击事件处理
    $('#submitDeliverDomain').on('click', function () {
        handleButtonClick('deliverDomain', 'deliverDomain');
    });

    // 通用的处理函数，接受不同的模态框标识
    function handleButtonClick(modalId, action) {
        const domain = $(`#${modalId} #domain`).val();
        const record_id = $(`#${modalId} #selectHost`).val();
        const host = $(`#${modalId} #host`).val();
        const type = $(`#${modalId} #inputGroupSelect01`).val();
        const recordNum = $(`#${modalId} #recordNum`).val();
        const TTL = $(`#${modalId} #TTL`).val();
        const MX = $(`#${modalId} #MX`).val();
        const user = $(`#${modalId} #selectUser`).val();
        const userStatus = $(`#${modalId} #selectStatus`).val();

        const data = {
            data: JSON.stringify({
                "action": action,
                "domain": domain,
                "record_id": record_id,
                "host": host,
                "type": type,
                "value": recordNum,
                "ttl": TTL,
                "mx": MX,
                "user": user,
                "userStatus": userStatus
            })
        };
        $("#loading").addClass("active");
        $(`#${modalId}`).modal('hide');
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/admin",
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

$(document).ready(function () {
    $('#saveSetting').on('click', function () {
        handleButtonClick('modify_setting');
    });

    // 修改记录按钮点击事件处理
    $('#syncData').on('click', function () {
        handleButtonClick( 'sync_all');
    });

    // 通用的处理函数，接受不同的模态框标识
    function handleButtonClick(action) {
        const namesilo_api_key = $(`#namesilo_api_key`).val();
        const auth_url = $(`#auth_url`).val();
        const token_url = $(`#token_url`).val();
        const user_url = $(`#user_url`).val();
        const issuer = $(`#issuer`).val();
        const client_id = $(`#client_id`).val();
        const client_secret = $(`#client_secret`).val();
        const redirect_uri = $(`#redirect_uri`).val();
        const secret_key = $(`#secret_key`).val();
        const log_level = $(`#log_level`).val();

        const data = {
            data: JSON.stringify({
                "action": action,
                "namesilo_api_key": namesilo_api_key,
                "auth_url": auth_url,
                "token_url": token_url,
                "user_url": user_url,
                "issuer": issuer,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "secret_key": secret_key,
                "log_level": log_level
            })
        };
        $("#loading").addClass("active");
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/admin",
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
// sidebar.js

document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.sidebar-link');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            links.forEach(item => {
                item.classList.remove('active');
            });

            this.classList.add('active');
        });
    });
});

$(document).ready(function () {
    const button01 = document.getElementById('button01');
    const button02 = document.getElementById('button02');
    const button03 = document.getElementById('button03');
    const recordTables = document.getElementById('recordTables');
    const userTables = document.getElementById('userTables');
    const setting= document.getElementById('setting');
    const deleteRecord = document.getElementById('deleteRecord');
    const deleteRecordTitle = document.getElementById('deleteRecordTitle');
    const modifyRecord = document.getElementById('modifyRecord');
    const modifyRecordTitle = document.getElementById('modifyRecordTitle');
    const recordText = document.getElementById('recordText');
    const ttlText = document.getElementById('ttlText');
    const mxText = document.getElementById('mxText');
    const typeText = document.getElementById('typeText');
    const statusText = document.getElementById('statusText');

    const modifyUserText = document.getElementById('modifyRecord').querySelector('#userText');
    const deleteUserText = document.getElementById('deleteRecord').querySelector('#userText');
    const deleteSelectHost = document.getElementById('selectHostText');

    const sumbitModifyRecord = document.getElementById('submitModifyRecord');
    const sumbitDeleteRecord = document.getElementById('submitDeleteRecord');
    const sumbitModifyUser = document.getElementById('submitModifyUser');
    const sumbitDeliverDomain = document.getElementById('submitDeliverDomain');
    $('#domainButton').on('click', function () {
        button01.innerHTML = "添加记录";
        button01.dataset.bsTarget = "#addRecord";
        button02.innerHTML = "修改记录";
        button02.dataset.bsTarget = "#modifyRecord";
        button03.innerHTML = "删除记录";
        button01.hidden = false;
        button03.hidden = false;
        button02.hidden = false;

        recordTables.hidden = false;
        userTables.hidden = true;
        setting.hidden = true;
        modifyRecord.id="modifyRecord";
        modifyRecordTitle.innerHTML = "修改记录";
        deleteRecord.id="deleteRecord";
        deleteRecordTitle.innerHTML = "删除记录";
        recordText.hidden = false;
        ttlText.hidden = false;
        mxText.hidden = false;
        typeText.hidden = false;
        statusText.hidden = true;

        modifyUserText.hidden = true;
        deleteUserText.hidden = true;
        deleteSelectHost.hidden = false;

        sumbitModifyRecord.hidden = false;
        sumbitDeleteRecord.hidden = false;
        sumbitModifyUser.hidden = true;
        sumbitDeliverDomain.hidden = true;

    });
    $('#userButton').on('click', function () {
        button01.innerHTML = "分配域名";
        button01.dataset.bsTarget = "#deliverDomain";
        button01.hidden = false;
        button02.innerHTML = "修改状态";
        button02.dataset.bsTarget = "#modifyUser";
        button02.hidden = false;
        button03.hidden = true;
        recordTables.hidden = true;
        userTables.hidden = false;
        setting.hidden = true;
        deleteRecord.id="modifyUser";
        deleteRecordTitle.innerHTML = "修改状态";
        modifyRecord.id="deliverDomain";
        modifyRecordTitle.innerHTML = "分配域名";
        recordText.hidden = true;
        ttlText.hidden = true;
        mxText.hidden = true;
        typeText.hidden = true;
        statusText.hidden = false;

        modifyUserText.hidden = false;
        deleteUserText.hidden = false;
        deleteSelectHost.hidden = true;

        sumbitModifyRecord.hidden = true;
        sumbitDeleteRecord.hidden = true;
        sumbitModifyUser.hidden = false;
        sumbitDeliverDomain.hidden = false;

    });
    $('#settingButton').on('click', function () {
        button01.hidden = true;
        button02.hidden = true;
        button03.hidden = true;
        recordTables.hidden = true;
        userTables.hidden = true;
        setting.hidden = false;


    });
});

setInterval(function () {
    $("#tables").load(location.href + " #tables>*", "");
}, 120000);