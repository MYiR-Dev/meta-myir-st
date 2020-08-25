# Copyright (C) 2019, MYIR - All Rights Reserved

inherit systemd

DESCRIPTION = "myd-ya157c"
LICENSE = "MIT"
PV = "1"
PR = "r0"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"


SRC_URI = " \ 
	    file://emmc_mount.sh \
		file://profile \
        file://myt_ya157c_factory \
        file://myd_ya157c_all \
	file://mmc_test.sh \
	file://set_usb.sh \
	file://wifi.sh \
	file://usb_install.sh \
	file://modeset \
          "
S_G = "${WORKDIR}"


do_install () {
      install -d ${D}/etc/
      install -d ${D}/usr/bin/


     

      install -m 0644 ${S_G}/profile ${D}/etc/
      install -m 0777 ${S_G}/*.sh ${D}/usr/bin/
      install -m 0777 ${S_G}/modeset ${D}/usr/bin/
      install -m 0777 ${S_G}/myt_ya157c_factory ${D}/usr/bin/
      install -m 0777 ${S_G}/myd_ya157c_all ${D}/usr/bin/
      
}

FILES_${PN} = " \
		 /etc \
	     /usr/bin/ \
             "

#For dev packages only
INSANE_SKIP_${PN}-dev = "ldflags"
INSANE_SKIP_${PN} = "${ERROR_QA} ${WARN_QA}"
