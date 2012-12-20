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
    '_SLT',
    '_ANDI',
    '_RFORMAT',
    # branches
    '_BEQ',
    '_BNE',
    '_BGEZ',
    '_BGEZAL',
    '_BGTZ',
    '_BLEZ',
    '_BLTZ',
    '_BLTZAL',
    '_J',
    '_JAL',
    '_JALR',
    '_JR',
    encoding='binary'
)


def alu_control(aluop, branch, funct_field, front_sel, control_out):

    @always_comb
    def logic():
        if branch == 1:
            front_sel.next = 1
            control_out.next = alu_code._SUB

        else:
            if aluop == alu_op_code._NOP:
                control_out.next = alu_code._ADD
                front_sel.next = 1

            elif aluop == alu_op_code._ADD:  # ADDI
                control_out.next = alu_code._ADD
                front_sel.next = 1

            elif aluop == alu_op_code._SLT:  # ADDI
                control_out.next = alu_code._SLT
                front_sel.next = 1

            elif aluop == alu_op_code._LUI:  # LUI
                control_out.next = alu_code._ADD
                front_sel.next = 0

            elif aluop == alu_op_code._ORI:  # ORI
                control_out.next = alu_code._OR
                front_sel.next = 0

            elif aluop == alu_op_code._ANDI:  # ANDI
                control_out.next = alu_code._AND
                front_sel.next = 0

            elif aluop == alu_op_code._RFORMAT:

                # ADD
                if funct_field == 0b100000:
                    control_out.next = alu_code._ADD
                    front_sel.next = 1
                # ADDU
                elif funct_field == 0b100001:
                    control_out.next = alu_code._ADD
                    front_sel.next = 1

                # SUB
                elif funct_field == 0b100010:
                    control_out.next = alu_code._SUB
                    front_sel.next = 1

                # SUBU
                elif funct_field == 0b100011:
                    control_out.next = alu_code._SUB
                    front_sel.next = 1

                # AND
                elif funct_field == 0b100100:
                    control_out.next = alu_code._AND
                    front_sel.next = 1

                # OR
                elif funct_field == 0b100101:
                    control_out.next = alu_code._OR
                    front_sel.next = 1

                # SLT
                elif funct_field == 0b101010:
                    control_out.next = alu_code._SLT
                    front_sel.next = 1

                # SLL, SRL, SRA, SRAV, SLLV
                elif funct_field == 0b000000:  # SLL
                    control_out.next = alu_code._ADD
                    front_sel.next = 1

                elif funct_field == 0b000010:  # SRL
                    control_out.next = alu_code._ADD
                    front_sel.next = 1

                elif funct_field == 0b000011:  # SRA
                    control_out.next = alu_code._ADD
                    front_sel.next = 1

                elif funct_field == 0b000100:  # SLLV
                    control_out.next = alu_code._ADD
                    front_sel.next = 1

                elif funct_field == 0b000111:  # SRAV
                    control_out.next = alu_code._ADD
                    front_sel.next = 1

                else:
                    control_out.next = alu_code._AND
                    front_sel.next = 1
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
