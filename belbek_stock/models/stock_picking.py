from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_sale_partner_email(self):
        """Return the Shopify sale order customer's email, for the report.

        The delivery slip must show the email of the *sale order customer*
        (``sale.order.partner_id``), not the email of the address set on the
        picking itself.

        Only sale orders imported from Shopify (i.e. with ``shopify_order_id``
        set) are considered; any other linked order is ignored. A picking can
        be linked to several sale orders through its stock moves, so we look
        at every linked Shopify order in a deterministic order and return the
        first valid (non-empty, well-formed) partner email found. Returns an
        empty string when none is available.
        """
        self.ensure_one()
        # ``sale_id`` is the picking's primary order; ``move_ids.sale_line_id``
        # covers the case where moves originate from several sale orders.
        sale_orders = (self.sale_id | self.move_ids.sale_line_id.order_id)
        shopify_orders = sale_orders.filtered('shopify_order_id').sorted('id')
        for order in shopify_orders:
            email = (order.partner_id.email or '').strip()
            if '@' in email:
                return email
        return ''
