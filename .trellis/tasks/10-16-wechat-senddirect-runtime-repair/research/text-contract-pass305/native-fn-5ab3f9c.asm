0x5ab3f9c	f657bda9	stp x22,x21,[sp, #-0x30]!
0x5ab3fa0	f44f01a9	stp x20,x19,[sp, #0x10]
0x5ab3fa4	fd7b02a9	stp x29,x30,[sp, #0x20]
0x5ab3fa8	fd830091	add x29,sp,#0x20
0x5ab3fac	f30302aa	mov x19,x2
0x5ab3fb0	f60301aa	mov x22,x1
0x5ab3fb4	f50300aa	mov x21,x0
0x5ab3fb8	080040f9	ldr x8,[x0]
0x5ab3fbc	082540f9	ldr x8,[x8, #0x48]
0x5ab3fc0	00013fd6	blr x8
0x5ab3fc4	f40300aa	mov x20,x0
0x5ab3fc8	1f00136b	cmp w0,w19
0x5ab3fcc	2c020054	b.gt 0x05ab4010
0x5ab3fd0	a80240f9	ldr x8,[x21]
0x5ab3fd4	082d40f9	ldr x8,[x8, #0x58]
0x5ab3fd8	e00315aa	mov x0,x21
0x5ab3fdc	e10316aa	mov x1,x22
0x5ab3fe0	00013fd6	blr x8
0x5ab3fe4	160016cb	sub x22,x0,x22
0x5ab3fe8	dfc234eb	cmp x22,w20, SXTW 
0x5ab3fec	20010054	b.eq 0x05ab4010
0x5ab3ff0	a80240f9	ldr x8,[x21]
0x5ab3ff4	082540f9	ldr x8,[x8, #0x48]
0x5ab3ff8	e00315aa	mov x0,x21
0x5ab3ffc	00013fd6	blr x8
0x5ab4000	e10300aa	mov x1,x0
0x5ab4004	e00314aa	mov x0,x20
0x5ab4008	e20316aa	mov x2,x22
0x5ab400c	62ffff97	bl 0x05ab3d94
0x5ab4010	9f02136b	cmp w20,w19
0x5ab4014	e0c79f1a	cset w0,le
0x5ab4018	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x5ab401c	f44f41a9	ldp x20,x19,[sp, #0x10]
0x5ab4020	f657c3a8	ldp x22,x21,[sp], #0x30
0x5ab4024	c0035fd6	ret
