0x56f4d14	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x56f4d18	fd7b01a9	stp x29,x30,[sp, #0x10]
0x56f4d1c	fd430091	add x29,sp,#0x10
0x56f4d20	f30301aa	mov x19,x1
0x56f4d24	080040f9	ldr x8,[x0]
0x56f4d28	080940f9	ldr x8,[x8, #0x10]
0x56f4d2c	00013fd6	blr x8
0x56f4d30	e00000b4	cbz x0,0x056f4d4c
0x56f4d34	080040f9	ldr x8,[x0]
0x56f4d38	020940f9	ldr x2,[x8, #0x10]
0x56f4d3c	e10313aa	mov x1,x19
0x56f4d40	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x56f4d44	f44fc2a8	ldp x20,x19,[sp], #0x20
0x56f4d48	40001fd6	br x2
0x56f4d4c	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x56f4d50	f44fc2a8	ldp x20,x19,[sp], #0x20
0x56f4d54	c0035fd6	ret
