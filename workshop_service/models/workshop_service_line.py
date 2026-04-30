from odoo import models, fields, api


class WorkshopServiceLine(models.Model):
    _name = 'workshop.service.line'
    _description = 'Workshop Service Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    service_id = fields.Many2one(
        'workshop.service.order',
        string='Service Order',
        required=True,
        ondelete='cascade',
    )
    line_type = fields.Selection([
        ('labor', 'Labor / Service'),
        ('part', 'Spare Part'),
    ], string='Type', default='labor', required=True)
    product_id = fields.Many2one('product.product', string='Product / Service')
    name = fields.Char(string='Description', required=True)
    qty = fields.Float(string='Quantity', default=1.0, required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float(string='Unit Price', required=True)
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
    )

    @api.depends('qty', 'price_unit')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.qty * rec.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.display_name
            self.price_unit = self.product_id.lst_price
            self.uom_id = self.product_id.uom_id
