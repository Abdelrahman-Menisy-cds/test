/** @odoo-module **/

import MainMenu from "@stock_barcode/stock_barcode_menu";
import Session from 'web.session';

MainMenu.include({
    events: Object.assign({}, MainMenu.prototype.events, {
        "click .button_operations": function () {
            this.do_action('cds_warehouse_restriction.action_picking_type_barcode_stock');
        },
    }),
    //   willStart: async function () {
    //     await this._super(...arguments);
    //     this.group_inventory_adjustment = await Session.user_has_group('cds_stock.group_edit_stock_quant');
    // },


});
