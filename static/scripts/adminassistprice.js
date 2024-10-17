document.addEventListener("DOMContentLoaded", function () {
  const cloneWrapper = document.getElementById("clone-wrapper");

  function createNewSection() {
      const originalClone = document.querySelector(".clone");
      const newSection = originalClone.cloneNode(true);

      const inputs = newSection.querySelectorAll("input, select, textarea");
      inputs.forEach((input) => (input.value = ""));

      const iconContainer = newSection.querySelector(".icon-bg i");
      iconContainer.classList.remove("fa-plus");
      iconContainer.classList.add("fa-trash");

      iconContainer.addEventListener("click", function () {
          newSection.remove();
      });

      cloneWrapper.appendChild(newSection);
  }

  cloneWrapper.addEventListener("click", function (event) {
      const icon = event.target.closest(".icon-bg i");
      if (icon && icon.classList.contains("fa-plus")) {
          createNewSection();
      } else if (icon && icon.classList.contains("fa-trash")) {
          icon.closest(".clone").remove();
      }
  });
});
