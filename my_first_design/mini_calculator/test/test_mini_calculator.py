import os
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, ReadOnly
from cocotb_tools.runner import get_runner


@cocotb.test()
async def test_all_sums(dut):
    segments = (0b1111110, 0b0110000, 0b1101101, 0b1111001, 0b0110011,
                0b1011011, 0b1011111, 0b1110000, 0b1111111, 0b1111011)
    dut.rst_n.value = 0
    dut.button.value = 0
    dut.X.value = 0
    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    previous = None

    for a in range(16):
        for b in range(16):
            for step, operand in enumerate((a, b, 0)):
                await FallingEdge(dut.clk)
                dut.X.value = operand
                dut.button.value = 1
                await RisingEdge(dut.clk)
                await ReadOnly()
                if step == 2:
                    previous = a + b
                if previous is not None:
                    assert int(dut.seg0.value) == segments[previous % 10]
                    assert int(dut.seg1.value) == segments[previous // 10]
                await FallingEdge(dut.clk)
                dut.button.value = 0
                dut.X.value = 15
                await RisingEdge(dut.clk)
                await ReadOnly()
                if previous is not None:
                    assert int(dut.seg0.value) == segments[previous % 10]
                    assert int(dut.seg1.value) == segments[previous // 10]


def test_mini_calculator_runner():
    project = Path(__file__).resolve().parents[2]
    sources = [project / module / "src" / source for module, source in (
        ("M1_Controller", "controller.sv"),
        ("M2_Adder", "adder.sv"),
        ("M3_BCD", "bcd_converter.sv"),
        ("M4_7segment", "seven_segment.sv"),
        ("mini_calculator", "mini_calculator.sv"),
    )]
    runner = get_runner(os.getenv("SIM", "icarus"))
    runner.build(sources=sources, hdl_toplevel="mini_calculator", always=True,
                 waves=True, timescale=("1ns", "1ps"))
    runner.test(hdl_toplevel="mini_calculator", test_module="test_mini_calculator", waves=True)


if __name__ == "__main__":
    test_mini_calculator_runner()
