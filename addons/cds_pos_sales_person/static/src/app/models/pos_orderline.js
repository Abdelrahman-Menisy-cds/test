/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { _t } from "@web/core/l10n/translation";
import { toRaw } from "@odoo/owl";

patch(PosOrderline.prototype, {
    
    setup() {
        super.setup(...arguments);
        if(this.sale_person_id){
            this.sale_person_id = this.sale_person_id;
            this.sale_person_name = this.sale_person_name;
        }
        else{
            this.sale_person_id = this.order_id?.sale_person_id;
            this.sale_person_name = this.order_id?.sale_person_name;
        }
    },

    /**
     * @override
     */
    getDisplayData() {
        // this.get_salesperson()
        return {
            ...super.getDisplayData(),
            sale_person_id: this.sale_person_id ? Number(this.sale_person_id) : null,
            sale_person_name: this.sale_person_name || "",
        };
    },
    
    /**
     * @override
     */
    serialize() {
        const json = super.serialize(...arguments);
        if (this.sale_person_id) {
            // Convert to primitive value to avoid Proxy serialization issues
            json.sale_person_id = Number(this.sale_person_id);
        }
        return json;
    },
});
