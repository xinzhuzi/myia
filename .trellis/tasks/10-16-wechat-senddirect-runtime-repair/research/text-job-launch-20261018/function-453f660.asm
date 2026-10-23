0x453f660	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x453f664	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x453f668	fd430091	add	x29, sp, #0x10
0x453f66c	f30300aa	mov	x19, x0
0x453f670	08200091	add	x8, x0, #0x8
0x453f674	001040f9	ldr	x0, [x0, #0x20]
0x453f678	1f0008eb	cmp	x0, x8
0x453f67c	a0000054	b.eq	0x453f690 <_WeChatMain+0x4525e24>
0x453f680	e00000b4	cbz	x0, 0x453f69c <_WeChatMain+0x4525e30>
0x453f684	080040f9	ldr	x8, [x0]
0x453f688	081540f9	ldr	x8, [x8, #0x28]
0x453f68c	03000014	b	0x453f698 <_WeChatMain+0x4525e2c>
0x453f690	080040f9	ldr	x8, [x0]
0x453f694	081140f9	ldr	x8, [x8, #0x20]
0x453f698	00013fd6	blr	x8
0x453f69c	e00313aa	mov	x0, x19
0x453f6a0	01058052	mov	w1, #0x28               ; =40
0x453f6a4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x453f6a8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x453f6ac	5802b014	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x453f6b0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x453f6b4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x453f6b8	fd430091	add	x29, sp, #0x10
0x453f6bc	f30300aa	mov	x19, x0
0x453f6c0	e8fe02f0	adrp	x8, 0xa51e000 <_wxam_enc_uninit_10+0xa51e000>
0x453f6c4	08812691	add	x8, x8, #0x9a0
0x453f6c8	00fddf88	ldar	w0, [x8]
0x453f6cc	c8188594	bl	0x66859ec <_SetWeixinCallbackFunc+0x189e5f0>
0x453f6d0	601240f9	ldr	x0, [x19, #0x20]
0x453f6d4	c00000b4	cbz	x0, 0x453f6ec <_WeChatMain+0x4525e80>
0x453f6d8	080040f9	ldr	x8, [x0]
0x453f6dc	011940f9	ldr	x1, [x8, #0x30]
0x453f6e0	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x453f6e4	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x453f6e8	20001fd6	br	x1
0x453f6ec	787df396	bl	0x21eccc <_WeChatMain+0x205460>
0x453f6f0	280440f9	ldr	x8, [x1, #0x8]
0x453f6f4	e92502f0	adrp	x9, 0x89fe000 <_wxam_enc_uninit_10+0x89fe000>
0x453f6f8	29a13191	add	x9, x9, #0xc68
0x453f6fc	0a00f0d2	mov	x10, #-0x8000000000000000 ; =-9223372036854775808
0x453f700	2a010a8b	add	x10, x9, x10
0x453f704	1f010aeb	cmp	x8, x10
0x453f708	61000054	b.ne	0x453f714 <_WeChatMain+0x4525ea8>
0x453f70c	00200091	add	x0, x0, #0x8
0x453f710	c0035fd6	ret
0x453f714	1f010aea	tst	x8, x10
0x453f718	6b000054	b.lt	0x453f724 <_WeChatMain+0x4525eb8>
0x453f71c	000080d2	mov	x0, #0x0                ; =0
0x453f720	c0035fd6	ret
0x453f724	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x453f728	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x453f72c	fd430091	add	x29, sp, #0x10
0x453f730	0a00f0d2	mov	x10, #-0x8000000000000000 ; =-9223372036854775808
0x453f734	29010a8b	add	x9, x9, x10
0x453f738	f30300aa	mov	x19, x0
0x453f73c	00f94092	and	x0, x8, #0x7fffffffffffffff
0x453f740	21f94092	and	x1, x9, #0x7fffffffffffffff
0x453f744	9508b094	bl	0x7141998 <_wxam_enc_uninit_10+0x7141998>
0x453f748	e80300aa	mov	x8, x0
0x453f74c	e00313aa	mov	x0, x19
0x453f750	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x453f754	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x453f758	a8fdff34	cbz	w8, 0x453f70c <_WeChatMain+0x4525ea0>
0x453f75c	000080d2	mov	x0, #0x0                ; =0
0x453f760	c0035fd6	ret
