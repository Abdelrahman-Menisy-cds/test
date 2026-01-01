# CDS POS Security - Odoo 19 Upgrade Notes

## Summary
All JavaScript files have been upgraded to match Odoo 19 Point of Sale structure and API changes.

## Key Changes Made

### 1. Import Path Updates
All files updated with new Odoo 19 import paths:

- **usePos hook**: `@point_of_sale/app/store/pos_hook` → `@point_of_sale/app/hooks/pos_hook`
- **PosStore**: `@point_of_sale/app/store/pos_store` → `@point_of_sale/app/services/pos_store`
- **NumberPopup**: `@point_of_sale/app/utils/input_popups/number_popup` → `@point_of_sale/app/components/popups/number_popup/number_popup`
- **makeAwaitable**: `@point_of_sale/app/store/make_awaitable_dialog` → `@point_of_sale/app/utils/make_awaitable_dialog`

### 2. Method Name Changes (Snake Case → Camel Case)
Updated all method calls to use camelCase convention:

- `this.pos.get_order()` → `this.pos.getOrder()`
- `order.get_selected_orderline()` → `order.getSelectedOrderline()`
- `selectedLine.get_quantity()` → `selectedLine.getQuantity()`

### 3. API Method Changes

#### pos_store.js
- **Replaced**: `showScreen(name, props)` → `navigate(routeName, routeParams)`
  - The `showScreen` method no longer exists in Odoo 19
  - Use `navigate` method for screen navigation instead

### 4. Files Updated

1. **clear_order_line.js**
   - Updated `usePos` import path

2. **control_buttons.js**
   - Updated `NumberPopup` and `makeAwaitable` import paths
   - Note: `apply_discount` method may need verification as it doesn't exist in base Odoo 19 ControlButtons

3. **order_summary.js**
   - Updated import paths
   - Changed `get_order()` → `getOrder()`
   - Changed `get_selected_orderline()` → `getSelectedOrderline()`
   - Changed `get_quantity()` → `getQuantity()`

4. **pos_store.js**
   - Updated `PosStore` import path
   - Updated `NumberPopup` and `makeAwaitable` import paths
   - Replaced `showScreen()` with `navigate()` method

5. **product_screen.js**
   - Updated import paths
   - Changed `get_order()` → `getOrder()`
   - Changed `get_selected_orderline()` → `getSelectedOrderline()`
   - Changed `get_quantity()` → `getQuantity()`

6. **ticket_screen.js**
   - Updated `NumberPopup` and `makeAwaitable` import paths

## Testing Recommendations

1. Test all password-protected features:
   - Pricelist changes
   - Fiscal position changes
   - Global discount application
   - Price modifications
   - Discount modifications
   - Order line deletion
   - Negative quantity (sign change)
   - Ticket screen access
   - Order deletion
   - Refund operations

2. Verify that password popups display correctly
3. Test that incorrect passwords are properly rejected
4. Ensure all security restrictions work as expected

## Potential Issues to Watch

1. The `apply_discount` method in `control_buttons.js` doesn't exist in base Odoo 19 ControlButtons. This might be:
   - From the `pos_discount` module dependency
   - A custom method that needs to be verified
   - May need additional updates depending on the discount module implementation

2. Ensure all async/await patterns work correctly with the new structure

## Dependencies
Module depends on:
- `point_of_sale`
- `pos_discount`
- `cds_pos_discount_reason`

Make sure these modules are also compatible with Odoo 19.
