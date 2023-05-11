


DESCRIPTION = "qt app"
DEPENDS = "zlib glibc ncurses "
SECTION = "libs"
LICENSE = "MIT"
PV = "3"
PR = "r0"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"


SRC_URI = " \ 
	    file://eeprom.sh \
	    file://eeprom_135_test \
          "
S_G = "${WORKDIR}"

do_install () {

      install -d ${D}/bin/


      
      install -m 0755 ${S_G}/eeprom.sh ${D}/bin/
      install -m 0755 ${S_G}/eeprom_135_test ${D}/bin/

      
}

FILES:${PN} = "/"

#For dev packages only
INSANE_SKIP_${PN}-dev = "ldflags"
INSANE_SKIP_${PN} = "${ERROR_QA} ${WARN_QA}"
INSANE_SKIP_${PN} = "file-rdeps"
INSANE_SKIP_${PN} = "installed-vs-shipped"

