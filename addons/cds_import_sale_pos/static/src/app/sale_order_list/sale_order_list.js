/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { SaleOrderRow } from "@cds_import_sale_pos/app/sale_order_row/sale_order_row";
import { useService } from "@web/core/utils/hooks";

/**
 * @props {models.Order} [initHighlightedOrder] initially highligted order
 * @props {Array<models.Order>} orders
 */
export class SaleOrderList extends Component {
    static components = { SaleOrderRow };
    static template = "cds_import_sale_pos.SaleOrderList";

    setup() {
        this.ui = useState(useService("ui"));
        this.state = useState({ highlightedOrder: this.props.initHighlightedOrder || null });
    }
    get highlightedOrder() {
        return this.state.highlightedOrder;
    }
    _onClickOrder(order) {
        this.state.highlightedOrder = order;
    }
}
