#!/bin/bash

echo "start up wifi ..."
wpa_passphrase MYiR-Tech 12345678 >> /run/wpa_supplicant.conf
ifconfig wlan0 up
wpa_supplicant -B -iwlan0 -c /run/wpa_supplicant.conf
dhclient wlan0
iw wlan0 link
