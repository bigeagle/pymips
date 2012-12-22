module tb_data_reg_judge;

reg [0:0] branch_if;
reg [0:0] jump;
reg [0:0] branch_en;
reg [0:0] RegW_en;
reg [31:0] Ip;
reg [4:0] InstRegDest;
reg [31:0] AluResult;
wire [4:0] RegDest;
wire [31:0] Data2Reg;
wire [0:0] RegWrite;

initial begin
    $from_myhdl(
        branch_if,
        jump,
        branch_en,
        RegW_en,
        Ip,
        InstRegDest,
        AluResult
    );
    $to_myhdl(
        RegDest,
        Data2Reg,
        RegWrite
    );
end

data_reg_judge dut(
    branch_if,
    jump,
    branch_en,
    RegW_en,
    Ip,
    InstRegDest,
    AluResult,
    RegDest,
    Data2Reg,
    RegWrite
);

endmodule
