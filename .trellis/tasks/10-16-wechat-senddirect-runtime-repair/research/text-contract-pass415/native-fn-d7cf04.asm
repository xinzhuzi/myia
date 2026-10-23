0xd7cf04	ff0302d1	sub sp,sp,#0x80
0xd7cf08	fc6f02a9	stp x28,x27,[sp, #0x20]
0xd7cf0c	fa6703a9	stp x26,x25,[sp, #0x30]
0xd7cf10	f85f04a9	stp x24,x23,[sp, #0x40]
0xd7cf14	f65705a9	stp x22,x21,[sp, #0x50]
0xd7cf18	f44f06a9	stp x20,x19,[sp, #0x60]
0xd7cf1c	fd7b07a9	stp x29,x30,[sp, #0x70]
0xd7cf20	fdc30191	add x29,sp,#0x70
0xd7cf24	f40300aa	mov x20,x0
0xd7cf28	f30308aa	mov x19,x8
0xd7cf2c	40e5054f	movi v0.16B,#0xaa
0xd7cf30	000100ad	stp q0,q0,[x8]
0xd7cf34	e8f301b2	orr x8,xzr,#-0x5555555555555556
0xd7cf38	7fa201a9	stp xzr,x8,[x19, #0x18]
0xd7cf3c	7f020039	strb wzr,[x19]
0xd7cf40	f50313aa	mov x21,x19
0xd7cf44	bf8e00f8	str xzr,[x21, #0x8]!
0xd7cf48	00e4006f	movi v0.2D,#0x0
0xd7cf4c	f60313aa	mov x22,x19
0xd7cf50	c08e823c	str q0,[x22, #0x28]!
0xd7cf54	7f0a00f9	str xzr,[x19, #0x10]
0xd7cf58	7f2200b9	str wzr,[x19, #0x20]
0xd7cf5c	6082833c	stur q0,[x19, #0x38]
0xd7cf60	6082843c	stur q0,[x19, #0x48]
0xd7cf64	6082853c	stur q0,[x19, #0x58]
0xd7cf68	6082863c	stur q0,[x19, #0x68]
0xd7cf6c	6082873c	stur q0,[x19, #0x78]
0xd7cf70	6082883c	stur q0,[x19, #0x88]
0xd7cf74	6082893c	stur q0,[x19, #0x98]
0xd7cf78	60828a3c	stur q0,[x19, #0xa8]
0xd7cf7c	60828b3c	stur q0,[x19, #0xb8]
0xd7cf80	7f6600f9	str xzr,[x19, #0xc8]
0xd7cf84	000040f9	ldr x0,[x0]
0xd7cf88	5177ca97	bl 0x0001accc
0xd7cf8c	e10300aa	mov x1,x0
0xd7cf90	e00316aa	mov x0,x22
0xd7cf94	530a8f95	bl 0x0713f8e0
0xd7cf98	800240f9	ldr x0,[x20]
0xd7cf9c	27810c94	bl 0x0109d438
0xd7cfa0	e10300aa	mov x1,x0
0xd7cfa4	60020191	add x0,x19,#0x40
0xd7cfa8	4e0a8f95	bl 0x0713f8e0
0xd7cfac	800240f9	ldr x0,[x20]
0xd7cfb0	000b0a94	bl 0x00fffbb0
0xd7cfb4	e10300aa	mov x1,x0
0xd7cfb8	e00315aa	mov x0,x21
0xd7cfbc	490a8f95	bl 0x0713f8e0
0xd7cfc0	800240f9	ldr x0,[x20]
0xd7cfc4	68f6d797	bl 0x0037a964
0xd7cfc8	085c4039	ldrb w8,[x0, #0x17]
0xd7cfcc	091d0013	sxtb w9,w8
0xd7cfd0	0a0440f9	ldr x10,[x0, #0x8]
0xd7cfd4	3f010071	cmp w9,#0x0
0xd7cfd8	48b1889a	csel x8,x10,x8,lt
0xd7cfdc	c80000b4	cbz x8,0x00d7cff4
0xd7cfe0	800240f9	ldr x0,[x20]
0xd7cfe4	60f6d797	bl 0x0037a964
0xd7cfe8	01008052	mov w1,#0x0
0xd7cfec	d765f794	bl 0x04b56748
0xd7cff0	602200b9	str w0,[x19, #0x20]
0xd7cff4	800240f9	ldr x0,[x20]
0xd7cff8	e678fe94	bl 0x04d1b390
0xd7cffc	085c4039	ldrb w8,[x0, #0x17]
0xd7d000	091d0013	sxtb w9,w8
0xd7d004	0a0440f9	ldr x10,[x0, #0x8]
0xd7d008	3f010071	cmp w9,#0x0
0xd7d00c	48b1889a	csel x8,x10,x8,lt
0xd7d010	a80900b4	cbz x8,0x00d7d144
0xd7d014	800240f9	ldr x0,[x20]
0xd7d018	de78fe94	bl 0x04d1b390
0xd7d01c	f50300aa	mov x21,x0
0xd7d020	48aa04d0	adrp x8,0xa2c7000
0xd7d024	09696739	ldrb w9,[x8, #0x9da]
0xd7d028	e9000037	tbnz w9,#0x0,0x00d7d044
0xd7d02c	49aa04d0	adrp x9,0xa2c7000
0xd7d030	29612791	add x9,x9,#0x9d8
0xd7d034	0a048052	mov w10,#0x20
0xd7d038	2a010079	strh w10,[x9]
0xd7d03c	29008052	mov w9,#0x1
0xd7d040	09692739	strb w9,[x8, #0x9da]
0xd7d044	a85e4039	ldrb w8,[x21, #0x17]
0xd7d048	1a1d0013	sxtb w26,w8
0xd7d04c	a90640f9	ldr x9,[x21, #0x8]
0xd7d050	5f030071	cmp w26,#0x0
0xd7d054	37b1889a	csel x23,x9,x8,lt
0xd7d058	40aa04d0	adrp x0,0xa2c7000
0xd7d05c	00602791	add x0,x0,#0x9d8
0xd7d060	66128f95	bl 0x071419f8
0xd7d064	e8f301b2	orr x8,xzr,#-0x5555555555555556
0xd7d068	e8a300a9	stp x8,x8,[sp, #0x8]
0xd7d06c	e80f00f9	str x8,[sp, #0x18]
0xd7d070	e8ef7db2	orr x8,xzr,#0x7ffffffffffffff8
0xd7d074	fb02008b	add x27,x23,x0
0xd7d078	7f0308eb	cmp x27,x8
0xd7d07c	220c0054	b.cs 0x00d7d200
0xd7d080	f60300aa	mov x22,x0
0xd7d084	7f5b00f1	cmp x27,#0x16
0xd7d088	a9010054	b.ls 0x00d7d0bc
0xd7d08c	680b40b2	orr x8,x27,#0x7
0xd7d090	1f5d00f1	cmp x8,#0x17
0xd7d094	29038052	mov w9,#0x19
0xd7d098	3905889a	csinc x25,x9,x8,eq
0xd7d09c	e00319aa	mov x0,x25
0xd7d0a0	e40b8f95	bl 0x07140030
0xd7d0a4	f80300aa	mov x24,x0
0xd7d0a8	280341b2	orr x8,x25,#-0x8000000000000000
0xd7d0ac	fb2301a9	stp x27,x8,[sp, #0x10]
0xd7d0b0	e00700f9	str x0,[sp, #0x8]
0xd7d0b4	f70000b5	cbnz x23,0x00d7d0d0
0xd7d0b8	0c000014	b 0x00d7d0e8
0xd7d0bc	ff7f01a9	stp xzr,xzr,[sp, #0x10]
0xd7d0c0	ff0700f9	str xzr,[sp, #0x8]
0xd7d0c4	f8230091	add x24,sp,#0x8
0xd7d0c8	fb7f0039	strb w27,[sp, #0x1f]
0xd7d0cc	f70000b4	cbz x23,0x00d7d0e8
0xd7d0d0	a80240f9	ldr x8,[x21]
0xd7d0d4	5f030071	cmp w26,#0x0
0xd7d0d8	01b1959a	csel x1,x8,x21,lt
0xd7d0dc	e00318aa	mov x0,x24
0xd7d0e0	e20317aa	mov x2,x23
0xd7d0e4	6c0f8f95	bl 0x07140e94
0xd7d0e8	1503178b	add x21,x24,x23
0xd7d0ec	d60000b4	cbz x22,0x00d7d104
0xd7d0f0	41aa04d0	adrp x1,0xa2c7000
0xd7d0f4	21602791	add x1,x1,#0x9d8
0xd7d0f8	e00315aa	mov x0,x21
0xd7d0fc	e20316aa	mov x2,x22
0xd7d100	650f8f95	bl 0x07140e94
0xd7d104	bf6a3638	strb wzr,[x21, x22]
0xd7d108	e87f4039	ldrb w8,[sp, #0x1f]
0xd7d10c	091d0013	sxtb w9,w8
0xd7d110	eaaf40a9	ldp x10,x11,[sp, #0x8]
0xd7d114	3f010071	cmp w9,#0x0
0xd7d118	e9230091	add x9,sp,#0x8
0xd7d11c	41b1899a	csel x1,x10,x9,lt
0xd7d120	62b1889a	csel x2,x11,x8,lt
0xd7d124	60620191	add x0,x19,#0x58
0xd7d128	af098f95	bl 0x0713f7e4
0xd7d12c	e87fc039	ldrsb w8,[sp, #0x1f]
0xd7d130	a800f836	tbz w8,#0x1f,0x00d7d144
0xd7d134	e00740f9	ldr x0,[sp, #0x8]
0xd7d138	e80f40f9	ldr x8,[sp, #0x18]
0xd7d13c	01f94092	and x1,x8,#0x7fffffffffffffff
0xd7d140	b30b8f95	bl 0x0714000c
0xd7d144	800240f9	ldr x0,[x20]
0xd7d148	d0358294	bl 0x02e0a888
0xd7d14c	085c4039	ldrb w8,[x0, #0x17]
0xd7d150	091d0013	sxtb w9,w8
0xd7d154	0a0440f9	ldr x10,[x0, #0x8]
0xd7d158	3f010071	cmp w9,#0x0
0xd7d15c	48b1889a	csel x8,x10,x8,lt
0xd7d160	680100b4	cbz x8,0x00d7d18c
0xd7d164	800240f9	ldr x0,[x20]
0xd7d168	c8358294	bl 0x02e0a888
0xd7d16c	085c4039	ldrb w8,[x0, #0x17]
0xd7d170	091d0013	sxtb w9,w8
0xd7d174	0a2c40a9	ldp x10,x11,[x0]
0xd7d178	3f010071	cmp w9,#0x0
0xd7d17c	41b1809a	csel x1,x10,x0,lt
0xd7d180	62b1889a	csel x2,x11,x8,lt
0xd7d184	60620191	add x0,x19,#0x58
0xd7d188	97098f95	bl 0x0713f7e4
0xd7d18c	800240f9	ldr x0,[x20]
0xd7d190	d778fe94	bl 0x04d1b4ec
0xd7d194	1f080071	cmp w0,#0x2
0xd7d198	41020054	b.ne 0x00d7d1e0
0xd7d19c	28008052	mov w8,#0x1
0xd7d1a0	68020039	strb w8,[x19]
0xd7d1a4	800240f9	ldr x0,[x20]
0xd7d1a8	cfc51594	bl 0x012ee8e4
0xd7d1ac	e10300aa	mov x1,x0
0xd7d1b0	60c20191	add x0,x19,#0x70
0xd7d1b4	cb098f95	bl 0x0713f8e0
0xd7d1b8	800240f9	ldr x0,[x20]
0xd7d1bc	031e2394	bl 0x016449c8
0xd7d1c0	e10300aa	mov x1,x0
0xd7d1c4	60220291	add x0,x19,#0x88
0xd7d1c8	c6098f95	bl 0x0713f8e0
0xd7d1cc	800240f9	ldr x0,[x20]
0xd7d1d0	8878fe94	bl 0x04d1b3f0
0xd7d1d4	e10300aa	mov x1,x0
0xd7d1d8	60820291	add x0,x19,#0xa0
0xd7d1dc	c1098f95	bl 0x0713f8e0
0xd7d1e0	fd7b47a9	ldp x29,x30,[sp, #0x70]
0xd7d1e4	f44f46a9	ldp x20,x19,[sp, #0x60]
0xd7d1e8	f65745a9	ldp x22,x21,[sp, #0x50]
0xd7d1ec	f85f44a9	ldp x24,x23,[sp, #0x40]
0xd7d1f0	fa6743a9	ldp x26,x25,[sp, #0x30]
0xd7d1f4	fc6f42a9	ldp x28,x27,[sp, #0x20]
0xd7d1f8	ff030291	add sp,sp,#0x80
0xd7d1fc	c0035fd6	ret
0xd7d200	e0230091	add x0,sp,#0x8
0xd7d204	e66eca97	bl 0x00018d9c
