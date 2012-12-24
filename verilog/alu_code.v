//ALU Code
parameter ALU_AND = 3'b000;
parameter ALU_OR = 3'b001;
parameter ALU_NOR = 3'b010;
parameter ALU_ADD = 3'b011;
parameter ALU_SUB = 3'b100;
parameter ALU_SLT = 3'b101;

//ALU OP Code
parameter ALU_OP_NOP = 5'b00000;
parameter ALU_OP_ADD = 5'b00001;
parameter ALU_OP_SUB = 5'b00010;
parameter ALU_OP_MUL = 5'b00011;
parameter ALU_OP_DIV = 5'b00100;
parameter ALU_OP_LUI = 5'b00101;
parameter ALU_OP_ORI = 5'b00110;
parameter ALU_OP_SLT = 5'b00111;
parameter ALU_OP_ANDI = 5'b01000;
parameter ALU_OP_RFORMAT = 5'b01001;
//branches
parameter ALU_OP_BEQ = 5'b01010;
parameter ALU_OP_BNE = 5'b01011;
parameter ALU_OP_BGEZ = 5'b01100;
parameter ALU_OP_BGEZAL = 5'b01101;
parameter ALU_OP_BGTZ = 5'b01110;
parameter ALU_OP_BLEZ = 5'b01111;
parameter ALU_OP_BLTZ = 5'b10000;
parameter ALU_OP_BLTZAL = 5'b10001;
parameter ALU_OP_J = 5'b10010;
parameter ALU_OP_JAL = 5'b10011;
parameter ALU_OP_JALR = 5'b10100;
parameter ALU_OP_JR = 5'b10101;
