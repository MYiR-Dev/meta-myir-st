#!/bin/sh

eeprom_135_test -d /dev/i2c-0 -a 0x50 -s 0x00 -r 25 > eeprom.txt
eeprom_135_test -d /dev/i2c-0 -a 0x50 -s 0x20 -r 20 >> eeprom.txt

echo ">>>PN=`cat eeprom.txt | grep PN | awk -F : '{print $3}'`"
echo ">>>PN=`cat eeprom.txt | grep PN | awk -F : '{print $3}'`"

echo ">>>SN=`cat eeprom.txt | grep SN | awk -F : '{print $3}'`"
echo ">>>SN=`cat eeprom.txt | grep SN | awk -F : '{print $3}'`"

echo "stm32mp13-disco login: root (super user)"

