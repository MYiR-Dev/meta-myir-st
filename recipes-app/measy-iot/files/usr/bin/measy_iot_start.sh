if test -z "$DBUS_SESSION_BUS_ADDRESS" ; then
        eval `dbus-launch --sh-syntax`
        echo "D-Bus per-session daemon address is: $DBUS_SESSION_BUS_ADDRESS"
fi
export DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS"
#systemctl disable systemd-networkd.service
#sleep 5
#MAC=$(ifconfig eth0|grep eth0|awk '{print $5}' | sed 's/://g' | tr '[A-Z]' '[a-z]')
#connmanctl config "ethernet_"$MAC"_cable" --ipv4 manual 192.168.1.100 255.255.255.0 192.168.1.1

date -s "2020-1-1 1:1:1"
myir_iec61850_server & >> /usr/share/iec.txt
python2.7 /usr/share/measy_iot/run.py & >> /usr/share/iot.txt
