from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    # def create(self, vals_list):
    #     res = super(AccountMove, self).create(vals_list)
    #     if res.ref and res.ref.startswith('pos_order_'):
    #         pos_order_id = int(res.ref.split('_')[1])
    #         pos_order = self.env['pos.order'].browse(pos_order_id)
    #         if pos_order:
    #             res.line_ids.analytic_distribution = {pos_order.analytic_account_id.id: 100.0}
            
    #     return res