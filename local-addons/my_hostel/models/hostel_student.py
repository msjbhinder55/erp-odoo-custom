from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re


class HostelStudent(models.Model):
    _name = 'hostel.student'
    _description = 'Hostel Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Student Name', required=True, tracking=True)
    student_id = fields.Char(string='Student ID', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Contact', domain=[
                                 ('is_student', '=', True)])
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    course = fields.Char(string='Course/Department')
    year_of_study = fields.Integer(string='Year of Study')
    allocation_ids = fields.One2many(
        'hostel.allocation', 'student_id', string='Allocations')
    current_allocation_id = fields.Many2one('hostel.allocation', string='Current Allocation',
                                            compute='_compute_current_allocation', store=True)
    active = fields.Boolean(string='Active', default=True)
    notes = fields.Text(string='Notes')

    @api.depends('date_of_birth')
    def _compute_age(self):
        for student in self:
            if student.date_of_birth:
                today = fields.Date.today()
                age = today.year - student.date_of_birth.year
                if today.month < student.date_of_birth.month or \
                   (today.month == student.date_of_birth.month and today.day < student.date_of_birth.day):
                    age -= 1
                student.age = age
            else:
                student.age = 0

    @api.depends('allocation_ids', 'allocation_ids.state')
    def _compute_current_allocation(self):
        for student in self:
            active_allocation = student.allocation_ids.filtered(
                lambda a: a.state in ['active', 'confirmed']
            )
            student.current_allocation_id = active_allocation[:
                                                              1].id if active_allocation else False

    @api.constrains('email')
    def _check_email(self):
        for student in self:
            if student.email:
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(pattern, student.email):
                    raise ValidationError(
                        _('Please enter a valid email address!'))

    @api.constrains('phone')
    def _check_phone(self):
        for student in self:
            if student.phone and not student.phone.isdigit():
                raise ValidationError(
                    _('Phone number must contain only digits.'))

    _sql_constraints = [
        ('unique_student_id', 'unique(student_id)', 'Student ID must be unique!'),
    ]
