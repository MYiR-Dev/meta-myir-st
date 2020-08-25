#!/bin/bash
SD_DRIVE=
check_for_sdcards()
{
	sd_card=$(basename $(dirname $(grep -l 'SD$' /sys/bus/mmc/devices/*/type)))  > /dev/null 2>&1

	# Find the avaible SD cards
	if [ -d  /sys/bus/mmc/devices/$sd_card/block/mmcblk0/ ]; then
		SD_DRIVE="/dev/mmcblk0"

	elif [ -d  /sys/bus/mmc/devices/$sd_card/block/mmcblk1/ ]; then
		SD_DRIVE="/dev/mmcblk1"
	else
		echo -e "===> No valid emmc"
		exit 1
	fi

}
up() {
#while true; do
#    for nr in a b c d e f g h i j k l m n o p q r s t u v w x y z; do
#        udisk="/dev/block/sd$nr"
#        udisk="/dev/block/sda"
        udisk0="/dev/sda"
        udisk1="/dev/sdb"
        udisk2="/dev/sdc"
        udisk3="/dev/sdd"
#        udiskp=$udisk"1"
        udiskp0=$udisk0"1"
        udiskp1=$udisk1"1"
        udiskp2=$udisk2"1"
        udiskp3=$udisk3"1"
#        part=$udisk
#        part1=$udisk1
#        part2=$udisk2
#        part3=$udisk3
    
        #echo "searching disk ..." >> LOG_FILE
        while true; do
#            while true; do
#                if [ -b "$udisk" ]; then
#                    busybox sleep 1
#                    if [ -b "$udisk" ]; then
#                        echo "udisk insert"
#                        break;
#                    fi
#                else
#                    busybox sleep 1
#                fi
#            done
            
#            if [ ! -d "/tmp/udisk" ]; then
#                busybox mkdir -p /tmp/udisk
                busybox mkdir -p /tmp/card0
                busybox mkdir -p /tmp/card1
                busybox mkdir -p /tmp/card2
                busybox mkdir -p /tmp/card3
#            fi
            
            #echo "mounting disk ..." >> LOG_FILE
#            busybox mount -t vfat $udisk /tmp/udisk
            busybox mount -t vfat $udisk0 /tmp/card0 > /dev/null 2>&1
            busybox mount -t vfat $udisk1 /tmp/card1 > /dev/null 2>&1
            busybox mount -t vfat $udisk2 /tmp/card2 > /dev/null 2>&1
            busybox mount -t vfat $udisk3 /tmp/card3 > /dev/null 2>&1
#            if [ $? -ne 0 ]; then
#                busybox mount -t vfat $udiskp /tmp/udisk
                busybox mount -t vfat $udiskp0 /tmp/card0 > /dev/null 2>&1
                busybox mount -t vfat $udiskp1 /tmp/card1 > /dev/null 2>&1
                busybox mount -t vfat $udiskp2 /tmp/card2 > /dev/null 2>&1
                busybox mount -t vfat $udiskp3 /tmp/card3 > /dev/null 2>&1
#                if [ $? -ne 0 ]; then
#                    echo "udisk mount failed" >> LOG_FILE
#                    exit 1
                    #SEND_CMD_PIPE_FAIL $3
                    #busybox sleep 3
                    # goto for nr in ...
                    # detect next plugin, the devno will changed
                    #continue 2
#                else
#                    part=$udiskp
#                    part1=$udiskp1
#                    part2=$udiskp2
#                    part3=$udiskp3
#                fi
#            fi
    
          break
        done
    
#        capacity=`busybox df | busybox grep /tmp/udisk | busybox awk '{printf $2}'`
        capacity0=`busybox df | busybox grep /tmp/card0 | busybox awk '{printf $2}'`
        capacity1=`busybox df | busybox grep /tmp/card1 | busybox awk '{printf $2}'`
        capacity2=`busybox df | busybox grep /tmp/card2 | busybox awk '{printf $2}'`
        capacity3=`busybox df | busybox grep /tmp/card3 | busybox awk '{printf $2}'`
        #echo "$part: $capacity" >> LOG_FILE

#        busybox umount /tmp/udisk
#        busybox umount /tmp/udisk0 > /dev/null 2>&1
#        busybox umount /tmp/udisk1 > /dev/null 2>&1
#        busybox umount /tmp/udisk2 > /dev/null 2>&1
#        busybox umount /tmp/udisk3 > /dev/null 2>&1
        #SEND_CMD_PIPE_OK_EX $3 $capacity

#        echo $capacity > /tmp/udisk_capacity.txt
if [ -n "$capacity0" ]; then
	echo "udisk capacity" $capacity0
        echo $capacity0 > /tmp/capacity0.txt
fi
if [ -n "$capacity1" ]; then
	echo "udisk capacity" $capacity1
        echo $capacity1 > /tmp/capacity1.txt
fi
if [ -n "$capacity2" ]; then
	echo "udisk capacity" $capacity2
        echo $capacity2 > /tmp/capacity2.txt
fi
if [ -n "$capacity3" ]; then
	echo "udisk capacity" $capacity3
        echo $capacity3 > /tmp/capacity3.txt
fi
#        break
    
#        while true; do
#            if [ -b "$udisk" ]; then
#                echo "please remove udisk"
#                busybox sleep 1
#            else
#                echo "udisk removed"
#                break
#            fi
#        done
#    done
#done


}

down() {
	echo "usb host test end"
#        busybox umount /tmp/udisk
        busybox umount /tmp/card0 > /dev/null 2>&1
        busybox umount /tmp/card1 > /dev/null 2>&1
        busybox umount /tmp/card2 > /dev/null 2>&1
        busybox umount /tmp/card3 > /dev/null 2>&1
	
	rm -rf /tmp/capacity*
}

if [ "$1" = "1" ]; then
#	echo "install "
	check_for_sdcards
	modprobe g_mass_storage stall=0 file=$SD_DRIVE"p1" removable=1
	sleep 5
	up
fi

if [ "$1" = "0" ]; then
#	echo "uninstall"
	down
fi
