from odoo import models, fields, api, _


class HostelService(models.Model):
    _name = 'hostel.service'
    _description = 'Hostel Service'
    _order = 'name'

    name = fields.Char(string='Service Name', required=True)
    service_type = fields.Selection([
        ('food', 'Food'),
        ('laundry', 'Laundry'),
        ('cleaning', 'Cleaning'),
        ('wifi', 'WiFi'),
        ('other', 'Other'),
    ], string='Service Type', required=True)
    description = fields.Text(string='Description')
    price = fields.Float(string='Price', required=True)
    price_type = fields.Selection([
        ('one_time', 'One Time'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string='Price Type', required=True, default='monthly')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)
