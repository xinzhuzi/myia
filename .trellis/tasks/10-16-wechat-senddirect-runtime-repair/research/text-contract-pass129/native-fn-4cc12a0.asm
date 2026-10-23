0x4cc12a0	ff8301d1	sub sp,sp,#0x60
0x4cc12a4	f44f04a9	stp x20,x19,[sp, #0x40]
0x4cc12a8	fd7b05a9	stp x29,x30,[sp, #0x50]
0x4cc12ac	fd430191	add x29,sp,#0x50
0x4cc12b0	f30301aa	mov x19,x1
0x4cc12b4	e10300aa	mov x1,x0
0x4cc12b8	f40308aa	mov x20,x8
0x4cc12bc	e0030091	mov x0,sp
0x4cc12c0	acbf0194	bl 0x04d31170
0x4cc12c4	e0030091	mov x0,sp
0x4cc12c8	e80314aa	mov x8,x20
0x4cc12cc	e10313aa	mov x1,x19
0x4cc12d0	b0a41197	bl 0x0112a590
0x4cc12d4	e8ffc039	ldrsb w8,[sp, #0x3f]
0x4cc12d8	e800f837	tbnz w8,#0x1f,0x04cc12f4
0x4cc12dc	e85fc039	ldrsb w8,[sp, #0x17]
0x4cc12e0	6801f837	tbnz w8,#0x1f,0x04cc130c
0x4cc12e4	fd7b45a9	ldp x29,x30,[sp, #0x50]
0x4cc12e8	f44f44a9	ldp x20,x19,[sp, #0x40]
0x4cc12ec	ff830191	add sp,sp,#0x60
0x4cc12f0	c0035fd6	ret
0x4cc12f4	e01740f9	ldr x0,[sp, #0x28]
0x4cc12f8	e81f40f9	ldr x8,[sp, #0x38]
0x4cc12fc	01f94092	and x1,x8,#0x7fffffffffffffff
0x4cc1300	43fb9194	bl 0x0714000c
0x4cc1304	e85fc039	ldrsb w8,[sp, #0x17]
0x4cc1308	e8feff36	tbz w8,#0x1f,0x04cc12e4
0x4cc130c	e00340f9	ldr x0,[sp]
0x4cc1310	e80b40f9	ldr x8,[sp, #0x10]
0x4cc1314	01f94092	and x1,x8,#0x7fffffffffffffff
0x4cc1318	3dfb9194	bl 0x0714000c
0x4cc131c	f2ffff17	b 0x04cc12e4
