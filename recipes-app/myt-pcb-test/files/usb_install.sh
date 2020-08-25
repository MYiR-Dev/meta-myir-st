#!/bin/sh

mkfs.fat /dev/ram1

if [ $? -ne 0 ];then
	exit 1;
fi

modprobe g_mass_storage stall=0 removable=1 file=/dev/ram1
if [ $? -ne 0 ];then   
    exit 1;        
fi

sleep 3
mkdir /media/sda > /dev/null
mount /dev/sda /media/sda
if [ $? -ne 0 ];then
	exit 1;
fi
