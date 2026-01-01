import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";

patch(TicketScreen.prototype, {
    setPartnerToRefundOrder(partner, destinationOrder) {
        super.setPartnerToRefundOrder(...arguments);
        //  set same sales person as the orginal order
        const Order = this.getSelectedOrder()
        if(!destinationOrder.sale_person_id || !destinationOrder.sale_person_name){
            if(Order.sale_person_id){
                destinationOrder.sale_person_id = Order.sale_person_id.id;
                destinationOrder.sale_person_name = Order.sale_person_id.name;
            }
            // get also sales person from the orderlines
            // const orderlines = Order.orderlines 
            let updateddestinationOrderlines = destinationOrder.lines
            for (const orderline of Order.lines) {
                    //loop through the destinationOrderlines
                for (const destinationOrderline of updateddestinationOrderlines) {
                    // validation to check if it is the same full_product_name
                    if(destinationOrderline.refunded_orderline_id.id == orderline.id){
                        if(orderline.sale_person_id){
                            destinationOrderline.sale_person_id = orderline.sale_person_id.id;
                            destinationOrderline.sale_person_name = orderline.sale_person_id.name;
                        }
                        break;
                    }
                }
            }
            destinationOrder.lines = updateddestinationOrderlines
        }
    },
});
