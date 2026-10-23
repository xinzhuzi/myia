0x2e86b60	ff0302d1	sub sp,sp,#0x80
0x2e86b64	f85f04a9	stp x24,x23,[sp, #0x40]
0x2e86b68	f65705a9	stp x22,x21,[sp, #0x50]
0x2e86b6c	f44f06a9	stp x20,x19,[sp, #0x60]
0x2e86b70	fd7b07a9	stp x29,x30,[sp, #0x70]
0x2e86b74	fdc30191	add x29,sp,#0x70
0x2e86b78	f30300aa	mov x19,x0
0x2e86b7c	88ec99d2	mov x8,#0xcf64
0x2e86b80	0888aaf2	movk x8,#0x5440, LSL #16
0x2e86b84	4847d6f2	movk x8,#0xb23a, LSL #32
0x2e86b88	e80ce0f2	movk x8,#0x67, LSL #48
0x2e86b8c	092840a9	ldp x9,x10,[x0]
0x2e86b90	4a0109cb	sub x10,x10,x9
0x2e86b94	4afd4393	asr x10,x10,#0x3
0x2e86b98	ebd582d2	mov x11,#0x16af
0x2e86b9c	eb26acf2	movk x11,#0x6137, LSL #16
0x2e86ba0	cbefcaf2	movk x11,#0x577e, LSL #32
0x2e86ba4	6b71f3f2	movk x11,#0x9b8b, LSL #48
0x2e86ba8	547d0b9b	mul x20,x10,x11
0x2e86bac	8a060091	add x10,x20,#0x1
0x2e86bb0	5f0108eb	cmp x10,x8
0x2e86bb4	c8090054	b.hi 0x02e86cec
0x2e86bb8	6c420091	add x12,x19,#0x10
0x2e86bbc	8d0140f9	ldr x13,[x12]
0x2e86bc0	a90109cb	sub x9,x13,x9
0x2e86bc4	29fd4393	asr x9,x9,#0x3
0x2e86bc8	297d0b9b	mul x9,x9,x11
0x2e86bcc	2bf97fd3	lsl x11,x9,#0x1
0x2e86bd0	7f010aeb	cmp x11,x10
0x2e86bd4	6a818a9a	csel x10,x11,x10,hi
0x2e86bd8	4bf68cd2	mov x11,#0x67b2
0x2e86bdc	0b44a5f2	movk x11,#0x2a20, LSL #16
0x2e86be0	ab23dbf2	movk x11,#0xd91d, LSL #32
0x2e86be4	6b06e0f2	movk x11,#0x33, LSL #48
0x2e86be8	3f010beb	cmp x9,x11
0x2e86bec	5531889a	csel x21,x10,x8,cc
0x2e86bf0	ec1b00f9	str x12,[sp, #0x30]
0x2e86bf4	350100b4	cbz x21,0x02e86c18
0x2e86bf8	bf0208eb	cmp x21,x8
0x2e86bfc	c8070054	b.hi 0x02e86cf4
0x2e86c00	f60301aa	mov x22,x1
0x2e86c04	084f8052	mov w8,#0x278
0x2e86c08	a07e089b	mul x0,x21,x8
0x2e86c0c	09e50a95	bl 0x07140030
0x2e86c10	e10316aa	mov x1,x22
0x2e86c14	02000014	b 0x02e86c1c
0x2e86c18	000080d2	mov x0,#0x0
0x2e86c1c	00e4006f	movi v0.2D,#0x0
0x2e86c20	e08300ad	stp q0,q0,[sp, #0x10]
0x2e86c24	094f8052	mov w9,#0x278
0x2e86c28	8802099b	madd x8,x20,x9,x0
0x2e86c2c	e02301a9	stp x0,x8,[sp, #0x10]
0x2e86c30	a902099b	madd x9,x21,x9,x0
0x2e86c34	e82702a9	stp x8,x9,[sp, #0x20]
0x2e86c38	e00308aa	mov x0,x8
0x2e86c3c	7d428397	bl 0x00f57630
0x2e86c40	140080d2	mov x20,#0x0
0x2e86c44	f5a341a9	ldp x21,x8,[sp, #0x18]
0x2e86c48	08e10991	add x8,x8,#0x278
0x2e86c4c	e81300f9	str x8,[sp, #0x20]
0x2e86c50	775a40a9	ldp x23,x22,[x19]
0x2e86c54	c802148b	add x8,x22,x20
0x2e86c58	1f0117eb	cmp x8,x23
0x2e86c5c	c0000054	b.eq 0x02e86c74
0x2e86c60	94e209d1	sub x20,x20,#0x278
0x2e86c64	8002158b	add x0,x20,x21
0x2e86c68	8102168b	add x1,x20,x22
0x2e86c6c	71428397	bl 0x00f57630
0x2e86c70	f9ffff17	b 0x02e86c54
0x2e86c74	a902148b	add x9,x21,x20
0x2e86c78	742240a9	ldp x20,x8,[x19]
0x2e86c7c	690200f9	str x9,[x19]
0x2e86c80	750a40f9	ldr x21,[x19, #0x10]
0x2e86c84	e00bc03d	ldr q0,[sp, #0x20]
0x2e86c88	e003803d	str q0,[sp]
0x2e86c8c	6082803c	stur q0,[x19, #0x8]
0x2e86c90	1f0114eb	cmp x8,x20
0x2e86c94	40010054	b.eq 0x02e86cbc
0x2e86c98	13e109d1	sub x19,x8,#0x278
0x2e86c9c	680240f9	ldr x8,[x19]
0x2e86ca0	080140f9	ldr x8,[x8]
0x2e86ca4	e00313aa	mov x0,x19
0x2e86ca8	00013fd6	blr x8
0x2e86cac	68e209d1	sub x8,x19,#0x278
0x2e86cb0	7f0214eb	cmp x19,x20
0x2e86cb4	f30308aa	mov x19,x8
0x2e86cb8	21ffff54	b.ne 0x02e86c9c
0x2e86cbc	940000b4	cbz x20,0x02e86ccc
0x2e86cc0	a10214cb	sub x1,x21,x20
0x2e86cc4	e00314aa	mov x0,x20
0x2e86cc8	d1e40a95	bl 0x0714000c
0x2e86ccc	e003c03d	ldr q0,[sp]
0x2e86cd0	0000669e	fmov x0,d0
0x2e86cd4	fd7b47a9	ldp x29,x30,[sp, #0x70]
0x2e86cd8	f44f46a9	ldp x20,x19,[sp, #0x60]
0x2e86cdc	f65745a9	ldp x22,x21,[sp, #0x50]
0x2e86ce0	f85f44a9	ldp x24,x23,[sp, #0x40]
0x2e86ce4	ff030291	add sp,sp,#0x80
0x2e86ce8	c0035fd6	ret
0x2e86cec	e00313aa	mov x0,x19
0x2e86cf0	66f1ff97	bl 0x02e83288
0x2e86cf4	738a4d97	bl 0x001e96c0
