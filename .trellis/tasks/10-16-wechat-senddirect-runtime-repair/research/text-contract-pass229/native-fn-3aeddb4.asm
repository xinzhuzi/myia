0x3aeddb4	ff4301d1	sub sp,sp,#0x50
0x3aeddb8	f44f03a9	stp x20,x19,[sp, #0x30]
0x3aeddbc	fd7b04a9	stp x29,x30,[sp, #0x40]
0x3aeddc0	fd030191	add x29,sp,#0x40
0x3aeddc4	e80300aa	mov x8,x0
0x3aeddc8	490203b0	adrp x9,0x9b36000
0x3aeddcc	294d46f9	ldr x9,[x9, #0xc98]
0x3aeddd0	290140f9	ldr x9,[x9]
0x3aeddd4	a9831ef8	stur x9,[x29, #-0x18]
0x3aeddd8	200c40f9	ldr x0,[x1, #0x18]
0x3aedddc	200100b4	cbz x0,0x03aede00
0x3aedde0	130540f9	ldr x19,[x8, #0x8]
0x3aedde4	1f0001eb	cmp x0,x1
0x3aedde8	00010054	b.eq 0x03aede08
0x3aeddec	080040f9	ldr x8,[x0]
0x3aeddf0	080940f9	ldr x8,[x8, #0x10]
0x3aeddf4	00013fd6	blr x8
0x3aeddf8	e01300f9	str x0,[sp, #0x20]
0x3aeddfc	09000014	b 0x03aede20
0x3aede00	20008052	mov w0,#0x1
0x3aede04	18000014	b 0x03aede64
0x3aede08	e8230091	add x8,sp,#0x8
0x3aede0c	e81300f9	str x8,[sp, #0x20]
0x3aede10	080040f9	ldr x8,[x0]
0x3aede14	080d40f9	ldr x8,[x8, #0x18]
0x3aede18	e1230091	add x1,sp,#0x8
0x3aede1c	00013fd6	blr x8
0x3aede20	f4230091	add x20,sp,#0x8
0x3aede24	e1230091	add x1,sp,#0x8
0x3aede28	e00313aa	mov x0,x19
0x3aede2c	c0187094	bl 0x056f412c
0x3aede30	e81340f9	ldr x8,[sp, #0x20]
0x3aede34	1f0114eb	cmp x8,x20
0x3aede38	a0000054	b.eq 0x03aede4c
0x3aede3c	480100b4	cbz x8,0x03aede64
0x3aede40	090140f9	ldr x9,[x8]
0x3aede44	291540f9	ldr x9,[x9, #0x28]
0x3aede48	03000014	b 0x03aede54
0x3aede4c	090140f9	ldr x9,[x8]
0x3aede50	291140f9	ldr x9,[x9, #0x20]
0x3aede54	f30300aa	mov x19,x0
0x3aede58	e00308aa	mov x0,x8
0x3aede5c	20013fd6	blr x9
0x3aede60	e00313aa	mov x0,x19
0x3aede64	a8835ef8	ldur x8,[x29, #-0x18]
0x3aede68	490203b0	adrp x9,0x9b36000
0x3aede6c	294d46f9	ldr x9,[x9, #0xc98]
0x3aede70	290140f9	ldr x9,[x9]
0x3aede74	3f0108eb	cmp x9,x8
0x3aede78	a1000054	b.ne 0x03aede8c
0x3aede7c	fd7b44a9	ldp x29,x30,[sp, #0x40]
0x3aede80	f44f43a9	ldp x20,x19,[sp, #0x30]
0x3aede84	ff430191	add sp,sp,#0x50
0x3aede88	c0035fd6	ret
0x3aede8c	c648d994	bl 0x071401a4
