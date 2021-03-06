// File: program_counter.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 14:27:41 2012

module program_counter (
    clk,
    reset,
    ip_in,
    ip_out, 
    stall
);
// clk : clock signal
// input: the input count
// output: address output

input [0:0] clk;
input reset;
input [32-1:0] ip_in;
input [0:0] stall;
output [32-1:0] ip_out;
reg [32-1:0] ip_out;

always @(negedge clk) begin: PROGRAM_COUNTER_UPDATE
    if (reset==1) 
      ip_out <= 0;
    if ((!stall)) begin
        ip_out <= ip_in; 
    end
end

endmodule
