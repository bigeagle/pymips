#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Data Memory
"""

import random

from myhdl import Signal, delay, always_comb, always, Simulation, \
    intbv, bin, instance, instances, now, toVHDL, concat

MIN= - 2 ** 31
MAX= 2 ** 31 - 1

def group(lst, n):
    return zip(*[lst[i::n] for i in range(n)])

def data_memory(clk, address, write_data, read_data, memread, memwrite, mem=None):
    """
    Ports:

    clk -- trigger
    read_data -- data out
    write_data -- data in
    address -- address bus
    memwrite -- write enable: write if 1
    memread -- interface enable: read address if 1
    """

    mem = mem or [Signal(intbv(0)[8:]) for i in range(4096)]

    #mem[6] = Signal(intbv(51, min=-(2 ** 31), max=2 ** 31 - 1))  # usefull to test load instruction directly

    @always(clk.negedge)
    def logic():
        dw = intbv(write_data.val, min=MIN, max=MAX)
        if memwrite == 3:
            mem[int(address[16:])].next = dw[8:0]
            mem[int(address[16:])+1].next = dw[16:8]
            mem[int(address[16:])+2].next = dw[24:16]
            mem[int(address[16:])+3].next = dw[32:24]

        elif memwrite == 1:
            mem[int(address[16:])].next = dw[8:0]

        elif memread == 3:
            read_data.next = concat(mem[int(address[16:])+3][8:], mem[int(address[16:])+2][8:], mem[int(address[16:])+1][8:], mem[int(address[16:])][8:]).signed()

        elif memread == 1:
            read_data.next = mem[int(address[16:])].signed()

        cared = mem[:96]
        data = group(cared, 4)

        string = ' '.join(map(lambda g: ''.join(map(lambda x: '%02x' % x, g[::-1])), data))

        print 'mem: %s' % string

    return logic


def testBench():

    depth = 5

    address = Signal(intbv(0)[32:])

    data_in, data_out = [Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1)) for i in range(2)]

    clk = Signal(intbv(1)[1:])
    write_control = Signal(intbv(0)[1:])
    read_control = Signal(intbv(0)[1:])

    memory_i = data_memory(clk, address, data_in, data_out, read_control, write_control)

    addresses = [random.randint(0, 1024) for i in range(depth)]
    values = [random.randint(-(2 ** 31), 2 ** 31 - 1) for i in range(depth)]

    @instance
    def stimulus():

        #write
        for addr, val in zip(addresses, values):

            address.next = intbv(addr)[32:]
            data_in.next = intbv(val, min=-(2 ** 31), max=2 ** 31 - 1)

            write_control.next = 1
            clk.next = 0

            print "Write: addr %i = %d" % (addr, val)
            yield delay(5)
            write_control.next = 0
            clk.next = 1
            yield delay(5)

        #read
        for addr in addresses:
            address.next = intbv(addr)[32:]
            read_control.next = 1
            clk.next = 0
            yield delay(5)
            print "Read: addr %i = %d" % (addr, data_out)
            clk.next = 1
            read_control.next = 0
            yield delay(5)

    return instances()


def main():
    sim = Simulation(testBench())
    sim.run()

if __name__ == '__main__':
    main()
