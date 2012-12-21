#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


"""
AND gate
"""

import random

from myhdl import Signal, delay, always_comb, always, Simulation, \
    intbv, bin, instance, instances, now, toVHDL

from myhdl.conversion import analyze

from alu_control import alu_op_code

def and_gate(op1, op2, out):
    """
    op1: operator 1.
    op2: operator 2.
    out: and
    """

    @always_comb
    def logic():
        out.next = op1 & op2

    return logic


def branch_judge(clk, ALUop, branch, jump, zero, positive, out):
    """
    clk: clock
    ALUop: BEQ, BGEZ, BGEZL, BGTZ, BLEZ, BLTZ, BLTZAL, BNE
    zero: is ALU result zero?
    positive: is ALU result positive?
    out: judgement
    """

    @always(clk.negedge)
    def logic():
        if jump == 1:
            out.next = 1
        elif branch == 1:
            if ALUop == alu_op_code.MBEQ:
                out.next = zero
            elif ALUop == alu_op_code.MBNE:
                out.next = ~zero
            elif ALUop == alu_op_code.MBGEZ:
                out.next = positive
            elif ALUop == alu_op_code.MBGEZAL:
                out.next = positive
            elif ALUop == alu_op_code.MBLTZ:
                out.next = ~positive
            elif ALUop == alu_op_code.MBLTZAL:
                out.next = ~positive
            elif ALUop == alu_op_code.MBGTZ:
                out.next = positive & (~zero)
            elif ALUop == alu_op_code.MBLEZ:
                out.next = (~positive) | zero
        else:
            out.next = 0

    return logic


def data_reg_judge(branch_if, jump, branch_en, RegW_en, Ip, InstRegDest, AluResult, RegDest, Data2Reg, RegWrite):
    """
    branch_if: weather this is a branch instruction
    branch_en: weather to branch
    RegW_en: weather to write register
    Ip: IP
    InstRegDest: Reg Dest in instruction
    ALUResult: ALU result
    RegDest: final reg dest
    Data2reg: final data2reg
    RegWrite: Signal to enable RegWrite
    """
    @always_comb
    def logic():
        if jump == 1 and RegW_en == 1:
            RegDest.next = 31
            Data2Reg.next = Ip + 4
            RegWrite.next = 1

        elif branch_if == 1 and RegW_en == 1:
            # set RegDest to $31 and Data2Reg IP+8
            # only if it is a branch instruction and branch has been detected
            # and it is a branch/jump and link instruction
            if branch_en == 1:
                RegDest.next = 31
                Data2Reg.next = Ip + 4
                RegWrite.next = 1

            if branch_en == 0:
                # if branch condition not satisfied, disable reg write
                RegDest.next = InstRegDest
                Data2Reg.next = AluResult
                RegWrite.next = 0

        else:
            # if it is not a branch instruction, pass through reg write
            # infomations
            RegDest.next = InstRegDest
            Data2Reg.next = AluResult
            RegWrite.next = RegW_en

    return logic


### TESTBENCHS

def testBench_gate():

    op1_i = Signal(intbv(0)[1:])
    op2_i = Signal(intbv(0)[1:])

    out_i = Signal(intbv(0)[1:])

    and_gate_i = toVHDL(and_gate, op1_i, op2_i, out_i)

    @instance
    def stimulus():
        for a in range(2):
            op1_i.next = a

            for b in range(2):
                op2_i.next = b

                yield delay(2)

                print "%i %i | %i " % (op1_i, op2_i, out_i)

    return instances()


def main():
    #sim = Simulation(testBench_alu_control())
    sim = Simulation(testBench_gate())
    sim.run()

if __name__ == '__main__':
    main()
