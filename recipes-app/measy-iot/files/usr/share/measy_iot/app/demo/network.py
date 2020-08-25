#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import threading
import readline  # noqa
import pyconnman
import sys
import dbus
import dbus.mainloop.glib
import gobject
import signal
from collections import namedtuple
from flask import session, request, flash
#from flask_socketio import SocketIO, emit, join_room, leave_room, \
#    close_room, rooms, disconnect
#from app import appbuilder, app

class NetworkObject(dbus.service.Object):

    services = {}
    def __init__ (self, bus, socketio=None):
        self.bus = bus
        try:
            self.manager = pyconnman.ConnManager()
            self.manager.add_signal_receiver(self.dump_signal,
                                        pyconnman.ConnManager.SIGNAL_TECHNOLOGY_ADDED,
                                        None)
            self.manager.add_signal_receiver(self.dump_signal,
                                        pyconnman.ConnManager.SIGNAL_TECHNOLOGY_REMOVED,  # noqa
                                        None)
            self.manager.add_signal_receiver(self.dump_signal,
                                        pyconnman.ConnManager.SIGNAL_SERVICES_CHANGED,
                                        None)
            self.manager.add_signal_receiver(self.dump_signal,
                                        pyconnman.ConnManager.SIGNAL_PROPERTY_CHANGED,
                                        None)
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()

    def dump_signal(signal, *args):
        print '\n========================================================='
        print '>>>>>', signal, '<<<<<'
        print args
        print '========================================================='
    #
    # def cmd_help(args):
    #     global cmd_table
    #
    #     if (len(args)):
    #         cmd_list = [args.pop(0)]
    #     else:
    #         cmd_list = cmd_table.keys()
    #
    #     for i in cmd_list:
    #         print i, cmd_table[i].args, ":", cmd_table[i].desc
    #

    def list_technologies(args):
        print '========================================================='
        global manager

        try:
            technologies = manager.get_technologies()
            for i in technologies:
                (path, params) = i
                print path, '['+params['Name']+']'
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def list_services(args):
        print '========================================================='
        global manager

        try:
            services = manager.get_services()
            for i in services:
                (path, params) = i
                print path, '['+params['Name']+']'
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def service_info(args):
        if (len(args)):
            service_path = args.pop(0)
        else:
            print 'Error: Must specify service path'
            return

        try:
            service = pyconnman.ConnService(service_path)
            print '========================================================='
            print service
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def service_get(args):
        if (len(args)):
            service_path = args.pop(0)
            if (len(args)):
                name = args.pop(0)
            else:
                name = None
        else:
            print 'Error: Must specify service path'
            return

        print '========================================================='

        try:
            service = pyconnman.ConnService(service_path)
            print service.get_property(name=name)
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def service_set(args):
        if (len(args) >= 3):
            service_path = args.pop(0)
            name = args.pop(0)
            value = args.pop(0)
        else:
            print 'Error: Requires service path, property name and value'
            return

        try:
            service = pyconnman.ConnService(service_path)
            service.set_property(name, value)
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def service_disconnect(args):
        if (len(args)):
            service_path = args.pop(0)
        else:
            print 'Error: Must specify service path'
            return

        try:
            service = pyconnman.ConnService(service_path)
            service.disconnect()
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def service_connect(args):
        if (len(args)):
            service_path = args.pop(0)
        else:
            print 'Error: Must specify service path'
            return

        try:
            service = pyconnman.ConnService(service_path)
            service.connect()
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def service_rm(args):
        if (len(args)):
            service_path = args.pop(0)
        else:
            print 'Error: Must specify service path'
            return

        try:
            service = pyconnman.ConnService(service_path)
            service.remove()
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def technology_get(args):
        if (len(args)):
            tech_path = args.pop(0)
            if (len(args)):
                name = args.pop(0)
            else:
                name = None
        else:
            print 'Error: Requires technology path'
            return

        try:
            tech = pyconnman.ConnTechnology(tech_path)
            print '========================================================='
            print tech.get_property(name=name)
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def technology_set(args):
        if (len(args) >= 3):
            tech_path = args.pop(0)
            name = args.pop(0)
            value = args.pop(0)
        else:
            print 'Error: Requires technology path, property name and value'
            return

        try:
            tech = pyconnman.ConnTechnology(tech_path)
            tech.set_property(name, value)
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def technology_info(args):
        if (len(args)):
            tech_path = args.pop(0)
        else:
            print 'Error: Must specify technology path'
            return

        try:
            tech = pyconnman.ConnTechnology(tech_path)
            print '========================================================='
            print tech
            print '========================================================='
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def technology_scan(args):
        if (len(args)):
            tech_path = args.pop(0)
        else:
            print 'Error: Must specify technology path'
            return

        try:
            tech = pyconnman.ConnTechnology(tech_path)
            tech.scan()
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def agent_start(args):

        global services, manager

        params = {'name': None,
                  'ssid': None,
                  'identity': None,
                  'username': None,
                  'password': None,
                  'passphrase': None,
                  'wpspin': None, }

        if (len(args)):
            agent_path = args.pop(0)
            while (len(args)):
                (param, value) = args.pop(0).split('=', 1)
                if (param in params):
                    params[param] = value
        else:
            print 'Error: Must provide agent path e.g., /test/agent'
            return

        try:
            agent = pyconnman.SimpleWifiAgent(agent_path)
            agent.set_service_params('*',
                                     params['name'],
                                     params['ssid'],
                                     params['identity'],
                                     params['username'],
                                     params['password'],
                                     params['passphrase'],
                                     params['wpspin'])
            services[agent_path] = agent
            manager.register_agent(agent_path)
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def agent_stop(args):

        global manager, services

        if (len(args)):
            path = args.pop(0)
        else:
            print 'Error: Must provide agent path e.g., /test/agent'
            return

        try:
            manager.unregister_agent(path)
            services[path].remove_from_connection()
        except dbus.exceptions.DBusException:
            print 'Unable to complete:', sys.exc_info()


    def exit_cleanup(args):
        sys.exit(0)

#
# CmdEntry = namedtuple('CmdEntry', 'func desc args')
# cmd_table = {'help': CmdEntry(cmd_help,
#                               'Display a list of commands or get help for a specific command',  # noqa
#                               '[command]'),
#              'list-technologies': CmdEntry(list_technologies,
#                                            'Provide a list of available network technologies',  # noqa
#                                            None),
#              'list-services': CmdEntry(list_services,
#                                        'Display a list of available network services',  # noqa
#                                        None),
#              'service-info': CmdEntry(service_info,
#                                       'Display information about a network service',  # noqa
#                                       '<service path>'),
#              'service-get': CmdEntry(service_get,
#                                      'Get network service property by name',
#                                      '<service path> [property]'),
#              'service-set': CmdEntry(service_set,
#                                      'Set network service property by name, value',  # noqa
#                                      '<service path> <property> <value>'),
#              'service-rm': CmdEntry(service_rm,
#                                     'Remove network service',
#                                     '<service path>'),
#              'technology-get': CmdEntry(technology_get,
#                                         'Get network technology property by name',  # noqa
#                                         '<tech path> [property]'),
#              'technology-set': CmdEntry(technology_set,
#                                         'Set network technology property by name, value',  # noqa
#                                         '<tech path> <property> <value>'),
#              'technology-info': CmdEntry(technology_info,
#                                          'Display information about a network technology',  # noqa
#                                          '<tech path>'),
#              'technology-scan': CmdEntry(technology_scan,
#                                          'Scan a network technology for services',  # noqa
#                                          '<tech path>'),
#              'service-disconnect': CmdEntry(service_disconnect,
#                                             'Disconnect a network device',
#                                             '<service path>'),
#              'service-connect': CmdEntry(service_connect,
#                                          'Connect a network service',
#                                          '<service path>'),
#              'agent-start': CmdEntry(agent_start,
#                                      'Start network service authentication agent',  # noqa
#                                      '<agent path> [param=value] ...'),  # noqa
#              'agent-stop': CmdEntry(agent_stop,
#                                    'Stop network service authentication agent',
#                                    '<agent path>'),
#              }
#
#
# def invoke_command(text):
#     if (not text):
#         return
#     args = text.split(' ')
#     cmd = args.pop(0)
#     cmd_entry = cmd_table.get(cmd)
#     if (cmd_entry):
#         cmd_entry.func(args)
#     else:
#         print 'Error: Command "%s" was not recognized.' % cmd
#
#
# def timeout_handler(signum, frame):
#     while gobject.MainLoop().get_context().pending():
#         gobject.MainLoop().get_context().iteration(False)
#
#
# dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
# gobject.threads_init()
# signal.signal(signal.SIGALRM, timeout_handler)
# signal.setitimer(signal.ITIMER_REAL, 0.01, 0.01)
#
#
# # Main command processing loop
# while True:
#     text = raw_input("CONN> ")
#     invoke_command(text)
class NetworkMainloop(gobject.MainLoop):

    def __init__(self, service):
        super(NetworkMainloop, self).__init__()
        self.__service = service
    #
    # def __stdin_cb(self, fd, condition):
    #     if condition & gobject.IO_IN:
    #         line = sys.stdin.readline().decode(coding, 'ignore').rstrip('\n\r')
    #         if len(line) > 0:
    #             args = line.split('|')
    #             self.__service.Message(args[0], args[1:])
    #     if condition & gobject.IO_HUP:
    #         exit()
    #     return True

    def run(self):
        # gobject.io_add_watch(0, gobject.IO_IN | gobject.IO_HUP, self.__stdin_cb)
        super(NetworkMainloop, self).run()



class NetworkAdapter(threading.Thread):

    def __init__(self, lock, socketio=None):
        self.lock = lock
        self.socketio = socketio

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        service = NetworkObject(dbus.SessionBus(),self.socketio)
        mainloop = NetworkMainloop(service)
        mainloop.run()