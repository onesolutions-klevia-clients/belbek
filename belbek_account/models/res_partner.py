from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    ch_qr_name = fields.Char("Name on QR")
