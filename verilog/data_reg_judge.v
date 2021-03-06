// File: data_reg_judge.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 15:55:40 2012


module data_reg_judge (
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
// branch_if: weather this is a branch instruction
// branch_en: weather to branch
// RegW_en: weather to write register
// Ip: IP
// InstRegDest: Reg Dest in instruction
// ALUResult: ALU result
// RegDest: final reg dest
// Data2reg: final data2reg
// RegWrite: Signal to enable RegWrite

input [0:0] branch_if;
input [0:0] jump;
input [0:0] branch_en;
input [0:0] RegW_en;
input [31:0] Ip;
input [4:0] InstRegDest;
input signed [31:0] AluResult;
output [4:0] RegDest;
reg [4:0] RegDest;
output signed [31:0] Data2Reg;
reg signed [31:0] Data2Reg;
output [0:0] RegWrite;
reg [0:0] RegWrite;


always @(branch_if, InstRegDest, Ip, RegW_en, jump, AluResult, branch_en) begin: DATA_REG_JUDGE_LOGIC
    if (((jump == 1) && (RegW_en == 1))) begin
        RegDest = 31;
        Data2Reg = (Ip + 4);
        RegWrite = 1;
    end
    else if (((branch_if == 1) && (RegW_en == 1))) begin
        if ((branch_en == 1)) begin
            RegDest = 31;
            Data2Reg = (Ip + 4);
            RegWrite = 1;
        end
        if ((branch_en == 0)) begin
            RegDest = InstRegDest;
            Data2Reg = AluResult;
            RegWrite = 0;
        end
    end
    else begin
        RegDest = InstRegDest;
        Data2Reg = AluResult;
        RegWrite = RegW_en;
    end
end

endmodule
