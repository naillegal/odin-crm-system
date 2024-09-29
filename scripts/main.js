// change tabs 
document.addEventListener("DOMContentLoaded", function () {
  const feedTab = document.querySelector(".tab1");
  const infoTab = document.querySelector(".tab2");
  const feedButton = document.querySelector(".feed");
  const infoButton = document.querySelector(".info");

  feedTab.style.display = "block";
  infoTab.style.display = "none";
  feedButton.classList.add("active");

  feedButton.addEventListener("click", function () {
    feedTab.style.display = "block"; 
    infoTab.style.display = "none"; 
    feedButton.classList.add("active"); 
    infoButton.classList.remove("active"); 
  });

  infoButton.addEventListener("click", function () {
    feedTab.style.display = "none"; 
    infoTab.style.display = "block"; 
    infoButton.classList.add("active"); 
    feedButton.classList.remove("active"); 
  });
});


// charCount for textarea 
const textarea = document.getElementById('note');
const charCount = document.getElementById('char-count');
const maxChars = 150;

textarea.addEventListener('input', () => {
  const currentLength = textarea.value.length;
  charCount.textContent = `${currentLength} / ${maxChars}`;
});