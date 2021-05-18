SUMMARY = "myir example of image based on QT framework."
LICENSE = "Proprietary"

include recipes-myir/images/myir-image.inc

inherit core-image features_check

# let's make sure we have a good image..
#CONFLICT_DISTRO_FEATURES = "x11 wayland"
REQUIRED_DISTRO_FEATURES = "wayland"


IMAGE_LINGUAS = "en-us"

IMAGE_FEATURES += " \
    splash              \
    package-management  \
    ssh-server-dropbear \
    hwcodecs            \
    tools-profile       \
    eclipse-debug       \
    "

# Define ROOTFS_MAXSIZE to 3GB
IMAGE_ROOTFS_MAXSIZE = "3145728"

IMAGE_INSTALL_append = " \
			ffmpeg \
			qt-demo \
			myd-ya157c \
			"

# Set ST_EXAMPLE_IMAGE property to '1' to allow specific use in image creation process
ST_EXAMPLE_IMAGE = "1"


#
# INSTALL addons
#
CORE_IMAGE_EXTRA_INSTALL += " \
    packagegroup-framework-core-base    \
    packagegroup-framework-tools-base   \
    \
    packagegroup-framework-core         \
    packagegroup-framework-tools       \
    \
    packagegroup-framework-core-extra   \
    packagegroup-framework-tools-extra  \
    \
    packagegroup-framework-sample-qt    \
    packagegroup-framework-sample-qt-extra   \
    packagegroup-st-demo \
    "
