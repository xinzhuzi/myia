0x6676714	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x6676718	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x667671c	fd430091	add	x29, sp, #0x10
0x6676720	ea0300aa	mov	x10, x0
0x6676724	480d41f8	ldr	x8, [x10, #0x10]!
0x6676728	e80100b4	cbz	x8, 0x6676764 <_SetWeixinCallbackFunc+0x188f368>
0x667672c	e9030aaa	mov	x9, x10
0x6676730	eb0308aa	mov	x11, x8
0x6676734	6c1140f9	ldr	x12, [x11, #0x20]
0x6676738	9f0101eb	cmp	x12, x1
0x667673c	29318b9a	csel	x9, x9, x11, lo
0x6676740	ec279f1a	cset	w12, lo
0x6676744	6b596cf8	ldr	x11, [x11, w12, uxtw #3]
0x6676748	6bffffb5	cbnz	x11, 0x6676734 <_SetWeixinCallbackFunc+0x188f338>
0x667674c	3f010aeb	cmp	x9, x10
0x6676750	a0000054	b.eq	0x6676764 <_SetWeixinCallbackFunc+0x188f368>
0x6676754	2b1140f9	ldr	x11, [x9, #0x20]
0x6676758	7f0101eb	cmp	x11, x1
0x667675c	5381899a	csel	x19, x10, x9, hi
0x6676760	89000054	b.ls	0x6676770 <_SetWeixinCallbackFunc+0x188f374>
0x6676764	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x6676768	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x667676c	c0035fd6	ret
0x6676770	2b0540f9	ldr	x11, [x9, #0x8]
0x6676774	ab0000b4	cbz	x11, 0x6676788 <_SetWeixinCallbackFunc+0x188f38c>
0x6676778	ea030baa	mov	x10, x11
0x667677c	6b0140f9	ldr	x11, [x11]
0x6676780	cbffffb5	cbnz	x11, 0x6676778 <_SetWeixinCallbackFunc+0x188f37c>
0x6676784	06000014	b	0x667679c <_SetWeixinCallbackFunc+0x188f3a0>
0x6676788	2a0940f9	ldr	x10, [x9, #0x10]
0x667678c	4b0140f9	ldr	x11, [x10]
0x6676790	7f0109eb	cmp	x11, x9
0x6676794	e9030aaa	mov	x9, x10
0x6676798	81ffff54	b.ne	0x6676788 <_SetWeixinCallbackFunc+0x188f38c>
0x667679c	090440f9	ldr	x9, [x0, #0x8]
0x66767a0	3f0113eb	cmp	x9, x19
0x66767a4	41000054	b.ne	0x66767ac <_SetWeixinCallbackFunc+0x188f3b0>
0x66767a8	0a0400f9	str	x10, [x0, #0x8]
0x66767ac	090c40f9	ldr	x9, [x0, #0x18]
0x66767b0	290500d1	sub	x9, x9, #0x1
0x66767b4	090c00f9	str	x9, [x0, #0x18]
0x66767b8	f40300aa	mov	x20, x0
0x66767bc	e00308aa	mov	x0, x8
0x66767c0	e10313aa	mov	x1, x19
0x66767c4	95b76696	bl	0x24618 <_WeChatMain+0xadac>
0x66767c8	e00313aa	mov	x0, x19
0x66767cc	01058052	mov	w1, #0x28               ; =40
0x66767d0	0f262b94	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x66767d4	e00314aa	mov	x0, x20
0x66767d8	21008052	mov	w1, #0x1                ; =1
0x66767dc	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x66767e0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x66767e4	e6feff17	b	0x667637c <_SetWeixinCallbackFunc+0x188ef80>
