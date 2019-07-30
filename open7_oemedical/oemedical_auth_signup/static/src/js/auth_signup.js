openerp.oemedical_auth_signup = function(instance) {

    var _t = instance.web._t;
    var compSelected = '';
    var errorMsg = '';

    instance.web.Login.include({
        
        validateEmail: function(email) {
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        },

        validateUserName: function(userName) {
            
            var illegalChars = /\W/; // allow letters, numbers, and underscores 
            var startNumbers = /^[0-9]+/;
            
            if (userName == "") {                
                errorMsg = "You didn't enter an UserName !";                
                return false;         
            } else if ((userName.length < 5) || (userName.length > 15)) {                 
                errorMsg = "UserName has wrong length, at least 5 characters are required !";                 
                return false;         
            }else if (startNumbers.test(userName)) {               
                errorMsg = "UserName can not start with a number !";                
                return false;         
            }  
            else if (illegalChars.test(userName)) {               
                errorMsg = "UserName contains illegal characters !";                
                return false;         
            }  
            return true;
        },

        validatePasswordStrenght: function(password){
            //var strongRegex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})");
            var lower = /[a-z]+/;
            var upper = /[A-A]+/;
            var number = /[0-9]+/;
            var specialSymbol = /[!@#\$%\^&\*]+/;
            var length = /.{8,}/;

            if (!lower.test(password)) {               
                errorMsg = "Password must contain at least 1 lowercase alphabetical character !";                
                return false;         
            } 
            else if (!upper.test(password)) {               
                errorMsg = "Password must contain at least 1 uppercase alphabetical character !";                
                return false;         
            } 
            else if (!number.test(password)) {               
                errorMsg = "Password must contain at least 1 digit character !";                
                return false;         
            }  
            else if (!specialSymbol.test(password)) {               
                errorMsg = "Password must contain at least 1 special character !";                
                return false;         
            }   
            else if (!length.test(password)) {               
                errorMsg = "Password must be 8 characters or longer !";                
                return false;         
            }
            return true;           
             
        },

        validateNames: function(names, areNames){
            var namesRegex = /^[A-Za-zñÑáéíóúÁÉÍÓÚ\s]+$/;
            if (!namesRegex.test(names)) { 
                errorMsg = areNames ? "Names contains illegal characters !": "LastNames contains illegal characters !";                
                return false;         
            }  
            return true;
        },

        hideErrorMessage: function(){
            $('.oe_login_error_message').css('display', 'none');
            $('.oe_login_logo').css('display', 'inline-block');
            if(compSelected){
                this.$("form input[name=" + compSelected +"]").css({
                    'border-color': '#999999',
                    'border-style': 'solid',
                    'border-width': 'inherit'
                }); 
                compSelected = '';
            }
        },

        showErrorMsg: function(msg, field){
            compSelected = field;
            $('.oe_login_logo').css('display', 'none');
            $('.oe_login_error_message').css('display', 'inline-block');
            this.highLightComponent(field);
            this.show_error( _t(msg));
            window.setTimeout(this.hideErrorMessage, 3000);
        },

        highLightComponent: function(component){
            this.$("form input[name=" + component +"]").css({
                'border-color': 'red',
                'border-style': 'solid',
                'border-width': 'medium'
            }); 
        },
        
        validateMobileNumber: function(mobile) {

            var stripped = mobile.replace(/[\(\)\.\-\ ]/g, '');
        
            if (mobile == "") {
                errorMsg = "You didn't enter a mobile number !";               
                return false;        
            } else if (isNaN(parseInt(stripped))) {
                errorMsg = "The mobile number contains illegal characters. Don't include dash (-) !";
                return false;
            } else if (!(stripped.length == 10)) {
                errorMsg = "The mobile number length must be 10 digits. Don't include dash (-) !";
                return false;
            }
            return true;
        },

        get_params: function(){

            // signup user (or reset password)
            this.hideErrorMessage();
           
            var db = this.$("form [name=db]").val();
            var name = this.$("form input[name=name]").val();
            var login = this.$("form input[name=login]").val();
            var use_name_for_logging_in = this.$("form input[name=use_name_for_logging_in]").prop('checked');
            var password = this.$("form input[name=password]").val();
            var confirm_password = this.$("form input[name=confirm_password]").val();
            var names = this.$("form input[name=names]").val();
            var last_names = this.$("form input[name=last_names]").val();
            var mobile = this.$("form input[name=mobile]").val();
            
            if (!db) {
                this.showErrorMsg("No database selected !", 'db');
                return false;
            } else if (!name) {
                this.showErrorMsg("Please enter a UserName !", 'name');
                return false;
            } 
            else if (!this.validateUserName(name)) {                          
                this.showErrorMsg(errorMsg, 'name');
                errorMsg = '';
                return false;
            }
            else if (!login) {
                this.showErrorMsg("Please enter an Email !", 'login');
                return false;
            }
            else if(!this.validateEmail(login)){ 
                this.showErrorMsg("Email Address is incorrect !", 'login');
                return false
            }  
            else if (!password || !confirm_password) {
                this.showErrorMsg("Please enter a password and confirm it !", 'password');
                return false;
            } else if (password !== confirm_password) {
                this.showErrorMsg("Passwords do not match; please retype them !", 'confirm_password');
                return false;
            }else if (!this.validatePasswordStrenght(password)) {
                this.showErrorMsg(errorMsg, 'password');
                errorMsg = '';
                return false;
            }else if (!names) {
                this.showErrorMsg("Please enter a name!", 'names');                
                return false;
            }
            else if (!this.validateNames(names, true)) {
                this.showErrorMsg(errorMsg, 'names');
                errorMsg = '';
                return false;
            }
            else if (!last_names) {
                this.showErrorMsg("Please enter a last name!", 'last_names');                 
                return false;
            }
            else if (!this.validateNames(last_names, false)) {
                this.showErrorMsg(errorMsg, 'last_names');
                errorMsg = '';
                return false;
            }


            else if (!mobile) {
                this.showErrorMsg("Please enter a valid mobile number!", 'mobile');               
                return false;
            }
            else if (!this.validateMobileNumber(mobile)) {
                this.showErrorMsg(errorMsg, 'mobile');
                errorMsg = '';
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
