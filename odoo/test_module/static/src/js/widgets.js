openerp.test_module = function(instance) {

    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    var _lt = instance.web._lt;

    instance.test_module = {};

    var module = instance.test_module;

    instance.test_module.test_template = instance.web.Widget.extend({
        template: 'test_template',
        init: function () {
            this._super(arguments[0],{});
            alert('Hola Mundo1');
        },

        start: function () {
            var self = this;
            this.$("#btn").click(function (ev) {
                ev.stopPropagation();
                alert('Hola Mundo2');
                //this.do_update_attendance();
            });
            alert("Hola Template");
        },

        /*
        start: function () {
            console.log("Comenzando");
            var self = this;
            console.log(self);

            return self.test_template.done(function () {
                if ($.browser.chrome) {
                    var chrome_version = $.browser.version.split('.')[0];
                    if (parseInt(chrome_version, 10) >= 50) {
                        openerp.loadCSS('/point_of_sale/static/src/css/chrome50.css');
                    }
                }

                // remove default webclient handlers that induce click delay
                $(document).off();
                $(window).off();
                $('html').off();
                $('body').off();
                $(self.$el).parent().off();
                $('document').off();
                $('.oe_web_client').off();
                $('.openerp_webclient_container').off();

                self.renderElement();

                instance.webclient.set_content_full_screen(true);

                self.$('.loader').animate({opacity: 0}, 1500, 'swing', function () {
                    self.$('.loader').addClass('oe_hidden');
                });

            }).fail(function (err) {   // error when loading models data from the backend
                self.loading_error(err);
            });

        },

        start: function () {
            var self = this;
            this.$("#btn").click(function (ev) {
                ev.stopPropagation();
                alert('Hola Mundo');
                this.do_update_attendance();
            });
            alert("Hola Template");
        },

        do_update_attendance: function () {
            var self = this;
            var hr_employee = new instance.web.DataSet(self, 'hr.employee');
            console.log(hr_employee);
            /*
            hr_employee.call('attendance_action_change', [
                [self.employee.id]
            ]).done(function (result) {
                self.last_sign = new Date();
                self.set({"signed_in": !self.get("signed_in")});
            });

        },
        */

    });

    instance.web.client_actions.add("test_module", "instance.test_module.test_template");
};