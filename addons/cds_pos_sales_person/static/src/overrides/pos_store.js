/**
 * CDS - Custom Development Solutions
 * Copyright (C) 2023-2025 CDS (<https://cds.net.sa/>)
 */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async afterProcessServerData() {
        await super.afterProcessServerData(...arguments);
        
        // Keep the original functionality for pos_hr module
        if (this.config.module_pos_hr) {
            const saved_cashier = this._getConnectedCashier();
            this.hasLoggedIn = saved_cashier ? true : false;
        }
        
        // Fetch sale_persons_ids from pos.config using data service
        try {
            const result = await this.data.searchRead(
                'pos.config',
                [['id', '=', this.config.id]],
                ['sale_persons_ids']
            );
            // get the id and name from the hr.employee model
            const sale_persons_ids = result[0].sale_persons_ids;
            const sale_persons = await this.data.searchRead(
                'hr.employee',
                [['id', 'in', sale_persons_ids]],
                ['id', 'name']
            );
            this.sale_persons = sale_persons;
            
            
            if (result && result.length > 0) {
                this.config.sale_persons_ids = result[0].sale_persons_ids || [];
            }
        } catch (error) {
            console.error('Error fetching sale_persons_ids:', error);
        }
    },
});