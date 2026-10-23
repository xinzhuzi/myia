0x3b1afc	ffc301d1	sub sp,sp,#0x70
0x3b1b00	fa6702a9	stp x26,x25,[sp, #0x20]
0x3b1b04	f85f03a9	stp x24,x23,[sp, #0x30]
0x3b1b08	f65704a9	stp x22,x21,[sp, #0x40]
0x3b1b0c	f44f05a9	stp x20,x19,[sp, #0x50]
0x3b1b10	fd7b06a9	stp x29,x30,[sp, #0x60]
0x3b1b14	fd830191	add x29,sp,#0x60
0x3b1b18	f50302aa	mov x21,x2
0x3b1b1c	f40301aa	mov x20,x1
0x3b1b20	f30300aa	mov x19,x0
0x3b1b24	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x3b1b28	e8a300a9	stp x8,x8,[sp, #0x8]
0x3b1b2c	e0230091	add x0,sp,#0x8
0x3b1b30	e10313aa	mov x1,x19
0x3b1b34	a437b695	bl 0x0713f9c4
0x3b1b38	e8234039	ldrb w8,[sp, #0x8]
0x3b1b3c	1f050071	cmp w8,#0x1
0x3b1b40	61050054	b.ne 0x003b1bec
0x3b1b44	680240f9	ldr x8,[x19]
0x3b1b48	08815ef8	ldur x8,[x8, #-0x18]
0x3b1b4c	6402088b	add x4,x19,x8
0x3b1b50	961440f9	ldr x22,[x4, #0x28]
0x3b1b54	980840b9	ldr w24,[x4, #0x8]
0x3b1b58	979040b9	ldr w23,[x4, #0x90]
0x3b1b5c	ff060031	cmn w23,#0x1
0x3b1b60	41020054	b.ne 0x003b1ba8
0x3b1b64	e8630091	add x8,sp,#0x18
0x3b1b68	f90304aa	mov x25,x4
0x3b1b6c	e00304aa	mov x0,x4
0x3b1b70	c336b695	bl 0x0713f67c
0x3b1b74	21bc04b0	adrp x1,0x9b36000
0x3b1b78	21e443f9	ldr x1,[x1, #0x7c8]
0x3b1b7c	e0630091	add x0,sp,#0x18
0x3b1b80	b936b695	bl 0x0713f664
0x3b1b84	080040f9	ldr x8,[x0]
0x3b1b88	081d40f9	ldr x8,[x8, #0x38]
0x3b1b8c	01048052	mov w1,#0x20
0x3b1b90	00013fd6	blr x8
0x3b1b94	f70300aa	mov x23,x0
0x3b1b98	e0630091	add x0,sp,#0x18
0x3b1b9c	9538b695	bl 0x0713fdf0
0x3b1ba0	e40319aa	mov x4,x25
0x3b1ba4	379300b9	str w23,[x25, #0x90]
0x3b1ba8	08168052	mov w8,#0xb0
0x3b1bac	0803080a	and w8,w24,w8
0x3b1bb0	8302158b	add x3,x20,x21
0x3b1bb4	1f810071	cmp w8,#0x20
0x3b1bb8	6200949a	csel x2,x3,x20,eq
0x3b1bbc	e51e0013	sxtb w5,w23
0x3b1bc0	e00316aa	mov x0,x22
0x3b1bc4	e10314aa	mov x1,x20
0x3b1bc8	2a000094	bl 0x003b1c70
0x3b1bcc	000100b5	cbnz x0,0x003b1bec
0x3b1bd0	680240f9	ldr x8,[x19]
0x3b1bd4	08815ef8	ldur x8,[x8, #-0x18]
0x3b1bd8	6002088b	add x0,x19,x8
0x3b1bdc	082040b9	ldr w8,[x0, #0x20]
0x3b1be0	a9008052	mov w9,#0x5
0x3b1be4	0101092a	orr w1,w8,w9
0x3b1be8	b538b695	bl 0x0713febc
0x3b1bec	e0230091	add x0,sp,#0x8
0x3b1bf0	7837b695	bl 0x0713f9d0
0x3b1bf4	e00313aa	mov x0,x19
0x3b1bf8	fd7b46a9	ldp x29,x30,[sp, #0x60]
0x3b1bfc	f44f45a9	ldp x20,x19,[sp, #0x50]
0x3b1c00	f65744a9	ldp x22,x21,[sp, #0x40]
0x3b1c04	f85f43a9	ldp x24,x23,[sp, #0x30]
0x3b1c08	fa6742a9	ldp x26,x25,[sp, #0x20]
0x3b1c0c	ffc30191	add sp,sp,#0x70
0x3b1c10	c0035fd6	ret
