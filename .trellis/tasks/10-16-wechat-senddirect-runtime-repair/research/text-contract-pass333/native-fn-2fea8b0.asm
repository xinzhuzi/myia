0x2fea8b0	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x2fea8b4	fd7b01a9	stp x29,x30,[sp, #0x10]
0x2fea8b8	fd430091	add x29,sp,#0x10
0x2fea8bc	136040f9	ldr x19,[x0, #0xc0]
0x2fea8c0	b30100b4	cbz x19,0x02fea8f4
0x2fea8c4	68220091	add x8,x19,#0x8
0x2fea8c8	09008092	mov x9,#-0x1
0x2fea8cc	0801e9f8	ldaddal x9,x8,[x8]
0x2fea8d0	280100b5	cbnz x8,0x02fea8f4
0x2fea8d4	680240f9	ldr x8,[x19]
0x2fea8d8	080940f9	ldr x8,[x8, #0x10]
0x2fea8dc	f40300aa	mov x20,x0
0x2fea8e0	e00313aa	mov x0,x19
0x2fea8e4	00013fd6	blr x8
0x2fea8e8	e00313aa	mov x0,x19
0x2fea8ec	cc540595	bl 0x0713fc1c
0x2fea8f0	e00314aa	mov x0,x20
0x2fea8f4	00200091	add x0,x0,#0x8
0x2fea8f8	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x2fea8fc	f44fc2a8	ldp x20,x19,[sp], #0x20
0x2fea900	b16cff17	b 0x02fc5bc4
