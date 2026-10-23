0x66874a4	fd7bbfa9	stp x29,x30,[sp, #-0x10]!
0x66874a8	fd030091	mov x29,sp
0x66874ac	36e22a94	bl 0x0713fd84
0x66874b0	689b86d2	mov x8,#0x34db
0x66874b4	c8f6baf2	movk x8,#0xd7b6, LSL #16
0x66874b8	48d0dbf2	movk x8,#0xde82, LSL #32
0x66874bc	6863e8f2	movk x8,#0x431b, LSL #48
0x66874c0	087c489b	smulh x8,x0,x8
0x66874c4	09fd5293	asr x9,x8,#0x12
0x66874c8	20fd488b	add x0,x9,x8, LSR #0x3f
0x66874cc	fd7bc1a8	ldp x29,x30,[sp], #0x10
0x66874d0	c0035fd6	ret
