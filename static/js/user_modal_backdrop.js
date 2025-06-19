let pendingAction = null; // 'like' or 'comment'
let isUserAuthenticated = false; // You'll set this from your Django template

// Modal management
function showModal(modalId) {
  document.getElementById("modalBackdrop").classList.remove("hidden");
  document
    .querySelectorAll('[id$="Modal"]')
    .forEach((modal) => modal.classList.add("hidden"));
  document.getElementById(modalId).classList.remove("hidden");
}

function closeModal() {
  document.getElementById("modalBackdrop").classList.add("hidden");
  pendingAction = null;
}

function showLogin() {
  showModal("loginModal");
}

function showSignup() {
  showModal("signupModal");
}

function showPasswordReset() {
  showModal("passwordResetModal");
}

// Action handlers
function handleLikeClick() {
  if (!isUserAuthenticated) {
    pendingAction = "like";
    showLogin();
    return;
  }
  performLike();
}

function handleCommentClick() {
  if (!isUserAuthenticated) {
    pendingAction = "comment";
    showLogin();
    return;
  }
  scrollToComments();
}

function performLike() {
  // Your existing like logic here
  const likeBtn = document.getElementById("likeBtn");
  const likeCount = document.getElementById("likeCount");
  const heartIcon = likeBtn.querySelector("i");

  // Toggle like state
  if (heartIcon.classList.contains("far")) {
    heartIcon.classList.remove("far");
    heartIcon.classList.add("fas", "text-red-600");
    likeCount.textContent = parseInt(likeCount.textContent) + 1;
  } else {
    heartIcon.classList.remove("fas", "text-red-600");
    heartIcon.classList.add("far");
    likeCount.textContent = parseInt(likeCount.textContent) - 1;
  }
}

function scrollToComments() {
  // Scroll to comments section or show comment form
  const commentsSection = document.getElementById("commentsSection");
  if (commentsSection) {
    commentsSection.scrollIntoView({ behavior: "smooth" });
  }
}

// Form handlers
function handleLogin(event) {
  event.preventDefault();
  const formData = new FormData(event.target);

  // Your Django login AJAX call here
  fetch("{% url 'users:login' %}", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        isUserAuthenticated = true;
        closeModal();

        // Execute pending action
        if (pendingAction === "like") {
          performLike();
        } else if (pendingAction === "comment") {
          scrollToComments();
        }
      } else {
        // Handle login errors
        console.error("Login failed:", data.errors);
      }
    });
}

function handleSignup(event) {
  event.preventDefault();
  const formData = new FormData(event.target);

  // Your Django signup AJAX call here
  fetch("{% url 'users:signup' %}", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        isUserAuthenticated = true;
        closeModal();

        // Execute pending action
        if (pendingAction === "like") {
          performLike();
        } else if (pendingAction === "comment") {
          scrollToComments();
        }
      } else {
        // Handle signup errors
        console.error("Signup failed:", data.errors);
      }
    });
}

function handlePasswordReset(event) {
  event.preventDefault();
  const formData = new FormData(event.target);

  // Your Django password reset AJAX call here
  fetch("{% url 'users:password_reset' %}", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Password reset email sent!");
        closeModal();
      } else {
        console.error("Password reset failed:", data.errors);
      }
    });
}

// Event listeners
document.getElementById("likeBtn").addEventListener("click", handleLikeClick);
document
  .getElementById("commentBtn")
  .addEventListener("click", handleCommentClick);

// Close modal when clicking backdrop
document
  .getElementById("modalBackdrop")
  .addEventListener("click", function (e) {
    if (e.target === this) {
      closeModal();
    }
  });
