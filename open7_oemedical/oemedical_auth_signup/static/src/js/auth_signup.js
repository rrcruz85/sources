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

        validateCedula: function(cedula) {

            if(cedula.length == 10){
                
                //Obtenemos el digito de la region que sonlos dos primeros digitos
                var digito_region = cedula.substring(0,2);
                
                //Pregunto si la region existe ecuador se divide en 24 regiones
                if( digito_region >= 1 && digito_region <=24 ){
                
                    // Extraigo el ultimo digito
                    var ultimo_digito   = cedula.substring(9,10);

                    //Agrupo todos los pares y los sumo
                    var pares = parseInt(cedula.substring(1,2)) + parseInt(cedula.substring(3,4)) + parseInt(cedula.substring(5,6)) + parseInt(cedula.substring(7,8));

                    //Agrupo los impares, los multiplico por un factor de 2, si la resultante es > que 9 le restamos el 9 a la resultante
                    var numero1 = cedula.substring(0,1);
                    var numero1 = (numero1 * 2);
                    if( numero1 > 9 ){ var numero1 = (numero1 - 9); }

                    var numero3 = cedula.substring(2,3);
                    var numero3 = (numero3 * 2);
                    if( numero3 > 9 ){ var numero3 = (numero3 - 9); }

                    var numero5 = cedula.substring(4,5);
                    var numero5 = (numero5 * 2);
                    if( numero5 > 9 ){ var numero5 = (numero5 - 9); }

                    var numero7 = cedula.substring(6,7);
                    var numero7 = (numero7 * 2);
                    if( numero7 > 9 ){ var numero7 = (numero7 - 9); }

                    var numero9 = cedula.substring(8,9);
                    var numero9 = (numero9 * 2);
                    if( numero9 > 9 ){ var numero9 = (numero9 - 9); }

                    var impares = numero1 + numero3 + numero5 + numero7 + numero9;

                    //Suma total
                    var suma_total = (pares + impares);

                    //extraemos el primero digito
                    var primer_digito_suma = String(suma_total).substring(0,1);

                    //Obtenemos la decena inmediata
                    var decena = (parseInt(primer_digito_suma) + 1)  * 10;

                    //Obtenemos la resta de la decena inmediata - la suma_total esto nos da el digito validador
                    var digito_validador = decena - suma_total;

                    //Si el digito validador es = a 10 toma el valor de 0
                    if(digito_validador == 10)
                        var digito_validador = 0;

                    //Validamos que el digito validador sea igual al de la cedula
                    return digito_validador == ultimo_digito;
                    
                }
                else{
                    // imprimimos en consola si la region no pertenece
                    return false;
                }
            }
            else{
                return false;
            }    

            /*
            var cad = cedula.trim();
            var total = 0;
            var longitud = cad.length;
            var longcheck = longitud - 1;
    
            if (cad !== "" && longitud === 10) {
                for (i = 0; i < longcheck; i++) {
                    if (i % 2 === 0) {
                        var aux = cad.charAt(i) * 2;
                        if (aux > 9) aux -= 9;
                        total += aux;
                    } else {
                        total += parseInt(cad.charAt(i)); // parseInt o concatenará en lugar de sumar
                    }
                }

                total = total % 10 ? 10 - total % 10 : 0;

                return (cad.charAt(longitud - 1) == total); 
            }

            return false;
            */
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
            var type_identification = this.$("form select[name=type_identification_list]").val();
            var type_identification_value = this.$("form input[name=type_identification_value]").val();
            
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
            else if (!type_identification_value) {
                this.showErrorMsg("Please enter a " + type_identification + "!", 'type_identification_value');                 
                return false;
            }
            else if (type_identification_value) {
                type_identification_value = type_identification_value.trim();
                if(type_identification == 'cedula'){
                    if(!this.validateCedula(type_identification_value)){
                       this.showErrorMsg("Cedula incorrecta !", 'type_identification_value');                 
                       return false;
                    }
                    return true;
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
                    return true;
                }
                else if(type_identification == 'pasaporte'){
                    return true;
                }                 
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
