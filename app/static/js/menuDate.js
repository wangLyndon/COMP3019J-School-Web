const menuDate = document.querySelector("#menuDate");

// Set date restrictions
const today = new Date();
const nextWeek = new Date();

// Only one week allowed
nextWeek.setDate(today.getDate() + 7);

menuDate.min = formatDate(today);
menuDate.max = formatDate(nextWeek);


function formatDate(date) {
    let year = date.getFullYear();
    // The default starts at 0, so +1
    let monthInt = date.getMonth() + 1;
    let month = monthInt < 10 ? "0" + monthInt.toString() : monthInt.toString();
    let dayInt = date.getDate();
    let day = dayInt < 10 ? "0" + dayInt.toString() : dayInt.toString();

    return `${year}-${month}-${day}`;
}
