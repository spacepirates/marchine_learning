var marsImage = document.getElementById('marsImage');

marsImage.style.height = window.innerHeight + "px";

window.onresize = function(event) {
    marsImage.style.height = window.innerHeight + "px";
};