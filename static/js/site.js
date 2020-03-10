function initSelect2 () {
  $('select:visible').select2({
    theme: 'bootstrap4'
  });
}

$(document).ready(function () {
  initSelect2();
});
