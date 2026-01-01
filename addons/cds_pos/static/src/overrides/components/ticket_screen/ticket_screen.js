/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
// import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";

const { DateTime } = luxon;
const now = DateTime.now();

patch(TicketScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.state.search = {
            fieldName: "RECEIPT_NUMBER",
            searchTerm: "",
        };
        this._matchingPartnerIds = [];
    },
    
    /**
     * Override the _getSearchFields method to enhance PARTNER search with phone/mobile
     */
    _getSearchFields() {
        const fields = super._getSearchFields();
        
        // Enhance the PARTNER field to include phone/mobile in the representation for local search
        if (fields.PARTNER) {
            fields.PARTNER.repr = (order) => {
                const partner = order.getPartner();
                if (!partner) return '';
                
                const name = partner.complete_name || partner.name || '';
                const phone = partner.phone || '';
                const mobile = partner.mobile || '';
                
                return `${name} ${phone} ${mobile}`.trim();
            };
        }
        
        return fields;
    },
    
    /**
     * Override onSearch to search partners by name, phone or mobile (same as PartnerList popup)
     */
    async onSearch(search) {
        this._matchingPartnerIds = [];
        
        // If searching by PARTNER, use the same search logic as the partner list popup
        if (search.fieldName === "PARTNER" && search.searchTerm) {
            const term = search.searchTerm.trim();
            try {
                // Use the same search fields as PartnerList popup
                const search_fields = [
                    "name",
                    "parent_name",
                    "phone_mobile_search",
                    "email",
                    "barcode",
                ];
                // Build domain with OR conditions for all search fields
                const domain = [
                    ...Array(search_fields.length - 1).fill("|"),
                    ...search_fields.map((field) => [field, "ilike", term + "%"]),
                ];
                
                const result = await this.pos.data.callRelated("res.partner", "get_new_partner", [
                    this.pos.config.id,
                    domain,
                    0,
                ]);
                
                if (result["res.partner"] && result["res.partner"].length > 0) {
                    this._matchingPartnerIds = result["res.partner"].map(p => p.id);
                }
            } catch (e) {
                console.error("Error searching partners:", e);
            }
        }
        
        return super.onSearch(search);
    },
    
    /**
     * Override _computeSyncedOrdersDomain to include partner IDs from phone/mobile search
     */
    _computeSyncedOrdersDomain() {
        // If we have matching partner IDs from phone search, use them directly
        if (this._matchingPartnerIds && this._matchingPartnerIds.length > 0 && 
            this.state.search.fieldName === "PARTNER") {
            return [["partner_id", "in", this._matchingPartnerIds]];
        }
        
        return super._computeSyncedOrdersDomain();
    },
    
    /**
     * Override getFilteredOrderList to filter by matching partners (name, phone, mobile)
     */
    getFilteredOrderList() {
        let orders = super.getFilteredOrderList();
        
        // If we found matching partners, filter orders to include only those partners
        if (this._matchingPartnerIds && this._matchingPartnerIds.length > 0 && 
            this.state.search.fieldName === "PARTNER") {
            orders = orders.filter(order => {
                const partner = order.getPartner();
                return partner && this._matchingPartnerIds.includes(partner.id);
            });
        }
        
        return orders;
    },
    async onDoRefund() {
        const order = this.getSelectedOrder();
        // In Odoo 19, order.date_order is already a Luxon DateTime object
        const orderDateTime = order.date_order;
        const fourteenDaysAgo = DateTime.now().minus({ days: this.pos.config.refund_period });
        if (orderDateTime < fourteenDaysAgo) {
            this.dialog.add(AlertDialog, {
                'title': _t("POS error"),
                'body': _t("Refund is only allowed for orders placed in the last %s days." , this.pos.config.refund_period)
            });
            return;
        }
        super.onDoRefund(...arguments);
    }
});