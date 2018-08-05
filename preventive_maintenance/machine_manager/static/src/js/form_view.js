
console.debug("[report_fleet_reparation] JS is loading...");

openerp.machine_manager = function (instance) {
    var _t = instance.web._t, _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.FormView.include({
        load_record: function (record) {
            res = this._super(record);
            if (this.dataset.model == 'machinery') {
                $('input.button_update_image').click();
            }
            return res;
        }
    });
};
