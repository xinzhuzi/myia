0x66767e8	ffc301d1	sub	sp, sp, #0x70
0x66767ec	fa6702a9	stp	x26, x25, [sp, #0x20]
0x66767f0	f85f03a9	stp	x24, x23, [sp, #0x30]
0x66767f4	f65704a9	stp	x22, x21, [sp, #0x40]
0x66767f8	f44f05a9	stp	x20, x19, [sp, #0x50]
0x66767fc	fd7b06a9	stp	x29, x30, [sp, #0x60]
0x6676800	fd830191	add	x29, sp, #0x60
0x6676804	f50301aa	mov	x21, x1
0x6676808	f30300aa	mov	x19, x0
0x667680c	f40308aa	mov	x20, x8
0x6676810	610000b5	cbnz	x1, 0x667681c <_SetWeixinCallbackFunc+0x188f420>
0x6676814	28f3ff97	bl	0x66734b4 <_SetWeixinCallbackFunc+0x188c0b8>
0x6676818	f50300aa	mov	x21, x0
0x667681c	f80313aa	mov	x24, x19
0x6676820	098f40f8	ldr	x9, [x24, #0x8]!
0x6676824	a90100b4	cbz	x9, 0x6676858 <_SetWeixinCallbackFunc+0x188f45c>
0x6676828	e80318aa	mov	x8, x24
0x667682c	2a1140f9	ldr	x10, [x9, #0x20]
0x6676830	5f0115eb	cmp	x10, x21
0x6676834	0831899a	csel	x8, x8, x9, lo
0x6676838	ea279f1a	cset	w10, lo
0x667683c	29596af8	ldr	x9, [x9, w10, uxtw #3]
0x6676840	69ffffb5	cbnz	x9, 0x667682c <_SetWeixinCallbackFunc+0x188f430>
0x6676844	1f0118eb	cmp	x8, x24
0x6676848	80000054	b.eq	0x6676858 <_SetWeixinCallbackFunc+0x188f45c>
0x667684c	091140f9	ldr	x9, [x8, #0x20]
0x6676850	bf0209eb	cmp	x21, x9
0x6676854	a2090054	b.hs	0x6676988 <_SetWeixinCallbackFunc+0x188f58c>
0x6676858	a80240f9	ldr	x8, [x21]
0x667685c	081d40f9	ldr	x8, [x8, #0x38]
0x6676860	e00315aa	mov	x0, x21
0x6676864	00013fd6	blr	x8
0x6676868	f70300aa	mov	x23, x0
0x667686c	000b8052	mov	w0, #0x58               ; =88
0x6676870	f0252b94	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x6676874	f60300aa	mov	x22, x0
0x6676878	e80300aa	mov	x8, x0
0x667687c	1f8d00f8	str	xzr, [x8, #0x8]!
0x6676880	e9c90190	adrp	x9, 0x9fb2000 <_wxam_enc_uninit_10+0x9fb2000>
0x6676884	29012e91	add	x9, x9, #0xb80
0x6676888	1f0800f9	str	xzr, [x0, #0x10]
0x667688c	090000f9	str	x9, [x0]
0x6676890	f90300aa	mov	x25, x0
0x6676894	378f01f8	str	x23, [x25, #0x18]!
0x6676898	1f7c03a9	stp	xzr, xzr, [x0, #0x30]
0x667689c	e90300aa	mov	x9, x0
0x66768a0	3f8d02f8	str	xzr, [x9, #0x28]!
0x66768a4	091000f9	str	x9, [x0, #0x20]
0x66768a8	1f7c04a9	stp	xzr, xzr, [x0, #0x40]
0x66768ac	990200a9	stp	x25, x0, [x20]
0x66768b0	f5e700a9	stp	x21, x25, [sp, #0x8]
0x66768b4	e00f00f9	str	x0, [sp, #0x18]
0x66768b8	600000b4	cbz	x0, 0x66768c4 <_SetWeixinCallbackFunc+0x188f4c8>
0x66768bc	29008052	mov	w9, #0x1                ; =1
0x66768c0	080129f8	ldadd	x9, x8, [x8]
0x66768c4	080340f9	ldr	x8, [x24]
0x66768c8	f70318aa	mov	x23, x24
0x66768cc	a80000b5	cbnz	x8, 0x66768e0 <_SetWeixinCallbackFunc+0x188f4e4>
0x66768d0	0d000014	b	0x6676904 <_SetWeixinCallbackFunc+0x188f508>
0x66768d4	e80240f9	ldr	x8, [x23]
0x66768d8	f80317aa	mov	x24, x23
0x66768dc	480100b4	cbz	x8, 0x6676904 <_SetWeixinCallbackFunc+0x188f508>
0x66768e0	f70308aa	mov	x23, x8
0x66768e4	081140f9	ldr	x8, [x8, #0x20]
0x66768e8	bf0208eb	cmp	x21, x8
0x66768ec	43ffff54	b.lo	0x66768d4 <_SetWeixinCallbackFunc+0x188f4d8>
0x66768f0	1f0115eb	cmp	x8, x21
0x66768f4	22030054	b.hs	0x6676958 <_SetWeixinCallbackFunc+0x188f55c>
0x66768f8	e80640f9	ldr	x8, [x23, #0x8]
0x66768fc	28ffffb5	cbnz	x8, 0x66768e0 <_SetWeixinCallbackFunc+0x188f4e4>
0x6676900	f8220091	add	x24, x23, #0x8
0x6676904	00078052	mov	w0, #0x38               ; =56
0x6676908	ca252b94	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x667690c	e10300aa	mov	x1, x0
0x6676910	e8230091	add	x8, sp, #0x8
0x6676914	356402a9	stp	x21, x25, [x1, #0x20]
0x6676918	361800f9	str	x22, [x1, #0x30]
0x667691c	1ffd00a9	stp	xzr, xzr, [x8, #0x8]
0x6676920	3f7c00a9	stp	xzr, xzr, [x1]
0x6676924	370800f9	str	x23, [x1, #0x10]
0x6676928	010300f9	str	x1, [x24]
0x667692c	680240f9	ldr	x8, [x19]
0x6676930	080140f9	ldr	x8, [x8]
0x6676934	680000b4	cbz	x8, 0x6676940 <_SetWeixinCallbackFunc+0x188f544>
0x6676938	680200f9	str	x8, [x19]
0x667693c	010340f9	ldr	x1, [x24]
0x6676940	600640f9	ldr	x0, [x19, #0x8]
0x6676944	feb56696	bl	0x2413c <_WeChatMain+0xa8d0>
0x6676948	680a40f9	ldr	x8, [x19, #0x10]
0x667694c	08050091	add	x8, x8, #0x1
0x6676950	680a00f9	str	x8, [x19, #0x10]
0x6676954	f60f40f9	ldr	x22, [sp, #0x18]
0x6676958	560200b4	cbz	x22, 0x66769a0 <_SetWeixinCallbackFunc+0x188f5a4>
0x667695c	c8220091	add	x8, x22, #0x8
0x6676960	09008092	mov	x9, #-0x1               ; =-1
0x6676964	0801e9f8	ldaddal	x9, x8, [x8]
0x6676968	c80100b5	cbnz	x8, 0x66769a0 <_SetWeixinCallbackFunc+0x188f5a4>
0x667696c	c80240f9	ldr	x8, [x22]
0x6676970	080940f9	ldr	x8, [x8, #0x10]
0x6676974	e00316aa	mov	x0, x22
0x6676978	00013fd6	blr	x8
0x667697c	e00316aa	mov	x0, x22
0x6676980	a7242b94	bl	0x713fc1c <_wxam_enc_uninit_10+0x713fc1c>
0x6676984	07000014	b	0x66769a0 <_SetWeixinCallbackFunc+0x188f5a4>
0x6676988	09a142a9	ldp	x9, x8, [x8, #0x28]
0x667698c	892200a9	stp	x9, x8, [x20]
0x6676990	880000b4	cbz	x8, 0x66769a0 <_SetWeixinCallbackFunc+0x188f5a4>
0x6676994	08210091	add	x8, x8, #0x8
0x6676998	29008052	mov	w9, #0x1                ; =1
0x667699c	080129f8	ldadd	x9, x8, [x8]
0x66769a0	fd7b46a9	ldp	x29, x30, [sp, #0x60]
0x66769a4	f44f45a9	ldp	x20, x19, [sp, #0x50]
0x66769a8	f65744a9	ldp	x22, x21, [sp, #0x40]
0x66769ac	f85f43a9	ldp	x24, x23, [sp, #0x30]
0x66769b0	fa6742a9	ldp	x26, x25, [sp, #0x20]
0x66769b4	ffc30191	add	sp, sp, #0x70
0x66769b8	c0035fd6	ret
0x66769bc	f30300aa	mov	x19, x0
0x66769c0	e0230091	add	x0, sp, #0x8
0x66769c4	d57e6f96	bl	0x256518 <_WeChatMain+0x23ccac>
0x66769c8	e00314aa	mov	x0, x20
0x66769cc	67cd6a96	bl	0x129f68 <_WeChatMain+0x1106fc>
0x66769d0	e00313aa	mov	x0, x19
0x66769d4	01222b94	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
