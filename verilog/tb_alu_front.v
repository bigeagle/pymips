`include "comb_alu_front.v"
`include "alu_front.v"

module tb_alu_front;

reg [0:0] clk;
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
    op1 = 17;
    op2 = -65535;
    clk = 1;
    #50 func = 'h18;
end

always #10  clk = ~clk;

comb_alu_front comb(
    aluop,
    func,
    shamt,
    op1,
    op2,
    out_1,
    out_2
);

alu_front seq(
    clk,
    aluop,
    func,
    shamt,
    op1,
    op2,
    out_1,
    out_2
);

endmodule
