0x2ab8f80	f657bda9	stp x22,x21,[sp, #-0x30]!
0x2ab8f84	f44f01a9	stp x20,x19,[sp, #0x10]
0x2ab8f88	fd7b02a9	stp x29,x30,[sp, #0x20]
0x2ab8f8c	fd830091	add x29,sp,#0x20
0x2ab8f90	f50300aa	mov x21,x0
0x2ab8f94	f40308aa	mov x20,x8
0x2ab8f98	007f8052	mov w0,#0x3f8
0x2ab8f9c	251c1a95	bl 0x07140030
0x2ab8fa0	f30300aa	mov x19,x0
0x2ab8fa4	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x2ab8fa8	a89703f0	adrp x8,0x9daf000
0x2ab8fac	08412d91	add x8,x8,#0xb50
0x2ab8fb0	088401f8	str x8,[x0], #0x18
0x2ab8fb4	e10315aa	mov x1,x21
0x2ab8fb8	15e4e197	bl 0x0233200c
0x2ab8fbc	804e00a9	stp x0,x19,[x20]
0x2ab8fc0	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x2ab8fc4	f44f41a9	ldp x20,x19,[sp, #0x10]
0x2ab8fc8	f657c3a8	ldp x22,x21,[sp], #0x30
0x2ab8fcc	c0035fd6	ret
