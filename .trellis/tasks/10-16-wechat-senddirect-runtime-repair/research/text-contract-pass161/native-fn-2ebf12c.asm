0x2ebf12c	ffc300d1	sub sp,sp,#0x30
0x2ebf130	f44f01a9	stp x20,x19,[sp, #0x10]
0x2ebf134	fd7b02a9	stp x29,x30,[sp, #0x20]
0x2ebf138	fd830091	add x29,sp,#0x20
0x2ebf13c	f30300aa	mov x19,x0
0x2ebf140	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x2ebf144	c87803f0	adrp x8,0x9dda000
0x2ebf148	08612e91	add x8,x8,#0xb98
0x2ebf14c	080000f9	str x8,[x0]
0x2ebf150	292040a9	ldp x9,x8,[x1]
0x2ebf154	e92300a9	stp x9,x8,[sp]
0x2ebf158	880000b4	cbz x8,0x02ebf168
0x2ebf15c	08210091	add x8,x8,#0x8
0x2ebf160	29008052	mov w9,#0x1
0x2ebf164	080129f8	ldadd x9,x8,[x8]
0x2ebf168	60620091	add x0,x19,#0x18
0x2ebf16c	e1030091	mov x1,sp
0x2ebf170	22008052	mov w2,#0x1
0x2ebf174	baca0894	bl 0x030f1c5c
0x2ebf178	f40740f9	ldr x20,[sp, #0x8]
0x2ebf17c	740100b4	cbz x20,0x02ebf1a8
0x2ebf180	88220091	add x8,x20,#0x8
0x2ebf184	09008092	mov x9,#-0x1
0x2ebf188	0801e9f8	ldaddal x9,x8,[x8]
0x2ebf18c	e80000b5	cbnz x8,0x02ebf1a8
0x2ebf190	880240f9	ldr x8,[x20]
0x2ebf194	080940f9	ldr x8,[x8, #0x10]
0x2ebf198	e00314aa	mov x0,x20
0x2ebf19c	00013fd6	blr x8
0x2ebf1a0	e00314aa	mov x0,x20
0x2ebf1a4	9e020a95	bl 0x0713fc1c
0x2ebf1a8	e00313aa	mov x0,x19
0x2ebf1ac	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x2ebf1b0	f44f41a9	ldp x20,x19,[sp, #0x10]
0x2ebf1b4	ffc30091	add sp,sp,#0x30
0x2ebf1b8	c0035fd6	ret
