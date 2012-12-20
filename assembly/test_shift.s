.text
.globl main

main:
start:
    lui $5, 0
    li $3, 8
    li $2, 0xff0000ee
    sll $7, $2, 5
    sllv $7, $2, $3
    srl $7, $2, 5
    sra $7, $2, 5
    srav $7, $2, $3

