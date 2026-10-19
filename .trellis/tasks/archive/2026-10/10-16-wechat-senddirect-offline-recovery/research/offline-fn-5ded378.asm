0x5ded378	f657bda9	stp x22,x21,[sp, #-0x30]!
0x5ded37c	f44f01a9	stp x20,x19,[sp, #0x10]
0x5ded380	fd7b02a9	stp x29,x30,[sp, #0x20]
0x5ded384	fd830091	add x29,sp,#0x20
0x5ded388	f50302aa	mov x21,x2
0x5ded38c	f30300aa	mov x19,x0
0x5ded390	080440f9	ldr x8,[x0, #0x8]
0x5ded394	1401018b	add x20,x8,x1
0x5ded398	e10314aa	mov x1,x20
0x5ded39c	0a000094	bl 0x05ded3c4
0x5ded3a0	b5000034	cbz w21,0x05ded3b4
0x5ded3a4	680a40f9	ldr x8,[x19, #0x10]
0x5ded3a8	9f0208eb	cmp x20,x8
0x5ded3ac	8882889a	csel x8,x20,x8,hi
0x5ded3b0	680a00f9	str x8,[x19, #0x10]
0x5ded3b4	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x5ded3b8	f44f41a9	ldp x20,x19,[sp, #0x10]
0x5ded3bc	f657c3a8	ldp x22,x21,[sp], #0x30
0x5ded3c0	c0035fd6	ret
