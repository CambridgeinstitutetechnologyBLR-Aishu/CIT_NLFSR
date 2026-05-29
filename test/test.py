import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_nlfsr(dut):
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    dut.ena.value = 1

    # Load Seed 0xAA
    dut.ui_in.value = 0xAA
    dut.uio_in.value = 0x01 # Load mode
    await RisingEdge(dut.clk)
    
    # Run NLFSR
    dut.uio_in.value = 0x02 # Run mode
    await RisingEdge(dut.clk)
    
    # Verify first transition manually or via model
    # Seed 0xAA (10101010) -> shift -> {0101010, feedback}
    # feedback = bit7(1)^bit5(1)^bit4(0)^(bit1(1)&bit0(0)) = 0
    # Expected: 01010100 (0x54)
    assert dut.uo_out.value == 0x54
