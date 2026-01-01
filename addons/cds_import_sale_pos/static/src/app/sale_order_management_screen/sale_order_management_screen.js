/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { parseFloat } from "@web/views/fields/parsers";
import { useBus, useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";


import { SaleOrderList } from "@cds_import_sale_pos/app/sale_order_list/sale_order_list";
import { SaleOrderManagementControlPanel } from "@cds_import_sale_pos/app/sale_order_management_control_panel/sale_order_management_control_panel";
import { Component, onMounted, useRef } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/hooks/pos_hook";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { Orderline as OrderlineComponent } from "@point_of_sale/app/components/orderline/orderline";

import { OrderDisplay } from "@point_of_sale/app/components/order_display/order_display";
import { Numpad } from "@point_of_sale/app/components/numpad/numpad";
import { useState } from "@odoo/owl";

/**
 * ID getter to take into account falsy many2one value.
 * @param {[id: number, display_name: string] | false} fieldVal many2one field value
 * @returns {number | false}
 */
function getId(fieldVal) {
    return fieldVal && fieldVal[0];
}

export class SaleOrderScreen extends Component {
    static storeOnOrder = false;
    static components = { SaleOrderList, SaleOrderManagementControlPanel,
        ActionpadWidget,
        OrderlineComponent,
        OrderDisplay,
        Numpad,
     };
    static template = "cds_import_sale_pos.SaleOrderScreen";
    static numpadActionName = _t("Refund");

    setup() {
        super.setup();
        this.pos = usePos();
        // this.popup = useService("popup");
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.root = useRef("root");
        this.numberBuffer = useService("number_buffer");
        this.numberBuffer.use({
            triggerAtInput: (event) => this._onUpdateSelectedOrderline(event),
        });
        this.saleOrderFetcher = useService("cds_sale_order_fetcher");
        // this.notification = useService("pos_notification");
        this.ui = useState(useService("ui"));
        // Add state to track the selected sale order and orderline
        this._state = useState({
            ui: {
                selectedOrderlineId: null,
                selectedOrder: this.pos.getOrder(),
                selectedOrderlineIds: {}
            },
            // Track qty to refund for each sale order line
            saleLineToRefundQty: {}
        });
        useBus(this.saleOrderFetcher, "update", this.render);

        onMounted(this.onMounted);
    }
    onMounted() {
        this.saleOrderFetcher.fetch();
    }
    _getSaleOrderOrigin(order) {
        for (const line of order.getOrderlines()) {
            if (line.refund_sale_order_id) {
                return line.refund_sale_order_id;
            }
        }
        return false;
    }
    get selectedPartner() {
        const order = this.pos.orderManagement.selectedOrder;
        return order ? order.getPartner() : null;
    }
    get orders() {
        return this.saleOrderFetcher.get();
    }
    async _setNumpadMode(event) {
        const { mode } = event.detail;
        this.numpadMode = mode;
        this.numberBuffer.reset();
    }
    onNextPage() {
        this.saleOrderFetcher.nextPage();
    }
    onPrevPage() {
        this.saleOrderFetcher.prevPage();
    }
    onSearch(domain) {
        this.saleOrderFetcher.setSearchDomain(domain);
        this.saleOrderFetcher.setPage(1);
        this.saleOrderFetcher.fetch();
    }
    async onClickSaleOrder(clickedOrder) {
        const sale_order = await this._getSaleOrder(clickedOrder.id);
        if(this.pos.getOrder()){
            this.pos.removeOrder(this.pos.getOrder());
        }
        const currentPosOrder = this.pos.addNewOrder();
        if (sale_order.partner_id) {
            currentPosOrder.setPartner(sale_order.partner_id);
        }

        // Fiscal position should be set after the partner is set
        // to ensure that the fiscal position is correctly computed
        // based on sale order.
        const orderFiscalPos = sale_order.fiscal_position_id;
        currentPosOrder.update({
            fiscal_position_id: orderFiscalPos,
        });
        await this.settleSO(currentPosOrder, sale_order, orderFiscalPos);
        this._state.ui.selectedOrder = currentPosOrder;
    }

    async _getSaleOrder(id) {
        const sale_order = (await this.pos.data.read("sale.order", [id]))[0];
        const orderlines = await this.pos.data.read("sale.order.line", sale_order.raw.order_line);
        sale_order.order_line = orderlines;
        return sale_order;
    }

    async settleSO(currentPosOrder, sale_order, orderFiscalPos) {
        if (sale_order.pricelist_id) {
            currentPosOrder.setPricelist(sale_order.pricelist_id);
        }
        let useLoadedLots = false;
        let userWasAskedAboutLoadedLots = false;
        let previousProductLine = null;

        const converted_lines = await this.pos.data.call("sale.order.line", "read_refund_converted", [
            sale_order.order_line.map((l) => l.id),
        ]);
        for (const line of sale_order.order_line) {
            if (line.display_type === "line_note") {
                if (previousProductLine) {
                    const previousNote = previousProductLine.customer_note;
                    previousProductLine.customer_note = previousNote
                        ? previousNote + "--" + line.name
                        : line.name;
                }
                continue;
            }


            const taxes = orderFiscalPos?.getTaxesAfterFiscalPosition(line.tax_ids) || line.tax_ids;
            const newLineValues = {
                product_tmpl_id: line.product_id?.product_tmpl_id,
                product_id: line.product_id,
                qty: line.product_uom_qty,
                price_unit: line.price_unit,
                price_type: "automatic",
                tax_ids: taxes.map((tax) => ["link", tax]),
                refund_sale_order_id: sale_order,
                refund_sale_order_line_id: line,
                refunded_sale_qty: line.pos_refunded_qty,
                customer_note: line.customer_note,
                description: line.name,
                order_id: currentPosOrder,
            };
            if (line.display_type === "line_section") {
                continue;
            }
            const newLine = await this.pos.addLineToCurrentOrder(newLineValues, {}, false);
            previousProductLine = newLine;

            const converted_line = converted_lines.find((l) => l.id === line.id);
            if (
                newLine.getProduct().tracking !== "none" &&
                (this.pos.pickingType.use_create_lots || this.pos.pickingType.use_existing_lots) &&
                converted_line.lot_names.length > 0
            ) {
                if (!useLoadedLots && !userWasAskedAboutLoadedLots) {
                    useLoadedLots = await ask(this.dialog, {
                        title: _t("SN/Lots Loading"),
                        body: _t("Do you want to load the SN/Lots linked to the Sales Order?"),
                    });
                    userWasAskedAboutLoadedLots = true;
                }
                if (useLoadedLots) {
                    newLine.setPackLotLines({
                        modifiedPackLotLines: [],
                        newPackLotLines: (converted_line.lot_names || []).map((name) => ({
                            lot_name: name,
                        })),
                    });
                }
            }

            // converted_line.has_valued_move_ids = await this.pos.data.call(
            //     "sale.order.line",
            //     "has_valued_move_ids",
            //     [converted_line.id]
            // );
            console.log(converted_line);
            newLine.setRefundQuantityFromSOL(converted_line);
            newLine.setUnitPrice(converted_line.price_unit);
            newLine.setDiscount(line.discount);

            const product_unit = line.product_id.uom_id;
            if (product_unit && !product_unit.is_pos_groupable) {
                let remaining_quantity = newLine.qty;
                newLineValues.product_id = newLine.product_id;
                newLine.delete();
                while (!product_unit.isZero(remaining_quantity)) {
                    const splitted_line = this.pos.models["pos.order.line"].create({
                        ...newLineValues,
                    });
                    splitted_line.setQuantity(Math.min(remaining_quantity, 1.0), true);
                    splitted_line.setDiscount(line.discount);
                    remaining_quantity -= splitted_line.qty;
                }
            }

            // Order line can only hold one lot, so we need to split the line if there are multiple lots
            if (line.product_id.tracking == "lot" && converted_line.lot_names.length > 0) {
                newLine.delete();
                for (const lot of converted_line.lot_names) {
                    const splitted_line = this.pos.models["pos.order.line"].create({
                        ...newLineValues,
                    });
                    splitted_line.setQuantity(converted_line.lot_qty_by_name[lot] || 0, true);
                    splitted_line.setPackLotLines({
                        modifiedPackLotLines: [],
                        newPackLotLines: [{ lot_name: lot }],
                        setQuantity: false,
                    });
                }
            }
        }
        console.log(currentPosOrder);
    }

    // async _getSOLines(ids) {
    //     const so_lines = await this.orm.call("sale.order.line", "read_refund_converted", [ids]);
    //     return so_lines;
    // }
    getSelectedPartner() {
        const order = this.getSelectedOrder();
        return order ? order.getPartner() : null;
    }
    getNumpadButtons() {
        return [
            { value: "1" },
            { value: "2" },
            { value: "3" },
            { value: "quantity", text: _t("Qty"), class: "active border-primary" },
            { value: "4" },
            { value: "5" },
            { value: "6" },
            { value: "discount", text: _t("% Disc"), disabled: true },
            { value: "7" },
            { value: "8" },
            { value: "9" },
            { value: "price", text: _t("Price"), disabled: true },
            { value: "-", text: "+/-", disabled: true },
            { value: "0" },
            { value: this.env.services.localization.decimalPoint },
            { value: "Backspace", text: "⌫" },
        ];
    }
    getHasItemsToRefund() {
        const saleOrder = this.getSelectedOrder();
        if (!saleOrder) {
            return false;
        }
        
        // Check if any sale order line has a to-refund quantity > 0
        for (const saleOrderLine of saleOrder?.orderlines || []) {
            const toRefundQty = this._getSaleLineToRefundQty(saleOrderLine);
            if (toRefundQty > 0) {
                return true;
            }
        }
        return false;
    }
    async onDoRefund() {
        const saleOrder = this.getSelectedOrder();
        if (!saleOrder) {
            this.dialog.add(AlertDialog, {
                title: _t("No order selected"),
                body: _t("Please select a sale order to refund."),
            });
            return;
        }

        // Collect sale order lines that have quantities to refund
        const linesToRefund = [];
        for (const saleOrderLine of saleOrder.lines) {
            const toRefundQty = this._getSaleLineToRefundQty(saleOrderLine);
            if (toRefundQty > 0) {
                linesToRefund.push({
                    saleOrderLine: saleOrderLine,
                    qtyToRefund: toRefundQty
                });
            }
        }

        if (!linesToRefund.length) {
            this.dialog.add(AlertDialog, {
                title: _t("No quantities to refund"),
                body: _t("Please select quantities to refund for at least one line using the numpad."),
            });
            return;
        }
        // remove lines from current order
        const to_remove_order = this.pos.getOrder();
        // Get or create the current POS order for the refund
        const refundOrder = this.pos.addNewOrder();
        
        // Create refund lines for each selected sale order line
        for (const { saleOrderLine, qtyToRefund } of linesToRefund) {
            // Create line values
            const new_line = this.pos.models["pos.order.line"].create({
                qty: -qtyToRefund,
                price_unit: saleOrderLine.price_unit,
                product_id: saleOrderLine.product_id,
                order_id: refundOrder,
                discount: saleOrderLine.discount,
                tax_ids: saleOrderLine.tax_ids.map((tax) => ["link", tax]),
                refund_sale_order_id: saleOrderLine.refund_sale_order_id,
                refund_sale_order_line_id: saleOrderLine.refund_sale_order_line_id,
                pack_lot_ids: saleOrderLine.pack_lot_ids.map((packLot) => [
                    "create",
                    { lot_name: packLot.lot_name },
                ]),
                price_type: "automatic",
            });

            // Handle lot/serial numbers if present
            if (saleOrderLine.pack_lot_lines && saleOrderLine.pack_lot_lines.length > 0) {
                new_line.setPackLotLines({
                    modifiedPackLotLines: [],
                    newPackLotLines: saleOrderLine.pack_lot_lines.map((lot) => ({
                        lot_name: lot.lot_name
                    })),
                });
            }
            // Reset the to-refund quantity for this line
            this._setSaleLineToRefundQty(saleOrderLine, 0);
        }
        
        // Set order customer
        if (saleOrder.partner_id) {
            refundOrder.setPartner(saleOrder.partner_id);
        }        
        // Clear the number buffer
        this.numberBuffer.reset();
        this.pos.removeOrder(to_remove_order);
        // Set the current order and go to payment screen
        this.pos.navigate("ProductScreen", { orderUuid: refundOrder.uuid });
    }

    getSelectedOrderlineId() {
        return this._state.ui.selectedOrderlineIds;
    }
    getSelectedOrder() {
        if (this._state.ui.selectedOrder) {
            return this._state.ui.selectedOrder;
        } else {
            return null;
        }
    }
    onClickOrderline(orderline) {
            const order = this.getSelectedOrder();
            this._state.ui.selectedOrderlineIds = orderline.id;
            this.numberBuffer.reset();
    }
    get isOrderSynced() {
        return true;
    }

    /**
     * Get or initialize the to-refund quantity for a sale order line
     * @param {Object} saleOrderLine - The sale order line object
     * @returns {number} - The quantity to refund
     */
    _getSaleLineToRefundQty(saleOrderLine) {
        if (!saleOrderLine || !saleOrderLine.id) {
            return 0;
        }
        // Initialize to 0 if not set
        if (!(saleOrderLine.id in this._state.saleLineToRefundQty)) {
            this._state.saleLineToRefundQty[saleOrderLine.id] = 0;
        }
        return this._state.saleLineToRefundQty[saleOrderLine.id];
    }

    /**
     * Set the to-refund quantity for a sale order line
     * @param {Object} saleOrderLine - The sale order line object
     * @param {number} qty - The quantity to refund
     */
    _setSaleLineToRefundQty(saleOrderLine, qty) {
        if (saleOrderLine && saleOrderLine.id) {
            this._state.saleLineToRefundQty[saleOrderLine.id] = qty;
        }
    }
    _onUpdateSelectedOrderline({ key, buffer }) {
        const order = this.getSelectedOrder();
        if (!order) {
            return this.numberBuffer.reset();
        }

        const selectedOrderlineId = this.getSelectedOrderlineId();
        const saleOrderLine = order.lines.find((line) => line.id == selectedOrderlineId);
        if (!saleOrderLine) {
            return this.numberBuffer.reset();
        }

        // Calculate refundable quantity (ordered qty - already refunded qty)
        const refundableQty = saleOrderLine.qty - (saleOrderLine.refunded_sale_qty || 0);
        
        if (refundableQty <= 0) {
            this.numberBuffer.reset();
            // this.notification.add(_t("This line has already been fully refunded."), 3000);
            return;
        }

        // Update the to-refund quantity based on numpad input
        if (buffer == null || buffer == "") {
            this._setSaleLineToRefundQty(saleOrderLine, 0);
        } else {
            const quantity = Math.abs(parseFloat(buffer));
            if (quantity > refundableQty) {
                this.numberBuffer.reset();
                this.dialog.add(AlertDialog, {
                    title: _t("Maximum Exceeded"),
                    body: _t(
                        "The requested quantity to be refunded is higher than the refundable quantity. %s is requested while only %s can be refunded.",
                        this.env.utils.formatProductQty(quantity),
                        this.env.utils.formatProductQty(refundableQty)
                    ),
                });
            } else {
                this._setSaleLineToRefundQty(saleOrderLine, quantity);
            }
        }
    }
}

registry.category("pos_pages").add("SaleOrderScreen", {
    name: "SaleOrderScreen",
    component: SaleOrderScreen,
    route: `/pos/ui/${odoo.pos_config_id}/sale_order`,
    params: {},
});