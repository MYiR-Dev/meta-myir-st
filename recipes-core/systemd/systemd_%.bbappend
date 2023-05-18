FILESEXTRAPATHS:append := ":${THISDIR}/${PN}"

SRC_URI:append = " file://0001-FEAT-add-ntp-service.patch \
									 file://touchscreen.rules"