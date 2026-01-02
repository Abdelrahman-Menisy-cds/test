# CDS Sale Internal Transfer Module

## Description
This module allows linking Sales Orders with Internal Transfers in Odoo 19.

## Features
- Add Internal Transfer field in Quotations/Sales Orders
- Select Internal Transfers with Done status only
- Auto-add products from Internal Transfer to Sales Order lines
- Prevent using the same Internal Transfer in multiple Sales Orders
- Ensure quantities and products match exactly those in the Internal Transfer
- Validation to prevent changes after order confirmation

## Technical Details
- **Module Name**: cds_sale_internal_transfer
- **Version**: 19.0.1.0.0
- **Dependencies**: sale, stock
- **Author**: CDS Solutions SRL

## Installation
1. Copy the module to your Odoo addons directory
2. Update the module list in Odoo
3. Install the module from Apps menu

## Usage
1. Create or edit a Sales Order/Quotation
2. Select an Internal Transfer from the dropdown (only Done status transfers are shown)
3. Products from the selected Internal Transfer will be automatically added to the order lines
4. Confirm the Sales Order

## Constraints
- Internal Transfer must be in Done status
- Same Internal Transfer cannot be used in multiple Sales Orders
- Internal Transfer cannot be changed after Sales Order confirmation
- Products and quantities are automatically synchronized from the Internal Transfer

## Development
**Developed by**: Abdelrahman Menisy (<a.mansy@cdsegypt.com>)
**Company**: CDS Solutions SRL (https://www.cdsegypt.com)

## License
LGPL-3

## Copyright
Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
