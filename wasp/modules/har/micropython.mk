HAR_MOD_DIR := $(USERMOD_DIR)

# Add all C files to SRC_USERMOD.
SRC_USERMOD += $(HAR_MOD_DIR)/har.c

# We can add our module folder to include paths if needed
# This is not actually needed in this har.
CFLAGS_USERMOD += -I$(HAR_MOD_DIR)
HAR_MOD_DIR := $(USERMOD_DIR)
