#!/bin/sh -e


echo "start myir HMI 2.0..."

export QT_QPA_EGLFS_ALWAYS_SET_MODE="1"
export QT_QPA_EGLFS_KMS_ATOMIC='1'
export QT_QPA_EGLFS_KMS_CONFIG='/usr/share/qt5/cursor.json'
#export QT_QPA_PLATFORM='eglfs'
psplash-drm-quit

strA=$(cat /sys/firmware/devicetree/base/compatible)
strB="ya157c"

result=$(echo $strA | grep "${strB}")
if [[ "$result" != "" ]]
then
        export QT_QPA_PLATFORM='eglfs'
        /home/mxapp2 -platform eglfs &
else
        /home/mxapp2 -platform linuxfb &
fi

exit 0

