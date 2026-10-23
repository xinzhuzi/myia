0x462fa2c	ff8301d1	sub sp,sp,#0x60
0x462fa30	f85f02a9	stp x24,x23,[sp, #0x20]
0x462fa34	f65703a9	stp x22,x21,[sp, #0x30]
0x462fa38	f44f04a9	stp x20,x19,[sp, #0x40]
0x462fa3c	fd7b05a9	stp x29,x30,[sp, #0x50]
0x462fa40	fd430191	add x29,sp,#0x50
0x462fa44	f30300aa	mov x19,x0
0x462fa48	e8c702f0	adrp x8,0x9f2e000
0x462fa4c	08011091	add x8,x8,#0x400
0x462fa50	170540f9	ldr x23,[x8, #0x8]
0x462fa54	e0fa4092	and x0,x23,#0x7fffffffffffffff
0x462fa58	e847ac94	bl 0x071419f8
0x462fa5c	e8ef7db2	orr x8,xzr,#0x7ffffffffffffff8
0x462fa60	1f0008eb	cmp x0,x8
0x462fa64	c2040054	b.cs 0x0462fafc
0x462fa68	f40300aa	mov x20,x0
0x462fa6c	1f5c00f1	cmp x0,#0x17
0x462fa70	a2000054	b.cs 0x0462fa84
0x462fa74	f47f0039	strb w20,[sp, #0x1f]
0x462fa78	f5230091	add x21,sp,#0x8
0x462fa7c	940100b5	cbnz x20,0x0462faac
0x462fa80	0f000014	b 0x0462fabc
0x462fa84	880a40b2	orr x8,x20,#0x7
0x462fa88	1f5d00f1	cmp x8,#0x17
0x462fa8c	29038052	mov w9,#0x19
0x462fa90	3605889a	csinc x22,x9,x8,eq
0x462fa94	e00316aa	mov x0,x22
0x462fa98	6641ac94	bl 0x07140030
0x462fa9c	f50300aa	mov x21,x0
0x462faa0	c80241b2	orr x8,x22,#-0x8000000000000000
0x462faa4	f42301a9	stp x20,x8,[sp, #0x10]
0x462faa8	e00700f9	str x0,[sp, #0x8]
0x462faac	e1fa4092	and x1,x23,#0x7fffffffffffffff
0x462fab0	e00315aa	mov x0,x21
0x462fab4	e20314aa	mov x2,x20
0x462fab8	f744ac94	bl 0x07140e94
0x462fabc	bf6a3438	strb wzr,[x21, x20]
0x462fac0	e1230091	add x1,sp,#0x8
0x462fac4	e00313aa	mov x0,x19
0x462fac8	2c494c94	bl 0x05941f78
0x462facc	e87fc039	ldrsb w8,[sp, #0x1f]
0x462fad0	a800f836	tbz w8,#0x1f,0x0462fae4
0x462fad4	e00740f9	ldr x0,[sp, #0x8]
0x462fad8	e80f40f9	ldr x8,[sp, #0x18]
0x462fadc	01f94092	and x1,x8,#0x7fffffffffffffff
0x462fae0	4b41ac94	bl 0x0714000c
0x462fae4	fd7b45a9	ldp x29,x30,[sp, #0x50]
0x462fae8	f44f44a9	ldp x20,x19,[sp, #0x40]
0x462faec	f65743a9	ldp x22,x21,[sp, #0x30]
0x462faf0	f85f42a9	ldp x24,x23,[sp, #0x20]
0x462faf4	ff830191	add sp,sp,#0x60
0x462faf8	c0035fd6	ret
0x462fafc	e0230091	add x0,sp,#0x8
0x462fb00	a7a4e796	bl 0x00018d9c
