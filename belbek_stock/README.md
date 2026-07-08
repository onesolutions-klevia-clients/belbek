# Belbek - Stock

Belbek-specific customisations for the Inventory (`stock`) module.

## Role

Adds the sale order customer's email to the delivery slip PDF
(`stock.report_delivery_document`), in the *Information* section, next to the
`Order` / `Shipping Date` fields.

The email shown is that of the **sale order customer**
(`sale.order.partner_id`) — **not** the email of the address set on the
picking itself. When a picking is linked to several sale orders (through its
stock moves), the first valid (non-empty, well-formed) customer email found,
in ascending sale order id order, is displayed.

This works with both the standard delivery slip layout and the DIN 5008
layout, since the field is added to the shared document body
(`stock.report_delivery_document`) rather than to a layout-specific template.

## Dependencies

- `sale_stock` — provides the `stock.picking.sale_id` field and the
  `stock.move.sale_line_id` link used to resolve the linked sale orders.

## Key models / methods

- `stock.picking._get_sale_partner_email()` — resolves the linked sale orders
  and returns the first valid customer email, or an empty string.

## Version history

- `18.0.1.0.0` — initial release: display the linked sale order customer's
  email in the delivery slip Information section.
