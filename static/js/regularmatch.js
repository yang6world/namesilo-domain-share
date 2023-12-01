$(document).ready(function () {
    function restrictInput(inputElements) {
        inputElements.forEach(function (inputElement) {
            inputElement.addEventListener('input', function (event) {
                var inputValue = event.target.value;
                var regex = /^\d+$/;

                if (!regex.test(inputValue)) {
                    event.target.value = inputValue.replace(/\D/g, '');
                }
            });
        });
    }

    var ttlInputElements = document.querySelectorAll('#TTL');
    restrictInput(ttlInputElements);

    var mxInputElements = document.querySelectorAll('#MX');
    restrictInput(mxInputElements);
});