# =========================================================================
# Kernel
# =========================================================================
PREFERRED_PROVIDER_virtual/kernel = "linux-myir"

# =========================================================================
# u-boot
# =========================================================================
PREFERRED_PROVIDER_virtual/bootloader = "u-boot-myir"
PREFERRED_PROVIDER_u-boot = "u-boot-myir"

# =========================================================================
# trusted-firmware-a
# =========================================================================
PREFERRED_PROVIDER_virtual/trusted-firmware-a = "tf-a-myir"
PREFERRED_PROVIDER_virtual/trusted-firmware-a-serialboot = "tf-a-myir-serialboot"
# Define default TF-A config
TF_A_CONFIG_append_pn-tf-a-myir-serialboot = " serialboot "
TF_A_CONFIG_append_pn-tf-a-myir = " ${@bb.utils.contains('BOOTSCHEME_LABELS', 'trusted', 'trusted', '', d)} "
TF_A_CONFIG_append_pn-tf-a-myir = " ${@bb.utils.contains('BOOTSCHEME_LABELS', 'optee', 'optee', '', d)} "

# =========================================================================
# optee-os
# =========================================================================
PREFERRED_PROVIDER_virtual/optee-os = "optee-os-myir"

