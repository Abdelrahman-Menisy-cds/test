/** @odoo-module */

import { PosStore } from "@point_of_sale/app/services/pos_store";
import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(PosStore.prototype, {
    async pay(){

        // check if the sale person is set
        if (!this.getOrder().sale_person_id) {
            this.env.services.dialog.add(AlertDialog, {
                title: _t("Error"),
                body: _t("Please select a sale person before paying the order."),
            });
            return;
        }
        super.pay(...arguments)
    },

    async selectSalePerson() {
        // Create the list to be passed to the SelectionPopup.
        const selectionList = [];
        for (const sale_person of this.config.sale_persons_ids) {
            const order = this.getOrder();
            selectionList.push({
                id: sale_person.id,
                label: sale_person.name,
                isSelected: order.sale_person_id === sale_person.id,
                item: sale_person,
            });
        }
        
        if (!this.default_sale_person) {
            selectionList.push({
                id: null,
                label: _t("Default Sale Person"),
                isSelected: !this.getOrder().sale_person_id,
                item: null,
            });
        }

        const selectedSalePerson = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select the Sale Person"),
            list: selectionList,
        });

        if (selectedSalePerson) {
            const order = this.getOrder();
            // Store only primitive values to avoid circular references
            order.sale_person_id = selectedSalePerson.id;
            order.sale_person_name = selectedSalePerson.name;
            // assign sale person to all order lines if it's not already assigned
            for (const line of order.lines) {
                if (!line.sale_person_id) {
                    line.sale_person_id = selectedSalePerson.id;
                    line.sale_person_name = selectedSalePerson.name;
                }
            }
        }
    },
    
    async addLineToCurrentOrder(vals, opts = {}, configure = true) {
        const line = await super.addLineToCurrentOrder(vals, opts, configure);
        
        // Check if the order lines length is 1 or less after adding the product
        const order = this.getOrder();
        // check if the order is not a refund sale order
        if (order && order.lines.length <= 1 && !order.sale_person_id && order.lines.filter((line) => line.refund_sale_order_id).length === 0) {
            await this.selectSalePerson();
        }
        
        return line;
    }
});