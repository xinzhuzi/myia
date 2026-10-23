0x56f8b78	f657bda9	stp x22,x21,[sp, #-0x30]!
0x56f8b7c	f44f01a9	stp x20,x19,[sp, #0x10]
0x56f8b80	fd7b02a9	stp x29,x30,[sp, #0x20]
0x56f8b84	fd830091	add x29,sp,#0x20
0x56f8b88	f30300aa	mov x19,x0
0x56f8b8c	484102f0	adrp x8,0x9f23000
0x56f8b90	08813891	add x8,x8,#0xe20
0x56f8b94	09e10091	add x9,x8,#0x38
0x56f8b98	f40300aa	mov x20,x0
0x56f8b9c	898e00f8	str x9,[x20, #0x8]!
0x56f8ba0	f50300aa	mov x21,x0
0x56f8ba4	a80601f8	str x8,[x21], #0x10
0x56f8ba8	e00315aa	mov x0,x21
0x56f8bac	362e4097	bl 0x02704484
0x56f8bb0	60420191	add x0,x19,#0x50
0x56f8bb4	0c36fd97	bl 0x056463e4
0x56f8bb8	7f5200f9	str xzr,[x19, #0xa0]
0x56f8bbc	e00313aa	mov x0,x19
0x56f8bc0	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x56f8bc4	f44f41a9	ldp x20,x19,[sp, #0x10]
0x56f8bc8	f657c3a8	ldp x22,x21,[sp], #0x30
0x56f8bcc	c0035fd6	ret
