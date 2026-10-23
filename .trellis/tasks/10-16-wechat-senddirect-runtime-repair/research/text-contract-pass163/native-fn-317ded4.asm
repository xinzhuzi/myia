0x317ded4	ffc300d1	sub sp,sp,#0x30
0x317ded8	f44f01a9	stp x20,x19,[sp, #0x10]
0x317dedc	fd7b02a9	stp x29,x30,[sp, #0x20]
0x317dee0	fd830091	add x29,sp,#0x20
0x317dee4	294c40a9	ldp x9,x19,[x1]
0x317dee8	e94f00a9	stp x9,x19,[sp]
0x317deec	930000b4	cbz x19,0x0317defc
0x317def0	69220091	add x9,x19,#0x8
0x317def4	2a008052	mov w10,#0x1
0x317def8	29012af8	ldadd x10,x9,[x9]
0x317defc	e1030091	mov x1,sp
0x317df00	22008052	mov w2,#0x1
0x317df04	18000094	bl 0x0317df64
0x317df08	b30000b4	cbz x19,0x0317df1c
0x317df0c	68220091	add x8,x19,#0x8
0x317df10	09008092	mov x9,#-0x1
0x317df14	0801e9f8	ldaddal x9,x8,[x8]
0x317df18	a80000b4	cbz x8,0x0317df2c
0x317df1c	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x317df20	f44f41a9	ldp x20,x19,[sp, #0x10]
0x317df24	ffc30091	add sp,sp,#0x30
0x317df28	c0035fd6	ret
0x317df2c	680240f9	ldr x8,[x19]
0x317df30	080940f9	ldr x8,[x8, #0x10]
0x317df34	e00313aa	mov x0,x19
0x317df38	00013fd6	blr x8
0x317df3c	e00313aa	mov x0,x19
0x317df40	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x317df44	f44f41a9	ldp x20,x19,[sp, #0x10]
0x317df48	ffc30091	add sp,sp,#0x30
0x317df4c	3407ff14	b 0x0713fc1c
