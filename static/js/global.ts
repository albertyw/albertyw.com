import '../css/global.css';
import '../css/syntax.css';
import { navbarBold, watchKeyboardEvents, setupSelectableListNavigation } from './navigation.js';

navbarBold();
watchKeyboardEvents();
setupSelectableListNavigation();

import { main } from './pid.js';
main();