document.addEventListener("DOMContentLoaded", function () {
  const copyButtons = document.querySelectorAll(".copy-link-btn");

  copyButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      // Linki alırıq
      const link = this.getAttribute("data-link");

      // Kopyalamaq üçün bir temp input yaradılır
      const tempInput = document.createElement("input");
      document.body.appendChild(tempInput);
      tempInput.value = window.location.origin + link; // Saytın əsas URL-i + səhifənin linki
      tempInput.select();
      document.execCommand("copy");
      document.body.removeChild(tempInput);
    });
  });
});
