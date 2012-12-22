`include "comb_alu_front.v"

module tb_comb_alu_front;

reg [4:0] aluop;
reg [5:0] func;
reg [4:0] shamt;
reg [31:0] op1;
reg [31:0] op2;
wire [31:0] out_1;
wire [31:0] out_2;

initial begin
    aluop = 5'b01001;
    func = 3;
    shamt = 5;
    op1 = 0;
    op2 = -65535;
end

comb_alu_front dut(
    aluop,
    func,
    shamt,
    op1,
    op2,
    out_1,
    out_2
);

endmodule
