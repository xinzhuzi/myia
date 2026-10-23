0x2ab9104	ff8301d1	sub sp,sp,#0x60
0x2ab9108	f85f02a9	stp x24,x23,[sp, #0x20]
0x2ab910c	f65703a9	stp x22,x21,[sp, #0x30]
0x2ab9110	f44f04a9	stp x20,x19,[sp, #0x40]
0x2ab9114	fd7b05a9	stp x29,x30,[sp, #0x50]
0x2ab9118	fd430191	add x29,sp,#0x50
0x2ab911c	f30301aa	mov x19,x1
0x2ab9120	285440b9	ldr w8,[x1, #0x54]
0x2ab9124	e81f00b9	str w8,[sp, #0x1c]
0x2ab9128	e0730091	add x0,sp,#0x1c
0x2ab912c	66b07194	bl 0x047252c4
0x2ab9130	e81f40b9	ldr w8,[sp, #0x1c]
0x2ab9134	685600b9	str w8,[x19, #0x54]
0x2ab9138	34128d94	bl 0x04dfda08
0x2ab913c	f50300aa	mov x21,x0
0x2ab9140	2e221a95	bl 0x071419f8
0x2ab9144	e8ef7db2	orr x8,xzr,#0x7ffffffffffffff8
0x2ab9148	1f0008eb	cmp x0,x8
0x2ab914c	c2040054	b.cs 0x02ab91e4
0x2ab9150	f40300aa	mov x20,x0
0x2ab9154	1f5c00f1	cmp x0,#0x17
0x2ab9158	a2000054	b.cs 0x02ab916c
0x2ab915c	f45f0039	strb w20,[sp, #0x17]
0x2ab9160	f6030091	mov x22,sp
0x2ab9164	940100b5	cbnz x20,0x02ab9194
0x2ab9168	0f000014	b 0x02ab91a4
0x2ab916c	880a40b2	orr x8,x20,#0x7
0x2ab9170	1f5d00f1	cmp x8,#0x17
0x2ab9174	29038052	mov w9,#0x19
0x2ab9178	3705889a	csinc x23,x9,x8,eq
0x2ab917c	e00317aa	mov x0,x23
0x2ab9180	ac1b1a95	bl 0x07140030
0x2ab9184	f60300aa	mov x22,x0
0x2ab9188	e80241b2	orr x8,x23,#-0x8000000000000000
0x2ab918c	f4a300a9	stp x20,x8,[sp, #0x8]
0x2ab9190	e00300f9	str x0,[sp]
0x2ab9194	e00316aa	mov x0,x22
0x2ab9198	e10315aa	mov x1,x21
0x2ab919c	e20314aa	mov x2,x20
0x2ab91a0	3d1f1a95	bl 0x07140e94
0x2ab91a4	df6a3438	strb wzr,[x22, x20]
0x2ab91a8	60a20291	add x0,x19,#0xa8
0x2ab91ac	e1030091	mov x1,sp
0x2ab91b0	cc191a95	bl 0x0713f8e0
0x2ab91b4	e85fc039	ldrsb w8,[sp, #0x17]
0x2ab91b8	a800f836	tbz w8,#0x1f,0x02ab91cc
0x2ab91bc	e00340f9	ldr x0,[sp]
0x2ab91c0	e80b40f9	ldr x8,[sp, #0x10]
0x2ab91c4	01f94092	and x1,x8,#0x7fffffffffffffff
0x2ab91c8	911b1a95	bl 0x0714000c
0x2ab91cc	fd7b45a9	ldp x29,x30,[sp, #0x50]
0x2ab91d0	f44f44a9	ldp x20,x19,[sp, #0x40]
0x2ab91d4	f65743a9	ldp x22,x21,[sp, #0x30]
0x2ab91d8	f85f42a9	ldp x24,x23,[sp, #0x20]
0x2ab91dc	ff830191	add sp,sp,#0x60
0x2ab91e0	c0035fd6	ret
0x2ab91e4	e0030091	mov x0,sp
0x2ab91e8	ed7e5597	bl 0x00018d9c
