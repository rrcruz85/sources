banks= [];
cards_type= [];

openerp.my_point_of_sale = function(instance) {
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

    var module = instance.point_of_sale;
    var round_pr = instance.web.round_precision;

    instance.point_of_sale.ProductListWidget.include({
        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
            this.model = options.model;
            this.productwidgets = [];
            this.weight = options.weight || 0;
            this.show_scale = options.show_scale || false;
            this.next_screen = options.next_screen || false;

            this.click_product_handler = function (event) {
                var product_id = this.dataset['productId'];
                var product = self.pos.db.get_product_by_id(this.dataset['productId']);
                if(product.lots)
                {
                    new_lots = [];
                    for(var i = 0 ; i < product.lots.length; i++)
                    {
                        if(product.lots[i][2] > 0)
                        {
                            new_lots.push(product.lots[i]);
                        }
                    }
                    if(new_lots.length > 0)
                    {
                        product.lots = new_lots;
                        $("div.pos-topheader div.order-selector").css('display', 'none');
                        self.pos_widget.screen_selector.set_current_screen('productlotlist', params = new_lots);
                    }
                    else
                    {
                        product.lots = null;
                    }
                }
                else
                {
                    var objStockProdLot = new instance.web.Model("stock.production.lot");
                    context = {}
                    objStockProdLot.call('search', [[['product_id', '=', product.id]]], context).then(function (record_ids) {
                        if (record_ids.length > 0) {
                            objStockProdLot.call('get_lots', [[record_ids]], context).then(function (quants) {
                                if (quants.length > 0) {
                                    for(var id in self.pos.db.product_by_id)
                                    {
                                        if(id == product_id)
                                        {
                                            self.pos.db.product_by_id[id].lots = quants;
                                            break;
                                        }
                                    }
                                    $("div.pos-topheader div.order-selector").css('display', 'none');
                                    self.pos_widget.screen_selector.set_current_screen('productlotlist', params = quants);
                                }
                            }, function (err, event) {
                                console.log(err);
                                event.preventDefault();
                                self.pos_widget.screen_selector.show_popup('error', {
                                    'message': _t('Error'),
                                    'comment': _t('Could not Load the lots of this product.Your Internet connection is probably down.'),
                                });
                            });
                        }
                    }, function (err, event) {
                        console.log(err);
                        event.preventDefault();
                        self.pos_widget.screen_selector.show_popup('error', {
                            'message': _t('Error'),
                            'comment': _t('Could not Load the lots of this product.Your Internet connection is probably down.'),
                        });
                    });
                }
                options.click_product_action(product);
            };

            this.product_list = options.product_list || [];
            this.product_cache = new module.DomCache();
        },

        renderElement: function() {
            var self = this;
            var el_str = openerp.qweb.render(this.template, {widget: this});
            var el_node = document.createElement('div');

            el_node.innerHTML = el_str;
            el_node = el_node.childNodes[1];

            if (this.el && this.el.parentNode) {
                this.el.parentNode.replaceChild(el_node, this.el);
            }

            this.el = el_node;
            var list_container = el_node.querySelector('.product-list');
            var order = self.pos.get('selectedOrder');

            for (var i = 0, len = this.product_list.length; i < len; i++) {
                this.product_list[i].stock_qty = order.pos.db.product_by_id[this.product_list[i].id].stock_qty;
                if(this.product_list[i].tpv_list_ids.length > 0){
                    if (this.product_list[i].tpv_list_ids.indexOf(this.pos.config.id) > -1) {
                        if(this.product_list[i].stock_qty > 0 ) {
                            var product_node = this.render_product(this.product_list[i]);
                            product_node.addEventListener('click', this.click_product_handler);
                            list_container.appendChild(product_node);
                        }
                    }
                }
                else{
                    if(this.product_list[i].stock_qty > 0 ) {
                        var product_node = this.render_product(this.product_list[i]);
                        product_node.addEventListener('click', this.click_product_handler);
                        list_container.appendChild(product_node);
                    }
                }
            }
            $('span.product').css("height", "135px");
        },

        render_product: function (product) {
            var image_url = this.get_product_image_url(product);
            var product_html = QWeb.render('Product', {
                widget: this,
                product: product,
                image_url: this.get_product_image_url(product),
            });
            var product_node = document.createElement('div');
            product_node.innerHTML = product_html;
            product_node = product_node.childNodes[1];
            var cached = this.product_cache.get_node(product.id);
            if (!cached) {
                this.product_cache.cache_node(product.id, product_node);
            }
            return product_node;
        },
    });

    instance.point_of_sale.PosModel = Backbone.Model.extend({
        initialize: function(session, attributes) {
            Backbone.Model.prototype.initialize.call(this, attributes);
            var  self = this;
            this.session = session;
            this.flush_mutex = new $.Mutex();                   // used to make sure the orders are sent to the server once at time
            this.pos_widget = attributes.pos_widget;

            this.proxy = new module.ProxyDevice(this);              // used to communicate to the hardware devices via a local proxy
            this.barcode_reader = new module.BarcodeReader({'pos': this, proxy:this.proxy, patterns: {}});  // used to read barcodes
            this.proxy_queue = new module.JobQueue();           // used to prevent parallels communications to the proxy
            this.db = new module.PosDB();                       // a local database used to search trough products and categories & store pending orders
            this.debug = jQuery.deparam(jQuery.param.querystring()).debug !== undefined;    //debug mode

            // Business data; loaded from the server at launch
            this.accounting_precision = 2; //TODO
            this.company_logo = null;
            this.company_logo_base64 = '';
            this.currency = null;
            this.shop = null;
            this.company = null;
            this.user = null;
            this.users = [];
            this.partners = [];
            this.cashier = null;
            this.cashregisters = [];
            this.bankstatements = [];
            this.taxes = [];
            this.pos_session = null;
            this.config = null;
            this.units = [];
            this.units_by_id = {};
            this.pricelist = null;
            this.order_sequence = 1;
            window.posmodel = this;

            // these dynamic attributes can be watched for change by other models or widgets
            this.set({
                'synch':            { state:'connected', pending:0 },
                'orders':           new module.OrderCollection(),
                'selectedOrder':    null,
            });

            this.bind('change:synch',function(pos,synch){
                clearTimeout(self.synch_timeout);
                self.synch_timeout = setTimeout(function(){
                    if(synch.state !== 'disconnected' && synch.pending > 0){
                        self.set('synch',{state:'disconnected', pending:synch.pending});
                    }
                },3000);
            });

            this.get('orders').bind('remove', function(order,_unused_,options){
                self.on_removed_order(order,options.index,options.reason);
            });

            // We fetch the backend data on the server asynchronously. this is done only when the pos user interface is launched,
            // Any change on this data made on the server is thus not reflected on the point of sale until it is relaunched.
            // when all the data has loaded, we compute some stuff, and declare the Pos ready to be used.
            this.ready = this.load_server_data()
                .then(function(){
                    if(self.config.use_proxy){
                        return self.connect_to_proxy();
                    }
                });

        },

        // releases ressources holds by the model at the end of life of the posmodel
        destroy: function(){
            // FIXME, should wait for flushing, return a deferred to indicate successfull destruction
            // this.flush();
            this.proxy.close();
            this.barcode_reader.disconnect();
            this.barcode_reader.disconnect_from_proxy();
        },
        connect_to_proxy: function(){
            var self = this;
            var  done = new $.Deferred();
            this.barcode_reader.disconnect_from_proxy();
            this.pos_widget.loading_message(_t('Connecting to the PosBox'),0);
            this.pos_widget.loading_skip(function(){
                    self.proxy.stop_searching();
                });
            this.proxy.autoconnect({
                    force_ip: self.config.proxy_ip || undefined,
                    progress: function(prog){
                        self.pos_widget.loading_progress(prog);
                    },
                }).then(function(){
                    if(self.config.iface_scan_via_proxy){
                        self.barcode_reader.connect_to_proxy();
                    }
                }).always(function(){
                    done.resolve();
                });
            return done;
        },

        // helper function to load data from the server. Obsolete use the models loader below.
        fetch: function(model, fields, domain, ctx){
            this._load_progress = (this._load_progress || 0) + 0.05;
            this.pos_widget.loading_message(_t('Loading')+' '+model,this._load_progress);
            return new instance.web.Model(model).query(fields).filter(domain).context(ctx).all()
        },

        // Server side model loaders. This is the list of the models that need to be loaded from
        // the server. The models are loaded one by one by this list's order. The 'loaded' callback
        // is used to store the data in the appropriate place once it has been loaded. This callback
        // can return a deferred that will pause the loading of the next module.
        // a shared temporary dictionary is available for loaders to communicate private variables
        // used during loading such as object ids, etc.
        models: [
        {
            model:  'res.users',
            fields: ['name','company_id'],
            ids:    function(self){ return [self.session.uid]; },
            loaded: function(self,users){ self.user = users[0]; },
        },{
            model:  'res.company',
            fields: [ 'currency_id', 'email', 'website', 'company_registry', 'vat', 'name', 'phone', 'partner_id' , 'country_id', 'tax_calculation_rounding_method','warranty'],
            ids:    function(self){ return [self.user.company_id[0]] },
            loaded: function(self,companies){ self.company = companies[0]; },
        },{
            model:  'decimal.precision',
            fields: ['name','digits'],
            loaded: function(self,dps){
                self.dp  = {};
                for (var i = 0; i < dps.length; i++) {
                    self.dp[dps[i].name] = dps[i].digits;
                }
            },
        },{
            model:  'product.uom',
            fields: [],
            domain: null,
            context: function(self){ return { active_test: false }; },
            loaded: function(self,units){
                self.units = units;
                var units_by_id = {};
                for(var i = 0, len = units.length; i < len; i++){
                    units_by_id[units[i].id] = units[i];
                    units[i].groupable = ( units[i].category_id[0] === 1 );
                    units[i].is_unit   = ( units[i].id === 1 );
                }
                self.units_by_id = units_by_id;
            }
        },{
            model:  'res.users',
            fields: ['name','ean13'],
            domain: null,
            loaded: function(self,users){ self.users = users; },
        },{
            model:  'res.partner',
            fields: ['name', 'street', 'city', 'state_id', 'country_id', 'vat', 'phone', 'zip', 'mobile', 'email',
                     'ean13', 'write_date', 'contact_address', 'ced_ruc', 'type_ced_ruc'
            ],
            domain: [['customer','=',true]],
            loaded: function(self,partners){
                self.partners = partners;
                self.db.add_partners(partners);
            },
        },{
            model:  'res.country',
            fields: ['name'],
            loaded: function(self,countries){
                self.countries = countries;
                self.company.country = null;
                for (var i = 0; i < countries.length; i++) {
                    if (countries[i].id === self.company.country_id[0]){
                        self.company.country = countries[i];
                    }
                }
            },
        },{
            model:  'account.tax',
            fields: ['name','amount', 'price_include', 'include_base_amount', 'type', 'child_ids', 'child_depend', 'include_base_amount'],
            domain: null,
            loaded: function(self, taxes){
                self.taxes = taxes;
                self.taxes_by_id = {};
                _.each(taxes, function(tax){
                    self.taxes_by_id[tax.id] = tax;
                });
                _.each(self.taxes_by_id, function(tax) {
                    tax.child_taxes = {};
                    _.each(tax.child_ids, function(child_tax_id) {
                        tax.child_taxes[child_tax_id] = self.taxes_by_id[child_tax_id];
                    });
                });
            },
        },{
            model:  'pos.session',
            fields: ['id', 'journal_ids','name','user_id','config_id','start_at','stop_at','sequence_number','login_number'],
            domain: function(self){ return [['state','=','opened'],['user_id','=',self.session.uid]]; },
            loaded: function(self,pos_sessions){
                self.pos_session = pos_sessions[0];

                var orders = self.db.get_orders();
                for (var i = 0; i < orders.length; i++) {
                    self.pos_session.sequence_number = Math.max(self.pos_session.sequence_number, orders[i].data.sequence_number+1);
                }
            },
        },{
            model: 'pos.config',
            fields: [],
            domain: function(self){ return [['id','=', self.pos_session.config_id[0]]]; },
            loaded: function(self,configs){
                self.config = configs[0];
                self.config.use_proxy = self.config.iface_payment_terminal ||
                                        self.config.iface_electronic_scale ||
                                        self.config.iface_print_via_proxy  ||
                                        self.config.iface_scan_via_proxy   ||
                                        self.config.iface_cashdrawer;

                self.barcode_reader.add_barcode_patterns({
                    'product':  self.config.barcode_product,
                    'cashier':  self.config.barcode_cashier,
                    'client':   self.config.barcode_customer,
                    'weight':   self.config.barcode_weight,
                    'discount': self.config.barcode_discount,
                    'price':    self.config.barcode_price,
                });

                if (self.config.company_id[0] !== self.user.company_id[0]) {
                    throw new Error(_t("Error: The Point of Sale User must belong to the same company as the Point of Sale. You are probably trying to load the point of sale as an administrator in a multi-company setup, with the administrator account set to the wrong company."));
                }
            },
        },{
            model: 'stock.location',
            fields: [],
            ids:    function(self){ return [self.config.stock_location_id[0]]; },
            loaded: function(self, locations){ self.shop = locations[0]; },
        },{
            model:  'product.pricelist',
            fields: ['currency_id'],
            ids:    function(self){ return [self.config.pricelist_id[0]]; },
            loaded: function(self, pricelists){ self.pricelist = pricelists[0]; },
        },{
            model: 'res.currency',
            fields: ['name','symbol','position','rounding','accuracy'],
            ids:    function(self){ return [self.pricelist.currency_id[0]]; },
            loaded: function(self, currencies){
                self.currency = currencies[0];
                if (self.currency.rounding > 0) {
                    self.currency.decimals = Math.ceil(Math.log(1.0 / self.currency.rounding) / Math.log(10));
                } else {
                    self.currency.decimals = 0;
                }

            },
        },{
            model: 'product.packaging',
            fields: ['ean','product_tmpl_id'],
            domain: null,
            loaded: function(self, packagings){
                self.db.add_packagings(packagings);
            },
        },{
            model:  'pos.category',
            fields: ['id','name','parent_id','child_id','image'],
            domain: null,
            loaded: function(self, categories){
                self.db.add_categories(categories);
            },
        },{
            model:  'product.product',
            fields: ['display_name', 'list_price','price','pos_categ_id', 'taxes_id', 'ean13', 'default_code',
                     'to_weight', 'uom_id', 'uos_id', 'uos_coeff', 'mes_type', 'description_sale', 'description',
                     'product_tmpl_id', 'tpv_list_ids','stock_qty','company_id'],
            domain: [['sale_ok','=',true],['available_in_pos','=',true]],
            context: function(self){ return { pricelist: self.pricelist.id, display_default_code: false }; },
            loaded: function(self, products){
                self.db.add_products(products);
            },
        },{
            model:  'account.bank.statement',
            fields: ['account_id','currency','journal_id','state','name','user_id','pos_session_id'],
            domain: function(self){ return [['state', '=', 'open'],['pos_session_id', '=', self.pos_session.id]]; },
            loaded: function(self, bankstatements, tmp){
                self.bankstatements = bankstatements;

                tmp.journals = [];
                _.each(bankstatements,function(statement){
                    tmp.journals.push(statement.journal_id[0]);
                });
            },
        },{
            model:  'account.journal',
            fields: [],
            domain: function(self,tmp){ return [['id','in',tmp.journals]]; },
            loaded: function(self, journals){
                self.journals = journals;

                // associate the bank statements with their journals.
                var bankstatements = self.bankstatements;
                for(var i = 0, ilen = bankstatements.length; i < ilen; i++){
                    for(var j = 0, jlen = journals.length; j < jlen; j++){
                        if(bankstatements[i].journal_id[0] === journals[j].id){
                            bankstatements[i].journal = journals[j];
                        }
                    }
                }
                self.cashregisters = bankstatements;
            },
        },{
            label: 'fonts',
            loaded: function(self){
                var fonts_loaded = new $.Deferred();

                // Waiting for fonts to be loaded to prevent receipt printing
                // from printing empty receipt while loading Inconsolata
                // ( The font used for the receipt )
                waitForWebfonts(['Lato','Inconsolata'], function(){
                    fonts_loaded.resolve();
                });

                // The JS used to detect font loading is not 100% robust, so
                // do not wait more than 5sec
                setTimeout(function(){
                    fonts_loaded.resolve();
                },5000);

                return fonts_loaded;
            },
        },{
            label: 'pictures',
            loaded: function(self){
                self.company_logo = new Image();
                var  logo_loaded = new $.Deferred();
                self.company_logo.onload = function(){
                    var img = self.company_logo;
                    var ratio = 1;
                    var targetwidth = 300;
                    var maxheight = 150;
                    if( img.width !== targetwidth ){
                        ratio = targetwidth / img.width;
                    }
                    if( img.height * ratio > maxheight ){
                        ratio = maxheight / img.height;
                    }
                    var width  = Math.floor(img.width * ratio);
                    var height = Math.floor(img.height * ratio);
                    var c = document.createElement('canvas');
                        c.width  = width;
                        c.height = height
                    var ctx = c.getContext('2d');
                        ctx.drawImage(self.company_logo,0,0, width, height);

                    self.company_logo_base64 = c.toDataURL();
                    logo_loaded.resolve();
                };
                self.company_logo.onerror = function(){
                    logo_loaded.reject();
                };
                    self.company_logo.crossOrigin = "anonymous";
                self.company_logo.src = '/web/binary/company_logo' +'?_'+Math.random();

                return logo_loaded;
            },
        },
        ],

        // loads all the needed data on the sever. returns a deferred indicating when all the data has loaded.
        load_server_data: function(){
            var self = this;
            var loaded = new $.Deferred();
            var progress = 0;
            var progress_step = 1.0 / self.models.length;
            var tmp = {}; // this is used to share a temporary state between models loaders

            function load_model(index){
                if(index >= self.models.length){
                    loaded.resolve();
                }else{
                    var model = self.models[index];
                    self.pos_widget.loading_message(_t('Loading')+' '+(model.label || model.model || ''), progress);
                    var fields =  typeof model.fields === 'function'  ? model.fields(self,tmp)  : model.fields;
                    var domain =  typeof model.domain === 'function'  ? model.domain(self,tmp)  : model.domain;
                    var context = typeof model.context === 'function' ? model.context(self,tmp) : model.context;
                    var ids     = typeof model.ids === 'function'     ? model.ids(self,tmp) : model.ids;
                    progress += progress_step;

                    if( model.model ){
                        if (model.ids) {
                            var records = new instance.web.Model(model.model).call('read',[ids,fields],context);
                        } else {
                            var records = new instance.web.Model(model.model).query(fields).filter(domain).context(context).all()
                        }
                        records.then(function(result){
                                try{    // catching exceptions in model.loaded(...)

                                    result_filtered = []
                                    if(model.model == "product.product")
                                    {
                                        for(var i = 0; i < result.length; i++)
                                        {
                                            //Filtrando los productos que tengan stock >0, que no tengan una compañia
                                            //o que tengan una compañia asignada y coincida con la que tiene configurada el
                                            //punto de venta
                                            if(result[i].stock_qty > 0  && (result[i].company_id  == false || (result[i].company_id != false &&  result[i].company_id[0] == self.config.company_id[0])))
                                            {
                                                result_filtered.push(result[i]);
                                            }
                                        }
                                        result = result_filtered;
                                    }

                                    $.when(model.loaded(self,result,tmp))
                                        .then(function(){ load_model(index + 1); },
                                              function(err){ loaded.reject(err); });
                                }catch(err){
                                    loaded.reject(err);
                                }
                            },function(err){
                                loaded.reject(err);
                            });
                    }else if( model.loaded ){
                        try{    // catching exceptions in model.loaded(...)
                            $.when(model.loaded(self,tmp))
                                .then( function(){ load_model(index +1); },
                                        function(err){ loaded.reject(err); });
                        }catch(err){
                            loaded.reject(err);
                        }
                    }else{
                        load_model(index + 1);
                    }
                }
            }

            try{
                load_model(0);
            }catch(err){
                loaded.reject(err);
            }

            //Cargando los bancos
            new instance.web.Model('res.bank')
                .query(['name'])
                .filter([['active', '=', 'true']])
                .all({'timeout': 3000, 'shadow': true})
                .then(function (list_banks) {
                    for (var i = 0, len = list_banks.length; i < len; i++) {
                        banks.push({id: list_banks[i].id, name: list_banks[i].name});
                    }
                });
            //Cargando los tipos de tarjetas
            new instance.web.Model('pos.credit_card')
                .query(['name'])
                .filter([['is_active', '=', 'true']])
                .all({'timeout': 3000, 'shadow': true})
                .then(function (credit_cards) {
                    for (var i = 0, len = credit_cards.length; i < len; i++) {
                        cards_type.push({id: credit_cards[i].id, name: credit_cards[i].name});
                    }
                });

            return loaded;
        },

        // reload the list of partner, returns as a deferred that resolves if there were
        // updated partners, and fails if not
        load_new_partners: function(){
            var self = this;
            var def  = new $.Deferred();
            var fields = _.find(this.models,function(model){ return model.model === 'res.partner'; }).fields;
            new instance.web.Model('res.partner')
                .query(fields)
                .filter([['write_date','>',this.db.get_partner_write_date()]])
                .all({'timeout':3000, 'shadow': true})
                .then(function(partners){
                    if (self.db.add_partners(partners)) {   // check if the partners we got were real updates
                        def.resolve();
                    } else {
                        def.reject();
                    }
                }, function(err,event){ event.preventDefault(); def.reject(); });
            return def;
        },

        // this is called when an order is removed from the order collection. It ensures that there is always an existing
        // order and a valid selected order
        on_removed_order: function(removed_order,index,reason){
            if( (reason === 'abandon' || removed_order.temporary) && this.get('orders').size() > 0){
                // when we intentionally remove an unfinished order, and there is another existing one
                this.set({'selectedOrder' : this.get('orders').at(index) || this.get('orders').last()});
            }else{
                // when the order was automatically removed after completion,
                // or when we intentionally delete the only concurrent order
                this.add_new_order();
            }
        },

        //creates a new empty order and sets it as the current order
        add_new_order: function(){
            var order = new module.Order({pos:this});
            this.get('orders').add(order);
            this.set('selectedOrder', order);
        },

        get_order: function(){
            return this.get('selectedOrder');
        },

        showMessageCreateOrder: function(){
            var self = this;
            if (self.db.get_orders().length > 0) {
                $('div.loader').removeClass('oe_hidden');
                $('div.loader-feedback').removeClass('oe_hidden');
                $('div.loader-feedback div.skip').addClass('my_class');
                $('div.loader-feedback div.skip').removeClass('button');
                $('div.loader-feedback div.skip').removeClass('oe_hidden');
                $('div.loader-feedback div.skip').removeClass('skip');

                $('div.loader-feedback div.my_class').addClass('fa').addClass('fa-spinner').addClass('fa-spin');
                $('div.loader-feedback div.my_class').css('font-size','48px');
                $('div.loader-feedback div.my_class').text('');

                $('div.loader-feedback h1.message').text("Creating Order");
                $('div.loader').css('opacity', 10);
                var cont = 0;
                var interval = setInterval(function () {
                    $('div.progressbar div.progress').css('width', cont.toString() + '%');

                    cont += 1;
                    if (cont > 100) {
                        cont = 0;
                        clearInterval(interval);
                        return;
                    }
                }, 100);
            }
        },

        hideMessageCreateOrder: function () {
            $('div.loader').addClass('oe_hidden');
            $('div.loader-feedback').addClass('oe_hidden');
            $('div.loader-feedback h1.message').text("Loading");
            $('div.progressbar div.progress').css('width', '0%');
            $('div.loader').css('opacity', 0);

            $('div.loader-feedback div.my_class').addClass('button');
            $('div.loader-feedback div.my_class').addClass('oe_hidden');
            $('div.loader-feedback div.my_class').addClass('skip');
            $('div.loader-feedback div.my_class').removeClass('fa');
            $('div.loader-feedback div.my_class').removeClass('fa-spinner');
            $('div.loader-feedback div.my_class').removeClass('fa-spin');
            $('div.loader-feedback div.my_class').text('skip');
            $('div.loader-feedback div.my_class').removeClass('my_class');

        },
        //removes the current order
        delete_current_order: function(){
            this.get('selectedOrder').destroy({'reason':'abandon'});
        },

        // saves the order locally and try to send it to the backend.
        // it returns a deferred that succeeds after having tried to send the order and all the other pending orders.
        push_order: function(order) {
            var self = this;

            if(order){
                this.proxy.log('push_order',order.export_as_JSON());
                this.db.add_order(order.export_as_JSON());
            }

            var pushed = new $.Deferred();

            //Showing Creating Order Message
            self.showMessageCreateOrder();

            this.flush_mutex.exec(function(){
                var flushed = self._flush_orders(self.db.get_orders());
                flushed.always(function(ids){
                    if(order != undefined)
                        order.order_id = ids.length > 0 ? ids[0] : 0;
                    pushed.resolve();

                    //Hidding Creating Message
                    self.hideMessageCreateOrder();

                });
            });
            return pushed;
        },

        // saves the order locally and try to send it to the backend and make an invoice
        // returns a deferred that succeeds when the order has been posted and successfully generated
        // an invoice. This method can fail in various ways:
        // error-no-client: the order must have an associated partner_id. You can retry to make an invoice once
        //     this error is solved
        // error-transfer: there was a connection error during the transfer. You can retry to make the invoice once
        //     the network connection is up

        push_and_invoice_order: function(order){
            var self = this;
            var invoiced = new $.Deferred();

            if(!order.get_client()){
                invoiced.reject('error-no-client');
                return invoiced;
            }

            //Showing Creating Order Message
            self.showMessageCreateOrder();

            var order_id = this.db.add_order(order.export_as_JSON());

            this.flush_mutex.exec(function(){
                var done = new $.Deferred(); // holds the mutex

                // send the order to the server
                // we have a 30 seconds timeout on this push.
                // FIXME: if the server takes more than 30 seconds to accept the order,
                // the client will believe it wasn't successfully sent, and very bad
                // things will happen as a duplicate will be sent next time
                // so we must make sure the server detects and ignores duplicated orders

                var transfer = self._flush_orders([self.db.get_order(order_id)], {timeout:30000, to_invoice:true});

                transfer.fail(function(){
                    //Hidding Creating Message
                    self.hideMessageCreateOrder();

                    invoiced.reject('error-transfer');
                    done.reject();
                });

                // on success, get the order id generated by the server
                transfer.pipe(function(order_server_id){

                    // generate the pdf and download it
                    self.pos_widget.do_action('point_of_sale.pos_invoice_report',{additional_context:{
                        active_ids:order_server_id,
                    }});

                    invoiced.resolve();
                    done.resolve();

                    //Hidding Creating Message
                    self.hideMessageCreateOrder();

                });

                return done;

            });

            return invoiced;
        },

        // wrapper around the _save_to_server that updates the synch status widget
        _flush_orders: function(orders, options) {
            var self = this;

            this.set('synch',{ state: 'connecting', pending: orders.length});

            return self._save_to_server(orders, options).done(function (server_ids) {
                var pending = self.db.get_orders().length;

                self.set('synch', {
                    state: pending ? 'connecting' : 'connected',
                    pending: pending
                });

                return server_ids;
            });
        },

        // send an array of orders to the server
        // available options:
        // - timeout: timeout for the rpc call in ms
        // returns a deferred that resolves with the list of
        // server generated ids for the sent orders
        _save_to_server: function (orders, options) {
            if (!orders || !orders.length) {
                var result = $.Deferred();
                result.resolve([]);
                return result;
            }

            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 15000 * orders.length;

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var posOrderModel = new instance.web.Model('pos.order');

            return posOrderModel.call('create_from_ui',
                [_.map(orders, function (order) {
                                        order.to_invoice = options.to_invoice || false;
                                        return order;
                })],
                undefined,
                {
                    shadow: !options.to_invoice,
                    timeout: timeout
                }
            ).then(function (server_ids) {
                _.each(orders, function (order) {
                    self.db.remove_order(order.id);
                });
                return server_ids;
            }).fail(function (error, event){
                if(error.code === 200 ){    // Business Logic Error, not a connection problem
                    self.pos_widget.screen_selector.show_popup('error-traceback',{
                        message: error.data.message,
                        comment: error.data.debug
                    });
                }
                // prevent an error popup creation by the rpc failure
                // we want the failure to be silent as we send the orders in the background
                event.preventDefault();
                console.error('Failed to send orders:', orders);
            });
        },

        scan_product: function(parsed_code){
            var self = this;
            var selectedOrder = this.get('selectedOrder');
            if(parsed_code.encoding === 'ean13'){
                var product = this.db.get_product_by_ean13(parsed_code.base_code);
            }else if(parsed_code.encoding === 'reference'){
                var product = this.db.get_product_by_reference(parsed_code.code);
            }

            if(!product){
                return false;
            }

            if(parsed_code.type === 'price'){
                selectedOrder.addProduct(product, {price:parsed_code.value});
            }else if(parsed_code.type === 'weight'){
                selectedOrder.addProduct(product, {quantity:parsed_code.value, merge:false});
            }else if(parsed_code.type === 'discount'){
                selectedOrder.addProduct(product, {discount:parsed_code.value, merge:false});
            }else{
                selectedOrder.addProduct(product);
            }
            return true;
        },
    });

    instance.point_of_sale.Order = instance.point_of_sale.Order.extend({

        initialize: function (attributes) {
            Backbone.Model.prototype.initialize.apply(this, arguments);
            this.pos = attributes.pos;
            this.sequence_number = this.pos.pos_session.sequence_number++;
            this.uid = this.generateUniqueId();
            this.set({
                creationDate: new Date(),
                orderLines: new module.OrderlineCollection(),
                paymentLines: new module.PaymentlineCollection(),
                name: _t("Order ") + this.uid,
                client: null,
                selectedLot: null,
            });
            this.selected_orderline = undefined;
            this.selected_paymentline = undefined;
            this.screen_data = {};  // see ScreenSelector
            this.receipt_type = 'receipt';  // 'receipt' || 'invoice'
            this.temporary = attributes.temporary || false;
            this.order_id = 0;
            this.apply_taxes = true;
            this.total = 0.0;
            return this;
        },

        get_config_iva_compensation: function(){
            return this.pos.config.iva_compensation;
        },

        get_config_card_comition: function(){
            return this.pos.config.card_comition;
        },

        addPaymentline: function(cashregister) {

            var paymentLines = this.get('paymentLines');
            var newPaymentline = new module.Paymentline({}, {cashregister: cashregister, pos: this.pos});

            paymentLines.add(newPaymentline);
            this.selectPaymentline(newPaymentline);
        },

        getSelectedPaymentline: function () {
            return this.selected_paymentline;
        },

        export_for_printing: function () {
            var orderlines = [];
            this.get('orderLines').each(function (orderline) {
                orderlines.push(orderline.export_for_printing());
            });

            var paymentlines = [];
            this.get('paymentLines').each(function (paymentline) {
                paymentlines.push(paymentline.export_for_printing());
            });
            var client = this.get('client');
            var cashier = this.pos.cashier || this.pos.user;
            var company = this.pos.company;
            var shop = this.pos.shop;
            var date = new Date();

            return {
                orderlines: orderlines,
                paymentlines: paymentlines,
                subtotal: this.getSubtotal(),
                total_with_tax: this.apply_taxes ? this.getTotalTaxIncluded(): this.getTotalTaxExcluded(),
                total_without_tax: this.getTotalTaxExcluded(),
                total_tax: this.apply_taxes ? this.getTax() : 0,
                total_paid: this.getPaidTotal(),
                total_discount: this.getDiscountTotal(),
                tax_details: this.apply_taxes ? this.getTaxDetails() : {},
                change: this.getChange(),
                name: this.getName(),
                client: client ? client.name : null,
                invoice_id: null,   //TODO
                cashier: cashier ? cashier.name : null,
                header: this.pos.config.receipt_header || '',
                footer: this.pos.config.receipt_footer || '',
                precision: {
                    price: 2,
                    money: 2,
                    quantity: 3,
                },
                date: {
                    year: date.getFullYear(),
                    month: date.getMonth(),
                    date: date.getDate(),       // day of the month
                    day: date.getDay(),         // day of the week
                    hour: date.getHours(),
                    minute: date.getMinutes(),
                    isostring: date.toISOString(),
                    localestring: date.toLocaleString(),
                },
                company: {
                    email: company.email,
                    website: company.website,
                    company_registry: company.company_registry,
                    contact_address: company.partner_id[1],
                    vat: company.vat,
                    name: company.name,
                    phone: company.phone,
                    logo: this.pos.company_logo_base64,
                },
                shop: {
                    name: shop.name,
                },
                currency: this.pos.currency,
            };
        },

        export_as_JSON: function () {
            var orderLines, paymentLines;
            orderLines = [];

            (this.get('orderLines')).each(_.bind(function (item) {
                return orderLines.push([0, 0, item.export_as_JSON()]);
            }, this));

            paymentLines = [];
            (this.get('paymentLines')).each(_.bind(function (item) {
                return paymentLines.push([0, 0, item.export_as_JSON()]);
            }, this));

            var obj = {
                state: 'paid',
                name: this.getName(),
                lines: orderLines,
                statement_ids: paymentLines,
                amount_return: this.getChange(),
                pos_session_id: this.pos.pos_session.id,
                partner_id: this.get_client() ? this.get_client().id : false,
                user_id: this.pos.cashier ? this.pos.cashier.id : this.pos.user.id,
                uid: this.uid,
                sequence_number: this.sequence_number,
                apply_taxes : this.apply_taxes
            };
            return obj;
        },

        getTotalWithTaxesCompensation: function() {
            var val = round_pr(this.getPaidTotal(), this.pos.currency.rounding);
            return val;
        },

        getTaxesCompensation: function() {
            var val = round_pr((this.get('paymentLines')).reduce((function(sum, paymentLine) {
                return sum + paymentLine.get_iva_compensation();
            }), 0), this.pos.currency.rounding);
            return val;
        },

        getTotalCardComition: function() {
            var objs = this.get('paymentLines').models;
            var total = 0;
            for(var i = 0; i < objs.length; i++)
            {
                if(objs[i].get_type() == 'card') {
                    total += objs[i].get_card_comition();
                }
            }
            return round_pr(total , this.pos.currency.rounding);
        },

        getTaxes: function() {
            var objs = this.get('paymentLines').models;
            var total = 0;
            for(var i = 0; i < objs.length; i++)
            {
                total += objs[i].get_tax();
            }
            return round_pr(total, this.pos.currency.rounding);
        },

        getDueLeft: function() {
            var val = this.getTotalTaxIncluded() - this.getPaidTotal();
            return val;
        },

        getPaidTotal: function () {
            var val = round_pr((this.get('paymentLines')).reduce((function (sum, paymentLine) {
                return sum + paymentLine.get_amount();
            }), 0), this.pos.currency.rounding);
            return val;
        },

        getIvaZero: function() {
            return 0.0
        },

        getTotalTaxIncluded: function() {
            var totalPaid = this.getTotalTaxExcluded() + this.getTax();
            return totalPaid;
        },

        getChange: function() {
            var paidTotal = this.getPaidTotal();
            var totalTaxIncluded = this.getTotalTaxExcluded() + this.getTotalCardComition() + this.getTaxes();

            //var iva_comp = $('.payment-taxes-compensation').html();
            //iva_comp = parseFloat(iva_comp.substring(0, iva_comp.indexOf(' ')));
            var val  = paidTotal - totalTaxIncluded;
            if(val < 0)
                val = 0.0;
            return val;
        },

        getTaxDetails: function(){
            var self = this;
            var taxes = [];
            var fulldetails = [];

            //Group Taxes
            this.get('paymentLines').each(function(line){
                var ltaxes = line.get_taxes();
                for(var i = 0 ; i < ltaxes.length; i++)
                {
                    var existe = false;
                    var pos = 0;
                    for(var j = 0; j < taxes.length; j++)
                    {
                        if(taxes[j].id == ltaxes[i].id)
                        {
                            existe = true;
                            pos = j;
                            break;
                        }
                    }
                    if (!existe)
                    {
                        taxes.push({id: ltaxes[i].id, tax : ltaxes[i].tax});
                    }
                    else
                    {
                        taxes[pos].tax +=  ltaxes[i].tax;
                    }
                }
            });

            for(var i = 0 ; i < taxes.length; i++)
            {
                fulldetails.push({amount: taxes[i].tax, tax: self.pos.taxes_by_id[taxes[i].id], name: self.pos.taxes_by_id[taxes[i].id].name});
            }

            return fulldetails;
        },

        // the selected lot related to the current order.
        set_selected_lot: function (lot) {
            this.set('selectedLot', lot);
        },
        get_selected_lot: function () {
            return this.get('selectedLot');
        },
        get_selected_qty: function () {
            var lot = this.get('selectedLot');
            return lot ? lot.qty : 0;
        },
        removeAllPaymentlines: function () {
            var self = this;
            for(var i =0; i<  this.get('paymentLines').models.length; i++)
            {
                self.pos.get('selectedOrder').removePaymentline(this.get('paymentLines').models[i]);
            }
        },

        getTax_2: function () {
            return round_pr((this.get('orderLines')).reduce((function (sum, orderLine) {
                return sum + orderLine.get_tax_2();
            }), 0), this.pos.currency.rounding);
        },

        get_applicable_taxes: function () {
            var lines = this.get('orderLines');
            var taxes = [];
            lines.each(function(line){
                var product_taxes = line.get_applicable_taxes();
                for(var i = 0 ; i < product_taxes.length; i++)
                {
                    var exist_tax = false;
                    for(var j = 0; j < taxes.length; j++)
                    {
                        if(taxes[j].id == product_taxes[i].id)
                        {
                            exist_tax = true;
                            break;
                        }
                    }

                    if(!exist_tax)
                    {
                        taxes.push({id: product_taxes[i].id, amount: product_taxes[i].amount});
                    }
                }
            });
            return taxes;
        },

        get_total: function () {
            return this.total;
        },

        set_total: function (total) {
            this.total = total;
        }
    });

    var orderline_id = 1;

    instance.point_of_sale.Orderline = instance.point_of_sale.Orderline.extend({

        initialize: function (attr, options) {
            this.pos = options.pos;
            this.order = options.order;
            this.product = options.product;
            this.price = options.product.price;
            this.set_quantity(1);
            this.discount = 0;
            this.selectedLot = null;
            this.discountStr = '0';
            this.type = 'unit';
            this.selected = false;
            this.id = orderline_id++;
        },

        get_selected_lot: function(){
            return this.selectedLot;
        },

        get_selected_lot_name: function(){
            if(this.selectedLot)
                return "Lot: " + this.selectedLot.name;
            return "";
        },

        set_selected_lot: function (lot) {
            this.selectedLot = lot;
        },

        set_lot_qty: function (qty) {
            if(this.selectedLot)
                this.selectedLot.qty = qty;
        },

        get_all_prices_whit_compensation: function() {

            var base = round_pr(this.get_quantity() * this.get_unit_price() * (1.0 - (this.get_discount() / 100.0)), currency_rounding);

            var totalTax = base;
            var totalNoTax = base;
            var taxtotal = 0;

            var product =  this.get_product();
            var taxes_ids = product.taxes_id;
            var taxes =  this.pos.taxes;
            var taxdetail = {};
            var product_taxes = [];

            _(taxes_ids).each(function(el){
                product_taxes.push(_.detect(taxes, function(t){
                    return t.id === el;
                }));
            });

            var all_taxes = _(this.compute_all(product_taxes, base)).flatten();

            _(all_taxes).each(function(tax) {
                if (tax.price_include) {
                    totalNoTax -= tax.amount;
                } else {
                    totalTax += tax.amount;
                }
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });
            totalNoTax = round_pr(totalNoTax, this.pos.currency.rounding);

            return {
                "priceWithTax": totalTax,
                "priceWithoutTax": totalNoTax,
                "tax": taxtotal,
                "taxDetails": taxdetail,
            };
        },

        get_tax_compensation: function() {
            return round_pr((this.get_unit_price() * this.get_quantity() - this.get_tax()), this.pos.currency.rounding);
        },

        //used to create a json of the ticket, to be sent to the printer
        export_for_printing: function () {

            var order = this.pos.get('selectedOrder');
            return {
                quantity: this.get_quantity(),
                unit_name: this.get_unit().name,
                price: this.get_unit_price(),
                discount: this.get_discount(),
                product_name: this.get_product().display_name,
                price_display: this.get_display_price(),
                price_with_tax: order.apply_taxes ? this.get_price_with_tax(): this.get_price_without_tax(),
                price_without_tax: this.get_price_without_tax(),
                tax: order.apply_taxes ? this.get_tax(): 0,
                product_description: this.get_product().description,
                product_description_sale: this.get_product().description_sale,
            };
        },

        export_as_JSON: function() {
            return {
                qty: this.get_quantity(),
                price_unit: this.get_unit_price(),
                discount: this.get_discount(),
                product_id: this.get_product().id,
                lot_id: this.get_selected_lot() != null ? this.get_selected_lot().id : null
            };
        },

        get_all_prices: function(){
            var base = round_pr(this.get_quantity() * this.get_unit_price() * (1.0 - (this.get_discount() / 100.0)), this.pos.currency.rounding);
            var totalTax = base;
            var totalNoTax = base;
            var taxtotal = 0;

            var product =  this.get_product();
            var taxes_ids = product.taxes_id;
            var taxes =  this.pos.taxes;
            var taxdetail = {};
            var product_taxes = [];

            _(taxes_ids).each(function(el){
                product_taxes.push(_.detect(taxes, function(t){
                    return t.id === el;
                }));
            });

            var all_taxes = _(this.compute_all(product_taxes, base)).flatten();

            _(all_taxes).each(function(tax) {
                if (tax.price_include) {
                    totalNoTax -= tax.amount;
                } else {
                    totalTax += tax.amount;
                }
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });
            totalNoTax = round_pr(totalNoTax, this.pos.currency.rounding);

            var order = this.pos.get('selectedOrder');

            return {
                "priceWithTax": order.apply_taxes ? totalTax : totalNoTax,
                "priceWithoutTax": totalNoTax,
                "tax": order.apply_taxes ? taxtotal : 0,
                "taxDetails": order.apply_taxes ? taxdetail : {},
            };
        },

        get_all_prices_2: function () {
            var base = round_pr(this.get_quantity() * this.get_unit_price() * (1.0 - (this.get_discount() / 100.0)), this.pos.currency.rounding);
            var totalTax = base;
            var totalNoTax = base;
            var taxtotal = 0;

            var product = this.get_product();
            var taxes_ids = product.taxes_id;
            var taxes = this.pos.taxes;
            var taxdetail = {};
            var product_taxes = [];

            _(taxes_ids).each(function (el) {
                product_taxes.push(_.detect(taxes, function (t) {
                    return t.id === el;
                }));
            });

            var all_taxes = _(this.compute_all(product_taxes, base)).flatten();

            _(all_taxes).each(function (tax) {
                if (tax.price_include) {
                    totalNoTax -= tax.amount;
                } else {
                    totalTax += tax.amount;
                }
                taxtotal += tax.amount;
                taxdetail[tax.id] = tax.amount;
            });
            totalNoTax = round_pr(totalNoTax, this.pos.currency.rounding);

            return {
                "priceWithTax": totalTax,
                "priceWithoutTax": totalNoTax,
                "tax": taxtotal,
                "taxDetails": taxdetail,
            };
        },

        get_tax_2: function () {
            return this.get_all_prices_2().tax;
        },
    });

    instance.point_of_sale.PaymentScreenWidget.include({

        bind_events: function() {

            if(this.old_order){
                this.old_order.unbind(null,null,this);
            }
            var order = this.pos.get('selectedOrder');
            order.bind('change:selected_paymentline',this.focus_selected_line,this);

            this.old_order = order;

            if(this.old_paymentlines){
                this.old_paymentlines.unbind(null,null,this);
            }
            var paymentlines = order.get('paymentLines');
            paymentlines.bind('add', this.add_paymentline, this);
            paymentlines.bind('change:selected', this.rerender_paymentline, this);
            paymentlines.bind('change:amount', function(line){
                if(!line.selected && line.node){
                    line.node.value = line.amount.toFixed(this.pos.currency.decimals);
                }
                this.update_payment_summary(line);
            },this);
            paymentlines.bind('remove', this.remove_paymentline, this);
            paymentlines.bind('all', this.update_payment_summary, this);

            this.old_paymentlines = paymentlines;

            if(this.old_orderlines){
                this.old_orderlines.unbind(null,null,this);
            }
            var orderlines = order.get('orderLines');
            orderlines.bind('all', this.update_payment_summary, this);

            this.old_orderlines = orderlines;
        },

        update_payment_summary: function(param) {

            var currentOrder = this.pos.get('selectedOrder');
            var paymentLines = currentOrder.get('paymentLines');

            var totalOrderWithoutTaxes = currentOrder.getTotalTaxExcluded();
            var taxes = round_pr(currentOrder.getTotalTaxIncluded() - currentOrder.getTotalTaxExcluded(), currentOrder.pos.currency.rounding);

            var totalByCard = 0.0;
            var total_card_comisition = 0.0;
            var total_discount_taxes = 0.0;
            var total_taxes = 0.0;
            var totalOrder = currentOrder.get_total();
            var total_lines = 0.0;

            //Buscando los totales
            for (var i = 0; i < paymentLines.models.length; i++) {
                total_lines += paymentLines.models[i].get_amount();
                if (paymentLines.models[i].get_type() == 'card') {
                    totalByCard += paymentLines.models[i].get_amount();
                    total_card_comisition += paymentLines.models[i].get_card_comition();
                }
                total_taxes += paymentLines.models[i].get_tax();
                total_discount_taxes +=  paymentLines.models[i].get_iva_compensation();
            }

            if(total_taxes > taxes && taxes != 0)
            {
                total_taxes = taxes;
            }

            var paidTotal = currentOrder.getPaidTotal();
            totalOrder = round_pr(totalOrder, currentOrder.pos.currency.rounding);
            var remaining = totalOrder > paidTotal ? totalOrder - paidTotal : 0;
            var change = paidTotal > totalOrder ? paidTotal -  totalOrder: 0;

            this.$('.payment-total-without-taxes').html(this.format_currency(totalOrderWithoutTaxes));
            this.$('.payment-card-comition').html(this.format_currency(total_card_comisition));
            this.$('.payment-taxes-compensation').html(this.format_currency(total_discount_taxes));
            this.$('.payment-taxes').html(this.format_currency(total_taxes));

            this.$('.payment-due-total').html(this.format_currency(totalOrder));
            this.$('.payment-paid-total').html(this.format_currency(paidTotal));
            this.$('.payment-remaining').html(this.format_currency(remaining));
            this.$('.payment-change').html(this.format_currency(change));

            if(this.pos_widget.action_bar){
                var activate = (paidTotal < totalOrder);
                this.pos_widget.action_bar.set_button_disabled('validation', activate);
                this.pos_widget.action_bar.set_button_disabled('invoice', activate);
            }
        },

        is_paid: function(){
            var currentOrder = this.pos.get('selectedOrder');
            var totalWithTaxes =  currentOrder.getTotalTaxIncluded();
            if(currentOrder.apply_taxes == false)
            {
                totalWithTaxes = currentOrder.getTotalTaxExcluded();
            }
            var discount =currentOrder.getPaidTotal() - currentOrder.getTotalTaxExcluded();
            var val1 = round_pr(currentOrder.getPaidTotal() + 0.000001, currentOrder.pos.currency.rounding);
            var val2 = round_pr(totalWithTaxes - discount,  currentOrder.pos.currency.rounding);
            return (totalWithTaxes < 0.000001 || (val1 >= val2));
        },

        init: function (parent, options) {
            var self = this;
            this._super(parent, options);

            this.pos.bind('change:selectedOrder', function () {
                this.bind_events();
                this.renderElement();
            }, this);

            this.bind_events();

            this.decimal_point = instance.web._t.database.parameters.decimal_point;

            this.line_delete_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    self.pos.get('selectedOrder').removePaymentline(node.line);
                    var lines = self.pos.get('selectedOrder').get('paymentLines').models;
                    if(lines.length == 0)
                    {
                        self.back();
                    }
                }
                event.stopPropagation();
            };

            this.line_change_handler = function (event) {
                var node = this;
                 while (node && !node.classList.contains('paymentline')) {
                     node = node.parentNode;
                 }
                if (node) {
                    var amount;
                    try {
                        amount = instance.web.parse_value(this.value, {type: "float"});
                    }
                    catch (e) {
                        amount = 0;
                    }

                    if(node.line.get_old_amount() == 0)
                    {
                        node.line.set_old_amount(node.line.get_amount());
                    }
                    node.line.set_amount(amount);
                }
            };

            this.line_click_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    self.pos.get('selectedOrder').selectPaymentline(node.line);
                }
            };

            this.hotkey_handler = function (event) {
                if (event.which === 13) {
                    self.validate_order();
                } else if (event.which === 27) {
                    self.back();
                }
            };

            this.line_change_check_number_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.check_number = this.value;
                }
            };

            this.line_change_check_bank_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.bank_id = this.value;
                }
            };

            this.line_change_check_date_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.check_date = this.value;
                }
            };

            this.line_change_card_type_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.card_type_id = this.value;
                }
            };

            this.line_change_card_number_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.card_number = this.value;
                }
            };

            this.line_change_approval_number_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.approval_number = this.value;
                }
            };

            this.line_change_lot_number_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.lot_number = this.value;
                }
            };

            this.line_change_reference_handler = function (event) {
                var node = this;
                while (node && !node.classList.contains('paymentline')) {
                    node = node.parentNode;
                }
                if (node) {
                    node.line.reference = this.value;
                }
            };
        },

        add_paymentline: function (line) {

            var currentOrder = this.pos.get('selectedOrder');
            var total = currentOrder.getTotalTaxIncluded();
            var taxes = round_pr(currentOrder.getTotalTaxIncluded() - currentOrder.getTotalTaxExcluded(), currentOrder.pos.currency.rounding);

            var totalAccumulated = 0;
            var totalByCard = 0;
            var paymentLines = currentOrder.get('paymentLines');

            for (var i = 0; i < paymentLines.models.length; i++) {
                totalAccumulated += paymentLines.models[i].get_amount();
                if (paymentLines.models[i].get_type() == 'card') {
                    totalByCard += paymentLines.models[i].get_amount();
                }
            }

            var total_exceeded = false;
            if(totalAccumulated >= total){
                total = 0;
                total_exceeded = true;
            }
            else{
                total -= totalAccumulated;
            }

            if(totalByCard == 0 && line.get_type() == 'card'){
                totalByCard = total;
            }

            //Calculando taxes en base al monto por tarjeta
            if (!currentOrder.apply_taxes) {
                taxes = 0.0;
                var applicables_taxes = currentOrder.get_applicable_taxes();
                for (var i = 0; i < applicables_taxes.length; i++) {
                    taxes += totalByCard * applicables_taxes[i].amount;
                }
            }

            var total_discount_iva = 0.0;

            //Si tiene Iva compensacion
            if (this.pos.config.iva_compensation > 0) {
                total_discount_iva = taxes * this.pos.config.iva_compensation / 100;
                taxes -= total_discount_iva;
                line.set_iva_compensation(total_discount_iva);
            }

            line.set_tax(taxes);

            var total_order = 0.0;
            if (currentOrder.apply_taxes) {
                total_order = total;
            }
            else {
                total_order = total + taxes;
            }

            //Si tiene comision
            if ((this.pos.config.card_comition > 0 && totalByCard > 0) || line.get_type() == 'card') {
                var card_comition = total_order * this.pos.config.card_comition / 100;
                line.set_card_comition(round_pr(card_comition, currentOrder.pos.currency.rounding));
                total_order += card_comition;
            }

            line.set_amount(total_order);

            if(!total_exceeded) {
                if (totalAccumulated == 0) {
                    currentOrder.set_total(total_order);
                }
                else {
                    currentOrder.set_total(totalAccumulated + total_order);
                }
            }

            var list_container = this.el.querySelector('.payment-lines');
            list_container.appendChild(this.render_paymentline(line));

            if (this.numpad_state) {
                this.numpad_state.reset();
            }

            /*if (line.get_type() == 'card' && self.pos.config.card_comition > 0) {
                $("#card_comition").removeClass("oe_hidden");
            }*/
        },

        render_paymentline: function (line) {

            var el_html = openerp.qweb.render('Paymentline', {widget: this, line: line});
            el_html = _.str.trim(el_html);

            var el_node = document.createElement('tbody');
            el_node.innerHTML = el_html;
            el_node = el_node.childNodes[0];
            el_node.line = line;
            el_node.querySelector('.paymentline-delete')
                .addEventListener('click', this.line_delete_handler);
            el_node.addEventListener('click', this.line_click_handler);
            el_node.querySelector('input.paymentline-input')
                .addEventListener('keyup', this.line_change_handler);

            var nodeSelect = '';
            if(line.get_type() == 'check') {
                nodeSelect = el_node.querySelector('#check-bank-select');
                //Seteando Valores
                el_node.querySelector('#pos_check_number').setAttribute("value",line.check_number);
                el_node.querySelector('#pos_check_date').setAttribute("value",line.check_date);

                el_node.querySelector('#pos_check_number').addEventListener('keyup', this.line_change_check_number_handler);
                el_node.querySelector('#pos_check_date').addEventListener('change', this.line_change_check_date_handler);
                el_node.querySelector('#pos_check_date').addEventListener('keyup', this.line_change_check_date_handler);
            }
            else if (line.get_type() == 'card') {
                nodeSelect = el_node.querySelector('#card-bank-select');
                var card = el_node.querySelector('#card-select');
                if(cards_type.length == 1)
                {
                    line.card_type_id = cards_type[0].id;
                }
                for (var i = 0; i < cards_type.length; i++) {
                    var opt = document.createElement('option');
                    opt.textContent = cards_type[i].name;
                    opt.value = cards_type[i].id;
                    if(line.card_type_id && line.card_type_id == cards_type[i].id) {
                        opt.selected = true;
                    }
                    card.appendChild(opt);
                }
                if (!line.card_type_id) {
                    line.card_type_id = cards_type[0].id;
                }
                card.addEventListener('change', this.line_change_card_type_handler);
                el_node.querySelector('#pos_card_number').setAttribute("value",line.card_number);
                el_node.querySelector('#pos_approval_number').setAttribute("value",line.approval_number);
                el_node.querySelector('#pos_lot_number').setAttribute("value",line.lot_number);
                el_node.querySelector('#pos_reference').setAttribute("value",line.reference);

                el_node.querySelector('#pos_card_number').addEventListener('keyup', this.line_change_card_number_handler);
                el_node.querySelector('#pos_approval_number').addEventListener('keyup', this.line_change_approval_number_handler);
                el_node.querySelector('#pos_lot_number').addEventListener('keyup', this.line_change_lot_number_handler);
                el_node.querySelector('#pos_reference').addEventListener('keyup', this.line_change_reference_handler);
            }

            if(nodeSelect) {
                if(banks.length == 1)
                {
                    line.bank_id = banks[0].id;
                }
                for (var i = 0; i < banks.length; i++) {
                    var opt = document.createElement('option');
                    opt.textContent = banks[i].name;
                    opt.value = banks[i].id;
                    if(line.bank_id && line.bank_id == banks[i].id) {
                        opt.selected = true;
                    }
                    nodeSelect.appendChild(opt);
                }
                if(!line.bank_id)
                {
                    line.bank_id = banks[0].id;
                }
                nodeSelect.addEventListener('change', this.line_change_check_bank_handler);
            }
            line.node = el_node;
            return el_node;
        },

        actualizarStockLotes: function (order, lines) {
            for (var i = 0; i < lines.length; i++) {
                for (var id in order.pos.db.product_by_id) {
                    if (id == lines[i].product.id) {
                        if (lines[i].selectedLot && order.pos.db.product_by_id[id].lots) {
                            for (var y = 0; y < order.pos.db.product_by_id[id].lots.length; y++) {
                                if (order.pos.db.product_by_id[id].lots[y][0] == lines[i].selectedLot.id) {
                                    if (lines[i].selectedLot.qty == lines[i].selectedLot.qty_tmp) {
                                        lines[i].selectedLot.qty -= 1;
                                    }
                                    var diff = lines[i].selectedLot.qty_tmp - lines[i].selectedLot.qty;
                                    order.pos.db.product_by_id[id].lots[y][2] = lines[i].selectedLot.qty;
                                    order.pos.db.product_by_id[id].lots[y][3] = lines[i].selectedLot.qty;
                                    order.pos.db.product_by_id[id].stock_qty -= diff;
                                    lines[i].selectedLot.qty_tmp = lines[i].selectedLot.qty;
                                }
                            }
                        }
                        else {
                            order.pos.db.product_by_id[id].stock_qty -= lines[i].quantity;
                        }
                    }
                }
            }
        },

        validate_order: function (options) {

            var self = this;
            options = options || {};

            var currentOrder = this.pos.get('selectedOrder');
            var slines = currentOrder.get('orderLines').models;
            var plines = currentOrder.get('paymentLines').models;
            if (slines.length === 0) {
                this.pos_widget.screen_selector.show_popup('error', {
                    'message': _t('Empty Order'),
                    'comment': _t('There must be at least one product in your order before it can be validated'),
                });
                return;
            }
            else {
                for (var k = 0; k < slines.length; k++) {
                    if (slines[k] && slines[k].product && slines[k].product.lots && !slines[k].selectedLot) {
                        currentOrder.selectLine(slines[k]);
                        currentOrder.removeAllPaymentlines();
                        alert('You must select one lot for the product: ' + slines[k].product.display_name);
                        this.pos_widget.screen_selector.back();
                        return;
                    }
                }
            }

            for (var i = 0; i < plines.length; i++) {
                if (plines[i].get_type() === 'bank' && plines[i].get_amount() < 0) {
                    this.pos_widget.screen_selector.show_popup('error', {
                        'message': _t('Negative Bank Payment'),
                        'comment': _t('You cannot have a negative amount in a Bank payment. Use a cash payment method to return money to the customer.'),
                    });
                    return;
                }
            }

            if (!this.is_paid()) {
                return;
            }

            // The exact amount must be paid if there is no cash payment method defined.
            if (Math.abs(currentOrder.getTotalTaxIncluded() - currentOrder.getPaidTotal()) > 0.00001) {
                var cash = false;
                for (var i = 0; i < this.pos.cashregisters.length; i++) {
                    cash = cash || (this.pos.cashregisters[i].journal.type === 'cash');
                }
                if (!cash) {
                    this.pos_widget.screen_selector.show_popup('error', {
                        message: _t('Cannot return change without a cash payment method'),
                        comment: _t('There is no cash payment method available in this point of sale to handle the change.\n\n Please pay the exact amount or add a cash payment method in the point of sale configuration'),
                    });
                    return;
                }
            }

            if (this.pos.config.iface_cashdrawer) {
                this.pos.proxy.open_cashbox();
            }

            if (options.invoice) {

                // deactivate the validation button while we try to send the order
                this.pos_widget.action_bar.set_button_disabled('validation', true);
                this.pos_widget.action_bar.set_button_disabled('invoice', true);

                //Creating Order and Invoice
                var invoiced = this.pos.push_and_invoice_order(currentOrder);

                invoiced.fail(function (error) {
                    if (error === 'error-no-client') {
                        self.pos_widget.screen_selector.show_popup('error', {
                            message: _t('An anonymous order cannot be invoiced'),
                            comment: _t('Please select a client for this order. This can be done by clicking the order tab'),
                        });
                    } else {
                        self.pos_widget.screen_selector.show_popup('error', {
                            message: _t('The order could not be sent'),
                            comment: _t('Check your internet connection and try again.'),
                        });
                    }
                    self.pos_widget.action_bar.set_button_disabled('validation', false);
                    self.pos_widget.action_bar.set_button_disabled('invoice', false);
                });

                invoiced.done(function () {
                    self.pos_widget.action_bar.set_button_disabled('validation', false);
                    self.pos_widget.action_bar.set_button_disabled('invoice', false);
                    //Actualizando Stock de los lotes
                    self.actualizarStockLotes(currentOrder, currentOrder.get('orderLines').models);
                    self.pos.get('selectedOrder').destroy();
                });

            } else {

                //Validating the client is selected
                if(currentOrder.get_client() == null || currentOrder.get_client() == undefined) {
                    self.pos_widget.screen_selector.show_popup('error', {
                        message: _t('An anonymous order cannot be created'),
                        comment: _t('Please select a client for this order. This can be done by clicking the order tab'),
                    });
                }
                else{

                    //Creating Order
                    this.pos.push_order(currentOrder);

                    if (this.pos.config.iface_print_via_proxy) {

                        var receipt = currentOrder.export_for_printing();
                        this.pos.proxy.print_receipt(QWeb.render('XmlReceipt', {
                            receipt: receipt, widget: self,
                        }));

                        //Actualizando Stock de los lotes
                        this.actualizarStockLotes(currentOrder, currentOrder.get('orderLines').models);

                        this.pos.get('selectedOrder').destroy();    //finish order and go back to scan screen
                    } else {
                        //Actualizando Stock de los lotes
                        this.actualizarStockLotes(currentOrder, currentOrder.get('orderLines').models);
                        this.pos_widget.screen_selector.set_current_screen(this.next_screen);
                    }

                }
            }

            // hide onscreen (iOS) keyboard
            setTimeout(function () {
                document.activeElement.blur();
                $("input").blur();
            }, 250);
        },

        remove_paymentline: function (line) {
            var self = this;
            line.node.parentNode.removeChild(line.node);
            line.node = undefined;

            if(line.get_type() == 'card'){
                var currentOrder = this.pos.get('selectedOrder');
                var total = currentOrder.get_total();
                total -= line.get_card_comition();
                if(!currentOrder.apply_taxes){
                    total -= line.get_tax();
                }
                currentOrder.set_total(total);
            }

            var paymentLines = self.pos.get('selectedOrder').get('paymentLines');
            if(paymentLines.models.length > 0)
            {
                self.pos.get('selectedOrder').selectPaymentline(paymentLines.models[paymentLines.models.length - 1]);
            }
        },
    });

    instance.point_of_sale.ClientListScreenWidget.include({
        save_client_details: function(partner) {
            var self = this;
            var fields = {}

            this.$('.client-details-contents .detail').each(function(idx, el) {
                fields[el.name] = el.value;
            });

            if (!fields.name) {
                this.pos_widget.screen_selector.show_popup('error', {
                    message: _t('A Customer Name Is Required'),
                });
                return;
            }

            if (this.uploaded_picture) {
                fields.image = this.uploaded_picture;
            }

            fields.id = partner.id || false;
            fields.country_id = fields.country_id || false;
            fields.ean13 = fields.ean13 ? this.pos.barcode_reader.sanitize_ean(fields.ean13) : false;

            new instance.web.Model('res.partner').call('create_from_ui',[fields]).then(function(partner_id) {

                self.pos_widget.screen_selector.show_popup('error', {
                                                       'message': _t('Process OK'),
                                                       'comment': _t('Client Successfully Created!!!!'),
                                                   });

                self.saved_client_details(partner_id);

                self.reload_partners();

            }, function(err, event){
                event.preventDefault();

                if (err.code === 200 ) {
                    self.pos_widget.screen_selector.show_popup('error', {
                        'message': _t('Error: Could not Save Changes'),
                        'comment': err.data.message,
                    });
                }
                else {
                    self.pos_widget.screen_selector.show_popup('error', {
                        'message': _t('Error: Could not Save Changes'),
                        'comment': _t('Your Internet connection is probably down.'),
                    });
                }
            });
        },
    });

    instance.point_of_sale.PosWidget.include({
        build_widgets: function() {
              var self = this;

              // --------  Screens ---------

              this.product_screen = new module.ProductScreenWidget(this,{});
              this.product_screen.appendTo(this.$('.screens'));

              this.receipt_screen = new module.ReceiptScreenWidget(this, {});
              this.receipt_screen.appendTo(this.$('.screens'));

              this.payment_screen = new module.PaymentScreenWidget(this, {});
              this.payment_screen.appendTo(this.$('.screens'));

              this.clientlist_screen = new module.ClientListScreenWidget(this, {});
              this.clientlist_screen.appendTo(this.$('.screens'));

              this.scale_screen = new module.ScaleScreenWidget(this,{});
              this.scale_screen.appendTo(this.$('.screens'));

              this.productlotlist_screen = new module.ProductLotListScreenWidget(this, {});
              this.productlotlist_screen.appendTo(this.$('.screens'));


              // --------  Popups ---------

              this.error_popup = new module.ErrorPopupWidget(this, {});
              this.error_popup.appendTo(this.$el);

              this.error_barcode_popup = new module.ErrorBarcodePopupWidget(this, {});
              this.error_barcode_popup.appendTo(this.$el);

              this.error_traceback_popup = new module.ErrorTracebackPopupWidget(this,{});
              this.error_traceback_popup.appendTo(this.$el);

              this.confirm_popup = new module.ConfirmPopupWidget(this,{});
              this.confirm_popup.appendTo(this.$el);

              this.unsent_orders_popup = new module.UnsentOrdersPopupWidget(this,{});
              this.unsent_orders_popup.appendTo(this.$el);

              // --------  Misc ---------

              this.close_button = new module.HeaderButtonWidget(this,{
                  label: _t('Close'),
                  action: function(){
                      var self = this;
                      if (!this.confirmed) {
                          this.$el.addClass('confirm');
                          this.$el.text(_t('Confirm'));
                          this.confirmed = setTimeout(function(){
                              self.$el.removeClass('confirm');
                              self.$el.text(_t('Close'));
                              self.confirmed = false;
                          },2000);
                      } else {
                          clearTimeout(this.confirmed);
                          this.pos_widget.close();
                      }
                  },
              });
              this.close_button.appendTo(this.$('.pos-rightheader'));

              this.notification = new module.SynchNotificationWidget(this,{});
              this.notification.appendTo(this.$('.pos-rightheader'));

              if(this.pos.config.use_proxy){
                  this.proxy_status = new module.ProxyStatusWidget(this,{});
                  this.proxy_status.appendTo(this.$('.pos-rightheader'));
              }

              this.username   = new module.UsernameWidget(this,{});
              this.username.replace(this.$('.placeholder-UsernameWidget'));

              this.action_bar = new module.ActionBarWidget(this);
              this.action_bar.replace(this.$(".placeholder-RightActionBar"));

              this.paypad = new module.PaypadWidget(this, {});
              this.paypad.replace(this.$('.placeholder-PaypadWidget'));

              this.numpad = new module.NumpadWidget(this);
              this.numpad.replace(this.$('.placeholder-NumpadWidget'));

              this.order_widget = new module.OrderWidget(this, {});
              this.order_widget.replace(this.$('.placeholder-OrderWidget'));

              this.onscreen_keyboard = new module.OnscreenKeyboardWidget(this, {
                  'keyboard_model': 'simple'
              });
              this.onscreen_keyboard.replace(this.$('.placeholder-OnscreenKeyboardWidget'));

              // --------  Screen Selector ---------

              this.screen_selector = new module.ScreenSelector({
                  pos: this.pos,
                  screen_set:{
                      'products': this.product_screen,
                      'payment' : this.payment_screen,
                      'scale':    this.scale_screen,
                      'receipt' : this.receipt_screen,
                      'clientlist': this.clientlist_screen,
                      'productlotlist': this.productlotlist_screen,
                  },
                  popup_set:{
                      'error': this.error_popup,
                      'error-barcode': this.error_barcode_popup,
                      'error-traceback': this.error_traceback_popup,
                      'confirm': this.confirm_popup,
                      'unsent-orders': this.unsent_orders_popup,
                  },
                  default_screen: 'products',
                  default_mode: 'cashier',
              });

              if(this.pos.debug){
                  this.debug_widget = new module.DebugWidget(this);
                  this.debug_widget.appendTo(this.$('.pos-content'));
              }

              this.disable_rubberbanding();

              //Adding Event
              this.el.querySelector('#apply_taxes').addEventListener('click',function (event) {
                  //Storing check status
                  self.pos.get('selectedOrder').apply_taxes = self.el.querySelector('#apply_taxes').checked;
                  if(self.el.querySelector('#apply_taxes').checked == false)
                  {
                      self.el.querySelector('.summary .total .subentry .value').textContent = self.format_currency(0);
                  }
              });
          }
    });

    module.ProductLotListScreenWidget = module.ScreenWidget.extend({
            template: 'ProductLotListScreenWidget',

            init: function(parent, options){
                this._super(parent, options);
                this.product_lots = [];
            },

            show_leftpane: false,

            auto_back: true,

            product_lots : [],

            show: function(){
                var self = this;
                this._super();

                this.old_lot = {};
                this.new_lot = this.old_lot;

                this.renderElement();

                var order = this.pos.get('selectedOrder');
                var last_orderline =  order.getLastOrderline();

                this.$('.back').click(function(){
                    $("div.pos-topheader div.order-selector").css('display', '');
                    self.pos_widget.screen_selector.back();
                });

                this.$('.next').click(function(){
                    //this.save_changes();
                    if (order.selected_orderline) {
                        order.selected_orderline.selectedLot = self.new_lot;
                    }
                    else {
                        var last_orderline = order.getLastOrderline();
                        last_orderline.selectedLot = self.new_lot;
                    }
                    var selected_Lot = self.new_lot;
                    if(selected_Lot != false && selected_Lot != undefined)
                    {
                        //var elem = document.createElement('div');
                        //elem.innerHTML = "Lot: " + selected_Lot.name;
                        if($("ul.orderlines li.selected ul.info-list").length > 0) {
                            //$("ul.orderlines li.selected ul.info-list").prepend(elem);
                            order.selected_orderline.node.childNodes[5].childNodes[1].innerHTML = "Lot: " + selected_Lot.name;
                            var qty = order.selected_orderline.get_quantity();
                            if(selected_Lot.qty <= qty) {
                                order.selected_orderline.set_quantity(selected_Lot.qty);
                                selected_Lot.qty = 0;
                                order.selected_orderline.selectedLot.qty = 0;
                            }
                            else {
                                if(qty > 1) {
                                    order.selected_orderline.set_quantity(qty - 1);
                                    order.selected_orderline.selectedLot.qty-=1;
                                }
                            }
                        }
                        else
                        {
                            order.selectLine(last_orderline);
                        }
                    }
                    $("div.pos-topheader div.order-selector").css('display', '');
                    self.pos_widget.screen_selector.back();
                });

                if(order.screen_data != undefined && order.screen_data.params != undefined
                    && order.screen_data.params != false  && order.screen_data.params.length > 0)
                {
                    this.render_list(order.screen_data.params);
                }

                this.$('.client-list-contents').delegate('.client-line','click',function(event){
                    self.line_select(event,$(this),parseInt($(this).data('id')));
                });

                var search_timeout = null;
            },

            render_list: function (lots) {
                var contents = this.$el[0].querySelector('.client-list-contents');
                contents.innerHTML = "";
                for (var i = 0, len = Math.min(lots.length, 1000); i < len; i++) {
                    var lot = {id: lots[i][0], name : lots[i][1], qty : lots[i][2], qty_tmp : lots[i][2]};
                    this.product_lots.push(lot);
                    var clientline_html = QWeb.render('LotLine', {widget: this, lot: lot});
                    var clientline = document.createElement('tbody');
                    clientline.innerHTML = clientline_html;
                    clientline = clientline.childNodes[1];
                    contents.appendChild(clientline);
                }
            },

            line_select: function (event, $line, id) {
                this.$('.client-list .lowlight').removeClass('lowlight');
                if ($line.hasClass('highlight')) {
                    $line.removeClass('highlight');
                    $line.addClass('lowlight');
                    this.new_lot = null;
                    this.toggle_save_button();
                } else {
                    this.$('.client-list .highlight').removeClass('highlight');
                    $line.addClass('highlight');
                    var lot = {};
                    for (var i = 0; i < this.product_lots.length; i++) {
                        if (this.product_lots[i].id == id) {
                            lot = this.product_lots[i];
                            break;
                        }
                    }
                   this.new_lot = lot;
                   this.toggle_save_button();
                }
            },

            has_client_changed: function () {
                if (this.old_lot && this.new_lot) {
                    return this.old_lot.id !== this.new_lot.id;
                } else {
                    return !!this.old_lot !== !!this.new_lot;
                }
            },

            toggle_save_button: function () {
                var $button = this.$('.button.next');
                $button.toggleClass('oe_hidden', !this.has_client_changed());
            },

            save_changes: function(){
                var order = this.pos.get('selectedOrder');
                if(order.selected_orderline) {
                    order.selected_orderline.selectedLot = this.new_lot;
                }
                else
                {
                    var last_orderline =  order.getLastOrderline();
                    last_orderline.selectedLot = this.new_lot;
                }
            },

            close: function(){
                this._super();
            },
    });

    instance.point_of_sale.NumpadWidget = instance.point_of_sale.NumpadWidget.extend({
        clickAppendNewChar: function (event) {
            var newChar;
            newChar = event.currentTarget.innerText || event.currentTarget.textContent;
            var order = this.pos.get('selectedOrder');
            var pos_widget = this.pos_widget;
            return this.state.appendNewChar(newChar, order, pos_widget);
        },
        clickDeleteLastChar: function() {
            var order = this.pos.get('selectedOrder');
            return this.state.deleteLastChar(order);
        },
    });

    instance.point_of_sale.NumpadState = instance.point_of_sale.NumpadState.extend({

        appendNewChar: function (newChar, order, pos_widget) {
            var oldBuffer;
            oldBuffer = this.get('buffer');
            if (oldBuffer === '0') {
                this.set({
                    buffer: newChar
                });
            } else if (oldBuffer === '-0') {
                this.set({
                    buffer: "-" + newChar
                });
            } else {
                this.set({
                    buffer: (this.get('buffer')) + newChar
                });
            }

            //Actualizando Stock
            if(this.attributes.mode == "quantity")
            {
                if(order.selected_orderline) {
                    var cant_selected = parseInt(this.get('buffer'));
                    if(order.selected_orderline.selectedLot) {
                        if (cant_selected > parseInt(order.selected_orderline.selectedLot.qty_tmp)) {
                            pos_widget.screen_selector.show_popup('error', {
                                message: _t("You selected " + cant_selected.toString() + " units for this product but there are only " + order.selected_orderline.selectedLot.qty_tmp.toString() + " units availables."),
                            });
                            return;
                        }
                        else {
                            for (var id in order.pos.db.product_by_id) {
                                if (id == order.selected_orderline.product.id && order.pos.db.product_by_id[id].lots && order.selected_orderline.selectedLot) {
                                    for (var i = 0; i < order.pos.db.product_by_id[id].lots.length; i++) {
                                        if (order.pos.db.product_by_id[id].lots[i][0] == order.selected_orderline.selectedLot.id) {
                                            var cant = order.pos.db.product_by_id[id].lots[i][3] - parseInt(this.get('buffer'));
                                            order.pos.db.product_by_id[id].lots[i][2] = cant;
                                            order.selected_orderline.selectedLot.qty = cant;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    else
                    {
                        if (cant_selected > parseInt(order.selected_orderline.product.stock_qty)) {
                            pos_widget.screen_selector.show_popup('error',
                                {message:
                                    _t("You selected " + cant_selected.toString() + " units for this product but there are only " + order.selected_orderline.product.stock_qty.toString() + " units availables."),
                                });
                            return;
                        }
                    }
                }
            }
            this.trigger('set_value', this.get('buffer'));
        },

        deleteLastChar: function (order) {
            var self = this;
            self.cant_ant = parseInt(this.get('buffer'));
            if (this.get('buffer') === "") {
                if (this.get('mode') === 'quantity') {
                    this.trigger('set_value', 'remove');
                } else {
                    this.trigger('set_value', this.get('buffer'));
                }
            } else {
                var newBuffer = this.get('buffer').slice(0, -1) || "";
                this.set({buffer: newBuffer});
                this.trigger('set_value', this.get('buffer'));
                if (this.get('mode') === 'quantity' && (!this.attributes.buffer || this.attributes.buffer.length == 0) ) {
                    if(order.selected_orderline && order.selected_orderline.selectedLot)
                    {
                        for(var id in order.pos.db.product_by_id)
                        {
                            if (id == order.selected_orderline.product.id && order.pos.db.product_by_id[id].lots) {
                                for (var i = 0; i < order.pos.db.product_by_id[id].lots.length; i++) {
                                    if (order.pos.db.product_by_id[id].lots[i][0] == order.selected_orderline.selectedLot.id) {
                                        order.pos.db.product_by_id[id].lots[i][2] = order.selected_orderline.selectedLot.qty_tmp;
                                        order.selected_orderline.selectedLot.qty = order.selected_orderline.selectedLot.qty_tmp;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
    });

    instance.point_of_sale.OrderWidget = instance.point_of_sale.OrderWidget.extend({
        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
            this.editable = false;
            this.pos.bind('change:selectedOrder', this.change_selected_order, this);
            this.line_click_handler = function (event) {
                if (!self.editable) {
                    return;
                }
                self.pos.get('selectedOrder').selectLine(this.orderline);
                self.pos_widget.numpad.state.reset();

                if (this.orderline.product && this.orderline.product.lots && !this.orderline.selectedLot) {
                    $("div.pos-topheader div.order-selector").css('display', 'none');
                    self.pos_widget.screen_selector.set_current_screen('productlotlist', params = this.orderline.product.lots);
                    self.pos.get('selectedOrder').selectLine(this.orderline);
                }
            };
            this.client_change_handler = function (event) {
                self.update_summary();
            }
            this.bind_order_events();
        },

        update_payment_summary: function() {
            var self = this;
            var screen = self.pos_widget.screen_selector.get_current_screen();
            self.pos_widget.screen_selector.set_current_screen(screen,null,'refresh');
            var order = self.pos.get('selectedOrder');
            if(order.selected_paymentline != undefined)
            {
                if(!order.apply_taxes) {
                    $('.payment-due-total').html(this.format_currency(order.getTotalTaxExcluded()));
                }
                else
                {
                    $('.payment-due-total').html(this.format_currency(order.getTotalTaxIncluded()));
                    if(order.getTotalTaxIncluded() > order.selected_paymentline.amount)
                    {
                      this.pos_widget.action_bar.set_button_disabled('validation', true);
                      this.pos_widget.action_bar.set_button_disabled('invoice', true);
                    }
                }
            }
        },

        render_orderline: function(orderline){
            var self = this;
            var el_str  = openerp.qweb.render('Orderline',{widget:this, line:orderline});
            var el_node = document.createElement('div');
                el_node.innerHTML = _.str.trim(el_str);
                el_node = el_node.childNodes[0];
                el_node.orderline = orderline;
                el_node.addEventListener('click',this.line_click_handler);

            orderline.node = el_node;

            self.el.querySelector('#apply_taxes').addEventListener('click',function (event) {

                var order = self.pos.get('selectedOrder');
                //Storing check status
                order.apply_taxes = self.el.querySelector('#apply_taxes').checked;
                self.update_summary();
                self.update_payment_summary();
            });
            return el_node;
        },

        renderElement: function(scrollbottom){
            this.pos_widget.numpad.state.reset();

            var order  = this.pos.get('selectedOrder');
            var orderlines = order.get('orderLines').models;

            var el_str  = openerp.qweb.render('OrderWidget',{widget:this, order:order, orderlines:orderlines});

            var el_node = document.createElement('div');
                el_node.innerHTML = _.str.trim(el_str);
                el_node = el_node.childNodes[0];


            var list_container = el_node.querySelector('.orderlines');
            for(var i = 0, len = orderlines.length; i < len; i++){
                var orderline = this.render_orderline(orderlines[i]);
                list_container.appendChild(orderline);
            }

            if(this.el && this.el.parentNode){
                this.el.parentNode.replaceChild(el_node,this.el);
            }
            this.el = el_node;

            //Updating check
            $('#apply_taxes').attr('checked',this.pos.get('selectedOrder').apply_taxes);

            this.update_summary();

            if(scrollbottom){
                this.el.querySelector('.order-scroller').scrollTop = 100 * orderlines.length;
            }
        },

        update_summary: function(){
            var order = this.pos.get('selectedOrder');
            var total     = order ? order.getTotalTaxIncluded() : 0;
            var taxes     = order ? total - order.getTotalTaxExcluded() : 0;

            if(this.el.querySelector('#apply_taxes').checked == false)
            {
                total = order.getTotalTaxExcluded();
                taxes = 0;
            }
            this.el.querySelector('.summary .total > .value').textContent = this.format_currency(total);
            this.el.querySelector('.summary .total .subentry .value').textContent = this.format_currency(taxes);
        },

    });

    instance.point_of_sale.Paymentline = instance.point_of_sale.Paymentline.extend({
        initialize: function (attributes, options) {
            this.amount = 0;
            this.cashregister = options.cashregister;
            this.name = this.cashregister.journal_id[1];
            this.selected = false;
            this.pos = options.pos;
            //New fields added
            this.bank_id= '';
            this.card_number = '';
            this.check_number = '';
            this.check_date = '';
            this.card_type_id= '';
            this.approval_number= '';
            this.lot_number= '';
            this.reference= '';
            this.iva_compensation = 0.0;
            this.old_amount = 0.0;
            this.tax = 0.0;
            this.taxes = [];
            this.card_comition = 0.0;
        },

        get_old_amount: function(){
            return this.old_amount;
        },

        set_old_amount: function(old_amount){
            this.old_amount = old_amount;
        },

        get_tax: function(){
            return this.tax;
        },

        set_tax: function(tax){
            this.tax = tax;
        },

        get_taxes: function(){
            return this.taxes;
        },

        set_taxes: function(tax){
            this.taxes.push(tax);
        },

        get_card_comition: function(){
            return this.card_comition;
        },

        set_card_comition: function(card_comition){
            this.card_comition = card_comition;
        },

        export_as_JSON: function () {

            var obj =  {
                name: instance.web.datetime_to_str(new Date()),
                statement_id: this.cashregister.id,
                account_id: this.cashregister.account_id[0],
                journal_id: this.cashregister.journal_id[0],
                amount: this.get_amount(),
                card_number: this.card_number,
                check_number : this.check_number,
                check_date : this.check_date,
                card_type_id : this.card_type_id,
                bank_id : this.bank_id,
                approval_number : this.approval_number,
                lot_number : this.lot_number,
                reference : this.reference,
                iva_compensation : this.get_iva_compensation(),
                card_comition : this.get_card_comition(),
                taxes : this.get_tax()
            };
            return obj;
        },

        get_iva_compensation: function () {
            return this.iva_compensation;
        },

        set_iva_compensation: function (new_iva_compensation) {
            this.iva_compensation = new_iva_compensation;
        }

    });

    instance.point_of_sale.ScreenWidget = instance.point_of_sale.ScreenWidget.extend({
        exits_action_button: function (label) {
            return this.pos_widget.action_bar.exist_action_button(label);
        },

        get_action_button: function (label) {
            return this.pos_widget.action_bar.get_action_button(label);
        },
    });

    instance.point_of_sale.ActionBarWidget = instance.point_of_sale.ActionBarWidget.extend({
        exist_action_button: function (label) {
            for (var i = 0; i < this.button_list.length; i++)
            {
                if( this.button_list[i].label == label) {
                    return true;
                }
            }
            return false;
        },

        get_action_button: function (label) {
            for (var i = 0; i < this.button_list.length; i++) {
                if (this.button_list[i].label == label) {
                    return this.button_list[i];
                }
            }
            return undefined;
        },
    });

    instance.point_of_sale.ReceiptScreenWidget = instance.point_of_sale.ReceiptScreenWidget.extend({
        show: function () {
            this._super();
            var self = this;
            var print_button = undefined;
            var finish_button = undefined;
            if(!this.pos_widget.action_bar.exist_action_button(_t('Print'))) {
                print_button = this.add_action_button({
                    label: _t('Print'),
                    icon: '/point_of_sale/static/src/img/icons/png48/printer.png',
                    click: function () {
                        self.print();
                    },
                });
            }
            else
            {
                print_button =  this.pos_widget.action_bar.get_action_button(_t('Print'));
            }

            if (!this.pos_widget.action_bar.exist_action_button(_t('Next Order'))) {
                finish_button = this.add_action_button({
                    label: _t('Next Order'),
                    icon: '/point_of_sale/static/src/img/icons/png48/go-next.png',
                    click: function () {
                        self.finishOrder();
                    },
                });
            }
            else
            {
                finish_button =  this.pos_widget.action_bar.get_action_button(_t('Next Order'));
            }

            this.refresh();

            finish_button.set_disabled(true);
            print_button.set_disabled(true);

            setTimeout(function () {
                finish_button.set_disabled(false);
                print_button.set_disabled(false);
            }, 2500);
        },

        refresh: function () {
            this._super();
            var client = this.pos.get('selectedOrder').get_client();

            /*Seteando Declaracion de Garantia*/
            if (this.pos.company.warranty != null && this.pos.company.warranty != undefined && this.pos.company.warranty != false && this.pos.company.warranty.length != 0) {
                $('#div_product_warranty').css('display', '');
                $('#span_product_warranty').html(this.pos.company.warranty);
            }
            else {
                $('#div_product_warranty').css('display', 'none');
            }

            if (client != null && client != undefined && client != false) {
                this.$('#div_ticker_customer_name').html(client.name);
                this.$('#div_ticker_customer_name').html(client.name);
                this.$('#div_ticker_customer_address').html(client.contact_address);
                this.$('#div_ticker_customer_email').html(client.email);
                this.$('#div_ticker_customer_mobile').html(client.mobile);
                this.$('#div_ticker_customer_phone').html(client.phone);

                var type_ced_ruc = false;
                if (client.type_ced_ruc == 'ruc') {
                    type_ced_ruc = 'Ruc';
                }
                if (client.type_ced_ruc == 'cedula') {
                    type_ced_ruc = 'Cedula';
                }
                if (client.type_ced_ruc == 'pasaporte') {
                    type_ced_ruc = 'Pasaporte';
                }

                if (type_ced_ruc) {
                    this.$('#div_ticker_customer_ced').html(type_ced_ruc + ': ' + client.ced_ruc);
                }
            }
            this.$('.pos-sale-ticket table').css('font-size', '16px');
        },

        print: function () {
            var self = this;
            var order_id = this.pos.get('selectedOrder').order_id;
            if(this.pos.config.pos_ticket_report) {
                if (order_id != 0) {
                    var ids = [order_id];
                    // generate the pdf and download it
                    self.pos_widget.do_action('my_point_of_sale.action_report_pos_ticket', {
                        additional_context: {
                            active_ids: ids,
                        }
                    });
                }
            }
            else{
                if(order_id != 0) {
                    window.print();
                }
            }
        },
    });

    instance.point_of_sale.PaypadButtonWidget.include({

        renderElement: function () {
            var self = this;
            this._super();

            this.$el.click(function () {

                if (self.pos.get('selectedOrder').get('screen') === 'receipt') {
                    return;
                }

                //Eliminando linea de pago repetida
                var paymentLines = self.pos.get('selectedOrder').get('paymentLines');
                var existe = false;
                var pos = 0;
                for(var i = 0; i < paymentLines.models.length - 1; i++)
                {
                      if(paymentLines.models[i].get_type() == self.cashregister.journal.type)
                      {
                          existe = true;
                          pos = i;
                          break;
                      }
                }

                //Eliminando Linea de Pago Repetida
                if(existe)
                {
                    var selectedLine = self.pos.get('selectedOrder').getSelectedPaymentline();
                    self.pos.get('selectedOrder').removePaymentline(selectedLine);
                    self.pos.get('selectedOrder').selectPaymentline(paymentLines.models[pos]);
                }

                //Ocultando campo IVA compensation
                if (self.pos.config.iva_compensation <= 0) {
                    $("#taxes-compensation").addClass("oe_hidden");
                }
                /*
                //Ocultando campo card comition
                if (self.cashregister.journal.type != 'card' || self.pos.config.card_comition == 0) {
                    $("#card_comition").addClass("oe_hidden");
                }
                */
            });
        },
    });
};
