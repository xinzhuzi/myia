0x4bb3a88	f85fbca9	stp x24,x23,[sp, #-0x40]!
0x4bb3a8c	f65701a9	stp x22,x21,[sp, #0x10]
0x4bb3a90	f44f02a9	stp x20,x19,[sp, #0x20]
0x4bb3a94	fd7b03a9	stp x29,x30,[sp, #0x30]
0x4bb3a98	fdc30091	add x29,sp,#0x30
0x4bb3a9c	095c4039	ldrb w9,[x0, #0x17]
0x4bb3aa0	281d0013	sxtb w8,w9
0x4bb3aa4	0a0440f9	ldr x10,[x0, #0x8]
0x4bb3aa8	1f010071	cmp w8,#0x0
0x4bb3aac	56b1899a	csel x22,x10,x9,lt
0x4bb3ab0	160400b4	cbz x22,0x04bb3b30
0x4bb3ab4	89c702d0	adrp x9,0xa4a5000
0x4bb3ab8	2ad55c39	ldrb w10,[x9, #0x735]
0x4bb3abc	8a010037	tbnz w10,#0x0,0x04bb3aec
0x4bb3ac0	8af80190	adrp x10,0x8ac3000
0x4bb3ac4	406944fd	ldr d0,[x10, #0x8d0]
0x4bb3ac8	8ac702d0	adrp x10,0xa4a5000
0x4bb3acc	4aa11c91	add x10,x10,#0x728
0x4bb3ad0	400100fd	str d0,[x10]
0x4bb3ad4	0bca01d0	adrp x11,0x84f5000
0x4bb3ad8	609d45fd	ldr d0,[x11, #0xb38]
0x4bb3adc	400900bd	str s0,[x10, #0x8]
0x4bb3ae0	5f310039	strb wzr,[x10, #0xc]
0x4bb3ae4	2a008052	mov w10,#0x1
0x4bb3ae8	2ad51c39	strb w10,[x9, #0x735]
0x4bb3aec	090040f9	ldr x9,[x0]
0x4bb3af0	1f010071	cmp w8,#0x0
0x4bb3af4	37b1809a	csel x23,x9,x0,lt
0x4bb3af8	80c702d0	adrp x0,0xa4a5000
0x4bb3afc	00a01c91	add x0,x0,#0x728
0x4bb3b00	be379694	bl 0x071419f8
0x4bb3b04	a00100b4	cbz x0,0x04bb3b38
0x4bb3b08	f30300aa	mov x19,x0
0x4bb3b0c	f802168b	add x24,x23,x22
0x4bb3b10	df0200eb	cmp x22,x0
0x4bb3b14	ea010054	b.ge 0x04bb3b50
0x4bb3b18	f60318aa	mov x22,x24
0x4bb3b1c	c80217cb	sub x8,x22,x23
0x4bb3b20	df0218eb	cmp x22,x24
0x4bb3b24	041941ba	ccmn x8,#0x1,#0x4,ne
0x4bb3b28	e0079f1a	cset w0,ne
0x4bb3b2c	04000014	b 0x04bb3b3c
0x4bb3b30	00008052	mov w0,#0x0
0x4bb3b34	02000014	b 0x04bb3b3c
0x4bb3b38	20008052	mov w0,#0x1
0x4bb3b3c	fd7b43a9	ldp x29,x30,[sp, #0x30]
0x4bb3b40	f44f42a9	ldp x20,x19,[sp, #0x20]
0x4bb3b44	f65741a9	ldp x22,x21,[sp, #0x10]
0x4bb3b48	f85fc4a8	ldp x24,x23,[sp], #0x40
0x4bb3b4c	c0035fd6	ret
0x4bb3b50	88c702d0	adrp x8,0xa4a5000
0x4bb3b54	14a1dc39	ldrsb w20,[x8, #0x728]
0x4bb3b58	95c702d0	adrp x21,0xa4a5000
0x4bb3b5c	b5a21c91	add x21,x21,#0x728
0x4bb3b60	e00317aa	mov x0,x23
0x4bb3b64	c80213cb	sub x8,x22,x19
0x4bb3b68	020500b1	adds x2,x8,#0x1
0x4bb3b6c	62fdff54	b.cs 0x04bb3b18
0x4bb3b70	e10314aa	mov x1,x20
0x4bb3b74	bf349694	bl 0x07140e70
0x4bb3b78	00fdffb4	cbz x0,0x04bb3b18
0x4bb3b7c	f60300aa	mov x22,x0
0x4bb3b80	e10315aa	mov x1,x21
0x4bb3b84	e20313aa	mov x2,x19
0x4bb3b88	bd349694	bl 0x07140e7c
0x4bb3b8c	80fcff34	cbz w0,0x04bb3b1c
0x4bb3b90	c0060091	add x0,x22,#0x1
0x4bb3b94	160300cb	sub x22,x24,x0
0x4bb3b98	df0213eb	cmp x22,x19
0x4bb3b9c	4afeff54	b.ge 0x04bb3b64
0x4bb3ba0	deffff17	b 0x04bb3b18
