document.addEventListener("DOMContentLoaded", function () {
  const cloneWrapper = document.getElementById("clone-wrapper");
  let productCount = 1; // Məhsul sayını izləyirik

  function createNewSection() {
    const originalClone = document.querySelector(".clone");
    const newSection = originalClone.cloneNode(true);

    const inputs = newSection.querySelectorAll("input, select");
    inputs.forEach((input) => {
      input.value = ""; // Input və select-ləri boşaldırıq
    });

    // Yeni məhsul üçün features[] input adını dəyişirik
    const featureSelect = newSection.querySelector('select[name^="features"]');
    if (featureSelect) {
      featureSelect.name = `features_${productCount}[]`;
    }

    const iconContainer = newSection.querySelector(".icon-bg i");
    iconContainer.classList.remove("fa-plus");
    iconContainer.classList.add("fa-trash");

    cloneWrapper.appendChild(newSection);
    productCount++; // Məhsul sayını artırırıq
  }

  // `.icon-bg` div-ə kliklə yeni bölmə yaratmaq və ya silmək
  cloneWrapper.addEventListener("click", function (event) {
    const iconBg = event.target.closest(".icon-bg");

    if (iconBg) {
      const icon = iconBg.querySelector("i");

      if (icon && icon.classList.contains("fa-plus")) {
        // Yeni bölmə yaratmaq
        createNewSection();
      } else if (icon && icon.classList.contains("fa-trash")) {
        // Bölməni silmək
        iconBg.closest(".clone").remove();
      }
    }
  });
});






// all phone inputs start with +994
document.addEventListener("DOMContentLoaded", function () {
  // Select all input elements of type phone
  const phoneInputs = document.querySelectorAll('input[type="phone"]');

  // Function to add +994 and prevent it from being removed
  phoneInputs.forEach((input) => {
    // Add +994 to the input if it's empty or doesn't already have it
    if (!input.value.startsWith("+994")) {
      input.value = "+994";
    }

    // Prevent +994 from being deleted
    input.addEventListener("input", function (event) {
      if (!input.value.startsWith("+994")) {
        input.value = "+994"; // Re-add +994 if the user tries to remove it
      }
    });

    // Prevent cursor from going before +994
    input.addEventListener("keydown", function (event) {
      if (
        input.selectionStart < 4 &&
        event.key !== "Tab" &&
        event.key !== "Shift"
      ) {
        event.preventDefault(); // Prevent moving cursor before +994
      }
    });
  });
});

