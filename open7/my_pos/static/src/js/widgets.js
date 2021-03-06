
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
            this.click_product_action = this.addProductAction; //options.click_product_action;

            this.pos.get('products').bind('reset', function(){
                self.renderElement();
            });
        },
        
        addProductAction : function(product){
        	var self = this;
        	
        	if(product.get('to_weight') && self.pos.iface_electronic_scale){
        	     self.pos_widget.screen_selector.set_current_screen(self.scale_screen, {product: product});
            }
        	else{            	 
            	if(product.get('sale_price_ids').length > 0){
            		/*
            		if($('input[name="'+ product.get('id').toString() +  '"]:checked').length == 0){
            		    //alert(_t('You must select one price for the product ') + product.get('name'));	
            		    //self.pos_widget.do_warn('Error','You must select one price for the product ' + product.get('name'), true);
            		}
            		else{
            		*/
            		if($('input[name="'+ product.get('id').toString() +  '"]:checked').length > 0){
                		
            			let productPrice = $('input[name="'+ product.get('id').toString() +  '"]:checked')[0].value;
            			 
            			for(var i = 0; i < product.get('sale_price_ids').length; i++){
            				if(product.get('sale_price_ids')[i].price == productPrice){ 	            				
	            				//product.attributes.name_price = ' (' + product.get('sale_price_ids')[i].name + ')';
	            				break;
            				}
            			}
            			
            			/*
            			//for setting the same price 
            			var products = self.pos.get('selectedOrder').get('orderLines').models;
            			var productId = product.get('id');
            			for(var i = 0; i < products.length; i++){
            				if(products[i].product.id == productId){
            					products[i].price = productPrice;
            				}
            			}      
            			*/  
            			
            			self.pos.get('selectedOrder').addProduct(product, {price: productPrice}); 
            		}	
            	}
            	else{ 
 				     self.pos.get('selectedOrder').addProduct(product);
            	}
            }          
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
	            	
	            	let product = null;
		               
	            	if(products[i].get('sale_price_ids').length > 0){
	                	product = new module.ProductWidget(self, {model: products[i]});
	                }
	            	else{
	            		product = new module.ProductWidget(self, {model: products[i], click_product_action: this.click_product_action});
	  	            }
	            	
	                this.productwidgets.push(product);
	                product.appendTo(this.$('.product-list'));
	                
	                let p = products[i]; 
	                if(p.get('sale_price_ids').length > 0){	                	
	                	               	
	                	let productId = p.get('id');
	                	$('input#' + productId.toString() + '-1').click(function(){	                		 
	                		self.click_product_action(p);	                		 	                	
	                	}); 
	                	
	                	for(var pos = 1; pos <= p.get('sale_price_ids').length; pos++){
	                		$('input#' + productId.toString() + '-' + (pos + 1).toString()).click(function(){	                		 
		                		self.click_product_action(p);	                		 	                	
		                	}); 
	                	}
	                }
	                
	                if(p.get('sale_price_ids').length >= 3){
	                	$('input#' + p.get('id').toString() + '-1').parent().parent().css("overflow-y", "scroll");
	                	$('input#' + p.get('id').toString() + '-' + (p.get('sale_price_ids').length + 1).toString()).parent().css("margin-bottom", "10px");
	                }
	            }
            }
            else {
            	for(var i = 0, len = products.length; i < len; i++) {
	            	if (products[i].get('tpv_list_ids').indexOf(this.pos.get('pos_config').id) > -1) {
		                var product = new module.ProductWidget(self, {model: products[i], click_product_action: this.click_product_action});
		                this.productwidgets.push(product);
		                product.appendTo(this.$('.product-list'));
		                
		                if(products[i].get('sale_price_ids').length >= 3){
		                 	$('input#' + products[i].get('id').toString() + '-1').parent().parent().css("overflow-y", "scroll");
		 	            }
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
	
	module.NumpadWidget.include({
		start: function() {
            this.state.bind('change:mode', this.changedMode, this);
            this.changedMode();
            this.$el.find('button#numpad-backspace').click(_.bind(this.clickDeleteLastChar, this));
            this.$el.find('button#numpad-minus').click(_.bind(this.clickSwitchSign, this));
            this.$el.find('button.number-char').click(_.bind(this.clickAppendNewChar, this));
            this.$el.find('button.mode-button').click(_.bind(this.clickChangeMode, this));
            
            this.$el.find('button:contains("0")').css('display','none');
            var btn0 = '<button class="input-button number-char" style="margin-left:3px !important;">0</button>'; 
            this.$el.find('button:contains("9")').after(btn0);
            this.$el.find('.mode-button[data-mode="price"]').css('display','none');
            this.$el.find('button:contains("0")').click(_.bind(this.clickAppendNewChar, this));
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
