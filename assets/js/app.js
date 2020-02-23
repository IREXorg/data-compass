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
} catch (e) {}

/**
 * We'll load jQuery plugins.
 */
require('autosize');
require('apexcharts');
require('flatpickr');
require('@fullcalendar/core');
require('@fullcalendar/daygrid');
require('@fullcalendar/interaction');
require('@fullcalendar/list');
require('@fullcalendar/timegrid');
require('imask');
require('jqvmap');
require('nouislider');
require('peity');
require('selectize');

/**
 * We'll load fontawesome.
 */
require('@fortawesome/fontawesome-free/js/fontawesome');
require('@fortawesome/fontawesome-free/js/solid');
require('@fortawesome/fontawesome-free/js/regular');
require('@fortawesome/fontawesome-free/js/brands');

/**
 * We'll load the theme's javascript.
 */
require('./theme/tabler.min');
