globalType = false;

function my_pos_header (instance) {
    module = instance.point_of_sale;
    
    /*
        Define : PosOrderHeaderWidget to allow possibility to include inside
        some extra informations.
    */
    module.PosOrderHeaderWidget = module.PosBaseWidget.extend({
        template: 'PosOrderHeaderWidget',

        init: function(parent, options){
            this._super(parent, options);
        }
    });
    
    /*
        Overload : PosWidget to include PosOrderHeaderWidget inside.
    */
    module.PosWidget = module.PosWidget.extend({
        build_widgets: function() {
            this._super();
            this.pos_order_header = new module.PosOrderHeaderWidget(this,{});
            this.pos_order_header.appendTo(this.$('#rightheader'));
        },
    	
        get_logo_url: function() {
        	if (this.pos.get('company') != null) {
        		return instance.session.url('/web/binary/image', {model: 'res.company', field: 'logo_web', id: this.pos.get('company').id});
        	}
        	
            return instance.session.url('/web/binary/image', {model: 'res.company', field: 'logo_web', id: 1});
        },
        
        renderElement: function() {
            this._super();
            var self = this;
            var url = this.get_logo_url();
            var html = '<img class="company_img" src="' + url + '"' + ' style="max-height: 65px"/>';
            this.$('.company_img').replaceWith(html);
            
            this.$('#btn-addcust').click(function() {
            	$('.txt').val('');
            	$('#titre_form_edit_client').css('display', 'none');
            	self.screen_selector.show_popup('add-customer');
            });
            
            this.add_customer_button = new module.HeaderButtonWidget(this,{
                label: _t('Add Customer'),
                action: function(){
                    self.screen_selector.show_popup('add-customer');
                },
            });
            this.add_customer_button.replace($('.placeholder-AddCustomerButton'));
            this.add_customer_button.renderElement();
        },
    });
};

function my_pos_partner (instance) {
    module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    _t = instance.web._t;
    
    module.CustomerOrderWidget = module.PosBaseWidget.extend({
        template: 'CustomerOrderWidget',

        /* Overload Section */
        init: function(parent, options){
            this._super(parent,options);
            this.pos.bind('change:selectedOrder', this.refresh, this);
        },

        start: function(){
            this._super();
            this._build_widgets();
        },

        /* Custom Section */
        refresh: function() {
        	globalClient = false;
        	globalType = false;
            this.renderElement();
            this._build_widgets();
        },

        _build_widgets: function() {
        	// Create a button to add customer popup
        	this.add_customer_button = new module.HeaderButtonWidget(this,{
                label: _t('Add Customer'),
                action: function(){
                    self.screen_selector.show_popup('add-customer');
                },
            });
            //this.add_customer_button.replace($('.placeholder-AddCustomerButton'));
           //this.add_customer_button.renderElement();
            
            // Create a button to open the customer popup
            this.select_customer_button = new module.HeaderButtonWidget(this,{
                label: _t('Select Customer'),
                action: function(){
                    self.screen_selector.show_popup('select-customer');
                },
            });
            this.select_customer_button.replace($('.placeholder-SelectCustomerButton'));
            this.select_customer_button.renderElement();

            if (this.get_name() !== ''){
                // Create a button to remove the current customer
                this.remove_customer_button = new module.HeaderButtonWidget(this,{
                    label:_t('Del.'),
                    action: function(){
                        this.pos.get('selectedOrder').set_client(undefined);
                        this.pos_widget.customer_order.refresh();
                        this.hide();
                    },
                });
                this.remove_customer_button.replace($('.placeholder-RemoveCustomerButton'));
                this.remove_customer_button.renderElement();
            }
        },

        get_name: function() {
            customer = this.pos.get('selectedOrder').get_client();
            if(customer){
            	globalClient = customer;
                return customer.name;
            }else{
            	globalClient = false;
                return "";
            }
        },
        
        get_address: function() {
        	customer = this.pos.get('selectedOrder').get_client();
            if(customer) {
                return customer.contact_address;
            }else{
                return "";
            }
        }
    });

    module.CustomerWidget = module.PosBaseWidget.extend({
        template: 'CustomerWidget',

        /* Overload Section */
        init: function(parent, options) {
            this._super(parent,options);
            this.model = options.model;
        },

        renderElement: function() {
            this._super();
            var self = this;
            //this.$('img').replaceWith(this.pos_widget.image_cache.get_image(this.model.get_image_small_url()));
            
            $(".partner_selector", this.$el).click(function(e) {
                self.pos.get('selectedOrder').set_client(self.model.toJSON());
                self.pos_widget.customer_order.refresh();
                self.pos_widget.screen_selector.set_current_screen('products');
            });
            
            $(".edit_btn", this.$el).click(function(e) {
            	$('#titre_form_edit_client').css('display', 'block');
            	$('#titre_form_create_client').css('display', 'none');
            	
            	$('#input_name').val(self.model.toJSON().name);
            	$('#input_id_type').val(self.model.toJSON().type_ced_ruc);
            	$('#input_id_number').val(self.model.toJSON().ced_ruc != false ? self.model.toJSON().ced_ruc : '');
            	$('#input_partner_id').val(self.model.toJSON().id);
            	
            	$('#input_zip').val(self.model.toJSON().contact_address != false ? self.model.toJSON().contact_address : '');
            	$('#input_phone').val(self.model.toJSON().phone != false ? self.model.toJSON().phone : '');
            	$('#input_mobile').val(self.model.toJSON().mobile != false ? self.model.toJSON().mobile : '');
            	$('#input_email').val(self.model.toJSON().email != false ? self.model.toJSON().email : '');
            	
            	self.pos_widget.screen_selector.show_popup('add-customer');
            });
        },
    });

    module.CustomerListScreenWidget = module.ScreenWidget.extend({
        template:'CustomerListScreenWidget',

        init: function(parent, options) {
            this._super(parent,options);
            this.customer_list = [];
        },

        start: function() {
            this._super();
            var self = this;
        },

        renderElement: function() {
            this._super();
            var self = this;
            // Delete old customers widget and display refreshed customers list
            for(var i = 0, len = this.customer_list.length; i < len; i++){
                this.customer_list[i].destroy();
            }
            this.customer_list = [];
            var customers = this.pos.get('customer_list_filter') || [];
            for(var i = 0, len = customers.models.length; i < len; i++){
                var customer = new module.CustomerWidget(this, {
                    model: customers.models[i],
                    click_product_action: this.click_product_action,
                });
                this.customer_list.push(customer);
                customer.appendTo(this.$('.customer-list'));
            }

            // Delete old scrollbar widget and display refreshed scrollbar
            if(this.scrollbar){
                this.scrollbar.destroy();
            }
            this.scrollbar = new module.ScrollbarWidget(this,{
                target_widget:   this,
                target_selector: '.customer-list-scroller',
                on_show: function(){
                    self.$('.customer-list-scroller').css({'padding-right':'62px'},100);
                },
                on_hide: function(){
                    self.$('.customer-list-scroller').css({'padding-right':'0px'},100);
                },
            });
            this.scrollbar.replace(this.$('.placeholder-ScrollbarWidget'));
        },
    });
    
    module.AddCustomerPopupWidget = module.PopUpWidget.extend({
    	template: 'FormClientWidget',
    	
    	start: function(){
            this._super();
            var self = this;
        },
        
        hide_form_client: function(){
        	$('#input_name').val('');
        	$('#input_id_type').val('');
        	$('#input_id_number').val('');
        	$('#input_partner_id').val(-1);
        	
        	$('#input_zip').val('');
        	$('#input_phone').val('');
        	$('#input_mobile').val('');
        	$('#input_email').val('');
        	
        	this.pos_widget.screen_selector.set_current_screen('products');
        },
        
        show: function(){
            this._super();
            var self = this;
            
            this.$('#input_cancel').off('click').click(function(){
                self.pos_widget.screen_selector.set_current_screen('products');
            });
            
            $('#error_cname').css('display', 'none');
            $('#error_czip').css('display', 'none');
            $('#error_cphone').css('display', 'none');
            $('#error_cmobile').css('display', 'none');
            $('#error_cemail').css('display', 'none');
            $('#error-msg').css('display', 'none');
        },
        
        validateEmail: function(email) {
        	if (email == '') {return true;}
            var emailReg = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
            return emailReg.test(email);
        },
        
        renderElement: function(){
            var self = this;
            this._super();
            
            this.$('.input_send_formclient').click(function() {
                var c_name = $('#input_name').val();
                var c_zip = $('#input_zip').val();
                var c_phone = $('#input_phone').val();
                var c_mobile = $('#input_mobile').val();
                var c_email = $('#input_email').val();
                var c_id = $('#input_partner_id').val();
                var c_id_type = $('#input_id_type').val();
                var c_id_number = $('#input_id_number').val();
                var nb_error = 0;

                // error messages
                $('#error_cname').css('display', 'none');
                $('#error_czip').css('display', 'none');
                $('#error_cphone').css('display', 'none');
                $('#error_cmobile').css('display', 'none');
                $('#error_cemail').css('display', 'none');
                $('#error-msg').css('display', 'none');

                if (c_name == ''){
                    $('#error_cname').css('display', 'block');
                    nb_error++;
                }

                if (c_zip == ''){
                    $('#error_czip').css('display', 'block');
                    nb_error++;
                }

                /*if (c_phone.length < 9){
                    $('#error_cphone').css('display', 'block');
                    nb_error++;
                }*/

                /*if (c_mobile.length < 10){
                    $('#error_cmobile').css('display', 'block');
                    nb_error++;
                }*/

                if (!self.validateEmail(c_email)){
                    $('#error_cemail').css('display', 'block');
                    nb_error++;
                }

                if (nb_error > 0){
                    $('#error-msg').css('display', 'block');
                }
                else {
                    self.save_client(c_id.trim(), c_name.trim(), c_zip.trim(), c_phone.trim(), c_mobile.trim(), c_email.trim(), c_id_type.trim(), c_id_number.trim());
                }
            });
        },
        
        save_client: function(cid, cname, czip, cphone, cmobile, cemail, c_id_type, c_id_number){
            var self = this;
            var Partners = new instance.web.Model('res.partner');
            Partners.call('write_partner_from_pos', [cid, cname, czip, cphone, cmobile, cemail, c_id_type, c_id_number], undefined, {shadow: true}).fail(function(res) {
                alert('Error : customer has not been created or updated...');
            }).done(function(res) {
            	if (typeof res === 'number') {
            		self.hide_form_client();
            		var customers = self.pos_widget.pos.fetch('res.partner', 
            			['name','display_name','title','function','type','parent_id',
            			 'is_company', 'lang','company_id','ean13','color','contact_address',
            			 'street','street2','city','zip','state_id','country_id', 
            			 'property_product_pricelist','vat','debit_limit','credit_limit','email',
            			 'website','fax','phone','mobile','ced_ruc','type_ced_ruc','id'], 
            			[['customer', '=', true], ['id', '=', res]]).then(
            				function (partners) {
            					for(var i = 0, len = partners.length; i < len; i++){
                                    self.pos_widget.pos.get('selectedOrder').set_client(partners[i]);
                                    self.pos_widget.customer_order.refresh();
                                    
                                    var customer = new module.CustomerWidget(this, {
                                        model: partners[i],
                                        click_product_action: this.click_product_action,
                                    });
                                    
                                    self.pos_widget.select_customer_popup.customer_list_widget.customer_list.push(customer);

                                    self.pos.get('customer_list').update_customer(partners[i]);

                                }
            					
            					self.pos_widget.pos.load_customers_data();
            				}
            			);
            	}
            	else {
            		alert(res);
            	}
            });
        },
    });
    
    module.SelectCustomerPopupWidget = module.PopUpWidget.extend({
        template:'SelectCustomerPopupWidget',

        start: function(){
            this._super();
            var self = this;
            this.customer_list_widget = new module.CustomerListScreenWidget(this,{});
        },

        show: function(){
            this._super();
            var self = this;
            this.reset_customers();
            this.customer_list_widget.replace($('.placeholder-CustomerListScreenWidget'));
            this.$('#customer-cancel').off('click').click(function(){
                self.pos_widget.screen_selector.set_current_screen('products');
            });
            // filter customers according to the search string
            //this.$('.customer-searchbox input').keyup(function(event){
            this.$('#search_customer_id').keyup(function(event){

                pattern = $(this).val().toLowerCase();
                if(pattern) {
                	var customers = self.pos.get('customer_list').search_customer(pattern);
                    self.pos.set({'customer_list_filter' : customers});
                    self.$('.customer-search-clear').fadeIn();
                    self.customer_list_widget.renderElement();
                	
//                	var l_filter = [['customer', '=', true], ['name', 'ilike', pattern]];
//                	self.pos_widget.pos.fetch('res.partner', 
//                					   ['id', 'name', 'zip', 'phone', 'mobile', 'email'],
//                					   l_filter).then(function (customers) {
//                						   //alert(customers.length);
//                						   console.log(customers);
//                						   customerWidgets = self.pos.set({'customer_list' : new module.CustomerCollection(customers)});
//                						   self.pos.set({'customer_list_filter' : customerWidgets});
//                					   });
//                	
//                    self.$('.customer-search-clear').fadeIn();
//                    self.customer_list_widget.renderElement();
                    
//                    var partners_list = [];
//                    var l_filter = [['customer', '=', true], ['name', 'ilike', pattern]];
//                	var loaded = self.pos_widget.pos.fetch('res.partner', 
//                					   ['id', 'name', 'zip', 'phone', 'mobile', 'email'],
//                					   l_filter).then(
//                		function (partners) {
//                			$('#client-list tr').remove();
//                            if(partners.length > 0) {
//                                for(var i = 0, len = partners.length; i < len; i++){
//                                   var one_client = QWeb.render('ClientWidget',{c_id: partners[i].id, c_name: partners[i].name, c_zip: partners[i].zip, c_phone: partners[i].phone, c_mobile: partners[i].mobile, c_email: partners[i].email});
//                                   $(one_client).appendTo($('#client-list')).click(
//                                       function () {
//                                    	   alert('ahhhhhhhhhhhhhhhhh');
//                                    	   //self.pos_widget.pos.get('selectedOrder').set_client(partners[i]);
//                                       }
//                                   );
//                                }
//                            }
//                		}
//                	);
                }
                else{
                    self.reset_customers();
                }
            });

            this.$('#search_customer_by_id').keyup(function (event) {
                pattern = $(this).val().toLowerCase();
                if (pattern) {
                    var customers = self.pos.get('customer_list').search_customer_by_id(pattern);
                    self.pos.set({'customer_list_filter': customers});
                    self.$('.customer-search-clear2').fadeIn();
                    self.customer_list_widget.renderElement();
                }
                else {
                    self.reset_customers();
                }
            });

            this.$('.btn').click(function () {
                self.reset_customers();
                ptr = "^" + this.innerText.toLowerCase();
                var customers = self.pos.get('customer_list').search_customer(ptr);
                self.pos.set({'customer_list_filter': customers});
                self.customer_list_widget.renderElement();
            });

            //reset the search when clicking on reset
            this.$('.customer-search-clear').click(function(){
                self.reset_customers();
            });
            this.$('.customer-search-clear2').click(function(){
                self.reset_customers();
            });
            //to create a customer
            this.$('#btn-addcust').click(function(){
            	self.pos_widget.screen_selector.show_popup('add-customer');
            	$('#titre_form_edit_client').css('display', 'none');
            	$('#titre_form_create_client').css('display', 'block');
            	
            	$('#input_name').val('');
            	$('#input_id_type').val('');
            	$('#input_id_number').val('');
            	$('#input_partner_id').val(-1);
            	
            	$('#input_zip').val('');
            	$('#input_phone').val('');
            	$('#input_mobile').val('');
            	$('#input_email').val('');
            });
        },

        reset_customers: function(){
            //this.pos.set({'customer_list_filter' : this.pos.get('customer_list')});
            this.pos.set({'customer_list_filter' : new module.CustomerCollection([])});
            this.$('.customer-search-clear').fadeOut();
            this.$('.customer-search-clear2').fadeOut();
            this.customer_list_widget.renderElement();
            this.$('.customer-searchbox input').val('').focus();
        },
    });

    module.PosWidget = module.PosWidget.extend({
        build_widgets: function(){
            this._super();
            var self = this;

            // Add a widget to manage customer
            this.customer_order = new module.CustomerOrderWidget(this,{});
            this.customer_order.appendTo(this.$('#pos_order_header'));

            // create a pop up 'select-customer' to search and select customers
            this.select_customer_popup = new module.SelectCustomerPopupWidget(this, {});
            this.select_customer_popup.appendTo($('.point-of-sale'));
            this.select_customer_popup.hide();
            this.screen_selector.popup_set['select-customer'] = this.select_customer_popup;
            
            // create a pop up 'add-customer' to create customers
            this.add_customer_popup = new module.AddCustomerPopupWidget(this, {});
            this.add_customer_popup.appendTo($('.point-of-sale'));
            this.add_customer_popup.hide();
            this.screen_selector.popup_set['add-customer'] = this.add_customer_popup;
            
        },
    });

    module.Customer = Backbone.Model.extend({
        get_image_small_url: function() {
            return instance.session.url('/web/binary/image', {model: 'res.partner', field: 'image_small', id: this.get('id')});
        },
    });

    module.CustomerCollection = Backbone.Collection.extend({
        model: module.Customer,

        search_customer: function(pattern){
            res = new module.CustomerCollection();
            var reg = RegExp(pattern,"i");
            for(var i = 0, len = this.models.length; i < len; i++){
                res_reg = reg.exec(this.models[i].attributes.name);
                if (res_reg){
                    res.push(this.models[i]);
                }
            }
            return res;
        },

        search_customer_by_id: function (pattern) {
            res = new module.CustomerCollection();
            var reg = RegExp(pattern, "i");
            for (var i = 0, len = this.models.length; i < len; i++) {
                res_reg = reg.exec(this.models[i].attributes.ced_ruc);
                if (res_reg) {
                    res.push(this.models[i]);
                }
            }
            return res;
        },

        update_customer: function (customer) {
            for (var i = 0, len = this.models.length; i < len; i++) {
                if(this.models[i].attributes.id == customer.id){
                    this.models[i].name = customer.name;
                    this.models[i].attributes.name = customer.name;
                    this.models[i].ced_ruc = customer.ced_ruc;
                    this.models[i].attributes.ced_ruc = customer.ced_ruc;
                    this.models[i].contact_address = customer.contact_address;
                    this.models[i].attributes.contact_address = customer.contact_address;
                    this.models[i].email = customer.email;
                    this.models[i].attributes.email = customer.email;
                    this.models[i].mobile = customer.mobile;
                    this.models[i].attributes.mobile = customer.mobile;
                    this.models[i].phone = customer.phone;
                    this.models[i].attributes.phone = customer.phone;
                    break;
                }
            }
        },

    });

    /*
        Overload: PosModel.initialize() to define two new lists.
        'customer_list' are the list of all customers available;
        'customer_list_filter' are a sub-list according to the current filter
        selection.
    */
    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
         _initialize_.call(this, session, attributes);
        this.set({
            'customer_list': new module.CustomerCollection(),
            'customer_list_filter': new module.CustomerCollection(),
        });
    };

    /*
        Overload: PosModel.load_server_data() function to get in memory
        customers.
        The function will load all usefull informations even if any
        informations won't be used in this module, to allow further modules
        to use them.
    */
    var _load_server_data_ = module.PosModel.prototype.load_server_data;
    module.PosModel.prototype.load_server_data = function(){
        var self = this;
        var load_def = _load_server_data_.call(self).done(self.load_customers_data());        
        return load_def;
    },

    module.PosModel = module.PosModel.extend({
        load_customers_data: function(){
        	var self = this;
        	var loaded = self.fetch(
                    'res.partner',
                    ['name','contact_address','zip','email','phone','mobile','ced_ruc','type_ced_ruc','id'],
                    [['customer', '=', true]])
                .then(function(customers){
                    self.set({'customer_list' : new module.CustomerCollection(customers)});
                    self.set({'customer_list_filter' : new module.CustomerCollection(customers)});
                });
            return loaded;
        },
    });
};

function my_pos_data(instance, module){ //module is instance.point_of_sale
    var module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    _t = instance.web._t;

    var round_di = instance.web.round_decimals;
    var round_pr = instance.web.round_precision;
    nbCards = 0;
    
    module.ReceiptScreenWidget.include({
    	show: function(){
    		var client = this.pos.get('selectedOrder').get_client();
            if (client != null && client != undefined && client != false) {
            	this.$('#div_customer_x_name').html(client.name);
            	this.$('#div_customer_x_address').html(client.contact_address);
            	this.$('#div_customer_x_email').html(client.email);
            	this.$('#div_customer_x_mobile').html(client.mobile);
            	this.$('#div_customer_x_phone').html(client.phone);
            	
            	if (client.ced_ruc) {
            		this.$('#div_customer_x_ced').html('ID: ' + client.ced_ruc);
            	}
            }
    			
    		this._super();
        },
        print: function () {
            if ((this.pos.get('selectedOrder')).get('orderLines').length >= 2) {
                $("div.pos-sale-ticket").css("max-height", "800px");
            }
            else {
                $("div.pos-sale-ticket").css("max-height", "400px");
            }
            window.print();
            if ((this.pos.get('selectedOrder')).get('orderLines').length >= 2) {
                $("div.pos-sale-ticket").css("max-height", "370px");
            }
        },
    });
    
    module.myPaymentScreenWidget = module.PaymentScreenWidget.include({
        template: 'PaymentScreenWidget',
        
        init: function(parent, options) {
            options = options || {};
            this._super(parent, options);
        },
        
        show: function(){
            this._super();
            var self = this;
            var client = this.pos.get('selectedOrder').get_client();
			
            if (client != null && client != undefined && client != false) {
            	this.$('#div_customer_name').html(client.name);
            	this.$('#div_customer_address').html(client.contact_address);
            	this.$('#div_customer_email').html(client.email);
            	this.$('#div_customer_mobile').html(client.mobile);
            	this.$('#div_customer_phone').html(client.phone);
            	
            	if (client.ced_ruc) {
            		this.$('#div_customer_ced').html('Id: ' + client.ced_ruc);
            	}
            }
            else {
            	this.$('.client_data_div').html();
            }
        },

        validateCurrentOrder: function () {
            var currentOrder = this.pos.get('selectedOrder');
            if (currentOrder.attributes.orderLines.length >= 2) {
                $("div.pos-sale-ticket").css("max-height", "800px");
            }
            else {
                $("div.pos-sale-ticket").css("max-height", "400px");
            }

            this.pos.push_order(currentOrder.exportAsJSON())
            if (this.pos.iface_print_via_proxy) {
                this.pos.proxy.print_receipt(currentOrder.export_for_printing());
                this.pos.get('selectedOrder').destroy();    //finish order and go back to scan screen
            } else {
                this.pos_widget.screen_selector.set_current_screen(this.next_screen);
            }

            if (currentOrder.attributes.orderLines.length >= 2) {
                $("div.pos-sale-ticket").css("max-height", "370px");
            }
        },
        
        fetch: function(model, fields, domain, ctx){
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
        },
        
        get_card_payment: function(journal){
            console.log('Diarios: ' + journal);
            var myPos = new instance.web.Model('pos.order');
            myPos.call('get_type_journal', [journal]).then(function (result) {});
        },
        
        get_cards: function(){
            var self = this;
            var card_list = [];
            
            var loaded = self.fetch('pos.credit.card',['name'],[['active', '=','true']]).then(function(cards){
                for(var i = 0, len = cards.length; i < len; i++){
                    card_list.push(cards[i].name);
                }
                nbCards = card_list.length;
                if(nbCards > 0){
                    if(nbCards > 1){
                        var new_option = '<option value="nobody"></option>\n';
                        self.$('#card_type').html(content + new_option);
                    }
                    for(var i = 0, len = card_list.length; i < len; i++){
                        var content = self.$('#card-select').html();
                        var new_option = '<option value="' + card_list[i] + '">' + card_list[i] + '</option>\n';
                        self.$('#card-select').html(content + new_option);
                    }
                }
            });
        },

        get_banks: function(){
            var self = this;
            var bank_list = [];
            var loaded = self.fetch('res.bank',['name'],[['active', '=','true']]).then(function(banks){
                for(var i = 0, len = banks.length; i < len; i++){
                    bank_list.push(banks[i].name);
                }
                nbBanks = bank_list.length;
                if(nbBanks > 0){
                    if(nbBanks > 1){
                        var new_option = '<option value="nobody"></option>\n';
                        self.$('#bank-select').html(content + new_option);
                    }
                    for(var i = 0, len = bank_list.length; i < len; i++){
                        var content = self.$('#bank-select').html();
                        var new_option = '<option value="' + bank_list[i] + '">' + bank_list[i] + '</option>\n';
                        self.$('#bank-select').html(content + new_option);
                    }
                }
            });
        }
    });

    module.PosModel = Backbone.Model.extend({
        initialize: function(session, attributes) {
            Backbone.Model.prototype.initialize.call(this, attributes);
            var  self = this;
            this.session = session;
            this.ready = $.Deferred();                          // used to notify the GUI that the PosModel has loaded all resources
            this.flush_mutex = new $.Mutex();                   // used to make sure the orders are sent to the server once at time

            this.barcode_reader = new module.BarcodeReader({'pos': this});  // used to read barcodes
            this.proxy = new module.ProxyDevice();              // used to communicate to the hardware devices via a local proxy
            this.db = new module.PosLS();                       // a database used to store the products and categories
            this.db.clear('products','categories');
            this.debug = jQuery.deparam(jQuery.param.querystring()).debug !== undefined;    //debug mode

            // default attributes values. If null, it will be loaded below.
            this.set({
                'nbr_pending_operations': 0,

                'currency':         {symbol: '$', position: 'after'},
                'shop':             null,
                'company':          null,
                'user':             null,   // the user that loaded the pos
                'user_list':        null,   // list of all users
                'partner_list':     null,   // list of all partners with an ean
                'cashier':          null,   // the logged cashier, if different from user

                'orders':           new module.OrderCollection(),
                //this is the product list as seen by the product list widgets, it will change based on the category filters
                'products':         new module.ProductCollection(),
                'cashRegisters':    null,

                'bank_statements':  null,
                'taxes':            null,
                'pos_session':      null,
                'pos_config':       null,
                'units':            null,
                'units_by_id':      null,

                'selectedOrder':    null,
                'acquirer':         null,
                'card_type':        null,
                'card_number':      null,
                'approval_number':  null,
                'lot_number':       null,
                'reference':        null
            });

            this.get('orders').bind('remove', function(){ self.on_removed_order(); });

            // We fetch the backend data on the server asynchronously. this is done only when the pos user interface is launched,
            // Any change on this data made on the server is thus not reflected on the point of sale until it is relaunched.
            // when all the data has loaded, we compute some stuff, and declare the Pos ready to be used.
            $.when(this.load_server_data())
                .done(function(){
                    //self.log_loaded_data(); //Uncomment if you want to log the data to the console for easier debugging
                    self.ready.resolve();
                }).fail(function(){
                    //we failed to load some backend data, or the backend was badly configured.
                    //the error messages will be displayed in PosWidget
                    self.ready.reject();
                });
        },

        // helper function to load data from the server
        fetch: function(model, fields, domain, ctx){
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
        },
        // loads all the needed data on the sever. returns a deferred indicating when all the data has loaded.
        load_server_data: function(){
            var self = this;

            var loaded = self.fetch('res.users',['name','company_id'],[['id','=',this.session.uid]])
                .then(function(users){
                    self.set('user',users[0]);

                    return self.fetch('res.company',
                    [
                        'currency_id',
                        'email',
                        'website',
                        'company_registry',
                        'vat',
                        'name',
                        'phone',
                        'partner_id',
                    ],
                    [['id','=',users[0].company_id[0]]]);
                }).then(function(companies){
                    self.set('company',companies[0]);

                    return self.fetch('res.partner',['contact_address'],[['id','=',companies[0].partner_id[0]]]);
                }).then(function(company_partners){
                    self.get('company').contact_address = company_partners[0].contact_address;

                    return self.fetch('res.currency',['symbol','position','rounding','accuracy'],[['id','=',self.get('company').currency_id[0]]]);
                }).then(function(currencies){
                    self.set('currency',currencies[0]);

                    return self.fetch('product.uom', null, null);
                }).then(function(units){
                    self.set('units',units);
                    var units_by_id = {};
                    for(var i = 0, len = units.length; i < len; i++){
                        units_by_id[units[i].id] = units[i];
                    }
                    self.set('units_by_id',units_by_id);

                    return self.fetch('product.packaging', null, null);
                }).then(function(packagings){
                    self.set('product.packaging',packagings);

                    return self.fetch('res.users', ['name','ean13'], [['ean13', '!=', false]]);
                }).then(function(users){
                    self.set('user_list',users);

                    return self.fetch('res.partner', ['name','ean13'], [['ean13', '!=', false]]);
                }).then(function(partners){
                    self.set('partner_list',partners);

                    return self.fetch('account.tax', ['amount', 'price_include', 'type']);
                }).then(function(taxes){
                    self.set('taxes', taxes);

                    return self.fetch(
                        'pos.session',
                        ['id', 'journal_ids','name','user_id','config_id','start_at','stop_at'],
                        [['state', '=', 'opened'], ['user_id', '=', self.session.uid]]
                    );
                }).then(function(sessions){
                    self.set('pos_session', sessions[0]);

                    return self.fetch(
                        'pos.config',
                        ['name','journal_ids','shop_id','journal_id',
                         'iface_self_checkout', 'iface_led', 'iface_cashdrawer',
                         'iface_payment_terminal', 'iface_electronic_scale', 'iface_barscan', 'iface_vkeyboard',
                         'iface_print_via_proxy','iface_cashdrawer','state','sequence_id','session_ids', 'iva_compensation', 'show_all_products','order_seq_start_from'],
                        [['id','=', self.get('pos_session').config_id[0]]]
                    );
                }).then(function(configs){
                    var pos_config = configs[0];
                    self.set('pos_config', pos_config);
                    self.iface_electronic_scale    =  !!pos_config.iface_electronic_scale;
                    self.iface_print_via_proxy     =  !!pos_config.iface_print_via_proxy;
                    self.iface_vkeyboard           =  !!pos_config.iface_vkeyboard;
                    self.iface_self_checkout       =  !!pos_config.iface_self_checkout;
                    self.iface_cashdrawer          =  !!pos_config.iface_cashdrawer;
                    self.order_number              =  pos_config.order_seq_start_from;

                    return self.fetch('sale.shop',[],[['id','=',pos_config.shop_id[0]]]);
                }).then(function(shops){
                    self.set('shop',shops[0]);

                    return self.fetch('product.packaging',['ean','product_id']);
                }).then(function(packagings){
                    self.db.add_packagings(packagings);

                    return self.fetch('pos.category', ['id','name','parent_id','child_id','image'])
                }).then(function(categories){
                    self.db.add_categories(categories);

                    return self.fetch(
                        'product.product',
                        ['name', 'list_price','price','pos_categ_id', 'taxes_id', 'ean13',
                         'to_weight', 'uom_id', 'uos_id', 'uos_coeff', 'mes_type', 'description_sale', 'description',
                         'tpv_list_ids','sale_price_ids'],
                        [['sale_ok','=',true],['available_in_pos','=',true]],
                        {pricelist: self.get('shop').pricelist_id[0]} // context for price
                    );
                    
                }).then(function(products){
                	
                	_.each(products,function(product) {                		
                		if(product.sale_price_ids.length > 0){
	                		let alternativePrice = [];
	                		_.each(product.sale_price_ids,function(sale_id) {	                			 
	                			self.fetch('product.price', ['price'], [['id','=',sale_id]]).then(function(sale_obj){
	                				alternativePrice.push(sale_obj[0]);
	                			});
	                        });
	                		product.sale_price_ids = alternativePrice;
                	    }
                    });
                	
                	self.db.add_products(products);
                	
                    return self.fetch(
                        'account.bank.statement',
                        ['account_id','currency','journal_id','state','name','user_id','pos_session_id'],
                        [['state','=','open'],['pos_session_id', '=', self.get('pos_session').id]]
                    );
                }).then(function(bank_statements){
                    var journals = new Array();
                    _.each(bank_statements,function(statement) {
                        journals.push(statement.journal_id[0])
                    });
                    self.set('bank_statements', bank_statements);
                    return self.fetch('account.journal', undefined, [['id','in', journals]]);
                }).then(function(journals){
                    self.set('journals',journals);

                    // associate the bank statements with their journals.
                    var bank_statements = self.get('bank_statements');
                    for(var i = 0, ilen = bank_statements.length; i < ilen; i++){
                        for(var j = 0, jlen = journals.length; j < jlen; j++){
                            if(bank_statements[i].journal_id[0] === journals[j].id){
                                bank_statements[i].journal = journals[j];
                                bank_statements[i].self_checkout_payment_method = journals[j].self_checkout_payment_method;
                            }
                        }
                    }
                    self.set({'cashRegisters' : new module.CashRegisterCollection(self.get('bank_statements'))});
                });
            
            return loaded;
        },

        // logs the usefull posmodel data to the console for debug purposes
        log_loaded_data: function(){
        	
            console.log('PosModel data has been loaded:');
            console.log('PosModel: units:',this.get('units'));
            console.log('PosModel: bank_statements:',this.get('bank_statements'));
            console.log('PosModel: journals:',this.get('journals'));
            console.log('PosModel: taxes:',this.get('taxes'));
            console.log('PosModel: pos_session:',this.get('pos_session'));
            console.log('PosModel: pos_config:',this.get('pos_config'));
            console.log('PosModel: cashRegisters:',this.get('cashRegisters'));
            console.log('PosModel: shop:',this.get('shop'));
            console.log('PosModel: company:',this.get('company'));
            console.log('PosModel: currency:',this.get('currency'));
            console.log('PosModel: user_list:',this.get('user_list'));
            console.log('PosModel: user:',this.get('user'));
            console.log('PosModel: acquirer:',this.get('bank-select'));
            console.log('PosModel: card_type:',this.get('card-select'));
            console.log('PosModel: card_number:',this.get('card_number'));
            console.log('PosModel: approval_number:',this.get('approval_number'));
            console.log('PosModel: lot_number:',this.get('lot_number'));
            console.log('PosModel: reference:',this.get('reference'));
            console.log('PosModel.session:',this.session);
            console.log('PosModel end of data log.');
        },

        // this is called when an order is removed from the order collection. It ensures that there is always an existing
        // order and a valid selected order
        on_removed_order: function(removed_order){
            if( this.get('orders').isEmpty()){
                this.add_new_order();
            }
            if( this.get('selectedOrder') === removed_order){
                this.set({ selectedOrder: this.get('orders').last() });
            }
        },

        // saves the order locally and try to send it to the backend. 'record' is a bizzarely defined JSON version of the Order
        push_order: function(record) {
        	//alert(JSON.stringify(record));
            this.db.add_order(record);
            this.flush();
        },

        //creates a new empty order and sets it as the current order
        add_new_order: function(){
            var order = new module.Order({pos:this});
            this.get('orders').add(order);
            this.set('selectedOrder', order);
        },

        // attemps to send all pending orders ( stored in the pos_db ) to the server,
        // and remove the successfully sent ones from the db once
        // it has been confirmed that they have been sent correctly.
        flush: function() {
            //TODO make the mutex work
            //this makes sure only one _int_flush is called at the same time
            /*
            return this.flush_mutex.exec(_.bind(function() {
                return this._flush(0);
            }, this));
            */
            this._flush(0);
        },
        // attempts to send an order of index 'index' in the list of order to send. The index
        // is used to skip orders that failed. do not call this method outside the mutex provided
        // by flush()
        _flush: function(index){
            var self = this;
            var orders = this.db.get_orders();
            self.set('nbr_pending_operations',orders.length);

            var order  = orders[index];
            if(!order){
                return;
            }
            //try to push an order to the server
            // shadow : true is to prevent a spinner to appear in case of timeout
            (new instance.web.Model('pos.order')).call('create_from_ui',[[order]],undefined,{ shadow:true })
                .fail(function(unused, event){
                    //don't show error popup if it fails
                    event.preventDefault();
                    console.error('Failed to send order:',order);
                    self._flush(index+1);
                })
                .done(function(){                	 
                	self.order_number += 1;
                	//remove from db if success
                    self.db.remove_order(order.id);
                    self._flush(index);
                });
        },

        scan_product: function(parsed_ean){
            var self = this;
            var product = this.db.get_product_by_ean13(parsed_ean.base_ean);
            var selectedOrder = this.get('selectedOrder');

            if(!product){
                return false;
            }

            if(parsed_ean.type === 'price'){
            	if(product.secondary_price > 0){
            		selectedOrder.addProduct(new module.Product(product), {price:secondary_price});
                }
            	else{
            		selectedOrder.addProduct(new module.Product(product), {price:parsed_ean.value});
            	}
            }else if(parsed_ean.type === 'weight'){
                selectedOrder.addProduct(new module.Product(product), {quantity:parsed_ean.value, merge:false});
            }else{
                selectedOrder.addProduct(new module.Product(product));
            }
            return true;
        },
    });

    module.Order = Backbone.Model.extend({
        initialize: function(attributes){
            Backbone.Model.prototype.initialize.apply(this, arguments);
            this.set({
                creationDate:   new Date(),
                orderLines:     new module.OrderlineCollection(),
                paymentLines:   new module.PaymentlineCollection(),
                name:           "Order " + this.generateUniqueId(),
                client:         null,
                acquirer:       null,
                card_type:      null,
                card_number:    null,
                approval_number:null,
                lot_number:     null,
                reference:      null
            });
            this.pos =     attributes.pos;
            this.selected_orderline = undefined;
            this.screen_data = {};  // see ScreenSelector
            this.receipt_type = 'receipt';  // 'receipt' || 'invoice'
            return this;
        },
        generateUniqueId: function() {
            //return new Date().getTime();       	 
        	return this.attributes.pos.order_number;
        },
        addProduct: function(product, options){
            options = options || {};
            var attr = product.toJSON();
            attr.pos = this.pos;
            attr.order = this;
            var line = new module.Orderline({}, {pos: this.pos, order: this, product: product});

            if(options.quantity !== undefined){
                line.set_quantity(options.quantity);
            }
            if(options.price !== undefined){
                line.set_unit_price(options.price);
            }

            var last_orderline = this.getLastOrderline();
            if( last_orderline && last_orderline.can_be_merged_with(line) && options.merge !== false){
                last_orderline.merge(line);
            }else{
                this.get('orderLines').add(line);
            }
            this.selectLine(this.getLastOrderline());
        },
        removeOrderline: function( line ){
            this.get('orderLines').remove(line);
            this.selectLine(this.getLastOrderline());
        },
        getLastOrderline: function(){
            return this.get('orderLines').at(this.get('orderLines').length -1);
        },
        addPaymentLine: function(cashRegister) {
            var paymentLines = this.get('paymentLines');
            var newPaymentline = new module.Paymentline({},{cashRegister:cashRegister});
            
            if (cashRegister.get('journal').type !== 'cash'){
            	globalType = true;
                newPaymentline.set_amount( this.getDueLeft());
                $('.pos-payment-container .footer .left-block').eq(1).css('display', '');
            	$('.pos-payment-container .footer .right-block').eq(1).css('display', '');
            	$('.header').eq(0).css('display', '');
            	
            }
            else {
            	globalType = false;
            	$('.pos-payment-container .footer .left-block').eq(1).css('display', 'none');
            	$('.pos-payment-container .footer .right-block').eq(1).css('display', 'none');
            	$('.header').eq(0).css('display', 'none');
            }
            
            if (cashRegister.get('journal').type === 'bank') {
            	globalType = true;
            }
            
            paymentLines.add(newPaymentline);
            
            //Destroying the payment lines of type 
            //not equal than cash if globalType == false;
            if (globalType === false) {
            	var i = 0;
            	while (i < 10) {
		            this.get('paymentLines').each(function(paymentline){
		        		if (paymentline.cashregister.get('journal').type !== 'cash') {
		        			paymentline.destroy();
		        		}
		            });		            
		            i++;
            	}
            }
        },
        getName: function() {
            return this.get('name');
        },
        getSubtotal : function(){
        	var pos_config = this.pos.get('pos_config');
        	
//            if (globalType) {
//            	return (this.get('orderLines')).reduce((function(sum, orderLine){
//                    return sum + orderLine.get_display_price() - ( orderLine.get_display_price() * pos_config.iva_compensation / 100 );
//                }), 0);
//            }
            
            return (this.get('orderLines')).reduce((function(sum, orderLine){
                return sum + orderLine.get_display_price();
            }), 0);
        },
        getTotalTaxIncluded: function() {
            return (this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_with_tax();
            }), 0);
        },
        getTotalTaxIncludedBaseIva: function(iva_compensation) {
        	return (this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + orderLine.get_tax_v2(iva_compensation);
            }), 0);
		},
        getDiscountTotal: function() {
            return (this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + (orderLine.get_unit_price() * (orderLine.get_discount()/100) * orderLine.get_quantity());
            }), 0);
        },
        getTotalTaxExcluded: function() {
            return (this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + orderLine.get_price_without_tax();
            }), 0);
        },
        getTax: function() {
            return (this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + orderLine.get_tax();
            }), 0);
        },
        getPaidTotal: function() {
            return (this.get('paymentLines')).reduce((function(sum, paymentLine) {
                return sum + paymentLine.get_amount();
            }), 0);
        },
        getChange: function() {
            return this.getPaidTotal() - this.getTotalTaxIncluded();
        },
        getDueLeft: function() {
        	return this.getTotalTaxIncluded() - this.getPaidTotal();
        },
        getIvaCompensation: function() {
        	if (globalType) {
        		var pos_config = this.pos.get('pos_config');
        		return this.getSubtotal() * pos_config.iva_compensation / 100;
        	}
        	else {
        		return 0.0;
        	}
        },
        getIvaZero: function() {
            return (this.get('orderLines')).reduce((function(sum, orderLine) {
                return sum + orderLine.get_tax_zero();
            }), 0);
        },
        // sets the type of receipt 'receipt'(default) or 'invoice'
        set_receipt_type: function(type){
            this.receipt_type = type;
        },
        get_receipt_type: function(){
            return this.receipt_type;
        },
        // the client related to the current order.
        set_client: function(client){
            this.set('client',client);
        },
        get_client: function(){
            return this.get('client');
        },
        get_client_name: function(){
            var client = this.get('client');
            return client ? client.name : "";
        },
        // the client related to the current order.
        set_acquirer: function(acquirer){
            this.set('bank-select',acquirer);
        },
        get_acquirer: function(){
            return this.get('bank-select');
        },
        get_acquirer_name: function(){
            var acquirer = this.get('bank-select');
            return acquirer ? acquirer.name : "";
        },
        // the client related to the current order.
        set_card_type: function(card_type){
            this.set('card-select',card_type);
        },
        get_card_type: function(){
            return this.get('card-select');
        },
        set_card_type_name: function(){
            var card_type = this.get('card-select');
            return card_type ? card_type.name : "";
        },
        // the client related to the current order.
        set_card_number: function(card_number){
            this.set('card_number',card_number);
        },
        set_card_number: function(){
            return this.get('card_number');
        },
        // the order also stores the screen status, as the PoS supports
        // different active screens per order. This method is used to
        // store the screen status.
        set_screen_data: function(key,value){
            if(arguments.length === 2){
                this.screen_data[key] = value;
            }else if(arguments.length === 1){
                for(key in arguments[0]){
                    this.screen_data[key] = arguments[0][key];
                }
            }
        },
        //see set_screen_data
        get_screen_data: function(key){
            return this.screen_data[key];
        },
        // exports a JSON for receipt printing
        export_for_printing: function(){
            var orderlines = [];
            this.get('orderLines').each(function(orderline){
                orderlines.push(orderline.export_for_printing());
            });

            var paymentlines = [];
            this.get('paymentLines').each(function(paymentline){
                paymentlines.push(paymentline.export_for_printing());
            });
            var client  = this.get('client');
            var cashier = this.pos.get('cashier') || this.pos.get('user');
            var company = this.pos.get('company');
            var shop    = this.pos.get('shop');
            var acquirer    = this.pos.get('bank-select');
            var card_type    = this.pos.get('card-select');
            var card_number    = this.pos.get('card_number');
            var date = new Date();

            return {
                orderlines: orderlines,
                paymentlines: paymentlines,
                subtotal: this.getSubtotal(),
                total_with_tax: this.getTotalTaxIncluded(),
                total_without_tax: this.getTotalTaxExcluded(),
                total_tax: this.getTax(),
                total_paid: this.getPaidTotal(),
                total_discount: this.getDiscountTotal(),
                change: this.getChange(),
                name : this.getName(),
                client: client ? client.name : null ,
                invoice_id: null,   //TODO
                cashier: cashier ? cashier.name : null,
                acquirer: acquirer ? acquirer.name : null,
                card_type: card_type ? card_type.name : null,
                card_number: card_number,
                date: {
                    year: date.getFullYear(),
                    month: date.getMonth(),
                    date: date.getDate(),       // day of the month
                    day: date.getDay(),         // day of the week
                    hour: date.getHours(),
                    minute: date.getMinutes()
                },
                company:{
                    email: company.email,
                    website: company.website,
                    company_registry: company.company_registry,
                    contact_address: company.contact_address,
                    vat: company.vat,
                    name: company.name,
                    phone: company.phone,
                },
                shop:{
                    name: shop.name,
                },
                currency: this.pos.get('currency'),
            };
        },
        exportAsJSON: function() {
            var orderLines, paymentLines;
            orderLines = [];
            (this.get('orderLines')).each(_.bind( function(item) {
                return orderLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            paymentLines = [];
            (this.get('paymentLines')).each(_.bind( function(item) {
                return paymentLines.push([0, 0, item.export_as_JSON()]);
            }, this));

            iva_comp =  0;
            if(globalType === true)
            {
                iva_comp = this.pos.get('pos_config').iva_compensation;
            }

            return {
                name: this.getName(),
                amount_paid: this.getPaidTotal(),
                amount_total: this.getTotalTaxIncluded(),
                amount_tax: this.getTax(),
                amount_return: this.getChange(),
                lines: orderLines,
                statement_ids: paymentLines,
                pos_session_id: this.pos.get('pos_session').id,
                partner_id: this.pos.get('client') ? this.pos.get('client').id : undefined,
                user_id: this.pos.get('cashier') ? this.pos.get('cashier').id : this.pos.get('user').id,
                acquirer: this.pos.get('bank-select') ? this.pos.get('bank-select').id : undefined,
                card_type: this.pos.get('card-select') ? this.pos.get('bank-select').id : undefined,
                card_number: this.pos.get('card_number'),
                customer: this.pos.get('selectedOrder').get_client() ? this.pos.get('selectedOrder').get_client().id : undefined,
                iva_compensation: iva_comp
            };
        },
        getSelectedLine: function(){
            return this.selected_orderline;
        },
        selectLine: function(line){
            if(line){
                if(line !== this.selected_orderline){
                    if(this.selected_orderline){
                        this.selected_orderline.set_selected(false);
                    }
                    this.selected_orderline = line;
                    this.selected_orderline.set_selected(true);
                }
            }else{
                this.selected_orderline = undefined;
            }
        }
    });
    
    module.Orderline = module.Orderline.extend({
    	get_tax_v2: function(iva_compensation) {
            //return this.get_all_prices().priceWithTaxBaseIva;
        },
        get_tax_zero: function() {
            return this.get_all_prices().taxzero;
        },
        get_all_prices: function(){
            var self = this;
            var currency_rounding = this.pos.get('currency').rounding;
            var base = round_pr(this.get_quantity() * this.get_unit_price() * (1.0 - (this.get_discount() / 100.0)), currency_rounding);
            
            if (globalType) {
            	var pos_config = this.pos.get('pos_config');
            	base = round_pr(this.get_quantity() * this.get_unit_price() * (1.0 - (this.get_discount() / 100.0) - (pos_config.iva_compensation / 100.0)), currency_rounding);
            }
            
            var totalTax = base;
            var totalNoTax = base;
            
            var product_list = this.pos.get('product_list');
            var product =  this.get_product(); 
            var taxes_ids = product.get('taxes_id');
            var taxes =  self.pos.get('taxes');

            var taxtotal = 0;
            var totalTaxZero = 0.0;

            _.each(taxes_ids, function(el) {
                var tax = _.detect(taxes, function(t) {return t.id === el;});
                if (tax.price_include) {
                    var tmp;

                    if (tax.amount == 0.0) {
                        totalTaxZero += self.get_quantity() * self.get_unit_price();
                    }

                    if (tax.type === "percent") {
                        tmp =  base - round_pr(base / (1 + tax.amount),currency_rounding);
                    } else if (tax.type === "fixed") {
                        tmp = round_pr(tax.amount * self.get_quantity(),currency_rounding);
                    } else {
                        throw "This type of tax is not supported by the point of sale: " + tax.type;
                    }
                    tmp = round_pr(tmp,currency_rounding);
                    taxtotal += tmp;
                    totalNoTax -= tmp;
                } else {
                    var tmp;

                    if (tax.amount == 0.0) {
                        totalTaxZero += self.get_quantity() * self.get_unit_price();
                    }

                    if (tax.type === "percent") {
                        tmp = tax.amount * base;
                    } else if (tax.type === "fixed") {
                        tmp = tax.amount * self.get_quantity();
                    } else {
                        throw "This type of tax is not supported by the point of sale: " + tax.type;
                    }
                    
                    tmp = round_pr(tmp, currency_rounding);
                    taxtotal += tmp;
                    totalTax += tmp;
                }
            });
            
            return {
                "priceWithTax": totalTax,
                "priceWithoutTax": totalNoTax,
                "tax": taxtotal,
                "taxzero": totalTaxZero
            };
        },
    });
    
    module.Orderline = module.Orderline.extend({
    	export_as_JSON: function() {
    		var pos_config = this.pos.get('pos_config');
            iva_comp = 0;
            if (globalType === true) {
                iva_comp = this.get_unit_price() * pos_config.iva_compensation/100;
            }
            return {
                qty: this.get_quantity(),
                price_unit: this.get_unit_price(),
                discount: this.get_discount(),
                product_id: this.get_product().get('id'),
                iva_compensation: iva_comp
            };
        },
    });
};

openerp.point_of_sale = function(instance) {
    instance.point_of_sale = {};
    var module = instance.point_of_sale;

    openerp_pos_db(instance, module);            // import db.js
    openerp_pos_models(instance, module);        // import pos_models.js
    openerp_pos_basewidget(instance, module);    // import pos_basewidget.js
    openerp_pos_keyboard(instance, module);      // import pos_keyboard_widget.js
    openerp_pos_scrollbar(instance, module);     // import pos_scrollbar_widget.js
    openerp_pos_screens(instance, module);       // import pos_screens.js
    openerp_pos_widgets(instance, module);       // import pos_widgets.js
    openerp_pos_devices(instance, module);       // import pos_devices.js

    my_pos_data(instance, module);               // import my_pos_models/pos.js
    my_pos_header(instance);                     // import my_pos_models/pos.js
    my_pos_partner(instance);                    // import my_pos_models/pos.js
    
    instance.web.client_actions.add('pos.ui', 'instance.point_of_sale.PosWidget');
};