0x2ab8e14	ff8301d1	sub sp,sp,#0x60
0x2ab8e18	f85f02a9	stp x24,x23,[sp, #0x20]
0x2ab8e1c	f65703a9	stp x22,x21,[sp, #0x30]
0x2ab8e20	f44f04a9	stp x20,x19,[sp, #0x40]
0x2ab8e24	fd7b05a9	stp x29,x30,[sp, #0x50]
0x2ab8e28	fd430191	add x29,sp,#0x50
0x2ab8e2c	f30301aa	mov x19,x1
0x2ab8e30	20200091	add x0,x1,#0x8
0x2ab8e34	e3ef8394	bl 0x04bb4dc0
0x2ab8e38	c0070034	cbz w0,0x02ab8f30
0x2ab8e3c	e8030091	mov x8,sp
0x2ab8e40	9ac76e94	bl 0x0466aca8
0x2ab8e44	e00340f9	ldr x0,[sp]
0x2ab8e48	080040f9	ldr x8,[x0]
0x2ab8e4c	080540f9	ldr x8,[x8, #0x8]
0x2ab8e50	00013fd6	blr x8
0x2ab8e54	f40740f9	ldr x20,[sp, #0x8]
0x2ab8e58	740100b4	cbz x20,0x02ab8e84
0x2ab8e5c	88220091	add x8,x20,#0x8
0x2ab8e60	09008092	mov x9,#-0x1
0x2ab8e64	0801e9f8	ldaddal x9,x8,[x8]
0x2ab8e68	e80000b5	cbnz x8,0x02ab8e84
0x2ab8e6c	880240f9	ldr x8,[x20]
0x2ab8e70	080940f9	ldr x8,[x8, #0x10]
0x2ab8e74	e00314aa	mov x0,x20
0x2ab8e78	00013fd6	blr x8
0x2ab8e7c	e00314aa	mov x0,x20
0x2ab8e80	671b1a95	bl 0x0713fc1c
0x2ab8e84	685640b9	ldr w8,[x19, #0x54]
0x2ab8e88	e81f00b9	str w8,[sp, #0x1c]
0x2ab8e8c	e0730091	add x0,sp,#0x1c
0x2ab8e90	d4a87194	bl 0x047231e0
0x2ab8e94	e81f40b9	ldr w8,[sp, #0x1c]
0x2ab8e98	685600b9	str w8,[x19, #0x54]
0x2ab8e9c	64a08d94	bl 0x04e2102c
0x2ab8ea0	f50300aa	mov x21,x0
0x2ab8ea4	d5221a95	bl 0x071419f8
0x2ab8ea8	e8ef7db2	orr x8,xzr,#0x7ffffffffffffff8
0x2ab8eac	1f0008eb	cmp x0,x8
0x2ab8eb0	c2040054	b.cs 0x02ab8f48
0x2ab8eb4	f40300aa	mov x20,x0
0x2ab8eb8	1f5c00f1	cmp x0,#0x17
0x2ab8ebc	a2000054	b.cs 0x02ab8ed0
0x2ab8ec0	f45f0039	strb w20,[sp, #0x17]
0x2ab8ec4	f6030091	mov x22,sp
0x2ab8ec8	940100b5	cbnz x20,0x02ab8ef8
0x2ab8ecc	0f000014	b 0x02ab8f08
0x2ab8ed0	880a40b2	orr x8,x20,#0x7
0x2ab8ed4	1f5d00f1	cmp x8,#0x17
0x2ab8ed8	29038052	mov w9,#0x19
0x2ab8edc	3705889a	csinc x23,x9,x8,eq
0x2ab8ee0	e00317aa	mov x0,x23
0x2ab8ee4	531c1a95	bl 0x07140030
0x2ab8ee8	f60300aa	mov x22,x0
0x2ab8eec	e80241b2	orr x8,x23,#-0x8000000000000000
0x2ab8ef0	f4a300a9	stp x20,x8,[sp, #0x8]
0x2ab8ef4	e00300f9	str x0,[sp]
0x2ab8ef8	e00316aa	mov x0,x22
0x2ab8efc	e10315aa	mov x1,x21
0x2ab8f00	e20314aa	mov x2,x20
0x2ab8f04	e41f1a95	bl 0x07140e94
0x2ab8f08	df6a3438	strb wzr,[x22, x20]
0x2ab8f0c	60a20291	add x0,x19,#0xa8
0x2ab8f10	e1030091	mov x1,sp
0x2ab8f14	731a1a95	bl 0x0713f8e0
0x2ab8f18	e85fc039	ldrsb w8,[sp, #0x17]
0x2ab8f1c	a800f836	tbz w8,#0x1f,0x02ab8f30
0x2ab8f20	e00340f9	ldr x0,[sp]
0x2ab8f24	e80b40f9	ldr x8,[sp, #0x10]
0x2ab8f28	01f94092	and x1,x8,#0x7fffffffffffffff
0x2ab8f2c	381c1a95	bl 0x0714000c
0x2ab8f30	fd7b45a9	ldp x29,x30,[sp, #0x50]
0x2ab8f34	f44f44a9	ldp x20,x19,[sp, #0x40]
0x2ab8f38	f65743a9	ldp x22,x21,[sp, #0x30]
0x2ab8f3c	f85f42a9	ldp x24,x23,[sp, #0x20]
0x2ab8f40	ff830191	add sp,sp,#0x60
0x2ab8f44	c0035fd6	ret
0x2ab8f48	e0030091	mov x0,sp
0x2ab8f4c	947f5597	bl 0x00018d9c
