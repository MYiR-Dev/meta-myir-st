# Adaptation from u-boot-common_${PV}.inc

HOMEPAGE = "http://www.denx.de/wiki/U-Boot/WebHome"
SECTION = "bootloaders"

LICENSE = "GPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://Licenses/README;md5=5a7450c57ffe5ae63fd732446b988025"

DEPENDS += "dtc-native bc-native"
DEPENDS += "flex-native bison-native"
DEPENDS += "python3-setuptools-native"

COMPATIBLE_MACHINE = "(stm32mpcommon)"

#SRC_URI = "git://github.com/myir-private/myir-st-uboot.git;protocol=https;branch=develop-v2021.10-stm32mp"
SRC_URI = "git:///media/system1/home/nene/ST/yt135-duxy/sources/uboot/myir-st-uboot;protocol=file;branch=${SRCBRANCH}"
SRCREV  = "742d0c3ea3a65a3f8edb26e8906a5133d503c390"
SRCBRANCH = "develop-v2021.10-stm32mp"




U_BOOT_VERSION = "v2021.10"
U_BOOT_SUBVERSION = "stm32mp"
U_BOOT_RELEASE = "r2"

PV = "${U_BOOT_VERSION}-${U_BOOT_SUBVERSION}-${U_BOOT_RELEASE}"

ARCHIVER_ST_BRANCH = "develop-${U_BOOT_VERSION}-${U_BOOT_SUBVERSION}"
ARCHIVER_ST_REVISION = "${PV}"
ARCHIVER_COMMUNITY_BRANCH = "develop-v2021.10-stm32mp"
ARCHIVER_COMMUNITY_REVISION = "${U_BOOT_VERSION}"

S = "${WORKDIR}/git"

# ---------------------------------
# Configure devupstream class usage
# ---------------------------------
BBCLASSEXTEND = "devupstream:target"

SRC_URI:class-devupstream = "git://github.com/myir-private/myir-st-uboot.git;protocol=https;branch=${ARCHIVER_ST_BRANCH}"
SRCREV:class-devupstream = "742d0c3ea3a65a3f8edb26e8906a5133d503c390"

# ---------------------------------
# Configure default preference to manage dynamic selection between tarball and github
# ---------------------------------
STM32MP_SOURCE_SELECTION ?= "tarball"

DEFAULT_PREFERENCE = "${@bb.utils.contains('STM32MP_SOURCE_SELECTION', 'github', '-1', '1', d)}"
