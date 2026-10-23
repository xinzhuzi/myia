0x667a110	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x667a114	f85f01a9	stp	x24, x23, [sp, #0x10]
0x667a118	f65702a9	stp	x22, x21, [sp, #0x20]
0x667a11c	f44f03a9	stp	x20, x19, [sp, #0x30]
0x667a120	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x667a124	fd030191	add	x29, sp, #0x40
0x667a128	f50304aa	mov	x21, x4
0x667a12c	f60303aa	mov	x22, x3
0x667a130	f70302aa	mov	x23, x2
0x667a134	f80301aa	mov	x24, x1
0x667a138	f40308aa	mov	x20, x8
0x667a13c	00828052	mov	w0, #0x410              ; =1040
0x667a140	bc172b94	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x667a144	f30300aa	mov	x19, x0
0x667a148	f90300aa	mov	x25, x0
0x667a14c	3f8f00f8	str	xzr, [x25, #0x8]!
0x667a150	c8c90190	adrp	x8, 0x9fb2000 <_wxam_enc_uninit_10+0x9fb2000>
0x667a154	08811c91	add	x8, x8, #0x720
0x667a158	1f0800f9	str	xzr, [x0, #0x10]
0x667a15c	088401f8	str	x8, [x0], #0x18
0x667a160	010340f9	ldr	x1, [x24]
0x667a164	e20240f9	ldr	x2, [x23]
0x667a168	c30240f9	ldr	x3, [x22]
0x667a16c	e40315aa	mov	x4, x21
0x667a170	41000094	bl	0x667a274 <_SetWeixinCallbackFunc+0x1892e78>
0x667a174	804e00a9	stp	x0, x19, [x20]
0x667a178	800200b4	cbz	x0, 0x667a1c8 <_SetWeixinCallbackFunc+0x1892dcc>
0x667a17c	601240f9	ldr	x0, [x19, #0x20]
0x667a180	800000b4	cbz	x0, 0x667a190 <_SetWeixinCallbackFunc+0x1892d94>
0x667a184	080440f9	ldr	x8, [x0, #0x8]
0x667a188	1f0500b1	cmn	x8, #0x1
0x667a18c	e1010054	b.ne	0x667a1c8 <_SetWeixinCallbackFunc+0x1892dcc>
0x667a190	d30000b4	cbz	x19, 0x667a1a8 <_SetWeixinCallbackFunc+0x1892dac>
0x667a194	68220091	add	x8, x19, #0x8
0x667a198	29008052	mov	w9, #0x1                ; =1
0x667a19c	080129f8	ldadd	x9, x8, [x8]
0x667a1a0	68420091	add	x8, x19, #0x10
0x667a1a4	080129f8	ldadd	x9, x8, [x8]
0x667a1a8	68620091	add	x8, x19, #0x18
0x667a1ac	68ce01a9	stp	x8, x19, [x19, #0x18]
0x667a1b0	400000b4	cbz	x0, 0x667a1b8 <_SetWeixinCallbackFunc+0x1892dbc>
0x667a1b4	9a162b94	bl	0x713fc1c <_wxam_enc_uninit_10+0x713fc1c>
0x667a1b8	930000b4	cbz	x19, 0x667a1c8 <_SetWeixinCallbackFunc+0x1892dcc>
0x667a1bc	08008092	mov	x8, #-0x1               ; =-1
0x667a1c0	2803e8f8	ldaddal	x8, x8, [x25]
0x667a1c4	e80000b4	cbz	x8, 0x667a1e0 <_SetWeixinCallbackFunc+0x1892de4>
0x667a1c8	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x667a1cc	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x667a1d0	f65742a9	ldp	x22, x21, [sp, #0x20]
0x667a1d4	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x667a1d8	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x667a1dc	c0035fd6	ret
0x667a1e0	680240f9	ldr	x8, [x19]
0x667a1e4	080940f9	ldr	x8, [x8, #0x10]
0x667a1e8	e00313aa	mov	x0, x19
0x667a1ec	00013fd6	blr	x8
0x667a1f0	e00313aa	mov	x0, x19
0x667a1f4	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x667a1f8	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x667a1fc	f65742a9	ldp	x22, x21, [sp, #0x20]
0x667a200	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x667a204	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x667a208	85162b14	b	0x713fc1c <_wxam_enc_uninit_10+0x713fc1c>
0x667a20c	f40300aa	mov	x20, x0
0x667a210	e00313aa	mov	x0, x19
0x667a214	88162b94	bl	0x713fc34 <_wxam_enc_uninit_10+0x713fc34>
0x667a218	930000b4	cbz	x19, 0x667a228 <_SetWeixinCallbackFunc+0x1892e2c>
0x667a21c	e00313aa	mov	x0, x19
0x667a220	01828052	mov	w1, #0x410              ; =1040
0x667a224	7a172b94	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x667a228	e00314aa	mov	x0, x20
0x667a22c	eb132b94	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
