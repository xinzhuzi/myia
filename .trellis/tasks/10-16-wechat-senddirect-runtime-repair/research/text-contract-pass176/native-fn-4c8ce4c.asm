0x4c8ce4c	f85fbca9	stp x24,x23,[sp, #-0x40]!
0x4c8ce50	f65701a9	stp x22,x21,[sp, #0x10]
0x4c8ce54	f44f02a9	stp x20,x19,[sp, #0x20]
0x4c8ce58	fd7b03a9	stp x29,x30,[sp, #0x30]
0x4c8ce5c	fdc30091	add x29,sp,#0x30
0x4c8ce60	f50301aa	mov x21,x1
0x4c8ce64	f30300aa	mov x19,x0
0x4c8ce68	08910290	adrp x8,0x9eac000
0x4c8ce6c	08813b91	add x8,x8,#0xee0
0x4c8ce70	08410091	add x8,x8,#0x10
0x4c8ce74	080000f9	str x8,[x0]
0x4c8ce78	f40300aa	mov x20,x0
0x4c8ce7c	9f0e01f8	str xzr,[x20, #0x10]!
0x4c8ce80	1f0800b9	str wzr,[x0, #0x8]
0x4c8ce84	1ffc01a9	stp xzr,xzr,[x0, #0x18]
0x4c8ce88	362040a9	ldp x22,x8,[x1]
0x4c8ce8c	170116eb	subs x23,x8,x22
0x4c8ce90	60010054	b.eq 0x04c8cebc
0x4c8ce94	9703f8b7	tbnz x23,#0x3f,0x04c8cf04
0x4c8ce98	e00317aa	mov x0,x23
0x4c8ce9c	65cc9294	bl 0x07140030
0x4c8cea0	600201a9	stp x0,x0,[x19, #0x10]
0x4c8cea4	1800178b	add x24,x0,x23
0x4c8cea8	781200f9	str x24,[x19, #0x20]
0x4c8ceac	e10316aa	mov x1,x22
0x4c8ceb0	e20317aa	mov x2,x23
0x4c8ceb4	f5cf9294	bl 0x07140e88
0x4c8ceb8	780e00f9	str x24,[x19, #0x18]
0x4c8cebc	a8bec039	ldrsb w8,[x21, #0x2f]
0x4c8cec0	c800f837	tbnz w8,#0x1f,0x04c8ced8
0x4c8cec4	a082c13c	ldur q0,[x21, #0x18]
0x4c8cec8	a88242f8	ldur x8,[x21, #0x28]
0x4c8cecc	688203f8	stur x8,[x19, #0x38]
0x4c8ced0	6082823c	stur q0,[x19, #0x28]
0x4c8ced4	04000014	b 0x04c8cee4
0x4c8ced8	a18a41a9	ldp x1,x2,[x21, #0x18]
0x4c8cedc	60a20091	add x0,x19,#0x28
0x4c8cee0	902fce96	bl 0x00018d20
0x4c8cee4	a83240b9	ldr w8,[x21, #0x30]
0x4c8cee8	684200b9	str w8,[x19, #0x40]
0x4c8ceec	e00313aa	mov x0,x19
0x4c8cef0	fd7b43a9	ldp x29,x30,[sp, #0x30]
0x4c8cef4	f44f42a9	ldp x20,x19,[sp, #0x20]
0x4c8cef8	f65741a9	ldp x22,x21,[sp, #0x10]
0x4c8cefc	f85fc4a8	ldp x24,x23,[sp], #0x40
0x4c8cf00	c0035fd6	ret
0x4c8cf04	e00314aa	mov x0,x20
0x4c8cf08	add3ed96	bl 0x00801dbc
0x4c8cf0c	200020d4	brk #0x1
