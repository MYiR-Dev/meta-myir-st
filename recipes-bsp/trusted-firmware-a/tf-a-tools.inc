FILESEXTRAPATHS:prepend := "${THISDIR}/tf-a-tools:"

#SRC_URI = "git://github.com/myir-private/myir-st-tfa.git;protocol=https;branch=develop-v2.6-stm32mp"
#SRCREV = "4cc966a5372b13517343009b2f8797cb99828ce8"

SRC_URI = "git://github.com/MYiR-Dev/myir-st-arm-trusted-firmware.git;protocol=https;branch=${SRCBRANCH}"
SRCREV = "4cc966a5372b13517343009b2f8797cb99828ce8"
SRCBRANCH = "develop-yf13x-v2.6"

DEPENDS += "dtc-native openssl"

COMPATIBLE_HOST:class-target = "null"

HOSTCC:class-native = "${BUILD_CC}"
HOSTCC:class-nativesdk = "${CC}"

EXTRA_OEMAKE += "HOSTCC='${HOSTCC}' OPENSSL_DIR='${STAGING_EXECPREFIXDIR}'"
EXTRA_OEMAKE += "certtool fiptool"
EXTRA_OEMAKE += "PLAT=${TFA_PLATFORM}"

do_configure[noexec] = "1"

do_compile:prepend:class-native () {
    # This is still needed to have the native fiptool executing properly by
    # setting the RPATH
    sed -e '/^LDLIBS/ s,$, \$\{BUILD_LDFLAGS},' \
        -e '/^INCLUDE_PATHS/ s,$, \$\{BUILD_CFLAGS},' \
        -i ${S}/tools/fiptool/Makefile
    # This is still needed to have the native cert_create executing properly by
    # setting the RPATH
    sed -e '/^LIB_DIR/ s,$, \$\{BUILD_LDFLAGS},' \
        -e '/^INC_DIR/ s,$, \$\{BUILD_CFLAGS},' \
        -i ${S}/tools/cert_create/Makefile
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 \
        ${B}/tools/fiptool/fiptool \
        ${B}/tools/cert_create/cert_create \
        ${D}${bindir}
}

BBCLASSEXTEND += "native nativesdk"
