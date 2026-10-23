0x667dcac	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x667dcb0	f65701a9	stp	x22, x21, [sp, #0x10]
0x667dcb4	f44f02a9	stp	x20, x19, [sp, #0x20]
0x667dcb8	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x667dcbc	fdc30091	add	x29, sp, #0x30
0x667dcc0	f30300aa	mov	x19, x0
0x667dcc4	151c40f9	ldr	x21, [x0, #0x38]
0x667dcc8	750300b4	cbz	x21, 0x667dd34 <_SetWeixinCallbackFunc+0x1896938>
0x667dccc	762240f9	ldr	x22, [x19, #0x40]
0x667dcd0	e00315aa	mov	x0, x21
0x667dcd4	df0215eb	cmp	x22, x21
0x667dcd8	60020054	b.eq	0x667dd24 <_SetWeixinCallbackFunc+0x1896928>
0x667dcdc	17008092	mov	x23, #-0x1              ; =-1
0x667dce0	04000014	b	0x667dcf0 <_SetWeixinCallbackFunc+0x18968f4>
0x667dce4	d68200d1	sub	x22, x22, #0x20
0x667dce8	df0215eb	cmp	x22, x21
0x667dcec	a0010054	b.eq	0x667dd20 <_SetWeixinCallbackFunc+0x1896924>
0x667dcf0	d4825ef8	ldur	x20, [x22, #-0x18]
0x667dcf4	94ffffb4	cbz	x20, 0x667dce4 <_SetWeixinCallbackFunc+0x18968e8>
0x667dcf8	88220091	add	x8, x20, #0x8
0x667dcfc	0801f7f8	ldaddal	x23, x8, [x8]
0x667dd00	28ffffb5	cbnz	x8, 0x667dce4 <_SetWeixinCallbackFunc+0x18968e8>
0x667dd04	880240f9	ldr	x8, [x20]
0x667dd08	080940f9	ldr	x8, [x8, #0x10]
0x667dd0c	e00314aa	mov	x0, x20
0x667dd10	00013fd6	blr	x8
0x667dd14	e00314aa	mov	x0, x20
0x667dd18	c1072b94	bl	0x713fc1c <_wxam_enc_uninit_10+0x713fc1c>
0x667dd1c	f2ffff17	b	0x667dce4 <_SetWeixinCallbackFunc+0x18968e8>
0x667dd20	601e40f9	ldr	x0, [x19, #0x38]
0x667dd24	752200f9	str	x21, [x19, #0x40]
0x667dd28	682640f9	ldr	x8, [x19, #0x48]
0x667dd2c	010100cb	sub	x1, x8, x0
0x667dd30	b7082b94	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x667dd34	611640f9	ldr	x1, [x19, #0x28]
0x667dd38	60820091	add	x0, x19, #0x20
0x667dd3c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x667dd40	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x667dd44	f65741a9	ldp	x22, x21, [sp, #0x10]
0x667dd48	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x667dd4c	8c496716	b	0x5037c <_WeChatMain+0x36b10>
