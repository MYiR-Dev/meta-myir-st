# Adaptation from u-boot-common_${PV}.inc

HOMEPAGE = "http://www.denx.de/wiki/U-Boot/WebHome"
SECTION = "bootloaders"

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://Licenses/README;md5=30503fd321432fc713238f582193b78e"

DEPENDS += "dtc-native bc-native"
DEPENDS += "flex-native bison-native"

COMPATIBLE_MACHINE = "(stm32mpcommon)"


#-----------------
# gitee
#-----------------
#SRC_URI += " \
#        git://gitee.com/lichang70/stm32mp15xc-uboot.git;protocol=https;branch=stm32mp-ya15xc"
#SRCREV= "06dffe26f118cc887d64b5d5714e11262960ab84"

#-----------------
# github
#-----------------
SRC_URI += " \
        git://github.com/MYiR-Dev/myir-st-u-boot.git;protocol=https;branch=develop"
SRCREV= "f6d1edcd80723c7c82ccd7f27957c8442c788df3"


U_BOOT_VERSION = "2020.1"
PV = "${U_BOOT_VERSION}"

S = "${WORKDIR}/git"

# ---------------------------------
# Configure devupstream class usage
# ---------------------------------
BBCLASSEXTEND = "devupstream:target"

#------------------
# gitee
#------------------
#SRC_URI_class-devupstream = "git://gitee.com/lichang70/stm32mp15xc-uboot.git;protocol=https;branch=stm32mp-ya15xc"
#SRCREV= "06dffe26f118cc887d64b5d5714e11262960ab84"

#-----------------
# github
#-----------------
SRC_URI_class-devupstream = "git://github.com/MYiR-Dev/myir-st-u-boot.git;protocol=https;branch=develop"
SRCREV= "f6d1edcd80723c7c82ccd7f27957c8442c788df3"

SRCREV_FORMAT_class-devupstream = "uboot"
PV_class-devupstream = "${U_BOOT_VERSION}+github+${SRCPV}"

# ---------------------------------
# Configure default preference to manage dynamic selection between tarball and github
# ---------------------------------
STM32MP_SOURCE_SELECTION ?= "github"

DEFAULT_PREFERENCE = "${@bb.utils.contains('STM32MP_SOURCE_SELECTION', 'github', '-1', '1', d)}"
