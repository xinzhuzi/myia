0x56f4f20	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x56f4f24	fd7b01a9	stp x29,x30,[sp, #0x10]
0x56f4f28	fd430091	add x29,sp,#0x10
0x56f4f2c	f30302aa	mov x19,x2
0x56f4f30	f40301aa	mov x20,x1
0x56f4f34	080040f9	ldr x8,[x0]
0x56f4f38	080940f9	ldr x8,[x8, #0x10]
0x56f4f3c	00013fd6	blr x8
0x56f4f40	000100b4	cbz x0,0x056f4f60
0x56f4f44	080040f9	ldr x8,[x0]
0x56f4f48	032d40f9	ldr x3,[x8, #0x58]
0x56f4f4c	e10314aa	mov x1,x20
0x56f4f50	e20313aa	mov x2,x19
0x56f4f54	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x56f4f58	f44fc2a8	ldp x20,x19,[sp], #0x20
0x56f4f5c	60001fd6	br x3
0x56f4f60	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x56f4f64	f44fc2a8	ldp x20,x19,[sp], #0x20
0x56f4f68	c0035fd6	ret
