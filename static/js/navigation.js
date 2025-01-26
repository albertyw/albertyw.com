const keyHistory = [];

const navigationOptions = {
  'g': '/',
  'n': '/',
  's': '/shelf',
  'p': '/projects',
  'r': '/reference',
};
const navigationOptionsFlipped = Object.fromEntries(Object.entries(navigationOptions).map(a => a.reverse()))

function underlineText() {
  const links = document.querySelectorAll('.navbar a');
  for (let i = 0; i < links.length; i++) {
    const link = links[i];
    const href = link.getAttribute('href');
    const letter = navigationOptionsFlipped[href];
    let text = link.innerHTML;
    for (let j = 0; j < text.length; j++) {
      if (text[j].toLowerCase() === letter) {
        text = text.replace(text[j], '<u>' + text[j] + '</u>');
        break;
      }
    }
    link.innerHTML = text;
  }
}

function processKeyHistory() {
  if (keyHistory[0] !== 'g') {
    keyHistory.length = 0;
    return;
  }
  if (keyHistory.length < 2) {
    underlineText();
    return;
  }
  const action = keyHistory[1];
  keyHistory.length = 0;
  const navLocation = navigationOptions[action];
  if (navLocation !== undefined) {
    window.location.href = navLocation;
    return;
  }
}

export function watchKeyboardEvents() {
  window.addEventListener('keyup', (event) => {
    keyHistory.push(event.key);
    processKeyHistory();
  });
}
