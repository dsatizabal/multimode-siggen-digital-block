module dump_gl();
	initial begin
		$dumpfile ("mmvfsg_gl.vcd");
		$dumpvars (0, tb_gl);
		#1;
	end
endmodule
