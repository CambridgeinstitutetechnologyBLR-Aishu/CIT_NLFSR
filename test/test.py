import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_nlfsr(dut):
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1
    dut.ui_in.value = 0x55
    dut.uio_in.value = 0x01
    await RisingEdge(dut.clk)
    dut.uio_in.value = 0x02
    await RisingEdge(dut.clk)
    assert dut.uo_out.value != 0x55
