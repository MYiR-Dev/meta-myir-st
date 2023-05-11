
inherit systemd

DESCRIPTION = "qt app"
DEPENDS = "zlib glibc ncurses "
SECTION = "libs"
LICENSE = "MIT"
PV = "3"
PR = "r0"

LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"


SRC_URI = " \ 
	    file://start.sh \
	    file://myir.service \
	    file://fonts \
	    file://files \
	    file://Capture \
	    file://Music \
	    file://Video \
	    file://ecg \
	    file://mxapp2 \
	    file://adl10-e \
	    file://adl10-e_client \
	    file://lib \
          "
S_G = "${WORKDIR}"

do_install () {
      install -d ${D}/lib/systemd/system/
      install -d ${D}/usr/lib/fonts/
      install -d ${D}/usr/share/fonts/ttf/
      install -d ${D}/usr/bin/
      install -d ${D}/usr/lib/
      install -d ${D}/home/
      install -d ${D}/usr/share/myir/
      install -d ${D}/usr/share/myir/Music/
      install -d ${D}/usr/share/myir/Capture/
      install -d ${D}/usr/share/myir/Video/

      cp -r ${S_G}/start.sh ${D}/usr/bin/
      install -m 0644 ${S_G}/myir.service ${D}/lib/systemd/system/
      cp -r ${S_G}/fonts/* ${D}/usr/lib/fonts/
      cp -r ${S_G}/fonts/* ${D}/usr/share/fonts/ttf/
      cp -r ${S_G}/files/* ${D}/usr/bin/
      cp -r ${S_G}/mxapp2 ${D}/home/
      cp -r ${S_G}/adl10-e ${D}/home/
      cp -r ${S_G}/adl10-e_client ${D}/home/
      cp -r ${S_G}/lib/* ${D}/usr/lib/
      cp -r ${S_G}/ecg/* ${D}/usr/share/myir/
      cp -r ${S_G}/Music/* ${D}/usr/share/myir/Music/
      cp -r ${S_G}/Capture/* ${D}/usr/share/myir/Capture/
      cp -r ${S_G}/Video/* ${D}/usr/share/myir/Video/
      
}

FILES:${PN} = "/"
RDEPENDS:${PN} = "qtbase qtdeclarative qtquickcontrols2  qtmultimedia libmodbus"

#For dev packages only
INSANE_SKIP_${PN}-dev = "ldflags"
INSANE_SKIP_${PN} = "${ERROR_QA} ${WARN_QA}"
INSANE_SKIP_${PN} = "file-rdeps"
INSANE_SKIP_${PN} = "installed-vs-shipped"
SYSTEMD_SERVICE:${PN} = "myir.service"
SYSTEMD_AUTO_ENABLE:${PN} = "enable"
