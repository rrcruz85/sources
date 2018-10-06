
openerp.WarningWidgetModule = function(instance) {
    var _t = instance.web._t; 
    var _lt = instance.web._lt;   
    
    instance.WarningWidget = instance.PosBaseWidget.extend({
        template:'WarningWidget',
        
        init: function(){
        	console.log(arguments);
        	this._super(arguments[0],{});
            instance.web.blockUI();
            instance.warningwidget = this;
        },        
         
        start: function() {
        	var self = this;
        	self.renderElement();
        	instance.webclient.set_content_full_screen(true);
        },        
        
    });
    
     
    instance.web.client_actions.add("show_warning", "instance.WarningWidget");    
    
};
