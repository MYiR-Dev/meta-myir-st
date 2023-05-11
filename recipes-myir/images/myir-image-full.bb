SUMMARY = "OpenSTLinux weston image with basic Wayland support (if enable in distro)."
LICENSE = "Proprietary"

include recipes-st/images/st-image.inc

inherit populate_sdk_qt5
inherit core-image features_check

# let's make sure we have a good image...
REQUIRED_DISTRO_FEATURES = "wayland"

IMAGE_LINGUAS = "en-us"

IMAGE_FEATURES += "\
    splash              \
    package-management  \
    ssh-server-dropbear \
    hwcodecs            \
    tools-profile       \
    eclipse-debug       \
    "



#IMAGE_INSTALL:append : " \
#                        qtbase \    
#                         qtbase-plugins \    
#                         qtbase-tools  \
#                        "

#
# INSTALL addons
#
CORE_IMAGE_EXTRA_INSTALL += " \
    resize-helper \
    \
    packagegroup-framework-core-base    \
    packagegroup-framework-tools-base   \
    \
    packagegroup-framework-core         \
    packagegroup-framework-tools        \
    \
    packagegroup-framework-core-extra   \
    packagegroup-framework-sample-qt    \
    packagegroup-framework-sample-qt-extra   \
    \
    ${@bb.utils.contains('COMBINED_FEATURES', 'optee', 'packagegroup-optee-core', '', d)} \
    \
    ${@bb.utils.contains('COMBINED_FEATURES', 'tpm2', 'packagegroup-security-tpm2', '', d)} \
    \
    packagegroup-st-demo \
    libmodbus \
    qtvirtualkeyboard \
    "

# NOTE:
#   packagegroup-st-demo are installed on rootfs to populate the package
#   database.


ROOTFS_POSTPROCESS_COMMAND:append = "install_demo;"
install_demo() {


 
 sed -i 's/myd-yf13x.*/myd-yf13x/g' ${IMAGE_ROOTFS}/etc/hosts
 sed -i 's/myd-yf13x.*/myd-yf13x/g' ${IMAGE_ROOTFS}/etc/hostname
    
}
