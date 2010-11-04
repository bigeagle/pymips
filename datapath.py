#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Datapath
"""

from myhdl import Signal, delay, always, always_comb, now, Simulation, \
                  intbv, bin, instance, instances, now, toVHDL


from program_counter import ClkDriver, program_counter
from instruction_memory import instruction_memory
from instruction_decoder import instruction_dec
from alu import ALU
from alu_control import alu_control
from control import control
from register_file import register_file
from sign_extender import sign_extend
from mux import mux2, mux4

DEBUG = True  #set to false to convert 


def datapath(clk, reset=Signal(intbv(0)[1:]), zero=Signal(intbv(0)[1:])):


    #
    #   internal signals
    #

    ip = Signal(intbv(0)[16:] ) #connect PC with intruction_memory
    instruction = Signal(intbv(0)[32:])   #32 bits instruction line.

    #control signals
    signal_1bit = [Signal(intbv(0)[1:]) for i in range(7)]
    RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch = signal_1bit     
    
    #ALUop connect Control with ALUcontrol
    ALUop = Signal(intbv(0)[2:])  

    #intruction memory output connectors
    opcode = Signal(intbv(0)[6:])   #instruction 31:26  - to Control
    rs = Signal(intbv(0)[5:])       #instruction 25:21  - to read_reg_1
    rt = Signal(intbv(0)[5:])       #instruction 20:16  - to read_reg_2 and mux controlled by RegDst
    rd = Signal(intbv(0)[5:])       #instruction 15:11  - to the mux controlled by RegDst
    shamt = Signal(intbv(0)[5:])    #instruction 10:6   - 
    func = Signal(intbv(0)[6:])     #instruction 5:0    - to ALUCtrl
    address = Signal(intbv(0)[16:]) #instruction 15:0   - to Sign Extend

    wr_reg_in = Signal(intbv(0)[5:]) #output of mux_wreg (it's rt or rd depends on RegDst)

    address32 = Signal(intbv(0)[32:]) #output of signextend

    #register file data vectors (input and outputs)
    data_in, data1, data2 = [Signal( intbv(0, min=-(2**31),max=2**31-1)) for i in range(3)]
    
    mux_alu_out = Signal( intbv(0, min=-(2**31),max=2**31-1)) #output of mux_alu_src 
                                                              #(data2 or address32 depends on ALUSrc)

    #ALU signals
    alu_control_out = Signal(intbv('1111')[4:])
    alu_out = Signal(intbv(0,  min=-(2**31), max=2**31-1)) 
    zero = Signal(bool(False))



    

    #
    # component instances
    #
    pc = program_counter(clk, ip)
    im = instruction_memory (ip, instruction)
    
    id = instruction_dec(instruction, opcode, rs, rt, rd, shamt, func, address)

    mux_wreg = mux2(RegDst, wr_reg_in, rt, rd)
    register_file_i = register_file(rs, rt, wr_reg_in, data_in, RegWrite, data1, data2, depth=32)
    
    
    sign_extend_i = sign_extend(address, address32)

    alu_control_i = alu_control(ALUop, func, alu_control_out)

    mux_alu_src = mux2(ALUSrc, mux_alu_out, data2, address32)
    alu_i = ALU(alu_control_out, data1, mux_alu_out, alu_out, zero)


    control_i = control(opcode, RegDst, Branch, MemRead, MemtoReg, ALUop, MemWrite, ALUSrc, RegWrite)

    

    if DEBUG:
        @always(clk.posedge)
        def debug_internals():
            print "-" * 78
            print "time: %s | Clock: %i | ip: %i" % (now(), clk, ip)
            print 'instruction', bin(instruction, 32) 

            print 'opcode %s | rs %i | rt %i | rd %i | shamt %i | func %i | address %i' % \
                 (bin(opcode, 6), rs, rt, rd, shamt, func, address )

            print 'wr_reg_in %i | dat1 %i | dat2 %i | muxALUo %i ' % \
                  (wr_reg_in, data1, data2, mux_alu_out)

            print 'RegDst %i | ALUSrc %i | Mem2Reg %i | RegW %i | MemR %i | MemW %i | Branch %i | ALUop %s' % ( RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, bin(ALUop, 2))
        
            print 'func: %s | aluop: %s | alu_c_out: %s' % ( bin(func, 5), 
                                                            bin(ALUop, 2), 
                                                            bin(alu_control_out, 4) )

            print 'ALU_out: %i | Zero: %i' % (alu_out, zero)

            
            

    return instances()



def testBench():

    clk = Signal(intbv(0)[1:])
    clkdriver_inst = ClkDriver(clk)


    if not DEBUG:
        datapath_i = toVHDL(datapath, clk)
    else:
        datapath_i = datapath(clk)

    

    return instances()



def main():
    sim = Simulation(testBench())
    sim.run(10)


if __name__ == '__main__':

    """
    DATAPATH


    problema detectado. La operacion add r0, r1, r2  representa la funcion 100100

    """


    main()



