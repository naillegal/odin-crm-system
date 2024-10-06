document.addEventListener("DOMContentLoaded", function () {
  // Select the initial container and plus icon
  const onelineInputsContainer = document.querySelector(".onelineinputs");
  const plusIcon = document.querySelector(".icon-bg");

  // Function to create a new section
  function createNewSection() {
    // Clone the initial onelineinputs div
    const newSection = onelineInputsContainer.cloneNode(true);

    // Clear the inputs in the cloned section
    const inputs = newSection.querySelectorAll("input, select");
    inputs.forEach((input) => {
      if (input.tagName === "INPUT") {
        input.value = "";
      }
    });

    // Replace the plus icon with a trash icon in the cloned section
    const iconContainer = newSection.querySelector(".icon-bg");
    iconContainer.innerHTML = '<i class="fa-solid fa-trash"></i>';
    iconContainer.classList.add("trash-icon"); // Add a class for styling the trash icon

    // Add event listener to the trash icon to remove the section
    iconContainer.addEventListener("click", function () {
      newSection.remove();
    });

    // Insert the new section right after the existing .onelineinputs div
    onelineInputsContainer.parentNode.insertBefore(
      newSection,
      onelineInputsContainer.nextSibling
    );
  }

  // Add a click event listener to the plus icon for creating new sections
  plusIcon.addEventListener("click", function () {
    createNewSection();
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
