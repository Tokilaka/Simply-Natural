const navbarStore = document.getElementById("store");
const dropdown = document.getElementById("dropdown");

function toggleDropdownActive() {
	dropdown.classList.toggle("active");
	console.log("works");
}

navbarStore.addEventListener("mouseenter", toggleDropdownActive);
navbarStore.addEventListener("mouseleave", toggleDropdownActive);

dropdown.addEventListener("mouseenter", toggleDropdownActive);
dropdown.addEventListener("mouseleave", toggleDropdownActive);
