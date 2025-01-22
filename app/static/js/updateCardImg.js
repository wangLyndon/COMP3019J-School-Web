const modules = document.querySelectorAll(".moduleWithImg");
const menus = document.querySelectorAll(".menuWithImg");

if (modules) {
    moduleImages = [
        {url: "../../static/images/001.png"},
        {url: "../../static/images/002.png"},
        {url: "../../static/images/003.png"},
        {url: "../../static/images/004.png"},
        {url: "../../static/images/005.png"},
        {url: "../../static/images/006.png"},
        {url: "../../static/images/007.png"},
        {url: "../../static/images/008.png"},
        {url: "../../static/images/009.png"},
        {url: "../../static/images/010.png"},
        {url: "../../static/images/011.png"},
        {url: "../../static/images/012.png"},
        {url: "../../static/images/013.png"},
    ];

    const numbers = [];

    for (let i = 0; i < modules.length; i++) {

        let num;
        do {
            num = Math.floor(Math.random() * moduleImages.length);
        } while (numbers.includes(num))
        numbers.push(num);
        modules[i].querySelector("img").src = moduleImages[num].url;
    }
}

if (menus) {
    menuImages = [
        {url: "../../static/images/food1.png"},
        {url: "../../static/images/food2.png"},
        {url: "../../static/images/food3.png"},
        {url: "../../static/images/food4.png"},
        {url: "../../static/images/food5.png"},
        {url: "../../static/images/food6.png"},
        {url: "../../static/images/food7.png"},
        {url: "../../static/images/food8.png"},
        {url: "../../static/images/food9.png"},
        {url: "../../static/images/0.png"},
        {url: "../../static/images/1.png"},
        {url: "../../static/images/2.png"},
        {url: "../../static/images/3.png"},
        {url: "../../static/images/4.png"},
        {url: "../../static/images/5.png"},
        {url: "../../static/images/6.png"},
        {url: "../../static/images/7.png"},
        {url: "../../static/images/8.png"},
        {url: "../../static/images/9.png"},
    ];

    const numbers = [];

    for (let i = 0; i < menus.length; i++) {
        let num;
        do {
            num = Math.floor(Math.random() * menuImages.length);
        } while (numbers.includes(num))
        numbers.push(num);
        menus[i].querySelector("img").src = menuImages[num].url;
    }
}
