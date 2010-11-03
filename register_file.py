#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Register file
"""

import random 

from myhdl import Signal, delay, always_comb, always, Simulation, \
                  intbv, bin, instance, instances, now, toVHDL


def register_file (read_reg1, read_reg2, write_reg, data_in, write_control, out_data1, out_data2, depth=8):

    mem = [Signal(intbv(0, min=-(2**31), max=2**31-1)) for i in range(depth)]
    

    @always_comb
    def write():
        if write_control:
            mem[int(write_reg)].next = data_in.signed()
    
    @always_comb
    def read():
        if not write_control:
            out_data1.next = mem[int(read_reg1)]
            out_data2.next = mem[int(read_reg2)]
        
        print [int(i.val) for i in mem]
    

    return write, read



def group(lst, n):
    """group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
    
    Group a list into consecutive n-tuples. Incomplete tuples are
    discarded e.g.
    
    >>> group(range(10), 3)
    [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    """
    return zip(*[lst[i::n] for i in range(n)]) 



def testBench():
    
    depth = 32

    read_reg1, read_reg2, write_reg = [ Signal(intbv(0)[5:]) for i in range(3) ] 

    data_in, out_data1, out_data2 = [Signal( intbv(0, min=-(2**31),max=2**31-1)) for i in range(3)]

    write_control = Signal(intbv(0)[1:])

    register_file_i = toVHDL(register_file, read_reg1, read_reg2, write_reg, data_in, write_control, out_data1, out_data2, depth)

    @instance
    def stimulus():

        #write
        for i in range(depth):
            value = random.randint(-(2**31), 2**31-1)
            data_in.next = intbv( value, min=-(2**31), max=2**31-1)
            write_reg.next = i
            write_control.next = 1

            print "Written: reg %i = %d" % ( i, value)
            yield delay(5)
            write_control.next = 0
            yield delay(5)
        
        #read
        for a, b in group(range(depth), 2):
            read_reg1.next, read_reg2.next = a, b
            yield delay(5)
            print "Read: reg %i = %d | reg %i = %d" % (read_reg1, out_data1, read_reg2, out_data2)
            
    return instances()


def main():
    sim = Simulation(testBench())
    sim.run()

if __name__ == '__main__':
    main()
