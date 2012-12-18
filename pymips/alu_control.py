#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


"""
ALU CONTROL
"""

import random

from myhdl import Signal, delay, always_comb, always, Simulation, \
    intbv, bin, instance, instances, now, toVHDL, enum

alu_code = enum(
    '_AND',
    '_OR',
    '_NOR',
    '_ADD',
    '_SUB',
    '_SLT',
    encoding='binary'
)

alu_op_code = enum(
    '_NOP',
    '_ADD',
    '_SUB',
    '_LUI',
    '_ORI',
    '_ANDI',
    '_RFORMAT',
    '_BEQ',
    encoding='binary'
)


def alu_control(aluop, funct_field, control_out):

    @always_comb
    def logic():
        if aluop == alu_op_code._NOP:
            control_out.next = alu_code._ADD

        elif aluop == alu_op_code._ADD:  # ADDI
            control_out.next = alu_code._ADD

        elif aluop == alu_op_code._BEQ:  # BRANCH
            control_out.next = alu_code._SUB

        elif aluop == alu_op_code._LUI:  # LUI
            control_out.next = alu_code._ADD

        elif aluop == alu_op_code._ORI:  # ORI
            control_out.next = alu_code._OR

        elif aluop == alu_op_code._ANDI:  # ANDI
            control_out.next = alu_code._AND

        elif aluop == alu_op_code._RFORMAT:

            # ADD
            if bin(funct_field[3:], 4) == '0000':
                control_out.next = alu_code._ADD

            # SUB
            elif bin(funct_field[3:], 4) == '0010':
                control_out.next = alu_code._SUB

            # AND
            elif bin(funct_field[3:], 4) == '0100':
                control_out.next = alu_code._AND

            # OR
            elif bin(funct_field[3:], 4) == '0101':
                control_out.next = alu_code._OR

            # SLT
            elif bin(funct_field[3:], 4) == '1010':
                control_out.next = alu_code._SLT

            else:
                control_out.next = alu_code._AND
        #else:
        #    control_out.next = intbv(0)

    return logic


def testBench_alu_control():

    aluop_i = Signal(intbv(0)[2:])
    funct_field_i = Signal(intbv(0)[6:])
    alu_control_lines = Signal(intbv(0)[4:])

    alu_control_i = toVHDL(alu_control, aluop_i, funct_field_i, alu_control_lines)

    @instance
    def stimulus():
        for i in range(4):
            aluop_i.next = intbv(i)

            for j in range(2 ** 6):

                funct_field_i.next = intbv(j)

                yield delay(10)
                print "aluop: %s | funct field: %s | alu_control_lines: %s" % (bin(aluop_i, 2), bin(funct_field_i, 6), bin(alu_control_lines, 4))

    return instances()


def main():
    #sim = Simulation(testBench_alu_control())
    sim = Simulation(testBench_alu_control())
    sim.run()

if __name__ == '__main__':
    main()
