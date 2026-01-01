/** @odoo-module */

// import { patch } from "@web/core/utils/patch";
// // import { Order } from "@point_of_sale/app/store/models";
// import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
// // import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
// import { _t } from "@web/core/l10n/translation";

// patch(PosOrderline.prototype, {

//     setup() {
//         super.setup(...arguments);
//     },
//     set_discount_pricelist(discount_pricelist_id) {
//         this.discount_pricelist_id = discount_pricelist_id;
//     },
//     init_from_JSON(json) {
//         super.init_from_JSON(...arguments);
//         this.discount_pricelist_id = json.discount_pricelist_id;
//     },

//     export_as_JSON() {
//         const json = super.export_as_JSON(...arguments);
//         json.discount_pricelist_id = this.discount_pricelist_id ? this.discount_pricelist_id.id : false;
//         return json;
//     },
// });
