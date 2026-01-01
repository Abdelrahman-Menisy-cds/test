/** @odoo-module */
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { toRaw } from "@odoo/owl";

patch(PosOrder.prototype, {
    setup() {
        super.setup(...arguments);
    },
    
//    serialize() {
//        const json = super.serialize(...arguments);
//        // Handle both object and primitive values safely
//        if (this.sale_person_id) {
//            // Use toRaw to unwrap any proxy objects before serialization
//            json.sale_person_id = toRaw(this.sale_person_id);
//            json.sale_person_name =this.sale_person_name || '';
//        }
//        return json;
//    },

    /**
     * @override
     */
//    export_for_printing() {
//        const result = super.export_for_printing(...arguments);
//        result.sale_person_name = this.sale_person_name;
//        return result;
//    },
    
});
