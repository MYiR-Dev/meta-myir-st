import logging
#from threading import Lock, Thread
from multiprocessing import Process,Value,Lock
import multiprocessing
from flask_socketio import SocketIO
from flask import Flask, send_from_directory, render_template, session, request, current_app
from flask_appbuilder import SQLA, AppBuilder, has_access
from mxde import MxdeManager
from network import  NetworkManager, NetworkObject
from globalvar import GlobalIp
from iw_parse import Iwlist_Parse
import commands
import dbus

version = "0.1.0"
"""
 Logging configuration
"""
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.WARNING)

app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
iw_parse = Iwlist_Parse()
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = 'gevent'
#ping_interval=1
socketio = SocketIO(app, async_mode=async_mode, ping_interval=1)

global_ip_config = GlobalIp()
mxde_manager = MxdeManager(socketio)
network_manager = NetworkManager(socketio,global_ip_config)

appbuilder = AppBuilder(app, db.session)
appbuilder.app.mqtt_connected = "disconnected"
appbuilder.app.eth_status = "OFF"
appbuilder.app.wifi_status = "OFF"
appbuilder.app.mobile_status = "OFF"
appbuilder.app.memory_size = "256MB"
appbuilder.app.storage_size = "4GB"
appbuilder.app.mqtt_id = "MEASY_IOT_0001"

@app.route('/<path:filename>')
def serveStaticResource(filename):
	return send_from_directory('static/', filename)

@app.route('/<pagename>')
def admin(pagename):
    return render_template(pagename, appbuilder=appbuilder, async_mode=None)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    

from app import models, views, forms
from app import ws, mq, mxde, network,socketio
