odoo.define('news_custom.newsclicktopbutton', function (require) {
"use strict";

var SystrayMenu = require('web.SystrayMenu');
var web_client = require('web.web_client');
var Widget = require('web.Widget');
var core = require('web.core');
var _t = core._t;

var newsclicktopbutton = {};

var newsclicktopbuttonCaller = Widget.extend({
    template: 'news_custom.OpenNews',
    events: {
        'click': 'on_open_news',
    },
    start: function () {
        this._super();
        var self = this;
        self.rpc('/news_custom/get_records_unread_total', {}).done(function(r) {          
            if (r.total>0) 
            {
                $("#new_custom_odoo-open-news").html($("#new_custom_odoo-open-news").html()+'<span class="o_notification_counter">'+r.total+'</span>');
                setTimeout(function(){
                    $("#new_custom_odoo-open-news").click();
                }, 2000);                
            }        
        });
    },
    on_open_news: function (event) {
        event.stopPropagation();
        var self = this;
        self.rpc('/news_custom/get_last_record_unread', {}).done(function(r) {
            if (r.record_unread !== false) 
            {
                var action = {                        
                    name: r.record_unread.name,                    
                    type: 'ir.actions.act_window',
                    res_model: 'new.custom',
                    res_id: r.record_unread.id,
                    view_mode: 'form,tree',
                    views: [[false, 'form']],
                    target: 'new',
                    context: {},
                    //flags: {'form': {'action_buttons': true}},
                };
                web_client.action_manager.do_action(action);
                setTimeout(function(){
                    $(".modal .modal-footer").remove();
                }, 2000);
            }
            else
            {
                window.location.href = odoo.session_info['web.base.url']+'/web?#action='+r.action.id;                
            }
        });
   },
});

SystrayMenu.Items.push(newsclicktopbuttonCaller);

});