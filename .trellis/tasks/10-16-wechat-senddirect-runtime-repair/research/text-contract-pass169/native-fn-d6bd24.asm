0xd6bd24	f44fbea9	stp x20,x19,[sp, #-0x20]!
0xd6bd28	fd7b01a9	stp x29,x30,[sp, #0x10]
0xd6bd2c	fd430091	add x29,sp,#0x10
0xd6bd30	f40308aa	mov x20,x8
0xd6bd34	00be8052	mov w0,#0x5f0
0xd6bd38	be508f95	bl 0x07140030
0xd6bd3c	f30300aa	mov x19,x0
0xd6bd40	29000094	bl 0x00d6bde4
0xd6bd44	686200b1	adds x8,x19,#0x18
0xd6bd48	884e00a9	stp x8,x19,[x20]
0xd6bd4c	80020054	b.eq 0x00d6bd9c
0xd6bd50	601640f9	ldr x0,[x19, #0x28]
0xd6bd54	800000b4	cbz x0,0x00d6bd64
0xd6bd58	090440f9	ldr x9,[x0, #0x8]
0xd6bd5c	3f0500b1	cmn x9,#0x1
0xd6bd60	e1010054	b.ne 0x00d6bd9c
0xd6bd64	d30000b4	cbz x19,0x00d6bd7c
0xd6bd68	69220091	add x9,x19,#0x8
0xd6bd6c	2a008052	mov w10,#0x1
0xd6bd70	29012af8	ldadd x10,x9,[x9]
0xd6bd74	69420091	add x9,x19,#0x10
0xd6bd78	29012af8	ldadd x10,x9,[x9]
0xd6bd7c	684e02a9	stp x8,x19,[x19, #0x20]
0xd6bd80	400000b4	cbz x0,0x00d6bd88
0xd6bd84	a64f8f95	bl 0x0713fc1c
0xd6bd88	b30000b4	cbz x19,0x00d6bd9c
0xd6bd8c	68220091	add x8,x19,#0x8
0xd6bd90	09008092	mov x9,#-0x1
0xd6bd94	0801e9f8	ldaddal x9,x8,[x8]
0xd6bd98	880000b4	cbz x8,0x00d6bda8
0xd6bd9c	fd7b41a9	ldp x29,x30,[sp, #0x10]
0xd6bda0	f44fc2a8	ldp x20,x19,[sp], #0x20
0xd6bda4	c0035fd6	ret
0xd6bda8	680240f9	ldr x8,[x19]
0xd6bdac	080940f9	ldr x8,[x8, #0x10]
0xd6bdb0	e00313aa	mov x0,x19
0xd6bdb4	00013fd6	blr x8
0xd6bdb8	e00313aa	mov x0,x19
0xd6bdbc	fd7b41a9	ldp x29,x30,[sp, #0x10]
0xd6bdc0	f44fc2a8	ldp x20,x19,[sp], #0x20
0xd6bdc4	964f8f15	b 0x0713fc1c
