from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class WorkshopService(models.Model):
    _name = 'workshop.service'
    _description = 'Workshop Service Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        default='New',
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partners',
        string='Customer',
        required=True,
        tracking=True,
    )
    vehicle_name = fields.Char(string='Vehicle / Equipment', required=True)
    license_plate = fields.Char(string='License Plate / Serial No.')
    technician_id = fields.Many2one(
        'res.users',
        string='Technician',
        tracking=True,
    )
    date_start = fields.Date(string='Service Date', default=fields.Date.today, required=True)
    date_end = fields.Date(string='Estimated End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)

    line_ids = fields.One2many('workshop.service.line', 'service_id', string='Service Lines')

    total_amount = fields.Float(
        string='Subtotal',
        compute='_compute_total_amount',
        store=True,
    )
    amount_tax = fields.Float(
        string='Tax (11%)',
        compute='_compute_amount_tax',
        store=True,
    )
    amount_total = fields.Float(
        string='Grand Total',
        compute='_compute_amount_total',
        store=True,
    )
    duration_days = fields.Integer(
        string='Duration (Days)',
        compute='_compute_duration_days',
        store=True,
    )

    sale_order_id = fields.Many2one(
        'sale.order', string='Related Sale Order', readonly=True, copy=False,
    )
    picking_id = fields.Many2one(
        'stock.picking', string='Related Picking', readonly=True, copy=False,
    )
    notes = fields.Text(string='Internal Notes')

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        pass

    @api.depends('total_amount')
    def _compute_amount_tax(self):
        for rec in self:
            rec.amount_tax = rec.total_amount * 1.11

    @api.depends('total_amount', 'amount_tax')
    def _compute_amount_total(self):
        for rec in self:
            rec.amount_total = rec.total_amount + rec.amount_tax

    @api.depends('date_start', 'date_end')
    def _compute_duration_days(self):
        if self.date_start and self.date_end:
            self.duration_days = (self.date_end - self.date_start).days
        else:
            self.duration_days = 0

    def action_confirm(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError('Cannot confirm: please add at least one service line.')
            rec.state = 'confirmed'

    def action_start(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError('Only confirmed orders can be started.')
            rec.state = 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'done':
                raise UserError('Cannot cancel a completed service order.')
            rec.state = 'cancelled'

    def action_reset_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError('Only cancelled orders can be reset to draft.')
            rec.state = 'draft'

    def action_create_sale_order(self):
        self.ensure_one()
        raise NotImplementedError('Implementasikan method ini.')

    def action_create_picking(self):
        self.ensure_one()
        raise NotImplementedError('Implementasikan method ini.')
