0x4bb4dc0	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4bb4dc4	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4bb4dc8	fd430091	add x29,sp,#0x10
0x4bb4dcc	f30300aa	mov x19,x0
0x4bb4dd0	2b000094	bl 0x04bb4e7c
0x4bb4dd4	685e4039	ldrb w8,[x19, #0x17]
0x4bb4dd8	091d0013	sxtb w9,w8
0x4bb4ddc	620640f9	ldr x2,[x19, #0x8]
0x4bb4de0	3f010071	cmp w9,#0x0
0x4bb4de4	4ab0889a	csel x10,x2,x8,lt
0x4bb4de8	8bc702b0	adrp x11,0xa4a5000
0x4bb4dec	6b210a91	add x11,x11,#0x288
0x4bb4df0	6c3d4039	ldrb w12,[x11, #0xf]
0x4bb4df4	891d0013	sxtb w9,w12
0x4bb4df8	6b0140f9	ldr x11,[x11]
0x4bb4dfc	3f010071	cmp w9,#0x0
0x4bb4e00	6bb18c9a	csel x11,x11,x12,lt
0x4bb4e04	5f010beb	cmp x10,x11
0x4bb4e08	41020054	b.ne 0x04bb4e50
0x4bb4e0c	8ac702b0	adrp x10,0xa4a5000
0x4bb4e10	4a010a91	add x10,x10,#0x280
0x4bb4e14	4b0140f9	ldr x11,[x10]
0x4bb4e18	3f010071	cmp w9,#0x0
0x4bb4e1c	61b18a9a	csel x1,x11,x10,lt
0x4bb4e20	c8013837	tbnz w8,#0x7,0x04bb4e58
0x4bb4e24	48020034	cbz w8,0x04bb4e6c
0x4bb4e28	080500d1	sub x8,x8,#0x1
0x4bb4e2c	6a164038	ldrb w10,[x19], #0x1
0x4bb4e30	2b144038	ldrb w11,[x1], #0x1
0x4bb4e34	080500f1	subs x8,x8,#0x1
0x4bb4e38	e9379f1a	cset w9,cs
0x4bb4e3c	5f010b6b	cmp w10,w11
0x4bb4e40	e0179f1a	cset w0,eq
0x4bb4e44	61010054	b.ne 0x04bb4e70
0x4bb4e48	29ff0737	tbnz w9,#0x0,0x04bb4e2c
0x4bb4e4c	09000014	b 0x04bb4e70
0x4bb4e50	00008052	mov w0,#0x0
0x4bb4e54	07000014	b 0x04bb4e70
0x4bb4e58	600240f9	ldr x0,[x19]
0x4bb4e5c	08309694	bl 0x07140e7c
0x4bb4e60	1f000071	cmp w0,#0x0
0x4bb4e64	e0179f1a	cset w0,eq
0x4bb4e68	02000014	b 0x04bb4e70
0x4bb4e6c	20008052	mov w0,#0x1
0x4bb4e70	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4bb4e74	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4bb4e78	c0035fd6	ret
