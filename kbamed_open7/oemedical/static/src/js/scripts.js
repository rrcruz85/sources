
openerp.oemedical = function(instance) {

    instance.web.str_to_datetime = function(str){
        if(!str) {
            return str;
        }
        var regex = /^(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)(?:\.\d+)?$/;
        var res = regex.exec(str);
        if ( !res ) {
            throw new Error(_.str.sprintf(_t("'%s' is not a valid datetime"), str));
        }
        var obj = Date.parseExact(res[1], 'yyyy-MM-dd HH:mm:ss');
        if (! obj) {
            throw new Error(_.str.sprintf(_t("'%s' is not a valid datetime"), str));
        }
        return obj;
    };
};

