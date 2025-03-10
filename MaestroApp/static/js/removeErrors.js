document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let errorMessages = document.querySelectorAll(".errorlist, .messages, .non-field-errors");
        errorMessages.forEach(function (error) {
            if (error) {
                error.style.transition = "opacity 0.5s";
                error.style.opacity = "0";

                setTimeout(function () {
                    if (error && error.parentNode) {
                        error.parentNode.removeChild(error);
                    }
                }, 500);
            }
        });

    }, 5000)
});

