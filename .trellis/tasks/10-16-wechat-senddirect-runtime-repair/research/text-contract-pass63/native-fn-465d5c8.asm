0x465d5c8	f657bda9	stp x22,x21,[sp, #-0x30]!
0x465d5cc	f44f01a9	stp x20,x19,[sp, #0x10]
0x465d5d0	fd7b02a9	stp x29,x30,[sp, #0x20]
0x465d5d4	fd830091	add x29,sp,#0x20
0x465d5d8	f30300aa	mov x19,x0
0x465d5dc	f40300aa	mov x20,x0
0x465d5e0	9f8e00f8	str xzr,[x20, #0x8]!
0x465d5e4	a8c10290	adrp x8,0x9e91000
0x465d5e8	08e13791	add x8,x8,#0xdf8
0x465d5ec	080000f9	str x8,[x0]
0x465d5f0	1f0800f9	str xzr,[x0, #0x10]
0x465d5f4	1f1800b9	str wzr,[x0, #0x18]
0x465d5f8	1f1000f9	str xzr,[x0, #0x20]
0x465d5fc	1f2800b9	str wzr,[x0, #0x28]
0x465d600	8bffff97	bl 0x0465d42c
0x465d604	e00313aa	mov x0,x19
0x465d608	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x465d60c	f44f41a9	ldp x20,x19,[sp, #0x10]
0x465d610	f657c3a8	ldp x22,x21,[sp], #0x30
0x465d614	c0035fd6	ret
