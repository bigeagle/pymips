#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Program counter
"""


from myhdl import Signal, delay, always_comb, always, Simulation, \
    intbv, bin, instance, instances, now, toVHDL, traceSignals, toVerilog

from clock_driver import clock_driver

from alu import ALU


def program_counter(clk, input, output, stall=Signal(intbv(0)[1:])):
    """

    clk : clock signal
    input: the input count
    output: address output
    """

    @always(clk.negedge)
    def update():
        if not stall:
            output.next = input

    return update


def testbench():

    clk = Signal(intbv(0)[1:])
    i = Signal(intbv(0, min=0, max=32))
    o = Signal(intbv(0, min=0, max=32))

    clkdriver_inst = clock_driver(clk)
    pc_inst = program_counter(clk, i, o)

    c = Signal(0b0010)
    alu_i = ALU(c, o, Signal(1), i, Signal(0))

    @instance
    def stimulus():
        while True:
            yield delay(1)
            print "time: %s | Clock: %i | in: %i | out: %i" % (now(), clk, i, o)

    return instances()


def main():
    #tc =  traceSignals(testbench)
    #sim = Simulation(testbench())
    #sim.run(20)
    clk = Signal(intbv(0)[1:])
    stall = Signal(intbv(0)[1:])
    i = Signal(intbv(0, min=0, max=32))
    o = Signal(intbv(0, min=0, max=32))

    pc_inst = toVerilog(program_counter, clk, i, o, stall)

if __name__ == '__main__':
    main()
