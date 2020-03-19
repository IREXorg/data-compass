/* eslint-disable */

function exportFilteredCSV(el) {
  var form = '#master-filter';
  var tmpInputClass = '_tmp-input';
  var exportType = $(el).data('exportType');
  console.log(exportType);

  $("<input />")
    .attr("type", "hidden")
    .attr("name", "format")
    .attr("value", "csv")
    .addClass(tmpInputClass)
    .appendTo(form);

  if (exportType) {
    $("<input />")
      .attr("type", "hidden")
      .attr("name", "export_type")
      .attr("value", exportType)
      .addClass(tmpInputClass)
      .appendTo(form);
  }

  $(form).submit();
  $('.' + tmpInputClass).remove();
}


$('.action-export-csv').click(function() {
  exportFilteredCSV(this);
});

/* eslint-enable */
