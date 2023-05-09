require u-boot-myir-common_${PV}.inc
require u-boot-myir.inc

SUMMARY = "Universal Boot Loader for embedded devices for stm32mp"
LICENSE = "GPL-2.0-or-later"

PROVIDES += "u-boot"
RPROVIDES:${PN} += "u-boot"

# ---------------------------------
# Configure archiver use
# ---------------------------------
include ${@oe.utils.ifelse(d.getVar('ST_ARCHIVER_ENABLE') == '1', 'u-boot-myir-archiver.inc','')}
