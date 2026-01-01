/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { LoginBackItem, LoginAsItem } from "./user_menu_items";
const serviceRegistry = registry.category("services");
const userMenuRegistry = registry.category("user_menuitems");

const LoginAsService = {
    start() {
        if (odoo.debug && !session.is_public) {
            userMenuRegistry.add("cds_login_as.login_as", LoginAsItem);
        }

        if (session.login_as_original_uid) {
            // userMenuRegistry.remove('cds_login_as.login_as');
            userMenuRegistry.add("cds_login_as.login_back", LoginBackItem);
        }
    },
};

serviceRegistry.add("login_as", LoginAsService);
