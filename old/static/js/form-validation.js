// form-validation.js - Reusable validation for all forms on your website

document.addEventListener("DOMContentLoaded", function () {
  // Get all forms on the page
  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    // Add validation to each form
    setupFormValidation(form);
  });

  /**
   * Sets up validation for a form
   * @param {HTMLFormElement} form - The form to validate
   */
  function setupFormValidation(form) {
    // Store error messages for reuse
    const errorMessages = {
      required: "This field is required",
      email: "Please enter a valid email address",
      phone: "Please enter a valid phone number",
      name: "Please enter your full name (at least 2 words)",
    };

    // Create and insert error elements for each input
    const inputs = form.querySelectorAll("input, select");
    inputs.forEach((input) => {
      const errorElement = document.createElement("div");
      errorElement.className =
        "validation-error text-red-600 text-xs mt-1 hidden";
      errorElement.id = `${input.id}-error`;
      input.parentNode.insertBefore(errorElement, input.nextSibling);

      // Add input event listeners for real-time validation
      input.addEventListener("input", function () {
        validateInput(input);
      });

      input.addEventListener("blur", function () {
        validateInput(input);
      });
    });

    // Add form submit handler
    form.addEventListener("submit", function (event) {
      let isValid = true;

      // Validate all inputs
      inputs.forEach((input) => {
        if (!validateInput(input)) {
          isValid = false;
        }
      });

      if (!isValid) {
        event.preventDefault();
        // Focus the first invalid input
        const firstInvalid = form.querySelector(".is-invalid");
        if (firstInvalid) {
          firstInvalid.focus();
        }
      }
    });

    /**
     * Validates a single input field
     * @param {HTMLElement} input - The input to validate
     * @returns {boolean} - Whether the input is valid
     */
    function validateInput(input) {
      const errorElement = document.getElementById(`${input.id}-error`);
      let isValid = true;
      let errorMessage = "";

      // Reset validation state
      input.classList.remove("is-invalid", "border-red-600");
      input.classList.remove("is-valid", "border-green-600");

      // Skip validation for non-required empty fields
      if (!input.required && input.value.trim() === "") {
        hideError(errorElement);
        return true;
      }

      // Required field validation
      if (input.required && input.value.trim() === "") {
        isValid = false;
        errorMessage = errorMessages.required;
      }
      // Type-specific validation for non-empty fields
      else if (input.value.trim() !== "") {
        switch (input.type) {
          case "email":
            // Email validation using regex
            const emailPattern =
              /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
            if (!emailPattern.test(input.value)) {
              isValid = false;
              errorMessage = errorMessages.email;
            }
            break;

          case "tel":
            // Phone validation - accepting various formats
            const phonePattern =
              /^(?:\+\d{1,3}[-\s]?)?\(?(?:\d{1,4})\)?[-\s]?(?:\d{1,4})[-\s]?(?:\d{1,9})$/;
            if (!phonePattern.test(input.value)) {
              isValid = false;
              errorMessage = errorMessages.phone;
            }
            break;

          case "text":
            // Handle different text fields based on id/name
            if (input.id === "full_name" || input.name === "full_name") {
              // Full name should have at least two words
              const nameParts = input.value.trim().split(/\s+/);
              if (
                nameParts.length < 2 ||
                nameParts.some((part) => part.length < 2)
              ) {
                isValid = false;
                errorMessage = errorMessages.name;
              }
            }
            break;

          case "select-one":
            // Select dropdown validation (already covered by required check)
            break;
        }
      }

      // Update UI based on validation result
      if (isValid) {
        markValid(input, errorElement);
      } else {
        markInvalid(input, errorElement, errorMessage);
      }

      return isValid;
    }

    /**
     * Marks an input as invalid
     */
    function markInvalid(input, errorElement, message) {
      input.classList.add("is-invalid", "border-red-600");
      input.classList.remove("is-valid", "border-green-600");
      errorElement.textContent = message;
      errorElement.classList.remove("hidden");
    }

    /**
     * Marks an input as valid
     */
    function markValid(input, errorElement) {
      input.classList.remove("is-invalid", "border-red-600");
      input.classList.add("is-valid", "border-green-600");
      hideError(errorElement);
    }

    /**
     * Hides an error element
     */
    function hideError(errorElement) {
      errorElement.textContent = "";
      errorElement.classList.add("hidden");
    }
  }
});
