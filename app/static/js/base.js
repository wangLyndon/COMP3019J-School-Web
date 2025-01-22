document.querySelector(".toggleTheme").addEventListener("click", toggleTheme);
const cardTitles = document.querySelectorAll(".card a");
const listTitles = document.querySelectorAll(".pageList a");
const forms = document.querySelectorAll(".form");
const header = document.querySelector("header");
const flash = document.querySelector(".flash");

initPage();

let currentY;
let lastY;

window.addEventListener("scroll", function () {
    currentY = window.scrollY;

    if (currentY < 98){
        // Scroll according to the scroll bar
        header.style.top = `-${currentY}px`;
    }else{
        // Max is 98px
        header.style.top = "-98px";
    }

    // If you return to top, the nav will pop up automatically
    if (currentY < lastY){
        header.style.top = "0";
        header.style.zIndex = "100";
        if (document.body.className === "light"){
            header.style.backgroundColor = "#f4f4f4";
        }else{
            header.style.backgroundColor = "#333";
        }
    }

    lastY = currentY;
});

// Make sure the content is not too long
for (let i = 0; i < cardTitles.length; i++) {
    if (cardTitles[i].innerHTML.length > 18) {
        cardTitles[i].innerHTML = cardTitles[i].innerHTML.slice(0, 16) + "...";
    }
}

for (let i = 0; i < listTitles.length; i++) {
    if (listTitles[i].innerHTML.length > 32) {
        listTitles[i].innerHTML = listTitles[i].innerHTML.slice(0, 31) + "...";
    }
}

// Prompt when the user does not enter any input
for (let i = 0; i < forms.length; i++) {
    const input = forms[i].querySelector("input");

    if (!input){
        // Avoid errors caused by not finding the input tag
        continue;
    }

    input.addEventListener("blur", function (e) {
        if (e.target.value.trim() === "") {
            forms[i].classList.add("error");

            forms[i].querySelector(".errorMsg").innerHTML = "You need to input...";
        }
    });

    input.addEventListener("input", function (e) {
        if (e.target.value.trim() !== "") {
            forms[i].classList.remove("error");

            forms[i].querySelector(".errorMsg").innerHTML = "";
        }
    })
}

function toggleTheme() {
    // set light and dark toggle
    document.body.classList.toggle("light");
    document.body.classList.toggle("dark");

    // To store the mode of the page
    localStorage.setItem("mode", document.body.className);
}

function initPage() {

    setTimeout(function () {
        flash.style.display = "none";
    }, 2000);

    const currentUrl = window.location.pathname;
    const as = document.querySelectorAll("nav a");
    for (let i = 0; i < as.length; i++) {
        if (as[i].getAttribute("href") === currentUrl){
            as[i].classList.add("active");
        }
    }

//     const mode = localStorage.getItem("mode");
// if (mode) {
//     document.body.className = mode;
// } else {
//     document.body.className = "light";
// }
}

