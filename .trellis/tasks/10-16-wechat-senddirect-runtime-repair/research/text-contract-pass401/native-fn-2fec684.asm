0x2fec684	ff4301d1	sub sp,sp,#0x50
0x2fec688	f65702a9	stp x22,x21,[sp, #0x20]
0x2fec68c	f44f03a9	stp x20,x19,[sp, #0x30]
0x2fec690	fd7b04a9	stp x29,x30,[sp, #0x40]
0x2fec694	fd030191	add x29,sp,#0x40
0x2fec698	f30300aa	mov x19,x0
0x2fec69c	15000491	add x21,x0,#0x100
0x2fec6a0	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x2fec6a4	f52300a9	stp x21,x8,[sp]
0x2fec6a8	4a4e0595	bl 0x0713ffd0
0x2fec6ac	e00b00b9	str w0,[sp, #0x8]
0x2fec6b0	600a40f9	ldr x0,[x19, #0x10]
0x2fec6b4	a00100b4	cbz x0,0x02fec6e8
0x2fec6b8	5c4d0595	bl 0x0713fc28
0x2fec6bc	e00f00f9	str x0,[sp, #0x18]
0x2fec6c0	400100b4	cbz x0,0x02fec6e8
0x2fec6c4	f40300aa	mov x20,x0
0x2fec6c8	680640f9	ldr x8,[x19, #0x8]
0x2fec6cc	e80b00f9	str x8,[sp, #0x10]
0x2fec6d0	080100b4	cbz x8,0x02fec6f0
0x2fec6d4	28f45994	bl 0x04669774
0x2fec6d8	61620091	add x1,x19,#0x18
0x2fec6dc	c01b5a94	bl 0x046735dc
0x2fec6e0	f30300aa	mov x19,x0
0x2fec6e4	04000014	b 0x02fec6f4
0x2fec6e8	13008052	mov w19,#0x0
0x2fec6ec	0c000014	b 0x02fec71c
0x2fec6f0	13008052	mov w19,#0x0
0x2fec6f4	88220091	add x8,x20,#0x8
0x2fec6f8	09008092	mov x9,#-0x1
0x2fec6fc	0801e9f8	ldaddal x9,x8,[x8]
0x2fec700	e80000b5	cbnz x8,0x02fec71c
0x2fec704	880240f9	ldr x8,[x20]
0x2fec708	080940f9	ldr x8,[x8, #0x10]
0x2fec70c	e00314aa	mov x0,x20
0x2fec710	00013fd6	blr x8
0x2fec714	e00314aa	mov x0,x20
0x2fec718	414d0595	bl 0x0713fc1c
0x2fec71c	00048052	mov w0,#0x20
0x2fec720	444e0595	bl 0x07140030
0x2fec724	c86c03d0	adrp x8,0x9d86000
0x2fec728	08e10d91	add x8,x8,#0x378
0x2fec72c	080000f9	str x8,[x0]
0x2fec730	e80300aa	mov x8,x0
0x2fec734	138d0038	strb w19,[x8, #0x8]!
0x2fec738	495a03d0	adrp x9,0x9b36000
0x2fec73c	295145f9	ldr x9,[x9, #0xaa0]
0x2fec740	092001a9	stp x9,x8,[x0, #0x10]
0x2fec744	e00b00f9	str x0,[sp, #0x10]
0x2fec748	a00240f9	ldr x0,[x21]
0x2fec74c	e1430091	add x1,sp,#0x10
0x2fec750	e3f3d994	bl 0x066696dc
0x2fec754	e00b40f9	ldr x0,[sp, #0x10]
0x2fec758	800000b4	cbz x0,0x02fec768
0x2fec75c	080040f9	ldr x8,[x0]
0x2fec760	080540f9	ldr x8,[x8, #0x8]
0x2fec764	00013fd6	blr x8
0x2fec768	1a4e0595	bl 0x0713ffd0
0x2fec76c	e80b40b9	ldr w8,[sp, #0x8]
0x2fec770	1f00086b	cmp w0,w8
0x2fec774	6d010054	b.le 0x02fec7a0
0x2fec778	e80340f9	ldr x8,[sp]
0x2fec77c	000140f9	ldr x0,[x8]
0x2fec780	ff0b00f9	str xzr,[sp, #0x10]
0x2fec784	e1430091	add x1,sp,#0x10
0x2fec788	32f2d994	bl 0x06669050
0x2fec78c	e00b40f9	ldr x0,[sp, #0x10]
0x2fec790	800000b4	cbz x0,0x02fec7a0
0x2fec794	080040f9	ldr x8,[x0]
0x2fec798	080540f9	ldr x8,[x8, #0x8]
0x2fec79c	00013fd6	blr x8
0x2fec7a0	fd7b44a9	ldp x29,x30,[sp, #0x40]
0x2fec7a4	f44f43a9	ldp x20,x19,[sp, #0x30]
0x2fec7a8	f65742a9	ldp x22,x21,[sp, #0x20]
0x2fec7ac	ff430191	add sp,sp,#0x50
0x2fec7b0	c0035fd6	ret
