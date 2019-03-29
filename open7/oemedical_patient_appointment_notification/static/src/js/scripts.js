
openerp.oemedical_patient_appointment_notification = function(instance) {
    var _t = instance.web._t, _lt = instance.web._lt;
	var QWeb = instance.web.qweb;

	instance.user_appointment_conf = null;
	
    instance.web.PatientNotification =  instance.web.Widget.extend({
	    template: 'AppointmentNotification',
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

	instance.web.execute_appointment_notif = function(){

		new instance.web.Model("res.users").call("call_patient_appointment_notification",[[instance.session.uid],new instance.web.CompoundContext()])
			.then(function(result) {
				if(result != null && result != ''){
					instance.client.do_warn(result.params.title, result.params.text, true);
				}
				else{
					instance.client.do_notify(_t('Appointment Notifications'), _t('No appointment were found after or in the current date.'), true);
				}
	    	});
	};

	instance.web.action_notify_appointment = function(element, action) {
		if(!action || !action.params){

			instance.web.execute_appointment_notif();	
		}
		else{

			element.do_warn(action.params.title, action.params.text, action.params.sticky);
		}
	};
	
	instance.web.client_actions.add("notify.appointment", "instance.web.action_notify_appointment"); 
	
	function loading_appointmet_config(){
		var self = this;
		
		if(!instance.session.uid){
			return;
		}
		
		if(!instance.user_appointment_conf){			 
			new instance.web.Model("res.users").call("read",[[instance.session.uid],['enable_appointment_notification','show_every_appointment_notification','show_unit_time_appointment_notification']])
			.then(function(result) {
				if(result && result.length > 0){
					instance.user_appointment_conf = result[0];					
				} 
	        });
	    }	
	};
	
	instance.web.Session.include({
	    
		session_reload: function () {
	        var self = this;
	        return this.rpc("/web/session/get_session_info", {}).done(function(result) {
				
				if(!instance.user_appointment_conf){
					loading_appointmet_config();
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
				
				if(!instance.user_appointment_conf){			 
					new instance.web.Model("res.users").call("read",[[instance.session.uid],['enable_appointment_notification','show_every_appointment_notification','show_unit_time_appointment_notification']])
					.then(function(result) {
						if(result && result.length > 0){
							instance.user_appointment_conf = result[0];					
						} 
					});
				}   	    
				
	            _.extend(self, result);
				
				if (!_volatile) {
	                self.set_cookie('session_id', self.session_id);
				}
				
	            return self.load_modules();
	        });
	    },
		
		session_logout: function() {
			var self = this;
			 	
			instance.user_appointment_conf = null;
	        
			this.set_cookie('session_id', '');
	        $.bbq.removeState();
	        return this.rpc("/web/session/destroy", {});
	    },
	});	
	
	instance.web.ViewManager.include({
        start: function () {
            this._super.apply(this, arguments);
			
			if (this.dataset.model == 'oemedical.appointment' ) {
                console.log("VIEW:");				 
				console.log(this); 

				//instance.web.execute_appointment_notif();
            }
        },

        switch_mode: function(view_type, no_store, view_options) {
			
				 
			
			if (view_type == 'calendar' && this.dataset.model == 'oemedical.appointment') {
				 
				console.log('Instance Config:');
				console.log(instance);

                //console.log("VIEW SWITCH:");
				//console.log(view_type);
				//console.log(this.dataset.model);
				//console.log(this);		

				instance.web.execute_appointment_notif();
            }

            return this._super(view_type, no_store, view_options);
        },
    });
};

