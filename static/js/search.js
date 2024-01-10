const searchBox = document.getElementById("searchBox");
const searchBtn = document.getElementById("searchBtn");

searchBtn.addEventListener("click", () => {
	if (searchBox.value != "") window.location.replace(`/store/${searchBox.value}`);
});
searchBox.addEventListener("keydown", function (key) {
	if (key.code == "Enter" && searchBox.value != "") window.location.replace(`/store/${searchBox.value}`);
});
