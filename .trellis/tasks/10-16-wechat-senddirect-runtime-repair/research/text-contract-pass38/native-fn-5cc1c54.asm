0x5cc1c54	ffc300d1	sub sp,sp,#0x30
0x5cc1c58	f44f01a9	stp x20,x19,[sp, #0x10]
0x5cc1c5c	fd7b02a9	stp x29,x30,[sp, #0x20]
0x5cc1c60	fd830091	add x29,sp,#0x20
0x5cc1c64	f30301aa	mov x19,x1
0x5cc1c68	f40300aa	mov x20,x0
0x5cc1c6c	e10300f9	str x1,[sp]
0x5cc1c70	00048052	mov w0,#0x20
0x5cc1c74	eff85194	bl 0x07140030
0x5cc1c78	281402b0	adrp x8,0x9f46000
0x5cc1c7c	08210491	add x8,x8,#0x108
0x5cc1c80	08410091	add x8,x8,#0x10
0x5cc1c84	087c00a9	stp x8,xzr,[x0]
0x5cc1c88	1f4c01a9	stp xzr,x19,[x0, #0x10]
0x5cc1c8c	e00700f9	str x0,[sp, #0x8]
0x5cc1c90	80420091	add x0,x20,#0x10
0x5cc1c94	e1030091	mov x1,sp
0x5cc1c98	e182f297	bl 0x0596281c
0x5cc1c9c	f30740f9	ldr x19,[sp, #0x8]
0x5cc1ca0	730100b4	cbz x19,0x05cc1ccc
0x5cc1ca4	68220091	add x8,x19,#0x8
0x5cc1ca8	09008092	mov x9,#-0x1
0x5cc1cac	0801e9f8	ldaddal x9,x8,[x8]
0x5cc1cb0	e80000b5	cbnz x8,0x05cc1ccc
0x5cc1cb4	680240f9	ldr x8,[x19]
0x5cc1cb8	080940f9	ldr x8,[x8, #0x10]
0x5cc1cbc	e00313aa	mov x0,x19
0x5cc1cc0	00013fd6	blr x8
0x5cc1cc4	e00313aa	mov x0,x19
0x5cc1cc8	d5f75194	bl 0x0713fc1c
0x5cc1ccc	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x5cc1cd0	f44f41a9	ldp x20,x19,[sp, #0x10]
0x5cc1cd4	ffc30091	add sp,sp,#0x30
0x5cc1cd8	c0035fd6	ret
