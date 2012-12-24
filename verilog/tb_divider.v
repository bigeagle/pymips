`include "divider.v"
`timescale 10ns/10ns;

module tb_divider;

reg [0:0] clk;
reg reset;
reg [31:0] dividend;
reg [31:0] divisor;
reg start;
wire [31:0] quotient;
wire [31:0] reminder;
wire done;
reg [31:0] HI;
reg [31:0] LO;

initial begin
    reset = 1;
    clk = 0;
    #5 reset = 0;
    dividend = 30;
    divisor = 7;
end
always #1 clk = ~clk;
always @(negedge clk)
    if(done == 1) begin
        start <= 0;
        HI <= reminder;
        LO <= quotient;
    end
    else begin
        start <= 1;
    end

stream_divider devider(
    clk,
    reset,
    
    start,
    dividend,
    divisor,

    done,
    quotient,
    reminder
);


endmodule
