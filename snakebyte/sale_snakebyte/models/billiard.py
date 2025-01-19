from odoo import models, fields, api


class Billiard(models.Model):
    _inherit = ['avatar.mixin', 'mail.thread', 'mail.activity.mixin']
    _name = "billiard"

    owner_id = fields.Many2one('res.partner', string="Owner")
    name = fields.Char(readonly=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('billiard', sequence_date=fields.datetime.now())
