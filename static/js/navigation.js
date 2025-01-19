const keyHistory = [];

const navigationOptions = {
  'g': '/',
  'n': '/',
  's': '/shelf',
  'p': '/projects',
  'r': '/reference',
};

function processKeyHistory() {
  if (keyHistory[0] !== 'g') {
    keyHistory.length = 0;
    return;
  }
  if (keyHistory.length < 2) {
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
