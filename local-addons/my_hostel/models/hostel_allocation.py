from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class HostelAllocation(models.Model):
    _name = 'hostel.allocation'
    _description = 'Hostel Room Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'
    _order = 'start_date desc, id desc'

    student_id = fields.Many2one(
        'hostel.student', string='Student', required=True, tracking=True)
    room_id = fields.Many2one(
        'hostel.room', string='Room', required=True, tracking=True)
    bed_number = fields.Integer(string='Bed Number')
    start_date = fields.Date(
        string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    fee_ids = fields.One2many('hostel.fee', 'allocation_id', string='Fees')
    total_fee = fields.Float(
        string='Total Fee', compute='_compute_total_fee', store=True)
    paid_amount = fields.Float(
        string='Paid Amount', compute='_compute_paid_amount', store=True)
    due_amount = fields.Float(
        string='Due Amount', compute='_compute_due_amount', store=True)
    notes = fields.Text(string='Notes')
    display_name = fields.Char(
        string='Display Name', compute='_compute_display_name', store=True)

    @api.depends('student_id', 'room_id', 'start_date')
    def _compute_display_name(self):
        for alloc in self:
            alloc.display_name = f"{alloc.student_id.name} - {alloc.room_id.display_name}"

    @api.depends('fee_ids', 'fee_ids.amount')
    def _compute_total_fee(self):
        for alloc in self:
            alloc.total_fee = sum(alloc.fee_ids.mapped('amount'))

    @api.depends('fee_ids', 'fee_ids.paid_amount')
    def _compute_paid_amount(self):
        for alloc in self:
            alloc.paid_amount = sum(alloc.fee_ids.mapped('paid_amount'))

    @api.depends('total_fee', 'paid_amount')
    def _compute_due_amount(self):
        for alloc in self:
            alloc.due_amount = alloc.total_fee - alloc.paid_amount

    @api.constrains('bed_number', 'room_id')
    def _check_bed_number(self):
        for alloc in self:
            if alloc.bed_number and alloc.room_id:
                if alloc.bed_number > alloc.room_id.capacity:
                    raise ValidationError(
                        _('Bed number cannot exceed room capacity!'))
                # Check if bed is already occupied
                existing = self.search([
                    ('room_id', '=', alloc.room_id.id),
                    ('bed_number', '=', alloc.bed_number),
                    ('state', 'in', ['confirmed', 'active']),
                    ('id', '!=', alloc.id)
                ])
                if existing:
                    raise ValidationError(
                        _('Bed number %s in this room is already occupied!') % alloc.bed_number)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for alloc in self:
            if alloc.start_date and alloc.end_date:
                if alloc.start_date > alloc.end_date:
                    raise ValidationError(
                        _('Start date cannot be after end date!'))

    def action_confirm(self):
        self.state = 'confirmed'

    def action_activate(self):
        self.state = 'active'

    def action_complete(self):
        self.state = 'completed'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_create_fee(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Fee',
            'res_model': 'hostel.fee',
            'view_mode': 'form',
            'context': {
                'default_allocation_id': self.id,
                'default_student_id': self.student_id.id,
                'default_amount': self.room_id.price_per_bed,
            },
            'target': 'new',
        }
