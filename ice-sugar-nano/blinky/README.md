# Blinky — iCESugar Nano

Complete `src/blinky.sv` to make the onboard LED blink at **1 Hz**: 0.5 seconds on, followed by 0.5 seconds off, repeating continuously.

## Requirements

- Keep the provided module name and ports: `clk` (input) and `led` (output).
- The FPGA has a **12 MHz** input clock. Update all sequential logic on its rising edge.
- Implement a counter to generate the required timing. 
- Drive `led` with the repeating on/off pattern. Either initial LED state is acceptable.

## Build and check

Use the supplied `Makefile` and pin constraints without changes. From this directory, run the following command in the course development environment:

```bash
make
```

The generated bitstream is `build/bitstream/blinky.bit`. After programming the board, verify that the LED completes one full on/off cycle per second. Programming the board is a separate step from `make`.
