module stream_divider(
    clk,
    reset,

    start,
    dividend,
    divisor,

    done,
    quotient,
    reminder
);
parameter width=32;
parameter shiftwidth=6;
parameter nshiftdone=33;
input clk;
input reset;
input start;
input [width-1:0] dividend;
input [width-1:0] divisor;

output done;
output [width-1:0] quotient;
output [width-1:0] reminder;

reg [shiftwidth:0] i;
reg [width:0] s;
reg [2*width-1:0] temp;
reg [2*width-1:0] diff;
reg isNeg;
reg isDone;

always @(posedge clk)
    if(reset == 1) begin
        i <= 0;
        s <= 0;
        temp <= 0;
        diff <= 0;
        isNeg <= 0;
        isDone <= 0;
    end
    else if(start)
        case(i)
            0: begin
                isNeg <= dividend[width-1] ^ divisor[width-1];
                s <= divisor[width-1] ? {1'b1, divisor} : {1'b1, ~divisor + 1'b1};
                temp <= dividend[width-1] ? {32'b0, ~dividend + 1'b1} : {32'b0, dividend};
                i <= 1;
            end
            33: begin
                isDone <= 1'b1;
                i <= i + 1'b1;
            end
            34: begin
                isDone <= 1'b0;
                i <= 0;
            end
            default: begin
                diff = temp + {s, 31'd0};
                if(diff[2*width-1]) 
                    temp <= {temp[2*width-2:0], 1'b0};
                else
                    temp <= {diff[2*width-2:0], 1'b1};
                i <= i + 1'b1;
            end
        endcase
    else
        begin
            isDone <= 0;
            i <= 0;
        end
    assign done = isDone;
    assign quotient = isNeg? {~temp[width-1:0] + 1'b1} : temp[width-1:0];
    assign reminder = dividend[width-1]? {~temp[2*width-1:width] + 1'b1}: temp[2*width-1:width];

endmodule
