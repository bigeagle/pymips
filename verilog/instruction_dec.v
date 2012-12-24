// File: instruction_dec.v
// Generated by MyHDL 0.7
// Date: Sat Dec 22 14:03:41 2012


module instruction_dec (
    instruction,
    opcode,
    rs,
    rt,
    rd,
    shamt,
    func,
    immediate, 
    jump,
    NopSignal
);
// Decode segments of 32bits encoded instruction
// 
// instruction: 32 bits
// rs = Signal(intbv(0)[5:])       #instruction 25:21  - to read_reg_1
// rt = Signal(intbv(0)[5:])       #instruction 20:16  - to read_reg_2 and mux controlled by RegDst
// rd = Signal(intbv(0)[5:])       #instruction 15:11  - to the mux controlled by RegDst
// shamt = Signal(intbv(0)[5:])    #instruction 10:6   -
// func = Signal(intbv(0)[6:])     #instruction 5:0    - to ALUCtrl
// address = Signal(intbv(0)[16:]) #instruction 15:0   - to Sign Extend

input [31:0] instruction;
output [5:0] opcode;
reg [5:0] opcode;
output [4:0] rs;
reg [4:0] rs;
output [4:0] rt;
reg [4:0] rt;
output [4:0] rd;
reg [4:0] rd;
output [4:0] shamt;
reg [4:0] shamt;
output [5:0] func;
reg [5:0] func;
output [15:0]immediate;
reg [15:0] immediate;
output [25:0] jump;
reg [25:0] jump;
output [0:0] NopSignal;
reg [0:0] NopSignal;

always @(instruction) begin: INSTRUCTION_DEC_DECODE
    opcode = instruction[32-1:26];
    rs = instruction[26-1:21];
    rt = instruction[21-1:16];
    rd = instruction[16-1:11];
    shamt = instruction[11-1:6];
    func = instruction[6-1:0];
    immediate = $signed(instruction[16-1:0]);
    jump = instruction[26-1:0];
    if ((instruction == 0)) begin
        NopSignal = 1;
    end
    else begin
        NopSignal = 0;
    end
end

endmodule