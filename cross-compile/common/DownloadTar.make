
PREFIX              := ${PREFIX}
ROOT_BUILD_DIR      := ${ROOT_BUILD_DIR}
FIRMWARE_NAME       := ${FIRMWARE_NAME}
FIRMWARE_VERSION    := ${VER_SIGROK_FIRMWARE_FX2LAFW}
DOWNLOAD_URL        := $(DOWNLOAD_URL)

DIR_NAME            := $(FIRMWARE_NAME)-bin-$(FIRMWARE_VERSION)
TAR_FILE            := $(DIR_NAME).tar.gz
SIGROK_TAR_URL      := $(DOWNLOAD_URL)/$(FIRMWARE_NAME)/$(TAR_FILE)
TIMESTAMP_FILE      := tar.timestamp  
WGET                := wget -c -N --quiet


all: $(TIMESTAMP_FILE)

$(TIMESTAMP_FILE) : $(TAR_FILE)
	tar xfz $(TAR_FILE) ;
	cp $(DIR_NAME)/*.fw $(PREFIX)/share/sigrok-firmware/
	@touch --reference=$(TAR_FILE) $(TIMESTAMP_FILE)

$(TAR_FILE) : download

download: 
	@if [ -t 1 ] ; then echo -e -n "\033[92m" ; fi
	@echo "Component $(FIRMWARE_NAME)"
	@if [ -t 1 ] ; then echo -e -n "\033[0m" ;fi
	$(WGET) $(SIGROK_TAR_URL)
	
.PHONY : all download