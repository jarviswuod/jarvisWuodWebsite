// Pricing data as JavaScript object
const pricingData = [
  {
    name: "Free",
    price: "0",
    targetAudience: "For Beginners",
    billingPeriod: "Billed annually",
    buttonText: "Start for free",
    features: [
      "1-on-1 coaching",
      "Personalized learning",
      "Hands-on project guidance",
      "Code reviews & feedback",
    ],
    highlight: false,
  },
  {
    name: "Pro",
    price: "29",
    targetAudience: "For Professionals",
    billingPeriod: "Billed annually",
    buttonText: "Continue with Plus",
    features: [
      "1-on-1 coaching",
      "Personalized learning",
      "Hands-on project guidance",
      "Code reviews & feedback",
    ],
    highlight: false,
  },
  {
    name: "Business",
    price: "59",
    targetAudience: "For Teams",
    billingPeriod: "Billed annually",
    buttonText: "Continue with Pro",
    features: [
      "1-on-1 coaching",
      "Personalized learning",
      "Hands-on project guidance",
      "Code reviews & feedback",
    ],
    highlight: true,
  },
  {
    name: "Enterprise",
    price: "119",
    targetAudience: "For Corporates",
    billingPeriod: "Billed annually",
    buttonText: "Continue with Max",
    features: [
      "1-on-1 coaching",
      "Personalized learning",
      "Hands-on project guidance",
      "Code reviews & feedback",
    ],
    highlight: false,
  },
];

const phoneNumber = "+254757464904";

function handleWhatsAppContact(packageName) {
  const message = encodeURIComponent(
    `Hi Jarvis, I'm interested in ${packageName} package`
  );
  window.open(`https://wa.me/${phoneNumber}?text=${message}`, "_blank");
}

function renderPricingPlans() {
  const pricingGrid = document.getElementById("mentorship-pricing-grid");

  pricingData.forEach((plan, index) => {
    const planElement = document.createElement("li");
    planElement.className =
      "border border-[#dedede63] p-4 py-8 flex flex-col gap-2";
    planElement.setAttribute("aria-labelledby", `plan-${index}`);

    // Create plan HTML
    planElement.innerHTML = `
          <p 
            id="plan-${index}"
            class="text-base sm:text-lg md:text-xl lg:text-2xl mb-2 lg:mb-4"
          >
            ${plan.name}
          </p>
          <p>
            <span class="font-bold text-lg sm:text-xl md:text-2xl lg:text-3xl mb-4 lg:mb-6">
              $ ${plan.price}
            </span>
            <span class="text-[#989898]"> / month</span>
          </p>
          <span class="text-xs text-[#989898] sm:text-base font-semibold mb-2 lg:mb-4">
            ${plan.billingPeriod}
          </span>
          <button
            id="contact-btn-${index}"
            class="border border-amber-400 mt-8 px-4 p-2 text-base font-bold ${
              plan.highlight ? "bg-amber-400 text-black" : ""
            }"
            aria-label="Contact about ${plan.name} package via WhatsApp"
          >
            ${plan.buttonText}
          </button>
          <p class="text-[#989898] font-bold mt-4">${plan.targetAudience}</p>
          ${plan.features
            .map(
              (feature) => `
            <p class="text-[#cbcbcb]">
              <span class="bg-[#5a5543a6] text-[#dedede] rounded-sm text-sm p-1 mr-1" aria-hidden="true">
                ✓
              </span>
              <span>${feature}</span>
            </p>
          `
            )
            .join("")}
        `;

    pricingGrid.appendChild(planElement);

    // Add event listener to button
    document
      .getElementById(`contact-btn-${index}`)
      .addEventListener("click", () => {
        handleWhatsAppContact(plan.name);
      });
  });
}

// Initialize the page
document.addEventListener("DOMContentLoaded", renderPricingPlans);
