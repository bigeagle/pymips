// File: sign_extend.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 14:32:45 2012


module sign_extend (
    input16,
    output32
);

input signed [15:0] input16;
output signed [31:0] output32;
wire signed [31:0] output32;

assign output32 = input16;

endmodule
