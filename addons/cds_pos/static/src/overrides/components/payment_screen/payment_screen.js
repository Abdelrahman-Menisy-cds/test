// Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
//
// Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
// It is forbidden to publish, distribute, sublicense, or sell copies
//
// of the Software or modified copies of the Software.

/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    onMounted() {
        // Check if this is a refund BEFORE calling super (which may add default payment line)
        const isRefundOrder = this.currentOrder?.isRefund;

        // Get original order - try refunded_order_id first, then fallback to first line's refunded_orderline_id
        const originalOrder = this.currentOrder?.refunded_order_id ||
            this.currentOrder?.lines[0]?.refunded_orderline_id?.order_id;

        // Store original payments info for multi-payment refund
        let originalPayments = [];
        let originalTotalPaid = 0;

        if (isRefundOrder && originalOrder?.payment_ids?.length > 0) {
            // Collect all original payments
            for (const payment of originalOrder.payment_ids) {
                const paymentMethod = payment.payment_method_id;
                const amount = payment.amount || 0;
                if (paymentMethod && amount > 0) {
                    originalPayments.push({
                        method: paymentMethod,
                        amount: amount
                    });
                    originalTotalPaid += amount;
                }
            }
        }

        super.onMounted(...arguments);

        // Auto-select original payment methods for refund orders with multi-payment
        if (isRefundOrder && originalPayments.length > 0) {
            setTimeout(() => {
                // Remove any existing payment lines first
                while (this.paymentLines.length > 0) {
                    this.currentOrder.removePaymentline(this.paymentLines[0]);
                }

                // Get the total refund amount (priceIncl is negative for refund orders)
                const refundTotal = Math.abs(this.currentOrder.priceIncl);

                // Add payment lines for each original payment method with proportional amounts
                let remainingRefund = refundTotal;

                for (let i = 0; i < originalPayments.length; i++) {
                    const origPayment = originalPayments[i];
                    const availableMethod = this.payment_methods_from_config.find(
                        (pm) => pm.id === origPayment.method.id
                    );

                    if (availableMethod) {
                        // Calculate proportional refund amount for this payment method
                        let refundAmount;
                        if (i === originalPayments.length - 1) {
                            // Last payment method gets the remaining amount to avoid rounding issues
                            refundAmount = remainingRefund;
                        } else {
                            // Calculate proportion: (original_amount / original_total) * refund_total
                            const proportion = origPayment.amount / originalTotalPaid;
                            refundAmount = Math.round(proportion * refundTotal * 100) / 100;
                            remainingRefund -= refundAmount;
                        }

                        // Add the payment line with the calculated amount
                        const result = this.currentOrder.addPaymentline(availableMethod);
                        if (result.status && result.data) {
                            // Set the refund amount (negative for refund)
                            result.data.setAmount(-refundAmount);
                        }
                    }
                }

                // If no payment lines were added (all original methods unavailable), 
                // fall back to default behavior - add first available method
                if (this.paymentLines.length === 0 && this.payment_methods_from_config.length > 0) {
                    const result = this.currentOrder.addPaymentline(this.payment_methods_from_config[0]);
                    if (result.status) {
                        this.numberBuffer.set(result.data.amount.toString());
                    }
                }
            }, 0);
        }
    },
});
