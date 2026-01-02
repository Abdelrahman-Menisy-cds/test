# CDS Sales Internal Transfer

## Overview

This module allows you to link Sales Orders with Internal Transfers, providing seamless integration between your sales and warehouse operations.

## Features

- **Internal Transfer Field**: Adds an "Internal Transfer" field in Sales Order (Quotation) form
- **Auto Product Addition**: Automatically adds products from the selected Internal Transfer to the Sales Order lines
- **Status Validation**: Only allows selection of Internal Transfers in "Done" status
- **Duplicate Prevention**: Prevents the same Internal Transfer from being linked to multiple Sales Orders
- **Quantity Validation**: Ensures quantities and products match exactly between Internal Transfer and Sales Order
- **Price Calculation**: Automatically calculates prices based on product list price or pricelist

## Usage

1. Go to Sales > Quotations or create a new Sales Order
2. In the Sales Order form, you'll see an "Internal Transfer" field (requires stock user permissions)
3. Select an Internal Transfer that is in "Done" status
4. The products from the Internal Transfer will be automatically added to the order lines
5. Review the quantities and prices, then confirm the Sales Order

## Constraints

- Each Internal Transfer can only be linked to one Sales Order
- Internal Transfer must be in "Done" status to be selected
- Quantities must match exactly between Internal Transfer and Sales Order
- Field becomes read-only when Sales Order is confirmed/cancelled

## Technical Details

### Models Modified

- `sale.order`: Added `internal_transfer_id` field and related methods

### Key Methods

- `_onchange_internal_transfer_id()`: Handles automatic product addition
- `_check_internal_transfer_unique()`: Constraint to prevent duplicates
- `action_confirm()`: Validation before confirming Sales Order

### Dependencies

- `sale`: Base Sales module
- `stock`: Warehouse/Inventory module

## Installation

1. Copy the module to your Odoo addons directory
2. Update the module list in Odoo
3. Install the "CDS Sales Internal Transfer" module
4. Restart Odoo server

## Security

The Internal Transfer field is only visible to users with "Stock User" permissions (`stock.group_stock_user`).

## Version Compatibility

- Odoo 19.0+

## Author

**CDS Solutions SRL**
- Website: https://www.cdsegypt.com
- Contributors: 
  - Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
  - Abdelrahman Menisy (<a.mansy@cdsegypt.com>)

## License

LGPL-3

## Changes by Abdelrahman Menisy

### Version 1.0 - Initial Implementation
- Created module structure
- Added Internal Transfer field to Sales Order
- Implemented automatic product addition logic
- Added validation constraints
- Created view modifications
- Added comprehensive documentation
