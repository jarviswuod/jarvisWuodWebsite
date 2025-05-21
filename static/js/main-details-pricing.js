document.addEventListener("DOMContentLoaded", function () {
  // This would normally fetch from an API or external file
  const programData = {
    plans: [
      {
        name: "Free Developer Path",
        price: "$0",
        period: "per month",
        cta: "Start Learning",
        highlightFeature: "12-week introduction to web development",
      },
      {
        name: "Growth Developer",
        price: "$10",
        period: "per month",
        cta: "Level Up",
        highlightFeature: "Build your first professional portfolio",
      },
      {
        name: "Code Pro",
        price: "$20",
        period: "per month",
        cta: "Get Serious",
        highlightFeature: "Recommended for career changers",
      },
      {
        name: "Career Accelerator",
        price: "$112",
        period: "per month",
        cta: "Transform Now",
        highlightFeature: "Premium career services included",
      },
    ],
    categories: [
      {
        name: "Learning & Development",
        features: [
          {
            name: "Learning Modules",
            values: [
              "First 12 weeks only",
              "Unlimited",
              "Unlimited",
              "Unlimited + Advanced",
            ],
          },
          {
            name: "Coding Challenges",
            values: [
              "5 per month",
              "20 per month",
              "Unlimited",
              "Unlimited + Custom",
            ],
          },
          {
            name: "Project Reviews",
            values: [
              "1 basic review",
              "3 detailed reviews",
              "Weekly reviews",
              "Priority unlimited reviews",
            ],
          },
          {
            name: "Tech Stack Coverage",
            values: [
              "HTML, CSS, JS basics",
              "Full frontend stack",
              "Full-stack development",
              "Enterprise architecture",
            ],
          },
          {
            name: "Advanced Topics",
            values: [
              false,
              "Selected topics",
              "Complete curriculum",
              "Specialized expertise",
            ],
          },
        ],
      },
      {
        name: "Tools & Technologies",
        features: [
          {
            name: "Docker & Containerization",
            values: [
              "Basic concepts",
              "Practical implementation",
              "Advanced usage",
              "Enterprise solutions",
            ],
          },
          {
            name: "Cloud Platforms",
            values: [
              "Intro to AWS/GCP",
              "AWS/GCP essentials",
              "Multi-cloud strategies",
              "Cloud architecture design",
            ],
          },
          {
            name: "GitHub & Version Control",
            values: [
              "Basic commands",
              "Branching strategies",
              "CI/CD implementation",
              "Advanced workflows",
            ],
          },
          {
            name: "CI/CD Pipeline Access",
            values: [
              false,
              "Basic pipeline",
              "Complete pipeline",
              "Custom pipelines + training",
            ],
          },
          {
            name: "Microservices Training",
            values: [
              "Basic concepts",
              "Implementation guides",
              "Architecture design",
              "System optimization",
            ],
          },
        ],
      },
      {
        name: "Career Development",
        features: [
          {
            name: "Portfolio Projects",
            values: [
              "1 guided project",
              "3 portfolio-ready",
              "5 advanced projects",
              "Real-world applications",
            ],
          },
          {
            name: "Resume Reviews",
            values: [
              false,
              "One-time review",
              "Quarterly updates",
              "Unlimited optimization",
            ],
          },
          {
            name: "LinkedIn Optimization",
            values: [
              false,
              "Basic tips",
              "Profile overhaul",
              "Personal branding strategy",
            ],
          },
          {
            name: "Job Application Support",
            values: [
              false,
              "Application tips",
              "Application reviews",
              "Personalized job search",
            ],
          },
          {
            name: "Interview Preparation",
            values: [
              false,
              "Basic Q&A prep",
              "Mock interviews",
              "Advanced interview coaching",
            ],
          },
          {
            name: "Job Connections",
            values: [
              false,
              "Job board access",
              "Regional opportunities",
              "Direct employer connections",
            ],
          },
        ],
      },
      {
        name: "Mentorship Access",
        features: [
          {
            name: "1:1 Sessions",
            values: [
              "30 min monthly",
              "30 min bi-weekly",
              "1 hour weekly",
              "Unlimited access",
            ],
          },
          {
            name: "Group Sessions",
            values: [
              "Weekly",
              "Weekly",
              "Weekly + recordings",
              "Weekly + priority Q&A",
            ],
          },
          {
            name: "Response Time",
            values: ["48 hours", "24 hours", "Same day", "Priority support"],
          },
          {
            name: "Code Reviews",
            values: [
              "Basic review",
              "Detailed feedback",
              "In-depth analysis",
              "Architecture consultation",
            ],
          },
          {
            name: "Project Debugging",
            values: [
              false,
              "Limited assistance",
              "Complete support",
              "Emergency support",
            ],
          },
          {
            name: "Career Guidance",
            values: [
              "General advice",
              "Personalized path",
              "Strategic planning",
              "Executive coaching",
            ],
          },
        ],
      },
      {
        name: "Community & Resources",
        features: [
          {
            name: "Community Access",
            values: [
              "Read-only",
              "Full participation",
              "Featured projects",
              "Leadership opportunities",
            ],
          },
          {
            name: "Resource Library",
            values: [
              "Limited articles",
              "Complete library",
              "Premium resources",
              "Early access content",
            ],
          },
          {
            name: "Event Access",
            values: [
              "Public webinars",
              "Monthly workshops",
              "Weekly masterclasses",
              "Private industry events",
            ],
          },
          {
            name: "Networking",
            values: [
              "Community forum",
              "Peer connections",
              "Industry introductions",
              "Executive connections",
            ],
          },
          {
            name: "Project Collaboration",
            values: [
              false,
              "Team projects",
              "Client projects",
              "Revenue-sharing options",
            ],
          },
          {
            name: "Code Repositories",
            values: [
              "Sample code",
              "Framework templates",
              "Enterprise patterns",
              "Proprietary solutions",
            ],
          },
        ],
      },
      {
        name: "Requirements",
        features: [
          {
            name: "Attendance Policy",
            values: [
              "Must attend weekly sessions",
              "Active participation",
              "Monthly progress reviews",
              "Commitment to goals",
            ],
          },
          {
            name: "Trial Period",
            values: ["One month", "One month", "One month", "One month"],
          },
        ],
      },
    ],
  };

  // Generate plan headers
  const planHeadersContainer = document.getElementById("plan-headers");
  const planButtonsContainer = document.getElementById("plan-buttons");

  programData.plans.forEach((plan, index) => {
    // Create plan column header
    const planHeader = document.createElement("th");
    planHeader.className =
      "p-4 text-center border-b-2 border-gray-200 plan-column";
    planHeader.innerHTML = `
                    <div class="font-bold text-lg mb-1">${plan.name}</div>
                    <div class="flex items-center justify-center">
                        <span class="text-2xl font-bold">${plan.price}</span>
                        <span class="text-gray-500 ml-1">${plan.period}</span>
                    </div>
                    <div class="text-xs text-gray-500 mt-1">${plan.highlightFeature}</div>
                    <button class="mt-3 px-4 py-2 rounded-full text-black bg-indigo-600 hover:bg-indigo-700 transition-colors text-sm font-medium">
                        ${plan.cta}
                    </button>
                `;
    planHeadersContainer.appendChild(planHeader);

    // Create plan selection button
    const planButton = document.createElement("button");
    planButton.className = `px-6 py-3 rounded-lg shadow font-medium text-center ${
      index === 2
        ? "bg-indigo-600 text-black"
        : "bg-black text-gray-800 hover:bg-gray-900"
    } ${index === 2 ? "ring-4 ring-indigo-300" : ""}`;
    planButton.innerHTML = `
                    <div class="font-bold">${plan.name}</div>
                    <div class="mt-1">
                        <span class="text-xl font-bold">${plan.price}</span>
                        <span class="text-sm opacity-75">${plan.period}</span>
                    </div>
                `;
    planButtonsContainer.appendChild(planButton);
  });

  // Generate features by category
  const featuresContainer = document.getElementById("features-container");

  programData.categories.forEach((category) => {
    // Category header row
    const categoryRow = document.createElement("tr");
    categoryRow.className = "category-header";
    categoryRow.innerHTML = `
                    <td colspan="${
                      programData.plans.length + 1
                    }" class="p-4 font-bold text-lg bg-gray-900">
                        ${category.name}
                    </td>
                `;
    featuresContainer.appendChild(categoryRow);

    // Feature rows for this category
    category.features.forEach((feature) => {
      const featureRow = document.createElement("tr");
      featureRow.className = "feature-row";

      // Feature name cell
      const featureNameCell = document.createElement("td");
      featureNameCell.className = "p-4 border-r border-gray-200";
      featureNameCell.textContent = feature.name;
      featureRow.appendChild(featureNameCell);

      // Feature values for each plan
      feature.values.forEach((value) => {
        const valueCell = document.createElement("td");
        valueCell.className = "p-4 text-center";

        if (value === false) {
          valueCell.innerHTML = '<span class="text-red-500">✕</span>';
        } else {
          valueCell.textContent = value;
        }

        featureRow.appendChild(valueCell);
      });

      featuresContainer.appendChild(featureRow);
    });
  });
});
