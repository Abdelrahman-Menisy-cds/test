# CDS Sale Internal Transfer Link

## Overview

This module provides functionality to link Sales Orders with Internal Transfers in Odoo. It allows users to select an Internal Transfer and automatically populate the Sales Order with products from that transfer.

## Features

- **Internal Transfer Field**: Adds a new field in Sales Orders (Quotations) to select Internal Transfers
- **Status Filtering**: Only shows Internal Transfers with "Done" status
- **Auto-population**: Automatically adds products from the selected Internal Transfer to the Sales Order
- **Duplicate Prevention**: Prevents selecting the same Internal Transfer in multiple Sales Orders
- **Quantity Matching**: Ensures quantities and products match exactly those in the Internal Transfer
- **Validation**: Validates that the Internal Transfer is in Done state before confirming the Sales Order

## Technical Details

### Added Fields

- `internal_transfer_id`: Many2one field linking to `stock.picking` model
  - Domain: Only shows Internal Transfers (`picking_type_code = 'internal'`) with Done state
  - Readonly after order confirmation
  - Tracked for changes

### Business Logic

1. **On Change**: When an Internal Transfer is selected, the system automatically:
   - Clears existing order lines
   - Adds new lines for each product move in the Internal Transfer
   - Uses product list price as unit price
   - Maintains exact quantities from the transfer

2. **Constraints**:
   - Each Internal Transfer can only be linked to one active Sales Order
   - Internal Transfer must be in Done state to be selected
   - Cannot change Internal Transfer after order confirmation

3. **Validation**:
   - Checks Internal Transfer state before order confirmation
   - Ensures Internal Transfer has product moves

### Views Modified

- **Sales Order Form**: Added Internal Transfer field after Order Date
- **Sales Order Tree**: Added Internal Transfer column (optional)
- **Search View**: Added filters for With/Without Internal Transfer and grouping option

## Installation

1. Copy the module to your Odoo addons directory
2. Update the module list in Odoo
3. Install the module from Apps menu

## Usage

1. Create or edit a Sales Order (Quotation)
2. Select an Internal Transfer from the dropdown (only Done transfers are shown)
3. Products from the Internal Transfer will be automatically added to the order
4. Review and confirm the Sales Order

## Dependencies

- `sale`: Sales Management
- `stock`: Inventory Management

## Compatibility

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

### Version 1.0 (2025-01-02)
- Initial implementation of Sales Order and Internal Transfer linking
- Added auto-population of products from Internal Transfer
- Implemented validation and constraints
- Created custom views for better user experience
