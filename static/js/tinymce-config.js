document.addEventListener("DOMContentLoaded", function () {
    tinymce.init({
        selector: "textarea",
        setup: function (editor) {
            editor.on("Change", function () {
                const images = editor.getDoc().getElementsByTagName("img");
                for (let img of images) {
                    if (!img.getAttribute("alt")) {
                        img.setAttribute("alt", "Paradise Boat Rides in Naivasha");
                    }
                }
            });
        }
    });
});
