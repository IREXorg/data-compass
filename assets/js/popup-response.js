/* eslint-disable */

function interpolate(fmt, obj, named) {
  if (named) {
    return fmt.replace(/%\(\w+\)s/g, function(match) {
      return String(obj[match.slice(2, -2)]);
    });
  } else {
    return fmt.replace(/%s/g, function(match) {
      return String(obj.shift());
    });
  }
}

function windowname_to_id(text) {
  text = text.replace(/__dot__/g, '.');
  text = text.replace(/__dash__/g, '-');
  return text;
}

function dismissChangeRelatedObjectPopup(win, objId, newRepr, newId) {
  var id = windowname_to_id(win.name).replace(/^edit_/, '');
  var selectsSelector = `#${id}, #${id}_from, #${id}_to`;
  var selects = $(selectsSelector);
  selects.find('option').each(function() {
    if (this.value === objId) {
      this.textContent = newRepr;
      this.value = newId;
    }
  });
  selects.next().find('.select2-selection__rendered').each(function(i) {
    if (this.nodeName === 'UL') {
      // TODO: Multi select
    } else {
      // The element can have a clear button as a child.
      // Use the lastChild to modify only the displayed value.
      this.lastChild.textContent = newRepr;
      this.title = newRepr;
    }
  });
  win.close();
}

function dismissChangeObjectPopup(win) {
  location.reload(true);
  win.close();
}

function dismissDeleteRelatedObjectPopup(win, objId) {
  var id = windowname_to_id(win.name).replace(/^delete_/, '');
  var selectsSelector = interpolate('#%s, #%s_from, #%s_to', [id, id, id]);
  var selects = $(selectsSelector);
  selects.find('option').each(function() {
    if (this.value === objId) {
      $(this).remove();
    }
  }).trigger('change');
  win.close();
}

/*global opener */
$(document).ready(function() {

  var response = document.getElementById('popup-response-constants');

  if (response) {
    var initData = JSON.parse(response.dataset.popupResponse);

    switch (initData.action) {
      case 'change':
        dismissChangeRelatedObjectPopup(window, initData.value, initData.obj, initData.new_value);
        break;
      case 'change_object':
        dismissChangeObjectPopup(window);
        break;
      case 'delete':
        dismissDeleteRelatedObjectPopup(window, initData.value);
        break;
      case 'delete_object':
        dismissChangeObjectPopup(window);
        break;
      default:
        dismissAddRelatedObjectPopup(window, initData.value, initData.obj);
        break;
    }

    opener.$('body').trigger('related-objects:dismiss');
  }
});

/* eslint-enable */
