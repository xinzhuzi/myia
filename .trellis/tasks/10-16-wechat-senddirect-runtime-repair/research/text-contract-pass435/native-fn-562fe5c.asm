0x562fe5c	f657bda9	stp x22,x21,[sp, #-0x30]!
0x562fe60	f44f01a9	stp x20,x19,[sp, #0x10]
0x562fe64	fd7b02a9	stp x29,x30,[sp, #0x20]
0x562fe68	fd830091	add x29,sp,#0x20
0x562fe6c	080840f9	ldr x8,[x0, #0x10]
0x562fe70	731002d0	adrp x19,0x983d000
0x562fe74	73422f91	add x19,x19,#0xbd0
0x562fe78	1f0900f1	cmp x8,#0x2
0x562fe7c	c3010054	b.cc 0x0562feb4
0x562fe80	09008012	mov w9,#0xffffffff
0x562fe84	0801e9b8	ldaddal w9,w8,[x8]
0x562fe88	1f050071	cmp w8,#0x1
0x562fe8c	41010054	b.ne 0x0562feb4
0x562fe90	080840f9	ldr x8,[x0, #0x10]
0x562fe94	f40300aa	mov x20,x0
0x562fe98	e00308aa	mov x0,x8
0x562fe9c	f50301aa	mov x21,x1
0x562fea0	8f426c94	bl 0x071408dc
0x562fea4	e10315aa	mov x1,x21
0x562fea8	e00314aa	mov x0,x20
0x562feac	9ffe00a9	stp xzr,xzr,[x20, #0x8]
0x562feb0	930200f9	str x19,[x20]
0x562feb4	2000c03d	ldr q0,[x1]
0x562feb8	0000803d	str q0,[x0]
0x562febc	280840f9	ldr x8,[x1, #0x10]
0x562fec0	080800f9	str x8,[x0, #0x10]
0x562fec4	3ffc00a9	stp xzr,xzr,[x1, #0x8]
0x562fec8	330000f9	str x19,[x1]
0x562fecc	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x562fed0	f44f41a9	ldp x20,x19,[sp, #0x10]
0x562fed4	f657c3a8	ldp x22,x21,[sp], #0x30
0x562fed8	c0035fd6	ret
