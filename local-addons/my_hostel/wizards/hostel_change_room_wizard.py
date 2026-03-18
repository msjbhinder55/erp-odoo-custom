from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HostelChangeRoomWizard(models.TransientModel):
    _name = 'hostel.change.room.wizard'
    _description = 'Change Room Wizard'

    allocation_id = fields.Many2one('hostel.allocation', string='Current Allocation', required=True)
    student_id = fields.Many2one(related='allocation_id.student_id', string='Student', readonly=True)
    current_room_id = fields.Many2one(related='allocation_id.room_id', string='Current Room', readonly=True)
    new_room_id = fields.Many2one('hostel.room', string='New Room', required=True, 
                                  domain="[('state', '=', 'available'), ('id', '!=', current_room_id)]")
    new_bed_number = fields.Integer(string='New Bed Number')
    change_date = fields.Date(string='Change Date', required=True, default=fields.Date.today)
    reason = fields.Text(string='Reason')

    @api.constrains('new_bed_number', 'new_room_id')
    def _check_bed_number(self):
        for wizard in self:
            if wizard.new_bed_number:
                if wizard.new_bed_number > wizard.new_room_id.capacity:
                    raise ValidationError(_('Bed number cannot exceed room capacity!'))
                # Check if bed is available
                existing = self.env['hostel.allocation'].search([
                    ('room_id', '=', wizard.new_room_id.id),
                    ('bed_number', '=', wizard.new_bed_number),
                    ('state', 'in', ['confirmed', 'active']),
                ])
                if existing:
                    raise ValidationError(_('Bed number %s in this room is already occupied!') % wizard.new_bed_number)

    def action_change_room(self):
        self.ensure_one()
        # End current allocation
        self.allocation_id.write({
            'end_date': self.change_date,
            'state': 'completed'
        })
        
        # Create new allocation
        new_allocation = self.env['hostel.allocation'].create({
            'student_id': self.student_id.id,
            'room_id': self.new_room_id.id,
            'bed_number': self.new_bed_number,
            'start_date': self.change_date,
            'state': 'active',
            'notes': f"Room changed from {self.current_room_id.display_name}. Reason: {self.reason or 'Not specified'}"
        })
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Allocation',
            'res_model': 'hostel.allocation',
            'res_id': new_allocation.id,
            'view_mode': 'form',
            'target': 'current',
        }