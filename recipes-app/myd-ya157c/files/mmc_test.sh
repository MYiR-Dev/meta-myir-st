#/bin/bash
SD_DRIVE=""
EMMC_DRIVE=""
TEST_DRIVE=""

check_for_emmc()
{
        #
        # Check the eMMC was whether identified or not
        #
        mmc=$(grep -l 'MMC$' /sys/bus/mmc/devices/*/type)
        if [ "$mmc" != "" ]; then
        
            mmc_card=$(basename $(dirname $(grep -l 'MMC$' /sys/bus/mmc/devices/*/type))) > /dev/null 2>&1

            if [ -d  /sys/bus/mmc/devices/$mmc_card/block/mmcblk0/ ]; then
                    EMMC_DRIVE="/dev/mmcblk0"
                    TEST_DRIVE=$EMMC_DRIVE"p1"
            elif [ -d  /sys/bus/mmc/devices/$mmc_card/block/mmcblk1/ ]; then
                    EMMC_DRIVE="/dev/mmcblk1"
                    TEST_DRIVE=$EMMC_DRIVE"p1"
            else
                    echo -e "===> No valid emmc"
            fi

            echo  "===> found emmc "$EMMC_DRIVE " on " $mmc_card
        else
            echo -e "===> No valid emmc"  
        fi
}
check_for_sdcards()
{
        sd=$(grep -l 'SD$' /sys/bus/mmc/devices/*/type)
        if [ "$sd" != "" ]; then

            sd_card=$(basename $(dirname $(grep -l 'SD$' /sys/bus/mmc/devices/*/type)))  > /dev/null 2>&1

            # Find the avaible SD cards
            if [ -d  /sys/bus/mmc/devices/$sd_card/block/mmcblk0/ ]; then
                    SD_DRIVE="/dev/mmcblk0"
                    TEST_DRIVE=$SD_DRIVE"p1" 

            elif [ -d  /sys/bus/mmc/devices/$sd_card/block/mmcblk1/ ]; then
                    SD_DRIVE="/dev/mmcblk1"
                    TEST_DRIVE=$SD_DRIVE"p1" 
            else
                    echo -e "===> Please insert a SD/TF card"
            fi
                    echo "===> found sd "$SD_DRIVE" on " $sd_card
        else
            echo -e "===> Please insert a SD/TF card"  
        fi
}
if [ $1 == 0 ]; then
        check_for_sdcards
        echo "$TEST_DRIVE"
else
        check_for_emmc
        echo "$TEST_DRIVE"
fi
while true; do
    while true; do
        if [ "$TEST_DRIVE" != "" ]; then
                    busybox  sleep 1
            if [  "$TEST_DRIVE" != "" ]; then
                break
            fi
        else
                    busybox sleep 1
                    if [ $1 == 0 ]; then                                                                               
                            check_for_sdcards                                            
                    else                                                                   
                            check_for_emmc                                                 
                    fi  
        fi
    done
        
    if [ ! -d "/tmp/extsd" ]; then
       mkdir -p /tmp/extsd
    fi
        
    mount -t vfat $TEST_DRIVE /tmp/extsd

    break
done
    
    capacity=`busybox df | busybox grep "/tmp/extsd" | busybox awk '{printf $2}'`
    echo "$mmcp: $capacity"
    
    umount /tmp/extsd
    
    echo $capacity > /tmp/sd_capacity
