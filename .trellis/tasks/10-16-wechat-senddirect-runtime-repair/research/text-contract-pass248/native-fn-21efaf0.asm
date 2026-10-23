0x21efaf0	f657bda9	stp x22,x21,[sp, #-0x30]!
0x21efaf4	f44f01a9	stp x20,x19,[sp, #0x10]
0x21efaf8	fd7b02a9	stp x29,x30,[sp, #0x20]
0x21efafc	fd830091	add x29,sp,#0x20
0x21efb00	f40308aa	mov x20,x8
0x21efb04	001f8052	mov w0,#0xf8
0x21efb08	4a413d95	bl 0x07140030
0x21efb0c	f30300aa	mov x19,x0
0x21efb10	f50300aa	mov x21,x0
0x21efb14	bf8e00f8	str xzr,[x21, #0x8]!
0x21efb18	1f0800f9	str xzr,[x0, #0x10]
0x21efb1c	a8dc03d0	adrp x8,0x9d85000
0x21efb20	08211f91	add x8,x8,#0x7c8
0x21efb24	088401f8	str x8,[x0], #0x18
0x21efb28	c1e31195	bl 0x06668a2c
0x21efb2c	804e00a9	stp x0,x19,[x20]
0x21efb30	800200b4	cbz x0,0x021efb80
0x21efb34	601240f9	ldr x0,[x19, #0x20]
0x21efb38	800000b4	cbz x0,0x021efb48
0x21efb3c	080440f9	ldr x8,[x0, #0x8]
0x21efb40	1f0500b1	cmn x8,#0x1
0x21efb44	e1010054	b.ne 0x021efb80
0x21efb48	d30000b4	cbz x19,0x021efb60
0x21efb4c	68220091	add x8,x19,#0x8
0x21efb50	29008052	mov w9,#0x1
0x21efb54	080129f8	ldadd x9,x8,[x8]
0x21efb58	68420091	add x8,x19,#0x10
0x21efb5c	080129f8	ldadd x9,x8,[x8]
0x21efb60	68620091	add x8,x19,#0x18
0x21efb64	68ce01a9	stp x8,x19,[x19, #0x18]
0x21efb68	400000b4	cbz x0,0x021efb70
0x21efb6c	2c403d95	bl 0x0713fc1c
0x21efb70	930000b4	cbz x19,0x021efb80
0x21efb74	08008092	mov x8,#-0x1
0x21efb78	a802e8f8	ldaddal x8,x8,[x21]
0x21efb7c	a80000b4	cbz x8,0x021efb90
0x21efb80	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x21efb84	f44f41a9	ldp x20,x19,[sp, #0x10]
0x21efb88	f657c3a8	ldp x22,x21,[sp], #0x30
0x21efb8c	c0035fd6	ret
0x21efb90	680240f9	ldr x8,[x19]
0x21efb94	080940f9	ldr x8,[x8, #0x10]
0x21efb98	e00313aa	mov x0,x19
0x21efb9c	00013fd6	blr x8
0x21efba0	e00313aa	mov x0,x19
0x21efba4	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x21efba8	f44f41a9	ldp x20,x19,[sp, #0x10]
0x21efbac	f657c3a8	ldp x22,x21,[sp], #0x30
0x21efbb0	1b403d15	b 0x0713fc1c
