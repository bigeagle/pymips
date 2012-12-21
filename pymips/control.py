#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Control
"""

from myhdl import Signal, delay, always_comb, always, Simulation, \
    intbv, bin, instance, instances, now, toVHDL, toVerilog

from alu_control import alu_op_code


def control(opcode, Rt, func, RegDst, Branch, Jump, MemRead, MemtoReg, ALUop,
            MemWrite, ALUSrc, RegWrite, NopSignal, Stall):
    """
    opcode -- 6bit opcode field from instruction
    RegDst, ALUSrc, MemtoReg -- 1bit signals to control multiplexors
    ALUSrc -- 1: Immediate Num, 0: Register/Forwarded
    RegWrite, MemRead, MemWrite -- 1bit signals to control reads and writes
                                   in registers and memory
    Branch -- 1bit signal to determining whether to possibly branch
    ALUop -- 2bit control signal for the ALU
    Signed -- whether immediate num is extended signed or unsigned
    """

    @always_comb
    def logic():
        if NopSignal == 1 or Stall == 1:
            RegDst.next = 0
            ALUSrc.next = 0
            MemtoReg.next = 0
            RegWrite.next = 0
            MemRead.next = 0
            MemWrite.next = 0
            Branch.next = 0
            Jump.next = 0
            ALUop.next = alu_op_code.MNOP

        else:

            if opcode == 0:  # r-format
                if func == 0b001000:
                    RegDst.next = 0
                    ALUSrc.next = 0
                    MemtoReg.next = 0
                    RegWrite.next = 0
                    MemRead.next = 0
                    MemWrite.next = 0
                    Branch.next = 1
                    Jump.next = 1
                    ALUop.next = alu_op_code.MJR
                elif func == 0b001001:
                    RegDst.next = 0
                    ALUSrc.next = 0
                    MemtoReg.next = 0
                    RegWrite.next = 1
                    MemRead.next = 0
                    MemWrite.next = 0
                    Branch.next = 1
                    Jump.next = 1
                    ALUop.next = alu_op_code.MJALR

                else:
                    RegDst.next = 1
                    ALUSrc.next = 0
                    MemtoReg.next = 0
                    RegWrite.next = 1
                    MemRead.next = 0
                    MemWrite.next = 0
                    Branch.next = 0
                    Jump.next = 0
                    ALUop.next = alu_op_code.MRFORMAT

            #add
            elif opcode == 0b001000:  # ADDI
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MADD

            elif opcode == 0b001001:  # ADDIU
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MADD

            elif opcode == 0b001111:  # LUI
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MLUI

            elif opcode == 0b001101:  # ORI
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MORI

            elif opcode == 0b001100:  # ORI
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MANDI

            elif opcode == 0x23:  # lw
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 1
                RegWrite.next = 1
                MemRead.next = 3
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MADD

            elif opcode == 0x20:  # lw
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 1
                RegWrite.next = 1
                MemRead.next = 1
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MADD

            elif opcode == 0x2b:  # sw
                ALUSrc.next = 1
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 3
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MADD

            # branch instructions
            elif opcode == 0x04:  # beq
                RegDst.next = 0
                ALUSrc.next = 0
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 1
                Jump.next = 0
                ALUop.next = alu_op_code.MBEQ

            elif opcode == 0b000101:  # BNE
                RegDst.next = 0
                ALUSrc.next = 0
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 1
                Jump.next = 0
                ALUop.next = alu_op_code.MBNE

            elif opcode == 0x01:  # BGEZ, BGEZAL, BLTZ, BLTZAL
                RegDst.next = 0
                ALUSrc.next = 0
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 1
                Jump.next = 0

                if Rt == 0b00001:
                    ALUop.next = alu_op_code.MBGEZ
                    RegWrite.next = 0
                elif Rt == 0b10001:
                    ALUop.next = alu_op_code.MBGEZAL
                    RegWrite.next = 1
                elif Rt == 0b00000:
                    ALUop.next = alu_op_code.MBLTZ
                    RegWrite.next = 0
                elif Rt == 0b10000:
                    ALUop.next = alu_op_code.MBLTZAL
                    RegWrite.next = 1

            elif opcode == 0b000111:  # BGTZ
                ALUSrc.next = 0
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 1
                Jump.next = 0
                if Rt == 0b00000:
                    ALUop.next = alu_op_code.MBGTZ

            elif opcode == 0b000110:  # BLEZ
                ALUSrc.next = 0
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 1
                Jump.next = 0
                if Rt == 0b00000:
                    ALUop.next = alu_op_code.MBLEZ

            # Jump
            elif opcode == 0b000010:
                ALUSrc.next = 0
                RegWrite.next = 0
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 1
                ALUop.next = alu_op_code.MJ

            elif opcode == 0b000011:
                ALUSrc.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 1
                ALUop.next = alu_op_code.MJ

            elif opcode == 0b001010:
                RegDst.next = 0
                ALUSrc.next = 1
                MemtoReg.next = 0
                RegWrite.next = 1
                MemRead.next = 0
                MemWrite.next = 0
                Branch.next = 0
                Jump.next = 0
                ALUop.next = alu_op_code.MSLT

    return logic


def testBench():

    signal_1bit = [Signal(intbv(0)[1:]) for i in range(7)]
    RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch = signal_1bit
    ALUop = Signal(intbv(0)[2:])

    opcode = Signal(intbv(0)[6:])

    control_inst = toVHDL(control, opcode, RegDst, Branch, MemRead, MemtoReg, ALUop, MemWrite, ALUSrc, RegWrite)

    @instance
    def stimulus():
        for op_value in [0, int('100011', 2), int('101011', 2), int('000100', 2)]:
            opcode.next = op_value
            yield delay(10)

            print 'opcode: ', bin(opcode, 6)
            print RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, bin(ALUop, 2)

    return instances()


def main():
    #sim = Simulation(testBench())
    #sim.run()
    signals_1bit = [Signal(intbv(0)[1:]) for i in range(7)]
    signals_2bit = [Signal(intbv(0)[2:]) for i in range(2)]
    RegDst_id, ALUSrc_id, MemtoReg_id, RegWrite_id, Branch_id, Jump_id, Stall = signals_1bit
    MemRead_id, MemWrite_id = signals_2bit
    Opcode_id = Signal(intbv(0)[6:])  # instruction 31:26  - to Control

    ALUop_id = Signal(alu_op_code.MNOP)
    NopSignal = Signal(intbv(0)[1:])
    Func_id = Signal(intbv(0)[6:])  # instruction 5:0    - to ALUCtrl
    Rt_id = Signal(intbv(0)[5:])  # instruction 20:16  - to read_reg_2 and mux controlled by RegDst

    toVerilog(control, Opcode_id, Rt_id, Func_id, RegDst_id, Branch_id, Jump_id, MemRead_id,
                       MemtoReg_id, ALUop_id, MemWrite_id, ALUSrc_id, RegWrite_id, NopSignal, Stall)

if __name__ == '__main__':
    main()
