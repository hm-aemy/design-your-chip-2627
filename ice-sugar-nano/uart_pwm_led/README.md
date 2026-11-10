# UART PWM LED — iCESugar Nano

Complete `src/uart_pwm_led.sv` to control the onboard LED brightness using bytes received over UART. Each valid byte sets the duty cycle of a PWM output; the brightness must remain constant until another valid byte arrives.

## Requirements

- Keep the module name `uart_pwm_led` and ports: `clk` and `rx` (inputs), `led` (output).
- Use the **12 MHz** clock and update all sequential logic on its rising edge. Initialize internal registers to known values.
- Receive UART at **115200 baud, 8N1**: one low start bit, eight data bits sent least significant bit first, no parity, and one high stop bit. The idle line is high.
- Synchronize `rx` to the clock and sample bits near their centers. Reject frames with an invalid stop bit.
- Interpret each received byte as an **unsigned binary value from 0 to 255**, not an ASCII number. No separator or newline is required.
- Generate **1 kHz PWM** with a period of **12,000 clock cycles**. For byte value `b`, the output must be high for `floor(b × 12000 / 256)` cycles per period. Thus, `0` turns the output off, `128` gives 50% duty cycle, and `255` gives approximately 99.6%.
- Start at **25% duty cycle** (byte value `64`). Apply each valid command by the start of the next PWM period and retain it until the next valid command.

## Build and check

From this directory, build the bitstream in the course development environment:

```bash
make
```

The output is `build/bitstream/uart_pwm_led.bit`. Programming the board is a separate step from `make`.

After programming, use the supplied `set_brightness.py` script on the computer connected to the board. It requires Python with `pyserial`. Replace `/dev/ttyACM0` with the board's serial port:

```bash
python3 set_brightness.py -p /dev/ttyACM0 -b 0
python3 set_brightness.py -p /dev/ttyACM0 -b 50
python3 set_brightness.py -p /dev/ttyACM0 -b 100
```

The script converts the percentage to a single byte from 0 to 255. Verify that each command changes the brightness and that the selected level remains stable after transmission ends. The `100` command selects the maximum byte value, corresponding to approximately 99.6% duty cycle.
