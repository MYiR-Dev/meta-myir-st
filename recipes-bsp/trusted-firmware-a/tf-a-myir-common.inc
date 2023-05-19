FILESEXTRAPATHS:prepend := "${THISDIR}/tf-a-myir:"

SECTION = "bootloaders"

LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://license.rst;md5=1dd070c98a281d18d9eefd938729b031"

#SRC_URI = "git://github.com:myir-private/myir-st-tfa.git;protocol=https;branch=develop-v2.6-stm32mp"
#SRCREV = "4cc966a5372b13517343009b2f8797cb99828ce8"

SRC_URI = "git://github.com/MYiR-Dev/myir-st-arm-trusted-firmware.git;protocol=https;branch=${SRCBRANCH}"
SRCREV = "4cc966a5372b13517343009b2f8797cb99828ce8"
SRCBRANCH = "develop-yf13x-v2.6"



TF_A_VERSION = "v2.6"
TF_A_SUBVERSION = "stm32mp"
TF_A_RELEASE = "r2"
PV = "${TF_A_VERSION}-${TF_A_SUBVERSION}-${TF_A_RELEASE}"

ARCHIVER_ST_BRANCH = "develop-${TF_A_VERSION}-${TF_A_SUBVERSION}"
ARCHIVER_ST_REVISION = "${PV}"
ARCHIVER_COMMUNITY_BRANCH = "develop-v2.6-stm32mp"
ARCHIVER_COMMUNITY_REVISION = "${TF_A_VERSION}"

S = "${WORKDIR}/git"

# ---------------------------------
# Configure devupstream class usage
# ---------------------------------
BBCLASSEXTEND = "devupstream:target"

SRC_URI:class-devupstream = "git://github.com/MYiR-Dev/myir-st-arm-trusted-firmware.git;protocol=https;branch=${SRCBRANCH}"
SRCREV:class-devupstream = "4cc966a5372b13517343009b2f8797cb99828ce8"

# ---------------------------------
# Configure default preference to manage dynamic selection between tarball and github
# ---------------------------------
STM32MP_SOURCE_SELECTION ?= "tarball"

DEFAULT_PREFERENCE = "${@bb.utils.contains('STM32MP_SOURCE_SELECTION', 'github', '-1', '1', d)}"
