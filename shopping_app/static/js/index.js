// static/js/index.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("add-store-form");
  const input = document.getElementById("store-input");
  const badges = document.getElementById("selected-stores");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const store = input.value.trim();
    if (
      store &&
      !Array.from(badges.children).some((b) => b.textContent === store)
    ) {
      const badge = document.createElement("span");
      badge.className = "store-badge";
      badge.textContent = store;
      // 點擊可移除
      badge.onclick = () => badge.remove();
      badges.appendChild(badge);
      input.value = "";
    }
  });
});
