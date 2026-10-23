0x462d99c	ff0301d1	sub sp,sp,#0x40
0x462d9a0	f44f02a9	stp x20,x19,[sp, #0x20]
0x462d9a4	fd7b03a9	stp x29,x30,[sp, #0x30]
0x462d9a8	fdc30091	add x29,sp,#0x30
0x462d9ac	e00301aa	mov x0,x1
0x462d9b0	ffff00a9	stp xzr,xzr,[sp, #0x8]
0x462d9b4	ff0f00f9	str xzr,[sp, #0x18]
0x462d9b8	e1230091	add x1,sp,#0x8
0x462d9bc	cc1d5a94	bl 0x05cb50ec
0x462d9c0	e87fc039	ldrsb w8,[sp, #0x1f]
0x462d9c4	0801f836	tbz w8,#0x1f,0x0462d9e4
0x462d9c8	e80740f9	ldr x8,[sp, #0x8]
0x462d9cc	e90f40f9	ldr x9,[sp, #0x18]
0x462d9d0	21f94092	and x1,x9,#0x7fffffffffffffff
0x462d9d4	f30300aa	mov x19,x0
0x462d9d8	e00308aa	mov x0,x8
0x462d9dc	8c49ac94	bl 0x0714000c
0x462d9e0	e00313aa	mov x0,x19
0x462d9e4	fd7b43a9	ldp x29,x30,[sp, #0x30]
0x462d9e8	f44f42a9	ldp x20,x19,[sp, #0x20]
0x462d9ec	ff030191	add sp,sp,#0x40
0x462d9f0	c0035fd6	ret
