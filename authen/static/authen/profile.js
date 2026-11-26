document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".profile-notice-success").forEach(function (notice) {
        window.setTimeout(function () {
            notice.classList.add("is-dismissing");
            window.setTimeout(function () {
                notice.remove();
            }, 250);
        }, 2000);
    });
});
