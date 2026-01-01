# CDS POS Sales Person - Odoo 19 Upgrade Notes

## Summary
All JavaScript files have been upgraded to match Odoo 19 Point of Sale structure and API changes.

## Key Changes Made

### 1. Import Path Updates
All files updated with new Odoo 19 import paths:

- **PosStore**: `@point_of_sale/app/store/pos_store` → `@point_of_sale/app/services/pos_store`
- **SelectionPopup**: `@point_of_sale/app/utils/input_popups/selection_popup` → `@point_of_sale/app/components/popups/selection_popup/selection_popup`
- **makeAwaitable**: `@point_of_sale/app/store/make_awaitable_dialog` → `@point_of_sale/app/utils/make_awaitable_dialog`

### 2. Method Name Changes (Snake Case → Camel Case)
Updated all method calls to use camelCase convention:

- `this.pos.get_order()` → `this.pos.getOrder()`
- `order.get_selected_orderline()` → `order.getSelectedOrderline()`

### 3. ORM/Data Service Changes

#### overrides/pos_store.js
- **Replaced**: `this.env.services.orm.call()` → `this.data.searchRead()`
  - Odoo 19 uses the `data` service for ORM operations
  - Changed from `orm.call('model', 'search_read', [domain, fields])` 
  - To: `data.searchRead('model', domain, fields)`

### 4. Component Path Changes

#### Odoo 19 removed `generic_components` folder:
- **Old**: `@point_of_sale/app/generic_components/orderline/orderline`
- **New**: `@point_of_sale/app/components/orderline/orderline`

- **Old**: `@point_of_sale/app/generic_components/order_widget/order_widget`
- **New**: `@point_of_sale/app/components/order_display/order_display`

**Note**: `OrderWidget` was renamed to `OrderDisplay` in Odoo 19.

### 5. Props Validation Changes

In Odoo 19, component props are strictly validated. However, both `Orderline` and `OrderDisplay` define their main props as `Object` type:

```javascript
// Orderline
static props = {
    line: Object,  // Accepts any object with any keys
    ...
}

// OrderDisplay
static props = {
    order: Object,  // Accepts any object with any keys
    ...
}
```

**Important**: Since `line` and `order` are defined as `Object`, you **don't need to patch the props** to add custom fields like `sale_person_id` or `sale_person_name`. These fields will be automatically accepted.

**Old approach (Odoo 18 - no longer needed):**
```javascript
patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            shape: {
                sale_person_id: { optional: true },
                sale_person_name: { type: String, optional: true },
            },
        },
    },
});
```

**New approach (Odoo 19):**
```javascript
// No props patch needed!
// Just patch the prototype to add methods:
patch(Orderline.prototype, {
    async selectLineSalePerson() {
        // Access this.props.line.sale_person_id directly
    }
});
```

### 6. Files Updated

1. **orderline.js** (`static/src/app/generic_components/orderline/orderline.js`)
   - Updated `Orderline` import: `generic_components/orderline` → `components/orderline`
   - Updated `SelectionPopup` and `makeAwaitable` import paths
   - Changed `get_order()` → `getOrder()`
   - Changed `get_selected_orderline()` → `getSelectedOrderline()`

2. **order_widget.js** (`static/src/app/generic_components/order_widget/order_widget.js`)
   - Updated import: `OrderWidget` → `OrderDisplay`
   - Updated path: `generic_components/order_widget` → `components/order_display`
   - Patched `OrderDisplay` instead of `OrderWidget`

2. **control_buttons.js** (`static/src/app/screens/product_screen/control_buttons/sale_person/control_buttons.js`)
   - Updated `SelectionPopup` and `makeAwaitable` import paths
   - Changed `get_order()` → `getOrder()`

3. **pos_store.js** (`static/src/app/store/pos_store.js`)
   - Updated `PosStore` import path
   - Updated `SelectionPopup` and `makeAwaitable` import paths
   - Changed all `get_order()` → `getOrder()` calls

4. **overrides/pos_store.js** (`static/src/overrides/pos_store.js`)
   - Updated `PosStore` import path
   - **Changed ORM calls**:
     - `this.env.services.orm.call('pos.config', 'search_read', ...)` 
     - → `this.data.searchRead('pos.config', domain, fields)`
     - `this.env.services.orm.call('hr.employee', 'search_read', ...)`
     - → `this.data.searchRead('hr.employee', domain, fields)`

5. **pos_order.js** (`static/src/app/store/pos_order.js`)
   - No changes needed (already compatible)

6. **pos_orderline.js** (`static/src/app/models/pos_orderline.js`)
   - No changes needed (already compatible)

7. **ticket_screen.js** (`static/src/app/screens/ticket_screen/ticket_screen.js`)
   - No changes needed (already compatible)

8. **order_widget.js** (`static/src/app/generic_components/order_widget/order_widget.js`)
   - No changes needed (already compatible)

## Testing Recommendations

1. **Sales Person Selection**:
   - Test selecting sales person when adding first product
   - Test changing sales person for entire order
   - Test changing sales person for individual order lines
   - Verify default sales person behavior

2. **Order Validation**:
   - Test that orders cannot be paid without a sales person assigned
   - Verify error message displays correctly

3. **Refund Operations**:
   - Test that refunded orders inherit sales person from original order
   - Verify order line sales persons are copied correctly

4. **Data Loading**:
   - Verify sales persons are loaded correctly from pos.config
   - Test with multiple sales persons configured
   - Test with no sales persons configured

5. **Order Lines**:
   - Test that new order lines inherit order's sales person
   - Test changing individual line sales person
   - Verify sales person data is saved correctly

## Data Service API Changes

### Old (Odoo 18):
```javascript
const result = await this.env.services.orm.call(
    'model.name',
    'search_read',
    [[['field', '=', value]], ['field1', 'field2']],
);
```

### New (Odoo 19):
```javascript
const result = await this.data.searchRead(
    'model.name',
    [['field', '=', value]],
    ['field1', 'field2']
);
```

## Dependencies
Module depends on:
- `pos_hr` - For employee/cashier management
- `bi_pos_order_line_view` - For order line view customizations

Make sure these modules are also compatible with Odoo 19.

## XML Template Changes

### 1. sale_person.xml (Control Buttons)
**Old (Odoo 18):**
```xml
<xpath expr="//OrderlineNoteButton" position="after">
```

**New (Odoo 19):**
```xml
<!-- For main screen -->
<xpath expr="//InternalNoteButton" position="after">
    <button t-if="!props.showRemainingButtons" ...>

<!-- For modal dialog -->
<xpath expr="//t[@t-if='props.showRemainingButtons']/div/NoteButton" position="after">
```

**Reason:** `OrderlineNoteButton` no longer exists in Odoo 19. Replaced with `InternalNoteButton` and `NoteButton`.

### 2. orderline.xml
**Old (Odoo 18):**
```xml
<xpath expr="//li[hasclass('orderline')]/div[hasclass('d-flex')]//div/div[hasclass('price')]" position="after">
```

**New (Odoo 19):**
```xml
<xpath expr="//div[hasclass('product-price')]" position="after">
```

**Reason:** Orderline template structure changed in Odoo 19. The price element now uses `product-price` class.

## Known Issues / Notes

1. The module uses `afterProcessServerData()` hook which should be verified for Odoo 19 compatibility
2. Sales person data is fetched via `data.searchRead()` - ensure the fields are accessible in POS
3. The module patches multiple core POS components - test thoroughly after upgrade
4. XML templates have been updated to match Odoo 19 structure - verify button placement in UI
