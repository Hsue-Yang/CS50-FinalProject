let hasMore = true;
let currentPage = 1;
let selectedSites = [];
let currentSuggestion = 0;
const searchSuggestions = [
  "iPhone 15",
  "MacBook Air",
  "AirPods Pro",
  "iPad Pro",
  "Nike Air Force",
];

document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("searchInput");
  const websiteChips = document.getElementById("websiteChips");
  const sentinel = document.getElementById("sentinel");
  sentinel.style.display = "none";
  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      searchProducts();
    }
  });
  setInterval(() => rotatePlaceholder(input), 3000);

  websiteChips.addEventListener("click", function (e) {
    if (e.target.classList.contains("website-chip")) {
      e.target.classList.toggle("disabled");

      const siteName = e.target.dataset.site?.toLowerCase();
      const site_products = document.querySelectorAll(`.${siteName}`);
      if (site_products.length > 0) {
        site_products.forEach((product) => {
          product.classList.toggle("d-none");
        });
      }
    }
  });

  if (sentinel) {
    const observer = new IntersectionObserver(async (entries) => {
      if (entries[0].isIntersecting && hasMore) {
        const query = document.getElementById("searchInput").value.trim();
        selectedSites = getSelectedSites();
        if (query && selectedSites.length > 0) {
          await loadMoreProducts(query, selectedSites);
        }
      }
    });
    observer.observe(sentinel);
  }
});

function rotatePlaceholder(input) {
  input.placeholder = `Enter a product name, for example:：${searchSuggestions[currentSuggestion]}`;
  currentSuggestion = (currentSuggestion + 1) % searchSuggestions.length;
}

function getSelectedSites() {
  return Array.from(
    document.querySelectorAll(".website-chip:not(.disabled)")
  ).map((el) => el.dataset.site);
}

async function searchProducts() {
  const loadingSpinner = document.getElementById("loadingSpinner");
  const searchResults = document.getElementById("searchResults");
  const noResults = document.getElementById("noResults");
  const sentinel = document.getElementById("sentinel");
  const query = document.getElementById("searchInput");
  const keyword = query.value.trim();
  hasMore = true;
  currentPage = 1;
  if (!keyword) {
    alert("Please enter a product name");
    return;
  }

  selectedSites = getSelectedSites();
  if (selectedSites.length === 0) {
    alert("Please select at least one shopping website");
    return;
  }
  searchResults.innerHTML = "";
  sentinel.style.display = "none";
  noResults.style.display = "none";
  loadingSpinner.style.display = "block";

  const success = await loadMoreProducts(keyword, selectedSites);
  loadingSpinner.style.display = "none";
  if (!success) {
    noResults.style.display = "block";
  } else {
    sentinel.style.display = "block";
  }
}

async function loadMoreProducts(keyword, selectedSites) {
  const sentinel = document.getElementById("sentinel");
  try {
    const response = await fetch("/shopping/search/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",
      },
      body: JSON.stringify({
        keyword: keyword,
        site: selectedSites,
        page: currentPage,
      }),
    });

    const data = await response.json();
    const products = data["products"] || [];

    if (products.length === 0) {
      hasMore = false;
      sentinel.style.display = "none";
      return false;
    }

    displayResults(products);
    currentPage++;
    return true;
  } catch (error) {
    hasMore = false;
    sentinel.style.display = "none";
    return false;
  }
}

function displayResults(products) {
  const resultsContainer = document.getElementById("searchResults");

  if (products.length === 0) {
    document.getElementById("noResults").style.display = "block";
    return;
  }

  resultsContainer.innerHTML += products
    .map(
      (product) => `
                <div class="col-lg-4 col-md-6 ${product.site}">
                    <div class="product-card h-100">
                        <div class="position-relative">
                            <img src="${product.image}" alt="${
        product.name
      }" class="product-image">
                        </div>
                        <div class="card-body p-3">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <small class="text-primary fw-bold">${
                                  product.site
                                }</small>
                                <span class="badge ${
                                  product.type == "Offer"
                                    ? "bg-success"
                                    : "bg-danger"
                                }">${
        product.type == "Offer" ? "In Stock" : "Out of Stock"
      }</span>
                            </div>
                            <h6 class="card-title">${product.name}</h6>
                            <div class="price-section">
                                <div class="d-flex align-items-center">
                                    <span class="price-tag">${
                                      product.priceCurrency
                                    }$ ${product.price}</span>
                                </div>
                            </div>
                            <div class="d-grid">
                                <a href="${
                                  product.url
                                }" target="_blank" class="btn btn-outline-primary btn-sm">
                                    <i class="fas fa-external-link-alt me-1"></i>Go to Buy
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `
    )
    .join("");
}
