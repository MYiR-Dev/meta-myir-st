FILESEXTRAPATHS_prepend_stm32mpcommon := "${THISDIR}/tf-a-myir:"

SECTION = "bootloaders"

LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://license.rst;md5=1dd070c98a281d18d9eefd938729b031"

#--------------------
# gitee
#--------------------
#SRC_URI += "git://gitee.com/lichang70/stm32mp15xc-tf-a.git;protocol=https;branch=stm32mp-ya15xc"
#SRCREV= "4c7f691f2d23512c69701ee2b6fb1bfa51f64862"

#-------------------
# github
#-------------------
SRC_URI += "git://github.com/MYiR-Dev/myir-st-arm-trusted-firmware.git;protocol=https;branch=develop"
SRCREV= "23ff275700c1389f06160ff38eed1e5d55477136"


TF_VERSION = "2.2"
PV = "${TF_VERSION}.r1"

S = "${WORKDIR}/git"
#S = "${WORKDIR}/arm-trusted-firmware"

# ---------------------------------
# Configure devupstream class usage
# ---------------------------------
BBCLASSEXTEND = "devupstream:target"

#--------------------
# gitee
#--------------------
#SRC_URI_class-devupstream ="git://gitee.com/lichang70/stm32mp15xc-tf-a.git;protocol=https;branch=stm32mp-ya15xc"
#SRCREV_class-devupstream ="4c7f691f2d23512c69701ee2b6fb1bfa51f64862"


#-------------------
# github
#-------------------
SRC_URI_class-devupstream ="git://github.com/MYiR-Dev/myir-st-arm-trusted-firmware.git;protocol=https;branch=develop"
SRCREV_class-devupstream ="23ff275700c1389f06160ff38eed1e5d55477136"



SRCREV_FORMAT_class-devupstream = "tfa"
PV_class-devupstream = "${TF_VERSION}+github+${SRCPV}"

# ---------------------------------
# Configure default preference to manage dynamic selection between tarball and github
# ---------------------------------
STM32MP_SOURCE_SELECTION ?= "tarball"

DEFAULT_PREFERENCE = "${@bb.utils.contains('STM32MP_SOURCE_SELECTION', 'github', '-1', '1', d)}"
