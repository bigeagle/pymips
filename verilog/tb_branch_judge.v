module tb_branch_judge;

reg [0:0] clk;
reg [4:0] ALUop;
reg [0:0] branch;
reg [0:0] jump;
reg [0:0] zero;
reg [0:0] positive;
wire [0:0] out;

initial begin
    $from_myhdl(
        clk,
        ALUop,
        branch,
        jump,
        zero,
        positive
    );
    $to_myhdl(
        out
    );
end

branch_judge dut(
    clk,
    ALUop,
    branch,
    jump,
    zero,
    positive,
    out
);

endmodule
