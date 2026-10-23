0x33c7c	290040f9	ldr x9,[x1]
0x33c80	3f0000f9	str xzr,[x1]
0x33c84	080040f9	ldr x8,[x0]
0x33c88	090000f9	str x9,[x0]
0x33c8c	e80100b4	cbz x8,0x00033cc8
0x33c90	09008012	mov w9,#0xffffffff
0x33c94	0901e9b8	ldaddal w9,w9,[x8]
0x33c98	3f050071	cmp w9,#0x1
0x33c9c	61010054	b.ne 0x00033cc8
0x33ca0	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x33ca4	fd7b01a9	stp x29,x30,[sp, #0x10]
0x33ca8	fd430091	add x29,sp,#0x10
0x33cac	090940f9	ldr x9,[x8, #0x10]
0x33cb0	f30300aa	mov x19,x0
0x33cb4	e00308aa	mov x0,x8
0x33cb8	20013fd6	blr x9
0x33cbc	e00313aa	mov x0,x19
0x33cc0	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x33cc4	f44fc2a8	ldp x20,x19,[sp], #0x20
0x33cc8	c0035fd6	ret
