from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_sale_partner_email(self):
        """Return the customer email of the linked sale order, for the report.

        The delivery slip must show the email of the *sale order customer*
        (``sale.order.partner_id``), not the email of the address set on the
        picking itself.

        A picking can be linked to several sale orders through its stock
        moves. We therefore look at every linked sale order in a deterministic
        order and return the first valid (non-empty, well-formed) partner
        email found. Returns an empty string when none is available.
        """
        self.ensure_one()
        # ``sale_id`` is the picking's primary order; ``move_ids.sale_line_id``
        # covers the case where moves originate from several sale orders.
        sale_orders = (self.sale_id | self.move_ids.sale_line_id.order_id).sorted('id')
        for order in sale_orders:
            email = (order.partner_id.email or '').strip()
            if '@' in email:
                return email
        return ''
