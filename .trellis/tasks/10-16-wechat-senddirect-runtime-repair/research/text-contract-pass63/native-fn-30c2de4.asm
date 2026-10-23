0x30c2de4	f657bda9	stp x22,x21,[sp, #-0x30]!
0x30c2de8	f44f01a9	stp x20,x19,[sp, #0x10]
0x30c2dec	fd7b02a9	stp x29,x30,[sp, #0x20]
0x30c2df0	fd830091	add x29,sp,#0x20
0x30c2df4	f40301aa	mov x20,x1
0x30c2df8	f30300aa	mov x19,x0
0x30c2dfc	1f1000b9	str wzr,[x0, #0x10]
0x30c2e00	f50300aa	mov x21,x0
0x30c2e04	bf8e01f8	str xzr,[x21, #0x18]!
0x30c2e08	1f7c02a9	stp xzr,xzr,[x0, #0x20]
0x30c2e0c	2820a052	mov w8,#0x1010000
0x30c2e10	083000b9	str w8,[x0, #0x30]
0x30c2e14	1f7c04a9	stp xzr,xzr,[x0, #0x40]
0x30c2e18	1f1c00f9	str xzr,[x0, #0x38]
0x30c2e1c	1f3400f9	str xzr,[x0, #0x68]
0x30c2e20	1fc00139	strb wzr,[x0, #0x70]
0x30c2e24	1f7400b9	str wzr,[x0, #0x74]
0x30c2e28	286903d0	adrp x8,0x9de8000
0x30c2e2c	08a10991	add x8,x8,#0x268
0x30c2e30	08fc87a8	stp x8,xzr,[x0], #0x78
0x30c2e34	de635694	bl 0x0465bdac
0x30c2e38	60a20291	add x0,x19,#0xa8
0x30c2e3c	e4635694	bl 0x0465bdcc
0x30c2e40	881240b9	ldr w8,[x20, #0x10]
0x30c2e44	680e00b9	str w8,[x19, #0xc]
0x30c2e48	81620091	add x1,x20,#0x18
0x30c2e4c	e00315aa	mov x0,x21
0x30c2e50	a4f20195	bl 0x0713f8e0
0x30c2e54	880e40b9	ldr w8,[x20, #0xc]
0x30c2e58	1f010071	cmp w8,#0x0
0x30c2e5c	e8079f1a	cset w8,ne
0x30c2e60	68c60039	strb w8,[x19, #0x31]
0x30c2e64	88c24039	ldrb w8,[x20, #0x30]
0x30c2e68	68ce0039	strb w8,[x19, #0x33]
0x30c2e6c	28008052	mov w8,#0x1
0x30c2e70	681200b9	str w8,[x19, #0x10]
0x30c2e74	e00313aa	mov x0,x19
0x30c2e78	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x30c2e7c	f44f41a9	ldp x20,x19,[sp, #0x10]
0x30c2e80	f657c3a8	ldp x22,x21,[sp], #0x30
0x30c2e84	c0035fd6	ret
