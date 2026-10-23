0x6674c94	ff4301d1	sub	sp, sp, #0x50
0x6674c98	f44f03a9	stp	x20, x19, [sp, #0x30]
0x6674c9c	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x6674ca0	fd030191	add	x29, sp, #0x40
0x6674ca4	09a601d0	adrp	x9, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x6674ca8	294d46f9	ldr	x9, [x9, #0xc98]
0x6674cac	290140f9	ldr	x9, [x9]
0x6674cb0	a9831ef8	stur	x9, [x29, #-0x18]
0x6674cb4	e9c901d0	adrp	x9, 0x9fb2000 <_wxam_enc_uninit_10+0x9fb2000>
0x6674cb8	29c11f91	add	x9, x9, #0x7f0
0x6674cbc	e90700f9	str	x9, [sp, #0x8]
0x6674cc0	e01300b9	str	w0, [sp, #0x10]
0x6674cc4	f3230091	add	x19, sp, #0x8
0x6674cc8	f31300f9	str	x19, [sp, #0x20]
0x6674ccc	e0230091	add	x0, sp, #0x8
0x6674cd0	a2d7ff97	bl	0x666ab58 <_SetWeixinCallbackFunc+0x188375c>
0x6674cd4	e01340f9	ldr	x0, [sp, #0x20]
0x6674cd8	1f0013eb	cmp	x0, x19
0x6674cdc	a0000054	b.eq	0x6674cf0 <_SetWeixinCallbackFunc+0x188d8f4>
0x6674ce0	e00000b4	cbz	x0, 0x6674cfc <_SetWeixinCallbackFunc+0x188d900>
0x6674ce4	080040f9	ldr	x8, [x0]
0x6674ce8	081540f9	ldr	x8, [x8, #0x28]
0x6674cec	03000014	b	0x6674cf8 <_SetWeixinCallbackFunc+0x188d8fc>
0x6674cf0	080040f9	ldr	x8, [x0]
0x6674cf4	081140f9	ldr	x8, [x8, #0x20]
0x6674cf8	00013fd6	blr	x8
0x6674cfc	a8835ef8	ldur	x8, [x29, #-0x18]
0x6674d00	09a601d0	adrp	x9, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x6674d04	294d46f9	ldr	x9, [x9, #0xc98]
0x6674d08	290140f9	ldr	x9, [x9]
0x6674d0c	3f0108eb	cmp	x9, x8
0x6674d10	a1000054	b.ne	0x6674d24 <_SetWeixinCallbackFunc+0x188d928>
0x6674d14	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x6674d18	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x6674d1c	ff430191	add	sp, sp, #0x50
0x6674d20	c0035fd6	ret
0x6674d24	202d2b94	bl	0x71401a4 <_wxam_enc_uninit_10+0x71401a4>
0x6674d28	e8230091	add	x8, sp, #0x8
0x6674d2c	f30300aa	mov	x19, x0
0x6674d30	e01340f9	ldr	x0, [sp, #0x20]
0x6674d34	1f0008eb	cmp	x0, x8
0x6674d38	80000054	b.eq	0x6674d48 <_SetWeixinCallbackFunc+0x188d94c>
0x6674d3c	c0792994	bl	0x70d343c <_SetWeixinCallbackFunc+0x22ec040>
0x6674d40	e00313aa	mov	x0, x19
0x6674d44	25292b94	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
0x6674d48	080040f9	ldr	x8, [x0]
0x6674d4c	081140f9	ldr	x8, [x8, #0x20]
0x6674d50	00013fd6	blr	x8
0x6674d54	e00313aa	mov	x0, x19
0x6674d58	20292b94	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
