import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_nlfsr(dut):
    dut._log.info("Starting NLFSR PQC Simulation")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset sequence
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Load initial seed
    dut.ui_in.value = 0xAA
    dut.uio_in.value = 0x01 # Set Load bit
    await RisingEdge(dut.clk)
    
    # Run NLFSR
    dut.uio_in.value = 0x02 # Set Enable bit
    await RisingEdge(dut.clk)
    
    # Check that output is not the same as input
    assert dut.uo_out.value != 0xAA
    dut._log.info("PQC NLFSR is functional!")
