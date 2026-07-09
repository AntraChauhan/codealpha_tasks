document.addEventListener("DOMContentLoaded", function () {

    // Double-click image to like
    document.querySelectorAll(".post-img-dbl").forEach(function (img) {
        img.addEventListener("dblclick", function () {
            window.location.href = img.dataset.like;
        });
    });

    // Heart pop animation on like button click
    document.querySelectorAll(".like-btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            btn.classList.add("heart-pop");
            setTimeout(() => btn.classList.remove("heart-pop"), 300);
        });
    });

    // Auto-scroll chat to bottom
    const chat = document.getElementById("chatMessages");
    if (chat) chat.scrollTop = chat.scrollHeight;

    // Disable comment submit if empty
    document.querySelectorAll(".comment-input").forEach(function (input) {
        const btn = input.closest("form").querySelector(".comment-submit");
        if (btn) {
            btn.disabled = !input.value.trim();
            input.addEventListener("input", function () {
                btn.disabled = !input.value.trim();
            });
        }
    });

});
