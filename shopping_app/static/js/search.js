// static/js/search.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("search-form");
  const input = document.getElementById("product-input");
  const results = document.getElementById("search-results");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const query = input.value.trim();
    if (query) {
      // 假資料，未來可串Django API
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
      results.innerHTML = "";
      sampleResults.forEach((item) => {
        results.innerHTML += `
                    <div class="result-card">
                        <img src="${item.img}" alt="${item.name}">
                        <div class="product-name">${item.name}</div>
                        <div class="price">${item.price}</div>
                        <div class="store">${item.store}</div>
                    </div>
                `;
      });
    }
  });
});
