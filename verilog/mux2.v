// File: mux2.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 13:58:07 2012


module mux2 (
    sel,
    mux_out,
    chan1,
    chan2
);
parameter dataWidth=32;
// 2-channels m-bits multiplexor
// 
// channels: generic bits input vectors
// mux_out: is the output vector
// sel: is the channel selector

input sel;
output [dataWidth-1:0] mux_out;
reg [dataWidth-1:0] mux_out;
input [dataWidth-1:0] chan1;
input [dataWidth-1:0] chan2;






always @(sel, chan1, chan2) begin: MUX2_ROUTE_CHANNEL
    if ((sel == 0)) begin
        mux_out = chan1;
    end
    else begin
        mux_out = chan2;
    end
end

endmodule
