0x465db80	3f0000eb	cmp x1,x0
0x465db84	c0010054	b.eq 0x0465dbbc
0x465db88	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x465db8c	fd7b01a9	stp x29,x30,[sp, #0x10]
0x465db90	fd430091	add x29,sp,#0x10
0x465db94	f30301aa	mov x19,x1
0x465db98	080040f9	ldr x8,[x0]
0x465db9c	081140f9	ldr x8,[x8, #0x20]
0x465dba0	f40300aa	mov x20,x0
0x465dba4	00013fd6	blr x8
0x465dba8	e00314aa	mov x0,x20
0x465dbac	e10313aa	mov x1,x19
0x465dbb0	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x465dbb4	f44fc2a8	ldp x20,x19,[sp], #0x20
0x465dbb8	1dfeff17	b 0x0465d42c
0x465dbbc	c0035fd6	ret
