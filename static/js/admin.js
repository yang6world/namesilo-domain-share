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
            $(`#${modalId}`).modal('hide');
            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/admin",
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

// sidebar.js

document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('.sidebar-link');

  links.forEach(link => {
    link.addEventListener('click', function(event) {
      event.preventDefault();

      links.forEach(item => {
        item.classList.remove('active');
      });

      this.classList.add('active');
    });
  });
});


setInterval(function () {
    $("#tables").load(location.href + " #tables>*", "");
}, 120000);