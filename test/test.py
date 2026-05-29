import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_nlfsr(dut):
    dut._log.info("Starting NLFSR PQC Test")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Load a seed (0xAA)
    dut.ui_in.value = 0xAA
    dut.uio_in.value = 0x01 # Load enabled
    await RisingEdge(dut.clk)
    
    # Switch to Run mode
    dut.uio_in.value = 0x02 # Enable high
    await RisingEdge(dut.clk)
    
    # If the state changed, the test is alive
    assert dut.uo_out.value != 0xAA
    dut._log.info("NLFSR is shifting!")
