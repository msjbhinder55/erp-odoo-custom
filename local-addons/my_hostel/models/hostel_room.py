from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = 'Hostel Room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'
    _order = 'hostel_id, room_number'

    hostel_id = fields.Many2one(
        'hostel.hostel', string='Hostel', required=True, tracking=True)
    room_number = fields.Char(string='Room Number', required=True)
    floor = fields.Integer(string='Floor', default=0)
    capacity = fields.Integer(string='Capacity', required=True, default=2)
    current_occupancy = fields.Integer(
        string='Current Occupancy', compute='_compute_occupancy', store=True)
    available_beds = fields.Integer(
        string='Available Beds', compute='_compute_occupancy', store=True)
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('dormitory', 'Dormitory'),
    ], string='Room Type', required=True, default='double')
    price_per_bed = fields.Float(string='Price per Bed', required=True)
    facilities = fields.Text(string='Facilities')
    state = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Fully Occupied'),
        ('maintenance', 'Under Maintenance'),
    ], string='Status', default='available', tracking=True)
    allocation_ids = fields.One2many(
        'hostel.allocation', 'room_id', string='Allocations')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    display_name = fields.Char(
        string='Display Name', compute='_compute_display_name', store=True)

    @api.depends('room_number', 'hostel_id')
    def _compute_display_name(self):
        for room in self:
            room.display_name = f"[{room.hostel_id.code}] {room.room_number}"

    @api.depends('allocation_ids', 'allocation_ids.state', 'capacity')
    def _compute_occupancy(self):
        for room in self:
            active_allocations = room.allocation_ids.filtered(
                lambda a: a.state == 'active')
            room.current_occupancy = len(active_allocations)
            room.available_beds = room.capacity - room.current_occupancy
            if room.current_occupancy >= room.capacity:
                room.state = 'occupied'
            elif room.state != 'maintenance':
                room.state = 'available'

    @api.constrains('capacity', 'current_occupancy')
    def _check_capacity(self):
        for room in self:
            if room.current_occupancy > room.capacity:
                raise ValidationError(
                    _('Current occupancy cannot exceed room capacity!'))

    @api.constrains('floor')
    def _check_floor(self):
        for room in self:
            if room.floor < 0:
                raise ValidationError(_('Floor number cannot be negative!'))

    _sql_constraints = [
        ('unique_room_per_hostel', 'unique(hostel_id, room_number)',
         'Room number must be unique per hostel!'),
    ]
