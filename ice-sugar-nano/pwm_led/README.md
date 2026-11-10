# PWM LED — iCESugar Nano

Complete `src/pwm_led.sv` to control the onboard LED brightness using pulse-width modulation (PWM). Make the brightness repeatedly increase and decrease to produce a breathing effect.

## Requirements

- Keep the provided module name and ports: `clk` (input) and `led` (output).
- The FPGA has a **12 MHz** input clock. Update all sequential logic on its rising edge and initialize the internal registers to known values.
- Generate a **1 kHz PWM signal** on `led`. Its duty cycle is the fraction of each PWM period for which the output is high.
- Start at **0% duty cycle**. Increase it by **2 percentage points every 30 PWM periods** until it reaches **100%**, then decrease it at the same rate back to **0%**. Repeat continuously, reversing direction at each endpoint without an extra pause.
- Apply duty cycle changes only at PWM period boundaries. One complete increase/decrease cycle must take **3 seconds**.

## Build and check

Use the supplied `Makefile` and pin constraints without changes. From this directory, run the following command in the course development environment:

```bash
make
```

The generated bitstream is `build/bitstream/pwm_led.bit`. After programming the board, verify that the LED repeatedly fades between minimum and maximum brightness, completing one breathing cycle every 3 seconds. Programming the board is a separate step from `make`.
