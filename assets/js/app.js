/* eslint-disable */

window._ = require('lodash');

/**
 * We'll load jQuery and the Bootstrap jQuery plugin which provides support
 * for JavaScript based Bootstrap features such as modals and tabs. This
 * code may be modified to fit the specific needs of your application.
 * Include the Popper.js library, since Boostrap 4 requires it.
 */
try {
  window.$ = window.jQuery = require('jquery');

  window.Popper = require('popper.js').default;

  require('bootstrap');

  //require('./related-objects.js');
  //require('./popup-response.js');

  require('select2')(window.$);
} catch (e) {}

/**
 * We'll load the theme's javascript.
 */

/** FIXME: It seems tabler js also includes bootstrap's js. Therefore we have to choose one
 * require('./theme/tabler.min');
*/
