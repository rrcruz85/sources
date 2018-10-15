
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
		if(!action || !action.params){
			new instance.web.Model("res.users").call("call_patient_notification",[[instance.session.uid],new instance.web.CompoundContext()])
			.then(function(result) {
				if(result != null && result != ''){
					instance.client.do_warn(result.params.title, result.params.text, true);
				}
				else{
					instance.client.do_notify('Operated Patients Notification', 'No patients were found for the current date.', true);
				}
	         });	
		}
		else{
			element.do_warn(action.params.title, action.params.text, action.params.sticky);
		}
	};
	
	instance.web.client_actions.add("notify.patient", "instance.web.action_notify_patient"); 
	 
	instance.user = null;
	
	function notifier(){
		var self = this;
		
		if(!instance.session.uid){
			return;
		}
		
		if(!instance.user){			 
			new instance.web.Model("res.users").call("read",[[instance.session.uid],['receive_patient_notification','show_notification','show_unit_time']])
			.then(function(result) {
				if(result && result.length > 0){
					instance.user = result[0];					
				} 
	         });
	    }
		
		if(instance.user && !instance.user.receive_patient_notification){
			return;
		}
		
		console.log('Executing :' + (new Date()).toLocaleTimeString());
		
		new instance.web.Model("res.users").call("call_patient_notification",[[instance.session.uid],new instance.web.CompoundContext()])
		.then(function(result) {				 
			if(result != null && result != ''){
				instance.client.do_warn(result.params.title, result.params.text, true);
			}
			else{
				instance.client.do_notify('Operated Patients Notification', 'No patients were found for the current date.', true);
			}
         });			
	};
	
	instance.web.Session.include({
	    init: function() {
		   this._super.apply(this, arguments);
		   this.name = instance._session_id;
		   this.qweb_mutex = new $.Mutex();
		   this.timerFunction = null;
		},
		
		session_reload: function () {
	        var self = this;
	        return this.rpc("/web/session/get_session_info", {}).done(function(result) {
	            
	        	if(instance.user != null){
		            if(self.timerFunction){
		            	clearInterval(self.timerFunction);
		            	self.timerFunction = null;
		            }           
		            
		            var defaultInterval = 30000;
		            var interval = 1;
		            if(instance.user.show_notification){
		            	interval = instance.user.show_notification;
		            }
		            
		            if(instance.user.show_unit_time == 'minute'){
		            	defaultInterval = interval * 60000;
		            }
		            if(instance.user.show_unit_time == 'hour'){
		            	defaultInterval = interval * 3600000;
		            }
		            
		            self.timerFunction = setInterval(notifier, defaultInterval);  
	            }
	        	
	            _.extend(self, result);
	        });
	    },
		
		session_authenticate: function(db, login, password, _volatile) {			 
	        var self = this;
	        var base_location = document.location.protocol + '//' + document.location.host;
	        var params = { db: db, login: login, password: password, base_location: base_location };
	        return this.rpc("/web/session/authenticate", params).then(function(result) {
	            if (!result.uid) {
	                return $.Deferred().reject();
	            }
	            
                new instance.web.Model("res.users").call("read",[[result.uid],['receive_patient_notification','show_notification','show_unit_time']])
        		.then(function(result) {
        			if(result && result.length > 0){
        				instance.user = result[0]; 
        				
        				if(instance.user != null){
        		            if(self.timerFunction){
        		            	clearInterval(self.timerFunction);
        		            	self.timerFunction = null;
        		            }           
        		            
        		            var defaultInterval = 30000;
        		            var interval = 1;
        		            if(instance.user.show_notification){
        		            	interval = instance.user.show_notification;
        		            }
        		            
        		            if(instance.user.show_unit_time == 'minute'){
        		            	defaultInterval = interval * 60000;
        		            }
        		            if(instance.user.show_unit_time == 'hour'){
        		            	defaultInterval = interval * 3600000;
        		            }
        		            
        		            self.timerFunction = setInterval(notifier, defaultInterval);  
        	            }
        		    } 
        	    });        	    
                
	            _.extend(self, result);
	            if (!_volatile) {
	                self.set_cookie('session_id', self.session_id);
	            }	    
	            
	            if(instance.user != null){
	            	
	            	if(self.timerFunction){
		            	clearInterval(self.timerFunction);
		            	self.timerFunction = null;
		            }  
	            	
	            	var defaultInterval = 30000;
		            var interval = 1;
		            if(instance.user.show_notification){
		            	interval = instance.user.show_notification;
		            }
		            
		            if(instance.user.show_unit_time == 'minute'){
		            	defaultInterval = interval * 60000;
		            }
		            if(instance.user.show_unit_time == 'hour'){
		            	defaultInterval = interval * 3600000;
		            }
		            
		            self.timerFunction = setInterval(notifier, defaultInterval);
	            }
	            
	            return self.load_modules();
	        });
	    },
		
		session_logout: function() {
			var self = this;
			
			if(self.timerFunction){
				clearInterval(self.timerFunction);
				self.timerFunction = null;
			}
			 	
			instance.user = null;
	        
			this.set_cookie('session_id', '');
	        $.bbq.removeState();
	        return this.rpc("/web/session/destroy", {});
	    },
	});
		
};

