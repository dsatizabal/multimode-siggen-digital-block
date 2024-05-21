`default_nettype none
`timescale 1ns/1ns

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

module tb (
    // testbench is controlled by test/test_*.py files
    input wire clk_tb,
    input wire n_rst_tb,
    input wire [3:0] freq_tb,
    input wire [3:0] mode_tb,
    output reg [7:0] r2r_out_tb
);

    // instantiate the DUT
    mmvfsg mmvfsg(
        .clk (clk_tb),
        .n_rst (n_rst_tb),
        .freq (freq_tb),
        .mode (mode_tb),
        .r2r_out (r2r_out_tb)
    );

endmodule
