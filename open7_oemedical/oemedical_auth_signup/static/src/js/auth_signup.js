openerp.oemedical_auth_signup = function(instance) {

    var _t = instance.web._t;

    instance.web.Login.include({
        get_params: function(){
            // signup user (or reset password)
            var db = this.$("form [name=db]").val();
            var name = this.$("form input[name=name]").val();
            var login = this.$("form input[name=login]").val();
            var use_name_for_logging_in = this.$("form input[name=use_name_for_logging_in]").prop('checked');
            var password = this.$("form input[name=password]").val();
            var confirm_password = this.$("form input[name=confirm_password]").val();

            if (!db) {
                this.do_warn(_t("Login"), _t("No database selected !"));
                return false;
            } else if (!name) {
                this.do_warn(_t("Login"), _t("Please enter a name."));
                return false;
            } else if (!login) {
                this.do_warn(_t("Login"), _t("Please enter a username."));
                return false;
            } else if (!password || !confirm_password) {
                this.do_warn(_t("Login"), _t("Please enter a password and confirm it."));
                return false;
            } else if (password !== confirm_password) {
                this.do_warn(_t("Login"), _t("Passwords do not match; please retype them."));
                return false;
            }
            var params = {
                dbname : db,
                token: this.params.token || "",
                name: name,
                login: login,
                password: password,
                usenameforloggingin: use_name_for_logging_in
            };
            return params;
        },
    });
};
