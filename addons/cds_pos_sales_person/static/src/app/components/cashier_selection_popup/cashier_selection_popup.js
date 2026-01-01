/** @odoo-module */

import { CashierSelectionPopup } from "@pos_hr/app/components/popups/cashier_selection_popup/cashier_selection_popup";
import { patch } from "@web/core/utils/patch";

patch(CashierSelectionPopup.prototype, {
    setup() {
        super.setup(...arguments);
        // Filter out employees with 'salesperson' role from the employees list
        this.filteredEmployees = this.props.employees.filter(
            (employee) => employee._role !== 'salesperson'
        );
    },
});
