// customer drop down menu
$(document).ready(function () {
  let autoOpened = false; // Dropdown-un avtomatik açılmasını izləyən dəyişən

  // URL parametrlərindən customer_id və open parametrlərini əldə edirik
  const urlParams = new URLSearchParams(window.location.search);
  const customerId = urlParams.get("customer_id");
  const openDropdown = urlParams.get("open") === "dropdown";

  // Müvafiq müştərinin dropdown-feedback sahəsini avtomatik açırıq
  if (customerId && openDropdown) {
      $(`#dropdown-feedback-${customerId}`).slideDown(300);
      autoOpened = true; // Avtomatik açıldığını qeyd edirik
  }

  // Mövcud dropdown toggle məntiqi
  $(".clicktodown").on("click", function (event) {
      event.stopImmediatePropagation(); // Birdən çox tıklamanın qarşısını alır

      const box = $(this).closest(".box");
      const customerId = box.data("customer-id");
      const dropdown = $(`#dropdown-feedback-${customerId}`);

      // Əgər avtomatik açılıbsa və ilk dəfə klik edilirsə, bağlayırıq
      if (autoOpened) {
          autoOpened = false; // Avtomatik açılma vəziyyətini sıfırlayırıq
          dropdown.slideUp(300); // Dropdown-u bağlayırıq
          return; // Daha irəli getmirik
      }

      // Mövcud dropdown-u açır və ya bağlayır
      if (dropdown.is(":visible")) {
          dropdown.slideUp(300); // Açıqdırsa bağlayırıq
      } else {
          dropdown.slideDown(300); // Bağlıdırsa açırıq
      }

      // Digər bütün dropdown-ları bağlayırıq
      $(".dropdown-feedback").not(dropdown).slideUp(300);
  });

  // Mövcud clicktodowncrud funksionallığı
  $(".clicktodowncrud").on("click", function () {
      $(this).next("#dropdown-crud").slideToggle(300);
      $(".clicktodowncrud").not(this).each(function () {
          $(this).next("#dropdown-crud").slideUp(300);
      });
  });

  // Feed və Info tablarını dəyişmək üçün məntiq
  $(".box").each(function () {
      const box = $(this);
      const feedButton = box.find(".feed");
      const infoButton = box.find(".info");
      const feedTab = box.find(".tab1");
      const infoTab = box.find(".tab2");

      // İlkin vəziyyət: Feed tabı açıq, Info tabı bağlı
      feedTab.show();
      infoTab.hide();
      feedButton.addClass("active");

      // Feed tabına klik edildikdə
      feedButton.on("click", function () {
          feedTab.show();
          infoTab.hide();
          feedButton.addClass("active");
          infoButton.removeClass("active");
      });

      // Info tabına klik edildikdə
      infoButton.on("click", function () {
          feedTab.hide();
          infoTab.show();
          infoButton.addClass("active");
          feedButton.removeClass("active");
      });
  });
});

  
  // footer change active
  document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL path (excluding domain)
    const currentPath = window.location.pathname;
  
    // Select all the tab elements
    const tabs = document.querySelectorAll(".tabs-box .tab");
  
    // Remove the 'active' class from all tabs
    tabs.forEach((tab) => tab.classList.remove("active"));
  
    // Determine which tab should be active based on the current URL
    if (currentPath.includes("task.html")) {
      document.querySelector('a[href="task.html"] .tab').classList.add("active");
    } else if (currentPath.includes("assistprice.html")) {
      document
        .querySelector('a[href="assistprice.html"] .tab')
        .classList.add("active");
    } else if (currentPath.includes("salescontract.html")) {
      document
        .querySelector('a[href="salescontract.html"] .tab')
        .classList.add("active");
    }
  });
  
  // task.html click to BAX functionality
  $(document).ready(function () {
    let autoOpened = false; // Variable to track if dropdown was auto-opened
  
    // Detect if the URL has the query parameter to open the dropdown
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("open") === "dropdown") {
      // Automatically open the dropdown when the parameter is present
      $("#dropdown-feedback").slideDown(300);
      autoOpened = true; // Set autoOpened to true
    }
  
    // Existing drop down toggle logic
    $(".clicktodown").on("click", function (event) {
      event.stopImmediatePropagation(); // Prevent multiple rapid triggers
  
      // If the dropdown is auto-opened and we're clicking for the first time, close it
      if (autoOpened) {
        autoOpened = false; // Reset the autoOpened state
        $("#dropdown-feedback").slideUp(300); // Close the dropdown if it's open
        return; // Stop further processing
      }
  
      // If the dropdown is manually toggled, toggle the dropdown behavior
      const feedbackDropdown = $(this).next("#dropdown-feedback");
  
      if (feedbackDropdown.is(":visible")) {
        feedbackDropdown.slideUp(300); // If it's open, close it
      } else {
        feedbackDropdown.slideDown(300); // If it's closed, open it
      }
  
      // Close other dropdowns that are not this one
      $(".clicktodown")
        .not(this)
        .each(function () {
          $(this).next("#dropdown-feedback").slideUp(300);
        });
    });
  });
  

// all phone inputs start with +994
document.addEventListener('DOMContentLoaded', function () {
    // Select all input elements of type phone
    const phoneInputs = document.querySelectorAll('input[type="phone"]');
  
    // Function to add +994 and prevent it from being removed
    phoneInputs.forEach(input => {
      // Add +994 to the input if it's empty or doesn't already have it
      if (!input.value.startsWith('+994')) {
        input.value = '+994';
      }
  
      // Prevent +994 from being deleted
      input.addEventListener('input', function (event) {
        if (!input.value.startsWith('+994')) {
          input.value = '+994'; // Re-add +994 if the user tries to remove it
        }
      });
  
      // Prevent cursor from going before +994
      input.addEventListener('keydown', function (event) {
        if (input.selectionStart < 4 && event.key !== 'Tab' && event.key !== 'Shift') {
          event.preventDefault(); // Prevent moving cursor before +994
        }
      });
    });
  });
  