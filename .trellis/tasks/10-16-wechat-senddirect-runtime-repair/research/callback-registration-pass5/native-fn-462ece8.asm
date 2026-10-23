0x462ece8	ff8301d1	sub sp,sp,#0x60
0x462ecec	f85f02a9	stp x24,x23,[sp, #0x20]
0x462ecf0	f65703a9	stp x22,x21,[sp, #0x30]
0x462ecf4	f44f04a9	stp x20,x19,[sp, #0x40]
0x462ecf8	fd7b05a9	stp x29,x30,[sp, #0x50]
0x462ecfc	fd430191	add x29,sp,#0x50
0x462ed00	f30301aa	mov x19,x1
0x462ed04	f40300aa	mov x20,x0
0x462ed08	08c80290	adrp x8,0x9f2e000
0x462ed0c	08011091	add x8,x8,#0x400
0x462ed10	180540f9	ldr x24,[x8, #0x8]
0x462ed14	00fb4092	and x0,x24,#0x7fffffffffffffff
0x462ed18	384bac94	bl 0x071419f8
0x462ed1c	e8ef7db2	orr x8,xzr,#0x7ffffffffffffff8
0x462ed20	1f0008eb	cmp x0,x8
0x462ed24	e2040054	b.cs 0x0462edc0
0x462ed28	f50300aa	mov x21,x0
0x462ed2c	1f5c00f1	cmp x0,#0x17
0x462ed30	a2000054	b.cs 0x0462ed44
0x462ed34	f57f0039	strb w21,[sp, #0x1f]
0x462ed38	f6230091	add x22,sp,#0x8
0x462ed3c	950100b5	cbnz x21,0x0462ed6c
0x462ed40	0f000014	b 0x0462ed7c
0x462ed44	a80a40b2	orr x8,x21,#0x7
0x462ed48	1f5d00f1	cmp x8,#0x17
0x462ed4c	29038052	mov w9,#0x19
0x462ed50	3705889a	csinc x23,x9,x8,eq
0x462ed54	e00317aa	mov x0,x23
0x462ed58	b644ac94	bl 0x07140030
0x462ed5c	f60300aa	mov x22,x0
0x462ed60	e80241b2	orr x8,x23,#-0x8000000000000000
0x462ed64	f52301a9	stp x21,x8,[sp, #0x10]
0x462ed68	e00700f9	str x0,[sp, #0x8]
0x462ed6c	01fb4092	and x1,x24,#0x7fffffffffffffff
0x462ed70	e00316aa	mov x0,x22
0x462ed74	e20315aa	mov x2,x21
0x462ed78	4748ac94	bl 0x07140e94
0x462ed7c	df6a3538	strb wzr,[x22, x21]
0x462ed80	e2230091	add x2,sp,#0x8
0x462ed84	e00314aa	mov x0,x20
0x462ed88	e10313aa	mov x1,x19
0x462ed8c	474c4c94	bl 0x05941ea8
0x462ed90	e87fc039	ldrsb w8,[sp, #0x1f]
0x462ed94	a800f836	tbz w8,#0x1f,0x0462eda8
0x462ed98	e00740f9	ldr x0,[sp, #0x8]
0x462ed9c	e80f40f9	ldr x8,[sp, #0x18]
0x462eda0	01f94092	and x1,x8,#0x7fffffffffffffff
0x462eda4	9a44ac94	bl 0x0714000c
0x462eda8	fd7b45a9	ldp x29,x30,[sp, #0x50]
0x462edac	f44f44a9	ldp x20,x19,[sp, #0x40]
0x462edb0	f65743a9	ldp x22,x21,[sp, #0x30]
0x462edb4	f85f42a9	ldp x24,x23,[sp, #0x20]
0x462edb8	ff830191	add sp,sp,#0x60
0x462edbc	c0035fd6	ret
0x462edc0	e0230091	add x0,sp,#0x8
0x462edc4	f6a7e796	bl 0x00018d9c
