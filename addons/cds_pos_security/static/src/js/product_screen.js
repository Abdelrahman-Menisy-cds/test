/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { NumberPopup } from "@point_of_sale/app/components/popups/number_popup/number_popup";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
    },

    async get_access(pass_name) {
        const pass_value = this.pos.config[pass_name];
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
    //@Override
    onNumpadClick(buttonValue) {
        
        if(buttonValue === "price"){
            this.get_access('price_password').then((access) => {
                if(access){
                    super.onNumpadClick(buttonValue);
                }
                else{
                    return;
                }
            })
        }
        else if(buttonValue === "discount"){
            this.get_access('discount_password').then((access) => {
                if(access){
                    super.onNumpadClick(buttonValue);
                }
                else{
                    return;
                }
            })
        }
        // else if(buttonValue === "Backspace"){
        //     this.get_access('delete_password').then((access) => {
        //         if(access){
        //             super.onNumpadClick(buttonValue);
        //         }
        //         else{
        //             return;
        //         }
        //     })
        // }
        // else if(buttonValue === "-"){
        //     this.get_access('change_sign_pwd').then((access) => {
        //         if(access){
        //             super.onNumpadClick(buttonValue);
        //         }
        //         else{
        //             return;
        //         }
        //     })
        // }
        else{
            super.onNumpadClick(buttonValue);
        }
    },
    async updateSelectedOrderline({ buffer, key }) {
        const order = this.pos.getOrder();
        const selectedLine = order.getSelectedOrderline();
        if (!selectedLine) {
            return false;
        }
        const quantity = selectedLine.getQuantity();
                
        if(quantity === 0 || quantity == 0){
            this.currentOrder.removeOrderline(selectedLine)
            return
        }
        if(key === "Backspace"){
                this.get_access('delete_password').then((access) => {
                    if(access){
                        super.updateSelectedOrderline({ buffer, key });
                        this.currentOrder.removeOrderline(selectedLine)
                        return
                    }
                    else{
                        return;
                    }
                })
            } else if(key === "Delete"){
                this.get_access('delete_password').then((access) => {
                    if(access){
                        super.updateSelectedOrderline({ buffer, key });
                        this.currentOrder.removeOrderline(selectedLine)
                        return
                    }
                    else{
                        return;
                    }
                })
            }else if(key === "-"){
                this.get_access('change_sign_pwd').then((access) => {
                    if(access){
                        super.updateSelectedOrderline({ buffer, key });
                    }
                    else{
                        return;
                    }
                })
            } else {
                super.updateSelectedOrderline({ buffer, key });
            }
    }

});
