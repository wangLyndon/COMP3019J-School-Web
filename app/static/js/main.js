const img = document.querySelector(".slide img");
const slide = document.querySelector(".slide");
const prev = document.querySelector(".slide .prev");
const next = document.querySelector(".slide .next");
let index = 0;

const images = [
    {url: "../../static/images/bg1.png"},
    {url: "../../static/images/bg2.png"},
    {url: "../../static/images/bg3.png"},
    {url: "../../static/images/bg4.png"},
];

let time = setInterval(update, 3000);

next.addEventListener("click", function () {
    update(false);
});

prev.addEventListener("click", function () {
    update(true);
});

slide.addEventListener("mouseenter", function () {
    clearInterval(time);
});

slide.addEventListener("mouseleave", function () {
    time = setInterval(update, 2000);
});

function update(ori) {
    // Distinguish between prev and next
    if (ori){
        index--;

        // Avoid negative values
        if (index < 0){
            index = images.length - 1;
        }
    }else{
        index++;
    }

    img.src = images[index % images.length].url;
}
