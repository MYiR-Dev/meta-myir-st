SUMMARY = "OPTEE TA development kit for myir"
LICENSE = "BSD-2-Clause & BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c1f21c4f72f372ef38a5a4aee55ec173"

SRC_URI = "git://github.com/MYiR-Dev/myir-st-optee_os.git;protocol=https;branch=${SRCBRANCH}"
SRCREV = "f44b6e4c9874d3c13a9155bc4393a48614dd6778"
SRCBRANCH = "develop-yf13x-v3.16"


OPTEE_VERSION = "3.16.0"
OPTEE_SUBVERSION = "stm32mp"
OPTEE_RELEASE = "r2"

PV = "${OPTEE_VERSION}-${OPTEE_SUBVERSION}-${OPTEE_RELEASE}"

ARCHIVER_ST_BRANCH = "develop-${OPTEE_VERSION}-${OPTEE_SUBVERSION}"
ARCHIVER_ST_REVISION = "${PV}"
ARCHIVER_COMMUNITY_BRANCH = "develop-3.16.0-stm32mp"
ARCHIVER_COMMUNITY_REVISION = "${OPTEE_VERSION}"

S = "${WORKDIR}/git"

COMPATIBLE_MACHINE = "(stm32mpcommon)"

OPTEEMACHINE ?= "stm32mp1"
OPTEEMACHINE:stm32mp1common = "stm32mp1"

OPTEEOUTPUTMACHINE ?= "stm32mp1"
OPTEEOUTPUTMACHINE:stm32mp1common = "stm32mp1"

# The package is empty but must be generated to avoid apt-get installation issue
ALLOW_EMPTY:${PN} = "1"

require optee-os-myir-common.inc

# ---------------------------------
# Configure archiver use
# ---------------------------------
include ${@oe.utils.ifelse(d.getVar('ST_ARCHIVER_ENABLE') == '1', 'optee-os-myir-archiver.inc','')}

# ---------------------------------
# Configure devupstream class usage
# ---------------------------------
BBCLASSEXTEND = "devupstream:target"

SRC_URI:class-devupstream = "git://github.com/MYiR-Dev/myir-st-optee_os.git;protocol=https;branch=${SRCBRANCH}"
SRCREV:class-devupstream = "f44b6e4c9874d3c13a9155bc4393a48614dd6778"

# ---------------------------------
# Configure default preference to manage dynamic selection between tarball and github
# ---------------------------------
STM32MP_SOURCE_SELECTION ?= "tarball"

DEFAULT_PREFERENCE = "${@bb.utils.contains('STM32MP_SOURCE_SELECTION', 'github', '-1', '1', d)}"
