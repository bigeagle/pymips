// File: hazard_detector.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 14:44:58 2012


`timescale 1ns/10ps

module hazard_detector (
    MemRead_ex,
    Rt_ex,
    Rs_id,
    Rt_id,
    Stall
);
// Stalls the pipeline when a instruction try to read a register
// following a load instruction that writes the same register.
// (raw data hazard)
// 
// it controls the writing of PC and IF/ID registers plus a multiplexor
// that choose between the real control values or all 0s

input [0:0] MemRead_ex;
input [4:0] Rt_ex;
input [4:0] Rs_id;
input [4:0] Rt_id;
output [0:0] Stall;
reg [0:0] Stall;






always @(Rt_id, Rs_id, Rt_ex, MemRead_ex) begin: HAZARD_DETECTOR_LOGIC
    if (((MemRead_ex != 0) && ((Rt_ex == Rs_id) || (Rt_ex == Rt_id)))) begin
        Stall = 1;
    end
    else begin
        Stall = 0;
    end
end

endmodule
