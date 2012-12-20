.text
.globl main

main:
    li $v0, 2
    li $3, 3
    li $4, 4
    li $6, 6 
    add $7, $v0, $v1
    sub $5, $7, $4
    add $3, $7, $2
loop:
    add $5, $5, $5
    beq $5, $2, loop
    add $7, $4, $3
    sub $5, $5, $5
    bgezal $5, test
    add $7, $6, $3
test:
    bgtz $7, L1
    nop
test2:
    blez $0, L2
    nop
test3:
    li $3, -1
    bgtz $3, test2
    nop
    bltz $3, L3
    nop
test4:
    bltzal $3, L4 
    nop
#test5:
#    bne $3, $0, end
#    nop

L1:
    li $8, 11
    beq $0, $0, test2 
    nop
L2:
    li $8, 12
    beq $0, $0, test3
    nop
L3:
    li $8, 13
    beq $0, $0, test4
    nop
L4:
    li $8, 14
#    jr $31
    nop
end:
    nop
    nop
    nop
