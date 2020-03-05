/*global opener */
(function() {
    'use strict';
    var initData = JSON.parse(document.getElementById('popup-response-constants').dataset.popupResponse);

    switch(initData.action) {
        case 'change':
            opener.dismissChangeRelatedObjectPopup(window, initData.value, initData.obj, initData.new_value);
            break;
        case 'change_object':
            opener.dismissChangeObjectPopup(window);
            break;
        case 'delete':
            opener.dismissDeleteRelatedObjectPopup(window, initData.value);
            break;
        case 'delete_object':
            opener.dismissChangeObjectPopup(window);
            break;
        default:
            opener.dismissAddRelatedObjectPopup(window, initData.value, initData.obj);
            break;
    }

    opener.$('body').trigger('related-objects:dismiss');


})();
