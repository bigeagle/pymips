// File: adder.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 13:53:28 2012

module adder (
    a,
    b,
    out
);
// ip: current IP
// increment: IP increment step
// pc_out: address output

input [31:0] a;
input [31:0] b;
output [31:0] out;
wire [31:0] out;

assign out = (a + b);

endmodule
