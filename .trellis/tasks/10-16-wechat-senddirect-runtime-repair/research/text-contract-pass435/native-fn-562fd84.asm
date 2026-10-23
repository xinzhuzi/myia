0x562fd84	080840f9	ldr x8,[x0, #0x10]
0x562fd88	1f0900f1	cmp x8,#0x2
0x562fd8c	63020054	b.cc 0x0562fdd8
0x562fd90	09008012	mov w9,#0xffffffff
0x562fd94	0801e9b8	ldaddal w9,w8,[x8]
0x562fd98	1f050071	cmp w8,#0x1
0x562fd9c	e1010054	b.ne 0x0562fdd8
0x562fda0	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x562fda4	fd7b01a9	stp x29,x30,[sp, #0x10]
0x562fda8	fd430091	add x29,sp,#0x10
0x562fdac	080840f9	ldr x8,[x0, #0x10]
0x562fdb0	f30300aa	mov x19,x0
0x562fdb4	e00308aa	mov x0,x8
0x562fdb8	c9426c94	bl 0x071408dc
0x562fdbc	e00313aa	mov x0,x19
0x562fdc0	7ffe00a9	stp xzr,xzr,[x19, #0x8]
0x562fdc4	681002d0	adrp x8,0x983d000
0x562fdc8	08412f91	add x8,x8,#0xbd0
0x562fdcc	680200f9	str x8,[x19]
0x562fdd0	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x562fdd4	f44fc2a8	ldp x20,x19,[sp], #0x20
0x562fdd8	c0035fd6	ret
