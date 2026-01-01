/** @odoo-module */

import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(Navbar.prototype, {
    onImportSaleButtonClick() {
        console.log("onImportSaleButtonClick");
        this.pos.navigate("SaleOrderScreen", { stateOverride: { filter: "ONGOING" } });
    },
});
