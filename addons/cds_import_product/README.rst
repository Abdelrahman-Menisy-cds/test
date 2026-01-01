CDS Import Product
==================

This module provides a wizard to import products and variants from an Excel file.

Features
========

- Import product templates and variants from XLSX
- Create/update product attributes and values
- Create/update POS categories and product categories mapping

Odoo 19 Updates
===============

Updated by: **Abdelrahman Menisy** (CDS Solutions SRL)

Changes
-------

- Import wizard fixes (``wizard/import_product_wizard.py``):

  - Made mandatory columns:

    - Template Code
    - Template Name
    - Product Category Code

  - Category lookup now prioritizes category **code** (fallback to name if needed).
  - Fixed POS categories write to avoid passing ``None`` to many2many commands.
  - Fixed variant matching so empty Color/Size does not match any variant by accident.
  - Forced variant generation and proper variant resolution during import:

    - Call ``product.template._create_variant_ids()`` after attribute lines updates.
    - Resolve/update variants using the template combination (supports dynamic variants).
  - Prevented newly-generated variants from being auto-archived when Variant Code is empty:

    - Only write ``default_code`` when provided.
    - Only archive variants with missing ``default_code`` when the import file contains variant codes.

- Enforced **Variant Code** uniqueness (variant internal reference) on ``product.product.default_code`` to prevent duplicated variant codes during manual creation and imports.

- Related fix in another addon (required for imports that generate many variants):

  - ``product_barcode/models/product_product.py`` was patched to support batch variant creation by switching to ``@api.model_create_multi``.
