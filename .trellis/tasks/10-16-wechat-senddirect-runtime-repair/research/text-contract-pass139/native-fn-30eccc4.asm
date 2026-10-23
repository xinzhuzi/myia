0x30eccc4	f657bda9	stp x22,x21,[sp, #-0x30]!
0x30eccc8	f44f01a9	stp x20,x19,[sp, #0x10]
0x30ecccc	fd7b02a9	stp x29,x30,[sp, #0x20]
0x30eccd0	fd830091	add x29,sp,#0x20
0x30eccd4	f50301aa	mov x21,x1
0x30eccd8	f40308aa	mov x20,x8
0x30eccdc	00738052	mov w0,#0x398
0x30ecce0	d44c0195	bl 0x07140030
0x30ecce4	f30300aa	mov x19,x0
0x30ecce8	f60300aa	mov x22,x0
0x30eccec	df8e00f8	str xzr,[x22, #0x8]!
0x30eccf0	1f0800f9	str xzr,[x0, #0x10]
0x30eccf4	e86703b0	adrp x8,0x9de9000
0x30eccf8	08211291	add x8,x8,#0x488
0x30eccfc	088401f8	str x8,[x0], #0x18
0x30ecd00	e10315aa	mov x1,x21
0x30ecd04	d4e1fd97	bl 0x03065454
0x30ecd08	c86703f0	adrp x8,0x9de7000
0x30ecd0c	08613d91	add x8,x8,#0xf58
0x30ecd10	08410091	add x8,x8,#0x10
0x30ecd14	680e00f9	str x8,[x19, #0x18]
0x30ecd18	804e00a9	stp x0,x19,[x20]
0x30ecd1c	800200b4	cbz x0,0x030ecd6c
0x30ecd20	681640f9	ldr x8,[x19, #0x28]
0x30ecd24	880000b4	cbz x8,0x030ecd34
0x30ecd28	090540f9	ldr x9,[x8, #0x8]
0x30ecd2c	3f0500b1	cmn x9,#0x1
0x30ecd30	e1010054	b.ne 0x030ecd6c
0x30ecd34	d30000b4	cbz x19,0x030ecd4c
0x30ecd38	69220091	add x9,x19,#0x8
0x30ecd3c	2a008052	mov w10,#0x1
0x30ecd40	29012af8	ldadd x10,x9,[x9]
0x30ecd44	69420091	add x9,x19,#0x10
0x30ecd48	29012af8	ldadd x10,x9,[x9]
0x30ecd4c	604e02a9	stp x0,x19,[x19, #0x20]
0x30ecd50	680000b4	cbz x8,0x030ecd5c
0x30ecd54	e00308aa	mov x0,x8
0x30ecd58	b14b0195	bl 0x0713fc1c
0x30ecd5c	930000b4	cbz x19,0x030ecd6c
0x30ecd60	08008092	mov x8,#-0x1
0x30ecd64	c802e8f8	ldaddal x8,x8,[x22]
0x30ecd68	a80000b4	cbz x8,0x030ecd7c
0x30ecd6c	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x30ecd70	f44f41a9	ldp x20,x19,[sp, #0x10]
0x30ecd74	f657c3a8	ldp x22,x21,[sp], #0x30
0x30ecd78	c0035fd6	ret
0x30ecd7c	680240f9	ldr x8,[x19]
0x30ecd80	080940f9	ldr x8,[x8, #0x10]
0x30ecd84	e00313aa	mov x0,x19
0x30ecd88	00013fd6	blr x8
0x30ecd8c	e00313aa	mov x0,x19
0x30ecd90	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x30ecd94	f44f41a9	ldp x20,x19,[sp, #0x10]
0x30ecd98	f657c3a8	ldp x22,x21,[sp], #0x30
0x30ecd9c	a04b0115	b 0x0713fc1c
