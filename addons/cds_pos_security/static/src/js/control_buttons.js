/** @odoo-module */
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(ControlButtons.prototype, {

    async clickPricelist() {
        const pass_value = this.pos.config["pricelist_pwd"];
        if (!pass_value) {
            return super.clickPricelist();
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
                return super.clickPricelist();
            }
        }
    },
    async apply_discount(pc) {
        const pass_value = this.pos.config["global_discount_password"];
        if (!pass_value) {
            return super.apply_discount(...arguments);
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
                return super.apply_discount(...arguments);
            }
        }
    },
    async clickFiscalPosition() {
        const pass_value = this.pos.config["fiscal_position_password"];
        if (!pass_value) {
            return super.clickFiscalPosition();
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
                return super.clickFiscalPosition();
            }
        }
    },
})