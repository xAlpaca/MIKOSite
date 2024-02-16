// Your JavaScript code for interactive elements here

// Example: Open/close dropdown menu
const dropdown = document.querySelector('.dropdown');
const dropdownButton = document.querySelector('.dropdown-button');
const dropdownContent = document.querySelector('.dropdown-content');

dropdownButton.addEventListener('click', function() {
  dropdownContent.classList.toggle('show');
});
