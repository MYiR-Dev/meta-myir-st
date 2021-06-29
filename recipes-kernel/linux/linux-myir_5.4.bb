SUMMARY = "Linux STM32MP Kernel"
SECTION = "kernel"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=bbea815ee2795b2f4230826c0c6b8814"

include linux-myir.inc

LINUX_VERSION = "5.4"
LINUX_SUBVERSION = "31"

S = "${WORKDIR}/git"
#S = "${WORKDIR}/linux-${LINUX_VERSION}.${LINUX_SUBVERSION}"

# ---------------------------------
# Configure devupstream class usage
# ---------------------------------
BBCLASSEXTEND = "devupstream:target"

SRC_URI += " \
      git://github.com/MYiR-Dev/myir-st-linux.git;protocol=https;branch=develop"
SRCREV= "da97d4715bf07759e56c2e57e978f857cf0dbb8c"

#PV = "${LINUX_VERSION}+${LINUX_SUBVERSION}+${SRCPV}"


PV = "${LINUX_VERSION}.${LINUX_SUBVERSION}"

#S = "${WORKDIR}/linux-${LINUX_VERSION}.${LINUX_SUBVERSION}"

# ---------------------------------
# Configure default preference to manage dynamic selection between tarball and github
# ---------------------------------
STM32MP_SOURCE_SELECTION ?= "tarball"

#DEFAULT_PREFERENCE = "${@bb.utils.contains('STM32MP_SOURCE_SELECTION', 'github', '-1', '1', d)}"

# ---------------------------------
# Configure archiver use
# ---------------------------------
include ${@oe.utils.ifelse(d.getVar('ST_ARCHIVER_ENABLE') == '1', 'linux-myir-archiver.inc','')}

# -------------------------------------------------------------
# Defconfig
#
KERNEL_DEFCONFIG        = "myc-ya157c_defconfig"
#KERNEL_CONFIG_FRAGMENTS = "${@bb.utils.contains('KERNEL_DEFCONFIG', 'myc-ya157c_defconfig', '${S}/arch/arm/configs/fragment-01-multiv7_cleanup.config', '', d)}"
KERNEL_CONFIG_FRAGMENTS += "${@bb.utils.contains('KERNEL_DEFCONFIG', 'myc-ya157c_defconfig', '${S}/arch/arm/configs/fragment-02-multiv7_addons.config', '', d)}"
KERNEL_CONFIG_FRAGMENTS += "${@bb.utils.contains('KERNEL_DEFCONFIG', 'myc-ya157c_defconfig', '${WORKDIR}/fragments/5.4/fragment-01-kernel.config', '', d)}"

SRC_URI += "file://${LINUX_VERSION}/fragment-01-kernel.config;subdir=fragments"



# -------------------------------------------------------------
# Kernel Args
#
KERNEL_EXTRA_ARGS += "LOADADDR=${ST_KERNEL_LOADADDR}"
