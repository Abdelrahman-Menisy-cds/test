/** @odoo-module */

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    getHasRefundLines() {
        for (const line of this.getOrderlines()) {
            if (line.refunded_orderline_id) {
                return true;
            }
            if (line.refund_sale_order_id) {
                return true;
            }
        }
        return false;
    },
});

patch(PosOrderline.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        // this.refund_sale_order_id = this.refund_sale_order_id || options.refund_sale_order_id;
        // this.refund_sale_order_line_id = this.refund_sale_order_line_id || options.refund_sale_order_line_id;
        // this.refunded_sale_qty = this.refunded_sale_qty || options.refunded_sale_qty;
    },    
    get_sale_order() {
        if (this.refund_sale_order_id) {
            const value = {
                name: this.refund_sale_order_id.name,
                // details: this.down_payment_details || false,
            };

            return value;
        }
        return false;
    },
    /**
     * Set quantity based on the give sale order line.
     * @param {'sale.order.line'} saleOrderLine
     */
    setRefundQuantityFromSOL(saleOrderLine) {
        const refundableQty = saleOrderLine.qty_delivered - saleOrderLine.pos_refunded_qty;
        if (refundableQty <= 0) {
            // set quantity to 0
            this.setQuantity(0);
            return;
        }
        this.setQuantity(refundableQty);
    },
});
