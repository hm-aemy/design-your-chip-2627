SRC_DIR = src
CONSTRAINTS_DIR = constraints
BUILD_DIR = build
SYNTH_DIR = synth
PNR_DIR = pnr
BITSTREAM_DIR = bitstream

TOP = uart_pwm_led
SOURCES = $(SRC_DIR)/$(TOP).sv
PCF = $(CONSTRAINTS_DIR)/constraints.pcf

# FPGA configuration
PART      ?= cm36

# ------------------------------------------------------------
# Output files
# ------------------------------------------------------------

JSON = $(BUILD_DIR)/$(SYNTH_DIR)/$(TOP).json
ASC = $(BUILD_DIR)/$(PNR_DIR)/$(TOP).asc
BIT  = $(BUILD_DIR)/$(BITSTREAM_DIR)/$(TOP).bit

# ------------------------------------------------------------
# Tools
# ------------------------------------------------------------

YOSYS          ?= yosys
NEXTPNR        ?= nextpnr-ice40
ICEPACK        ?= icepack

# ------------------------------------------------------------
# Default target
# ------------------------------------------------------------

.DEFAULT_GOAL := all
.PHONY: all synth pnr bitstream clean
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
	mkdir -p $(BUILD_DIR)/$(SYNTH_DIR)
	$(YOSYS) -l $(BUILD_DIR)/$(SYNTH_DIR)/synth.log -p "\
		read_verilog -sv $(SOURCES); \
		show -format png -prefix $(BUILD_DIR)/$(SYNTH_DIR)/diagram_before_synth $(TOP); \
		synth_ice40 -top $(TOP); \
		tee -o $(BUILD_DIR)/$(SYNTH_DIR)/stat.rpt stat; \
		show -format png -prefix $(BUILD_DIR)/$(SYNTH_DIR)/diagram_after_synth $(TOP); \
		write_verilog -noattr -noexpr $(BUILD_DIR)/$(SYNTH_DIR)/$(TOP).nl.v; \
		write_json $@"
	rm -f $(BUILD_DIR)/$(SYNTH_DIR)/diagram_before_synth.dot
	rm -f $(BUILD_DIR)/$(SYNTH_DIR)/diagram_after_synth.dot

# ------------------------------------------------------------
# Place & Route: JSON -> ASC
# ------------------------------------------------------------

pnr: $(ASC)

$(ASC): $(JSON) $(PFC)
	mkdir -p $(BUILD_DIR)/$(PNR_DIR)
	$(NEXTPNR) \
		--lp1k \
		--package $(PART) \
		--pcf $(PCF) \
		--report $(BUILD_DIR)/$(PNR_DIR)/pnr.json \
		--placed-svg $(BUILD_DIR)/$(PNR_DIR)/placed.svg \
		--routed-svg $(BUILD_DIR)/$(PNR_DIR)/routed.svg \
		--json $(JSON) \
		--asc $@
	python3 -c 'import json,sys; p=sys.argv[1]; d=json.load(open(p)); json.dump(d,open(p,"w"),indent=2)' $(BUILD_DIR)/$(PNR_DIR)/pnr.json

# ------------------------------------------------------------
# Bitstream generation: ASC -> BIT
# ------------------------------------------------------------

bitstream: $(BIT)

$(BIT): $(ASC)
	mkdir -p $(BUILD_DIR)/$(BITSTREAM_DIR)
	$(ICEPACK) \
		$(ASC) \
		$@

clean: 
	rm -rf $(BUILD_DIR)
