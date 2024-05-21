module dump();
	initial begin
		$dumpfile ("mmvfsg.vcd");
		$dumpvars (0, tb);
		#1;
	end
endmodule
