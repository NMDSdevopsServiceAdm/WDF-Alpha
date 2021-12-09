import '@babel/polyfill';
import { initAll } from 'govuk-frontend';
import List from 'list.js';

// IE11 polyfills
import foreachPolyfill from './polyfills/foreach-polyfill';
import closestPolyfill from './polyfills/closest-polyfill';

import '../sass/main.scss';

foreachPolyfill();
closestPolyfill();

// Worth us only initialising the specific components we use further down the line,
// but for the sake of speed in Alpha:
initAll();

window.ListJS = List;
