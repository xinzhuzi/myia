0x4cbfbbc	f657bda9	stp x22,x21,[sp, #-0x30]!
0x4cbfbc0	f44f01a9	stp x20,x19,[sp, #0x10]
0x4cbfbc4	fd7b02a9	stp x29,x30,[sp, #0x20]
0x4cbfbc8	fd830091	add x29,sp,#0x20
0x4cbfbcc	f50300aa	mov x21,x0
0x4cbfbd0	f40308aa	mov x20,x8
0x4cbfbd4	00528052	mov w0,#0x290
0x4cbfbd8	16019294	bl 0x07140030
0x4cbfbdc	f30300aa	mov x19,x0
0x4cbfbe0	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x4cbfbe4	887e02f0	adrp x8,0x9c92000
0x4cbfbe8	08410e91	add x8,x8,#0x390
0x4cbfbec	088401f8	str x8,[x0], #0x18
0x4cbfbf0	e10315aa	mov x1,x21
0x4cbfbf4	8f5e0a97	bl 0x00f57630
0x4cbfbf8	804e00a9	stp x0,x19,[x20]
0x4cbfbfc	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x4cbfc00	f44f41a9	ldp x20,x19,[sp, #0x10]
0x4cbfc04	f657c3a8	ldp x22,x21,[sp], #0x30
0x4cbfc08	c0035fd6	ret
