from odoo import api, fields, models, _


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    name = fields.Char(translate=True)
