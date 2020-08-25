#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process,Value,Lock
from multiprocessing import Queue
from threading import Lock, Thread
from measy_lib.utils import *
import dbus
import dbus.service
import dbus.mainloop.glib
import gobject
import sys
import time
from tdbus import SimpleDBusConnection,GEventDBusConnection, DBUS_BUS_SYSTEM,DBUS_BUS_SESSION ,DBusHandler, signal_handler, DBusError
import tdbus
class MxdeSignalNameNotRecognisedException:
    """
    Exception raised for when a signal name is not recognized.
    Check the originating class for a list of supported signal names
    """
    pass


DBUS_PATH="/com/myirtech/mxde"
DBUS_INTERFACE="com.myirtech.mxde.MxdeInterface"
DBUS_NAME="com.myirtech.mxde"
SIGNAL_LED_BRIGHTNESS_CHANGED='sigLedBrightnessChanged'
class MxdeObject(DBusHandler):
    def __init__(self, connect, sio):
        '''
        A DBUS signal handler class for the org.freedesktop.UPower.Device
        'Changed' event. To re-read the device data, a DBUS connection is
        required. This is established when an event is fired using the provided
        connect method.

        Essentially, this is a cluttered workaround for a bizarre object design
        and use of decorators in the tdbus library.

        :param connect: a DBUS system bus connection factory
        :param sio: the devices to watch
        '''
        super(MxdeObject, self).__init__()
        self.connect = connect
        self.sio = sio

    @signal_handler(member=SIGNAL_LED_BRIGHTNESS_CHANGED, interface=DBUS_INTERFACE)
    def sigLedChanged(self, message):
        res = message.get_args()[0]
        print res
        self.sio.emit("led_signal", {'data': res}, namespace='/test')

    def mxde_getLedList(self):
        res = self.connect.call_method(DBUS_PATH, 'getLedList',
                               interface=DBUS_INTERFACE, destination=DBUS_NAME)
        print res
        return res.get_args()[0]
    def mxde_updateAdcValue(self):
        res = self.connect.call_method(DBUS_PATH, 'updateAdcValue',
                               interface=DBUS_INTERFACE, destination=DBUS_NAME)
        print res
        return res.get_args()[0]
class MxdeManager(object):

    def __init__(self, sio=None):
        self.sio = sio
        self.connect = GEventDBusConnection(DBUS_BUS_SESSION)
        self.service = MxdeObject(self.connect, self.sio)
        self.connect.add_handler(self.service)
        self.connect.subscribe_to_signals()

    def getLedList(self):
        return self.service.mxde_getLedList()

    def updateAdcValue(self):
        return self.service.mxde_updateAdcValue()


if __name__ == '__main__':
     
    # sio  = None
    # # thread_lock = Lock()
    # # adapter = MxdeAdapter(thread_lock, sio)
    # # # adapter.start()
    # q = Queue()
    # l  = Lock()
    # print q
    # manager = MxdeManager(sio,q,l)
    #
    # manager.worker()
    # manager.handler()
    conn = GEventDBusConnection(DBUS_BUS_SESSION)
    hld = DbusHandler()
    conn.add_handler(hld)
    conn.subscribe_to_signals()

    res = conn.call_method(DBUS_PATH, 'getLedList',
                     interface=DBUS_INTERFACE, destination=DBUS_NAME)
    print res.get_args()[0]
    conn.dispatch()