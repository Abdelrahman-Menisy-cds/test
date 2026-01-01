/** @odoo-module */

import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    /**
     * Override setUnitPrice to apply discount from discount pricelist.
     */
    setUnitPrice(price) {
        // Call super first
        super.setUnitPrice(price);
        
        // Apply discount from discount pricelist after price is set
        this._applyDiscountPricelist();
    },

    canBeMergedWith(orderline) {
        // Keep Odoo default behavior first.
        if (super.canBeMergedWith(orderline)) {
            return true;
        }

        // Odoo core prevents merging discounted lines.
        // We allow merging if both lines have the same product and the same discount.
        const ProductPrice = this.models["decimal.precision"].find((dp) => dp.name === "Product Price");
        const price = ProductPrice.round(this.price_unit || 0);
        const product = orderline.getProduct();

        let order_line_price = product.getPrice(
            orderline.order_id.pricelist_id,
            this.getQuantity(),
            0,
            false,
            product
        );
        order_line_price = this.currency.round(order_line_price);

        const isSameCustomerNote =
            (Boolean(orderline.getCustomerNote()) === false && Boolean(this.getCustomerNote()) === false) ||
            orderline.getCustomerNote() === this.getCustomerNote();

        return (
            orderline.getNote() === this.getNote() &&
            this.getProduct().id === orderline.getProduct().id &&
            this.isPosGroupable() &&
            this.getDiscount() === orderline.getDiscount() &&
            this.currency.isZero(price - order_line_price - orderline.getPriceExtra()) &&
            !this.isLotTracked() &&
            this.full_product_name === orderline.full_product_name &&
            isSameCustomerNote &&
            !this.refunded_orderline_id &&
            !orderline.isPartOfCombo()
        );
    },
    
    /**
     * Apply discount from the discount pricelist if configured.
     * This is separated to avoid interfering with the base setUnitPrice logic.
     */
    _applyDiscountPricelist() {
        if (!this.config || !this.product_id || !this.order_id) {
            return;
        }

        const discountPricelist = this.config.discount_pricelist_id;
        if (!discountPricelist) {
            return;
        }

        const pricelistId = typeof discountPricelist === "object" ? discountPricelist.id : discountPricelist;
        if (!pricelistId) {
            return;
        }

        const product = this.product_id;
        const productTemplate = product.product_tmpl_id;
        const orderlines = this.order_id.lines || [];

        // Compute total quantity of this product in the order.
        // This is required to respect pricelist min_quantity rules.
        const totalQty = orderlines
            .filter((l) => l.product_id?.id === product.id)
            .reduce((sum, l) => sum + (typeof l.qty === "number" ? l.qty : 0), 0);

        const pricelistItemsModel = this.models["product.pricelist.item"];
        if (!pricelistItemsModel) {
            return;
        }

        const allItems = pricelistItemsModel.getAll
            ? pricelistItemsModel.getAll()
            : pricelistItemsModel.records
              ? Array.from(pricelistItemsModel.records.values())
              : [];

        const candidates = allItems.filter((rule) => {
            const rulePricelistId = typeof rule.pricelist_id === "object" ? rule.pricelist_id?.id : rule.pricelist_id;
            if (rulePricelistId !== pricelistId) {
                return false;
            }
            if ((rule.min_quantity || 0) > totalQty) {
                return false;
            }

            const appliedOn = rule.applied_on;
            const ruleProductId = typeof rule.product_id === "object" ? rule.product_id?.id : rule.product_id;
            const ruleTmplId = typeof rule.product_tmpl_id === "object" ? rule.product_tmpl_id?.id : rule.product_tmpl_id;
            const ruleCategId = typeof rule.categ_id === "object" ? rule.categ_id?.id : rule.categ_id;
            const productCategId =
                typeof productTemplate?.categ_id === "object" ? productTemplate?.categ_id?.id : productTemplate?.categ_id;

            if (appliedOn === "0_product_variant") {
                return !!ruleProductId && ruleProductId === product.id;
            }
            if (appliedOn === "1_product") {
                return !!ruleTmplId && ruleTmplId === productTemplate?.id;
            }
            if (appliedOn === "2_product_category") {
                return !!ruleCategId && !!productCategId && ruleCategId === productCategId;
            }
            if (appliedOn === "3_global") {
                return true;
            }
            return false;
        });

        // Prefer higher min_quantity, then more specific rule.
        const specificity = {
            "0_product_variant": 3,
            "1_product": 2,
            "2_product_category": 1,
            "3_global": 0,
        };
        candidates.sort((a, b) => {
            const mq = (b.min_quantity || 0) - (a.min_quantity || 0);
            if (mq) {
                return mq;
            }
            return (specificity[b.applied_on] || 0) - (specificity[a.applied_on] || 0);
        });

        const applicableRule = candidates[0];
        if (applicableRule && applicableRule.compute_price === "percentage") {
            // Use setDiscount so that the POS recomputes totals properly.
            this.setDiscount(applicableRule.percent_price);
        }
    },
});
