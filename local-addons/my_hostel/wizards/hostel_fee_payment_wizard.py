from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HostelFeePaymentWizard(models.TransientModel):
    _name = 'hostel.fee.payment.wizard'
    _description = 'Fee Payment Wizard'

    fee_id = fields.Many2one('hostel.fee', string='Fee', required=True)
    amount = fields.Float(string='Payment Amount', required=True)
    payment_date = fields.Date(
        string='Payment Date', required=True, default=fields.Date.today)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
        ('cheque', 'Cheque'),
    ], string='Payment Method', required=True)
    reference = fields.Char(string='Reference')
    notes = fields.Text(string='Notes')

    @api.constrains('amount')
    def _check_amount(self):
        for wizard in self:
            if wizard.amount <= 0:
                raise ValidationError(_('Payment amount must be positive!'))
            if wizard.amount > wizard.fee_id.due_amount:
                raise ValidationError(
                    _('Payment amount cannot exceed due amount!'))

    def action_register_payment(self):
        self.ensure_one()

        # Update fee
        new_paid = self.fee_id.paid_amount + self.amount
        self.fee_id.write({
            'paid_amount': new_paid,
            'payment_date': self.payment_date if new_paid >= self.fee_id.amount else False,
            'state': 'paid' if new_paid >= self.fee_id.amount else 'confirmed',
        })

        # Create payment record (optional - you could create an account.move if using accounting)

        return {'type': 'ir.actions.act_window_close'}
