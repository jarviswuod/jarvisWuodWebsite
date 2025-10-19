// Get CSRF token
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
const csrftoken = getCookie("csrftoken");

// Like functionality
document.querySelectorAll(".likeBtn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const slug = this.dataset.slug;

    fetch(`/blog/${slug}/like/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Update ALL like buttons with the same slug
        document
          .querySelectorAll(`.likeBtn[data-slug="${slug}"]`)
          .forEach((button) => {
            const icon = button.querySelector("i");
            const count = button.querySelector(".likeCount");

            icon.className = data.liked
              ? "fas fa-heart text-red-600 text-2xl"
              : "far fa-heart text-2xl";
            button.setAttribute(
              "aria-label",
              data.liked ? "Unlike this post" : "Like this post"
            );

            if (count) {
              count.textContent = data.total_likes;
            }
          });
      });
  });
});

// Share functionality
const shareOn = (platform) => {
  const blogElement = document.getElementById("blog-content");
  let shareUrl = "";

  const title = blogElement.dataset.title;
  const slug = blogElement.dataset.slug;
  const url = window.location.href;

  switch (platform) {
    case "facebook":
      shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(
        url
      )}`;
      break;
    case "twitter":
      shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(
        url
      )}&text=${encodeURIComponent(title)}`;
      break;
    case "linkedin":
      shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(
        url
      )}`;
      break;
    case "whatsapp":
      shareUrl = `https://wa.me/?text=${encodeURIComponent(title + " " + url)}`;
      break;
  }

  if (shareUrl) {
    window.open(shareUrl, "_blank", "width=600,height=400");

    // Track share
    fetch(`/blog/${slug}/share/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `platform=${platform}`,
    });
  }
};

const copyLink = () => {
  navigator.clipboard.writeText(window.location.href).then(() => {
    alert("Link copied to clipboard!");

    // Track share
    fetch(`/blog/{{ blog.slug }}/share/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "platform=copy_link",
    });
  });
};

// Auto-hide messages
setTimeout(() => {
  const messages = document.getElementById("messages");
  if (messages) {
    messages.style.display = "none";
  }
}, 5000);

// Reply functionality
document.querySelectorAll(".reply-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    const commentId = this.dataset.commentId;
    const form = document.getElementById("commentForm");
    const textarea = form.querySelector("textarea");

    // Add hidden parent_id field
    let parentInput = form.querySelector('input[name="parent_id"]');
    if (!parentInput) {
      parentInput = document.createElement("input");
      parentInput.type = "hidden";
      parentInput.name = "parent_id";
      form.appendChild(parentInput);
    }
    parentInput.value = commentId;

    // Focus on textarea
    textarea.focus();
    textarea.placeholder = "Write a reply...";

    // Add cancel button
    let cancelBtn = form.querySelector(".cancel-reply");
    if (!cancelBtn) {
      cancelBtn = document.createElement("button");
      cancelBtn.type = "button";
      cancelBtn.className =
        "cancel-reply bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors duration-200 mr-2";
      cancelBtn.textContent = "Cancel Reply";
      cancelBtn.addEventListener("click", function () {
        parentInput.remove();
        textarea.placeholder = "Write your comment here...";
        this.remove();
      });
      form
        .querySelector('button[type="submit"]')
        .parentNode.insertBefore(
          cancelBtn,
          form.querySelector('button[type="submit"]')
        );
    }
  });
});

// ------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------
// USER MODAL BACKDROP
// ------------------------------------------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------
const showModalBackdrop = () => {
  const modalBackdrop = document.getElementById("modalBackdrop");
  modalBackdrop.classList.remove("hidden");
  modalBackdrop.classList.add("flex");
};

const showModal = (modalId) => {
  document
    .querySelectorAll(".modal")
    .forEach((modal) => modal.classList.add("hidden"));
  document.getElementById(modalId).classList.remove("hidden");
};

const closeModal = () => {
  const modalBackdrop = document.getElementById("modalBackdrop");
  modalBackdrop.classList.add("hidden");
  modalBackdrop.classList.remove("flex");
  // pendingAction = null;
};

const showLogin = () => {
  showModal("loginModal");
};

const showSignup = () => {
  showModal("signupModal");
};

const showPasswordReset = () => {
  showModal("passwordResetModal");
};

const scrollToCommentForm = () => {
  const commentsSection = document.getElementById("commentFormSection");
  if (commentsSection) {
    commentsSection.scrollIntoView({ behavior: "smooth" });
  }
};
