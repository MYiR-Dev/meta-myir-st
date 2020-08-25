DESCRIPTION = "myir-systemd"
LICENSE = "MIT"
PV = "1"
PR = "r0"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \ 
	    file://system.conf \
		  "
S_G = "${WORKDIR}"

do_install () {
	      install -d ${D}/etc/systemd/
		  cp -r ${S_G}/system.conf ${D}/etc/systemd/
}
FILES_${PN} = "/etc/systemd/ \
				"

TARGET_CC_ARCH += "${LDFLAGS}"
INSANE_SKIP_${PN}-dev = "ldflags"
INSANE_SKIP_${PN} = "${ERROR_QA} ${WARN_QA}"  
