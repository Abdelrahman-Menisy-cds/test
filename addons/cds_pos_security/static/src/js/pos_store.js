import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(PosStore.prototype, {
    async get_access(pass_name) {
        const pass_value = this.config[pass_name];
        if (!pass_value) {
            return true;
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
                return true;
            }
        }
    },
    async onDeleteOrder(order) {
        const pass_value = this.config["delete_order_pwd"];
        if (!pass_value) {
            return super.onDeleteOrder(...arguments);
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
                return super.onDeleteOrder(...arguments);
            }
        }
    },
    navigate(routeName, routeParams = {}) {
        if (routeName === "TicketScreen") {
            this.get_access('view_orders_pwd').then((access) => {
                if(access){
                    super.navigate(routeName, routeParams);
                }
                else{
                    return;
                }
            })
        }else{
            return super.navigate(routeName, routeParams);
        }
    }
})