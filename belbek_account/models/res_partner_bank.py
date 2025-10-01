from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    def _l10n_ch_get_qr_vals(self, amount, currency, debtor_partner, free_communication, structured_communication):
        res = super()._l10n_ch_get_qr_vals(amount, currency, debtor_partner, free_communication, structured_communication)
        if self.partner_id.ch_qr_name:
            res[5] = self.partner_id.ch_qr_name[:70]
        return res
