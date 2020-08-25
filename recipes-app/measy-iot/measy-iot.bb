# Copyright (C) 2019, MYIR - All Rights Reserved


DESCRIPTION = "Measy IOT"
DEPENDS = "zlib glibc ncurses "
SECTION = "libs"
LICENSE = "MIT"
PV = "3"
PR = "r0"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"


SRC_URI = " \ 
	    file://etc \
	    file://lib \
	    file://usr \ 
          "
S_G = "${WORKDIR}"

do_install () {
      install -d ${D}/etc/dbus-1/system.d/
      install -d ${D}/etc/systemd/system/
      install -d ${D}/etc/systemd/network/
      install -d ${D}/lib/
      install -d ${D}/usr/bin/
	  install -d ${D}/usr/lib/
      install -d ${D}/usr/lib/python2.7/
      install -d ${D}/usr/share/measy_iot/
      install -d ${D}/lib/systemd/system/
      

      cp -r ${S_G}/etc/dbus-1/system.d/* ${D}/etc/dbus-1/system.d/
      cp -r ${S_G}/etc/systemd/system/* ${D}/lib/systemd/system/
      cp -r ${S_G}/etc/systemd/network/* ${D}/etc/systemd/network/
      cp -r ${S_G}/lib/* ${D}/lib/
      cp -r ${S_G}/usr/bin/* ${D}/usr/bin/
	  cp -r ${S_G}/usr/lib/* ${D}/usr/lib/
      cp -rfav ${S_G}/usr/lib/python2.7/* ${D}/usr/lib/python2.7/
      cp -r ${S_G}/usr/share/measy_iot/* ${D}/usr/share/measy_iot/
      cp -r ${S_G}/lib/systemd/system/systemd-networkd.service ${D}/lib/systemd/system/
}

FILES_${PN} = "/etc/dbus-1/system.d/ \
	     /etc/systemd/system/ \
         /etc/systemd/network/ \
	     /lib/ \
	     /usr/bin/ \
	     /usr/lib/ \
	     /usr/lib/python2.7/ \
	     /usr/share/measy_iot/ \
         /lib/systemd/system/ \
             "

#For dev packages only
INSANE_SKIP_${PN}-dev = "ldflags"
INSANE_SKIP_${PN} = "${ERROR_QA} ${WARN_QA}"
SYSTEMD_SERVICE_${PN} = "connmand.service"
SYSTEMD_AUTO_ENABLE_${PN} = "enable"
SYSTEMD_SERVICE_${PN} = "measy_iot_start.service"
SYSTEMD_AUTO_ENABLE_${PN} = "enable"

