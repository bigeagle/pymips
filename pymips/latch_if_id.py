#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Latch between IF and ID stage
"""

import random


from myhdl import Signal, delay, always_comb, always, Simulation, \
    intbv, bin, instance, instances, now, toVHDL


def latch_if_id(clk, rst, instruction_in, ip_in, instruction_out, ip_out, stall=Signal(intbv(0)[1:])):
    """
    Latch to control state between Instruction Fetch and Instruction Decoder

    clk -- trigger
    rst -- reset
    instruction_in  -- 32 bits signal input
    pc_adder_in -- 32 bits signal input
    instruction_out  -- 32 bits signal output for instruction decoder
    pc_adder_out -- 32 bits signal output for pc_add

    stall -- inhibit the count increment
    """

    @always(clk.posedge)
    def latch():
        if rst == 1:
            print "latch_if_id: Reset %d, %d" % (ip_out, ip_in)
            instruction_out.next = 0
            ip_out.next = 0

        else:
            if not stall:
                instruction_out.next = instruction_in
                ip_out.next = ip_in

    return latch


def testBench():

    i_in, pc_in, i_out, pc_out = [Signal(intbv(0)[32:]) for i in range(4)]

    clk, rst, stall = [Signal(intbv(0)[1:]) for i in range(3)]

    latch_inst = toVHDL(latch_if_id, clk, rst, i_in, pc_in, i_out, pc_out, stall)

    @instance
    def stimulus():
        for i in range(10):
            i_in.next, pc_in.next = [Signal(intbv(random.randint(0, 255))[32:]) for i in range(2)]

            if random.random() > 0.10:
                clk.next = 1
            if random.random() > 0.75:
                rst.next = 1
            if random.random() > 0.5:
                stall.next = 1

            yield delay(1)
            print "Inputs: %i %i | clk: %i  rst: %i stall:%i | Output: %i %i" % (i_in, pc_in, clk, rst, stall, i_out, pc_out)
            clk.next = 0
            rst.next = 0
            stall.next = 0
            yield delay(1)

    return instances()


def main():
    sim = Simulation(testBench())
    sim.run()


if __name__ == '__main__':
    main()
