.text
.globl main

main:
start:
    li $5, 0x10000000
    sw $0, 0($5)
    li $2, 0xff
    li $3, 0xfe
    sw $2, 4($5)
    sw $3, 8($5)

    lb $4, 4($5)
    add $6, $4, $2
    sw $6, 4($5)
    lw $7, 4($5)
    sw $6, 12($5)
    lw $8, 12($5)
