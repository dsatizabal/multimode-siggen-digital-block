`default_nettype none
`timescale 1ns/1ns

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

module tb_gl (
    // testbench is controlled by test/test_*.py files
    input wire VGND_tb,
    input wire VPWR_tb,
    input wire clk_tb,
    input wire rst_tb,
    input wire enable_tb,
    input wire operation_tb,
    input wire [15:0] data_in_tb,
    output reg [15:0] data_out_tb,
    output wire full_tb,
    output wire empty_tb
);

    // instantiate the DUT
    stack_gl stack_gl(
        .VGND (VGND_tb),
        .VPWR (VPWR_tb),
        .clk (clk_tb),
        .rst (rst_tb),
        .enable (enable_tb),
        .operation (operation_tb),
        .data_in (data_in_tb),
        .data_out (data_out_tb),
        .full (full_tb),
        .empty (empty_tb)
    );

endmodule
