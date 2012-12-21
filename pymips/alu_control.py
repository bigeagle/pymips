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
    'MAND',
    'MOR',
    'MNOR',
    'MADD',
    'MSUB',
    'MSLT',
    encoding='binary'
)

alu_op_code = enum(
    'MNOP',
    'MADD',
    'MSUB',
    'MMUL',
    'MDIV',
    'MLUI',
    'MORI',
    'MSLT',
    'MANDI',
    'MRFORMAT',
    # branches
    'MBEQ',
    'MBNE',
    'MBGEZ',
    'MBGEZAL',
    'MBGTZ',
    'MBLEZ',
    'MBLTZ',
    'MBLTZAL',
    # jumps
    'MJ',
    'MJAL',
    'MJALR',
    'MJR',
    encoding='binary'
)


def alu_control(aluop, branch, funct_field, front_sel, control_out):

    @always_comb
    def logic():
        if branch == 1:
            front_sel.next = 1
            control_out.next = alu_code.MSUB

        else:
            if aluop == alu_op_code.MNOP:
                control_out.next = alu_code.MADD
                front_sel.next = 1

            elif aluop == alu_op_code.MADD:  # ADDI
                control_out.next = alu_code.MADD
                front_sel.next = 1

            elif aluop == alu_op_code.MSLT:  # ADDI
                control_out.next = alu_code.MSLT
                front_sel.next = 1

            elif aluop == alu_op_code.MLUI:  # LUI
                control_out.next = alu_code.MADD
                front_sel.next = 1

            elif aluop == alu_op_code.MORI:  # ORI
                control_out.next = alu_code.MOR
                front_sel.next = 1

            elif aluop == alu_op_code.MANDI:  # ANDI
                control_out.next = alu_code.MAND
                front_sel.next = 1

            elif aluop == alu_op_code.MRFORMAT:

                # ADD
                # if funct_field == 0b100000:
                #    control_out.next = alu_code.MADD
                #    front_sel.next = 1
                # ADDU
                # elif funct_field == 0b100001:
                #    control_out.next = alu_code.MADD
                #    front_sel.next = 1

                # SUB
                if funct_field == 0b100010:
                    control_out.next = alu_code.MSUB
                    front_sel.next = 1

                # SUBU
                elif funct_field == 0b100011:
                    control_out.next = alu_code.MSUB
                    front_sel.next = 1

                # AND
                elif funct_field == 0b100100:
                    control_out.next = alu_code.MAND
                    front_sel.next = 1

                # OR
                elif funct_field == 0b100101:
                    control_out.next = alu_code.MOR
                    front_sel.next = 1

                # SLT
                elif funct_field == 0b101010:
                    control_out.next = alu_code.MSLT
                    front_sel.next = 1

                # SLL, SRL, SRA, SRAV, SLLV
                # elif funct_field == 0b000000:  # SLL
                #     control_out.next = alu_code.MADD
                #     front_sel.next = 1

                # elif funct_field == 0b000010:  # SRL
                #     control_out.next = alu_code.MADD
                #     front_sel.next = 1

                # elif funct_field == 0b000011:  # SRA
                #     control_out.next = alu_code.MADD
                #     front_sel.next = 1

                # elif funct_field == 0b000100:  # SLLV
                #     control_out.next = alu_code.MADD
                #     front_sel.next = 1

                # elif funct_field == 0b000111:  # SRAV
                #     control_out.next = alu_code.MADD
                #     front_sel.next = 1
                elif funct_field == 0b011000:  # MULT
                    control_out.next = alu_code.MADD
                    front_sel.next = 0

                elif funct_field == 0b011001:  # MULTU
                    control_out.next = alu_code.MADD
                    front_sel.next = 0

                elif funct_field == 0b010000:  # MFHI
                    control_out.next = alu_code.MADD
                    front_sel.next = 0

                elif funct_field == 0b010010:  # MFLO
                    control_out.next = alu_code.MADD
                    front_sel.next = 0

                elif funct_field == 0b011010:   # DIV
                    control_out.next = alu_code.MADD
                    front_sel.next = 0

                elif funct_field == 0b011011:   # DIVU
                    control_out.next = alu_code.MADD
                    front_sel.next = 0

                else:
                    control_out.next = alu_code.MADD
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
