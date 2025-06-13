// 模擬商品資料
const mockProducts = {
  iphone: [
    {
      name: "iPhone 15 Pro 128GB",
      price: 35900,
      originalPrice: 39900,
      image: "https://via.placeholder.com/300x200?text=iPhone+15+Pro",
      site: "amazon",
      siteName: "Amazon",
      rating: 4.5,
      reviews: 128,
      inStock: true,
      url: "#",
    },
    {
      name: "iPhone 15 Pro 128GB",
      price: 36500,
      originalPrice: 39900,
      image: "https://via.placeholder.com/300x200?text=iPhone+15+Pro",
      site: "pchome",
      siteName: "PChome",
      rating: 4.3,
      reviews: 89,
      inStock: true,
      url: "#",
    },
    {
      name: "iPhone 15 Pro 128GB",
      price: 35500,
      originalPrice: 39900,
      image: "https://via.placeholder.com/300x200?text=iPhone+15+Pro",
      site: "shopee",
      siteName: "蝦皮購物",
      rating: 4.7,
      reviews: 256,
      inStock: false,
      url: "#",
    },
  ],
  macbook: [
    {
      name: "MacBook Air M2 13吋",
      price: 35900,
      originalPrice: 39900,
      image: "https://via.placeholder.com/300x200?text=MacBook+Air",
      site: "amazon",
      siteName: "Amazon",
      rating: 4.8,
      reviews: 342,
      inStock: true,
      url: "#",
    },
    {
      name: "MacBook Air M2 13吋",
      price: 36900,
      originalPrice: 39900,
      image: "https://via.placeholder.com/300x200?text=MacBook+Air",
      site: "momo",
      siteName: "momo購物",
      rating: 4.6,
      reviews: 187,
      inStock: true,
      url: "#",
    },
  ],
};

// 網站選擇功能
let selectedSites = ["amazon", "pchome", "shopee", "momo"];

document.getElementById("websiteChips").addEventListener("click", function (e) {
  if (e.target.classList.contains("website-chip")) {
    const site = e.target.dataset.site;
    if (selectedSites.includes(site)) {
      selectedSites = selectedSites.filter((s) => s !== site);
      e.target.classList.add("disabled");
    } else {
      selectedSites.push(site);
      e.target.classList.remove("disabled");
    }
  }
});

// 搜尋功能
function searchProducts() {
  const query = document
    .getElementById("searchInput")
    .value.toLowerCase()
    .trim();
  if (!query) {
    alert("請輸入商品名稱");
    return;
  }

  // 顯示載入動畫
  document.getElementById("loadingSpinner").style.display = "block";
  document.getElementById("searchResults").innerHTML = "";
  document.getElementById("noResults").style.display = "none";

  // 模擬搜尋延遲
  setTimeout(() => {
    const results = findProducts(query);
    displayResults(results);
    document.getElementById("loadingSpinner").style.display = "none";
  }, 2000);
}

// 搜尋商品邏輯
function findProducts(query) {
  let results = [];

  // 簡單的關鍵字匹配
  for (const [key, products] of Object.entries(mockProducts)) {
    if (query.includes(key) || key.includes(query)) {
      results = results.concat(
        products.filter((p) => selectedSites.includes(p.site))
      );
    }
  }

  // 按價格排序
  return results.sort((a, b) => a.price - b.price);
}

// 顯示搜尋結果
function displayResults(products) {
  const resultsContainer = document.getElementById("searchResults");

  if (products.length === 0) {
    document.getElementById("noResults").style.display = "block";
    return;
  }

  const html = products
    .map(
      (product) => `
                <div class="col-lg-4 col-md-6">
                    <div class="product-card">
                        ${
                          product.originalPrice > product.price
                            ? `<div class="discount-badge">-${Math.round(
                                (1 - product.price / product.originalPrice) *
                                  100
                              )}%</div>`
                            : ""
                        }
                        <div class="position-relative">
                            <img src="${product.image}" alt="${
        product.name
      }" class="product-image">
                            ${
                              !product.inStock
                                ? '<div class="position-absolute top-50 start-50 translate-middle"><span class="badge bg-danger fs-6">缺貨</span></div>'
                                : ""
                            }
                        </div>
                        <div class="card-body p-3">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <small class="text-primary fw-bold">${
                                  product.siteName
                                }</small>
                                <span class="badge ${
                                  product.inStock ? "bg-success" : "bg-danger"
                                }">${product.inStock ? "有貨" : "缺貨"}</span>
                            </div>
                            <h6 class="card-title">${product.name}</h6>
                            <div class="price-section mb-3">
                                <div class="d-flex align-items-center">
                                    <span class="price-tag me-2">NT$ ${product.price.toLocaleString()}</span>
                                    ${
                                      product.originalPrice > product.price
                                        ? `<small class="text-muted text-decoration-line-through">NT$ ${product.originalPrice.toLocaleString()}</small>`
                                        : ""
                                    }
                                </div>
                            </div>
                            <div class="rating-section mb-3">
                                <div class="rating-stars">
                                    ${"★".repeat(
                                      Math.floor(product.rating)
                                    )}${"☆".repeat(
        5 - Math.floor(product.rating)
      )}
                                    <small class="text-muted ms-1">${
                                      product.rating
                                    } (${product.reviews})</small>
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

  resultsContainer.innerHTML = html;
}

// 按Enter搜尋
document
  .getElementById("searchInput")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      searchProducts();
    }
  });

// 示範搜尋建議
const searchSuggestions = [
  "iPhone 15",
  "MacBook Air",
  "AirPods Pro",
  "iPad Pro",
  "Nike 球鞋",
];
let currentSuggestion = 0;

function rotatePlaceholder() {
  const input = document.getElementById("searchInput");
  input.placeholder = `輸入商品名稱，例如：${searchSuggestions[currentSuggestion]}`;
  currentSuggestion = (currentSuggestion + 1) % searchSuggestions.length;
}

// 每3秒更換一次placeholder
setInterval(rotatePlaceholder, 3000);
