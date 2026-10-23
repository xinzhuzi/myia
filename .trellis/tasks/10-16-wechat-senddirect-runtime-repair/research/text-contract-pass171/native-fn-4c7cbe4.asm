0x4c7cba8	ffc301d1	sub sp,sp,#0x70
0x4c7cbac	f65704a9	stp x22,x21,[sp, #0x40]
0x4c7cbb0	f44f05a9	stp x20,x19,[sp, #0x50]
0x4c7cbb4	fd7b06a9	stp x29,x30,[sp, #0x60]
0x4c7cbb8	fd830191	add x29,sp,#0x60
0x4c7cbbc	f50301aa	mov x21,x1
0x4c7cbc0	f40300aa	mov x20,x0
0x4c7cbc4	f30308aa	mov x19,x8
0x4c7cbc8	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x4c7cbcc	e82302a9	stp x8,x8,[sp, #0x20]
0x4c7cbd0	e8830091	add x8,sp,#0x20
0x4c7cbd4	a08700d1	sub x0,x29,#0x21
0x4c7cbd8	7efceb96	bl 0x0077bdd0
0x4c7cbdc	e81340f9	ldr x8,[sp, #0x20]
0x4c7cbe0	29008052	mov w9,#0x1
0x4c7cbe4	09e500b9	str w9,[x8, #0xe4]
0x4c7cbe8	a90240f9	ldr x9,[x21]
0x4c7cbec	00211791	add x0,x8,#0x5c8
0x4c7cbf0	21210591	add x1,x9,#0x148
0x4c7cbf4	3b0b9394	bl 0x0713f8e0
0x4c7cbf8	a92240a9	ldp x9,x8,[x21]
0x4c7cbfc	e92301a9	stp x9,x8,[sp, #0x10]
0x4c7cc00	880000b4	cbz x8,0x04c7cc10
0x4c7cc04	08210091	add x8,x8,#0x8
0x4c7cc08	29008052	mov w9,#0x1
0x4c7cc0c	080129f8	ldadd x9,x8,[x8]
0x4c7cc10	e92342a9	ldp x9,x8,[sp, #0x20]
0x4c7cc14	e92300a9	stp x9,x8,[sp]
0x4c7cc18	880000b4	cbz x8,0x04c7cc28
0x4c7cc1c	08210091	add x8,x8,#0x8
0x4c7cc20	29008052	mov w9,#0x1
0x4c7cc24	080129f8	ldadd x9,x8,[x8]
0x4c7cc28	e1430091	add x1,sp,#0x10
0x4c7cc2c	e2030091	mov x2,sp
0x4c7cc30	e00314aa	mov x0,x20
0x4c7cc34	67beff97	bl 0x04c6c5d0
0x4c7cc38	f40740f9	ldr x20,[sp, #0x8]
0x4c7cc3c	740100b4	cbz x20,0x04c7cc68
0x4c7cc40	88220091	add x8,x20,#0x8
0x4c7cc44	09008092	mov x9,#-0x1
0x4c7cc48	0801e9f8	ldaddal x9,x8,[x8]
0x4c7cc4c	e80000b5	cbnz x8,0x04c7cc68
0x4c7cc50	880240f9	ldr x8,[x20]
0x4c7cc54	080940f9	ldr x8,[x8, #0x10]
0x4c7cc58	e00314aa	mov x0,x20
0x4c7cc5c	00013fd6	blr x8
0x4c7cc60	e00314aa	mov x0,x20
0x4c7cc64	ee0b9394	bl 0x0713fc1c
0x4c7cc68	f40f40f9	ldr x20,[sp, #0x18]
0x4c7cc6c	740100b4	cbz x20,0x04c7cc98
0x4c7cc70	88220091	add x8,x20,#0x8
0x4c7cc74	09008092	mov x9,#-0x1
0x4c7cc78	0801e9f8	ldaddal x9,x8,[x8]
0x4c7cc7c	e80000b5	cbnz x8,0x04c7cc98
0x4c7cc80	880240f9	ldr x8,[x20]
0x4c7cc84	080940f9	ldr x8,[x8, #0x10]
0x4c7cc88	e00314aa	mov x0,x20
0x4c7cc8c	00013fd6	blr x8
0x4c7cc90	e00314aa	mov x0,x20
0x4c7cc94	e20b9394	bl 0x0713fc1c
0x4c7cc98	e00bc03d	ldr q0,[sp, #0x20]
0x4c7cc9c	6002803d	str q0,[x19]
0x4c7cca0	fd7b46a9	ldp x29,x30,[sp, #0x60]
0x4c7cca4	f44f45a9	ldp x20,x19,[sp, #0x50]
0x4c7cca8	f65744a9	ldp x22,x21,[sp, #0x40]
0x4c7ccac	ffc30191	add sp,sp,#0x70
0x4c7ccb0	c0035fd6	ret
