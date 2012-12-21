.text 
.globl main

main:
    li $2, 5
    li $3, 6
    mult $2, $3
    mflo $4
    #break 0x7 
    #slt $4, $2, $3
    #slt $4, $3, $2
    #slti $2, 6
    #slti $3, 5
