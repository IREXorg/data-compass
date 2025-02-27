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

function id_to_windowname(text) {
  text = text.replace(/\./g, '__dot__');
  text = text.replace(/\-/g, '__dash__');
  return text;
}

function windowname_to_id(text) {
  text = text.replace(/__dot__/g, '.');
  text = text.replace(/__dash__/g, '-');
  return text;
}

function showObjectPopup(triggeringLink, name_regexp, add_popup) {
  var name = triggeringLink.id.replace(name_regexp, '');
  name = id_to_windowname(name);

  var href = triggeringLink.href;
  if (add_popup) {
    if (href.indexOf('?') === -1) {
      href += '?_popup=1';
    } else {
      href += '&_popup=1';
    }
  }

  var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');

  win.focus();
  return false;
}

function showRelatedObjectPopup(triggeringLink) {
  return showObjectPopup(triggeringLink, /^(change|add|delete)_/, false);
}

function showRelatedObjectLookupPopup(triggeringLink) {
  return showObjectPopup(triggeringLink, /^lookup_/, true);
}

function dismissRelatedLookupPopup(win, chosenId) {
  var name = windowname_to_id(win.name);
  var elem = document.getElementById(name);
  if (elem.className.indexOf('m2m') !== -1 && elem.value) {
    elem.value += ',' + chosenId;
  } else {
    document.getElementById(name).value = chosenId;
  }
  win.close();
}

function updateRelatedObjectLinks(triggeringLink) {
  var $this = $(triggeringLink);
  var siblings = $this.nextAll('.view-related, .change-related, .delete-related');
  if (!siblings.length) {
    return;
  }
  var value = $this.val();
  if (value) {
    siblings.each(function() {
      var elm = $(this);
      elm.attr('href', elm.attr('data-href-template').replace('__fk__', value));
    });
  } else {
    siblings.removeAttr('href');
  }
}

function dismissAddRelatedObjectPopup(win, newId, newRepr) {
  var name = windowname_to_id(win.name);
  var elem = document.getElementById(name);
  if (elem) {
    var elemName = elem.nodeName.toUpperCase();
    if (elemName === 'SELECT') {
      elem.options[elem.options.length] = new Option(newRepr, newId, true, true);
    } else if (elemName === 'INPUT') {
      if (elem.className.indexOf('m2m') !== -1 && elem.value) {
        elem.value += ',' + newId;
      } else {
        elem.value = newId;
      }
    }
    // Trigger a change event to update related links if required.
    $(elem).trigger('change', [newRepr]);
  } else {
    var toId = name + "_to";
    var o = new Option(newRepr, newId);
    SelectBox.add_to_cache(toId, o);
    SelectBox.redisplay(toId);
  }
  win.close();
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

function dismissChangeObjectPopup(win) {
  win.opener.location.reload(true);
  win.close();
}


$(document).ready(function() {

  $("a[data-popup-opener]").on('click', function(event) {
    event.preventDefault();
    opener.dismissRelatedLookupPopup(window, $(this).data("popup-opener"));
  });

  $('body').on('click', '.related-widget-wrapper-link', function(e) {
    e.preventDefault();
    if (this.href) {
      var event = $.Event('related-objects:show', { href: this.href });
      $(this).trigger(event);
      if (!event.isDefaultPrevented()) {
        showRelatedObjectPopup(this);
      }
    }
  });

  $('body').on('change', '.related-widget-wrapper select', function(e) {
    var event = $.Event('related-objects:update');
    $(this).trigger(event);
    if (!event.isDefaultPrevented()) {
      updateRelatedObjectLinks(this);
    }
  });

  $('body').on('click', '.related-lookup', function(e) {
    e.preventDefault();
    var event = $.Event('related-objects:lookup');
    $(this).trigger(event);
    if (!event.isDefaultPrevented()) {
      showRelatedObjectLookupPopup(this);
    }
  });
})

/* eslint-enable */
