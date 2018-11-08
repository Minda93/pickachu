document.getElementById("gomoku").addEventListener("click", function () {
    document.getElementById("gomoku_board").style.display = "block";
    document.getElementById("flaw_image").style.display= "none";
    document.getElementById("aircraft_image").style.display = "none";
});

document.getElementById("flaw_detection").addEventListener("click", function () {
    document.getElementById("gomoku_board").style.display = "none";
    document.getElementById("flaw_image").style.display= "block";
    document.getElementById("aircraft_image").style.display = "none";
});

document.getElementById("aircraft").addEventListener("click", function () {
    document.getElementById("gomoku_board").style.display = "none";
    document.getElementById("flaw_image").style.display= "none";
    document.getElementById("aircraft_image").style.display = "block";
});