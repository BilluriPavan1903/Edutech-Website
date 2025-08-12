function toggleProfile() {
  const dropdown = document.getElementById("profile-dropdown");
  dropdown.classList.toggle("hidden");
}

document.addEventListener("DOMContentLoaded", function () {
  const logoutLink = document.getElementById("logoutLink");

  if (logoutLink) {
    logoutLink.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent default link behavior

      const confirmed = confirm("Are you sure you want to logout?");
      if (confirmed) {
        window.location.href = "/login/"; // Or {% url 'login' %} via data attribute if using Django templating
      }
    });
  }
});