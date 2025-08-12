// static/js/signup.js

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signupForm");

  signupForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = document.getElementById("signupUsername").value.trim();
    const password = document.getElementById("signupPassword").value;
    const email = document.getElementById("signupEmail").value.trim();

    // comments

    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$/;
    if (!passwordRegex.test(password)) {
      alert("Password must be at least 8 characters with uppercase, lowercase, number, and special character.");
      return;
    }

    if (!email.endsWith("@gmail.com")) {
      alert("Email must be a Gmail address.");
      return;
    }

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    formData.append("email", email);

    fetch("/signup_user/", {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("Sign up successful!");
        const homeURL = document.getElementById("routeData").dataset.homeUrl;
        window.location.href = homeURL;
      } else {
        alert(data.message || "Sign up failed.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Something went wrong. Please try again.");
    });
  });
});
