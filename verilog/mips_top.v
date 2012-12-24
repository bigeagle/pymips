`include "adder.v"
`include "ALU.v"
`include "alu_control.v"
`include "alu_front.v"
`include "branch_judge.v"
`include "branch_jump.v"
`include "comb_alu_front.v"
`include "control.v"
`include "forwarding.v"
`include "hazard_detector.v"
`include "instruction_dec.v"
`include "latch_ex_mem.v"
`include "latch_if_id.v"
`include "latch_id_ex.v"
`include "latch_mem_wb.v"
`include "mux2.v"
`include "mux4.v"
`include "program_counter.v"
`include "register_file.v"
`include "sign_extend.v"


module mips_processor(
    Rst,            // Reset
    Clk,            // Clock In
    DataMemIn,      // Data To Data Memory
    DataMemOut,     // Data From Data Memory
    MemRead,        // Data Memory Read
    MemWrite,       // Data Memory Write
    MemAddr,        // Data Memroy Address
    Instruction,    // Instruction From Instruction Memory
    InstAddr,       // Instruction Address
    Halt            // Halt Signal
);


// ------------ Input ports ---------------
input Rst;
input Clk;
input [32-1:0] DataMemOut;
input [32-1:0] Instruction;

// ------------ Output Ports --------------
output [32-1:0] DataMemIn;
output [1:0] MemRead;
output [1:0] MemWrite;
output [32-1:0] MemAddr;
output [32-1:0] InstAddr;
output  Halt;
//output InstRead;

// ------ Type of Input Ports -------------
wire Clk;
wire Rst;
wire signed [32-1:0] DataIn;
wire [32-1:0] Instruction;

// ------ Type of Output Ports ------------
wire signed [32-1:0] DataOut;
wire [32-1:0] MemAddr;
wire [32-1:0] InstAddr;
wire [1:0] MemRead;
wire [1:0] MemWrite;
wire Halt;
//wire InstRead;



// ------- Feedback Signals -----------
wire [32-1:0] BranchAdderO_mem;
wire PcSrc_mem;

wire [4:0] WrRegDest_wb;
wire signed [32-1:0] MuxMemO_wb;
wire RegWrite_wb;
wire [1:0] ForwardA;
wire [1:0] ForwardB;
wire signed [32-1:0] AluResult_mem;
wire Stall;

// ------- IF Stage ---------
wire [32-1:0] Ip;
wire [32-1:0] NextIp;
wire [32-1:0] PcInc;
wire [32-1:0] PcAdderOut_if;
wire [32-1:0] Instruction_if;

// ------- Latch IF/ID --------
wire [32-1:0] PcAdderOut_id;
wire [32-1:0] Instruction_id;

// ------- ID Stage ---------
wire [5:0] Opcode_id;
wire [4:0] Rs_id;
wire [4:0] Rt_id;
wire [4:0] Rd_id;
wire [4:0] Shamt_id;
wire [5:0] Func_id;
wire [25:0] JumpAddr_id;
wire signed [15:0] Address16_id;
wire NopSignal;

wire RegDst_id;
wire ALUSrc_id;
wire MemtoReg_id;
wire RegWrite_id;
wire Branch_id;
wire Jump_id;
wire [1:0] MemRead_id;
wire [1:0] MemWrite_id;
wire [4:0] ALUop_id;

wire signed [32-1:0] Address32_id;
wire signed [32-1:0] Data1_id;
wire signed [32-1:0] Data2_id;

// -------- Latch EX/ID ---------
wire [32-1:0] PcAdderOut_ex;

wire RegDst_ex;
wire ALUSrc_ex;
wire MemtoReg_ex;
wire RegWrite_ex;
wire Branch_ex;
wire Jump_ex;
wire [1:0] MemRead_ex;
wire [1:0] MemWrite_ex;

wire [4:0] ALUop_ex;
wire [32-1:0] Data1_ex;
wire [32-1:0] Data2_ex;

wire [4:0] Rs_ex;
wire [4:0] Rt_ex;
wire [4:0] Rd_ex;
wire [4:0] Shamt_ex;
wire [5:0] Func_ex;
wire [32-1:0] JumpAddr_ex;
wire signed [32-1:0] Address32_ex;
wire signed [32-1:0] BranchAddr_ex;

// -------- EX Stage ----------
wire signed [32-1:0] BranchAdderO_ex;
wire Zero_ex;
wire Positive_ex;
wire signed [32-1:0] AluResult_ex;

wire signed [32-1:0] ForwMux1Out;
wire signed [32-1:0] ForwMux2Out;
wire signed [32-1:0] ALUFout1;
wire signed [32-1:0] ALUFout2;
wire signed [32-1:0] BALUFout1;
wire signed [32-1:0] BALUFout2;
wire signed [32-1:0] ALUIn1;
wire signed [32-1:0] ALUIn2;
wire signed [32-1:0] MuxAluDataSrc_ex;

wire [4:0] WrRegDest_ex;
wire [2:0] AluControl;
wire AluFrontSel;
wire MultiClk_ex;
wire ALUBusy; 

wire [4:0] RegDest_ex;
wire signed [32-1:0] Data2Reg_ex;
wire FinalRegWrite_ex;

// ---------- Latch EX/MEM --------
wire signed [32-1:0] Data2_mem;
wire [4:0] WrRegDest_mem;
wire MemtoReg_mem;
wire RegWrite_mem;
wire [1:0] MemRead_mem;
wire [1:0] MemWrite_mem;

// ---------- MEM Stage ---------
// MemDataIO has been defined as IO ports

// ---------- Latch MEM/WB ------
wire MemtoReg_wb;
wire signed [32-1:0] DataMemOut_wb;
wire signed [32-1:0] AluResult_wb;
// ---------- WB--------------
wire signed [32-1:0] DataMemOut_mem;


// ---------- IF Stage -------
assign PcInc = 32'd4;
adder Pc_adder_ (Ip, PcInc, PcAdderOut_if);
mux2 Mux_pc_source_ (.sel(PCSrc_mem), .mux_out(NextIp), .chan1(PcAdderOut_if), .chan2(BranchAdderO_mem));
program_counter Pc_ (Clk, Rst, NextIp, Ip, Stall);
assign Instruction_if = Instruction;
assign InstAddr = Ip;

// ---------- Latch IF/ID -----------
latch_if_id Latch_if_id_ (Clk, PCSrc_mem, Instruction_if, PcAdderOut_if, 
                        Instruction_id, PcAdderOut_id, Stall);

// ----------  ID Stage -------------
instruction_dec Instruction_decoder_ (Instruction_id, Opcode_id, Rs_id, Rt_id, Rd_id, Shamt_id, Func_id, Address16_id, JumpAddr_id, NopSignal);

control Control_ (Opcode_id, Rt_id, Func_id, RegDst_id, Branch_id, Jump_id, MemRead_id,
                       MemtoReg_id, ALUop_id, MemWrite_id, ALUSrc_id, RegWrite_id, NopSignal, Stall);

sign_extend sign_extend_ (Address16_id, Address32_id);

register_file Reg_file_ (Clk, Rst, Rs_id, Rt_id, WrRegDest_wb, MuxMemO_wb, RegWrite_wb, Data1_id, Data2_id);

// ---------  Latch ID/EX ------------

latch_id_ex Latch_id_ex_ (Clk, Rst,
                          PcAdderOut_id,
                          Data1_id, Data2_id, Address32_id, JumpAddr_id,
                          Rs_id, Rt_id, Rd_id, Shamt_id, Func_id,

                          RegDst_id, ALUop_id, ALUSrc_id, Branch_id, Jump_id,
                          MemRead_id, MemWrite_id, 
                          RegWrite_id, MemtoReg_id,

                          PcAdderOut_ex,
                          Data1_ex, Data2_ex, Address32_ex, BranchAddr_ex, JumpAddr_ex,
                          Rs_ex, Rt_ex, Rd_ex, Shamt_ex, Func_ex,

                          RegDst_ex, ALUop_ex, ALUSrc_ex, Branch_ex, Jump_ex,
                          MemRead_ex, MemWrite_ex,
                          RegWrite_ex, MemtoReg_ex
                          );

// --------- EX -----------------
wire [32-1:0] zero;
assign zero = 32'h0;

mux4 forw_mux1_ (.sel(ForwardA), .mux_out(ForwMux1Out),
                    .chan1(Data1_ex), .chan2(MuxMemO_wb), .chan3(AluResult_mem), .chan4(zero));

                    
mux4 forw_mux2_ (.sel(ForwardB), .mux_out(ForwMux2Out),
                    .chan1(Data2_ex), .chan2(MuxMemO_wb), .chan3(AluResult_mem), .chan4(zero));


mux2 mux_alu_front_src_ (.sel(ALUSrc_ex), .mux_out(MuxAluDataSrc_ex), .chan1(ForwMux2Out), .chan2(Address32_ex));


branch_jump branch_jump_ (Branch_ex, Jump_ex, PcAdderOut_ex, BranchAddr_ex, JumpAddr_ex, ForwMux1Out, BranchAdderO_ex);

alu_control alu_control_ (Rst, ALUop_ex, Branch_ex, ALUBusy, Func_ex, AluFrontSel, MultiClk_ex, AluControl, Halt);

alu_front Clk_Alu_front_ (Clk, Rst, ALUop_ex, Func_ex, Shamt_ex, ForwMux1Out, MuxAluDataSrc_ex, ALUFout1, ALUFout2, ALUBusy);
comb_alu_front Comb_Alu_front_ (ALUop_ex, Func_ex, Shamt_ex, ForwMux1Out, MuxAluDataSrc_ex, BALUFout1, BALUFout2);

mux2  mux_alu_src1_ (AluFrontSel, ALUIn1, ALUFout1, BALUFout1);
mux2  mux_alu_src2_ (AluFrontSel, ALUIn2, ALUFout2, BALUFout2);

ALU  alu_ (AluControl, ALUIn1, ALUIn2, AluResult_ex, Zero_ex, Positive_ex);

mux2 #5 mux_wreg_ (RegDst_ex, WrRegDest_ex, Rt_ex, Rd_ex);

branch_judge branch_judge_ (Clk, ALUop_ex, Branch_ex, Jump_ex, Zero_ex, Positive_ex, PCSrc_mem);
    
data_reg_judge  Data_2_reg_judge_ (Branch_ex, Jump_ex, PCSrc_mem, RegWrite_ex, PcAdderOut_ex, WrRegDest_ex, AluResult_ex, RegDest_ex, Data2Reg_ex, FinalRegWrite_ex);

// -----------Latch Ex/Mem --------------
latch_ex_mem latch_ex_mem_ (Clk, Rst,
                             BranchAdderO_ex,
                             Data2Reg_ex,
                             ForwMux2Out, RegDest_ex,
                             MemRead_ex, MemWrite_ex,  
                             FinalRegWrite_ex, MemtoReg_ex, 

                             BranchAdderO_mem,
                             AluResult_mem,
                             Data2_mem, WrRegDest_mem,
                             MemRead_mem, MemWrite_mem,  
                             RegWrite_mem, MemtoReg_mem
                             );

// ----------- MEM --------------------
assign DataMemIn = Data2_mem;
assign DataMemOut_mem = DataMemOut;
assign MemAddr = AluResult_mem;
assign MemRead = MemRead_mem;
assign MemWrite = MemWrite_mem;

// ----------- Latch MEM/WB -------------
latch_mem_wb latch_mem_wb_ (Clk, Rst,
                             DataMemOut_mem,
                             AluResult_mem,
                             WrRegDest_mem,
                             RegWrite_mem, MemtoReg_mem,

                             DataMemOut_wb,
                             AluResult_wb,
                             WrRegDest_wb,
                             RegWrite_wb, MemtoReg_wb
                             );

// ----------- WB  ---------------------
mux2 mux_mem2reg_ (MemtoReg_wb, MuxMemO_wb, AluResult_wb, DataMemOut_wb);


// ----------- Forwarding Unit ----------
forwarding Forwarder (RegWrite_mem, WrRegDest_mem, Rs_ex, Rt_ex, 
                      RegWrite_wb, WrRegDest_wb,
                      ForwardA, ForwardB
                      );

// -----------  Harzard Detect -----------

hazard_detector Hazard_detector_ (MultiClk_ex, MemRead_ex, Rt_ex, Rs_id, Rt_id, Stall);


endmodule

