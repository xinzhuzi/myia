0x56ccae0	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x56ccae4	fd7b01a9	stp x29,x30,[sp, #0x10]
0x56ccae8	fd430091	add x29,sp,#0x10
0x56ccaec	f30300aa	mov x19,x0
0x56ccaf0	8fd6ff97	bl 0x056c252c
0x56ccaf4	28008052	mov w8,#0x1
0x56ccaf8	08800039	strb w8,[x0, #0x20]
0x56ccafc	e00313aa	mov x0,x19
0x56ccb00	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x56ccb04	f44fc2a8	ldp x20,x19,[sp], #0x20
0x56ccb08	c0035fd6	ret
