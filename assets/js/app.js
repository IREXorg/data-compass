/* eslint-disable */

window._ = require('lodash');

/**
 * We'll load jQuery and the Bootstrap jQuery plugin which provides support
 * for JavaScript based Bootstrap features such as modals and tabs. This
 * code may be modified to fit the specific needs of your application.
 * Include the Popper.js library, since Boostrap 4 requires it.
 */

window.Popper = require('popper.js').default;

require('bootstrap');

var select2 = require('select2');

require('./related-objects.js');
require('./popup-response.js');
require('./export-utils.js');


// initialize once dom ready
$(document).ready(function() {

  // wire boostrap tooltip
  $('[data-toggle="tooltip"]').tooltip();

  // wire boostrap popover
  $('[data-toggle="popover"]').popover();

  // wire boostrap dropdown
  $('.dropdown-toggle').dropdown();

  // wire select2
  // select2(window.$);
  $("select:visible[name='country']").select2({theme: 'bootstrap4'});

  // Alerts
  $(".alert").fadeTo(2000, 500).slideUp(500, function(){
      $(".alert").slideUp(500);
  });
});


