0x2ebf1d8	ffc300d1	sub sp,sp,#0x30
0x2ebf1dc	f44f01a9	stp x20,x19,[sp, #0x10]
0x2ebf1e0	fd7b02a9	stp x29,x30,[sp, #0x20]
0x2ebf1e4	fd830091	add x29,sp,#0x20
0x2ebf1e8	f30300aa	mov x19,x0
0x2ebf1ec	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x2ebf1f0	c87803f0	adrp x8,0x9dda000
0x2ebf1f4	08612e91	add x8,x8,#0xb98
0x2ebf1f8	080000f9	str x8,[x0]
0x2ebf1fc	292040a9	ldp x9,x8,[x1]
0x2ebf200	e92300a9	stp x9,x8,[sp]
0x2ebf204	880000b4	cbz x8,0x02ebf214
0x2ebf208	08210091	add x8,x8,#0x8
0x2ebf20c	29008052	mov w9,#0x1
0x2ebf210	080129f8	ldadd x9,x8,[x8]
0x2ebf214	60620091	add x0,x19,#0x18
0x2ebf218	e1030091	mov x1,sp
0x2ebf21c	22008052	mov w2,#0x1
0x2ebf220	8fca0894	bl 0x030f1c5c
0x2ebf224	f40740f9	ldr x20,[sp, #0x8]
0x2ebf228	740100b4	cbz x20,0x02ebf254
0x2ebf22c	88220091	add x8,x20,#0x8
0x2ebf230	09008092	mov x9,#-0x1
0x2ebf234	0801e9f8	ldaddal x9,x8,[x8]
0x2ebf238	e80000b5	cbnz x8,0x02ebf254
0x2ebf23c	880240f9	ldr x8,[x20]
0x2ebf240	080940f9	ldr x8,[x8, #0x10]
0x2ebf244	e00314aa	mov x0,x20
0x2ebf248	00013fd6	blr x8
0x2ebf24c	e00314aa	mov x0,x20
0x2ebf250	73020a95	bl 0x0713fc1c
0x2ebf254	e00313aa	mov x0,x19
0x2ebf258	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x2ebf25c	f44f41a9	ldp x20,x19,[sp, #0x10]
0x2ebf260	ffc30091	add sp,sp,#0x30
0x2ebf264	c0035fd6	ret
