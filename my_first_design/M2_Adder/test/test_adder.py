"""
Modern cocotb 2.0 testbench for the Controller module.
Uses async/await syntax and modern pythonic patterns.
"""

import os
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly, Timer
from cocotb.types import LogicArray

from cocotb_tools.runner import get_runner
import random

os.environ['COCOTB_ANSI_OUTPUT'] = '1'

class AdderTester:
    """Helper class for adder testing."""

    def __init__(self, dut):
        self.dut = dut
        self.clk = dut.clk
        self.rst_n = dut.rst_n
        self.operand = dut.operand
        self.save_A = dut.save_A
        self.save_B = dut.save_B
        self.result = dut.result

    async def reset(self):
        self.operand.value = 0
        self.save_A.value = 0
        self.save_B.value = 0
        self.rst_n.value = 0
        await RisingEdge(self.clk)
        await ReadOnly()
        assert self.result.value == 0
        await FallingEdge(self.clk)
        self.rst_n.value = 1
        await RisingEdge(self.clk)
        await ReadOnly()

    async def set_operand(self, value: int, save_A: bool, save_B: bool):
        """Set operand input value."""
        await FallingEdge(self.clk)     
        self.operand.value = value
        self.save_A.value = save_A
        self.save_B.value = save_B


@cocotb.test()
async def test_basic_operation(dut):
    """Test: Check the basic functionality"""
    tester = AdderTester(dut)

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await tester.reset()

    await tester.set_operand(5, save_A=1, save_B=0)
    await RisingEdge(tester.clk)

    await tester.set_operand(3, save_A=0, save_B=1)  
    await RisingEdge(tester.clk)

    await tester.set_operand(0, save_A=0, save_B=0)  
    await ReadOnly()
    assert tester.result.value == 8, f"Expected result 8, got {tester.result.value}"

    dut._log.info("✓ Basic test passed")


@cocotb.test()
async def test_random(dut):
    """Test: Test 10 random additions"""
    tester = AdderTester(dut)

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await tester.reset()

    for i in range(10):
        a = random.randint(0, 15)
        b = random.randint(0, 15)
        expected_sum = a + b

        dut._log.info(f"Test {i}: Adding {a} and {b}, expecting {expected_sum}")

        await tester.set_operand(a, save_A=1, save_B=0)
        await RisingEdge(tester.clk)

        await tester.set_operand(b, save_A=0, save_B=1)  
        await RisingEdge(tester.clk)

        await tester.set_operand(0, save_A=0, save_B=0)  
        await ReadOnly()
        assert tester.result.value == expected_sum, f"Test {i}: Expected {expected_sum}, got {tester.result.value}"

    await RisingEdge(tester.clk)
    dut._log.info("✓ Random test passed")

@cocotb.test()
async def test_reset(dut):
    tester = AdderTester(dut)
    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())
    await tester.reset()

    for save_a, save_b in ((1, 0), (0, 1), (1, 1)):
        await tester.set_operand(5, save_A=1, save_B=0)
        await RisingEdge(dut.clk)
        await tester.set_operand(3, save_A=0, save_B=1)
        await RisingEdge(dut.clk)
        await tester.set_operand(15, save_A=save_a, save_B=save_b)
        dut.rst_n.value = 0
        await Timer(1, unit="us")
        await ReadOnly()
        assert dut.result.value == 8

        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.result.value == 0
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.result.value == 0

        await FallingEdge(dut.clk)
        dut.save_A.value = 0
        dut.save_B.value = 0
        dut.rst_n.value = 1
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.result.value == 0

        await tester.set_operand(7, save_A=1, save_B=0)
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.result.value == 7
        await tester.set_operand(4, save_A=0, save_B=1)
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert dut.result.value == 11


@cocotb.test()
async def test_all(dut):
    """Test: Test 10 random additions"""
    tester = AdderTester(dut)

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    await tester.reset()

    # TODO: Run full test

    dut._log.info("✓ Full test passed")


def test_adder_runner():
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [proj_path / "src" / "adder.sv"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="adder",
        always=True,
        waves=True,
        timescale=("1ns", "1ps"),
    )

    runner.test(hdl_toplevel="adder", test_module="test_adder", waves=True)

if __name__ == "__main__":
    test_adder_runner()
