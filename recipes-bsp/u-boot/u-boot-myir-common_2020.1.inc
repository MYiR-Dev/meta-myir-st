# Adaptation from u-boot-common_${PV}.inc

HOMEPAGE = "http://www.denx.de/wiki/U-Boot/WebHome"
SECTION = "bootloaders"

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://Licenses/README;md5=30503fd321432fc713238f582193b78e"

DEPENDS += "dtc-native bc-native"
DEPENDS += "flex-native bison-native"

COMPATIBLE_MACHINE = "(stm32mpcommon)"

#-----------------
# github
#-----------------
SRC_URI += " \
        git://github.com/MYiR-Dev/myir-st-u-boot.git;protocol=https;branch=develop"
#SRCREV= "797b0dca64646f895c1261ca2574a47b33384fe4"
SRCREV= "62f4cbc47284b674a974849368dfd6add469f7ea"


U_BOOT_VERSION = "2020.1"
PV = "${U_BOOT_VERSION}"

S = "${WORKDIR}/git"

# ---------------------------------
# Configure devupstream class usage
# ---------------------------------
BBCLASSEXTEND = "devupstream:target"


#-----------------
# github
#-----------------
SRC_URI_class-devupstream = "git://github.com/MYiR-Dev/myir-st-u-boot.git;protocol=https;branch=develop"
#SRCREV= "797b0dca64646f895c1261ca2574a47b33384fe4"
SRCREV= "62f4cbc47284b674a974849368dfd6add469f7ea"

SRCREV_FORMAT_class-devupstream = "uboot"
PV_class-devupstream = "${U_BOOT_VERSION}+github+${SRCPV}"

# ---------------------------------
# Configure default preference to manage dynamic selection between tarball and github
# ---------------------------------
STM32MP_SOURCE_SELECTION ?= "github"

DEFAULT_PREFERENCE = "${@bb.utils.contains('STM32MP_SOURCE_SELECTION', 'github', '-1', '1', d)}"
