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

    $('#saveSetting').on('click', function () {
        buttonClickSetting('modify_setting');
    });

    // 修改记录按钮点击事件处理
    $('#syncData').on('click', function () {
        buttonClickSetting( 'sync_all');
    });
    function sendAjaxRequest(data) {
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
                } else if (result.status == 400) {
                    document.getElementById("toastTitle").innerHTML = "警告";
                    document.getElementById("toastBody").innerHTML = "操作失败，请检查是否有重复记录或输入参数";
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

    // 通用的处理函数，接受不同的模态框标识
    function buttonClickSetting(action) {
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
        sendAjaxRequest(data);

    }

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
        sendAjaxRequest(data)


    }
    const elements = {
        button01: document.getElementById('button01'),
        button02: document.getElementById('button02'),
        button03: document.getElementById('button03'),
        recordTables: document.getElementById('recordTables'),
        userTables: document.getElementById('userTables'),
        setting: document.getElementById('setting'),
        deleteRecord: document.getElementById('deleteRecord'),
        deleteRecordTitle: document.getElementById('deleteRecordTitle'),
        modifyRecord: document.getElementById('modifyRecord'),
        modifyRecordTitle: document.getElementById('modifyRecordTitle'),
        recordText: document.getElementById('recordText'),
        ttlText: document.getElementById('ttlText'),
        mxText: document.getElementById('mxText'),
        typeText: document.getElementById('typeText'),
        statusText: document.getElementById('statusText'),
        modifyUserText: document.getElementById('modifyRecord').querySelector('#userText'),
        deleteUserText: document.getElementById('deleteRecord').querySelector('#userText'),
        deleteSelectHost: document.getElementById('selectHostText'),
        submitModifyRecord: document.getElementById('submitModifyRecord'),
        submitDeleteRecord: document.getElementById('submitDeleteRecord'),
        submitModifyUser: document.getElementById('submitModifyUser'),
        submitDeliverDomain: document.getElementById('submitDeliverDomain')
    };

    function updateElementsForDomain() {
        elements.button01.innerHTML = "添加记录";
        elements.button01.dataset.bsTarget = "#addRecord";
        elements.button02.innerHTML = "修改记录";
        elements.button02.dataset.bsTarget = "#modifyRecord";
        elements.button03.innerHTML = "删除记录";
        elements.button01.hidden = false;
        elements.button03.hidden = false;
        elements.button02.hidden = false;
        elements.recordTables.hidden = false;
        elements.userTables.hidden = true;
        elements.setting.hidden = true;
        elements.modifyRecord.id = "modifyRecord";
        elements.modifyRecordTitle.innerHTML = "修改记录";
        elements.deleteRecord.id = "deleteRecord";
        elements.deleteRecordTitle.innerHTML = "删除记录";
        elements.recordText.hidden = false;
        elements.ttlText.hidden = false;
        elements.mxText.hidden = false;
        elements.typeText.hidden = false;
        elements.statusText.hidden = true;
        elements.modifyUserText.hidden = true;
        elements.deleteUserText.hidden = true;
        elements.deleteSelectHost.hidden = false;
        elements.submitModifyRecord.hidden = false;
        elements.submitDeleteRecord.hidden = false;
        elements.submitModifyUser.hidden = true;
        elements.submitDeliverDomain.hidden = true;
    }

    function updateElementsForUser() {
        elements.button01.innerHTML = "分配域名";
        elements.button01.dataset.bsTarget = "#deliverDomain";
        elements.button01.hidden = false;
        elements.button02.innerHTML = "修改状态";
        elements.button02.dataset.bsTarget = "#modifyUser";
        elements.button02.hidden = false;
        elements.button03.hidden = true;
        elements.recordTables.hidden = true;
        elements.userTables.hidden = false;
        elements.setting.hidden = true;
        elements.deleteRecord.id = "modifyUser";
        elements.deleteRecordTitle.innerHTML = "修改状态";
        elements.modifyRecord.id = "deliverDomain";
        elements.modifyRecordTitle.innerHTML = "分配域名";
        elements.recordText.hidden = true;
        elements.ttlText.hidden = true;
        elements.mxText.hidden = true;
        elements.typeText.hidden = true;
        elements.statusText.hidden = false;
        elements.modifyUserText.hidden = false;
        elements.deleteUserText.hidden = false;
        elements.deleteSelectHost.hidden = true;
        elements.submitModifyRecord.hidden = true;
        elements.submitDeleteRecord.hidden = true;
        elements.submitModifyUser.hidden = false;
        elements.submitDeliverDomain.hidden = false;
    }

    function updateElementsForSetting() {
        elements.button01.hidden = true;
        elements.button02.hidden = true;
        elements.button03.hidden = true;
        elements.recordTables.hidden = true;
        elements.userTables.hidden = true;
        elements.setting.hidden = false;
    }

    $('#domainButton').on('click', updateElementsForDomain);
    $('#userButton').on('click', updateElementsForUser);
    $('#settingButton').on('click', updateElementsForSetting);
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
/*
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
*/
setInterval(function () {
    $("#tables").load(location.href + " #tables>*", "");
}, 120000);