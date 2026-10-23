0x4bb6cd4	f85fbca9	stp x24,x23,[sp, #-0x40]!
0x4bb6cd8	f65701a9	stp x22,x21,[sp, #0x10]
0x4bb6cdc	f44f02a9	stp x20,x19,[sp, #0x20]
0x4bb6ce0	fd7b03a9	stp x29,x30,[sp, #0x30]
0x4bb6ce4	fdc30091	add x29,sp,#0x30
0x4bb6ce8	095c4039	ldrb w9,[x0, #0x17]
0x4bb6cec	281d0013	sxtb w8,w9
0x4bb6cf0	0a0440f9	ldr x10,[x0, #0x8]
0x4bb6cf4	1f010071	cmp w8,#0x0
0x4bb6cf8	56b1899a	csel x22,x10,x9,lt
0x4bb6cfc	760300b4	cbz x22,0x04bb6d68
0x4bb6d00	69c702f0	adrp x9,0xa4a5000
0x4bb6d04	2a816039	ldrb w10,[x9, #0x820]
0x4bb6d08	ea000037	tbnz w10,#0x0,0x04bb6d24
0x4bb6d0c	0af60190	adrp x10,0x8a76000
0x4bb6d10	40a540fd	ldr d0,[x10, #0x148]
0x4bb6d14	6ac702f0	adrp x10,0xa4a5000
0x4bb6d18	400d04fd	str d0,[x10, #0x818]
0x4bb6d1c	2a008052	mov w10,#0x1
0x4bb6d20	2a812039	strb w10,[x9, #0x820]
0x4bb6d24	090040f9	ldr x9,[x0]
0x4bb6d28	1f010071	cmp w8,#0x0
0x4bb6d2c	37b1809a	csel x23,x9,x0,lt
0x4bb6d30	60c702f0	adrp x0,0xa4a5000
0x4bb6d34	00602091	add x0,x0,#0x818
0x4bb6d38	302b9694	bl 0x071419f8
0x4bb6d3c	a00100b4	cbz x0,0x04bb6d70
0x4bb6d40	f30300aa	mov x19,x0
0x4bb6d44	f802168b	add x24,x23,x22
0x4bb6d48	df0200eb	cmp x22,x0
0x4bb6d4c	ea010054	b.ge 0x04bb6d88
0x4bb6d50	f60318aa	mov x22,x24
0x4bb6d54	c80217cb	sub x8,x22,x23
0x4bb6d58	df0218eb	cmp x22,x24
0x4bb6d5c	041941ba	ccmn x8,#0x1,#0x4,ne
0x4bb6d60	e0079f1a	cset w0,ne
0x4bb6d64	04000014	b 0x04bb6d74
0x4bb6d68	00008052	mov w0,#0x0
0x4bb6d6c	02000014	b 0x04bb6d74
0x4bb6d70	20008052	mov w0,#0x1
0x4bb6d74	fd7b43a9	ldp x29,x30,[sp, #0x30]
0x4bb6d78	f44f42a9	ldp x20,x19,[sp, #0x20]
0x4bb6d7c	f65741a9	ldp x22,x21,[sp, #0x10]
0x4bb6d80	f85fc4a8	ldp x24,x23,[sp], #0x40
0x4bb6d84	c0035fd6	ret
0x4bb6d88	68c702f0	adrp x8,0xa4a5000
0x4bb6d8c	1461e039	ldrsb w20,[x8, #0x818]
0x4bb6d90	75c702f0	adrp x21,0xa4a5000
0x4bb6d94	b5622091	add x21,x21,#0x818
0x4bb6d98	e00317aa	mov x0,x23
0x4bb6d9c	c80213cb	sub x8,x22,x19
0x4bb6da0	020500b1	adds x2,x8,#0x1
0x4bb6da4	62fdff54	b.cs 0x04bb6d50
0x4bb6da8	e10314aa	mov x1,x20
0x4bb6dac	31289694	bl 0x07140e70
0x4bb6db0	00fdffb4	cbz x0,0x04bb6d50
0x4bb6db4	f60300aa	mov x22,x0
0x4bb6db8	e10315aa	mov x1,x21
0x4bb6dbc	e20313aa	mov x2,x19
0x4bb6dc0	2f289694	bl 0x07140e7c
0x4bb6dc4	80fcff34	cbz w0,0x04bb6d54
0x4bb6dc8	c0060091	add x0,x22,#0x1
0x4bb6dcc	160300cb	sub x22,x24,x0
0x4bb6dd0	df0213eb	cmp x22,x19
0x4bb6dd4	4afeff54	b.ge 0x04bb6d9c
0x4bb6dd8	deffff17	b 0x04bb6d50
