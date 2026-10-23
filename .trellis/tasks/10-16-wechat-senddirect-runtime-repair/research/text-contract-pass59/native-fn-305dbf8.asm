0x305dbf8	f657bda9	stp x22,x21,[sp, #-0x30]!
0x305dbfc	f44f01a9	stp x20,x19,[sp, #0x10]
0x305dc00	fd7b02a9	stp x29,x30,[sp, #0x20]
0x305dc04	fd830091	add x29,sp,#0x20
0x305dc08	f40301aa	mov x20,x1
0x305dc0c	f30300aa	mov x19,x0
0x305dc10	1f1000b9	str wzr,[x0, #0x10]
0x305dc14	f50300aa	mov x21,x0
0x305dc18	bf8e01f8	str xzr,[x21, #0x18]!
0x305dc1c	1f7c02a9	stp xzr,xzr,[x0, #0x20]
0x305dc20	2820a052	mov w8,#0x1010000
0x305dc24	083000b9	str w8,[x0, #0x30]
0x305dc28	1f7c04a9	stp xzr,xzr,[x0, #0x40]
0x305dc2c	1f1c00f9	str xzr,[x0, #0x38]
0x305dc30	1f3400f9	str xzr,[x0, #0x68]
0x305dc34	1fc00139	strb wzr,[x0, #0x70]
0x305dc38	1f7400b9	str wzr,[x0, #0x74]
0x305dc3c	486c0390	adrp x8,0x9de5000
0x305dc40	08812191	add x8,x8,#0x860
0x305dc44	08fc87a8	stp x8,xzr,[x0], #0x78
0x305dc48	2b468294	bl 0x050ef4f4
0x305dc4c	60620391	add x0,x19,#0xd8
0x305dc50	37468294	bl 0x050ef52c
0x305dc54	881240b9	ldr w8,[x20, #0x10]
0x305dc58	680e00b9	str w8,[x19, #0xc]
0x305dc5c	81620091	add x1,x20,#0x18
0x305dc60	e00315aa	mov x0,x21
0x305dc64	1f870395	bl 0x0713f8e0
0x305dc68	880e40b9	ldr w8,[x20, #0xc]
0x305dc6c	1f010071	cmp w8,#0x0
0x305dc70	e8079f1a	cset w8,ne
0x305dc74	68c60039	strb w8,[x19, #0x31]
0x305dc78	88c24039	ldrb w8,[x20, #0x30]
0x305dc7c	68ce0039	strb w8,[x19, #0x33]
0x305dc80	28008052	mov w8,#0x1
0x305dc84	681200b9	str w8,[x19, #0x10]
0x305dc88	e00313aa	mov x0,x19
0x305dc8c	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x305dc90	f44f41a9	ldp x20,x19,[sp, #0x10]
0x305dc94	f657c3a8	ldp x22,x21,[sp], #0x30
0x305dc98	c0035fd6	ret
