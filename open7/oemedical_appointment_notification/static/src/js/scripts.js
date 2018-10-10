
openerp.oemedical_appointment_notification = function(instance) {
    var _t = instance.web._t, _lt = instance.web._lt;
	var QWeb = instance.web.qweb;

    instance.web.OeMedicalMail = instance.web.Widget.extend({
        template:'OeMedicalMail',

        start: function () {
            this.$('button').on('click', this.on_action_send_notification );
            this._super();
        },

        on_action_send_notification: function (event) {
            event.stopPropagation();
            var action = {
                name: _t('Enviar correo a pacientes...'),
                type: 'ir.actions.act_window',
                res_model: 'oemedical.send_notification_wizard',
                views: [[false, 'form']],
                view_mode: 'form',
                view_type: 'form',
                target: 'new',
                view_id: 'oemedical_appointment_notification.oemedical_send_notification_wizard_form_view',
                context: {'form_view_ref': 'oemedical_appointment_notification.oemedical_send_notification_wizard_form_view'},
            };

            instance.client.action_manager.do_action(action);
        },
    });   
   
    var button = false;

    instance.web.ViewManager.include({
        start: function () {
            this._super.apply(this, arguments);
            if (button == false && this.dataset.model == 'oemedical.patient') {
                button = new instance.web.OeMedicalMail();
                button.appendTo(instance.webclient.$el.find('.oe_view_manager_buttons'));
            }
        },

        switch_mode: function(view_type, no_store, view_options) {
            if (instance.webclient.$el.find('#oemedical_mail_wizard').length == 0) {
                if (this.dataset.model == 'oemedical.patient') {
                    button = new instance.web.OeMedicalMail();
                    button.appendTo(instance.webclient.$el.find('.oe_view_manager_buttons'));
                }
            }

            return this._super(view_type, no_store, view_options);
        },
    });
    
    
    instance.web.PatientNotification =  instance.web.Widget.extend({
	    template: 'PatientNotification',
	    init: function() {
	        this._super.apply(this, arguments);
	        instance.web.patientnotification = this;	        
	    },
	    
	    start: function() {
	        this._super.apply(this, arguments);	         
	        this.$el.notify();	        	       
	    },
	    
	    warn: function(title, text, sticky) {
	        sticky = !!sticky;
	        var opts = {};
	        if (sticky) {
	            opts.expires = false;
	        }
	        return this.$el.notify('create', 'oe_notification_alert', {
	            title: title,
	            text: text
	        }, opts);
	    },
	   
	    notify: function(title, text, sticky) {
	        sticky = !!sticky;
	        var opts = {};
	        if (sticky) {
	            opts.expires = false;
	        }
	        return this.$el.notify('create', {
	            title: title,
	            text: text
	        }, opts);
	    }
	});

	instance.web.action_notify_patient = function(element, action) {
	    element.do_warn(action.params.title, action.params.text, action.params.sticky);
	};
	instance.web.client_actions.add("notify.patient", "instance.web.action_notify_patient");   
	
};

