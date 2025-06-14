// 示範搜尋建議
let currentSuggestion = 0;
const searchSuggestions = [
  "iPhone 15",
  "MacBook Air",
  "AirPods Pro",
  "iPad Pro",
  "Nike 球鞋",
];

document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("searchInput");
  const websiteChips = document.getElementById("websiteChips");

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
});

function rotatePlaceholder(input) {
  input.placeholder = `輸入商品名稱，例如：${searchSuggestions[currentSuggestion]}`;
  currentSuggestion = (currentSuggestion + 1) % searchSuggestions.length;
}

async function searchProducts() {
  const loadingSpinner = document.getElementById("loadingSpinner");
  const searchResults = document.getElementById("searchResults");
  const noResults = document.getElementById("noResults");
  const query = document.getElementById("searchInput");
  const keyword = query.value.trim();

  if (!keyword) {
    alert("請輸入商品名稱");
    return;
  }

  const selectedSites = Array.from(
    document.querySelectorAll(".website-chip:not(.disabled)")
  ).map((el) => el.dataset.site);

  if (selectedSites.length === 0) {
    alert("請至少選擇一個購物網站");
    return;
  }

  loadingSpinner.style.display = "block";
  searchResults.innerHTML = "";
  noResults.style.display = "none";
  try {
    const response = await fetch("/shopping/search/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",
      },
      body: JSON.stringify({
        keyword,
        site: selectedSites,
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "搜尋失敗");
    }
    const products = data["products"] || [];

    if (products.length === 0) {
      noResults.style.display = "block";
    } else {
      const sorted = products.sort((a, b) => a.price - b.price);
      displayResults(sorted);
    }
  } catch (error) {
    alert("搜尋失敗，請稍後再試。");
    noResults.style.display = "block";
  } finally {
    loadingSpinner.style.display = "none";
    query.value = "";
  }
}

function displayResults(products) {
  const resultsContainer = document.getElementById("searchResults");

  if (products.length === 0) {
    document.getElementById("noResults").style.display = "block";
    return;
  }

  resultsContainer.innerHTML = products
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
        product.type == "Offer" ? "有貨" : "缺貨"
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
                                    <i class="fas fa-external-link-alt me-1"></i>前往購買
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `
    )
    .join("");
}
