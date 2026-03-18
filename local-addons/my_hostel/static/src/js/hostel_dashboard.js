odoo.define("my_hostel.hostel_dashboard", function (require) {
    "use strict"

    var AbstractAction = require("web.AbstractAction")
    var core = require("web.core")
    var rpc = require("web.rpc")

    var HostelDashboard = AbstractAction.extend({
        template: "hostel_dashboard",

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.action = action
        },

        start: function () {
            this._super.apply(this, arguments)
            this.load_dashboard_data()
        },

        load_dashboard_data: function () {
            var self = this
            rpc.query({
                model: "hostel.hostel",
                method: "search_read",
                fields: [
                    "name",
                    "total_rooms",
                    "occupied_rooms",
                    "available_rooms",
                ],
            }).then(function (result) {
                self.$(".hostel-stats").html(JSON.stringify(result))
            })
        },
    })

    core.action_registry.add("hostel.dashboard", HostelDashboard)

    return HostelDashboard
})
