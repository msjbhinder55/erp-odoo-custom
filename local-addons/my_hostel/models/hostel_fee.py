from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HostelFee(models.Model):
    _name = 'hostel.fee'
    _description = 'Hostel Fee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'due_date desc, id desc'

    name = fields.Char(string='Fee Description', required=True)
    student_id = fields.Many2one(
        'hostel.student', string='Student', required=True, tracking=True)
    allocation_id = fields.Many2one('hostel.allocation', string='Allocation')
    fee_type = fields.Selection([
        ('rent', 'Rent'),
        ('deposit', 'Deposit'),
        ('food', 'Food'),
        ('laundry', 'Laundry'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ], string='Fee Type', required=True, default='rent')
    amount = fields.Float(string='Amount', required=True, tracking=True)
    paid_amount = fields.Float(string='Paid Amount', default=0.0)
    due_amount = fields.Float(
        string='Due Amount', compute='_compute_due_amount', store=True)
    paid = fields.Boolean(string='Paid', compute='_compute_paid', store=True)
    due_date = fields.Date(string='Due Date', required=True)
    payment_date = fields.Date(string='Payment Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    @api.depends('amount', 'paid_amount')
    def _compute_due_amount(self):
        for fee in self:
            fee.due_amount = fee.amount - fee.paid_amount

    @api.depends('due_amount')
    def _compute_paid(self):
        for fee in self:
            fee.paid = fee.due_amount <= 0

    @api.constrains('amount', 'paid_amount')
    def _check_amounts(self):
        for fee in self:
            if fee.paid_amount > fee.amount:
                raise ValidationError(
                    _('Paid amount cannot exceed total amount!'))

    def action_confirm(self):
        self.state = 'confirmed'

    def action_paid(self):
        self.state = 'paid'
        self.payment_date = fields.Date.today()

    def action_cancel(self):
        self.state = 'cancelled'

    def action_register_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Register Payment',
            'res_model': 'hostel.fee.payment.wizard',
            'view_mode': 'form',
            'context': {
                'default_fee_id': self.id,
                'default_amount': self.due_amount,
            },
            'target': 'new',
        }
