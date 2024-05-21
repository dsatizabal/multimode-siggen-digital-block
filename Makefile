# cocotb setup
# MODULE = test.test_stack
# export MODULE
TOPLEVEL = mmvfsg
VERILOG_SOURCES = mmvfsg.v

include $(shell cocotb-config --makefiles)/Makefile.sim

synth:
	yosys -p "read_verilog mmvfsg.v; proc; opt; show -colors 2 -width -signed mmvfsg"

tests:
	rm -rf sim_build/
	mkdir sim_build/
	iverilog -o sim_build/sim.vvp -s tb -s dump -g2012 dump_mmvfsg.v mmvfsg.v tb.v
	PYTHONOPTIMIZE=${NOASSERT} MODULE=test.test_mmvfsg vvp -M $$(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus sim_build/sim.vvp
	! grep failure results.xml

tests_gl:
	rm -rf sim_build/
	mkdir sim_build/
	iverilog -o sim_build/sim.vvp -s tb_gl -s dump_gl -g2012 mmvfsg_gl.v dump_mmvfsg_gl.v tb_gl.v -I $(PDK_ROOT)/sky130A
	PYTHONOPTIMIZE=${NOASSERT} MODULE=test.test_mmvfsg_gl vvp -M $$(cocotb-config --prefix)/cocotb/libs -m libcocotbvpi_icarus sim_build/sim.vvp
	! grep failure results.xml

gtkwave:
	gtkwave mmvfsg.vcd mmvfsg.gtkw

formal:
	sby -f mmvfsg.sby
