/** @odoo-module **/

import {_t} from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

export function LoginAsItem(env) {
    return {
        type: "item",
        id: "cds_login_as.login_as",
        description: _t("Login As..."),
        callback: () => {
            env.services.action.doAction({
                name: _t('Login As'),
                views: [[false, 'form']],
                res_model: 'cds.login.as.wizard',
                target: 'new',
                type: "ir.actions.act_window",
            });
        },
        sequence: 100,
    };
}

export function LoginBackItem(env) {
    return {
        type: "item",
        id: "cds_login_as.login_back",
        description: _t("Restore Original User"),
        callback: () => {
            env.services.action.doAction({
                type: 'ir.actions.act_url',
                url: '/web/cds_login_back',
                target: 'self',
            });
        },
        sequence: 300,
    };
}

//registry
//    .category("user_menuitems")
//    .add("cds_login_as.login_as", LoginAsItem)
//    .add("cds_login_as.login_back", LoginBackItem);