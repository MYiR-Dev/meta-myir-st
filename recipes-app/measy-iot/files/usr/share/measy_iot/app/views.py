# -*- coding: utf-8 -*-
import calendar
from flask import render_template, session, json, request, jsonify
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder import BaseView, expose, has_access
from flask_babel import lazy_gettext as _
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from app import appbuilder, db

from forms import *

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404

"""
    create appbuilder link
"""
class MeasyView(BaseView):
    route_base = "/measy"
    @expose('/sysinfo')
    @has_access
    def sysinfo(self):
        # do something with param1
        # and render template with param
        return self.render_template('measy/sysinfo.html', appbuilder=appbuilder)

    @expose('/sysupgrade')
    @has_access
    def sysupgrade(self):
        # do something with param1
        # and render template with param
        return self.render_template('measy/sysupgrade.html', appbuilder=appbuilder)

    def get_ethernet_info(self):
        info = {'status': 'OK',
                'lan_dhcpen': 0,
                'lan_address': '192.168.30.101',
                'lan_netmask': '255.255.0.0',
                'lan_gateway': '192.168.30.1',
                'wan_dhcpen': 1,
                'wan_address': '10.1.1.10',
                'wan_netmask': '255.255.0.0',
                'wan_gateway': '10.1.1.1',
                }
        # return json.dumps(data)
        # return jsonify(data)
        return info

    def set_ethernet_info(self, info):
        pass
        data = {}
        return data

    @expose('/ethernet', methods=['GET', 'POST'])
    @has_access
    def ethernet(self):
        # do something with param1
        # and render template with param
        # print unicode(lazy_gettext(u"Home"))
        form_lan = IPForm(meta={'csrf': False},prefix='lan',interface=0)
        form_wan = IPForm(meta={'csrf':False},prefix='wan',interface=1)
        forms={}
        forms['lan'] = form_lan
        forms['wan'] = form_wan

        interface = request.args.get("interface", 0)
        forms['active'] = interface

        if request.method == 'POST':
            if interface == '1':
                if(form_wan.validate_on_submit()):
                    # save ip settings for wan
                    info = {}
                    forms['info'] = self.set_ethernet_info(info)
                    pass
            else:
                if(form_lan.validate_on_submit()):
                    # save ip settings for lan
                    info = {}
                    forms['info'] = self.set_ethernet_info(info)
                    pass

        if request.method == 'GET':
        # get ip settings for lan and wan
            forms['info'] = self.get_ethernet_info()
            pass

        return self.render_template('measy/ethernet.html', appbuilder=appbuilder, forms=forms)

    @expose('/ethernet/info',methods=['GET', 'POST'] )
    # @has_access
    def ethernet_info(self):
        if(request.method == 'GET'):
            return jsonify(self.get_ethernet_info())
        if(request.method == 'POST'):
            info = {}
            return jsonify(self.set_ethernet_info(info))

    @expose('/wifi')
    @has_access
    def wifi(self):
        # do something with param1
        # and render template with param
        return self.render_template('measy/wifi.html', appbuilder=appbuilder)

    @expose('/mobile')
    @has_access
    def mobile(self):
        # do something with param1
        # and render template with param
        return self.render_template('measy/mobile.html', appbuilder=appbuilder)

    @expose('/mqtt', methods=('GET','POST'))
    @has_access
    def mqtt(self):
        # do something with param1
        # and render template with param
        # if(request.method=='POST'):
        #     data = json.loads(request.form.get('data'))
        #     mq_clientid = data['mq_clientid']
        #     mq_host = data['mq_host']
        #     mq_port = data['mq_port']
        #     mq_qos = data['mq_qos']
        #     mq_retain = data['mq_retain']

        return self.render_template('measy/mqtt.html', appbuilder=appbuilder)

    @expose('/iec')
    @has_access
    def iec(self):
        # do something with param1
        # and render template with param
        return self.render_template('measy/iec.html', appbuilder=appbuilder)

    @expose('/document')
    @has_access
    def document(self):
        # do something with param1
        # and render template with param
        return self.render_template('measy/document.html', appbuilder=appbuilder)


appbuilder.add_view_no_menu(MeasyView())

