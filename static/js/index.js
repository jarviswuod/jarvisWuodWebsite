"use strict";

// HOME HERO CARD SLIDER
const cards = document.querySelectorAll(".home-hero-card");
const section = document.querySelector(".home-hero-section");

const newImageUrl = [
  "static/hero-img.webp",
  "static/hero-img2.webp",
  "static/hero-img3.webp",
];

let index = 0;

const rotateContent = (i) => {
  cards.forEach((card, idx) => {
    card.classList.toggle("hidden", idx !== i);
  });
  if (section) {
    section.style.backgroundImage = `url('${newImageUrl[i]}')`;
  }
};

rotateContent(index);
setInterval(() => {
  index = (index + 1) % cards.length;
  rotateContent(index);
}, 10000);

// TWITTER TESTIMONIAL SLIDER
let current = 0;
const testimonialUls = document.querySelectorAll("ul.testimonial.grid");

function showSlide(index) {
  testimonialUls.forEach((ul, i) => ul.classList.toggle("hidden", i !== index));
}

function nextSlide() {
  current = (current + 1) % testimonialUls.length;
  showSlide(current);
}

function prevSlide() {
  current = (current - 1 + testimonialUls.length) % testimonialUls.length;
  showSlide(current);
}

showSlide(current); // init

// //////////////////////////////////////////////////////////
// CONTACT FORM MODAL IN CONTACT PAGE
// //////////////////////////////////////////////////////////
const contactFormModal = document.querySelector(".contact-modal");
const contactOptions = document.querySelector(".contact-options");

const contactFormModalClose = document.querySelector(".close-btn");
const contactFormModalOverlay = document.querySelector(".modal-overlay");

contactOptions?.addEventListener("click", () => {
  contactFormModal.classList.remove("hidden");
});

contactFormModalClose?.addEventListener("click", () => {
  contactFormModal.classList.add("hidden");
});

contactFormModalOverlay?.addEventListener("click", () => {
  contactFormModal.classList.add("hidden");
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") contactFormModal.classList.add("hidden");
});

function showFormSection(section) {
  const forms = document.querySelectorAll(".form--contact");
  forms.forEach((form) => form.classList.add("hidden"));

  const formToShow = document.querySelector(`.${section}`);
  formToShow.classList.remove("hidden");
}

// MENU RESPONSIVENESS
const menu = document.getElementById("menu");
const icon = document.getElementById("menu-icon");

const toggleMenu = () => {
  menu.classList.toggle("max-md:hidden");
  menu.classList.toggle("max-md:flex");
  icon.classList.toggle("ph-list");
  icon.classList.toggle("ph-x");
};

const submenu = document.getElementById("submenu");
const submenuIcon = document.getElementById("submenu-icon");

function showSubmenu() {
  if (window.innerWidth >= 768) {
    submenu.classList.remove("hidden");
    submenuIcon.classList.remove("ph-caret-down");
    submenuIcon.classList.add("ph-caret-up");
  }
}

function hideSubmenu() {
  if (window.innerWidth >= 768) {
    submenu.classList.add("hidden");
    submenuIcon.classList.remove("ph-caret-up");
    submenuIcon.classList.add("ph-caret-down");
  }
}

function toggleSubmenu(e) {
  if (window.innerWidth < 768) {
    // e.preventDefault();
    submenu.classList.toggle("hidden");
    submenuIcon.classList.toggle("ph-caret-down");
    submenuIcon.classList.toggle("ph-caret-up");
  }
}
