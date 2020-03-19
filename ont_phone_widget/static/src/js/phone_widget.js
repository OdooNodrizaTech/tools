odoo.define('account_doctorproperty.phone_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var formwidgets = require('web.form_widgets');
    var web_client = require('web.web_client');
    var _t = core._t;

    var FieldPhone = formwidgets.FieldEmail.extend({
        template: 'FieldPhone',
        prefix: '',
        render_value: function() {
            var value_tel_code = 34;
            if('field_phone_code' in this.options) {
                value_tel_code = this.field_manager.get_field_value(this.options.field_phone_code)                
            }            
            this.prefix = 'tel:+'+value_tel_code;
            this._super();
            if (this.get("effective_readonly") && this.clickable) {
                var self = this;
                this.$el.attr('href', this.prefix + this.get('value'));
            }            
        }
    });

    // To avoid conflicts, we check that widgets do not exist before using
    if(!core.form_widget_registry.get('phone')){
        core.form_widget_registry.add('phone', FieldPhone);
    }
});