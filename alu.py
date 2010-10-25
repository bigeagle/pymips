#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


"""
ALU
"""

import random

from myhdl import Signal, delay, always_comb, always, Simulation, \
                  intbv, bin, instance, instances, now



def alu(control, op1, op2, out, zero):
    """
    control : 4 bit control vector.
    op1: operator 1. 32bits
    op2: operator 2. 32bits
    out: ALU result. 32bits
    zero: zero detector. ``1`` when out is 0. 

    =============  =======================
     ALU control    Function
    =============  =======================
     0000           AND
     0001           OR
     0010           add
     0110           substract
     0111           set on less than
     1100           NOR
    =============  =======================

    """

    @always_comb
    def logic():
        if bin(control, 4) == '0000':
            out.next =  op1 & op2

        elif bin(control, 4) == '0001':
            out.next =  op1 | op2

        elif bin(control, 4) == '0010':
            out.next =  op1 + op2           #what happend if there is overflow ?
       
        elif bin(control, 4) == '0110':
            out.next =  op1 - op2

        elif bin(control, 4) == '0111':
            #TODO: set on less than
            pass
        elif bin(control, 4) == '1100':
            out.next =  ~ (op1 | op2)   #TODO check this

    return logic




def testBench():

    control_i = Signal(intbv(0)[4:])

    op1_i = Signal(intbv(0)[32:].signed())
    op2_i = Signal(intbv(0)[32:].signed())
    
    out_i = Signal(intbv(0)[32:].signed())

    zero_i = Signal(0)
    
    alu_i = alu(control_i, op1_i, op2_i, out_i, zero_i)

    control_func = (('0000', 'AND'), ('0001', 'OR'),  ('0010', 'add'), ('0110', 'substract'), ('0111', 'set on <'), ('1100', 'NOR') )

    @instance
    def stimulus():
        for control_val, func in [(int(b, 2), func) for (b,func) in control_func]:
            control_i.next = Signal(intbv(control_val))

            op1_i.next, op2_i.next = [Signal(intbv(random.randint(0, 255))[32:]) for i in range(2)]
            
            yield delay(10)
            print "Control: %s | %i %s %i | %i" % (bin(control_i, 4), op1_i, func, op2_i, out_i) 
            
    return instances()
        
def main():
    sim = Simulation(testBench())
    sim.run()

if __name__ == '__main__':
    main()