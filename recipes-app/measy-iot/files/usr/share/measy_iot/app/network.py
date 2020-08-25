

import sys
from tdbus import SimpleDBusConnection,GEventDBusConnection, DBUS_BUS_SYSTEM,DBUS_BUS_SESSION ,DBusHandler, signal_handler, DBusError
import dbus
import copy

DBUS_PATH = "/"
DBUS_INTERFACE = 'net.connman.Manager'
DBUS_NAME = 'net.connman'
DBUS_SERVER_INTERFACE= 'net.connman.Service'
CONNMAN_SIGNAL_ETH='ServicesChanged'

class NetworkObject(DBusHandler):

    def __init__ (self, connect, sio, ipconfig):
        super(NetworkObject, self).__init__()
        self.connect = connect
        self.sio = sio
        self.gl_ip_config = ipconfig
    @signal_handler(path=DBUS_PATH, member=CONNMAN_SIGNAL_ETH, interface=DBUS_INTERFACE)
    def sigServicesChanged(self, message):
        res = message
        ip = dict()
        if res.get_args()[0]:
            for i in res.get_args()[0]:
                (path, params) = i
                if not self.gl_ip_config.find_ip(path):
                    if not params:
                        print '============second sig================'
                        self.sio.emit("ethernet_changed", {'status':'changed'}, namespace='/test')
        if res.get_args()[1]:
            for i in res.get_args()[1]:
                path = i
                # print path
                self.gl_ip_config.delete_ip(path)
                # print self.gl_ip_config.get_ip()
                self.sio.emit("ethernet_config",  self.gl_ip_config.get_ip(), namespace='/test')

        # self.sio.emit("led_signal", {'data': res}, namespace='/test')

    def list_technologies(self, args):
        print '========================================================='
        # global manager

        try:
            self.technologies = self.connect.call_method(DBUS_PATH, 'GetTechnologies',
                                     interface=DBUS_INTERFACE, destination=DBUS_NAME).get_args()[0]
            # self.technologies = self.manager.get_technologies()
            for i in self.technologies:
                (path, params) = i
                print path,params
        except DBusError:
            print 'Unable to complete:', sys.exc_info()


    def list_services(self):
        print '========================================================='
        try:
            self.services = self.connect.call_method(DBUS_PATH, 'GetServices',
                                                         interface=DBUS_INTERFACE, destination=DBUS_NAME).get_args()[0]
            # self.services = self.manager.get_services()
            # print self.services

            return self.services
        except DBusError:
            print 'Unable to complete:', sys.exc_info()
    def set_ip(self, path, ipconfig):
        print '========================================================='
        try:
            self.services = self.connect.call_method(path, 'SetProperty',
                                                         interface=DBUS_SERVER_INTERFACE, destination=DBUS_NAME, args=(ipconfig)).get_args()[0]
            # self.services = self.manager.get_services()
            # print self.services

            return self.services
        except DBusError:
            print 'Unable to complete:', sys.exc_info()


    def exit_cleanup(args):
        sys.exit(0)




class NetworkManager(object):

    def __init__(self, sio=None, ip_config=None):
        self.sio = sio
        self.ip_config = ip_config
        self.connect = GEventDBusConnection(DBUS_BUS_SYSTEM)
        self.service = NetworkObject(self.connect, self.sio,self.ip_config)
        self.connect.add_handler(self.service)
        self.connect.subscribe_to_signals()

    def list_services(self):
        return self.service.list_services()
    def set_ip(self,patch,ipconfig):
        return self.service.set_ip(patch,ipconfig)
    def list_technologies(self, args=None):
        return self.service.list_technologies(args)
if __name__ == '__main__':
#    from app.ws import socketio
#    thread_lock = Lock()
#    adapter = NetworkAdapter(thread_lock,None)
#    adapter.start()
#     import multiprocessing
#
#     mqueue = multiprocessing.Queue()
#     mlock = multiprocessing.Lock()
#
#     network_manager= NetworkManager(None, mqueue, mlock)
#     network_manager.worker()
#     network_manager.handler()
      manager = NetworkManager()
      manager.list_services()
      manager.list_technologies()