import '../css/global.css';
import '../css/syntax.css';
import { watchKeyboardEvents } from './navigation.js';
watchKeyboardEvents();

function navbarBold() {
  const currentPage = window.location.pathname;
  console.log(currentPage);
  for (const link of document.getElementsByClassName('nav-link')) {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  }
}
navbarBold();
