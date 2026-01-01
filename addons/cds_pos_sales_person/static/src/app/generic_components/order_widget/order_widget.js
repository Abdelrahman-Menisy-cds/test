/** @odoo-module **/

import { OrderDisplay } from "@point_of_sale/app/components/order_display/order_display";
import { patch } from "@web/core/utils/patch";

// No need to patch props since order is defined as Object which accepts any keys
// The sale_person_name will be accessible via props.order.sale_person_name

// If you need to add custom methods to OrderDisplay, you can patch the prototype:
// patch(OrderDisplay.prototype, {
//     // your custom methods here
// });

