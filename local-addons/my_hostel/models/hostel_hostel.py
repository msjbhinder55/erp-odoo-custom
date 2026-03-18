from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HostelHostel(models.Model):
    _name = 'hostel.hostel'
    _description = 'Hostel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Hostel Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    warden_id = fields.Many2one('res.partner', string='Warden', domain=[
                                ('is_warden', '=', True)])
    total_rooms = fields.Integer(
        string='Total Rooms', compute='_compute_room_stats', store=True)
    occupied_rooms = fields.Integer(
        string='Occupied Rooms', compute='_compute_room_stats', store=True)
    available_rooms = fields.Integer(
        string='Available Rooms', compute='_compute_room_stats', store=True)
    room_ids = fields.One2many('hostel.room', 'hostel_id', string='Rooms')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company)

    @api.depends('room_ids', 'room_ids.state')
    def _compute_room_stats(self):
        for hostel in self:
            rooms = hostel.room_ids
            hostel.total_rooms = len(rooms)
            hostel.occupied_rooms = len(
                rooms.filtered(lambda r: r.state == 'occupied'))
            hostel.available_rooms = len(
                rooms.filtered(lambda r: r.state == 'available'))

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError(
                    _('Phone number must contain only digits.'))

    _sql_constraints = [
        ('unique_hostel_code', 'unique(code)', 'Hostel code must be unique!'),
    ]
