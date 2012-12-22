#!/usr/bin/env python2
# -*- coding:utf8 -*-
from myhdl import intbv, always_comb, toVerilog, Signal


def adder(a, b, out, debug=False):
    """
    ip: current IP
    increment: IP increment step
    pc_out: address output
    """

    @always_comb
    def update():
        out.next = a + b
    return update


def branch_jump(branch, jump, pc, baddr, jaddr, rs, out):
    """
    branch:
    jump:
    pc: pc adder out
    addr:
    out:
    """
    @always_comb
    def logic():
        if jump == 1:
            if branch == 1:
                out.next = rs
            elif branch == 0:
                out.next = intbv((pc & intbv(0xf0000000)[32:]) | (jaddr << 2))[32:]
        else:
            out.next = pc + baddr

    return logic

if __name__=="__main__":
    a, b, pc, baddr, jaddr, rs, out = [Signal(intbv(0)[32:]) for i in range(7)]
    branch, jump = [Signal(intbv(0)[1:]) for i in range(2)]

    toVerilog(adder, a, b, out)
    toVerilog(branch_jump, branch, jump, pc, baddr, jaddr, rs, out)



# vim: ts=4 sw=4 sts=4 expandtab
