openerp.warning = function(instance) {
    var _t = instance.web._t; 
    var _lt = instance.web._lt;
    var QWeb = instance.web.qweb;   
    
    instance.web.WarningMessage = instance.web.Widget.extend({
    	template:'WarningWidget',
    	
        init:function(parent,options){
            this._super(parent,options);
            console.log("Loading Parent:");
            console.log(parent);
            console.log("Loading Options:");
            console.log(options);
            
            instance.web.WarningMessage = this;
            
            options = options || {};
            //instance.webclient.set_content_full_screen(true);
            //instance.web.blockUI();
            //instance.web.unblockUI();
            //this.warning = options.warning || (parent ? parent.warning : undefined);
        },  
        
        start: function() {
            var self = this;
            this._super.apply(this);
            console.log("Warning Widget:");           
            /*self.renderElement();            
            this.warning_message = new intance.WarningMessageWidget(this, {});                     
            console.log(this.warning_message);
            this.warning_message.show();
            */
              
        },
        
        show: function(){
            if(this.$el){
               this.$el.show();
            }
        },
         
        close: function(){
        	this._super();
        },
        
        hide: function(){
            if(this.$el){
                this.$el.hide();
            }
        }        
    });  
    
    instance.web.client_actions.add("show.warning", "instance.web.WarningMessage");
    
};
