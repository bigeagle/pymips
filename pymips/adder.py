#!/usr/bin/env python2
# -*- coding:utf8 -*-
from myhdl import always_comb


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

# vim: ts=4 sw=4 sts=4 expandtab
