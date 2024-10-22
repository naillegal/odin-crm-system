document.addEventListener("DOMContentLoaded", function () {
    const cloneWrapper = document.getElementById("clone-wrapper");

    // Yeni bölmə yaratmaq funksiyası
    function createNewSection() {
        const originalClone = document.querySelector(".clone");
        const newSection = originalClone.cloneNode(true);

        // Bütün input, select və textarea-ları təmizləyirik
        const inputs = newSection.querySelectorAll("input, select, textarea");
        inputs.forEach((input) => {
            input.value = "";
            if (input.tagName === "TEXTAREA") {
                input.style.height = "auto"; // Textarea-nın hündürlüyünü sıfırlayırıq
            }
        });

        // "+" işarəsini "sil" işarəsinə dəyişirik
        const iconContainer = newSection.querySelector(".icon-bg i");
        iconContainer.classList.remove("fa-plus");
        iconContainer.classList.add("fa-trash");

        // Yeni bölməni silmək üçün event listener əlavə edirik
        iconContainer.addEventListener("click", function () {
            newSection.remove();
        });

        // Yeni bölməni formaya əlavə edirik
        cloneWrapper.appendChild(newSection);
    }

    // Məhsul seçiləndə açıqlamanı textarea-ya dolduran event delegation
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

    // Textarea məzmununa uyğun genişlənmə funksiyası
    function enableTextareaAutoExpand(textareas) {
        textareas.forEach((textarea) => {
            textarea.addEventListener("input", function () {
                this.style.height = "auto"; // Hündürlüyü sıfırlayırıq
                this.style.height = `${this.scrollHeight}px`; // Yeni hündürlüyü təyin edirik
            });
        });
    }

    // İlk bölməyə textarea genişlənməsi funksiyasını tətbiq edirik
    enableTextareaAutoExpand(document.querySelectorAll(".auto-expand"));

    // "+" və ya "sil" işarəsinə klik olunduqda işləyir
    cloneWrapper.addEventListener("click", function (event) {
        const icon = event.target.closest(".icon-bg i");
        if (icon && icon.classList.contains("fa-plus")) {
            createNewSection();
        } else if (icon && icon.classList.contains("fa-trash")) {
            icon.closest(".clone").remove();
        }
    });
});
