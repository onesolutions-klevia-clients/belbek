from odoo.tests.common import TransactionCase


class TestStockPickingSaleEmail(TransactionCase):
    """Tests for stock.picking._get_sale_partner_email."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'type': 'consu',
        })
        cls.partner_no_email = cls.env['res.partner'].create({
            'name': 'Partner Without Email',
        })
        cls.partner_a = cls.env['res.partner'].create({
            'name': 'Partner A',
            'email': 'partner.a@example.com',
        })
        cls.partner_b = cls.env['res.partner'].create({
            'name': 'Partner B',
            'email': 'partner.b@example.com',
        })
        warehouse = cls.env['stock.warehouse'].search([], limit=1)
        cls.picking_type_out = warehouse.out_type_id
        cls.stock_location = warehouse.lot_stock_id
        cls.customer_location = cls.env.ref('stock.stock_location_customers')

    def _create_sale_order(self, partner):
        return self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
            })],
        })

    def _create_picking(self, sale_orders):
        """Create an outgoing picking with one move per sale order line."""
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
        })
        for order in sale_orders:
            line = order.order_line[0]
            self.env['stock.move'].create({
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'product_uom': self.product.uom_id.id,
                'picking_id': picking.id,
                'location_id': self.stock_location.id,
                'location_dest_id': self.customer_location.id,
                'sale_line_id': line.id,
            })
        return picking

    def test_single_sale_order_email(self):
        """The email of the sole linked sale order's customer is returned."""
        order = self._create_sale_order(self.partner_a)
        picking = self._create_picking(order)
        self.assertEqual(picking._get_sale_partner_email(), 'partner.a@example.com')

    def test_first_valid_email_across_orders(self):
        """With several linked orders, the first valid partner email wins.

        The first order (by id) has a partner without email, so the second
        order's partner email must be returned.
        """
        order_1 = self._create_sale_order(self.partner_no_email)
        order_2 = self._create_sale_order(self.partner_b)
        picking = self._create_picking(order_1 | order_2)
        self.assertEqual(picking._get_sale_partner_email(), 'partner.b@example.com')

    def test_no_email_returns_empty_string(self):
        """When no linked customer has an email, an empty string is returned."""
        order = self._create_sale_order(self.partner_no_email)
        picking = self._create_picking(order)
        self.assertEqual(picking._get_sale_partner_email(), '')
