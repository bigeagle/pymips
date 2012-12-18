#!/usr/bin/env python2
# -*- coding:utf-8 -*-

from myhdl import always, always_comb, intbv, bin

from alu_control import alu_op_code


def alu_front(clk, aluop, op1, op2, out_1, out_2):
    """
    aluop : ALU operation vector.
    op1: operator 1. 32bits
    op2: operator 2. 32bits
    out_1: data send to ALU
    out_2: data send to ALU
    """

    @always(clk.negedge)
    def logic():
        if aluop == alu_op_code._ORI:  # ORI
            out_1.next = op1
            out_2.next[32:16] = intbv('0000000000000000')
            out_2.next[16:] = op2[16:]

        elif aluop == alu_op_code._ANDI:  # ANDI
            #print "ALU_FRONT: %s, %s" % (bin(op1, 32), bin(op2, 32))
            out_1.next = op1
            out_2.next[32:16] = intbv('0000000000000000')
            out_2.next[16:] = op2[16:]

        elif aluop == alu_op_code._LUI:  # LUI
            out_1.next = 0
            out_2.next[32:16] = op2[16:]
            out_2.next[16:] = intbv('0000000000000000')

        else:
            out_1.next = op1
            out_2.next = op2

    return logic







# vim: ts=4 sw=4 sts=4 expandtab
