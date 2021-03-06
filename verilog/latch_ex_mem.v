// File: latch_ex_mem.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 14:09:54 2012

module latch_ex_mem (
    clk,
    rst,
    branch_adder_in,
    alu_result_in,
    data2_in,
    wr_reg_in,
    MemRead_in,
    MemWrite_in,
    RegWrite_in,
    MemtoReg_in,
    branch_adder_out,
    alu_result_out,
    data2_out,
    wr_reg_out,
    MemRead_out,
    MemWrite_out,
    RegWrite_out,
    MemtoReg_out
);
// Latch to control state between Execution and MEM pipeline stages

input [0:0] clk;
input [0:0] rst;
input signed [31:0] branch_adder_in;
input signed [31:0] alu_result_in;
input signed [31:0] data2_in;
input signed [4:0] wr_reg_in;
input [1:0] MemRead_in;
input [1:0] MemWrite_in;
input [0:0] RegWrite_in;
input [0:0] MemtoReg_in;
output signed [31:0] branch_adder_out;
reg signed [31:0] branch_adder_out;
output signed [31:0] alu_result_out;
reg signed [31:0] alu_result_out;
output signed [31:0] data2_out;
reg signed [31:0] data2_out;
output signed [4:0] wr_reg_out;
reg signed [4:0] wr_reg_out;
output [0:0] MemRead_out;
reg [1:0] MemRead_out;
output [1:0] MemWrite_out;
reg [1:0] MemWrite_out;
output [1:0] RegWrite_out;
reg [0:0] RegWrite_out;
output [0:0] MemtoReg_out;
reg [0:0] MemtoReg_out;






always @(posedge clk, posedge rst) begin: LATCH_EX_MEM_LATCH
    if ((rst == 1)) begin
        branch_adder_out <= 0;
        alu_result_out <= 0;
        data2_out <= 0;
        wr_reg_out <= 0;
        MemRead_out <= 0;
        MemWrite_out <= 0;
        RegWrite_out <= 0;
        MemtoReg_out <= 0;
    end
    else begin
        branch_adder_out <= branch_adder_in;
        alu_result_out <= alu_result_in;
        data2_out <= data2_in;
        wr_reg_out <= wr_reg_in;
        MemRead_out <= MemRead_in;
        MemWrite_out <= MemWrite_in;
        RegWrite_out <= RegWrite_in;
        MemtoReg_out <= MemtoReg_in;
    end
end

endmodule
