// File: mux4.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 13:58:07 2012


module mux4 (
    sel,
    mux_out,
    chan1,
    chan2,
    chan3,
    chan4
);
// 4-channels m-bits multiplexor
// 
// channels: generic bits input vectors
// mux_out: is the output vector
// sel: is the channel selector

input [1:0] sel;
output [31:0] mux_out;
reg [31:0] mux_out;
input [31:0] chan1;
input [31:0] chan2;
input [31:0] chan3;
input [31:0] chan4;






always @(chan4, sel, chan1, chan3, chan2) begin: MUX4_ROUTE_CHANNEL
    case (sel)
        'h0: begin
            mux_out = chan1;
        end
        'h1: begin
            mux_out = chan2;
        end
        'h2: begin
            mux_out = chan3;
        end
        'h3: begin
            mux_out = chan4;
        end
    endcase
end

endmodule
