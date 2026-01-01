from odoo import _, api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def _load_pos_data_read(self, records, config):
        """Override to assign 'salesperson' role to sales persons instead of 'cashier'."""
        read_records = super()._load_pos_data_read(records, config)
        sale_person_ids = config.sale_persons_ids.ids
        for employee in read_records:
            if employee['id'] in sale_person_ids and employee.get('_role') == 'cashier' and not employee['id'] in config.basic_employee_ids.ids :
                employee['_role'] = 'salesperson'
        return read_records