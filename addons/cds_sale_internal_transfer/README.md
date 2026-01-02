# CDS Sale Internal Transfer Module

## Overview

This module allows linking Sales Orders with Internal Transfers by adding a new field in Quotations named "Internal Transfer". When an Internal Transfer in Done status is selected, the products from the Internal Transfer are automatically added to the Sales Order.

## Features

- **Internal Transfer Selection**: Add a field in Sales Order (Quotation) to select an Internal Transfer
- **Status Filtering**: Only shows Internal Transfers with "Done" status
- **Auto Product Addition**: Automatically adds products from the selected Internal Transfer to the Sales Order lines
- **Uniqueness Constraint**: Prevents selecting the same Internal Transfer in multiple Sales Orders
- **Exact Matching**: Ensures quantities and products match exactly those in the Internal Transfer

## Installation

1. Copy the module to your Odoo addons directory
2. Update the module list in Odoo
3. Install the "CDS Sale Internal Transfer" module

## Usage

1. Create or edit a Sales Order (Quotation)
2. In the Internal Transfer field, select an Internal Transfer that has "Done" status
3. The products from the selected Internal Transfer will be automatically added to the order lines
4. The system will prevent you from selecting an Internal Transfer that is already linked to another Sales Order

## Technical Details

### Model Extensions

- `sale.order`: Added `cds_internal_transfer_id` field to link with internal transfers
- Added onchange method to automatically populate order lines
- Added constraints to prevent duplicate internal transfer usage

### Dependencies

- `sale_management`: For Sales Order functionality
- `stock`: For Internal Transfer (stock.picking) functionality

## Development

**Developed by**: CDS Solutions SRL  
**Maintainers**: 
- Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
- Abdelrahman Menisy (<a.mansy@cdsegypt.com>)

**Website**: https://www.cdsegypt.com

## License

This module is licensed under LGPL-3.

## Changes by Abdelrahman Menisy

### Version 1.0 (2025-01-02)
- Initial implementation
- Added Internal Transfer field to Sales Order
- Implemented automatic product population from Internal Transfer
- Added uniqueness constraints to prevent duplicate usage
- Created comprehensive documentation
