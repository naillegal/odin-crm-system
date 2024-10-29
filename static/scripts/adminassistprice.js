document.addEventListener("DOMContentLoaded", function () {
  const cloneWrapper = document.getElementById("clone-wrapper");

  // Textarea-nın hündürlüyünü avtomatik genişləndirmək üçün funksiya
  function enableTextareaAutoExpand(container) {
    const textareas = container.querySelectorAll(".auto-expand");
    textareas.forEach((textarea) => {
      textarea.addEventListener("input", function () {
        this.style.height = "auto"; // Reset height
        this.style.height = `${this.scrollHeight}px`; // Set new height
      });
    });
  }

  // Custom-select üçün event delegation ilə işləyən funksiya
  function initCustomSelect(container) {
    container.addEventListener("click", function (e) {
      const selectedOption = e.target.closest(".selected-option");
      const option = e.target.closest(".option");

      // Açılan menyunu idarə edir
      if (selectedOption) {
        const select = selectedOption.closest(".custom-select");
        select.classList.toggle("open");
      }

      // Seçim edildikdə custom-select-i yeniləyir
      if (option) {
        const select = option.closest(".custom-select");
        const hiddenInput = select.querySelector("input[type='hidden']");
        const selectedOption = select.querySelector(".selected-option");

        const value = option.getAttribute("data-value");
        const img = option.querySelector("img");
        const text = option.textContent.trim();

        hiddenInput.value = value;
        selectedOption.innerHTML = ""; // Reset selected content

        if (img) {
          const imgClone = img.cloneNode(true);
          selectedOption.appendChild(imgClone);
        }
        selectedOption.appendChild(document.createTextNode(" " + text));

        select.classList.remove("open");
      }
    });

    // Saytdan kənar klikləri izləyərək açıq menyunu bağlayır
    document.addEventListener("click", function (e) {
      if (!container.contains(e.target)) {
        container.querySelectorAll(".custom-select").forEach((select) => {
          select.classList.remove("open");
        });
      }
    });
  }

  // Yeni bir klonlanmış bölmə yaradır
  function createNewSection() {
    const originalClone = document.querySelector(".clone");
    const newSection = originalClone.cloneNode(true);

    // Bütün input və textarea-ları sıfırlayır
    newSection.querySelectorAll("input, select, textarea").forEach((input) => {
      if (input.type !== "hidden") input.value = "";
      if (input.tagName === "TEXTAREA") input.style.height = "auto"; // Reset height
    });

    // "+" işarəsini "sil" işarəsinə çevirir
    const icon = newSection.querySelector(".icon-bg i");
    icon.classList.remove("fa-plus");
    icon.classList.add("fa-trash");

    // Yeni bölməni formaya əlavə edir
    cloneWrapper.appendChild(newSection);

    // Yeni bölmə üçün funksiyaları işə salır
    enableTextareaAutoExpand(newSection);
  }

  // "+" və "sil" işarələrinə klikləri idarə edir
  cloneWrapper.addEventListener("click", function (event) {
    const icon = event.target.closest(".icon-bg i");
    if (icon) {
      if (icon.classList.contains("fa-plus")) {
        createNewSection();
      } else if (icon.classList.contains("fa-trash")) {
        icon.closest(".clone").remove();
      }
    }
  });

  // Məhsul seçiləndə açıqlamanı doldurur
  cloneWrapper.addEventListener("change", function (event) {
    if (event.target.classList.contains("product-select")) {
      const selectedOption = event.target.options[event.target.selectedIndex];
      const description = selectedOption.getAttribute("data-description") || "";

      const section = event.target.closest(".clone");
      const descriptionField = section.querySelector(".description");

      descriptionField.value = description;
      descriptionField.dispatchEvent(new Event("input"));
    }
  });

  // İlk bölmə üçün funksiyaları işə salır
  enableTextareaAutoExpand(document);
  initCustomSelect(cloneWrapper);
});
