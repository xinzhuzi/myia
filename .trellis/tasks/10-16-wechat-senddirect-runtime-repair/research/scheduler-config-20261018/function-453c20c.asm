0x453c20c	ffc303d1	sub	sp, sp, #0xf0
0x453c210	f85f0ba9	stp	x24, x23, [sp, #0xb0]
0x453c214	f6570ca9	stp	x22, x21, [sp, #0xc0]
0x453c218	f44f0da9	stp	x20, x19, [sp, #0xd0]
0x453c21c	fd7b0ea9	stp	x29, x30, [sp, #0xe0]
0x453c220	fd830391	add	x29, sp, #0xe0
0x453c224	f50304aa	mov	x21, x4
0x453c228	f60302aa	mov	x22, x2
0x453c22c	f80300aa	mov	x24, x0
0x453c230	f30308aa	mov	x19, x8
0x453c234	c8af02d0	adrp	x8, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x453c238	084d46f9	ldr	x8, [x8, #0xc98]
0x453c23c	080140f9	ldr	x8, [x8]
0x453c240	a8831cf8	stur	x8, [x29, #-0x38]
0x453c244	c10000b4	cbz	x1, 0x453c25c <_WeChatMain+0x45229f0>
0x453c248	f70303aa	mov	x23, x3
0x453c24c	f40301aa	mov	x20, x1
0x453c250	20200091	add	x0, x1, #0x8
0x453c254	ad1a8594	bl	0x6682d08 <_SetWeixinCallbackFunc+0x189b90c>
0x453c258	20020036	tbz	w0, #0x0, 0x453c29c <_WeChatMain+0x4522a30>
0x453c25c	000740f9	ldr	x0, [x24, #0x8]
0x453c260	a8835cf8	ldur	x8, [x29, #-0x38]
0x453c264	c9af02d0	adrp	x9, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x453c268	294d46f9	ldr	x9, [x9, #0xc98]
0x453c26c	290140f9	ldr	x9, [x9]
0x453c270	3f0108eb	cmp	x9, x8
0x453c274	a10d0054	b.ne	0x453c428 <_WeChatMain+0x4522bbc>
0x453c278	e80313aa	mov	x8, x19
0x453c27c	e10316aa	mov	x1, x22
0x453c280	e20315aa	mov	x2, x21
0x453c284	fd7b4ea9	ldp	x29, x30, [sp, #0xe0]
0x453c288	f44f4da9	ldp	x20, x19, [sp, #0xd0]
0x453c28c	f6574ca9	ldp	x22, x21, [sp, #0xc0]
0x453c290	f85f4ba9	ldp	x24, x23, [sp, #0xb0]
0x453c294	ffc30391	add	sp, sp, #0xf0
0x453c298	b2feff17	b	0x453bd60 <_WeChatMain+0x45224f4>
0x453c29c	b88301d1	sub	x24, x29, #0x60
0x453c2a0	40e5054f	movi.16b	v0, #0xaa
0x453c2a4	a0033dad	stp	q0, q0, [x29, #-0x60]
0x453c2a8	a88301d1	sub	x8, x29, #0x60
0x453c2ac	e00317aa	mov	x0, x23
0x453c2b0	49060094	bl	0x453dbd4 <_WeChatMain+0x4524368>
0x453c2b4	e8230091	add	x8, sp, #0x8
0x453c2b8	e00316aa	mov	x0, x22
0x453c2bc	e10315aa	mov	x1, x21
0x453c2c0	b3060094	bl	0x453dd8c <_WeChatMain+0x4524520>
0x453c2c4	e87fc039	ldrsb	w8, [sp, #0x1f]
0x453c2c8	c800f837	tbnz	w8, #0x1f, 0x453c2e0 <_WeChatMain+0x4522a74>
0x453c2cc	e083c03c	ldur	q0, [sp, #0x8]
0x453c2d0	e00b803d	str	q0, [sp, #0x20]
0x453c2d4	e80f40f9	ldr	x8, [sp, #0x18]
0x453c2d8	e81b00f9	str	x8, [sp, #0x30]
0x453c2dc	04000014	b	0x453c2ec <_WeChatMain+0x4522a80>
0x453c2e0	e18b40a9	ldp	x1, x2, [sp, #0x8]
0x453c2e4	e0830091	add	x0, sp, #0x20
0x453c2e8	8e72eb96	bl	0x18d20 <__text+0x1d20>
0x453c2ec	e003679e	fmov	d0, xzr
0x453c2f0	0004186e	mov.d	v0[1], v0[0]
0x453c2f4	ff2700f9	str	xzr, [sp, #0x48]
0x453c2f8	e083833c	stur	q0, [sp, #0x38]
0x453c2fc	e0e5002f	movi	d0, #0x000000ffffffff
0x453c300	0040611e	fneg	d0, d0
0x453c304	e02b00fd	str	d0, [sp, #0x50]
0x453c308	a0835bf8	ldur	x0, [x29, #-0x48]
0x453c30c	e00000b4	cbz	x0, 0x453c328 <_WeChatMain+0x4522abc>
0x453c310	a88301d1	sub	x8, x29, #0x60
0x453c314	1f0008eb	cmp	x0, x8
0x453c318	00010054	b.eq	0x453c338 <_WeChatMain+0x4522acc>
0x453c31c	08630091	add	x8, x24, #0x18
0x453c320	e03f00f9	str	x0, [sp, #0x78]
0x453c324	03000014	b	0x453c330 <_WeChatMain+0x4522ac4>
0x453c328	e8830191	add	x8, sp, #0x60
0x453c32c	08610091	add	x8, x8, #0x18
0x453c330	1f0100f9	str	xzr, [x8]
0x453c334	07000014	b	0x453c350 <_WeChatMain+0x4522ae4>
0x453c338	e8830191	add	x8, sp, #0x60
0x453c33c	e83f00f9	str	x8, [sp, #0x78]
0x453c340	080040f9	ldr	x8, [x0]
0x453c344	080d40f9	ldr	x8, [x8, #0x18]
0x453c348	e1830191	add	x1, sp, #0x60
0x453c34c	00013fd6	blr	x8
0x453c350	f5830191	add	x21, sp, #0x60
0x453c354	e1830091	add	x1, sp, #0x20
0x453c358	e2830191	add	x2, sp, #0x60
0x453c35c	e80313aa	mov	x8, x19
0x453c360	e00314aa	mov	x0, x20
0x453c364	0a228594	bl	0x6684b8c <_SetWeixinCallbackFunc+0x189d790>
0x453c368	e03f40f9	ldr	x0, [sp, #0x78]
0x453c36c	1f0015eb	cmp	x0, x21
0x453c370	a0000054	b.eq	0x453c384 <_WeChatMain+0x4522b18>
0x453c374	e00000b4	cbz	x0, 0x453c390 <_WeChatMain+0x4522b24>
0x453c378	080040f9	ldr	x8, [x0]
0x453c37c	081540f9	ldr	x8, [x8, #0x28]
0x453c380	03000014	b	0x453c38c <_WeChatMain+0x4522b20>
0x453c384	080040f9	ldr	x8, [x0]
0x453c388	081140f9	ldr	x8, [x8, #0x20]
0x453c38c	00013fd6	blr	x8
0x453c390	e8dfc039	ldrsb	w8, [sp, #0x37]
0x453c394	6801f837	tbnz	w8, #0x1f, 0x453c3c0 <_WeChatMain+0x4522b54>
0x453c398	e87fc039	ldrsb	w8, [sp, #0x1f]
0x453c39c	e801f837	tbnz	w8, #0x1f, 0x453c3d8 <_WeChatMain+0x4522b6c>
0x453c3a0	a0835bf8	ldur	x0, [x29, #-0x48]
0x453c3a4	a88301d1	sub	x8, x29, #0x60
0x453c3a8	1f0008eb	cmp	x0, x8
0x453c3ac	00020054	b.eq	0x453c3ec <_WeChatMain+0x4522b80>
0x453c3b0	400200b4	cbz	x0, 0x453c3f8 <_WeChatMain+0x4522b8c>
0x453c3b4	080040f9	ldr	x8, [x0]
0x453c3b8	081540f9	ldr	x8, [x8, #0x28]
0x453c3bc	0e000014	b	0x453c3f4 <_WeChatMain+0x4522b88>
0x453c3c0	e01340f9	ldr	x0, [sp, #0x20]
0x453c3c4	e81b40f9	ldr	x8, [sp, #0x30]
0x453c3c8	01f94092	and	x1, x8, #0x7fffffffffffffff
0x453c3cc	100fb094	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x453c3d0	e87fc039	ldrsb	w8, [sp, #0x1f]
0x453c3d4	68feff36	tbz	w8, #0x1f, 0x453c3a0 <_WeChatMain+0x4522b34>
0x453c3d8	e00740f9	ldr	x0, [sp, #0x8]
0x453c3dc	e80f40f9	ldr	x8, [sp, #0x18]
0x453c3e0	01f94092	and	x1, x8, #0x7fffffffffffffff
0x453c3e4	0a0fb094	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x453c3e8	eeffff17	b	0x453c3a0 <_WeChatMain+0x4522b34>
0x453c3ec	080040f9	ldr	x8, [x0]
0x453c3f0	081140f9	ldr	x8, [x8, #0x20]
0x453c3f4	00013fd6	blr	x8
0x453c3f8	a8835cf8	ldur	x8, [x29, #-0x38]
0x453c3fc	c9af02d0	adrp	x9, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x453c400	294d46f9	ldr	x9, [x9, #0xc98]
0x453c404	290140f9	ldr	x9, [x9]
0x453c408	3f0108eb	cmp	x9, x8
0x453c40c	e1000054	b.ne	0x453c428 <_WeChatMain+0x4522bbc>
0x453c410	fd7b4ea9	ldp	x29, x30, [sp, #0xe0]
0x453c414	f44f4da9	ldp	x20, x19, [sp, #0xd0]
0x453c418	f6574ca9	ldp	x22, x21, [sp, #0xc0]
0x453c41c	f85f4ba9	ldp	x24, x23, [sp, #0xb0]
0x453c420	ffc30391	add	sp, sp, #0xf0
0x453c424	c0035fd6	ret
0x453c428	5f0fb094	bl	0x71401a4 <_wxam_enc_uninit_10+0x71401a4>
0x453c42c	096beb96	bl	0x17050 <__text+0x50>
0x453c430	f30300aa	mov	x19, x0
0x453c434	0c000014	b	0x453c464 <_WeChatMain+0x4522bf8>
0x453c438	f30300aa	mov	x19, x0
0x453c43c	e03f40f9	ldr	x0, [sp, #0x78]
0x453c440	1f0015eb	cmp	x0, x21
0x453c444	e0010054	b.eq	0x453c480 <_WeChatMain+0x4522c14>
0x453c448	fd5bae94	bl	0x70d343c <_SetWeixinCallbackFunc+0x22ec040>
0x453c44c	e8dfc039	ldrsb	w8, [sp, #0x37]
0x453c450	a800f836	tbz	w8, #0x1f, 0x453c464 <_WeChatMain+0x4522bf8>
0x453c454	e01340f9	ldr	x0, [sp, #0x20]
0x453c458	e81b40f9	ldr	x8, [sp, #0x30]
0x453c45c	01f94092	and	x1, x8, #0x7fffffffffffffff
0x453c460	eb0eb094	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x453c464	e87fc039	ldrsb	w8, [sp, #0x1f]
0x453c468	a801f836	tbz	w8, #0x1f, 0x453c49c <_WeChatMain+0x4522c30>
0x453c46c	e00740f9	ldr	x0, [sp, #0x8]
0x453c470	e80f40f9	ldr	x8, [sp, #0x18]
0x453c474	01f94092	and	x1, x8, #0x7fffffffffffffff
0x453c478	e50eb094	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x453c47c	08000014	b	0x453c49c <_WeChatMain+0x4522c30>
0x453c480	080040f9	ldr	x8, [x0]
0x453c484	081140f9	ldr	x8, [x8, #0x20]
0x453c488	00013fd6	blr	x8
0x453c48c	e8dfc039	ldrsb	w8, [sp, #0x37]
0x453c490	28feff37	tbnz	w8, #0x1f, 0x453c454 <_WeChatMain+0x4522be8>
0x453c494	f4ffff17	b	0x453c464 <_WeChatMain+0x4522bf8>
0x453c498	f30300aa	mov	x19, x0
0x453c49c	a0835bf8	ldur	x0, [x29, #-0x48]
0x453c4a0	a88301d1	sub	x8, x29, #0x60
0x453c4a4	1f0008eb	cmp	x0, x8
0x453c4a8	81000054	b.ne	0x453c4b8 <_WeChatMain+0x4522c4c>
0x453c4ac	080040f9	ldr	x8, [x0]
0x453c4b0	081140f9	ldr	x8, [x8, #0x20]
0x453c4b4	04000014	b	0x453c4c4 <_WeChatMain+0x4522c58>
0x453c4b8	800000b4	cbz	x0, 0x453c4c8 <_WeChatMain+0x4522c5c>
0x453c4bc	080040f9	ldr	x8, [x0]
0x453c4c0	081540f9	ldr	x8, [x8, #0x28]
0x453c4c4	00013fd6	blr	x8
0x453c4c8	e00313aa	mov	x0, x19
0x453c4cc	430bb094	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
