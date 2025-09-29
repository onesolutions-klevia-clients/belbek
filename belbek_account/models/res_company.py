from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    ch_qr_name = fields.Char(related="partner_id.ch_qr_name", store=True, readonly=False, inverse="_inverse_ch_qr_name")

    def _inverse_ch_qr_name(self):
        for company in self:
            if company.partner_id:
                company.partner_id.ch_qr_name = company.ch_qr_name
