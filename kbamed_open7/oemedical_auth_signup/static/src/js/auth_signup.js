openerp.oemedical_auth_signup = function(instance) {

    var _t = instance.web._t;
    var compSelected = '';
    var errorMsg = '';

    instance.web.Login.include({

        start: function() {
            var self = this;
            this.signup_enabled = false;
            this.reset_password_enabled = false;
            return this._super().always(function() {

                // Switches the login box to the select mode whith mode == [default|signup|reset]
                self.on('change:login_mode', self, function() {
                    var mode = self.get('login_mode') || 'default';
                    self.$('*[data-modes]').each(function() {
                        var modes = $(this).data('modes').split(/\s+/);
                        $(this).toggle(modes.indexOf(mode) > -1);
                    });
                    self.$('a.oe_signup_signup:visible').toggle(self.signup_enabled);
                    self.$('a.oe_signup_reset_password:visible').toggle(self.reset_password_enabled);
                });

                // to switch between the signup and regular login form
                self.$('a.oe_signup_signup').click(function(ev) {
                    self.set('login_mode', 'signup');
                    return false;
                });
                self.$('a.oe_signup_back').click(function(ev) {
                    self.clearForm();
                    self.set('login_mode', 'default');
                    delete self.params.token;                    
                    return false;
                });

                var dbname = self.selected_db;

                // if there is an error message in params, show it then forget it
                if (self.params.error_message) {
                    self.show_error(self.params.error_message);
                    delete self.params.error_message;
                }

                if (dbname && self.params.login) {
                    self.$("form input[name=login]").val(self.params.login);
                }

                // bind reset password link
                self.$('a.oe_signup_reset_password').click(self.do_reset_password);

                if (dbname) {
                    self.rpc("/auth_signup/get_config", {dbname: dbname}).then(function(result) {
                        self.signup_enabled = result.signup;
                        self.reset_password_enabled = result.reset_password;
                        if (!self.signup_enabled || self.$("form input[name=login]").val()){
                            self.set('login_mode', 'default');
                        } else {
                            self.set('login_mode', 'signup');
                        }

                        // in case of a signup, retrieve the user information from the token
                        if (self.params.token) {
                            self.rpc("/auth_signup/retrieve", {dbname: dbname, token: self.params.token})
                                .then(self.on_token_loaded, self.on_token_failed);
                        }

                    });
                } 
                else {                     
                    self.set('login_mode', 'default');
                }
            });
        },
        
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
            var upper = /[A-Z]+/;
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
            var namesRegex = /^[A-Za-zñÑáéíóúÁÉÍÓÚüÜ\s]+$/;
            if (!namesRegex.test(names)) { 
                errorMsg = areNames ? "Names contains illegal characters !": "LastNames contains illegal characters !";                
                return false;         
            }  
            return true;
        },

        hideErrorMessage: function(){
            $('.oe_login_error_message').css('display', 'none');
            $('.oe_login_error_message').css('background-color', '#b41616');
            $('.oe_login_error_message').text('');
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
            this.show_error(_t(msg));
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

        validateCedula: function(cedula) {

            if(cedula.length == 10){           

                var digito_region = cedula.substring(0,2);                
                if( digito_region >= 1 && digito_region <=24 ){
                
                    var ultimo_digito   = cedula.substring(9,10);
                    var pares = parseInt(cedula.substring(1,2)) + parseInt(cedula.substring(3,4)) + parseInt(cedula.substring(5,6)) + parseInt(cedula.substring(7,8));

                    var numero1 = cedula.substring(0,1);
                    var numero1 = (numero1 * 2);
                    if( numero1 > 9 ){ numero1 = (numero1 - 9); }

                    var numero3 = cedula.substring(2,3);
                    var numero3 = (numero3 * 2);
                    if( numero3 > 9 ){ numero3 = (numero3 - 9); }

                    var numero5 = cedula.substring(4,5);
                    var numero5 = (numero5 * 2);
                    if( numero5 > 9 ){ numero5 = (numero5 - 9); }

                    var numero7 = cedula.substring(6,7);
                    var numero7 = (numero7 * 2);
                    if( numero7 > 9 ){ numero7 = (numero7 - 9); }

                    var numero9 = cedula.substring(8,9);
                    var numero9 = (numero9 * 2);
                    if( numero9 > 9 ){ numero9 = (numero9 - 9); }

                    var impares = numero1 + numero3 + numero5 + numero7 + numero9;

                    var suma_total = (pares + impares);
                    var primer_digito_suma = String(suma_total).substring(0,1);
                    var decena = (parseInt(primer_digito_suma) + 1)  * 10;
                    var digito_validador = decena - suma_total;
                    if(digito_validador == 10){
                        var digito_validador = 0;
                    }

                    return digito_validador == ultimo_digito;
                }
                else{
                    return false;
                }
            }
            else{
                return false;
            }
        },    

        validateDate: function(dateString){

            var regExp = /^(((0?[1-9])|1[0-9]|2[0-9])|(30)|(31))-((0?[1-9])|1[0-2])-(?:19|20)[0-9]{2}$/;
            
            // First check for the pattern
            if(!regExp.test(dateString)){
                errorMsg = "BirthDate is incorrect. Enter a date with the following format DD-MM-YYYY !"; 
                return false;
            }

            // Parse the date parts to integers
            var parts = dateString.split("-");
            var day = parseInt(parts[0], 10); 
            var month = parseInt(parts[1], 10);                       
            var year = parseInt(parts[2], 10);

            // Check the ranges of years
            if(year < 1900 || year > (new Date().getFullYear())){
                errorMsg = "BirthDate is incorrect. Year is incorrect !"; 
                return false;
            }

            // Check the ranges of months
            if(month == 0 || month > 12){
                errorMsg = "BirthDate is incorrect. Month is incorrect !"; 
                return false;
            }

            var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

            // Adjust for leap years
            if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0))
                monthLength[1] = 29;

            // Check the range of the day
            var dayIsCorrect = day > 0 && day <= monthLength[month - 1];
            if(!dayIsCorrect){
                errorMsg = "BirthDate is incorrect. Day is incorrect !"; 
            }

            return dayIsCorrect
        },

        get_params: function(){

            // signup user (or reset password)
            this.hideErrorMessage();
           
            var db = this.$("form [name=db]").val();
            var name = this.$("form input[name=name]").val();
            var login = this.$("form input[name=login]").val();
            var use_email_for_logging_in = this.$("form input[name=use_email_for_logging_in]").prop('checked');
            var password = this.$("form input[name=password]").val();
            var confirm_password = this.$("form input[name=confirm_password]").val();
            var names = this.$("form input[name=names]").val();
            var last_names = this.$("form input[name=last_names]").val();
            var gender = this.$("form select[name=gender]").val();
            var birthdate = this.$("form input[name=birthdate]").val();
            var mobile = this.$("form input[name=mobile]").val();
            var type_identification = this.$("form select[name=type_identification_list]").val();
            var type_identification_value = this.$("form input[name=type_identification_value]").val();
            var operadora = this.$("form select[name=operator]").val();
            
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
            } 
            else if (password !== confirm_password) {
                this.showErrorMsg("Passwords do not match; please retype them !", 'confirm_password');
                return false;
            }
            else if (!this.validatePasswordStrenght(password)) {
                this.showErrorMsg(errorMsg, 'password');
                errorMsg = '';
                return false;
            }
            else if (!names) {
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
            else if (!birthdate) {
                this.showErrorMsg("Please enter a birthdate!", 'birthdate');                 
                return false;
            }
            else if (!this.validateDate(birthdate)) {
                this.showErrorMsg(errorMsg, 'birthdate'); 
                errorMsg = '';                
                return false;
            }
            else if (!type_identification_value) {
                this.showErrorMsg("Please enter a " + type_identification + "!", 'type_identification_value');                 
                return false;
            }
            
            if (type_identification_value) {
                type_identification_value = type_identification_value.trim();
                if(type_identification == 'cedula'){
                    if(!this.validateCedula(type_identification_value)){
                       this.showErrorMsg("Cedula incorrecta !", 'type_identification_value');                 
                       return false;
                    }                     
                }
                else if(type_identification == 'ruc'){

                    if(type_identification_value.length != 13 || !type_identification_value.endsWith('001')){   
                        this.showErrorMsg("Ruc incorrecto !", 'type_identification_value');                 
                        return false; 
                    }                   
                    var ced = type_identification_value.substring(0, 10);
                    
                    if(!this.validateCedula(ced)){
                       this.showErrorMsg("Ruc incorrecto !", 'type_identification_value');                 
                       return false;
                    }
                }
                else if(type_identification == 'pasaporte'){                    
                    var checkExpression = /^[A-Z]*[0-9]+$/;
                    if (!checkExpression.test(type_identification_value)) {               
                        this.showErrorMsg("El pasaporte contiene caracteres no permitidos !", 'type_identification_value');                 
                        return false;         
                    }
                }                 
            }           
            
            if (!mobile) {
                this.showErrorMsg("Please enter a valid mobile number!", 'mobile');               
                return false;
            }
            else if (!this.validateMobileNumber(mobile)) {
                this.showErrorMsg(errorMsg, 'mobile');
                errorMsg = '';
                return false;
            }
            
            var words = last_names.trim().split(/(\s+)/).filter( e => e.trim().length > 0)
 
            var params = {
                dbname : db,
                token: this.params.token || "",
                name: name,
                login: login,
                password: password,
                use_email: use_email_for_logging_in,
                first_name: names,
                last_name: words.length > 0 ? words[0] : '', 
                slastname: words.length > 1 ? words[1] : '',               
                type_ced_ruc: type_identification,
                ced_ruc: type_identification_value,
                mobile: mobile,
                mobile_operator: operadora,
                is_patient: true,
                is_person: true,
                email: login,
                tipo_persona: 6,
                sex: gender,
                birthdate: birthdate
            };
            return params;
        },

        clearForm: function(){
            this.$("form input[name=name]").val('');
            this.$("form input[name=login]").val('');
            this.$("form input[name=use_email_for_logging_in]").prop('checked', false);
            this.$("form input[name=password]").val('');
            this.$("form input[name=confirm_password]").val('');
            this.$("form input[name=names]").val('');
            this.$("form input[name=last_names]").val('');
            this.$("form select[name=gender]").val('m');
            this.$("form input[name=birthdate]").val('');
            this.$("form select[name=type_identification_list]").val('cedula');
            this.$("form input[name=type_identification_value]").val('');
            this.$("form input[name=mobile]").val('');
            this.$("form select[name=operator]").val('claro');
        },

        on_submit: function(ev) {
            
            var self = this, super_ = this._super;
            if (ev) {
                ev.preventDefault();
            }
            var login_mode = self.get('login_mode');
            if (login_mode === 'signup' || login_mode === 'reset') {
                var params = self.get_params();
                if (_.isEmpty(params)){
                    return false;
                }
                context = {
                   'create_patient': true
                }
                self.rpc('/auth_signup/signup', params)
                    .done(function(result) {
 
                        if (result.error) {
                            $('.oe_login_logo').css('display', 'none');
                            $('.oe_login_error_message').css('display', 'inline-block'); 
                            self.show_error(_t(result.error));
                            window.setTimeout(self.hideErrorMessage, 3000);
                        } 
                        else {
                            self.clearForm();
                            $('.oe_login_logo').css('display', 'none');
                            $('.oe_login_error_message').css({
                                'display':'inline-block',
                                'background-color': 'darkgreen'
                            });
                            $('.oe_login_error_message').text(_t("User has been successfully signed up.\nPlease check your email account and click in the link that we sent you to activate your account."));
                            window.setTimeout(self.hideErrorMessage, 10000);                            
                            self.set('login_mode', 'default');
                        }
                    });
            } else {
                // regular login
                self._super(ev);
            }
        },
    });
};
