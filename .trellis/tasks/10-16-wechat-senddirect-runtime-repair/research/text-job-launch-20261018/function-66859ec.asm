0x66859ec	ff0301d1	sub	sp, sp, #0x40
0x66859f0	f44f02a9	stp	x20, x19, [sp, #0x20]
0x66859f4	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x66859f8	fdc30091	add	x29, sp, #0x30
0x66859fc	e8230091	add	x8, sp, #0x8
0x6685a00	a5bcff97	bl	0x6674c94 <_SetWeixinCallbackFunc+0x188d898>
0x6685a04	e0230091	add	x0, sp, #0x8
0x6685a08	3dffff97	bl	0x66856fc <_SetWeixinCallbackFunc+0x189e300>
0x6685a0c	f30b40f9	ldr	x19, [sp, #0x10]
0x6685a10	730100b4	cbz	x19, 0x6685a3c <_SetWeixinCallbackFunc+0x189e640>
0x6685a14	68220091	add	x8, x19, #0x8
0x6685a18	09008092	mov	x9, #-0x1               ; =-1
0x6685a1c	0801e9f8	ldaddal	x9, x8, [x8]
0x6685a20	e80000b5	cbnz	x8, 0x6685a3c <_SetWeixinCallbackFunc+0x189e640>
0x6685a24	680240f9	ldr	x8, [x19]
0x6685a28	080940f9	ldr	x8, [x8, #0x10]
0x6685a2c	e00313aa	mov	x0, x19
0x6685a30	00013fd6	blr	x8
0x6685a34	e00313aa	mov	x0, x19
0x6685a38	79e82a94	bl	0x713fc1c <_wxam_enc_uninit_10+0x713fc1c>
0x6685a3c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x6685a40	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x6685a44	ff030191	add	sp, sp, #0x40
0x6685a48	c0035fd6	ret
0x6685a4c	f30300aa	mov	x19, x0
0x6685a50	e0230091	add	x0, sp, #0x8
0x6685a54	45916a96	bl	0x129f68 <_WeChatMain+0x1106fc>
0x6685a58	e00313aa	mov	x0, x19
0x6685a5c	dfe52a94	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
