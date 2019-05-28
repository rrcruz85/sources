openerp.oemedical_dentist_test_view_form = function (instance) {
	var _t = instance.web._t, _lt = instance.web._lt;
	var QWeb = instance.web.qweb;
	
	instance.web.form.FieldTextXHtml = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin, {
	    template: 'FieldTextXHtml',
	    init: function() {
	        this._super.apply(this, arguments);
	    },
	    initialize_content: function() {
	        var self = this;
	        if (! this.get("effective_readonly")) {
	            self._updating_editor = false;
	            this.$textarea = this.$el.find('textarea');
	            var width = ((this.node.attrs || {}).editor_width || '100%');
	            var height = ((this.node.attrs || {}).editor_height || 250);
	            this.$textarea.cleditor({
	                width:      width, // width not including margins, borders or padding
	                height:     height, // height not including margins, borders or padding
	                controls:   // controls to add to the toolbar
	                            "bold italic underline strikethrough " +
	                            "| removeformat | bullets numbering | outdent " +
	                            "indent | link unlink | source",
	                bodyStyle:  // style to assign to document body contained within the editor
	                            "margin:4px; color:#4c4c4c; font-size:13px; font-family:'Lucida Grande',Helvetica,Verdana,Arial,sans-serif; cursor:text"
	            });
	            this.$cleditor = this.$textarea.cleditor()[0];
	            this.$cleditor.change(function() {
	                if (! self._updating_editor) {
	                    self.$cleditor.updateTextArea();
	                    self.internal_set_value(self.$textarea.val());
	                }
	            });
	            if (this.field.translate) {
	                var $img = $('<img class="oe_field_translate oe_input_icon" src="/web/static/src/img/icons/terp-translate.png" width="16" height="16" border="0"/>')
	                    .click(this.on_translate);
	                this.$cleditor.$toolbar.append($img);
	            }
	        }
	    },
	    render_value: function() {
	        if (! this.get("effective_readonly")) {
	            this.$textarea.val(this.get('value') || '');
	            this._updating_editor = true;
	            this.$cleditor.updateFrame();
	            this._updating_editor = false;
	        } else {
	            this.$el.html(this.get('value'));
	        }
	    },
	});
	
	instance.web.form.widgets.add('xhtml', 'instance.web.form.FieldTextXHtml');

	instance.web.Odontograma =  instance.web.Widget.extend({
		template: 'Odontograma',
		init: function() {
			this._super.apply(this, arguments);
			instance.web.odontograma = this;
		},
		start: function() {
			this._super.apply(this, arguments);	
			
			var $content = this.$('#odonto');
			console.log('Select');
			console.log($content);
            /*
			var line = new module.OrderlineWidget(this, {
				model: orderLine,
				order: this.pos.get('selectedOrder'),
			});		
			line.appendTo($content);
            */
			this.appendTo($content);
		}
	});

	instance.web.client_actions.add("show_odontogram", "instance.web.Odontograma");
	
}