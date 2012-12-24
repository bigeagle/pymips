`include "mips_top.v"
`timescale 10ns/10ns

module tb_mips();

reg signed [32-1:0] DataMemory [0:1024-1];
reg [32-1:0] InstructionMemory [0:1024-1];

reg signed [32-1:0] DataMemOut;
reg [32-1:0] Instruction;
reg Clk;
reg Reset;

wire [32-1:0] DataMemIn;
wire [32-1:0] MemAddr;
wire [10-1:0] MemAddrin;
wire [32-1:0] InstAddr;
wire [10-1:0] InstAddrin;
wire [1:0] MemRead;
wire [1:0] MemWrite;
wire Halt;

integer i;

initial begin
    $dumpfile("mips.vcd");
    $dumpvars;
    Reset = 1'b0;
    #1 Reset = 1'b1;
    Clk = 1'b1;
    for(i=0;i<1024;i=i+1) DataMemory[i] = 0; 


    $readmemh("pirom.txt", InstructionMemory);
    $readmemh("piram.txt", DataMemory);

    #2 Reset = 1'b0;
    #450000 $finish;      // Terminate simulation
end

always #1 Clk = ~Clk;

assign MemAddrin = {2'b00, MemAddr[10-1:2]};
assign InstAddrin = {2'b00, InstAddr[10-1:2]};

always @(InstAddrin) begin
    Instruction = InstructionMemory[InstAddrin];
end

always @(negedge Clk) begin
    if (MemRead == 2'b11 && MemWrite == 2'b00) 
        DataMemOut = DataMemory[MemAddrin];
    else
        if (MemRead == 2'b00 && MemWrite == 2'b11)
            DataMemory[MemAddrin] = DataMemIn;
        else 
            DataMemOut = 32'hZZZZZZZZ;
end

always @(posedge Halt) begin
    $finish;
end

mips_processor MIPS(
    Reset,
    Clk,
    DataMemIn,
    DataMemOut,
    MemRead,
    MemWrite,
    MemAddr,
    Instruction,
    InstAddr,
    Halt
);

endmodule
