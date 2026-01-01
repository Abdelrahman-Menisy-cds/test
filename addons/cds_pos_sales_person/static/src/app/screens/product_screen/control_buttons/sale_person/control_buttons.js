/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { SelectionPopup } from "@point_of_sale/app/components/popups/selection_popup/selection_popup";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(ControlButtons.prototype, {
    get currentOrder() {
        return this.pos.getOrder();
    },
    
    get currentSalePersonName() {
        const order = this.currentOrder;
        return order && order.sale_person_id ? order.sale_person_id.name : _t("Sale Person");
    },
    
    async selectSalePerson() {
        // Create the list to be passed to the SelectionPopup.
        const selectionList = [];
        console.log(this.pos.config.sale_persons_ids);
        for (const sale_person of this.pos.config.sale_persons_ids) {
            selectionList.push({
                id: sale_person.id,
                label: sale_person.name,
                isSelected: this.currentOrder.sale_person_id === sale_person.id,
                item: sale_person,
            });
        }
        
        if (!this.pos.default_sale_person) {
            selectionList.push({
                id: null,
                label: _t("Default Sale Person"),
                isSelected: !this.currentOrder.sale_person_id,
                item: null,
            });
        }

        const selectedSalePerson = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select the Sale Person"),
            list: selectionList,
        });

        if (selectedSalePerson) {
            const order = this.pos.getOrder();
            // Store only primitive values to avoid circular references
            order.sale_person_id = selectedSalePerson.id;
            order.sale_person_name = selectedSalePerson.name;
            // assign sale person to all order lines if it's not already assigned
            for (const line of order.lines) {
                if (!line.sale_person_id) {
                    console.log('not assigned sale person to order line')
                    line.sale_person_id = selectedSalePerson.id;
                    line.sale_person_name = selectedSalePerson.name;
                }
            }
        }
    }
});
