import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def normal_push_operation(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.VGND_tb.value = 0
    dut.VPWR_tb.value = 1

    dut.enable_tb.value = 1
    dut.operation_tb.value = 0 # Pop

    dut.rst_tb.value = 1
    await ClockCycles(dut.clk_tb, 2)
    dut.rst_tb.value = 0

    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");
    assert dut.empty_tb == 1, f"Expected EMPTY";

    dut.operation_tb.value = 1 # Push
    dut.data_in_tb.value = 43690 # AAAAh
    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");
    dut.enable_tb.value = 0
    assert dut.empty_tb == 0, f"Expected NOT EMPTY";

@cocotb.test()
async def normal_pop_operation(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.VGND_tb.value = 0
    dut.VPWR_tb.value = 1

    dut.enable_tb.value = 1
    dut.operation_tb.value = 0 # Pop

    dut.rst_tb.value = 1
    await ClockCycles(dut.clk_tb, 2)
    dut.rst_tb.value = 0

    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");
    assert dut.empty_tb == 1, f"Expected EMPTY";

    dut.operation_tb.value = 1 # Push
    dut.data_in_tb.value = 43690 # AAAAh
    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");
    assert dut.empty_tb == 0, f"Expected NOT EMPTY";

    dut.operation_tb.value = 0 # Pop
    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");
    assert dut.empty_tb == 1, f"Expected EMPTY AGAIN";
    assert dut.data_out_tb == 43690, f"Expected popped address to be 43690, got {dut.data_out_tb}";

@cocotb.test()
async def stack_gets_full(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.VGND_tb.value = 0
    dut.VPWR_tb.value = 1

    dut.enable_tb.value = 1
    dut.operation_tb.value = 1 # Push

    dut.rst_tb.value = 1
    await ClockCycles(dut.clk_tb, 2)
    dut.rst_tb.value = 0

    assert dut.empty_tb == 1, f"Expected EMPTY after reset";
    assert dut.full_tb == 0, f"Expected NOT FULL after reset";


    dut.data_in_tb.value = 43680 # AAA0h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43681 # AAA1h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43682 # AAA2h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43683 # AAA3h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43684 # AAA4h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43685 # AAA5h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43686 # AAA6h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43687 # AAA7h
    await ClockCycles(dut.clk_tb, 1)

    dut.data_in_tb.value = 43688 # AAA8h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43689 # AAA9h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43690 # AAAAh
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43691 # AAABh
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43692 # AAACh
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43693 # AAADh
    await ClockCycles(dut.clk_tb, 1)

    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");
    assert dut.empty_tb == 0, f"Expected NOT EMPTY";
    assert dut.full_tb == 0, f"Expected not yet FULL";

    dut.data_in_tb.value = 43694 # AAAEh
    await ClockCycles(dut.clk_tb, 1)

    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");

    assert dut.empty_tb == 0, f"Expected NOT EMPTY";
    assert dut.full_tb == 1, f"Expected FULL";

@cocotb.test()
async def stack_pops_same_values(dut):
    clock = Clock(dut.clk_tb, 10, "us")
    cocotb.fork(clock.start())

    dut.VGND_tb.value = 0
    dut.VPWR_tb.value = 1

    dut.enable_tb.value = 1
    dut.operation_tb.value = 1 # Push

    dut.rst_tb.value = 1
    await ClockCycles(dut.clk_tb, 2)
    dut.rst_tb.value = 0

    assert dut.empty_tb == 1, f"Expected EMPTY after reset";
    assert dut.full_tb == 0, f"Expected NOT FULL after reset";

    dut.data_in_tb.value = 43680 # AAA0h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43681 # AAA1h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43682 # AAA2h
    await ClockCycles(dut.clk_tb, 1)
    dut.data_in_tb.value = 43683 # AAA3h
    await ClockCycles(dut.clk_tb, 1)

    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");
    assert dut.empty_tb == 0, f"Expected NOT EMPTY";
    assert dut.full_tb == 0, f"Expected not yet FULL";

    dut.operation_tb.value = 0 # Pop

    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");

    assert dut.empty_tb == 0, f"Expected NOT EMPTY (Pop 4)";
    assert dut.full_tb == 0, f"Expected NOT FULL (Pop 4)";
    assert dut.data_out_tb == 43683, f"Unxpected pop value, expected 43683 got {dut.data_out_tb}";

    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");

    assert dut.empty_tb == 0, f"Expected NOT EMPTY (Pop 3)";
    assert dut.full_tb == 0, f"Expected NOT FULL (Pop 3)";
    assert dut.data_out_tb == 43682, f"Unxpected pop value, expected 43682 got {dut.data_out_tb}";

    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");

    assert dut.empty_tb == 0, f"Expected NOT EMPTY (Pop 2)";
    assert dut.full_tb == 0, f"Expected NOT FULL (Pop 2)";
    assert dut.data_out_tb == 43681, f"Unxpected pop value, expected 43681 got {dut.data_out_tb}";

    await ClockCycles(dut.clk_tb, 1)
    # Required to have the propper results (propagation?), otherwise we'd require an additional clk cycle
    await Timer(10, units="ns");

    assert dut.empty_tb == 1, f"Expected EMPTY (Pop 1)";
    assert dut.full_tb == 0, f"Expected NOT FULL (Pop 1)";
    assert dut.data_out_tb == 43680, f"Unxpected pop value, expected 43680 got {dut.data_out_tb}";
