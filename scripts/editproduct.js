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
