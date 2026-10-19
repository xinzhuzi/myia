// FUN_05a6c22c 05a6c22c
05a6c22c	sub sp,sp,#0x70
05a6c230	stp x22,x21,[sp, #0x40]
05a6c234	stp x20,x19,[sp, #0x50]
05a6c238	stp x29,x30,[sp, #0x60]
05a6c23c	add x29,sp,#0x60
05a6c240	mov x20,x1
05a6c244	mov x19,x0
05a6c248	cmp x1,x0
05a6c24c	b.ne 0x05a6c28c
05a6c250	adrp x2,0x9883000
05a6c254	add x2,x2,#0xa4e
05a6c258	add x0,sp,#0x10
05a6c25c	mov w1,#0x3
05a6c260	mov w3,#0x264
05a6c264	bl 0x05ab442c
05a6c268	adrp x1,0x9859000
05a6c26c	add x1,x1,#0x34f
05a6c270	add x0,sp,#0x10
05a6c274	bl 0x05ab4444
05a6c278	mov x1,x0
05a6c27c	add x0,sp,#0xf
05a6c280	bl 0x05ab4574
05a6c284	add x0,sp,#0x10
05a6c288	bl 0x05ab457c
05a6c28c	ldrb w8,[x20, #0x24]
05a6c290	cbz w8,0x05a6c2c0
05a6c294	adrp x22,0xa524000
05a6c298	add x22,x22,#0xad0
05a6c29c	tbnz w8,#0x0,0x05a6c2d4
05a6c2a0	tbnz w8,#0x1,0x05a6c314
05a6c2a4	tbnz w8,#0x2,0x05a6c330
05a6c2a8	tbz w8,#0x3,0x05a6c2c0
05a6c2ac	ldr w8,[x20, #0x1c]
05a6c2b0	ldr w9,[x19, #0x24]
05a6c2b4	orr w9,w9,#0x8
05a6c2b8	str w9,[x19, #0x24]
05a6c2bc	str w8,[x19, #0x1c]
05a6c2c0	ldp x29,x30,[sp, #0x60]
05a6c2c4	ldp x20,x19,[sp, #0x50]
05a6c2c8	ldp x22,x21,[sp, #0x40]
05a6c2cc	add sp,sp,#0x70
05a6c2d0	ret
05a6c2d4	ldr x21,[x20, #0x8]
05a6c2d8	ldr w8,[x19, #0x24]
05a6c2dc	orr w8,w8,#0x1
05a6c2e0	str w8,[x19, #0x24]
05a6c2e4	ldr x0,[x19, #0x8]
05a6c2e8	cmp x0,x22
05a6c2ec	b.ne 0x05a6c304
05a6c2f0	mov w0,#0x18
05a6c2f4	bl 0x07140030
05a6c2f8	stp xzr,xzr,[x0, #0x8]
05a6c2fc	str xzr,[x0]
05a6c300	str x0,[x19, #0x8]
05a6c304	mov x1,x21
05a6c308	bl 0x0713f8e0
05a6c30c	ldr w8,[x20, #0x24]
05a6c310	tbz w8,#0x1,0x05a6c2a4
05a6c314	ldr w8,[x20, #0x18]
05a6c318	ldr w9,[x19, #0x24]
05a6c31c	orr w9,w9,#0x2
05a6c320	str w9,[x19, #0x24]
05a6c324	str w8,[x19, #0x18]
05a6c328	ldr w8,[x20, #0x24]
05a6c32c	tbz w8,#0x2,0x05a6c2a8
05a6c330	ldr x21,[x20, #0x10]
05a6c334	ldr w8,[x19, #0x24]
05a6c338	orr w8,w8,#0x4
05a6c33c	str w8,[x19, #0x24]
05a6c340	ldr x0,[x19, #0x10]
05a6c344	cmp x0,x22
05a6c348	b.ne 0x05a6c360
05a6c34c	mov w0,#0x18
05a6c350	bl 0x07140030
05a6c354	stp xzr,xzr,[x0, #0x8]
05a6c358	str xzr,[x0]
05a6c35c	str x0,[x19, #0x10]
05a6c360	mov x1,x21
05a6c364	bl 0x0713f8e0
05a6c368	ldr w8,[x20, #0x24]
05a6c36c	tbnz w8,#0x3,0x05a6c2ac
05a6c370	b 0x05a6c2c0
