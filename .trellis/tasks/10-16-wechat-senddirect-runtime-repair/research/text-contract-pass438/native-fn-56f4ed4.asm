0x56f4ed4	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x56f4ed8	fd7b01a9	stp x29,x30,[sp, #0x10]
0x56f4edc	fd430091	add x29,sp,#0x10
0x56f4ee0	f30302aa	mov x19,x2
0x56f4ee4	f40301aa	mov x20,x1
0x56f4ee8	080040f9	ldr x8,[x0]
0x56f4eec	080940f9	ldr x8,[x8, #0x10]
0x56f4ef0	00013fd6	blr x8
0x56f4ef4	000100b4	cbz x0,0x056f4f14
0x56f4ef8	080040f9	ldr x8,[x0]
0x56f4efc	032540f9	ldr x3,[x8, #0x48]
0x56f4f00	e10314aa	mov x1,x20
0x56f4f04	e20313aa	mov x2,x19
0x56f4f08	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x56f4f0c	f44fc2a8	ldp x20,x19,[sp], #0x20
0x56f4f10	60001fd6	br x3
0x56f4f14	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x56f4f18	f44fc2a8	ldp x20,x19,[sp], #0x20
0x56f4f1c	c0035fd6	ret
