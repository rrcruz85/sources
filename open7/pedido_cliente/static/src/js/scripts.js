
openerp.pedido_cliente = function(instance) {
    var _t = instance.web._t, _lt = instance.web._lt;
	var QWeb = instance.web.qweb;     

    instance.web.ListView.include({
    	limit: function () {
        	
        	if(this.model == 'request.product.variant' || this.model == 'purchase.lines.wzd' || this.model == 'summary.by.farm.wizard'){
            	this._limit = 10000;
        	}
        	else
        	{
        		if (this._limit === undefined) {
                    this._limit = (this.options.limit
                                || this.defaults.limit
                                || (this.getParent().action || {}).limit
                                || 80);
                }                
        	}        	
        	return this._limit;
        },
    });    	
};

