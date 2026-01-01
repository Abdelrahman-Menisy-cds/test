# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'


    def _load_pos_data_models(self, config_id):
        res = super()._load_pos_data_models(config_id)
        if 'hr.employee' not in res:
            res.append('hr.employee')
        return res
    # def _load_pos_data(self,data):
    #     """Load POS data and add `res_users` to the response dictionary.
    #     return: A dictionary containing the POS data.
    #     """
    #     res = super()._load_pos_data(data)
    #     # if self.config_id.module_pos_hr:
    #     # dict has id and name of each sale person
    #     res['data'][0]['sale_persons'] = self.env['hr.employee'].search_read([('id', 'in', self.config_id.sale_persons_ids.ids)],fields=['id','name'])
        
    #     return res


    # def _get_pos_ui_hr_employee_sales_persons(self, params):

    #     employees_data = self.env['hr.employee'].search_read(**params['search_params'])

    #     return employees_data

    # def _pos_ui_models_to_load(self):
    #     result = super()._pos_ui_models_to_load()
    #     if self.config_id.module_pos_hr:
    #         new_model = 'hr.employee.sales.persons'
    #         if new_model not in result:
    #             result.append(new_model)
    #     return result

    # def _loader_params_hr_employee_sales_persons(self):
    #     sale_persons_ids = self.config_id.sale_persons_ids.ids
    #     return {'search_params': {'domain': [('id', 'in', sale_persons_ids)], 'fields': ['name', 'id', 'salesperson_name'], 'load': False}}

    # def _loader_params_hr_employee(self):
    #     res = super()._loader_params_hr_employee()
    #     res['search_params']['fields'].extend(['salesperson_name'])
    #     return res
        