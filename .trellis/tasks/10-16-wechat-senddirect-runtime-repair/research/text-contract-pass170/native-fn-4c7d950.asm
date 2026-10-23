0x4c7d950	ff0302d1	sub sp,sp,#0x80
0x4c7d954	f85f04a9	stp x24,x23,[sp, #0x40]
0x4c7d958	f65705a9	stp x22,x21,[sp, #0x50]
0x4c7d95c	f44f06a9	stp x20,x19,[sp, #0x60]
0x4c7d960	fd7b07a9	stp x29,x30,[sp, #0x70]
0x4c7d964	fdc30191	add x29,sp,#0x70
0x4c7d968	f50301aa	mov x21,x1
0x4c7d96c	f40300aa	mov x20,x0
0x4c7d970	f30308aa	mov x19,x8
0x4c7d974	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x4c7d978	e82303a9	stp x8,x8,[sp, #0x30]
0x4c7d97c	e8c30091	add x8,sp,#0x30
0x4c7d980	e0830091	add x0,sp,#0x20
0x4c7d984	e8b80397	bl 0x00d6bd24
0x4c7d988	a80240f9	ldr x8,[x21]
0x4c7d98c	168942f9	ldr x22,[x8, #0x510]
0x4c7d990	178d42f9	ldr x23,[x8, #0x518]
0x4c7d994	f65f02a9	stp x22,x23,[sp, #0x20]
0x4c7d998	970000b4	cbz x23,0x04c7d9a8
0x4c7d99c	e8220091	add x8,x23,#0x8
0x4c7d9a0	29008052	mov w9,#0x1
0x4c7d9a4	080129f8	ldadd x9,x8,[x8]
0x4c7d9a8	e00316aa	mov x0,x22
0x4c7d9ac	cec31997	bl 0x012ee8e4
0x4c7d9b0	085c4039	ldrb w8,[x0, #0x17]
0x4c7d9b4	091d0013	sxtb w9,w8
0x4c7d9b8	0a0440f9	ldr x10,[x0, #0x8]
0x4c7d9bc	3f010071	cmp w9,#0x0
0x4c7d9c0	49b1889a	csel x9,x10,x8,lt
0x4c7d9c4	e81b40f9	ldr x8,[sp, #0x30]
0x4c7d9c8	3f0100f1	cmp x9,#0x0
0x4c7d9cc	49088052	mov w9,#0x42
0x4c7d9d0	4a058052	mov w10,#0x2a
0x4c7d9d4	4901891a	csel w9,w10,w9,eq
0x4c7d9d8	09e500b9	str w9,[x8, #0xe4]
0x4c7d9dc	970000b4	cbz x23,0x04c7d9ec
0x4c7d9e0	e9220091	add x9,x23,#0x8
0x4c7d9e4	2a008052	mov w10,#0x1
0x4c7d9e8	29012af8	ldadd x10,x9,[x9]
0x4c7d9ec	16e502f9	str x22,[x8, #0x5c8]
0x4c7d9f0	16e942f9	ldr x22,[x8, #0x5d0]
0x4c7d9f4	17e902f9	str x23,[x8, #0x5d0]
0x4c7d9f8	760100b4	cbz x22,0x04c7da24
0x4c7d9fc	c8220091	add x8,x22,#0x8
0x4c7da00	09008092	mov x9,#-0x1
0x4c7da04	0801e9f8	ldaddal x9,x8,[x8]
0x4c7da08	e80000b5	cbnz x8,0x04c7da24
0x4c7da0c	c80240f9	ldr x8,[x22]
0x4c7da10	080940f9	ldr x8,[x8, #0x10]
0x4c7da14	e00316aa	mov x0,x22
0x4c7da18	00013fd6	blr x8
0x4c7da1c	e00316aa	mov x0,x22
0x4c7da20	7f089394	bl 0x0713fc1c
0x4c7da24	a92240a9	ldp x9,x8,[x21]
0x4c7da28	e92301a9	stp x9,x8,[sp, #0x10]
0x4c7da2c	880000b4	cbz x8,0x04c7da3c
0x4c7da30	08210091	add x8,x8,#0x8
0x4c7da34	29008052	mov w9,#0x1
0x4c7da38	080129f8	ldadd x9,x8,[x8]
0x4c7da3c	e92343a9	ldp x9,x8,[sp, #0x30]
0x4c7da40	e92300a9	stp x9,x8,[sp]
0x4c7da44	880000b4	cbz x8,0x04c7da54
0x4c7da48	08210091	add x8,x8,#0x8
0x4c7da4c	29008052	mov w9,#0x1
0x4c7da50	080129f8	ldadd x9,x8,[x8]
0x4c7da54	e1430091	add x1,sp,#0x10
0x4c7da58	e2030091	mov x2,sp
0x4c7da5c	e00314aa	mov x0,x20
0x4c7da60	dcbaff97	bl 0x04c6c5d0
0x4c7da64	f40740f9	ldr x20,[sp, #0x8]
0x4c7da68	740100b4	cbz x20,0x04c7da94
0x4c7da6c	88220091	add x8,x20,#0x8
0x4c7da70	09008092	mov x9,#-0x1
0x4c7da74	0801e9f8	ldaddal x9,x8,[x8]
0x4c7da78	e80000b5	cbnz x8,0x04c7da94
0x4c7da7c	880240f9	ldr x8,[x20]
0x4c7da80	080940f9	ldr x8,[x8, #0x10]
0x4c7da84	e00314aa	mov x0,x20
0x4c7da88	00013fd6	blr x8
0x4c7da8c	e00314aa	mov x0,x20
0x4c7da90	63089394	bl 0x0713fc1c
0x4c7da94	f40f40f9	ldr x20,[sp, #0x18]
0x4c7da98	740100b4	cbz x20,0x04c7dac4
0x4c7da9c	88220091	add x8,x20,#0x8
0x4c7daa0	09008092	mov x9,#-0x1
0x4c7daa4	0801e9f8	ldaddal x9,x8,[x8]
0x4c7daa8	e80000b5	cbnz x8,0x04c7dac4
0x4c7daac	880240f9	ldr x8,[x20]
0x4c7dab0	080940f9	ldr x8,[x8, #0x10]
0x4c7dab4	e00314aa	mov x0,x20
0x4c7dab8	00013fd6	blr x8
0x4c7dabc	e00314aa	mov x0,x20
0x4c7dac0	57089394	bl 0x0713fc1c
0x4c7dac4	e00fc03d	ldr q0,[sp, #0x30]
0x4c7dac8	6002803d	str q0,[x19]
0x4c7dacc	ff7f03a9	stp xzr,xzr,[sp, #0x30]
0x4c7dad0	f31740f9	ldr x19,[sp, #0x28]
0x4c7dad4	730100b4	cbz x19,0x04c7db00
0x4c7dad8	68220091	add x8,x19,#0x8
0x4c7dadc	09008092	mov x9,#-0x1
0x4c7dae0	0801e9f8	ldaddal x9,x8,[x8]
0x4c7dae4	e80000b5	cbnz x8,0x04c7db00
0x4c7dae8	680240f9	ldr x8,[x19]
0x4c7daec	080940f9	ldr x8,[x8, #0x10]
0x4c7daf0	e00313aa	mov x0,x19
0x4c7daf4	00013fd6	blr x8
0x4c7daf8	e00313aa	mov x0,x19
0x4c7dafc	48089394	bl 0x0713fc1c
0x4c7db00	f31f40f9	ldr x19,[sp, #0x38]
0x4c7db04	730100b4	cbz x19,0x04c7db30
0x4c7db08	68220091	add x8,x19,#0x8
0x4c7db0c	09008092	mov x9,#-0x1
0x4c7db10	0801e9f8	ldaddal x9,x8,[x8]
0x4c7db14	e80000b5	cbnz x8,0x04c7db30
0x4c7db18	680240f9	ldr x8,[x19]
0x4c7db1c	080940f9	ldr x8,[x8, #0x10]
0x4c7db20	e00313aa	mov x0,x19
0x4c7db24	00013fd6	blr x8
0x4c7db28	e00313aa	mov x0,x19
0x4c7db2c	3c089394	bl 0x0713fc1c
0x4c7db30	fd7b47a9	ldp x29,x30,[sp, #0x70]
0x4c7db34	f44f46a9	ldp x20,x19,[sp, #0x60]
0x4c7db38	f65745a9	ldp x22,x21,[sp, #0x50]
0x4c7db3c	f85f44a9	ldp x24,x23,[sp, #0x40]
0x4c7db40	ff030291	add sp,sp,#0x80
0x4c7db44	c0035fd6	ret
