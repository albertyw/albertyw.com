const keyHistory = [];

const navigationOptions = {};
const navigationOptionsText = {};
function generateNavigationOptions() {
  const links = document.querySelectorAll('.navbar a');
  for (let i = 0; i < links.length; i++) {
    const link = links[i];
    const href = link.getAttribute('href');
    const text = link.innerHTML;
    const letter = findUnusedLetter(text, Object.keys(navigationOptions));
    if (letter === undefined) {
      continue;
    }
    navigationOptions[letter] = href;
    navigationOptionsText[text] = letter;
  }
}
function findUnusedLetter(text, usedLetters) {
  for (let i = 0; i < text.length; i++) {
    const letter = text[i].toLowerCase();
    if (!usedLetters.includes(letter)) {
      return letter;
    }
  }
  return undefined;
}

function underlineText() {
  const links = document.querySelectorAll('.navbar a');
  for (let i = 0; i < links.length; i++) {
    const link = links[i];
    const letter = navigationOptionsText[link.innerHTML];
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
  generateNavigationOptions();
  window.addEventListener('keyup', (event) => {
    keyHistory.push(event.key);
    processKeyHistory();
  });
}

export function navbarBold() {
  const currentPage = window.location.pathname;
  for (const link of document.getElementsByClassName('nav-link')) {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  }
}

// Keyboard navigation for .selectable-list using "j" and "k"
export function setupSelectableListNavigation() {
  const list = document.querySelector('.selectable-list');
  if (!list) return;
  const items = Array.from(list.querySelectorAll('li'));
  if (items.length === 0) return;

  let selectedIdx: number | null = null;

  function updateSelection(newIdx: number | null) {
    items.forEach((item, idx) => {
      if (idx === newIdx) {
        item.classList.add('selected');
      } else {
        item.classList.remove('selected');
      }
    });
    selectedIdx = newIdx;
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.target && (event.target as HTMLElement).tagName === 'INPUT') return;
    if (event.target && (event.target as HTMLElement).tagName === 'TEXTAREA') return;
    if (event.key === 'j') {
      if (selectedIdx === null) {
        updateSelection(0);
      } else if (selectedIdx < items.length - 1) {
        updateSelection(selectedIdx + 1);
      }
      event.preventDefault();
    } else if (event.key === 'k') {
      if (selectedIdx === null) {
        updateSelection(items.length - 1);
      } else if (selectedIdx > 0) {
        updateSelection(selectedIdx - 1);
      }
      event.preventDefault();
    } else if ((event.key === 'Enter' || event.key === 'o') && selectedIdx !== null) {
      const selectedItem = items[selectedIdx];
      const link = selectedItem.querySelector('a');
      if (link && link instanceof HTMLAnchorElement) {
        window.location.href = link.href;
        event.preventDefault();
      }
    }
  
  }
  // Ensure no item is selected initially
  updateSelection(null);

  window.addEventListener('keydown', handleKeydown);
}