0x2ebf038	ffc300d1	sub sp,sp,#0x30
0x2ebf03c	f44f01a9	stp x20,x19,[sp, #0x10]
0x2ebf040	fd7b02a9	stp x29,x30,[sp, #0x20]
0x2ebf044	fd830091	add x29,sp,#0x20
0x2ebf048	f30300aa	mov x19,x0
0x2ebf04c	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x2ebf050	c87803f0	adrp x8,0x9dda000
0x2ebf054	08612e91	add x8,x8,#0xb98
0x2ebf058	080000f9	str x8,[x0]
0x2ebf05c	292040a9	ldp x9,x8,[x1]
0x2ebf060	e92300a9	stp x9,x8,[sp]
0x2ebf064	880000b4	cbz x8,0x02ebf074
0x2ebf068	08210091	add x8,x8,#0x8
0x2ebf06c	29008052	mov w9,#0x1
0x2ebf070	080129f8	ldadd x9,x8,[x8]
0x2ebf074	60620091	add x0,x19,#0x18
0x2ebf078	e1030091	mov x1,sp
0x2ebf07c	22008052	mov w2,#0x1
0x2ebf080	f7ca0894	bl 0x030f1c5c
0x2ebf084	f40740f9	ldr x20,[sp, #0x8]
0x2ebf088	740100b4	cbz x20,0x02ebf0b4
0x2ebf08c	88220091	add x8,x20,#0x8
0x2ebf090	09008092	mov x9,#-0x1
0x2ebf094	0801e9f8	ldaddal x9,x8,[x8]
0x2ebf098	e80000b5	cbnz x8,0x02ebf0b4
0x2ebf09c	880240f9	ldr x8,[x20]
0x2ebf0a0	080940f9	ldr x8,[x8, #0x10]
0x2ebf0a4	e00314aa	mov x0,x20
0x2ebf0a8	00013fd6	blr x8
0x2ebf0ac	e00314aa	mov x0,x20
0x2ebf0b0	db020a95	bl 0x0713fc1c
0x2ebf0b4	e00313aa	mov x0,x19
0x2ebf0b8	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x2ebf0bc	f44f41a9	ldp x20,x19,[sp, #0x10]
0x2ebf0c0	ffc30091	add sp,sp,#0x30
0x2ebf0c4	c0035fd6	ret
