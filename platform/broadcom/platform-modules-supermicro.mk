SMCI_PLATFORM_MODULE_VERSION = 0.1

export SMCI_PLATFORM_MODULE_VERSION

SMCI_SSE_T8164_PLATFORM_MODULE = platform-modules-sse-t8164_$(SMCI_PLATFORM_MODULE_VERSION)_$(CONFIGURED_ARCH).deb
$(SMCI_SSE_T8164_PLATFORM_MODULE)_SRC_PATH = $(PLATFORM_PATH)/sonic-platform-modules-supermicro
$(SMCI_SSE_T8164_PLATFORM_MODULE)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON)
$(SMCI_SSE_T8164_PLATFORM_MODULE)_PLATFORM = x86_64-supermicro_sse_t8164-r0
SONIC_DPKG_DEBS += $(SMCI_SSE_T8164_PLATFORM_MODULE)

SMCI_SSE_T8196_PLATFORM_MODULE = platform-modules-sse-t8196_$(SMCI_PLATFORM_MODULE_VERSION)_$(CONFIGURED_ARCH).deb
$(SMCI_SSE_T8196_PLATFORM_MODULE)_PLATFORM = x86_64-supermicro_sse_t8196-r0
$(eval $(call add_extra_package,$(SMCI_SSE_T8164_PLATFORM_MODULE),$(SMCI_SSE_T8196_PLATFORM_MODULE)))