# CDS POS Pricelist Discount

## Overview

This module allows you to configure a separate discount pricelist on POS configuration. When products are added to the order, discounts from the discount pricelist are automatically applied based on the pricelist rules.

## Features

- **Discount Pricelist Configuration**: Configure a discount pricelist per POS config
- **Auto-Apply Discounts**: Automatically apply percentage discounts from pricelist rules when adding products
- **Discount Tracking**: Track total discount amount and total without discount on orders
- **Bulk Product Wizard**: Add multiple products to a pricelist with discount using a wizard

## Installation

1. Copy the module to your custom addons folder
2. Update the apps list in Odoo
3. Install the module from Apps menu

## Configuration

1. Go to **Point of Sale > Configuration > Settings**
2. Select your POS configuration
3. In the **Pricing** section, find **Discount Pricelist**
4. Select the pricelist that contains your discount rules

## Usage

### Setting up Discount Rules

1. Go to **Sales > Products > Pricelists**
2. Open or create a pricelist for discounts
3. Click **Add Products (Discount)** button to bulk add products with discount
4. Or manually add pricelist items with percentage discount

### In POS

When a product is added to the order:
- The system checks if there's a discount pricelist configured
- If a matching rule exists for the product with percentage discount, it's automatically applied
- The discount is applied only on the first occurrence of the product in the order

## Technical Details

### Models Extended

- `pos.config`: Added `discount_pricelist_id` field
- `pos.order`: Added `total_discount_amount`, `total_without_discount`, `discount_pricelist_id` fields
- `pos.order.line`: Added `discount_amount` computed field
- `res.config.settings`: Added `pos_discount_pricelist_id` related field

### JavaScript Components

- Patched `PosOrderline.setUnitPrice()` to apply discounts from discount pricelist

## Version History

### 19.0.1.0.0
**Upgraded by: Abdelrahman Menisy**

Changes made for Odoo 19 compatibility:
- Removed deprecated `_order_fields` method (not used in Odoo 19)
- Added `_load_pos_data_fields` method for loading custom fields in POS
- Updated JavaScript to use Odoo 19 model system (`setUnitPrice` instead of `set_unit_price`)
- Replaced deprecated `attrs` attribute with direct `invisible`/`required`/`readonly` attributes in XML views
- Updated manifest with proper versioning and metadata

## Dependencies

- `point_of_sale`

## License

OPL-1 (Odoo Proprietary License v1.0)

## Authors

- **CDS Solutions SRL** - [https://www.cdsegypt.com](https://www.cdsegypt.com)

### Contributors

- Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>)
- Abdelrahman Menisy (<a.mansy@cdsegypt.com>)
- Ragab Deaf (<ragabdeaf93@outlook.com>)
