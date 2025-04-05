// "use strict";

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
