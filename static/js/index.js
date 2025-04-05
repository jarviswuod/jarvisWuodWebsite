"use strict";

// HOME HERO CARD SLIDER
const cards = document.querySelectorAll(".home-hero-card");
const section = document.querySelector('section[style*="background-image"]');

const newImageUrl = [
  "static/hero-img.webp",
  "static/hero-img2.webp",
  "static/hero-img3.webp",
];

let index = 0;

function rotateContent(i) {
  cards.forEach((card, idx) => {
    card.classList.toggle("hidden", idx !== i);
  });
  section.style.backgroundImage = `url('${newImageUrl[i]}')`;
}

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
