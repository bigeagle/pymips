#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


"""
ALU
"""

import random

from myhdl import Signal, delay, always_comb, always, Simulation, \
    intbv, bin, instance, instances, now, toVerilog, traceSignals

from myhdl.conversion import analyze

from alu_control import alu_code


def ALU(control, op1, op2, out_, zero, positive):
    """
    control : 4 bit control/selector vector.
    op1: operator 1. 32bits
    op2: operator 2. 32bits
    out: ALU result. 32bits
    zero: zero detector. ``1`` when out is 0.

    """

    @always_comb
    def logic_alu():
        if control == alu_code.MAND:  # int('0000',2):
            out_.next = op1 & op2

        elif control == alu_code.MOR:  # int('0001',2):
            out_.next = op1 | op2

        elif control == alu_code.MADD:  # int('0010',2):
            out_.next = op1 + op2  # what happend if there is overflow ?

        elif control == alu_code.MSUB:  # int('0110',2):
            out_.next = op1 - op2

        elif control == alu_code.MSLT:  # int('0111',2):
            if op1.val < op2.val:
                out_.next = 1
            else:
                out_.next = 0

        elif control == alu_code.MNOR:  # int('1100', 2):
            out_.next = ~ (op1 | op2)  # TODO check this

    @always_comb
    def zero_detector():
        if out_ == 0:
            zero.next = 1
        else:
            zero.next = 0

    @always_comb
    def positive_detector():
        if out_ >= 0:
            positive.next = 1
        else:
            positive.next = 0

    return logic_alu, zero_detector, positive_detector


### TESTBENCHS

def testBench_alu():

    control_i = Signal(intbv(0)[4:])

    op1_i = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    op2_i = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))

    out_i = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))

    zero_i = Signal(bool(False))

    alu_i = ALU(control_i, op1_i, op2_i, out_i, zero_i)
    #alu_i = toVHDL(ALU, control_i, op1_i, op2_i, out_i, zero_i)
    #alu_i = analyze(alu, control_i, op1_i, op2_i, out_i, zero_i)

    control_func = (('0000', 'AND'), ('0001', 'OR'), ('0010', 'add'), ('0110', 'substract'), ('0111', '<'), ('1100', 'NOR'))

    @instance
    def stimulus():
        for control_val, func in [(int(b, 2), func) for (b, func) in control_func]:
            control_i.next = Signal(intbv(control_val))

            op1_i.next, op2_i.next = [intbv(random.randint(0, 255))[32:] for i in range(2)]

            yield delay(10)
            print "Control: %s | %i %s %i | %i | z=%i" % (bin(control_i, 4), op1_i, func, op2_i, out_i, zero_i)

    return instances()


def main():
    control = Signal(alu_code.MAND)
    op1 = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    op2 = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    out = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    zero = Signal(bool(False))
    positive = Signal(bool(False))
    toVerilog(ALU, control, op1, op2, out, zero, positive)
    #tb = traceSignals(testBench_alu)
    #sim = Simulation(tb)
    #sim.run()

if __name__ == '__main__':
    main()
