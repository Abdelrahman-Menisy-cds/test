.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :target: https://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

Restrict Journal for Users
====================
This module helps to restrict journal for the specific users.Users can access allowed journals only

Configuration
=============
No additional configuration required

Company
-------
* `Cybrosys Techno Solutions <https://cybrosys.com/>`__

License
-------
General Public License, Version 3 (LGPL v3).
(https://www.gnu.org/licenses/lgpl-3.0-standalone.html)

Credits
-------
Developer: (V16) Sreeshanth V S @cybrosys, Contact: odoo@cybrosys.com

Contacts
--------
* Mail Contact : odoo@cybrosys.com
* Website : https://cybrosys.com

Bug Tracker
-----------
Bugs are tracked on GitHub Issues. In case of trouble, please check there if
your issue has already been reported.

Maintainer
==========
.. image:: https://cybrosys.com/images/logo.png
   :target: https://cybrosys.com

This module is maintained by Cybrosys Technologies.

For support and more information, please visit `Our Website <https://cybrosys.com/>`__

Further information
===================
HTML Description: `<static/description/index.html>`__

Odoo 19 Migration
=================
Migrated by: **Abdelrahman Menisy** (CDS Solutions SRL)

Changes Made (v19.0.1.0.0)
--------------------------
* Updated ``__manifest__.py`` with version 19.0.1.0.0 and CDS author info
* Updated ``account_payment_register.py``:
  - Replaced ``_get_batches()`` with ``batches`` property (Odoo 19 API change)
  - Added ``Command`` import for proper Many2many assignment
  - Updated ``_compute_available_journal_ids`` to use new batches iteration pattern
  - Updated ``_get_batch_available_journals`` to use ``_check_company_domain()`` method
  - Added support for ``'credit'`` journal type (new in Odoo 19)
* Updated ``account_move.py``:
  - Fixed ``_onchange_partner_id`` to call super() first without return value (Odoo 19 pattern)
* Fixed ``security/account_journal_security.xml``:
  - Removed ``category_id`` (invalid xmlid ``base.module_category_usability`` in Odoo 19)
* Fixed ``views/res_users_views.xml``:
  - Changed xpath from ``page[@name='security']`` to ``page[@name='page_security']`` (renamed in Odoo 19)

Logic Change by Abdelrahman Menisy (Dec 2024)
---------------------------------------------
* **Changed journal_ids from "Restricted" to "Allowed" logic:**
  - Previously: ``journal_ids`` stored journals the user was NOT allowed to access
  - Now: ``journal_ids`` stores journals the user IS allowed to access
  - If ``journal_ids`` is empty, user can access all journals (no restriction)
* Updated ``res_users.py``:
  - Changed field label from "Restricted Journals" to "Allowed Journals"
  - Updated help text to reflect new behavior
* Updated ``account_move.py``:
  - Inverted validation logic to check if journal is NOT in allowed list
  - Added check for empty allowed list (allows all journals)
* Updated ``account_payment_register.py``:
  - Inverted filtering logic to include only allowed journals
  - Added check for empty allowed list (shows all journals)
* Updated ``views/res_users_views.xml``:
  - Changed page title from "Restricted Journal" to "Allowed Journals"
* Updated ``security/ir_rule.xml``:
  - Changed domain from ``'not in'`` to ``'in'`` for both journal and payment rules
  - Now only journals in user's allowed list are accessible
  - Added a rule for ``account.move`` to restrict moves by allowed journals
* Added ``views/am_cds_account_move_action.xml``:
  - Created server action to dynamically filter Journal Entries by allowed journals
  - Overrode Journal Entries menu to use the filtered action
* Updated ``models/account_move.py``:
  - Added ``am_cds_action_move_journal_line()`` method for dynamic domain filtering