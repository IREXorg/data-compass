/* eslint-disable */

$('.btn-export-csv').click(function() {
  var form = '#master-filter';
  var tmpInputId = '_tmp-input';

  $("<input />")
    .attr("type", "hidden")
    .attr("name", "format")
    .attr("value", "csv")
    .attr("id", tmpInputId)
    .appendTo(form);

  $(form).submit();
  $('#' + tmpInputId).remove();

});

/* eslint-enable */
