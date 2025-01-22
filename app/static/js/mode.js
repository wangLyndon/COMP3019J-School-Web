const mode = localStorage.getItem("mode");
if (mode) {
    document.body.className = mode;
} else {
    document.body.className = "light";
}