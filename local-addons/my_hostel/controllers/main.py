from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home


class HostelController(Home):

    @http.route('/hostel/dashboard', type='http', auth='user', website=True)
    def hostel_dashboard(self):
        hostels = request.env['hostel.hostel'].search([])
        rooms = request.env['hostel.room'].search([])
        students = request.env['hostel.student'].search([])

        values = {
            'hostel_count': len(hostels),
            'room_count': len(rooms),
            'occupied_rooms': len(rooms.filtered(lambda r: r.state == 'occupied')),
            'student_count': len(students),
            'hostels': hostels,
        }
        return request.render('my_hostel.hostel_dashboard_template', values)
