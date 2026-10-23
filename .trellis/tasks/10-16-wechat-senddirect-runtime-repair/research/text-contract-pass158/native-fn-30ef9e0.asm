0x30ef9e0	ff8301d1	sub sp,sp,#0x60
0x30ef9e4	fa6701a9	stp x26,x25,[sp, #0x10]
0x30ef9e8	f85f02a9	stp x24,x23,[sp, #0x20]
0x30ef9ec	f65703a9	stp x22,x21,[sp, #0x30]
0x30ef9f0	f44f04a9	stp x20,x19,[sp, #0x40]
0x30ef9f4	fd7b05a9	stp x29,x30,[sp, #0x50]
0x30ef9f8	fd430191	add x29,sp,#0x50
0x30ef9fc	f90302aa	mov x25,x2
0x30efa00	f70301aa	mov x23,x1
0x30efa04	f30300aa	mov x19,x0
0x30efa08	c86703d0	adrp x8,0x9de9000
0x30efa0c	08a11491	add x8,x8,#0x528
0x30efa10	080000f9	str x8,[x0]
0x30efa14	280040f9	ldr x8,[x1]
0x30efa18	f40300aa	mov x20,x0
0x30efa1c	888e00f8	str x8,[x20, #0x8]!
0x30efa20	280440f9	ldr x8,[x1, #0x8]
0x30efa24	080800f9	str x8,[x0, #0x10]
0x30efa28	880000b4	cbz x8,0x030efa38
0x30efa2c	08210091	add x8,x8,#0x8
0x30efa30	29008052	mov w9,#0x1
0x30efa34	080129f8	ldadd x9,x8,[x8]
0x30efa38	00e4006f	movi v0.2D,#0x0
0x30efa3c	f50313aa	mov x21,x19
0x30efa40	a08e813c	str q0,[x21, #0x18]!
0x30efa44	f60315aa	mov x22,x21
0x30efa48	c00e813c	str q0,[x22, #0x10]!
0x30efa4c	f80315aa	mov x24,x21
0x30efa50	000f823c	str q0,[x24, #0x20]!
0x30efa54	bf2a00f9	str xzr,[x21, #0x50]
0x30efa58	a08201ad	stp q0,q0,[x21, #0x30]
0x30efa5c	a8620191	add x8,x21,#0x58
0x30efa60	e0030091	mov x0,sp
0x30efa64	2300c497	bl 0x021efaf0
0x30efa68	68020291	add x8,x19,#0x80
0x30efa6c	e0030091	mov x0,sp
0x30efa70	2000c497	bl 0x021efaf0
0x30efa74	68420291	add x8,x19,#0x90
0x30efa78	e0030091	mov x0,sp
0x30efa7c	1d00c497	bl 0x021efaf0
0x30efa80	68820291	add x8,x19,#0xa0
0x30efa84	e0030091	mov x0,sp
0x30efa88	1a00c497	bl 0x021efaf0
0x30efa8c	79c20239	strb w25,[x19, #0xb0]
0x30efa90	00e4006f	movi v0.2D,#0x0
0x30efa94	f90313aa	mov x25,x19
0x30efa98	200f8d3c	str q0,[x25, #0xd0]!
0x30efa9c	60428b3c	stur q0,[x19, #0xb4]
0x30efaa0	60428c3c	stur q0,[x19, #0xc4]
0x30efaa4	e8030091	mov x8,sp
0x30efaa8	e00313aa	mov x0,x19
0x30efaac	8e000094	bl 0x030efce4
0x30efab0	e003c03d	ldr q0,[sp]
0x30efab4	ff7f00a9	stp xzr,xzr,[sp]
0x30efab8	7a1240f9	ldr x26,[x19, #0x20]
0x30efabc	6082813c	stur q0,[x19, #0x18]
0x30efac0	7a0100b4	cbz x26,0x030efaec
0x30efac4	48230091	add x8,x26,#0x8
0x30efac8	09008092	mov x9,#-0x1
0x30efacc	0801e9f8	ldaddal x9,x8,[x8]
0x30efad0	e80000b5	cbnz x8,0x030efaec
0x30efad4	480340f9	ldr x8,[x26]
0x30efad8	080940f9	ldr x8,[x8, #0x10]
0x30efadc	e0031aaa	mov x0,x26
0x30efae0	00013fd6	blr x8
0x30efae4	e0031aaa	mov x0,x26
0x30efae8	4d400195	bl 0x0713fc1c
0x30efaec	fa0740f9	ldr x26,[sp, #0x8]
0x30efaf0	7a0100b4	cbz x26,0x030efb1c
0x30efaf4	48230091	add x8,x26,#0x8
0x30efaf8	09008092	mov x9,#-0x1
0x30efafc	0801e9f8	ldaddal x9,x8,[x8]
0x30efb00	e80000b5	cbnz x8,0x030efb1c
0x30efb04	480340f9	ldr x8,[x26]
0x30efb08	080940f9	ldr x8,[x8, #0x10]
0x30efb0c	e0031aaa	mov x0,x26
0x30efb10	00013fd6	blr x8
0x30efb14	e0031aaa	mov x0,x26
0x30efb18	41400195	bl 0x0713fc1c
0x30efb1c	e80240f9	ldr x8,[x23]
0x30efb20	01410291	add x1,x8,#0x90
0x30efb24	e00318aa	mov x0,x24
0x30efb28	6e3f0195	bl 0x0713f8e0
0x30efb2c	00188052	mov w0,#0xc0
0x30efb30	40410195	bl 0x07140030
0x30efb34	f50300aa	mov x21,x0
0x30efb38	bf8e00f8	str xzr,[x21, #0x8]!
0x30efb3c	1f0800f9	str xzr,[x0, #0x10]
0x30efb40	c86703d0	adrp x8,0x9de9000
0x30efb44	08811791	add x8,x8,#0x5e0
0x30efb48	080000f9	str x8,[x0]
0x30efb4c	00e4006f	movi v0.2D,#0x0
0x30efb50	e80300aa	mov x8,x0
0x30efb54	008d813c	str q0,[x8, #0x18]!
0x30efb58	0080843c	stur q0,[x0, #0x48]
0x30efb5c	0080853c	stur q0,[x0, #0x58]
0x30efb60	0080833c	stur q0,[x0, #0x38]
0x30efb64	0080823c	stur q0,[x0, #0x28]
0x30efb68	0080883c	stur q0,[x0, #0x88]
0x30efb6c	0080873c	stur q0,[x0, #0x78]
0x30efb70	0080863c	stur q0,[x0, #0x68]
0x30efb74	1f4c00f9	str xzr,[x0, #0x98]
0x30efb78	29008052	mov w9,#0x1
0x30efb7c	09010039	strb w9,[x8]
0x30efb80	00e0843c	stur q0,[x0, #0x4e]
0x30efb84	0040843c	stur q0,[x0, #0x44]
0x30efb88	0040833c	stur q0,[x0, #0x34]
0x30efb8c	0040823c	stur q0,[x0, #0x24]
0x30efb90	008003ad	stp q0,q0,[x0, #0x70]
0x30efb94	1f200179	strh wzr,[x0, #0x90]
0x30efb98	099c00b9	str w9,[x0, #0x9c]
0x30efb9c	000005ad	stp q0,q0,[x0, #0xa0]
0x30efba0	600000b4	cbz x0,0x030efbac
0x30efba4	29008052	mov w9,#0x1
0x30efba8	a90229f8	ldadd x9,x9,[x21]
0x30efbac	741a40f9	ldr x20,[x19, #0x30]
0x30efbb0	688202a9	stp x8,x0,[x19, #0x28]
0x30efbb4	b40100b4	cbz x20,0x030efbe8
0x30efbb8	88220091	add x8,x20,#0x8
0x30efbbc	09008092	mov x9,#-0x1
0x30efbc0	0801e9f8	ldaddal x9,x8,[x8]
0x30efbc4	280100b5	cbnz x8,0x030efbe8
0x30efbc8	880240f9	ldr x8,[x20]
0x30efbcc	080940f9	ldr x8,[x8, #0x10]
0x30efbd0	f60300aa	mov x22,x0
0x30efbd4	e00314aa	mov x0,x20
0x30efbd8	00013fd6	blr x8
0x30efbdc	e00314aa	mov x0,x20
0x30efbe0	0f400195	bl 0x0713fc1c
0x30efbe4	e00316aa	mov x0,x22
0x30efbe8	400100b4	cbz x0,0x030efc10
0x30efbec	08008092	mov x8,#-0x1
0x30efbf0	a802e8f8	ldaddal x8,x8,[x21]
0x30efbf4	e80000b5	cbnz x8,0x030efc10
0x30efbf8	080040f9	ldr x8,[x0]
0x30efbfc	080940f9	ldr x8,[x8, #0x10]
0x30efc00	f40300aa	mov x20,x0
0x30efc04	00013fd6	blr x8
0x30efc08	e00314aa	mov x0,x20
0x30efc0c	04400195	bl 0x0713fc1c
0x30efc10	e00313aa	mov x0,x19
0x30efc14	fd7b45a9	ldp x29,x30,[sp, #0x50]
0x30efc18	f44f44a9	ldp x20,x19,[sp, #0x40]
0x30efc1c	f65743a9	ldp x22,x21,[sp, #0x30]
0x30efc20	f85f42a9	ldp x24,x23,[sp, #0x20]
0x30efc24	fa6741a9	ldp x26,x25,[sp, #0x10]
0x30efc28	ff830191	add sp,sp,#0x60
0x30efc2c	c0035fd6	ret
