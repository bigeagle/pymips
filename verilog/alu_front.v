// File: alu_front.v
// Generated by MyHDL 0.7
// Date: Fri Dec 21 20:31:39 2012
`include "divider.v"

module alu_front (
    clk,
    reset,
    aluop,
    func,
    shamt,
    op1,
    op2,
    out_1,
    out_2,
    busy
);
// aluop : ALU operation vector.
// op1: operator 1. 32bits
// op2: operator 2. 32bits
// out_1: data send to ALU
// out_2: data send to ALU

input [0:0] clk;
input reset;
input [4:0] aluop;
input [5:0] func;
input [4:0] shamt;
input signed [31:0] op1;
input signed [31:0] op2;
output signed [31:0] out_1;
reg signed [31:0] out_1;
output signed [31:0] out_2;
reg signed [31:0] out_2;
output busy;
reg busy;

reg signed [31:0] LO;
reg signed [31:0] HI;

reg [64-1:0] tmp;
reg mul_or_div;

reg divstart;
wire divdone;

wire [32-1:0] quotient;
wire [32-1:0] reminder;

wire [32-1:0] dividend;
wire [32-1:0] divisor;

stream_divider divider(
    clk,
    reset,

    divstart,
    dividend, 
    divisor,

    divdone,
    quotient,
    reminder
);

`include "alu_code.v"

assign dividend = op1;
assign divisor = op2;

always @(negedge reset) begin
    divstart <= 0;
end

always @(negedge clk) begin: ALU_FRONT_LOGIC
    if (divstart == 0) begin
        busy <= 0;
        if (aluop == ALU_OP_RFORMAT) begin
            case (func)
                'h18: begin
                    out_1 <= 0;
                    out_2 <= 0;
                    tmp = (op1 * op2);
                    HI <= $signed(tmp[64-1:32]);
                    LO <= $signed(tmp[32-1:0]);
                end
                'h19: begin
                    out_1 <= 0;
                    out_2 <= 0;
                    tmp = (op1 * op2);
                    HI <= $signed(tmp[64-1:32]);
                    LO <= $signed(tmp[32-1:0]);
                end
                'h10: begin
                    out_1 <= 0;
                    out_2 <= HI;
                end
                'h12: begin
                    out_1 <= 0;
                    out_2 <= LO;
                end
                'h1a: begin
                    out_1 <= 0;
                    out_2 <= 0;
                    divstart <= 1; 
                end
                'h1b: begin
                    out_1 <= 0;
                    out_2 <= 0;
                    divstart <= 1; 
                end
            endcase
        end
        else begin
            out_1 <= op1;
            out_2 <= op2;
            divstart <= 0; 
        end
    end
    else begin
        busy <= 1;
        if(divdone == 1) begin
            divstart <= 0;
            HI <= reminder;
            LO <= quotient;
        end
        else
            divstart <= 1;
    end
end

endmodule
