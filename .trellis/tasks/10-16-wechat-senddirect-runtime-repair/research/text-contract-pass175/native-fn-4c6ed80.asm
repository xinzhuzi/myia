0x4c6ed80	ff4302d1	sub sp,sp,#0x90
0x4c6ed84	f65706a9	stp x22,x21,[sp, #0x60]
0x4c6ed88	f44f07a9	stp x20,x19,[sp, #0x70]
0x4c6ed8c	fd7b08a9	stp x29,x30,[sp, #0x80]
0x4c6ed90	fd030291	add x29,sp,#0x80
0x4c6ed94	f40301aa	mov x20,x1
0x4c6ed98	f30308aa	mov x19,x8
0x4c6ed9c	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x4c6eda0	a8233da9	stp x8,x8,[x29, #-0x30]
0x4c6eda4	292040a9	ldp x9,x8,[x1]
0x4c6eda8	e92304a9	stp x9,x8,[sp, #0x40]
0x4c6edac	880000b4	cbz x8,0x04c6edbc
0x4c6edb0	08210091	add x8,x8,#0x8
0x4c6edb4	29008052	mov w9,#0x1
0x4c6edb8	080129f8	ldadd x9,x8,[x8]
0x4c6edbc	a8c300d1	sub x8,x29,#0x30
0x4c6edc0	e1030191	add x1,sp,#0x40
0x4c6edc4	fdf1ff97	bl 0x04c6b5b8
0x4c6edc8	f52740f9	ldr x21,[sp, #0x48]
0x4c6edcc	750100b4	cbz x21,0x04c6edf8
0x4c6edd0	a8220091	add x8,x21,#0x8
0x4c6edd4	09008092	mov x9,#-0x1
0x4c6edd8	0801e9f8	ldaddal x9,x8,[x8]
0x4c6eddc	e80000b5	cbnz x8,0x04c6edf8
0x4c6ede0	a80240f9	ldr x8,[x21]
0x4c6ede4	080940f9	ldr x8,[x8, #0x10]
0x4c6ede8	e00315aa	mov x0,x21
0x4c6edec	00013fd6	blr x8
0x4c6edf0	e00315aa	mov x0,x21
0x4c6edf4	8a439394	bl 0x0713fc1c
0x4c6edf8	940240f9	ldr x20,[x20]
0x4c6edfc	800e41f9	ldr x0,[x20, #0x218]
0x4c6ee00	000a00b4	cbz x0,0x04c6ef40
0x4c6ee04	019202f0	adrp x1,0x9eb1000
0x4c6ee08	21000191	add x1,x1,#0x40
0x4c6ee0c	029202d0	adrp x2,0x9eb0000
0x4c6ee10	42003391	add x2,x2,#0xcc0
0x4c6ee14	030080d2	mov x3,#0x0
0x4c6ee18	c5449394	bl 0x0714012c
0x4c6ee1c	200900b4	cbz x0,0x04c6ef40
0x4c6ee20	881241f9	ldr x8,[x20, #0x220]
0x4c6ee24	e02303a9	stp x0,x8,[sp, #0x30]
0x4c6ee28	880000b4	cbz x8,0x04c6ee38
0x4c6ee2c	08210091	add x8,x8,#0x8
0x4c6ee30	29008052	mov w9,#0x1
0x4c6ee34	080129f8	ldadd x9,x8,[x8]
0x4c6ee38	158842f9	ldr x21,[x0, #0x510]
0x4c6ee3c	148c42f9	ldr x20,[x0, #0x518]
0x4c6ee40	f55302a9	stp x21,x20,[sp, #0x20]
0x4c6ee44	940000b4	cbz x20,0x04c6ee54
0x4c6ee48	88220091	add x8,x20,#0x8
0x4c6ee4c	29008052	mov w9,#0x1
0x4c6ee50	080129f8	ldadd x9,x8,[x8]
0x4c6ee54	b50300b4	cbz x21,0x04c6eec8
0x4c6ee58	b6035df8	ldur x22,[x29, #-0x30]
0x4c6ee5c	74e10694	bl 0x04e2742c
0x4c6ee60	e8230091	add x8,sp,#0x8
0x4c6ee64	e10315aa	mov x1,x21
0x4c6ee68	42449394	bl 0x0713ff70
0x4c6ee6c	c0c20491	add x0,x22,#0x130
0x4c6ee70	e1230091	add x1,sp,#0x8
0x4c6ee74	9b429394	bl 0x0713f8e0
0x4c6ee78	e87fc039	ldrsb w8,[sp, #0x1f]
0x4c6ee7c	a800f836	tbz w8,#0x1f,0x04c6ee90
0x4c6ee80	e00740f9	ldr x0,[sp, #0x8]
0x4c6ee84	e80f40f9	ldr x8,[sp, #0x18]
0x4c6ee88	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6ee8c	60449394	bl 0x0714000c
0x4c6ee90	b6035df8	ldur x22,[x29, #-0x30]
0x4c6ee94	66e10694	bl 0x04e2742c
0x4c6ee98	e8230091	add x8,sp,#0x8
0x4c6ee9c	e10315aa	mov x1,x21
0x4c6eea0	34449394	bl 0x0713ff70
0x4c6eea4	c0220591	add x0,x22,#0x148
0x4c6eea8	e1230091	add x1,sp,#0x8
0x4c6eeac	8d429394	bl 0x0713f8e0
0x4c6eeb0	e87fc039	ldrsb w8,[sp, #0x1f]
0x4c6eeb4	a800f836	tbz w8,#0x1f,0x04c6eec8
0x4c6eeb8	e00740f9	ldr x0,[sp, #0x8]
0x4c6eebc	e80f40f9	ldr x8,[sp, #0x18]
0x4c6eec0	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6eec4	52449394	bl 0x0714000c
0x4c6eec8	740100b4	cbz x20,0x04c6eef4
0x4c6eecc	88220091	add x8,x20,#0x8
0x4c6eed0	09008092	mov x9,#-0x1
0x4c6eed4	0801e9f8	ldaddal x9,x8,[x8]
0x4c6eed8	e80000b5	cbnz x8,0x04c6eef4
0x4c6eedc	880240f9	ldr x8,[x20]
0x4c6eee0	080940f9	ldr x8,[x8, #0x10]
0x4c6eee4	e00314aa	mov x0,x20
0x4c6eee8	00013fd6	blr x8
0x4c6eeec	e00314aa	mov x0,x20
0x4c6eef0	4b439394	bl 0x0713fc1c
0x4c6eef4	a003dd3c	ldur q0,[x29, #-0x30]
0x4c6eef8	0800669e	fmov x8,d0
0x4c6eefc	29008052	mov w9,#0x1
0x4c6ef00	090900b9	str w9,[x8, #0x8]
0x4c6ef04	6002803d	str q0,[x19]
0x4c6ef08	bf7f3da9	stp xzr,xzr,[x29, #-0x30]
0x4c6ef0c	f31f40f9	ldr x19,[sp, #0x38]
0x4c6ef10	b30100b4	cbz x19,0x04c6ef44
0x4c6ef14	68220091	add x8,x19,#0x8
0x4c6ef18	09008092	mov x9,#-0x1
0x4c6ef1c	0801e9f8	ldaddal x9,x8,[x8]
0x4c6ef20	280100b5	cbnz x8,0x04c6ef44
0x4c6ef24	680240f9	ldr x8,[x19]
0x4c6ef28	080940f9	ldr x8,[x8, #0x10]
0x4c6ef2c	e00313aa	mov x0,x19
0x4c6ef30	00013fd6	blr x8
0x4c6ef34	e00313aa	mov x0,x19
0x4c6ef38	39439394	bl 0x0713fc1c
0x4c6ef3c	02000014	b 0x04c6ef44
0x4c6ef40	7f7e00a9	stp xzr,xzr,[x19]
0x4c6ef44	b3835df8	ldur x19,[x29, #-0x28]
0x4c6ef48	730100b4	cbz x19,0x04c6ef74
0x4c6ef4c	68220091	add x8,x19,#0x8
0x4c6ef50	09008092	mov x9,#-0x1
0x4c6ef54	0801e9f8	ldaddal x9,x8,[x8]
0x4c6ef58	e80000b5	cbnz x8,0x04c6ef74
0x4c6ef5c	680240f9	ldr x8,[x19]
0x4c6ef60	080940f9	ldr x8,[x8, #0x10]
0x4c6ef64	e00313aa	mov x0,x19
0x4c6ef68	00013fd6	blr x8
0x4c6ef6c	e00313aa	mov x0,x19
0x4c6ef70	2b439394	bl 0x0713fc1c
0x4c6ef74	fd7b48a9	ldp x29,x30,[sp, #0x80]
0x4c6ef78	f44f47a9	ldp x20,x19,[sp, #0x70]
0x4c6ef7c	f65746a9	ldp x22,x21,[sp, #0x60]
0x4c6ef80	ff430291	add sp,sp,#0x90
0x4c6ef84	c0035fd6	ret
