0x466aca8	ffc300d1	sub sp,sp,#0x30
0x466acac	f44f01a9	stp x20,x19,[sp, #0x10]
0x466acb0	fd7b02a9	stp x29,x30,[sp, #0x20]
0x466acb4	fd830091	add x29,sp,#0x20
0x466acb8	f30308aa	mov x19,x8
0x466acbc	88ef02f0	adrp x8,0xa45d000
0x466acc0	009d47f9	ldr x0,[x8, #0xf38]
0x466acc4	080040f9	ldr x8,[x0]
0x466acc8	093540f9	ldr x9,[x8, #0x68]
0x466accc	e8030091	mov x8,sp
0x466acd0	20013fd6	blr x9
0x466acd4	e92340a9	ldp x9,x8,[sp]
0x466acd8	692200a9	stp x9,x8,[x19]
0x466acdc	080200b4	cbz x8,0x0466ad1c
0x466ace0	08210091	add x8,x8,#0x8
0x466ace4	29008052	mov w9,#0x1
0x466ace8	080129f8	ldadd x9,x8,[x8]
0x466acec	f30740f9	ldr x19,[sp, #0x8]
0x466acf0	730100b4	cbz x19,0x0466ad1c
0x466acf4	68220091	add x8,x19,#0x8
0x466acf8	09008092	mov x9,#-0x1
0x466acfc	0801e9f8	ldaddal x9,x8,[x8]
0x466ad00	e80000b5	cbnz x8,0x0466ad1c
0x466ad04	680240f9	ldr x8,[x19]
0x466ad08	080940f9	ldr x8,[x8, #0x10]
0x466ad0c	e00313aa	mov x0,x19
0x466ad10	00013fd6	blr x8
0x466ad14	e00313aa	mov x0,x19
0x466ad18	c153ab94	bl 0x0713fc1c
0x466ad1c	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x466ad20	f44f41a9	ldp x20,x19,[sp, #0x10]
0x466ad24	ffc30091	add sp,sp,#0x30
0x466ad28	c0035fd6	ret
