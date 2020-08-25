FILESEXTRAPATHS_prepend_stm32mpcommon := "${THISDIR}/${PN}:"

# Add calibration file
SRC_URI_append_stm32mpcommon = " file://brcmfmac43430-sdio.txt "
SRC_URI_append_stm32mpcommon = " file://brcmfmac43362-sdio.txt "
SRC_URI_append_stm32mpcommon = " file://brcmfmac43430-sdio.bin "
SRC_URI_append_stm32mpcommon = " file://brcmfmac43430-sdio.clm_blob "
#SRC_URI_append_stm32mpcommon = " git://e.coding.net/lichang70/linux-fw-myir.git;protocol=https;branch=master "
SRCREV_murata = "8d87950bfad28c65926695b7357bd8995b60016a"
SRCREV_FORMAT = "linux-firmware-murata"

do_install_append_stm32mpcommon() {
   # Install calibration file
   install -m 0644 ${WORKDIR}/brcmfmac43430-sdio.txt ${D}${nonarch_base_libdir}/firmware/brcm/
   install -m 0644 ${WORKDIR}/brcmfmac43430-sdio.txt ${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.myir,stm32mp157c-ya157c-v2.txt
   install -m 0644 ${WORKDIR}/brcmfmac43362-sdio.txt ${D}${nonarch_base_libdir}/firmware/brcm/
   install -m 0644 ${WORKDIR}/brcmfmac43362-sdio.txt ${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43362-sdio.myir,stm32mp157c-ya157c-v2.txt

   #take newest murata firmware
   install -m 0644 ${WORKDIR}/brcmfmac43430-sdio.bin ${D}${nonarch_base_libdir}/firmware/brcm/
   install -m 0644 ${WORKDIR}/brcmfmac43430-sdio.clm_blob ${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.clm_blob

}

FILES_${PN}-bcm43430_append_stm32mpcommon = " \
  ${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.txt \
  ${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.myir,stm32mp157c-ya157c-v2.txt \
  ${nonarch_base_libdir}/firmware/brcm/brcmfmac43362-sdio.txt \
  ${nonarch_base_libdir}/firmware/brcm/brcmfmac43362-sdio.myir,stm32mp157c-ya157c-v2.txt \
  ${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.bin \
  ${nonarch_base_libdir}/firmware/brcm/brcmfmac43430-sdio.clm_blob \
"
RDEPENDS_${PN}-bcm43430_remove_stm32mpcommon = " ${PN}-cypress-license "

RRECOMMENDS_${PN}-bcm43430_append_stm32mpcommon += "${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'wifi-suspend', '', d)}"
