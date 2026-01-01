// Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
//
// Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
// It is forbidden to publish, distribute, sublicense, or sell copies
//
// of the Software or modified copies of the Software.

import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { loadJS } from "@web/core/assets";
import { onMounted, useState } from "@odoo/owl";

// Load JsBarcode library globally
let jsBarcodeLoaded = false;
let jsBarcodeLoadPromise = null;

async function ensureJsBarcodeLoaded() {
    if (jsBarcodeLoaded && window.JsBarcode) {
        return true;
    }
    if (jsBarcodeLoadPromise) {
        return jsBarcodeLoadPromise;
    }
    jsBarcodeLoadPromise = (async () => {
        try {
            await loadJS('/cds_pos/static/src/js/libs/jquery-barcode-last.min.js');
            jsBarcodeLoaded = true;
            console.log('JsBarcode loaded successfully, available:', !!window.JsBarcode);
            return !!window.JsBarcode;
        } catch (e) {
            console.error('Failed to load JsBarcode:', e);
            return false;
        }
    })();
    return jsBarcodeLoadPromise;
}

// Patch the OrderReceipt component to add barcode functionality for order search during refund
patch(OrderReceipt.prototype, {
    setup() {
        super.setup(...arguments);
        this.barcodeState = useState({ src: '' });
        
        onMounted(async () => {
            await this.generateBarcode();
        });
    },
    
    async generateBarcode() {
        const order = this.props.order;
        if (!order) return;
        
        const order_barcode = order.pos_reference || order.name || '';
        if (!order_barcode) return;
        
        await ensureJsBarcodeLoaded();
        
        if (window.JsBarcode) {
            try {
                const img = document.createElement("IMG");
                window.JsBarcode(img, order_barcode, {
                    format: "code128",
                    displayValue: true,
                    fontSize: 20,
                    height: 50,
                    width: 1.5,
                });
                this.barcodeState.src = img.src;
                console.log('Barcode generated successfully');
            } catch (error) {
                console.error('Error generating barcode:', error);
            }
        }
    },

    /**
     * Generate a barcode image for the order
     * This barcode can be scanned to search for the order during refund
     * @returns {string} - Base64 encoded barcode image source
     */
    order_jsbarcode() {
        return this.barcodeState?.src || '';
    },
});
