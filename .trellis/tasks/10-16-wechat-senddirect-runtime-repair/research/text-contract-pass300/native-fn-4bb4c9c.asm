0x4bb4c9c	ff4301d1	sub sp,sp,#0x50
0x4bb4ca0	f65702a9	stp x22,x21,[sp, #0x20]
0x4bb4ca4	f44f03a9	stp x20,x19,[sp, #0x30]
0x4bb4ca8	fd7b04a9	stp x29,x30,[sp, #0x40]
0x4bb4cac	fd030191	add x29,sp,#0x40
0x4bb4cb0	f30300aa	mov x19,x0
0x4bb4cb4	88c702b0	adrp x8,0xa4a5000
0x4bb4cb8	09495d39	ldrb w9,[x8, #0x752]
0x4bb4cbc	49010037	tbnz w9,#0x0,0x04bb4ce4
0x4bb4cc0	89c702b0	adrp x9,0xa4a5000
0x4bb4cc4	29311d91	add x9,x9,#0x74c
0x4bb4cc8	6af801f0	adrp x10,0x8ac3000
0x4bb4ccc	409144fd	ldr d0,[x10, #0x920]
0x4bb4cd0	200100bd	str s0,[x9]
0x4bb4cd4	ea0c8052	mov w10,#0x67
0x4bb4cd8	2a090079	strh w10,[x9, #0x4]
0x4bb4cdc	29008052	mov w9,#0x1
0x4bb4ce0	09491d39	strb w9,[x8, #0x752]
0x4bb4ce4	80c702b0	adrp x0,0xa4a5000
0x4bb4ce8	00301d91	add x0,x0,#0x74c
0x4bb4cec	43339694	bl 0x071419f8
0x4bb4cf0	e8ef7db2	orr x8,xzr,#0x7ffffffffffffff8
0x4bb4cf4	1f0008eb	cmp x0,x8
0x4bb4cf8	22050054	b.cs 0x04bb4d9c
0x4bb4cfc	f40300aa	mov x20,x0
0x4bb4d00	1f5c00f1	cmp x0,#0x17
0x4bb4d04	a2000054	b.cs 0x04bb4d18
0x4bb4d08	f47f0039	strb w20,[sp, #0x1f]
0x4bb4d0c	f5230091	add x21,sp,#0x8
0x4bb4d10	940100b5	cbnz x20,0x04bb4d40
0x4bb4d14	10000014	b 0x04bb4d54
0x4bb4d18	880a40b2	orr x8,x20,#0x7
0x4bb4d1c	1f5d00f1	cmp x8,#0x17
0x4bb4d20	29038052	mov w9,#0x19
0x4bb4d24	3605889a	csinc x22,x9,x8,eq
0x4bb4d28	e00316aa	mov x0,x22
0x4bb4d2c	c12c9694	bl 0x07140030
0x4bb4d30	f50300aa	mov x21,x0
0x4bb4d34	c80241b2	orr x8,x22,#-0x8000000000000000
0x4bb4d38	f42301a9	stp x20,x8,[sp, #0x10]
0x4bb4d3c	e00700f9	str x0,[sp, #0x8]
0x4bb4d40	81c702b0	adrp x1,0xa4a5000
0x4bb4d44	21301d91	add x1,x1,#0x74c
0x4bb4d48	e00315aa	mov x0,x21
0x4bb4d4c	e20314aa	mov x2,x20
0x4bb4d50	4e309694	bl 0x07140e88
0x4bb4d54	bf6a3438	strb wzr,[x21, x20]
0x4bb4d58	e1230091	add x1,sp,#0x8
0x4bb4d5c	e00313aa	mov x0,x19
0x4bb4d60	194d6b94	bl 0x066881c4
0x4bb4d64	e87fc039	ldrsb w8,[sp, #0x1f]
0x4bb4d68	0801f836	tbz w8,#0x1f,0x04bb4d88
0x4bb4d6c	e80740f9	ldr x8,[sp, #0x8]
0x4bb4d70	e90f40f9	ldr x9,[sp, #0x18]
0x4bb4d74	21f94092	and x1,x9,#0x7fffffffffffffff
0x4bb4d78	f30300aa	mov x19,x0
0x4bb4d7c	e00308aa	mov x0,x8
0x4bb4d80	a32c9694	bl 0x0714000c
0x4bb4d84	e00313aa	mov x0,x19
0x4bb4d88	fd7b44a9	ldp x29,x30,[sp, #0x40]
0x4bb4d8c	f44f43a9	ldp x20,x19,[sp, #0x30]
0x4bb4d90	f65742a9	ldp x22,x21,[sp, #0x20]
0x4bb4d94	ff430191	add sp,sp,#0x50
0x4bb4d98	c0035fd6	ret
0x4bb4d9c	e0230091	add x0,sp,#0x8
0x4bb4da0	ff8fd196	bl 0x00018d9c
