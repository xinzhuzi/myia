0x4bb5f30	085c4039	ldrb w8,[x0, #0x17]
0x4bb5f34	091d0013	sxtb w9,w8
0x4bb5f38	0a0440f9	ldr x10,[x0, #0x8]
0x4bb5f3c	3f010071	cmp w9,#0x0
0x4bb5f40	48b1889a	csel x8,x10,x8,lt
0x4bb5f44	880400b4	cbz x8,0x04bb5fd4
0x4bb5f48	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4bb5f4c	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4bb5f50	fd430091	add x29,sp,#0x10
0x4bb5f54	f30300aa	mov x19,x0
0x4bb5f58	07ceea97	bl 0x04669774
0x4bb5f5c	080040f9	ldr x8,[x0]
0x4bb5f60	081540f9	ldr x8,[x8, #0x28]
0x4bb5f64	00013fd6	blr x8
0x4bb5f68	685e4039	ldrb w8,[x19, #0x17]
0x4bb5f6c	091d0013	sxtb w9,w8
0x4bb5f70	620640f9	ldr x2,[x19, #0x8]
0x4bb5f74	3f010071	cmp w9,#0x0
0x4bb5f78	4ab0889a	csel x10,x2,x8,lt
0x4bb5f7c	0b5c4039	ldrb w11,[x0, #0x17]
0x4bb5f80	691d0013	sxtb w9,w11
0x4bb5f84	0c0440f9	ldr x12,[x0, #0x8]
0x4bb5f88	3f010071	cmp w9,#0x0
0x4bb5f8c	8bb18b9a	csel x11,x12,x11,lt
0x4bb5f90	5f010beb	cmp x10,x11
0x4bb5f94	41020054	b.ne 0x04bb5fdc
0x4bb5f98	0a0040f9	ldr x10,[x0]
0x4bb5f9c	3f010071	cmp w9,#0x0
0x4bb5fa0	41b1809a	csel x1,x10,x0,lt
0x4bb5fa4	08023837	tbnz w8,#0x7,0x04bb5fe4
0x4bb5fa8	88020034	cbz w8,0x04bb5ff8
0x4bb5fac	080500d1	sub x8,x8,#0x1
0x4bb5fb0	6a164038	ldrb w10,[x19], #0x1
0x4bb5fb4	2b144038	ldrb w11,[x1], #0x1
0x4bb5fb8	080500f1	subs x8,x8,#0x1
0x4bb5fbc	e9379f1a	cset w9,cs
0x4bb5fc0	5f010b6b	cmp w10,w11
0x4bb5fc4	e0179f1a	cset w0,eq
0x4bb5fc8	a1010054	b.ne 0x04bb5ffc
0x4bb5fcc	29ff0737	tbnz w9,#0x0,0x04bb5fb0
0x4bb5fd0	0b000014	b 0x04bb5ffc
0x4bb5fd4	00008052	mov w0,#0x0
0x4bb5fd8	c0035fd6	ret
0x4bb5fdc	00008052	mov w0,#0x0
0x4bb5fe0	07000014	b 0x04bb5ffc
0x4bb5fe4	600240f9	ldr x0,[x19]
0x4bb5fe8	a52b9694	bl 0x07140e7c
0x4bb5fec	1f000071	cmp w0,#0x0
0x4bb5ff0	e0179f1a	cset w0,eq
0x4bb5ff4	02000014	b 0x04bb5ffc
0x4bb5ff8	20008052	mov w0,#0x1
0x4bb5ffc	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4bb6000	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4bb6004	c0035fd6	ret
