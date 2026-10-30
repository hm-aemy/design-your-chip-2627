# Student Instructions – Mini Calculator

## 1. Goal

Design a small digital system implementing a mini adder controlled by a single button and a finite state machine (FSM).

The system sequentially captures two 4-bit operands, computes their sum, and displays the result on two 7-segment displays.

The control button is considered ideal, meaning it produces a single-clock-cycle pulse synchronized to clk (see below).

## 2. System Specifications

### Mini Calculator Interface

#### Inputs

1. `clk` - System clock
2. `rst_n` - Active-low synchronous reset (High value means no reset)
3. `button` - Ideal button: synchronized, debounced, single-cycle pulse
4. `X[3:0]` - 4-bit input bus

#### Outputs

1. `seg0[6:0]` - Units digit, active-high segment pattern
2. `seg1[6:0]` - Tens digit, active-high segment pattern

### Functional Behavior

The system operates in a sequential manner using a simple FSM and a single control button. The intended usage sequence is:

1. The user sets the input bus `X[3:0]` to operand A
2. The user presses the control button → operand A is stored
3. The user sets the input bus `X[3:0]` to operand B
4. The user presses the control button → operand B is stored
5. The system computes A + B
6. On the next button press, the system display is updated to show the result, and operation returns to step 1

This sequence repeats indefinitely.

### Example Waveform

The waveform below shows how the calculator works:

![Waveform](img/wavedrom.svg)

### FSM Behavior

The system is based on a circular FSM. Each press of `button` performs the action for the current state and advances to the next state.
Two 7-segment displays show the sum in decimal, from 00 to 30.

**Initial State:** Upon reset (`rst_n` = 0), the FSM must initialize to the `GET_A` state.

#### FSM sequence

1. `GET_A`
    - When `button` is pressed: capture the current value of `X[3:0]` into a register, advance to `GET_B`.

2. `GET_B`
    - When `button` is pressed: capture the current value of `X[3:0]` into another register, advance to `SHOW_RESULT`

3. `SHOW_RESULT`
    - When `button` is pressed: change the display value, which is stored in a register, return to `GET_A`.

The FSM always progresses forward; no backward navigation or editing is required.

### Specifications

#### Button Specification

The `button` input of `mini_calculator` is considered IDEAL, meaning:

- Already synchronized to the `clk` domain
- Already debounced (no mechanical bouncing)
- Produces exactly **one** clock cycle pulse per button press
- No additional debouncing or edge detection circuitry is required inside `mini_calculator`

#### Display Specification

**Two** decimal digits are used:

- `seg0[6:0]`: units digit of the sum
- `seg1[6:0]`: tens digit of the sum
- Segment encoding: `seg[6:0] = {a, b, c, d, e, f, g}`
- The calculator outputs are active-high: a value of 1 lights a segment.

#### Reset Specification

- `rst_n` is active-low and synchronous
- On a rising clock edge with `rst_n` = 0: the calculator initializes to `GET_A` with the operand and display registers cleared
- When `rst_n` = 1: normal operation; the displays show `00` after reset until a result is displayed

### Architecture

The chip architecture is shown in the following.

![Architecture](img/architecture.drawio.svg)

The main data path consists of the following modules:

- `adder`: stores the operands and computes the result
- `bcd_converter`: convert the result to two BCD values
- `seven_segment`: convert BCD value to seven segment (and stores the last one)
- `controller`: controls the operation based on the button pushes

## 3. Module Development and Simulation

### 3.1 Module Organization

The system is divided into four modules, labeled M1 to M4. Each module implements a specific functional block of the system.

The corresponding directory contains:

1. A SystemVerilog (.sv) template with the module interface already defined.
2. Test files to verify the expected behavior.
3. A Makefile to execute the module simulation.

### 3.2 Implementation

For each module:

1. Navigate to the corresponding module directory (M1, M2, M3, or M4).
2. Open the provided .sv template.
3. Complete the module implementation according to its specifications.
4. Keep the predefined module interface unchanged.
5. Run the provided tests to verify your implementation.

### 3.3 Running the Tests

Once the SystemVerilog implementation is complete, open a terminal in the corresponding module directory and execute:
```
make
```

This command runs the provided simulation and tests for the module.

If the tests fail, review the simulation output, correct your implementation, and run the tests again. Repeat this process for all four modules. Each module should pass its individual tests before proceeding to the complete FPGA implementation.

### 3.4 Complete System Integration

After M1–M4 pass their tests, connect them in `mini_calculator/src/mini_calculator.sv`. Inside the Dev Container, run `make` from `my_first_design/mini_calculator` to verify the complete calculator with ideal button pulses.

The project is organized as follows:

| Directory | Purpose |
|---|---|
| `M1_Controller/` | Controller implementation and tests |
| `M2_Adder/` | Operand storage, addition, and tests |
| `M3_BCD/` | Binary-to-BCD conversion and tests |
| `M4_7segment/` | Digit storage, segment decoding, and tests |
| `mini_calculator/` | Calculator integration and simulation |
| `fpga/` | FPGA implementation Makefile |
| `fpga/src/` | Provided board top, debouncer, display multiplexer, and constraints |

The files in `fpga/src/` are provided for hardware integration; students do not need to design the debouncer or multiplexer. The FPGA top instantiates `mini_calculator` and adapts its button and display interfaces to the board.

## 4. FPGA Implementation

After completing and testing all four modules and the integrated calculator, the next step is to implement the complete system on an FPGA.

The FPGA implementation flow is:
```
SystemVerilog
     |
     v
  Synthesis
   (Yosys)
     |
     v
Place & Route
(nextpnr-xilinx)
     |
     v
Bitstream Generation
   (fpga-as)
     |
     v
FPGA Programming
 (openFPGALoader)
```

The required tools for synthesis, place-and-route, and bitstream generation are already installed inside the Dev Container.

However, FPGA programming must be performed outside the Dev Container, using openFPGALoader installed on your host operating system.
### 4.1 Installing the Required Tools

To program the FPGA, you must install:

1. openFPGALoader: Used to detect and program the FPGA.
2. GNU Make: Used to execute the commands defined in the Makefile.

If you have not installed them yet, follow the installation instructions in [Troubleshooting](../docs/troubleshooting.md).

### 4.2 Using the Makefile

The Makefile in `fpga/` contains the commands required to perform the FPGA implementation flow, starting from the SystemVerilog source files and ending with FPGA programming.

From `my_first_design/fpga`, run all FPGA commands below. To see the available commands, execute:
```
make help
```
The implementation flow must be executed in two different environments:

| Task | Environment |
|---|---|
| SystemVerilog development | Dev Container |
| Module simulation | Dev Container |
| Synthesis | Dev Container |
| Place & Route | Dev Container |
| Bitstream generation | Dev Container |
| FPGA detection (`make detect`) | Host OS |
| FPGA programming (`make program`) | Host OS |

Important: Always execute make detect and make program outside the Dev Container. These commands use openFPGALoader installed directly on your computer.

### 4.3 Selecting Your FPGA Board

The supported boards are the Nexys A7-100T / Nexys 4 DDR and the Arty A7-100T. Both use the configured `xc7a100tcsg324-1` device and the provided 100T ChipDB.

The Makefile defaults to:

- `BOARD=nexys_a7_100`
- `XDC=src/constraints_nexys4ddr.xdc`
- `BUILD_DIR=build`

For the Arty A7-100T, override the board, constraints, and build directory:

```bash
make <target> BOARD=arty_a7_100t XDC=src/constraints_arty.xdc BUILD_DIR=build/arty
```

Use the same configuration for bitstream generation and programming. Separate build directories keep the two boards' bitstreams apart. `BOARD` selects the openFPGALoader profile; `XDC` selects the pin assignments. Changing `BOARD` alone does not change the FPGA device or constraints.

### 4.4 Generating the Bitstream

**Inside the Dev Container**, navigate to `my_first_design/fpga`.

Execute the bitstream generation target using your assigned board configuration.

**Arty A7-100T:**

```bash
make bitstream BOARD=arty_a7_100t XDC=src/constraints_arty.xdc BUILD_DIR=build/arty
```

**Nexys A7-100T:**

```bash
make bitstream
```

The Makefile executes the required implementation steps using the tools installed in the Dev Container.

After successful execution, the bitstream is generated as `build/top.bit` for the Nexys or `build/arty/top.bit` for the Arty.

This file contains the configuration data required to program your FPGA.

### 4.5 Detecting the FPGA

**Exit the Dev Container or open a separate terminal on your host operating system.**

Connect the FPGA development board to your computer using its programming USB port.

Navigate to `my_first_design/fpga` on the host.

Run:

**Arty A7-100T:**

```bash
make detect BOARD=arty_a7_100t XDC=src/constraints_arty.xdc BUILD_DIR=build/arty
```

**Nexys A7-100T:**

```bash
make detect
```

If the FPGA is correctly connected and accessible, openFPGALoader should report information about the detected JTAG device.

If detection fails:

1. Verify that the FPGA is powered on.
2. Check the USB cable and programming port.
3. Verify that openFPGALoader is installed.
4. On Linux, check the USB permissions.
5. On Windows, check the USB driver configuration.

### 4.6 Programming the FPGA

Once the bitstream has been generated and the FPGA has been detected, you can program the board.

**This step must be executed outside the Dev Container.**

From `my_first_design/fpga` on the host, execute:

**Arty A7-100T:**

```bash
make program BOARD=arty_a7_100t XDC=src/constraints_arty.xdc BUILD_DIR=build/arty
```

**Nexys A7-100T:**

```bash
make program
```

The Makefile will invoke openFPGALoader to load the generated bitstream into the FPGA.

The programming process does not require Yosys, nextpnr-xilinx, or the FPGA chip database on your host computer.

**Note:** The default programming procedure loads the bitstream into the FPGA's volatile configuration memory. The configuration will be lost when the board is powered off.

### 4.7 Testing the Design on Hardware

The board controls are assigned as follows:

| Signal | Nexys A7-100T / Nexys 4 DDR | Arty A7-100T |
|---|---|---|
| `clk` | Onboard 100 MHz clock | Onboard 100 MHz clock |
| `rst_n` | CPU RESET | RESET |
| `button` | BTNC | BTN0 |
| `X[3:0]` | SW3–SW0 | SW3–SW0 |
| Display | Two rightmost onboard digits | External display connected to Pmod JA and JD |

For the Arty, connect the external display interface according to this table. Pin numbers refer to the physical Pmod connector pins:

| Signal | Pmod pin |
|---|---|
| `seg[6]` (A) | JA1 |
| `seg[5]` (B) | JA2 |
| `seg[4]` (C) | JA3 |
| `seg[3]` (D) | JA4 |
| `seg[2]` (E) | JA7 |
| `seg[1]` (F) | JA8 |
| `seg[0]` (G) | JA9 |
| `dp` | JA10 |
| `an[0]` (units) | JD1 |
| `an[1]` (tens) | JD2 |
| `an[2]`–`an[7]` (unused) | JD3, JD4, JD7, JD8, JD9, JD10 |

The external hardware must accept 3.3 V logic, active-low segment signals, and active-low digit enables, with suitable current limiting and digit drivers. Connect its ground to the board ground.

After programming, verify that the mini calculator behaves as expected.

1. Reset the system and release reset; the displays should show `00`.
2. Set operand A using the FPGA input switches.
3. Press the control button to store operand A.
4. Set operand B using the FPGA input switches.
5. Press the control button to store operand B.
6. Press the control button again to update the displays.
7. Verify that the displays show the expected decimal sum, from `00` to `30`.
8. Repeat the procedure with different operands.

Release the control button between presses.

Compare the observed hardware behavior with the expected simulation results.

