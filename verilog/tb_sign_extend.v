`include "sign_extend.v"

module tb_sign_extend;

reg signed [15:0] in_16;
reg [31:0] extout;
wire [31:0] out;

initial begin
    in_16 = -32767;
end
always #20 extout = out;
sign_extend sex (in_16, out);

endmodule
