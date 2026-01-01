/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate = false) {
        var order = this.currentOrder;
        var old_order_total = order.priceExcl;
        const rewardLines = order._get_reward_lines();
        if (rewardLines.length > 0) {
            var total_reward_discount = 0;
            for (let line of rewardLines) {
                total_reward_discount += Math.abs(line.priceExcl);
                if (total_reward_discount > 0) {
                    order.removeOrderline(line);
                }
            }
            var order_total = order.priceExcl;
            if (total_reward_discount > 0) {
                const discount_percentage = total_reward_discount / order_total;
                for (let line of order.getOrderlines()) {

                    if (line.discount > 0) {

                        var total_before_discount = line.price_unit * line.qty;
                        var total_second_discount = line.priceIncl * (discount_percentage)
                        var second_discount_precentage = total_second_discount / total_before_discount;
                        line.discount = line.discount + (second_discount_precentage * 100);
                    } else {
                        line.setDiscount(discount_percentage * 100);
                    }
                }
            }
            var new_order_total = order.priceExcl;
            console.log("new_order_total", new_order_total);

            var difference = old_order_total - new_order_total;
            console.log("difference", difference);
            //            difference = Math.abs(difference);
            //            console.log("difference", difference);
            if (difference < 0) {
                difference = Math.abs(difference);
                for (let line of order.getOrderlines()) {
                    if (line) {
                        const unit_price = line.price_unit;
                        const quantity = line.getQuantity();
                        const line_total = unit_price * quantity;
                        const discount_amount = Math.ceil((difference + Number.EPSILON) * 100) / 100;
                        const discount_percent = (discount_amount / line_total) * 100;
                        console.log(discount_percent, "discount_percent");
                        const current_discount = line.getDiscount();
                        line.setDiscount(current_discount + discount_percent);
                        break;
                    }

                }
            } else if (difference > 0) {
                difference = Math.abs(difference);
                for (let line of order.getOrderlines()) {
                    if (line) {
                        const unit_price = line.price_unit;
                        const quantity = line.getQuantity();
                        const line_total = unit_price * quantity;
                        const discount_amount = Math.ceil((difference + Number.EPSILON) * 100) / 100;
                        const discount_percent = (discount_amount / line_total) * 100;
                        const current_discount = line.getDiscount();
                        line.setDiscount(current_discount - discount_percent);
                        break;
                    }

                }


            }

            console.log(order.priceExcl, "AAAAAAAAAAAA");

        }
        await super.validateOrder(isForceValidate)
    },

});
