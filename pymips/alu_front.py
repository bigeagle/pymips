#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from myhdl import Signal, always, always_comb, intbv, bin, concat, instances, Simulation, traceSignals, toVerilog

from alu_control import alu_op_code
from shift import shift, shift_op

MIN = -2**31
MAX = 2**31 - 1


def alu_front(clk, aluop, func, shamt, op1, op2, out_1, out_2):
    """
    aluop : ALU operation vector.
    op1: operator 1. 32bits
    op2: operator 2. 32bits
    out_1: data send to ALU
    out_2: data send to ALU
    """

    HI, LO = [Signal(intbv(0, min=MIN, max=MAX)) for x in range(2)]

    @always(clk.negedge)
    def logic():
        if aluop == alu_op_code.MRFORMAT:
            if func == 0b011000:  # MULT
                out_1.next = 0
                out_2.next = 0
                tmp = intbv(op1 * op2)[64:]
                HI.next = tmp[64:32].signed()
                LO.next = tmp[32:].signed()

            elif func == 0b011001:  # MULTU
                out_1.next = 0
                out_2.next = 0
                tmp = intbv(op1 * op2)[64:]
                HI.next = tmp[64:32].signed()
                LO.next = tmp[32:].signed()

            elif func == 0b010000:  # MFHI
                out_1.next = 0
                out_2.next = HI

            elif func == 0b010010:  # MFLO
                out_1.next = 0
                out_2.next = LO

            elif func == 0b011010:   # DIV
                out_1.next = 0
                out_2.next = 0
                HI.next = op1 % op2
                LO.next = op1 // op2

            elif func == 0b011011:   # DIVU
                out_1.next = 0
                out_2.next = 0
                HI.next = op1 % op2
                LO.next = op1 // op2

            elif func == 13:  # break
                raise Exception("program break")

        else:
            out_1.next = op1
            out_2.next = op2

    return instances()


def branch_alu_front(aluop, op1, op2, out_1, out_2):
    # branch instructions
    @always_comb
    def logic():
        if aluop == alu_op_code.MBGEZ:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBGEZAL:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBLTZ:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBLTZAL:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBGTZ:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBLEZ:
            out_1.next = op1
            out_2.next = 0
        else:
            out_1.next = op1
            out_2.next = op2

    return logic


def shift_alu_front(func, shamt, op1, op2, out_1, out_2):
    shift_in, shift_out = [Signal(intbv(0, min=MIN, max=MAX)) for x in range(2)]

    shift_in = Signal(intbv(0, min=MIN, max=MAX))
    shift_ctl = Signal(shift_op._NOP)
    shift_amount = Signal(intbv(0)[5:])
    shift_ = shift(shift_in, shift_amount, shift_ctl, shift_out)

    @always_comb
    def logic():
        if func == 0:
            shift_in.next = op2
            shift_ctl.next = shift_op.LL
            shift_amount.next = shamt
            out_2.next = op1
            out_1.next = shift_out
        else:
            out_1.next = op1
            out_2.next = op2

    return instances()


def comb_alu_front(aluop, func, shamt, op1, op2, out_1, out_2):

    shift_in, shift_out = [Signal(intbv(0, min=MIN, max=MAX)) for x in range(2)]
    shift_ctl = Signal(shift_op.NNOP)
    shift_amount = Signal(intbv(0)[5:])

    shift_ = shift(shift_in, shift_amount, shift_ctl, shift_out)

    @always_comb
    def logic():
        if aluop == alu_op_code.MRFORMAT:
            if func == 0:
                shift_in.next = op2
                shift_ctl.next = shift_op.LL
                shift_amount.next = shamt
                out_2.next = 0
                out_1.next = shift_out
            elif func == 4:
                shift_in.next = op2
                shift_ctl.next = shift_op.LL
                shift_amount.next = op1[5:]
                out_2.next = 0
                out_1.next = shift_out
            elif func == 2:
                shift_in.next = op2
                shift_ctl.next = shift_op.RL
                shift_amount.next = shamt
                out_2.next = 0
                out_1.next = shift_out
            elif func == 3:
                shift_in.next = op2
                shift_ctl.next = shift_op.RA
                shift_amount.next = shamt
                out_2.next = 0
                out_1.next = shift_out
            elif func == 7:
                shift_in.next = op2
                shift_ctl.next = shift_op.RA
                shift_amount.next = op1[5:]
                out_2.next = 0
                out_1.next = shift_out

            elif func == 13:  # break
                raise Exception("program break")

            else:
                out_1.next = op1
                out_2.next = op2

        elif aluop == alu_op_code.MORI:  # ORI
            out_1.next = op1
            out_2.next = concat(intbv(0)[16:], op2[16:])

        elif aluop == alu_op_code.MANDI:  # ANDI
            #print "ALU_FRONT: %s, %s" % (bin(op1, 32), bin(op2, 32))
            out_1.next = op1
            out_2.next = concat(intbv(0)[16:], op2[16:])

        elif aluop == alu_op_code.MLUI:  # LUI
            out_1.next = 0
            out_2.next = concat(op2[16:], intbv(0)[16:]).signed()

        elif aluop == alu_op_code.MBGEZ:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBGEZAL:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBLTZ:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBLTZAL:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBGTZ:
            out_1.next = op1
            out_2.next = 0
        elif aluop == alu_op_code.MBLEZ:
            out_1.next = op1
            out_2.next = 0
        else:
            out_1.next = op1
            out_2.next = op2

    return instances()

from clock_driver import clock_driver


def test_instance():
    clk = Signal(intbv(0)[1:])
    op1 = Signal(intbv(0b10110111, min=MIN, max=MAX))
    op2 = Signal(intbv(0b10110111, min=MIN, max=MAX))
    out_1 = Signal(intbv(0, min=MIN, max=MAX))
    out_2 = Signal(intbv(0, min=MIN, max=MAX))

    clkdriver_inst = clock_driver(clk)

    shifter_ = comb_alu_front(alu_op_code.MRFORMAT, Signal(0b000000), Signal(0b000111), op1, op2, out_1, out_2)

    return instances()


def main():
    #sim = Simulation(traceSignals(test_instance))
    ##sim = Simulation(testbench())
    #sim.run(20)

    op1 = Signal(intbv(0b10110111, min=MIN, max=MAX))
    op2 = Signal(intbv(0b10110111, min=MIN, max=MAX))
    out_1 = Signal(intbv(0, min=MIN, max=MAX))
    out_2 = Signal(intbv(0, min=MIN, max=MAX))
    func = Signal(intbv(0)[6:])
    shamt = Signal(intbv(0b00111)[5:])
    opcode = Signal(alu_op_code.MRFORMAT)
    clk = Signal(intbv(1)[1:])
    toVerilog(alu_front, clk, opcode, func, shamt, op1, op2, out_1, out_2)


if __name__ == '__main__':
    main()


# vim: ts=4 sw=4 sts=4 expandtab
