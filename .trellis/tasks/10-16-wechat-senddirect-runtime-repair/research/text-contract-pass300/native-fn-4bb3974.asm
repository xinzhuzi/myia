0x4bb3974	f85fbca9	stp x24,x23,[sp, #-0x40]!
0x4bb3978	f65701a9	stp x22,x21,[sp, #0x10]
0x4bb397c	f44f02a9	stp x20,x19,[sp, #0x20]
0x4bb3980	fd7b03a9	stp x29,x30,[sp, #0x30]
0x4bb3984	fdc30091	add x29,sp,#0x30
0x4bb3988	095c4039	ldrb w9,[x0, #0x17]
0x4bb398c	281d0013	sxtb w8,w9
0x4bb3990	0a0440f9	ldr x10,[x0, #0x8]
0x4bb3994	1f010071	cmp w8,#0x0
0x4bb3998	56b1899a	csel x22,x10,x9,lt
0x4bb399c	d60300b4	cbz x22,0x04bb3a14
0x4bb39a0	89c702d0	adrp x9,0xa4a5000
0x4bb39a4	2a295b39	ldrb w10,[x9, #0x6ca]
0x4bb39a8	4a010037	tbnz w10,#0x0,0x04bb39d0
0x4bb39ac	8ac702d0	adrp x10,0xa4a5000
0x4bb39b0	4a011b91	add x10,x10,#0x6c0
0x4bb39b4	8bca01d0	adrp x11,0x8505000
0x4bb39b8	60d940fd	ldr d0,[x11, #0x1b0]
0x4bb39bc	400100fd	str d0,[x10]
0x4bb39c0	ab0d8052	mov w11,#0x6d
0x4bb39c4	4b110079	strh w11,[x10, #0x8]
0x4bb39c8	2a008052	mov w10,#0x1
0x4bb39cc	2a291b39	strb w10,[x9, #0x6ca]
0x4bb39d0	090040f9	ldr x9,[x0]
0x4bb39d4	1f010071	cmp w8,#0x0
0x4bb39d8	37b1809a	csel x23,x9,x0,lt
0x4bb39dc	80c702d0	adrp x0,0xa4a5000
0x4bb39e0	00001b91	add x0,x0,#0x6c0
0x4bb39e4	05389694	bl 0x071419f8
0x4bb39e8	a00100b4	cbz x0,0x04bb3a1c
0x4bb39ec	f30300aa	mov x19,x0
0x4bb39f0	f802168b	add x24,x23,x22
0x4bb39f4	df0200eb	cmp x22,x0
0x4bb39f8	ea010054	b.ge 0x04bb3a34
0x4bb39fc	f60318aa	mov x22,x24
0x4bb3a00	c80217cb	sub x8,x22,x23
0x4bb3a04	df0218eb	cmp x22,x24
0x4bb3a08	041941ba	ccmn x8,#0x1,#0x4,ne
0x4bb3a0c	e0079f1a	cset w0,ne
0x4bb3a10	04000014	b 0x04bb3a20
0x4bb3a14	00008052	mov w0,#0x0
0x4bb3a18	02000014	b 0x04bb3a20
0x4bb3a1c	20008052	mov w0,#0x1
0x4bb3a20	fd7b43a9	ldp x29,x30,[sp, #0x30]
0x4bb3a24	f44f42a9	ldp x20,x19,[sp, #0x20]
0x4bb3a28	f65741a9	ldp x22,x21,[sp, #0x10]
0x4bb3a2c	f85fc4a8	ldp x24,x23,[sp], #0x40
0x4bb3a30	c0035fd6	ret
0x4bb3a34	88c702d0	adrp x8,0xa4a5000
0x4bb3a38	1401db39	ldrsb w20,[x8, #0x6c0]
0x4bb3a3c	95c702d0	adrp x21,0xa4a5000
0x4bb3a40	b5021b91	add x21,x21,#0x6c0
0x4bb3a44	e00317aa	mov x0,x23
0x4bb3a48	c80213cb	sub x8,x22,x19
0x4bb3a4c	020500b1	adds x2,x8,#0x1
0x4bb3a50	62fdff54	b.cs 0x04bb39fc
0x4bb3a54	e10314aa	mov x1,x20
0x4bb3a58	06359694	bl 0x07140e70
0x4bb3a5c	00fdffb4	cbz x0,0x04bb39fc
0x4bb3a60	f60300aa	mov x22,x0
0x4bb3a64	e10315aa	mov x1,x21
0x4bb3a68	e20313aa	mov x2,x19
0x4bb3a6c	04359694	bl 0x07140e7c
0x4bb3a70	80fcff34	cbz w0,0x04bb3a00
0x4bb3a74	c0060091	add x0,x22,#0x1
0x4bb3a78	160300cb	sub x22,x24,x0
0x4bb3a7c	df0213eb	cmp x22,x19
0x4bb3a80	4afeff54	b.ge 0x04bb3a48
0x4bb3a84	deffff17	b 0x04bb39fc
