// Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
//
// Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
// It is forbidden to publish, distribute, sublicense, or sell copies
//
// of the Software or modified copies of the Software.

/**
 * This file ensures the JsBarcode library is properly loaded and available
 * for use in the Odoo 19.0 environment.
 */

import { loadJS } from "@web/core/assets";

/**
 * Hook to ensure JsBarcode is loaded and available
 * @returns {Object} - Object with loadJsBarcode method
 */
export function useJsBarcode() {
    return {
        loadJsBarcode: async () => {
            if (typeof JsBarcode === 'undefined') {
                try {
                    // Load JsBarcode from the module's static files
                    await loadJS('/cds_pos/static/src/js/libs/jquery-barcode-last.min.js');
                    console.log('JsBarcode library loaded successfully');
                } catch (e) {
                    console.error('Failed to load JsBarcode library:', e);
                    return false;
                }
                
                // Verify it loaded correctly
                if (typeof JsBarcode === 'undefined') {
                    console.error('JsBarcode still undefined after loading');
                    return false;
                }
            }
            return true;
        }
    };
}

// Export the global JsBarcode function for backward compatibility
export const JsBarcodeFunction = function(element, data, options) {
    if (typeof JsBarcode !== 'undefined') {
        return JsBarcode(element, data, options);
    } else {
        console.error('JsBarcode not loaded yet');
        return null;
    }
};
