import logging
import commands
import os
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask import session, request, json, current_app
from app import appbuilder,app, socketio,iw_parse, mxde_manager, network_manager,global_ip_config
from threading import Lock, Thread
from app.mq import MQTTAdapter
import copy
from ifparser import Ifcfg
from itertools import islice
thread = None
thread_lock = Lock()

socketio.mqtt_adapter = None
wifi_is_connect =0

def _get_wifi_statu():
    global wifi_is_connect
    command = "iwconfig wlan0 | grep ESSID"
    (status, wlan) = commands.getstatusoutput(command)
    wifi_connect = wlan.split(":")[1]

    command = "ps -ef | grep wpa_supplicant| grep -v grep"
    (status, output) = commands.getstatusoutput(command)
    if output != "":
        wifi_switch = "on"
        appbuilder.app.wifi_status = "ON"

    else:
        wifi_switch = "off"
        appbuilder.app.wifi_status = "OFF"
    wifi_status ={}
    wifi_status["switch"] = wifi_switch

    if "off/any" in wifi_connect :
        wifi_status["connect"] = wifi_connect[:-2]
        wifi_is_connect = 0
    else:
        if wifi_is_connect == 0:
            command = "udhcpc -i wlan0 -b"
            # commands.getstatusoutput(command)
            os.system(command)
            wifi_is_connect = 1
            ifdata = Ifcfg(commands.getoutput('ifconfig'))
            if "wlan0" in ifdata.interfaces:
                wlan0 = ifdata.get_interface('wlan0')
                temp = wlan0.ip.split(".")
                wlan_gw = temp[0] + "." + temp[1] + "." + temp[2] + ".1"
                command = "route del -net 0.0.0.0 "
                os.system(command)
                command = "route add default gw " + wlan_gw + " wlan0 "
                print command
                os.system(command)
        wifi_status["connect"] = wifi_connect[1:-3]
        appbuilder.app.wifi_status = wifi_connect[1:-3]
    return wifi_status
def _get_4g_statu():
    mobile_info = {}

    command = "ps | grep pppd| grep -v grep"
    (status, output) = commands.getstatusoutput(command)
    if output != "":
        mobile_switch = "on"
        appbuilder.app.mobile_status = "ON"
    else:
        mobile_switch = "off"
        appbuilder.app.mobile_status = "OFF"
    mobile_info["switch"] = mobile_switch

    ifdata = Ifcfg(commands.getoutput('ifconfig'))
    if "ppp0" in ifdata.interfaces:
        ppp0 = ifdata.get_interface('ppp0')
        mobile_info["ip"] = ppp0.ip
        mobile_info["ptp"] = ppp0.ptp
        mobile_info["mask"] = ppp0.mask
        print mobile_info["ip"]
        if mobile_info["ip"] :
            appbuilder.app.mobile_status = "4G"
    return mobile_info

def _get_ethernet_statu():
    eth_info = {}

    ifdata = Ifcfg(commands.getoutput('ifconfig'))
    if "eth1" in ifdata.interfaces:
        eth = ifdata.get_interface('eth1')
        eth_info["ip"] = eth.ip
        eth_info["bcast"] = eth.bcast
        eth_info["mask"] = eth.mask
        if not eth_info["ip"] :
            appbuilder.app.eth_status = "OFF"
        else:
            appbuilder.app.eth_status = "ON"
    return eth_info
def get_nand_size():
    sum = 0
    parts = open("/proc/partitions")

    for line in islice(parts, 2, None):
        t = line.split()[3]
        s = line.split()[2]
        if 'mtdblock' in t:
            sum = sum + int(s)
    sum = sum / 1024
    return str(sum) + 'MB'+ " NAND"
def get_memory_size():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes / (1024. ** 3)
    if 0.6 < mem_gib:
        appbuilder.app.memory_size = "1GB"
    if 0.4 < mem_gib < 0.6:
        appbuilder.app.memory_size = "512MB"
    if 0.1 < mem_gib < 0.3:
        appbuilder.app.memory_size = "256MB"
    if mem_gib < 0.1:
        appbuilder.app.memory_size = "128MB"

def get_storage_size():
    command = "cat /proc/cmdline"
    str_param='rootfstype='
    len_str_check=len(str_param)
    (status, output) = commands.getstatusoutput(command)
    read_param = output.split(" ")
    if str_param in read_param:
        for i in range(0,len(read_param)):
            if read_param[i][0:len_str_check]==str_param:
                rel=read_param[i][len_str_check:]
                if rel == "ubifs":
                    nand_size = get_nand_size()
                    appbuilder.app.storage_size = nand_size
    else:
        appbuilder.app.storage_size = "4GB EMMC"
def get_mqtt_id():
    command = "ifconfig eth0|grep eth0|awk '{print $5}' | sed 's/://g'"
    base_str ='MEASY_IOT_'
    (status, output) = commands.getstatusoutput(command)
    mqtt_str = base_str + output
    appbuilder.app.mqtt_id = mqtt_str
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    get_memory_size()
    get_storage_size()
    get_mqtt_id()


    while True:
        socketio.sleep(2)
        count += 1

        wifi_status = _get_wifi_statu()
        # if cmp(wifi_status, wifi_status_old) != 0:
        #     wifi_status_old = wifi_status
        socketio.emit("wifi_badge_status", wifi_status, namespace='/test')
        mobile_status = _get_4g_statu()
        # if cmp(mobile_status, mobile_status_old) != 0:
        #     mobile_status_old = mobile_status
        socketio.emit("mobile_status", mobile_status, namespace='/test')
        eth_status = _get_ethernet_statu()
        socketio.emit("eth_badge_status", eth_status, namespace='/test')

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    # emit('my_response', {'data': 'ws Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid, request.namespace )

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('adc_update', namespace='/test')
def adc_update(message):
    res = mxde_manager.updateAdcValue()
    adc= res.split(" ")
    str = dict()
    str['adc1'] = adc[0]
    str['adc2'] = adc[1]
    str['adc3'] = adc[2]
    str['adc4'] = adc[3]
    socketio.emit("adc_values", str, namespace='/test')

@socketio.on('get_led_status', namespace='/test')
def get_led_status(message):
    res = mxde_manager.getLedList()
    leds = res.split("\n")
    led_status = dict()
    led_status['led1'] = leds[0].split(" ")[1]
    led_status['led2'] = leds[1].split(" ")[1]

    socketio.emit("led_status", led_status, namespace='/test')
ip_config = dict()
def parse_ip_config(res):
    ip = dict()
    list = []

    for i in res:
        (path, params) = i
        # print params['Ethernet'][1]['Interface'][1]
        ip['Path'] = path
        if params['IPv4'][1]['Method'][1] == "manual":

            ip['Method'] = params['IPv4'][1]['Method'][1]
            ip['Address'] = params['IPv4.Configuration'][1]['Address'][1]
            ip['Netmask'] = params['IPv4.Configuration'][1]['Netmask'][1]
            if "Gateway" in params['IPv4.Configuration'][1].keys():
                ip['Gateway'] = params['IPv4.Configuration'][1]['Gateway'][1]
            # print "IPV4_MANUAL:%s" % ip
            ip_config[params['Ethernet'][1]['Interface'][1]] = copy.copy(ip)
            global_ip_config.set_ip(params['Ethernet'][1]['Interface'][1],copy.copy(ip))
            global_ip_config.print_ip();
            # print ip_config
        else:
            ip['Method'] = params['IPv4'][1]['Method'][1]
            ip['Address'] = params['IPv4'][1]['Address'][1]
            ip['Netmask'] = params['IPv4'][1]['Netmask'][1]
            # print params['IPv4'][1].keys()
            if "Gateway" in params['IPv4'][1].keys():
                ip['Gateway'] = params['IPv4'][1]['Gateway'][1]
            # print  "IPV4_DHCP:%s" % ip
            ip_config[params['Ethernet'][1]['Interface'][1]]= copy.copy(ip)
            global_ip_config.set_ip(params['Ethernet'][1]['Interface'][1], copy.copy(ip))
            global_ip_config.print_ip();
            # print ip_config
    return global_ip_config.get_ip();

@socketio.on('get_ethernet_config', namespace='/test')
def get_ethernet_config(message):
    res = network_manager.list_services()
    # print res
    ip_data = parse_ip_config(res)
    socketio.emit("ethernet_config", ip_data, namespace='/test')

@socketio.on('set_ethernet_config', namespace='/test')
def set_ethernet_config(message):
    res = json.loads(message['data'])
    # print res
    # print res['Interface']
    eth_cable = ip_config[res['Interface']]['Path'].split("/")[4]
    if res['Method'] == 'manual':
        command = "connmanctl config %s --ipv4 manual %s %s %s"%(eth_cable, res['Address'],res['Netmask'],res['Gateway'] )
    if res['Method'] == 'dhcp':
        command = "connmanctl config %s --ipv4 dhcp "%(eth_cable)
    # print command
    (status, output)=commands.getstatusoutput(command)
    # print status
    # print output
@socketio.on('get_wifi_statu', namespace='/test')
def get_wifi_statu(message):
    wifi_status = _get_wifi_statu()
    print wifi_status
    socketio.sleep(2)
    socketio.emit("wifi_status", wifi_status, namespace='/test')

    socketio.emit("wifi_badge_status", wifi_status, namespace='/test')
@socketio.on('wifi_open', namespace='/test')
def wifi_open(message):

    command = "killall wpa_supplicant"
    commands.getstatusoutput(command)

    command = "ifconfig wlan0 up"
    commands.getstatusoutput(command)
    socketio.sleep(2)
    networks = iw_parse.get_interfaces("wlan0")
    socketio.emit("wifi_list", networks, namespace='/test')
    command = "wpa_supplicant -i wlan0 -c /etc/wpa_supplicant.conf -B"
    commands.getstatusoutput(command)

@socketio.on('wifi_close', namespace='/test')
def wifi_close(message):

    command = "killall udhcpc"
    commands.getstatusoutput(command)

    command = "wpa_cli -i wlan0 disconnect"
    commands.getstatusoutput(command)

    command = "killall wpa_supplicant"
    commands.getstatusoutput(command)

    command = "ifconfig wlan0 down"
    commands.getstatusoutput(command)
@socketio.on('wifi_scan', namespace='/test')
def wifi_scan(message):

    command = "ifconfig wlan0 up"
    commands.getstatusoutput(command)
    socketio.sleep(1)
    networks = iw_parse.get_interfaces("wlan0")
    # print networks

    socketio.emit("wifi_list", networks, namespace='/test')

@socketio.on('wifi_disconnect', namespace='/test')
def wifi_disconnect(message):
    command = "wpa_cli -i wlan0 disconnect"
    commands.getstatusoutput(command)




@socketio.on('wifi_connect_info', namespace='/test')
def wifi_connect(wifi_info):
    print wifi_info['wifi_essid']
    print wifi_info['wifi_passwd']
    print wifi_info['wifi_encryption']
    encryption = wifi_info['wifi_encryption']
    ssid = wifi_info['wifi_essid']
    passwd = wifi_info['wifi_passwd']
    if encryption =='Open':
        command = "wpa_cli -i wlan0 add_network"
        (status, wifi_id) = commands.getstatusoutput(command)

        command =  "wpa_cli -i wlan0 set_network " + wifi_id + " ssid " + "\'\""+ssid+"\"\'"
        commands.getstatusoutput(command)

        command = "wpa_cli -i wlan0 set_network "+ wifi_id +" key_mgmt NONE"
        commands.getstatusoutput(command)

        command = "wpa_cli -i wlan0 select_network "+wifi_id
        commands.getstatusoutput(command)

        # command = "udhcpc -i wlan0 "
        # commands.getstatusoutput(command)
    else:
        command = "wpa_cli -i wlan0 add_network"
        (status, wifi_id) = commands.getstatusoutput(command)

        command =  "wpa_cli -i wlan0 set_network " + wifi_id + " ssid " + "\'\""+ssid+"\"\'"
        commands.getstatusoutput(command)

        command = "wpa_cli -i wlan0 set_network "+ wifi_id + " psk "+ "\'\""+passwd+"\"\'"
        commands.getstatusoutput(command)

        command = "wpa_cli -i wlan0 select_network "+wifi_id
        commands.getstatusoutput(command)

        # command = "udhcpc -i wlan0 "
        # commands.getstatusoutput(command)


@socketio.on('4g_connect', namespace='/test')
def mobile_connect(message):

    command = "killall pppd"
    os.system(command)
    socketio.sleep(1)

    command = "pppd call quectel-ppp &"
    os.system(command)


@socketio.on('4g_disconnect', namespace='/test')
def mobile_disconnect(message):
    command = "killall pppd"
    os.system(command)
@socketio.on('get_4g_status', namespace='/test')
def get_4g_status(message):
    mobile_status = _get_4g_statu()
    socketio.emit("mobile_status", mobile_status, namespace='/test')
@socketio.on('mq_connect',  namespace='/test')
def mq_connect(message):

    data = json.loads(message['data'])
    logging.error("create mqtt connection")
    pclientid = data['mq_clientid']
    phost = data['mq_host']
    if data['mq_port']:
        pport = int(data['mq_port'])
    else:
        pport = 0
    pqos = int(data['mq_qos'])

    try:
        socketio.mqtt_adapter = MQTTAdapter(phost, None, None, 1,
                        "1", pport, websocket=None, client_id=pclientid,
                          auth=None, tls=None, keepalive=60,
                         qos=pqos, socketio=socketio)
        socketio.mqtt_adapter.start()
        # mqtt_adapter.setDaemon(True)
    except Exception, e:
        # mqtt_adapter.disconnect()
        # mqtt_adapter.reconnect()
        socketio.sleep(3)
        socketio.emit("mqtt_connection", {"status": "disconnected"}, namespace='/test')
        print "Error:{0} ".format(str(e))

@socketio.on('mq_disconnect', namespace='/test')
def mq_disconnect():
    logging.error("delete mqtt connection")
    if socketio.mqtt_adapter :
        socketio.mqtt_adapter.setStop(True)
        del socketio.mqtt_adapter
        socketio.mqtt_adapter = None

@socketio.on('mq_subscribe', namespace='/test')
def mq_subscribe(message):
    logging.info("susbscribe to "+ message['data'])
    data = json.loads(message['data'])
    if socketio.mqtt_adapter:
        socketio.mqtt_adapter.subscribe(data['mq_topic'], 1)

@socketio.on('mq_unsubscribe', namespace='/test')
def mq_unsubscribe(message):
    logging.info("unsubscribe "+ message['data'])
    data = json.loads(message['data'])
    if(socketio.mqtt_adapter):
        socketio.mqtt_adapter.unsubscribe(data['mq_topic'])

@socketio.on('mq_publish', namespace='/test')
def mq_publish(message):
    logging.info("publish "+ message['data'])
    data = json.loads(message['data'])
    pqos = int(data['mq_qos'])
    if(socketio.mqtt_adapter):
        socketio.mqtt_adapter.publish(data['mq_topic'], data['mq_message'], pqos)

if __name__ == '__main__':
    get_wifi_statu()




