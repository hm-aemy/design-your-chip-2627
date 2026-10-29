# ============================================================
# OpenXC7 FPGA Flow
# Default board: Digilent Arty A7-100T
#
# Flow:
#   RTL -> Yosys -> nextpnr-xilinx -> fpga-as -> FPGA
# ============================================================

# ------------------------------------------------------------
# Project configuration
# ------------------------------------------------------------

TOP       ?= full_adder
SOURCES   ?= $(TOP).sv
XDC       ?= constraints_arty.xdc

# FPGA configuration
PART      ?= xc7a100tcsg324-1
FAMILY    ?= artix7
BOARD     ?= arty

# Existing ChipDB
CHIPDB    ?= /opt/openxc7/chipdb/xc7a100tcsg324.bin

# Build directory
BUILD_DIR ?= build

# ------------------------------------------------------------
# Output files
# ------------------------------------------------------------

JSON = $(BUILD_DIR)/$(TOP).json
FASM = $(BUILD_DIR)/$(TOP).fasm
BIT  = $(BUILD_DIR)/$(TOP).bit

# ------------------------------------------------------------
# Tools
# ------------------------------------------------------------

YOSYS          ?= yosys
NEXTPNR        ?= nextpnr-xilinx
FPGA_AS        ?= fpga-as
OPENFPGALOADER ?= openFPGALoader

# ------------------------------------------------------------
# Default target
# ------------------------------------------------------------

.DEFAULT_GOAL := all

.PHONY: all synth pnr bitstream program clean detect help

.DELETE_ON_ERROR:

all: bitstream

# ------------------------------------------------------------
# Create build directory
# ------------------------------------------------------------

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# ------------------------------------------------------------
# Synthesis: RTL -> JSON
# ------------------------------------------------------------

synth: $(JSON)

$(JSON): $(SOURCES) | $(BUILD_DIR)
	$(YOSYS) -p "\
		read_verilog -sv $(SOURCES); \
		synth_xilinx -flatten -abc9 -arch xc7 -top $(TOP); \
		write_json $@"

# ------------------------------------------------------------
# Place & Route: JSON -> FASM
# ------------------------------------------------------------

pnr: $(FASM)

$(FASM): $(JSON) $(XDC) $(CHIPDB)
	$(NEXTPNR) \
		--chipdb $(CHIPDB) \
		--xdc $(XDC) \
		--json $(JSON) \
		--fasm $@

# ------------------------------------------------------------
# Bitstream generation: FASM -> BIT
# ------------------------------------------------------------

bitstream: $(BIT)

$(BIT): $(FASM)
	$(FPGA_AS) \
		--prjxray_db_path=$(PRJXRAY_DB_DIR)/$(FAMILY) \
		--part $(PART) \
		$< > $@

# ------------------------------------------------------------
# FPGA programming
# ------------------------------------------------------------

program:
	$(OPENFPGALOADER) \
		--board $(BOARD) \
		--bitstream $(BIT)

# ------------------------------------------------------------
# Detect FPGA
# ------------------------------------------------------------

detect:
	$(OPENFPGALOADER) \
		--board $(BOARD) \
		--detect

# ------------------------------------------------------------
# Clean generated files
# ------------------------------------------------------------

clean:
	rm -rf $(BUILD_DIR)

# ------------------------------------------------------------
# Help
# ------------------------------------------------------------

help:
	@echo "OpenXC7 FPGA Flow"
	@echo ""
	@echo "Targets:"
	@echo "  make synth       - Synthesize RTL with Yosys"
	@echo "  make pnr         - Run placement and routing"
	@echo "  make bitstream   - Generate FPGA bitstream"
	@echo "  make program     - Program the FPGA"
	@echo "  make detect      - Detect connected FPGA"
	@echo "  make clean       - Remove generated files"
	@echo ""
	@echo "Configuration:"
	@echo "  TOP=$(TOP)"
	@echo "  SOURCES=$(SOURCES)"
	@echo "  XDC=$(XDC)"
	@echo "  PART=$(PART)"
	@echo "  BOARD=$(BOARD)"
