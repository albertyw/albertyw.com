import '../css/global.css';
import '../css/syntax.css';
import { navbarBold, watchKeyboardEvents } from './navigation.js';

navbarBold();
watchKeyboardEvents();

import { main } from './pid.js';
main();