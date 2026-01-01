# CDS POS Updates

# Copyright (c) 2021 CDS Solutions SRL. (http://cdsegypt.com)
#
# Maintainer: Eng.Ramadan Khalil (<ramadan.khalil@cdsegypt.com>),Abdelrahman Menisy (<a.mansy@cdsegypt.com>) ,
# It is forbidden to publish, distribute, sublicense, or sell copies
# of the Software or modified copies of the Software.

## Overview

This module extends the Odoo Point of Sale (POS) functionality with various CDS-specific customizations and improvements.

## Features

### 1. Show/Hide Invoice Button
- **Purpose**: Control the visibility of the Invoice button on the POS payment screen.
- **Configuration**: Go to **Point of Sale > Configuration > Settings** and look for the "Show/Hide Invoice Button" option in the **PoS Interface** section.
- **Behavior**: 
  - When enabled (checked): The Invoice button is visible on the payment screen, allowing users to create invoices for orders.
  - When disabled (unchecked): The Invoice button is hidden from the payment screen.
- **Default**: Enabled (button is visible by default).

### 2. Refund Period Setting
- **Purpose**: Set the number of days within which refunds can be processed.
- **Configuration**: In POS settings, set the "POS Refund Period" field.
- **Default**: 14 days.

### 3. Load Orders of Last Days
- **Purpose**: Control how many days of historical orders to load in the POS.
- **Configuration**: Enable "Load Orders of Last Days" and specify the number of days.
- **Default**: Disabled.

### 4. Refund Payment Method Auto-Selection
- **Purpose**: Automatically selects the original payment method when processing a refund.
- **Behavior**: When a refund is initiated, the system automatically uses the original order's payment method if available in the current POS configuration.

### 5. Custom Order Receipt
- **Purpose**: Customized order receipt format for CDS requirements.

### 6. Closing Popup Customizations
- **Purpose**: Enhanced closing control popup with additional features.

## Technical Details

### Models Extended
- `pos.config`: Added fields for invoice button visibility, refund period, and order loading configuration.
- `res.config.settings`: Added related fields for POS configuration settings.

### New Fields
| Model | Field Name | Type | Description |
|-------|------------|------|-------------|
| `pos.config` | `show_invoice_button` | Boolean | Controls Invoice button visibility |
| `pos.config` | `refund_period` | Integer | Days allowed for refund processing |
| `pos.config` | `enable_load_pos_orders_days` | Boolean | Enable order loading by days |
| `pos.config` | `load_pos_orders_days` | Integer | Number of days to load orders |

### Frontend Overrides
- `payment_screen.xml`: Conditionally displays/hides the Invoice button based on configuration.
- `payment_screen.js`: Auto-selects original payment method for refunds.
- `closing_popup.xml`: Customized closing popup.
- `order_receipt.xml`: Custom receipt template.

## Dependencies
- `pos_hr`
- `pos_sale`
- `pos_discount`
- `pos_loyalty`

## Configuration

1. Navigate to **Point of Sale > Configuration > Settings**.
2. Select your Point of Sale from the dropdown.
3. Scroll to the **PoS Interface** section.
4. Configure the following settings as needed:
   - **Show/Hide Invoice Button**: Toggle the visibility of the invoice button.
   - **POS Refund Period**: Set the refund period in days.
   - **POS Load Order Days**: Enable and configure historical order loading.

## Version

- Module Version: 0.1
- Compatible with: Odoo 19.0

## Support

For support, please contact:
- Website: [https://www.cdsegypt.com](https://www.cdsegypt.com)
- Email: support@cdsegypt.com
