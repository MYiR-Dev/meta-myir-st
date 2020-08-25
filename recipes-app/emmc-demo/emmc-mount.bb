# Copyright (C) 2019, MYIR - All Rights Reserved

inherit systemd

DESCRIPTION = "emmc_mount"
LICENSE = "MIT"
PV = "1"
PR = "r0"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"


SRC_URI = " \ 
	    file://emmc_mount.sh \
		file://profile \
	    file://emmc_mount.service \ 
          "
S_G = "${WORKDIR}"


do_install () {
      install -d ${D}/lib/systemd/system/
      install -d ${D}/etc/
      install -d ${D}/usr/bin/
     

      install -m 0644 ${S_G}/profile ${D}/etc/
      install -m 0644 ${S_G}/emmc_mount.service ${D}/lib/systemd/system/
      install -m 0777 ${S_G}/emmc_mount.sh ${D}/usr/bin/
}

FILES_${PN} = "/lib/systemd/system/ \
		 /etc \
	     /usr/bin/ \
             "

#For dev packages only
INSANE_SKIP_${PN}-dev = "ldflags"
INSANE_SKIP_${PN} = "${ERROR_QA} ${WARN_QA}"
SYSTEMD_SERVICE_${PN} = "emmc_mount.service"
SYSTEMD_AUTO_ENABLE_${PN} = "enable"
