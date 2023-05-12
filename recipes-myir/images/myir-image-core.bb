SUMMARY = "OpenSTLinux core image."
LICENSE = "Proprietary"

include recipes-st/images/myir-image.inc

inherit core-image

IMAGE_LINGUAS = "en-us"

IMAGE_FEATURES += "\
    splash              \
    package-management  \
    ssh-server-dropbear \
    "

#
# INSTALL addons
#
CORE_IMAGE_EXTRA_INSTALL += " \
    resize-helper \
    \
    packagegroup-framework-core-base    \
    packagegroup-framework-tools-base   \
    \
    ${@bb.utils.contains('COMBINED_FEATURES', 'optee', 'packagegroup-optee-core', '', d)}   \
    ${@bb.utils.contains('COMBINED_FEATURES', 'optee', 'packagegroup-optee-test', '', d)}   \
    libmodbus \
    iperf3 \
    udev-extraconf \
    genext2fs \
    ppp \
    ecm \
    check-snpn \
    camera-demo \
    "
# NOTE:
#   packagegroup-st-demo are installed on rootfs to populate the package
#   database.


ROOTFS_POSTPROCESS_COMMAND:append = "install_demo;"
install_demo() {

 echo "bash eeprom.sh" >> ${IMAGE_ROOTFS}/etc/profile
 
 sed -i 's/myd-yf13x.*/myd-yf13x/g' ${IMAGE_ROOTFS}/etc/hosts
 sed -i 's/myd-yf13x.*/myd-yf13x/g' ${IMAGE_ROOTFS}/etc/hostname
    
}
