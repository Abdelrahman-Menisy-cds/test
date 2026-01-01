/** @odoo-module **/

import {SearchModel} from "@web/search/search_model";
import {patch} from "@web/core/utils/patch";

/**
 * This is the conversion of ForecastModelExtension. See there for more
 * explanations of what is done here.
 *
 */

function isMultiSearch(str) {
    // Define a regular expression pattern to match the desired format
    const pattern = /^\{.*\}$/;
    // Test if the string matches the pattern
    return pattern.test(str);
}

patch(SearchModel.prototype, {
    addAutoCompletionValues(searchItemId, autocompleteValue) {
        // this._super(...arguments);
        const trimmed_string = autocompleteValue.value;
        var self = this
         const {label, value, operator} = autocompleteValue;

        if (isMultiSearch(trimmed_string)) {
            console.log('it is worked')
            const search_values = trimmed_string.slice(1, -1).split(" ");

            search_values.forEach(search_value => {
                console.log(search_value);
                const multi_autocompleteValue = {
                    label: search_value,
                    operator: operator,
                    value: search_value,
                }
                self.addAutoCompletionValues(searchItemId,multi_autocompleteValue);
            });

        }else {
            super.addAutoCompletionValues(...arguments);

        }

    }

});




