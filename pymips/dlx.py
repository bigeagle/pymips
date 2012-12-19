#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#

"""
Datapath
"""

from myhdl import Signal, always, Simulation, \
    intbv, bin, instance, instances, now, toVHDL, toVerilog, traceSignals, delay

from clock_driver import clock_driver
from program_counter import program_counter
from adder import adder
from instruction_memory import instruction_memory
from instruction_decoder import instruction_dec
from alu import ALU
from alu_front import alu_front, branch_alu_front

from alu_control import alu_control, alu_code, alu_op_code
from branch_judge import branch_judge, data_reg_judge
from control import control
from register_file import register_file
from sign_extender import sign_extend
from mux import mux2, mux4
from data_memory import data_memory

from latch_if_id import latch_if_id
from latch_id_ex import latch_id_ex
from latch_ex_mem import latch_ex_mem
from latch_mem_wb import latch_mem_wb

#hazard controls

from forwarding import forwarding
from hazard_detector import hazard_detector


SIM_TIME = 40  # time to simulation.

DEBUG = False  # set to false to convert


MIN = -(2 ** 31)
MAX = 2 ** 31 - 1

MIN_16 = -(2 ** 15)
MAX_16 = 2 ** 15 - 1


def dlx(clk_period=1, Reset=Signal(intbv(0)[1:]), Zero=Signal(intbv(0)[1:]), program=None, data_mem=None, reg_mem=None):
    """
    A DLX processor with 5 pipeline stages.
    =======================================

    Stages
    ------
     +------------------+
     |        +------- Hazard
     |        |    +-> Detect <-----+
     |        |    |   |            |
     |        |    |   |            |
     v        v    |   v            |
     [IF] -> IF/ID -> [ID] -> ID/EX -> [EX] -> EX/MEM -> [MEM] -> MEM/WB __
                   ^                |  ^                |               |  |
                   |                |  |  <_____________|               |  |
                   |                +> FORW <___________________________|  |
                   |                                                       |
                   |_______________________________________________________|

    Conventions:
    ------------

    * Signals are in ``CamelCase``

    * Instances are with ``under_score_`` (with a last ``_``)

    * The signals shared two or more stage are suffixed with the pipeline stage to which it belongs.
      For example: ``PcAdderO_if``  before IF/ID latch is the same signal than
      ``PcAdderO_id`` after it.

    """

    ##############################
    # clock settings
    ##############################

    Clk = Signal(intbv(0)[1:])  # internal clock

    clk_driver = clock_driver(Clk, clk_period)

    ####################
    #feedback Signals
    ######################

    # signals from and advanced stage which feeds a previous component

    BranchAdderO_mem = Signal(intbv(0, min=MIN, max=MAX))
    PCSrc_mem = Signal(intbv(0)[1:])  # control of mux for program_counter on IF stage - (branch or inmediante_next)

    FlushOnBranch = PCSrc_mem           # 1 when beq condition is asserted => flush IF / ID / EX to discard
                                        # instructions chargued wrongly

    WrRegDest_wb = Signal(intbv(0)[32:])  # register pointer where MuxMemO_wb data will be stored.
    MuxMemO_wb = Signal(intbv(0, min=MIN, max=MAX))  # data output from WB mux connected as Write Data input on Register File (ID stage)

    RegWrite_wb = Signal(intbv(0)[1:])

    ForwardA, ForwardB = [Signal(intbv(0)[2:]) for i in range(2)]  # Signals Generated in Forwarding units to control ALU's input muxers

    AluResult_mem = Signal(intbv(0, min=MIN, max=MAX))

    Stall = Signal(intbv(0)[1:])  # when asserted the pipeline is stalled. It 'freezes' PC count
                                  #and put all Control Signals to 0's

    ##############################
    # IF
    ##############################
    #instruction memory
    Ip = Signal(intbv(0)[32:])  # connect PC with intruction_memory

    #PC
    NextIp = Signal(intbv(0)[32:])  # output of mux_branch - input of pc

    #pc_adder
    INCREMENT = 1  # it's 4 in the book, but my instruction memory is organized in 32bits words, not in bytes
    PcAdderOut_if = Signal(intbv(0)[32:])  # output of pc_adder - input0 branch_adder and mux_branch

    #pc_adder = ALU(Signal(intbv('0010')[4:]), Ip, Signal(intbv(INCREMENT)[1:]), PcAdderOut_if, Signal(intbv(0)[1:]))  # hardwiring an ALU to works as an adder

    pc_adder = adder(a=Ip, b=Signal(intbv(INCREMENT)[1:]), out=PcAdderOut_if)

    #mux controlling next ip branches.

    mux_pc_source = mux2(sel=PCSrc_mem, mux_out=NextIp, chan1=PcAdderOut_if, chan2=BranchAdderO_mem)

    pc = program_counter(Clk, input=NextIp, output=Ip, stall=Stall)

    Instruction_if = Signal(intbv(0)[32:])  # 32 bits instruction line.
    im = instruction_memory(Ip, Instruction_if, program)

    ##############################
    # IF/ID
    ##############################
    Ip_id = Signal(intbv(0)[32:])
    Instruction_id = Signal(intbv(0)[32:])

    latch_if_id_ = latch_if_id(clk=Clk, rst=FlushOnBranch, instruction_in=Instruction_if,
                               ip_in=Ip, instruction_out=Instruction_id,
                               ip_out=Ip_id, stall=Stall)

    ##############################
    # ID
    ##############################
    #DECODER
    Opcode_id = Signal(intbv(0)[6:])  # instruction 31:26  - to Control
    Rs_id = Signal(intbv(0)[5:])  # instruction 25:21  - to read_reg_1
    Rt_id = Signal(intbv(0)[5:])  # instruction 20:16  - to read_reg_2 and mux controlled by RegDst
    Rd_id = Signal(intbv(0)[5:])  # instruction 15:11  - to the mux controlled by RegDst
    Shamt_id = Signal(intbv(0)[5:])  # instruction 10:6   -
    Func_id = Signal(intbv(0)[6:])  # instruction 5:0    - to ALUCtrl
    Address16_id = Signal(intbv(0, min=-(2 ** 15), max=2 ** 15 - 1))  # instruction 15:0   - to Sign Extend

    NopSignal = Signal(intbv(0)[1:])

    instruction_decoder_ = instruction_dec(Instruction_id, Opcode_id, Rs_id, Rt_id, Rd_id, Shamt_id, Func_id, Address16_id, NopSignal)

    #CONTROL
    signals_1bit = [Signal(intbv(0)[1:]) for i in range(7)]
    RegDst_id, ALUSrc_id, MemtoReg_id, RegWrite_id, MemRead_id, MemWrite_id, Branch_id = signals_1bit

    ALUop_id = Signal(alu_op_code._NOP)

    control_ = control(Opcode_id, Rt_id, RegDst_id, Branch_id, MemRead_id,
                       MemtoReg_id, ALUop_id, MemWrite_id, ALUSrc_id, RegWrite_id, NopSignal, Stall)

    #sign extend
    Address32_id = Signal(intbv(0, min=MIN, max=MAX))

    sign_extend_ = sign_extend(Address16_id, Address32_id)

    #REGISTER FILE
    Data1_id = Signal(intbv(0, min=MIN, max=MAX))
    Data2_id = Signal(intbv(0, min=MIN, max=MAX))

    register_file_i = register_file(Clk, Rs_id, Rt_id, WrRegDest_wb, MuxMemO_wb, RegWrite_wb, Data1_id, Data2_id, depth=32, mem=reg_mem)

    ##############################
    # ID/EX
    ##############################
    Ip_ex = Signal(intbv(0)[32:])

    signals_1bit = [Signal(intbv(0)[1:]) for i in range(7)]
    RegDst_ex, ALUSrc_ex, MemtoReg_ex, RegWrite_ex, MemRead_ex, MemWrite_ex, Branch_ex = signals_1bit

    ALUop_ex = Signal(alu_op_code._NOP)

    Data1_ex = Signal(intbv(0, min=MIN, max=MAX))
    Data2_ex = Signal(intbv(0, min=MIN, max=MAX))

    Rs_ex = Signal(intbv(0)[5:])  # instruction 25:21  - to read_reg_1
    Rt_ex = Signal(intbv(0)[5:])  # instruction 20:16  - to read_reg_2 and mux controlled by RegDst
    Rd_ex = Signal(intbv(0)[5:])  # instruction 15:11  - to the mux controlled by RegDst
    #Shamt_ex = Signal(intbv(0)[5:])    #instruction 10:6   -
    Func_ex = Signal(intbv(0)[6:])  # instruction 5:0    - to ALUCtrl

    Address32_ex = Signal(intbv(0, min=MIN, max=MAX))

    latch_id_ex_ = latch_id_ex(Clk, Reset,
                               Ip_id,
                               Data1_id, Data2_id, Address32_id,
                               Rs_id, Rt_id, Rd_id, Func_id,

                               RegDst_id, ALUop_id, ALUSrc_id,  # signals to EX pipeline stage
                               Branch_id, MemRead_id, MemWrite_id,  # signals to MEM pipeline stage
                               RegWrite_id, MemtoReg_id,  # signals to WB pipeline stage

                               Ip_ex,
                               Data1_ex, Data2_ex, Address32_ex,
                               Rs_ex, Rt_ex, Rd_ex, Func_ex,

                               RegDst_ex, ALUop_ex, ALUSrc_ex,  # signals to EX pipeline stage
                               Branch_ex, MemRead_ex, MemWrite_ex,  # signals to MEM pipeline stage
                               RegWrite_ex, MemtoReg_ex  # signals to WB pipeline stage
                               )

    ##############################
    # EX
    ##############################
    BranchAdderO_ex = Signal(intbv(0, min=MIN, max=MAX))

    Zero_ex = Signal(intbv(0)[1:])
    Positive_ex = Signal(intbv(0)[1:])
    AluResult_ex = Signal(intbv(0, min=MIN, max=MAX))

    ForwMux1Out, ForwMux2Out, ALUFout1, ALUFout2, BALUFout1, BALUFout2, ALUIn1, ALUIn2 = [Signal(intbv(0, min=MIN, max=MAX)) for i in range(8)]  # Output of forw_mux1 and forw_mux2

    MuxAluDataSrc_ex = Signal(intbv(0, min=MIN, max=MAX))

    WrRegDest_ex = Signal(intbv(0)[5:])

    forw_mux1_ = mux4(sel=ForwardA, mux_out=ForwMux1Out,
                      chan1=Data1_ex, chan2=MuxMemO_wb, chan3=AluResult_mem)

    forw_mux2_ = mux4(sel=ForwardB, mux_out=ForwMux2Out,
                      chan1=Data2_ex, chan2=MuxMemO_wb, chan3=AluResult_mem)

    #2nd muxer of 2nd operand in ALU
    mux_alu_front_src_ = mux2(sel=ALUSrc_ex, mux_out=MuxAluDataSrc_ex, chan1=ForwMux2Out, chan2=Address32_ex)

    #Branch adder
    branch_adder_ = adder(Ip_ex, Address32_ex, BranchAdderO_ex, debug=True)

    #ALU Control
    AluControl = Signal(alu_code._AND)  # control signal to alu
    alu_control_ = alu_control(ALUop_ex, Func_ex, AluControl)

    #ALU Front
    Alu_front_ = alu_front(Clk, ALUop_ex, ForwMux1Out, MuxAluDataSrc_ex, ALUFout1, ALUFout2)
    Branch_Alu_front_ = branch_alu_front(ALUop_ex, ForwMux1Out, MuxAluDataSrc_ex, BALUFout1, BALUFout2)

    mux_alu_src1_ = mux2(sel=Branch_ex, mux_out=ALUIn1, chan1=ALUFout1, chan2=BALUFout1)
    mux_alu_src2_ = mux2(sel=Branch_ex, mux_out=ALUIn2, chan1=ALUFout2, chan2=BALUFout2)

    alu_ = ALU(control=AluControl, op1=ALUIn1, op2=ALUIn2, out_=AluResult_ex, zero=Zero_ex, positive=Positive_ex)

    #Mux RegDestiny Control Write register between rt and rd.
    mux_wreg = mux2(RegDst_ex, WrRegDest_ex, Rt_ex, Rd_ex)

    RegDest_ex = Signal(intbv(0)[5:])
    Data2Reg_ex = Signal(intbv(0, min=MIN, max=MAX))
    FinalRegWrite_ex = Signal(intbv(0)[1:])

    branch_judge_ = branch_judge(Clk, ALUop_ex, Branch_ex, Zero_ex, Positive_ex, PCSrc_mem)

    Data_2_reg_judge_ = data_reg_judge(Branch_ex, PCSrc_mem, RegWrite_ex, Ip_ex, WrRegDest_ex, AluResult_ex, RegDest_ex, Data2Reg_ex, FinalRegWrite_ex)

    ##############################
    # EX/MEM
    ##############################
    Zero_mem = Signal(intbv(0)[1:])

    Data2_mem = Signal(intbv(0, min=MIN, max=MAX))

    WrRegDest_mem = Signal(intbv(0)[32:])

    #control signals
    signals_1bit = [Signal(intbv(0)[1:]) for i in range(5)]
    MemtoReg_mem, RegWrite_mem, MemRead_mem, MemWrite_mem, Branch_mem = signals_1bit

    latch_ex_mem_ = latch_ex_mem(Clk, Reset,
                                 BranchAdderO_ex,
                                 Data2Reg_ex, Zero_ex,
                                 ForwMux2Out, RegDest_ex,
                                 Branch_ex, MemRead_ex, MemWrite_ex,  # signals to MEM pipeline stage
                                 FinalRegWrite_ex, MemtoReg_ex,  # signals to WB pipeline stage

                                 BranchAdderO_mem,
                                 AluResult_mem, Zero_mem,
                                 Data2_mem, WrRegDest_mem,
                                 Branch_mem, MemRead_mem, MemWrite_mem,  # signals to MEM pipeline stage
                                 RegWrite_mem, MemtoReg_mem,  # signals to WB pipeline stage
                                 )

    ##############################
    # MEM
    ##############################
    DataMemOut_mem = Signal(intbv(0, min=MIN, max=MAX))

    #branch AND gate

    #data memory
    data_memory_ = data_memory(Clk, AluResult_mem, Data2_mem, DataMemOut_mem, MemRead_mem, MemWrite_mem, mem=data_mem)

    ##############################
    # EX/WB
    ##############################
    #RegWrite_wb, on feedback signals section
    MemtoReg_wb = Signal(intbv(0)[1:])

    DataMemOut_wb = Signal(intbv(0, min=MIN, max=MAX))
    AluResult_wb = Signal(intbv(0, min=MIN, max=MAX))

    #WrRegDest_wb on feedback signals sections.
    latch_mem_wb_ = latch_mem_wb(Clk, Reset,
                                 DataMemOut_mem,
                                 AluResult_mem,
                                 WrRegDest_mem,
                                 RegWrite_mem, MemtoReg_mem,  # signals to WB pipeline stage

                                 DataMemOut_wb,
                                 AluResult_wb,
                                 WrRegDest_wb,
                                 RegWrite_wb, MemtoReg_wb,  # signals to WB pipeline stage
                                 )

    ##############################
    # WB
    ##############################

    #mux2(sel, mux_out, chan1, chan2):

    mux_mem2reg_ = mux2(MemtoReg_wb, MuxMemO_wb, AluResult_wb, DataMemOut_wb)

    ##############################
    # Forwarding unit
    ##############################
    forwarding_ = forwarding(RegWrite_mem, WrRegDest_mem, Rs_ex, Rt_ex,  # inputs of EX hazards
                             RegWrite_wb, WrRegDest_wb,  # left inputs of MEM hazards
                             ForwardA, ForwardB
                             )

    ##############################
    # hazard detection unit
    ##############################
    hazard_detector_ = hazard_detector(MemRead_ex, Rt_ex,
                                       Rs_id, Rt_id,
                                       Stall)

    if DEBUG:
        @always(Clk.posedge)
        def debug_internals():
            sep = "\n" + "=" * 31 + " cycle %i (%ins)" + "=" * 31
            print sep % (int(now() / 2.0 + 0.5), now())
            #IF
            print "\n" + "." * 35 + " IF " + "." * 35 + "\n"
            print "PcAdderOut_if %i | BranchAdderO_mem %i | PCSrc_mem %i | NextIp %i | Ip %i" % (PcAdderOut_if, BranchAdderO_mem, PCSrc_mem, NextIp, Ip)
            print 'Instruction_if %s (%x)' % (bin(Instruction_if, 32), Instruction_if)

            if True:  # now () > 2:

                #ID
                print "\n" + "." * 35 + " ID " + "." * 35 + "\n"
                print "Ip_id %i | Instruction_id %s (%x) | Nop %i" % (Ip_id, bin(Instruction_id, 32), Instruction_id, NopSignal)
                print 'Op %s | Rs %i | Rt %i | Rd %i | Func %i | Addr16 %i | Addr32 %i' % \
                    (bin(Opcode_id, 6), Rs_id, Rt_id, Rd_id, Func_id, Address16_id, Address32_id)

                print 'Data1 %i | Data2 %i' % (Data1_id, Data2_id)
                print '-->CONTROL'
                print 'RegDst %i  ALUop %s  ALUSrc %i | Branch %i  MemR %i  MemW %i |  RegW %i Mem2Reg %i ' % \
                    (RegDst_id, ALUop_id, ALUSrc_id, Branch_id, MemRead_id, MemWrite_id, RegWrite_id, MemtoReg_id)

                print 'Stall --> %i' % Stall

            if True:  # if now () > 4:

                #EX
                print "\n" + "." * 35 + " EX " + "." * 35 + "\n"

                print "Ip_ex %i | BranchAdderO_ex %i " % (Ip_ex, BranchAdderO_ex)
                print "Rs %i | Rt %i | Rd %i | Func %i | Addr32 %i" % (Rs_ex, Rt_ex, Rd_ex, Func_ex, Address32_ex)

                print 'Data1_ex %i | Data2_ex %i' % (Data1_ex, Data2_ex)

                print 'ForwardA %i | ForwardB %i' % (ForwardA, ForwardB)
                print 'ForwMux1Out %i | ForwMux2Out %i' % (ForwMux1Out, ForwMux2Out)

                print '-->CONTROL'
                print 'RegDst %i  ALUop %s  ALUSrc %i | Branch %i  MemR %i  MemW %i |  RegW %i Mem2Reg %i ' % \
                    (RegDst_ex, ALUop_ex, ALUSrc_ex, Branch_ex, MemRead_ex, MemWrite_ex, RegWrite_ex, MemtoReg_ex)

                print '--> ALU'
                print 'MuxAluDataSrc %i  | AluCtrl %s | AluResult_ex %i | Zero_ex %i' % (MuxAluDataSrc_ex, AluControl, AluResult_ex, Zero_ex)
                print 'WrRegDest_ex %i' % WrRegDest_ex

            if True:  # if now () > 6:

                #MEM
                print "\n" + "." * 35 + "MEM " + "." * 35 + "\n"
                print "BranchAdderO_mem %i " % (BranchAdderO_mem)

                print '-->CONTROL'
                print 'Branch %i  MemR %i  MemW %i |  RegW %i Mem2Reg %i ' % \
                    (Branch_mem, MemRead_mem, MemWrite_mem, RegWrite_mem, MemtoReg_mem)

                print '--> Branch'
                print 'Branch_mem %i Zero %i | PCSrc_mem %i' % (Branch_mem, Zero_mem, PCSrc_mem)

                print '--> Data mem'
                print 'AluResult_mem %i | Data2_mem %i | DataMemOut_mem %i | MemW %i MemR %i' \
                    % (AluResult_mem, Data2_mem, DataMemOut_mem, MemWrite_mem, MemRead_mem)

                print 'WrRegDest_mem %i' % WrRegDest_mem

            if True:  # if now() > 8:
                #WB
                print "\n" + "." * 35 + "WB" + "." * 35 + "\n"
                print 'CONTROL --> RegW %i Mem2Reg %i ' % (RegWrite_mem, MemtoReg_mem)

                print 'DataMemOut_wb %i | AluResult_wb %i | MuxMemO_wb %i ' % (DataMemOut_wb, AluResult_wb, MuxMemO_wb)
                print 'WrRegDest_wb %i | MuxMemO_wb %i' % (WrRegDest_wb, MuxMemO_wb)

    return instances()


def testBench(args):
    global DEBUG
    DEBUG = args.debug
    if args.vcd:
        datapath_i = traceSignals(dlx)  # () #toVHDL(datapath)
    elif args.debug:
        datapath_i = dlx()
    elif args.to_vhdl:
        toVHDL(dlx)
    elif args.to_verilog:
        toVerilog(dlx)

    return instances()


def main(test=False):
    import argparse
    parser = argparse.ArgumentParser(description='A simple mips')
    parser.add_argument('--debug', action='store_true', help='print debug information')
    parser.add_argument('--vcd', action='store_true', help='export vcd file')
    parser.add_argument('--to-vhdl', action='store_true', help='export to VHDL')
    parser.add_argument('--to-verilog', action='store_true', help='export to Verilog')

    args = parser.parse_args()

    sim = Simulation(testBench(args))
    sim.run(SIM_TIME)


if __name__ == '__main__':

    main()
