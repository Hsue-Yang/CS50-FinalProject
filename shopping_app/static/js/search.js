const sampleResults = [
  {
    name: "Apple AirPods Pro",
    price: "$199",
    store: "Amazon",
    img: "https://via.placeholder.com/120?text=AirPods",
  },
  {
    name: "Apple AirPods Pro",
    price: "$210",
    store: "BestBuy",
    img: "https://via.placeholder.com/120?text=AirPods",
  },
  {
    name: "Apple AirPods Pro",
    price: "$205",
    store: "Momo",
    img: "https://via.placeholder.com/120?text=AirPods",
  },
];

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const suggestionsDiv = document.getElementById("searchSuggestions");
  const loadingSpinner = document.getElementById("loadingSpinner");

  // 搜尋建議功能
  let searchTimeout;
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout);
      const query = this.value.trim();

      if (query.length >= 2) {
        searchTimeout = setTimeout(() => {
          fetch(`/ajax/search/?q=${encodeURIComponent(query)}`)
            .then((response) => response.json())
            .then((data) => {
              showSuggestions(data.suggestions);
            })
            .catch((error) => console.error("Error:", error));
        }, 300);
      } else {
        hideSuggestions();
      }
    });
  }

  function showSuggestions(suggestions) {
    if (!suggestions || suggestions.length === 0) {
      hideSuggestions();
      return;
    }

    suggestionsDiv.innerHTML = "";
    suggestions.forEach((suggestion) => {
      const item = document.createElement("div");
      item.className = "suggestion-item";
      item.innerHTML = `<i class="fas fa-search me-2 text-muted"></i>${suggestion}`;
      item.addEventListener("click", () => {
        searchInput.value = suggestion;
        hideSuggestions();
      });
      suggestionsDiv.appendChild(item);
    });
    suggestionsDiv.style.display = "block";
  }

  function hideSuggestions() {
    if (suggestionsDiv) {
      suggestionsDiv.style.display = "none";
    }
  }

  // 點擊其他地方隱藏建議
  document.addEventListener("click", function (e) {
    if (
      searchInput &&
      !searchInput.contains(e.target) &&
      suggestionsDiv &&
      !suggestionsDiv.contains(e.target)
    ) {
      hideSuggestions();
    }
  });

  // 表單提交時顯示載入動畫
  const searchForms = document.querySelectorAll('form[action*="search"]');
  searchForms.forEach((form) => {
    form.addEventListener("submit", function () {
      if (loadingSpinner) {
        loadingSpinner.style.display = "block";
      }
    });
  });

  // 商品卡片hover效果
  const productCards = document.querySelectorAll(".product-card");
  productCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-5px)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });
});
