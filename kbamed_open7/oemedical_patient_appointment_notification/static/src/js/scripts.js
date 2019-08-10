
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

		if(instance.user_appointment_conf && instance.user_appointment_conf.enable_notification){
			
			new instance.web.Model("res.users").call("call_patient_appointment_notification",[[instance.session.uid],new instance.web.CompoundContext()])
				.then(function(result) {
					
					if(result != null && result != ''){
						instance.client.do_warn(result.params.title, result.params.text, true);
					}
					else{
						instance.client.do_notify(_t('Appointment Notes'), _t('No appointment notes were found after or in the current date.'), true);
					}
		    	});
		}
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
	
	instance.web.Session.include({
	    
		session_reload: function () {
	        var self = this;
	        return this.rpc("/web/session/get_session_info", {}).done(function(result) {
				
	        	if(result.uid && !instance.user_appointment_conf){
	        		
	        		new instance.web.Model("res.users").call("read",[[result.uid],['enable_appointment_notification','show_every_appointment_notification','show_unit_time_appointment_notification']])
	    			.then(function(resp) {
	    				
	    				if(resp && resp.length > 0){
	    					instance.user_appointment_conf = {
	    						enable_notification : resp[0].enable_appointment_notification,
	    						show_every : resp[0].show_every_appointment_notification,
	    						show_unit_time : resp[0].show_unit_time_appointment_notification
	    					} 
	    				} 
	    			});		
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
					
					new instance.web.Model("res.users").call("read",[[result.uid],['enable_appointment_notification','show_every_appointment_notification','show_unit_time_appointment_notification']])
					.then(function(resp) {
						
						if(resp && resp.length > 0){
							 
							instance.user_appointment_conf = {
								enable_notification : resp[0].enable_appointment_notification,
								show_every : resp[0].show_every_appointment_notification,
								show_unit_time : resp[0].show_unit_time_appointment_notification
							} 							 
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
            
			if (instance.user_appointment_conf && instance.user_appointment_conf.enable_notification 
					&&  this.dataset.model == 'oemedical.appointment' && this.active_view == 'calendar') {
                
				instance.web.execute_appointment_notif();
            }
        },

        switch_mode: function(view_type, no_store, view_options) {	
        	
        	var model = this.dataset.model;
        	
			if (view_type == 'calendar' && model == 'oemedical.appointment' 
				&& instance.user_appointment_conf && instance.user_appointment_conf.enable_notification) {
					        
				instance.web.execute_appointment_notif();
            }
			
			instance.web_calendar.Sidebar = instance.web.Widget.extend({
			    template: 'CalendarView.sidebar',
			    start: function() {
			        this._super();
			        
			        var element = this.$('.btn-appointment-notif');
			         
			        element.mouseover(function(){
			        	element.css('background-color', 'cornflowerblue');
			        });	
			        
			        element.mouseleave(function(){
				        element.css('background-color', '#C2D5FC');
			        });			         
			        
			        if(model == 'oemedical.appointment' && instance.user_appointment_conf 
			        		&& instance.user_appointment_conf.enable_notification){
			        	element.css('display', 'block');
			        }
			        else{
			        	element.css('display', 'none');
			        }	
			        
			        element.on('click', instance.web.execute_appointment_notif );
			        
			        this.mini_calendar = scheduler.renderCalendar({
			            container: this.$el.find('.oe_calendar_mini')[0],
			            navigation: true,
			            date: scheduler._date,
			            handler: function(date, calendar) {
			                scheduler.setCurrentView(date, 'day');
			            }
			        });
			        
			        scheduler.linkCalendar(this.mini_calendar);
			        this.filter = new instance.web_calendar.SidebarFilter(this, this.getParent());
			        this.filter.appendTo(this.$el.find('.oe_calendar_filter'));
			    }
			});			

            return this._super(view_type, no_store, view_options); 
        },
    });
	
	showAppointment = function(id){
		
		$('div.ui-state-error.ui-notify-message.ui-notify-message-style').css('display','none');
		
		var action = {
                type: 'ir.actions.act_window',
                res_model: 'oemedical.appointment',
                view_mode: 'form',
                res_id: id,
                view_type: 'form',
                views: [[false, 'form']],
                target: 'current',
                context: {},
        };
        
		instance.client.action_manager.do_action(action);
	}; 
};

