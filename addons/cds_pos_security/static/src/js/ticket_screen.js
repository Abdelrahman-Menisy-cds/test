/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

//Refund password validation and popup
patch(TicketScreen.prototype, {


    async onDoRefund() {
        const pass_value = this.pos.config["refund_security"];
        if (!pass_value) {
            return super.onDoRefund(...arguments);
        }
        const payload = await makeAwaitable(this.dialog, NumberPopup, {
                formatDisplayedValue: (x) => x.replace(/./g, "•"),
                title: _t("Password?"),
            });
        if (payload) {
            if (payload !== pass_value) {
                this.dialog.add(AlertDialog,{
                    title: _t('Wrong Password'),
                    body : _t('Invalid Password'),
                    });
                return false;
            }
            else {
                return super.onDoRefund(...arguments);
            }
        }
    },
})
