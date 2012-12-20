#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Instruction memory
"""

from myhdl import Signal, delay, always_comb, now, Simulation, \
    intbv, bin, instance, instances, toVHDL, toVerilog


def load_program(ROM, program=None, comment_char='#'):
    if program is None:
        #try:
        #    import sys
        #    program = sys.argv[1]
        #    #import pdb
        #    #pdb.set_trace()
        #except IndexError:
        #    #default
        program = '../programs/simple.txt'
    index = 0
    for line in open(program):
        line = line.split(comment_char)[0]
        line = line.replace(' ', '')

        if len(line) in (8, 32):
            try:
                t = int(line, 2)
            except:
                t = int(line, 16)
            inst = "%08x" % t
            for i in range(4):
                ROM[4*index+i] = int(inst[2*i:2*(i+1)], 16)
            index += 1

    return tuple(ROM)


def instruction_memory(address, instruction, program=None):
    """
    address -- the pointer defined by PC
    instruction -- 32 bit encoded instruction
    """
    ROM = load_program([0] * 2048, program=program)

    @always_comb
    def logic():
            #print "Address:", address
            instruction.next[32:24] = ROM[int(address)]
            instruction.next[24:16] = ROM[int(address+1)]
            instruction.next[16:8] = ROM[int(address+2)]
            instruction.next[8:] = ROM[int(address+3)]
    return logic


def testBench():

    I = Signal(intbv(0, min=0, max=16))
    O = Signal(intbv(0)[32:])

    #pd_instance = prime_detector(E, S)
    im_instance = toVHDL(instruction_memory, I, O)

    @instance
    def stimulus():
        for i in range(8):
            I.next = intbv(i)
            yield delay(10)
            print "address: " + bin(I, 4) + " (" + str(I) + ") | instruction: " + bin(O, 32)

    return instances()


def main():
    sim = Simulation(testBench())
    sim.run()


if __name__ == '__main__':
    main()
