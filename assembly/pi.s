	.file	1 "pi.c"
	.globl	a
	.align 4
a:
	.word	10000
	.globl	bb
	.align 4
bb:
	.space	4
	.globl	c
	.align 4
c:
	.word	140
	.globl	d
	.align 4
d:
	.space	4
	.globl	e
	.align 4
e:
	.space	4

	.comm	f 564
	.globl	g
	.align 4
g:
	.space	4
	.text
	.align 4
	.globl	main
	.set	nomips16
	.ent	main
main:
	.frame	$fp,56,$31		# vars= 48, regs= 1/0, args= 0, gp= 0
	.mask	0x40000000,-4
	.fmask	0x00000000,0
	addiu	$sp,$sp,-56
	sw	$fp,52($sp)
	move	$fp,$sp
	j	$L2
$L3:
	lw	$2,bb
	lw	$4,a
	li	$3,5			# 0x5
	.set	noreorder
	bne	$3,$0,f1
	div	$0,$4,$3
	break	7
	.set	reorder
f1:
	mfhi	$4
	mflo	$3
	move	$4,$3
	sll	$5,$2,2
	la	$3,f
	addu	$3,$5,$3
	sw	$4,0($3)
	addiu	$2,$2,1
	sw	$2,bb
$L2:
	lw	$3,bb
	lw	$2,c
	#nop
	bne	$3,$2,$L3
	sw	$0,0($fp)
	j	$L4
$L7:
	lw	$2,c
	#nop
	sw	$2,bb
	j	$L5
$L6:
	lw	$3,d
	lw	$2,bb
	#nop
	mult	$3,$2
	mflo	$2
	sw	$2,d
$L5:
	lw	$2,bb
	#nop
	sll	$3,$2,2
	la	$2,f
	addu	$2,$3,$2
	lw	$3,0($2)
	lw	$2,a
	#nop
	mult	$3,$2
	mflo	$3
	lw	$2,d
	#nop
	addu	$2,$3,$2
	sw	$2,d
	lw	$2,bb
	lw	$4,d
	lw	$3,g
	#nop
	addiu	$3,$3,-1
	sw	$3,g
	lw	$3,g
	#nop
	.set	noreorder
	bne	$3,$0,f2
	div	$0,$4,$3
	break	7
	.set	reorder
f2:
	mfhi	$3
	sll	$4,$2,2
	la	$2,f
	addu	$2,$4,$2
	sw	$3,0($2)
	lw	$3,d
	lw	$2,g
	#nop
	.set	noreorder
	bne	$2,$0,f3
	div	$0,$3,$2
	break	7
	.set	reorder
f3:
	mfhi	$4
	mflo	$3
	sw	$3,d
	addiu	$2,$2,-1
	sw	$2,g
	lw	$2,bb
	#nop
	addiu	$2,$2,-1
	sw	$2,bb
	lw	$2,bb
	#nop
	bne	$2,$0,$L6
	lw	$3,d
	lw	$2,a
	#nop
	.set	noreorder
	bne	$2,$0,f4
	div	$0,$3,$2
	break	7
	.set	reorder
f4:
	mfhi	$3
	mflo	$2
	move	$3,$2
	lw	$2,e
	#nop
	addu	$3,$3,$2
	lw	$2,0($fp)
	#nop
	sll	$2,$2,2
	addu	$2,$fp,$2
	sw	$3,4($2)
	lw	$2,0($fp)
	#nop
	addiu	$2,$2,1
	sw	$2,0($fp)
	lw	$2,c
	#nop
	addiu	$2,$2,-14
	sw	$2,c
	lw	$3,d
	lw	$2,a
	#nop
	.set	noreorder
	bne	$2,$0,f5
	div	$0,$3,$2
	break	7
	.set	reorder
f5:
	mfhi	$2
	sw	$2,e
$L4:
	sw	$0,d
	lw	$2,c
	#nop
	sll	$2,$2,1
	sw	$2,g
	lw	$2,g
	#nop
	bne	$2,$0,$L7
	lw	$2,4($fp)
	#nop
	sw	$2,a
	lw	$2,8($fp)
	#nop
	sw	$2,bb
	move	$sp,$fp
	lw	$fp,52($sp)
	addiu	$sp,$sp,56
	j	$31
	.end	main
