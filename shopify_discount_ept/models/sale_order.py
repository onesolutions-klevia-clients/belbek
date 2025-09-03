from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def shopify_set_tax_in_sale_order_line(self, instance, line, order_response, is_shipping, is_discount,
                                           previous_line, order_line_vals, is_duties):
        """
        This Method is used to add the discount percent to sale order line.
        """
        order_line = super(SaleOrder, self).shopify_set_tax_in_sale_order_line(instance, line, order_response,
                                                                               is_shipping, is_discount, previous_line,
                                                                               order_line_vals, is_duties)
        if line.get('discount_allocations'):
            discount = sum([float(disc.get('amount')) for disc in line.get('discount_allocations', {})])
            discount_percent = discount / (
                    (float(order_line.get('price_unit')) * float(order_line.get('product_uom_qty'))) / 100)
            order_line.update({'discount': discount_percent})

        return order_line

    def shopify_create_sale_order_line(self, line, product, quantity, product_name, price, order_response,
                                       is_shipping=False, previous_line=False, is_discount=False, is_duties=False):
        """
        This Method is used for stopping creation of discount line
        """
        if is_discount:
            return False
        return super(SaleOrder, self).shopify_create_sale_order_line(line, product, quantity, product_name, price,
                                                                     order_response, is_shipping, previous_line,
                                                                     is_discount, is_duties)
