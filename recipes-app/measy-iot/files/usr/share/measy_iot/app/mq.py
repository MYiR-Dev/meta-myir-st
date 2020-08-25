import logging
import threading

import paho.mqtt.client as mqtt
from flask import session, request, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from app import appbuilder, app

class MQTTAdapter(threading.Thread):
    _stop = False

    def __init__(self, hostname, topic, statsd_topic, statsd_type,
                 statsd_client, port=1883, websocket=False, client_id=None,
                 keepalive=60, will=None, auth=None, tls=None, qos=0, socketio=None):
        super(MQTTAdapter, self).__init__()
        self.hostname = hostname
        self.port = port
        self.client_id = client_id
        self.keepalive = keepalive
        self.mqtt_topic = topic
        self.will = will
        self.auth = auth
        self.tls = tls
        self.qos = qos
        self.socketio = socketio
        transport = "tcp"
        if websocket:
            transport = "websocket"
        self.statsd_client = statsd_client
        self.statsd_topic = statsd_topic
        self.statsd_type = statsd_type
        self.client = mqtt.Client(transport=transport)
        if tls:
            self.client.tls_set(**tls)
        if auth:
            self.client.username_pw_set(auth['username'],
                                        password=auth.get('password'))

    def __del__(self):
        # self.client.disconnect()
        # self.client.on_message = NotImplemented
        # self.client.on_connect = NotImplemented
        # self.client.loop_stop(True)
        # self._stop = True
        # del self.client
        # self.client=None
        logging.error("MQTT thread destroyed!!")

    def run(self):
        def on_connect(client, userdata, flags, rc):
            if(self.mqtt_topic):
                client.subscribe(self.mqtt_topic)

            replies = {0: "Connection successful",
                       1: "Connection refused - incorrect protocol version",
                       2: "Connection refused - invalid client identifier",
                       3: "Connection refused - server unavailable",
                       4: "Connection refused - bad username or password",
                       5: "Connection refused - not authorised"}
            print replies[rc]

            self.socketio.emit("mqtt_connection", {"status":"connected"}, namespace='/test')
            appbuilder.app.mqtt_connected = "connected"

        def on_disconnect(client, userdata, rc):
            self.socketio.emit("mqtt_connection", {"status":"disconnected"}, namespace='/test')
            appbuilder.app.mqtt_connected = "disconnected"

        def on_message(client, userdata, msg):
            logging.info(msg.topic + msg.payload)
            self.socketio.emit("mqtt_message",{'data': msg.payload, 'count': msg.topic}, namespace='/test')
            # self.socketio.emit("my_response",{'data': msg.payload, 'count': 100}, namespace='/test')
            if self.statsd_type == 'gauge':
                self.statsd_client.gauge(self.statsd_topic, msg.payload)
            elif self.statsd_type == 'timer':
                self.statsd_client.timer(self.statsd_topic, msg.payload)
            elif self.statsd_type == 'counter':
                self.statsd_client.incr(self.statsd_topic)

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect

        try:
            ret = self.client.connect(self.hostname, self.port)
        except Exception, e:
            self.client.disconnect()

        while not self._stop and self.client.loop_forever()==0:
            pass
        logging.error("MQTT thread terminated!!")
        self.socketio.emit("mqtt_connection", {"status": "disconnected"}, namespace='/test')

    def setStop(self,flag):
        self._stop = flag
        self.client.disconnect()
        self.client.loop_stop(True)
        del self.client
        self.client = None
        appbuilder.app.mqtt_connected = "disconnected"

    def subscribe(self, topic, qos):
        self.client.subscribe(topic, qos)

    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)

    def publish(self,topic, message, qos):
        self.client.publish(topic, message, qos, retain=0)