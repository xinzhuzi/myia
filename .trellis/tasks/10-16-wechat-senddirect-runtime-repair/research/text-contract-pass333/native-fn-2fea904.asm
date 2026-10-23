0x2fea904	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x2fea908	fd7b01a9	stp x29,x30,[sp, #0x10]
0x2fea90c	fd430091	add x29,sp,#0x10
0x2fea910	136040f9	ldr x19,[x0, #0xc0]
0x2fea914	b30100b4	cbz x19,0x02fea948
0x2fea918	68220091	add x8,x19,#0x8
0x2fea91c	09008092	mov x9,#-0x1
0x2fea920	0801e9f8	ldaddal x9,x8,[x8]
0x2fea924	280100b5	cbnz x8,0x02fea948
0x2fea928	680240f9	ldr x8,[x19]
0x2fea92c	080940f9	ldr x8,[x8, #0x10]
0x2fea930	f40300aa	mov x20,x0
0x2fea934	e00313aa	mov x0,x19
0x2fea938	00013fd6	blr x8
0x2fea93c	e00313aa	mov x0,x19
0x2fea940	b7540595	bl 0x0713fc1c
0x2fea944	e00314aa	mov x0,x20
0x2fea948	f30300aa	mov x19,x0
0x2fea94c	00200091	add x0,x0,#0x8
0x2fea950	9d6cff97	bl 0x02fc5bc4
0x2fea954	e00313aa	mov x0,x19
0x2fea958	01198052	mov w1,#0xc8
0x2fea95c	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x2fea960	f44fc2a8	ldp x20,x19,[sp], #0x20
0x2fea964	aa550515	b 0x0714000c
