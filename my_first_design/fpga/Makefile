# ============================================================
# OpenXC7 FPGA Flow
# Default board: Digilent Nexys A7-100T
#
# Flow:
#   RTL -> Yosys -> nextpnr-xilinx -> fpga-as -> FPGA
# ============================================================

# ------------------------------------------------------------
# Project configuration
# ------------------------------------------------------------

TOP       ?= top
SOURCES   ?= src/top.sv \
             src/debouncer.sv \
             src/time_multiplexer.sv \
             ../mini_calculator/src/mini_calculator.sv \
             ../M1_Controller/src/controller.sv \
             ../M2_Adder/src/adder.sv \
             ../M3_BCD/src/bcd_converter.sv \
             ../M4_7segment/src/seven_segment.sv
XDC       ?= src/constraints_nexys4ddr.xdc

# FPGA configuration
PART      ?= xc7a100tcsg324-1
FAMILY    ?= artix7
BOARD     ?= nexys_a7_100

# Existing ChipDB
CHIPDB    ?= /opt/openxc7/chipdb/xc7a100tcsg324.bin

# Build directory
BUILD_DIR ?= build
SYNTH_DIR ?= $(BUILD_DIR)/synth
PNR_DIR ?= $(BUILD_DIR)/pnr
BITSTREAM_DIR ?= $(BUILD_DIR)/bitstream

# ------------------------------------------------------------
# Output files
# ------------------------------------------------------------

JSON = $(SYNTH_DIR)/$(TOP).json
FASM = $(PNR_DIR)/$(TOP).fasm
BIT  = $(BITSTREAM_DIR)/$(TOP).bit

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
	mkdir -p $(SYNTH_DIR)
	mkdir -p $(PNR_DIR)
	mkdir -p $(BITSTREAM_DIR)

# ------------------------------------------------------------
# Synthesis: RTL -> JSON
# ------------------------------------------------------------

synth: $(JSON)

$(JSON): $(SOURCES) | $(BUILD_DIR)
	$(YOSYS) -p "\
		read_verilog -sv $(SOURCES); \
		show -format png -prefix $(SYNTH_DIR)/diagram_before_synth $(TOP); \
		synth_xilinx -flatten -abc9 -arch xc7 -top $(TOP); \
		tee -o $(SYNTH_DIR)/stat.rpt stat; \
		show -format png -prefix $(SYNTH_DIR)/diagram_after_synth $(TOP); \
		write_verilog -noattr -noexpr $(SYNTH_DIR)/$(TOP).nl.v; \
		write_json $@"
	rm -f $(SYNTH_DIR)/diagram_before_synth.dot
	rm -f $(SYNTH_DIR)/diagram_after_synth.dot

# ------------------------------------------------------------
# Place & Route: JSON -> FASM
# ------------------------------------------------------------

pnr: $(FASM)

$(FASM): $(JSON) $(XDC) $(CHIPDB)
	$(NEXTPNR) \
		--chipdb $(CHIPDB) \
		--xdc $(XDC) \
		--report $(PNR_DIR)/pnr.json \
		--json $(JSON) \
		--fasm $@
	python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); json.dump(d,open(p,"w"),indent=2)' $(PNR_DIR)/pnr.json

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
