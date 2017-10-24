
openerp.my_pos = function(instance) {
	var QWeb = instance.web.qweb, _t = instance.web._t;
	
	module.ProductListWidget = module.ScreenWidget.extend({
        template:'ProductListWidget',
        init: function(parent, options) {
            var self = this;
            this._super(parent,options);
            this.model = options.model;
            this.productwidgets = [];
            this.weight = options.weight || 0;
            this.show_scale = options.show_scale || false;
            this.next_screen = options.next_screen || false;
            this.click_product_action = options.click_product_action;

            this.pos.get('products').bind('reset', function(){
                self.renderElement();
            });
        },
        renderElement: function() {
            var self = this;
            this._super();
            
            for(var i = 0, len = this.productwidgets.length; i < len; i++) {
                this.productwidgets[i].destroy();
            }
            
            this.productwidgets = []; 
            if(this.scrollbar){
                this.scrollbar.destroy();
            }
            
            var products = this.pos.get('products').models || [];
            if (this.pos.get('pos_config').show_all_products) {
	            for(var i = 0, len = products.length; i < len; i++) {
	                var product = new module.ProductWidget(self, {model: products[i], click_product_action: this.click_product_action});
	                this.productwidgets.push(product);
	                product.appendTo(this.$('.product-list'));
	            }
            }
            else {
            	for(var i = 0, len = products.length; i < len; i++) {
	            	//this.pos.db.get_product_by_id(products[i].id)
	            	if (products[i].get('tpv_list_ids').indexOf(this.pos.get('pos_config').id) > -1) {
		                var product = new module.ProductWidget(self, {model: products[i], click_product_action: this.click_product_action});
		                this.productwidgets.push(product);
		                product.appendTo(this.$('.product-list'));
	            	}
	            }
            }
            
            this.scrollbar = new module.ScrollbarWidget(this,{
                target_widget:   this,
                target_selector: '.product-list-scroller',
                on_show: function(){
                    self.$('.product-list-scroller').css({'padding-right':'62px'},100);
                },
                on_hide: function(){
                    self.$('.product-list-scroller').css({'padding-right':'0px'},100);
                },
            });

            this.scrollbar.replace(this.$('.placeholder-ScrollbarWidget'));
        },
    });
	
	module.PaypadButtonWidget = module.PosBaseWidget.extend({
        template: 'PaypadButtonWidget',
        init: function(parent, options){
            this._super(parent, options);
            this.cashRegister = options.cashRegister;
        },
        renderElement: function() {
            var self = this;
            this._super();

            this.$el.click(function(){
                if (self.pos.get('selectedOrder').get('screen') === 'receipt'){  //TODO Why ?
                    console.warn('TODO should not get there...?');
                    return;
                }
                self.pos.get('selectedOrder').addPaymentLine(self.cashRegister);
                self.pos_widget.screen_selector.set_current_screen('payment');
            });
        },
    });
	
	module.OrderWidget.include({
		update_summary: function(){
			this._super();
			var order = this.pos.get('selectedOrder');
			var pos_config = this.pos.get('pos_config');
			var total = order ? order.getTotalTaxExcluded() : 0;
            var iva_restitution = total * pos_config.iva_compensation/100;
			this.$('.summary .total .iva_subentry .value').html(this.format_currency(iva_restitution));
        },
	});
	
	module.PaymentScreenWidget.include({
		updatePaymentSummary: function() {
			if (globalType == false) {
				this._super();
				this.$('#payment-iva-compensation').html(this.format_currency(0.0));
				this.$('#payment-iva-zero').html(this.format_currency(0.0));
				this.$('#payment-total-iva-excluded').html(this.format_currency(this.pos.get('selectedOrder').getTotalTaxExcluded()));
				$('.pos-payment-container .footer .left-block').eq(1).css('display', 'none');
            	$('.pos-payment-container .footer .right-block').eq(1).css('display', 'none');
            	$('.header').eq(0).css('display', 'none');
			}
			else {
				var pos_config = this.pos.get('pos_config');
				var currentOrder = this.pos.get('selectedOrder');
				var dueTotal = currentOrder.getTotalTaxIncluded();
				var dueTotalNotIVA = currentOrder.getTotalTaxExcluded();
				
				var paidTotal = currentOrder.getPaidTotal();
	            var iva_compensation = currentOrder.getIvaCompensation();
	            var iva_zero = currentOrder.getIvaZero();

	            var remaining = dueTotal > paidTotal ? dueTotal - paidTotal: 0;
	            var change = paidTotal > dueTotal ? paidTotal - dueTotal : 0;
	            
	            this.$('#payment-due-total').html(this.format_currency(dueTotal));
	            this.$('#payment-total-iva-excluded').html(this.format_currency(dueTotalNotIVA));
	            this.$('#payment-iva-compensation').html(this.format_currency(iva_compensation));
	            this.$('#payment-iva-zero').html(this.format_currency(iva_zero));
	            this.$('#payment-paid-total').html(this.format_currency(paidTotal));
	            this.$('#payment-remaining').html(this.format_currency(remaining));
	            this.$('#payment-change').html(this.format_currency(change));
	            
	            if(currentOrder.selected_orderline === undefined){
	                remaining = 1;
	            }
	                
	            if(this.pos_widget.action_bar){
	                this.pos_widget.action_bar.set_button_disabled('validation', remaining > 0.000001);
	            }
			}
			
			var client = this.pos.get('selectedOrder').get_client();
            if (client != null && client != undefined && client != false) {
            	this.$('#div_customer_name').html(client.name);
            	this.$('#div_customer_address').html(client.contact_address);
            	this.$('#div_customer_email').html(client.email);
            	this.$('#div_customer_mobile').html(client.mobile);
            	this.$('#div_customer_phone').html(client.phone);
            	
            	if (client.ced_ruc) {
            		this.$('#div_customer_ced').html('ID: ' + client.ced_ruc);
            	}
            }
            else {
            	this.$('.client_data_div').html('<div class="client_data_div"><div id="div_customer_name"/><div id="div_customer_ced"/><div id="div_customer_ruc"/><div id="div_customer_address"/><div id="div_customer_email"/><div id="div_customer_mobile"/><div id="div_customer_phone"/></div>');
            }
        },
	});
}