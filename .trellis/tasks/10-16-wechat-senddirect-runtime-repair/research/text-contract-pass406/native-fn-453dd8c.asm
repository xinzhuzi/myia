0x453dd8c	ff8301d1	sub sp,sp,#0x60
0x453dd90	f65703a9	stp x22,x21,[sp, #0x30]
0x453dd94	f44f04a9	stp x20,x19,[sp, #0x40]
0x453dd98	fd7b05a9	stp x29,x30,[sp, #0x50]
0x453dd9c	fd430191	add x29,sp,#0x50
0x453dda0	f40301aa	mov x20,x1
0x453dda4	f30308aa	mov x19,x8
0x453dda8	e8630091	add x8,sp,#0x18
0x453ddac	55feff97	bl 0x0453d700
0x453ddb0	c8f80290	adrp x8,0xa455000
0x453ddb4	09215f39	ldrb w9,[x8, #0x7c8]
0x453ddb8	e9000037	tbnz w9,#0x0,0x0453ddd4
0x453ddbc	c9f80290	adrp x9,0xa455000
0x453ddc0	29191f91	add x9,x9,#0x7c6
0x453ddc4	4a078052	mov w10,#0x3a
0x453ddc8	2a010079	strh w10,[x9]
0x453ddcc	29008052	mov w9,#0x1
0x453ddd0	09211f39	strb w9,[x8, #0x7c8]
0x453ddd4	c1f80290	adrp x1,0xa455000
0x453ddd8	21181f91	add x1,x1,#0x7c6
0x453dddc	e0630091	add x0,sp,#0x18
0x453dde0	7e06b094	bl 0x0713f7d8
0x453dde4	f50300aa	mov x21,x0
0x453dde8	f6030091	mov x22,sp
0x453ddec	e8030091	mov x8,sp
0x453ddf0	e00314aa	mov x0,x20
0x453ddf4	4d08b094	bl 0x0713ff28
0x453ddf8	e85f4039	ldrb w8,[sp, #0x17]
0x453ddfc	091d0013	sxtb w9,w8
0x453de00	ea2f40a9	ldp x10,x11,[sp]
0x453de04	3f010071	cmp w9,#0x0
0x453de08	41b1969a	csel x1,x10,x22,lt
0x453de0c	62b1889a	csel x2,x11,x8,lt
0x453de10	e00315aa	mov x0,x21
0x453de14	7406b094	bl 0x0713f7e4
0x453de18	085cc039	ldrsb w8,[x0, #0x17]
0x453de1c	c800f837	tbnz w8,#0x1f,0x0453de34
0x453de20	0000c03d	ldr q0,[x0]
0x453de24	080840f9	ldr x8,[x0, #0x10]
0x453de28	680a00f9	str x8,[x19, #0x10]
0x453de2c	6002803d	str q0,[x19]
0x453de30	04000014	b 0x0453de40
0x453de34	010840a9	ldp x1,x2,[x0]
0x453de38	e00313aa	mov x0,x19
0x453de3c	b96beb96	bl 0x00018d20
0x453de40	e85fc039	ldrsb w8,[sp, #0x17]
0x453de44	0801f837	tbnz w8,#0x1f,0x0453de64
0x453de48	e8bfc039	ldrsb w8,[sp, #0x2f]
0x453de4c	8801f837	tbnz w8,#0x1f,0x0453de7c
0x453de50	fd7b45a9	ldp x29,x30,[sp, #0x50]
0x453de54	f44f44a9	ldp x20,x19,[sp, #0x40]
0x453de58	f65743a9	ldp x22,x21,[sp, #0x30]
0x453de5c	ff830191	add sp,sp,#0x60
0x453de60	c0035fd6	ret
0x453de64	e00340f9	ldr x0,[sp]
0x453de68	e80b40f9	ldr x8,[sp, #0x10]
0x453de6c	01f94092	and x1,x8,#0x7fffffffffffffff
0x453de70	6708b094	bl 0x0714000c
0x453de74	e8bfc039	ldrsb w8,[sp, #0x2f]
0x453de78	c8feff36	tbz w8,#0x1f,0x0453de50
0x453de7c	e00f40f9	ldr x0,[sp, #0x18]
0x453de80	e81740f9	ldr x8,[sp, #0x28]
0x453de84	01f94092	and x1,x8,#0x7fffffffffffffff
0x453de88	6108b094	bl 0x0714000c
0x453de8c	f1ffff17	b 0x0453de50
