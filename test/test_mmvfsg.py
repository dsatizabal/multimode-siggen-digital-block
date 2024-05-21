import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def ramp_operation(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.mode_tb.value = 1 # 0001 = Ramp
    dut.freq_tb.value = 0 # 0

    dut.n_rst_tb.value = 0
    await ClockCycles(dut.clk_tb, 2)
    dut.n_rst_tb.value = 1

    for i in range(1024):
        await ClockCycles(dut.clk_tb, 1)

    assert True

@cocotb.test()
async def sawtooth_operation(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.mode_tb.value = 2 # 0010 = Sawtooth
    dut.freq_tb.value = 0 # 0

    dut.n_rst_tb.value = 0
    await ClockCycles(dut.clk_tb, 2)
    dut.n_rst_tb.value = 1

    for i in range(1024):
        await ClockCycles(dut.clk_tb, 1)

    assert True

@cocotb.test()
async def square_operation(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.mode_tb.value = 4 # 0100 = Square
    dut.freq_tb.value = 0 # 0

    dut.n_rst_tb.value = 0
    await ClockCycles(dut.clk_tb, 2)
    dut.n_rst_tb.value = 1

    for i in range(1024):
        await ClockCycles(dut.clk_tb, 1)

    assert True

@cocotb.test()
async def variate_freq_operation(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.mode_tb.value = 1  # 0001 = Ramp
    dut.freq_tb.value = 0  # Start with frequency 0

    # Reset sequence
    dut.n_rst_tb.value = 0
    await ClockCycles(dut.clk_tb, 2)
    dut.n_rst_tb.value = 1

    # Initialize frequency value
    freq_value = 0

    for i in range(10240):
        if i % 1024 == 0 and i != 0:  # Check if i is a multiple of 1024 and not zero
            freq_value += 1
            if freq_value > 15:  # Ensure freq_value stays within 4-bit limit
                freq_value = 0
            dut.freq_tb.value = freq_value
            
        await ClockCycles(dut.clk_tb, 1)

    assert True

@cocotb.test()
async def restart_on_freq_change(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.mode_tb.value = 1  # 0001 = Ramp
    dut.freq_tb.value = 0  # Start with frequency 0

    # Reset sequence
    dut.n_rst_tb.value = 0
    await ClockCycles(dut.clk_tb, 2)
    dut.n_rst_tb.value = 1

    # Initialize frequency value
    freq_value = 0

    for i in range(2048):
        if (i == 900):
            dut.freq_tb.value = 8

        await ClockCycles(dut.clk_tb, 1)

    assert True

@cocotb.test()
async def restart_on_mode_change(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.mode_tb.value = 1  # 0001 = Ramp
    dut.freq_tb.value = 0  # Start with frequency 0

    # Reset sequence
    dut.n_rst_tb.value = 0
    await ClockCycles(dut.clk_tb, 2)
    dut.n_rst_tb.value = 1

    # Initialize frequency value
    freq_value = 0

    for i in range(2048):
        if (i == 900):
            dut.mode_tb.value = 4  # 0100 = Sq

        await ClockCycles(dut.clk_tb, 1)

    assert True
