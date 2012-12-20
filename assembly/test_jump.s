.text
.globl main

main:
start:
    lui $5, 0
    li $3, 8
loop:
    addi $5, 4
    sub $2, $5, $3
    bgezal $2, test
    nop
    li $31, 7
    bgez $2, end
    nop
    j loop
    nop
test:
    jalr $31
    nop
end:
    nop
    nop
    nop
