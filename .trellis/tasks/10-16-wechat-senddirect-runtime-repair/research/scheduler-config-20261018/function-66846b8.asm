0x66846b8	ff8307d1	sub	sp, sp, #0x1e0
0x66846bc	f85f1aa9	stp	x24, x23, [sp, #0x1a0]
0x66846c0	f6571ba9	stp	x22, x21, [sp, #0x1b0]
0x66846c4	f44f1ca9	stp	x20, x19, [sp, #0x1c0]
0x66846c8	fd7b1da9	stp	x29, x30, [sp, #0x1d0]
0x66846cc	fd430791	add	x29, sp, #0x1d0
0x66846d0	f50303aa	mov	x21, x3
0x66846d4	f60302aa	mov	x22, x2
0x66846d8	f70301aa	mov	x23, x1
0x66846dc	f40300aa	mov	x20, x0
0x66846e0	f30308aa	mov	x19, x8
0x66846e4	88a501d0	adrp	x8, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x66846e8	084d46f9	ldr	x8, [x8, #0xc98]
0x66846ec	080140f9	ldr	x8, [x8]
0x66846f0	a8831cf8	stur	x8, [x29, #-0x38]
0x66846f4	00e4006f	movi.2d	v0, #0000000000000000
0x66846f8	e00307ad	stp	q0, q0, [sp, #0xe0]
0x66846fc	e037803d	str	q0, [sp, #0xd0]
0x6684700	e0e5002f	movi	d0, #0x000000ffffffff
0x6684704	0040611e	fneg	d0, d0
0x6684708	e08300fd	str	d0, [sp, #0x100]
0x668470c	e0430391	add	x0, sp, #0xd0
0x6684710	74ec2a94	bl	0x713f8e0 <_wxam_enc_uninit_10+0x713f8e0>
0x6684714	e80e40f9	ldr	x8, [x23, #0x18]
0x6684718	480000b5	cbnz	x8, 0x6684720 <_SetWeixinCallbackFunc+0x189d324>
0x668471c	889240f9	ldr	x8, [x20, #0x120]
0x6684720	e87700f9	str	x8, [sp, #0xe8]
0x6684724	e81240f9	ldr	x8, [x23, #0x20]
0x6684728	480000b5	cbnz	x8, 0x6684730 <_SetWeixinCallbackFunc+0x189d334>
0x668472c	889640f9	ldr	x8, [x20, #0x128]
0x6684730	e87b00f9	str	x8, [sp, #0xf0]
0x6684734	e81640f9	ldr	x8, [x23, #0x28]
0x6684738	480000b5	cbnz	x8, 0x6684740 <_SetWeixinCallbackFunc+0x189d344>
0x668473c	889a40f9	ldr	x8, [x20, #0x130]
0x6684740	e87f00f9	str	x8, [sp, #0xf8]
0x6684744	e83240b9	ldr	w8, [x23, #0x30]
0x6684748	1f050031	cmn	w8, #0x1
0x668474c	41000054	b.ne	0x6684754 <_SetWeixinCallbackFunc+0x189d358>
0x6684750	883a41b9	ldr	w8, [x20, #0x138]
0x6684754	e80301b9	str	w8, [sp, #0x100]
0x6684758	e83640b9	ldr	w8, [x23, #0x34]
0x668475c	0900b052	mov	w9, #-0x80000000        ; =-2147483648
0x6684760	1f01096b	cmp	w8, w9
0x6684764	41000054	b.ne	0x668476c <_SetWeixinCallbackFunc+0x189d370>
0x6684768	883e41b9	ldr	w8, [x20, #0x13c]
0x668476c	e80701b9	str	w8, [sp, #0x104]
0x6684770	e80316aa	mov	x8, x22
0x6684774	008d41f8	ldr	x0, [x8, #0x18]!
0x6684778	e9f301b2	mov	x9, #-0x5555555555555556 ; =-6148914691236517206
0x668477c	692600a9	stp	x9, x9, [x19]
0x6684780	a00000b4	cbz	x0, 0x6684794 <_SetWeixinCallbackFunc+0x189d398>
0x6684784	1f0016eb	cmp	x0, x22
0x6684788	e0000054	b.eq	0x66847a4 <_SetWeixinCallbackFunc+0x189d3a8>
0x668478c	a08317f8	stur	x0, [x29, #-0x88]
0x6684790	03000014	b	0x668479c <_SetWeixinCallbackFunc+0x189d3a0>
0x6684794	a88302d1	sub	x8, x29, #0xa0
0x6684798	08610091	add	x8, x8, #0x18
0x668479c	1f0100f9	str	xzr, [x8]
0x66847a0	07000014	b	0x66847bc <_SetWeixinCallbackFunc+0x189d3c0>
0x66847a4	a88302d1	sub	x8, x29, #0xa0
0x66847a8	a88317f8	stur	x8, [x29, #-0x88]
0x66847ac	080040f9	ldr	x8, [x0]
0x66847b0	080d40f9	ldr	x8, [x8, #0x18]
0x66847b4	a18302d1	sub	x1, x29, #0xa0
0x66847b8	00013fd6	blr	x8
0x66847bc	a00e40f9	ldr	x0, [x21, #0x18]
0x66847c0	c00000b4	cbz	x0, 0x66847d8 <_SetWeixinCallbackFunc+0x189d3dc>
0x66847c4	1f0015eb	cmp	x0, x21
0x66847c8	c0000054	b.eq	0x66847e0 <_SetWeixinCallbackFunc+0x189d3e4>
0x66847cc	080040f9	ldr	x8, [x0]
0x66847d0	080940f9	ldr	x8, [x8, #0x10]
0x66847d4	00013fd6	blr	x8
0x66847d8	a08315f8	stur	x0, [x29, #-0xa8]
0x66847dc	07000014	b	0x66847f8 <_SetWeixinCallbackFunc+0x189d3fc>
0x66847e0	a80303d1	sub	x8, x29, #0xc0
0x66847e4	a88315f8	stur	x8, [x29, #-0xa8]
0x66847e8	080040f9	ldr	x8, [x0]
0x66847ec	080d40f9	ldr	x8, [x8, #0x18]
0x66847f0	a10303d1	sub	x1, x29, #0xc0
0x66847f4	00013fd6	blr	x8
0x66847f8	b50303d1	sub	x21, x29, #0xc0
0x66847fc	e0430391	add	x0, sp, #0xd0
0x6684800	a18302d1	sub	x1, x29, #0xa0
0x6684804	a20303d1	sub	x2, x29, #0xc0
0x6684808	e80313aa	mov	x8, x19
0x668480c	7be5ff97	bl	0x667ddf8 <_SetWeixinCallbackFunc+0x18969fc>
0x6684810	a08355f8	ldur	x0, [x29, #-0xa8]
0x6684814	1f0015eb	cmp	x0, x21
0x6684818	a0000054	b.eq	0x668482c <_SetWeixinCallbackFunc+0x189d430>
0x668481c	e00000b4	cbz	x0, 0x6684838 <_SetWeixinCallbackFunc+0x189d43c>
0x6684820	080040f9	ldr	x8, [x0]
0x6684824	081540f9	ldr	x8, [x8, #0x28]
0x6684828	03000014	b	0x6684834 <_SetWeixinCallbackFunc+0x189d438>
0x668482c	080040f9	ldr	x8, [x0]
0x6684830	081140f9	ldr	x8, [x8, #0x20]
0x6684834	00013fd6	blr	x8
0x6684838	a08357f8	ldur	x0, [x29, #-0x88]
0x668483c	a88302d1	sub	x8, x29, #0xa0
0x6684840	1f0008eb	cmp	x0, x8
0x6684844	a0000054	b.eq	0x6684858 <_SetWeixinCallbackFunc+0x189d45c>
0x6684848	e00000b4	cbz	x0, 0x6684864 <_SetWeixinCallbackFunc+0x189d468>
0x668484c	080040f9	ldr	x8, [x0]
0x6684850	081540f9	ldr	x8, [x8, #0x28]
0x6684854	03000014	b	0x6684860 <_SetWeixinCallbackFunc+0x189d464>
0x6684858	080040f9	ldr	x8, [x0]
0x668485c	081140f9	ldr	x8, [x8, #0x20]
0x6684860	00013fd6	blr	x8
0x6684864	88024539	ldrb	w8, [x20, #0x140]
0x6684868	e8000837	tbnz	w8, #0x1, 0x6684884 <_SetWeixinCallbackFunc+0x189d488>
0x668486c	e8134439	ldrb	w8, [sp, #0x104]
0x6684870	a8000837	tbnz	w8, #0x1, 0x6684884 <_SetWeixinCallbackFunc+0x189d488>
0x6684874	80220091	add	x0, x20, #0x8
0x6684878	e10313aa	mov	x1, x19
0x668487c	27f9ff97	bl	0x6682d18 <_SetWeixinCallbackFunc+0x189b91c>
0x6684880	71000014	b	0x6684a44 <_SetWeixinCallbackFunc+0x189d648>
0x6684884	20008052	mov	w0, #0x1                ; =1
0x6684888	92240094	bl	0x668dad0 <_SetWeixinCallbackFunc+0x18a66d4>
0x668488c	c00d0036	tbz	w0, #0x0, 0x6684a44 <_SetWeixinCallbackFunc+0x189d648>
0x6684890	a8f40190	adrp	x8, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684894	09b56139	ldrb	w9, [x8, #0x86d]
0x6684898	29010037	tbnz	w9, #0x0, 0x66848bc <_SetWeixinCallbackFunc+0x189d4c0>
0x668489c	e90701d0	adrp	x9, 0x8782000 <_wxam_enc_uninit_10+0x8782000>
0x66848a0	208d44fd	ldr	d0, [x9, #0x918]
0x66848a4	a9f40190	adrp	x9, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x66848a8	29a12191	add	x9, x9, #0x868
0x66848ac	200100bd	str	s0, [x9]
0x66848b0	3f110039	strb	wzr, [x9, #0x4]
0x66848b4	29008052	mov	w9, #0x1                ; =1
0x66848b8	09b52139	strb	w9, [x8, #0x86d]
0x66848bc	a8f40190	adrp	x8, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x66848c0	09e96139	ldrb	w9, [x8, #0x87a]
0x66848c4	49010037	tbnz	w9, #0x0, 0x66848ec <_SetWeixinCallbackFunc+0x189d4f0>
0x66848c8	a9f40190	adrp	x9, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x66848cc	29c12191	add	x9, x9, #0x870
0x66848d0	0a8001d0	adrp	x10, 0x9686000 <_wxam_enc_uninit_10+0x9686000>
0x66848d4	402142fd	ldr	d0, [x10, #0x440]
0x66848d8	200100fd	str	d0, [x9]
0x66848dc	0a0d8052	mov	w10, #0x68              ; =104
0x66848e0	2a110079	strh	w10, [x9, #0x8]
0x66848e4	29008052	mov	w9, #0x1                ; =1
0x66848e8	09e92139	strb	w9, [x8, #0x87a]
0x66848ec	a8f40190	adrp	x8, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x66848f0	09356239	ldrb	w9, [x8, #0x88d]
0x66848f4	89010037	tbnz	w9, #0x0, 0x6684924 <_SetWeixinCallbackFunc+0x189d528>
0x66848f8	098001d0	adrp	x9, 0x9686000 <_wxam_enc_uninit_10+0x9686000>
0x66848fc	202542fd	ldr	d0, [x9, #0x448]
0x6684900	a9f40190	adrp	x9, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684904	29012291	add	x9, x9, #0x880
0x6684908	200100fd	str	d0, [x9]
0x668490c	6a2501d0	adrp	x10, 0x8b32000 <_wxam_enc_uninit_10+0x8b32000>
0x6684910	402146fd	ldr	d0, [x10, #0xc40]
0x6684914	200900bd	str	s0, [x9, #0x8]
0x6684918	3f310039	strb	wzr, [x9, #0xc]
0x668491c	29008052	mov	w9, #0x1                ; =1
0x6684920	09352239	strb	w9, [x8, #0x88d]
0x6684924	a1f40190	adrp	x1, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684928	21a02191	add	x1, x1, #0x868
0x668492c	a2f40190	adrp	x2, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684930	42c02191	add	x2, x2, #0x870
0x6684934	a3f40190	adrp	x3, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684938	63002291	add	x3, x3, #0x880
0x668493c	e0030091	mov	x0, sp
0x6684940	040085d2	mov	x4, #0x2800             ; =10240
0x6684944	a40ac0f2	movk	x4, #0x55, lsl #32
0x6684948	85240094	bl	0x668db5c <_SetWeixinCallbackFunc+0x18a6760>
0x668494c	e80340f9	ldr	x8, [sp]
0x6684950	a9f40190	adrp	x9, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684954	2a456439	ldrb	w10, [x9, #0x911]
0x6684958	ca030037	tbnz	w10, #0x0, 0x66849d0 <_SetWeixinCallbackFunc+0x189d5d4>
0x668495c	0a0080d2	mov	x10, #0x0               ; =0
0x6684960	ebe702b2	mov	x11, #-0x3333333333333334 ; =-3689348814741910324
0x6684964	ab9999f2	movk	x11, #0xcccd
0x6684968	6c028092	mov	x12, #-0x14             ; =-20
0x668496c	0d8001d0	adrp	x13, 0x9686000 <_wxam_enc_uninit_10+0x9686000>
0x6684970	ad411291	add	x13, x13, #0x490
0x6684974	aef40190	adrp	x14, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684978	ce392291	add	x14, x14, #0x88e
0x668497c	4f7dcb9b	umulh	x15, x10, x11
0x6684980	effd44d3	lsr	x15, x15, #4
0x6684984	b0010a8b	add	x16, x13, x10
0x6684988	ef410c9b	madd	x15, x15, x12, x16
0x668498c	007248bc	ldur	s0, [x16, #0x87]
0x6684990	00a4082f	ushll.8h	v0, v0, #0x0
0x6684994	e13147bc	ldur	s1, [x15, #0x73]
0x6684998	21a4082f	ushll.8h	v1, v1, #0x0
0x668499c	201c202e	eor.8b	v0, v1, v0
0x66849a0	0018000e	uzp1.8b	v0, v0, v0
0x66849a4	c0692abc	str	s0, [x14, x10]
0x66849a8	4a110091	add	x10, x10, #0x4
0x66849ac	5f0102f1	cmp	x10, #0x80
0x66849b0	61feff54	b.ne	0x668497c <_SetWeixinCallbackFunc+0x189d580>
0x66849b4	aaf40190	adrp	x10, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x66849b8	4a392491	add	x10, x10, #0x90e
0x66849bc	ab048f52	mov	w11, #0x7825            ; =30757
0x66849c0	4b010079	strh	w11, [x10]
0x66849c4	5f090039	strb	wzr, [x10, #0x2]
0x66849c8	2a008052	mov	w10, #0x1               ; =1
0x66849cc	2a452439	strb	w10, [x9, #0x911]
0x66849d0	02a10191	add	x2, x8, #0x68
0x66849d4	09fdc139	ldrsb	w9, [x8, #0x7f]
0x66849d8	4900f836	tbz	w9, #0x1f, 0x66849e0 <_SetWeixinCallbackFunc+0x189d5e4>
0x66849dc	420040f9	ldr	x2, [x2]
0x66849e0	40e5054f	movi.16b	v0, #0xaa
0x66849e4	a0033cad	stp	q0, q0, [x29, #-0x80]
0x66849e8	a0033dad	stp	q0, q0, [x29, #-0x60]
0x66849ec	e9008052	mov	w9, #0x7                ; =7
0x66849f0	4a008052	mov	w10, #0x2               ; =2
0x66849f4	a98318b8	stur	w9, [x29, #-0x78]
0x66849f8	aa0318b8	stur	w10, [x29, #-0x80]
0x66849fc	8a4241b9	ldr	w10, [x20, #0x140]
0x6684a00	a98319b8	stur	w9, [x29, #-0x68]
0x6684a04	aa0319b8	stur	w10, [x29, #-0x70]
0x6684a08	ea0741b9	ldr	w10, [sp, #0x104]
0x6684a0c	a9831ab8	stur	w9, [x29, #-0x58]
0x6684a10	aa031ab8	stur	w10, [x29, #-0x60]
0x6684a14	c9008052	mov	w9, #0x6                ; =6
0x6684a18	a9831bb8	stur	w9, [x29, #-0x48]
0x6684a1c	bf031bb8	stur	wzr, [x29, #-0x50]
0x6684a20	a1f40190	adrp	x1, 0xa518000 <_wxam_enc_uninit_10+0xa518000>
0x6684a24	21382291	add	x1, x1, #0x88e
0x6684a28	00e10091	add	x0, x8, #0x38
0x6684a2c	a30302d1	sub	x3, x29, #0x80
0x6684a30	64008052	mov	w4, #0x3                ; =3
0x6684a34	ec250094	bl	0x668e1e4 <_SetWeixinCallbackFunc+0x18a6de8>
0x6684a38	5d240094	bl	0x668dbac <_SetWeixinCallbackFunc+0x18a67b0>
0x6684a3c	e0030091	mov	x0, sp
0x6684a40	5e240094	bl	0x668dbb8 <_SetWeixinCallbackFunc+0x18a67bc>
0x6684a44	80220091	add	x0, x20, #0x8
0x6684a48	b0f8ff97	bl	0x6682d08 <_SetWeixinCallbackFunc+0x189b90c>
0x6684a4c	60000036	tbz	w0, #0x0, 0x6684a58 <_SetWeixinCallbackFunc+0x189d65c>
0x6684a50	08038052	mov	w8, #0x18               ; =24
0x6684a54	04000014	b	0x6684a64 <_SetWeixinCallbackFunc+0x189d668>
0x6684a58	e8134439	ldrb	w8, [sp, #0x104]
0x6684a5c	c8000037	tbnz	w8, #0x0, 0x6684a74 <_SetWeixinCallbackFunc+0x189d678>
0x6684a60	08028052	mov	w8, #0x10               ; =16
0x6684a64	600240f9	ldr	x0, [x19]
0x6684a68	090040f9	ldr	x9, [x0]
0x6684a6c	286968f8	ldr	x8, [x9, x8]
0x6684a70	00013fd6	blr	x8
0x6684a74	e89fc339	ldrsb	w8, [sp, #0xe7]
0x6684a78	a800f836	tbz	w8, #0x1f, 0x6684a8c <_SetWeixinCallbackFunc+0x189d690>
0x6684a7c	e06b40f9	ldr	x0, [sp, #0xd0]
0x6684a80	e87340f9	ldr	x8, [sp, #0xe0]
0x6684a84	01f94092	and	x1, x8, #0x7fffffffffffffff
0x6684a88	61ed2a94	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x6684a8c	a8835cf8	ldur	x8, [x29, #-0x38]
0x6684a90	89a501d0	adrp	x9, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x6684a94	294d46f9	ldr	x9, [x9, #0xc98]
0x6684a98	290140f9	ldr	x9, [x9]
0x6684a9c	3f0108eb	cmp	x9, x8
0x6684aa0	e1000054	b.ne	0x6684abc <_SetWeixinCallbackFunc+0x189d6c0>
0x6684aa4	fd7b5da9	ldp	x29, x30, [sp, #0x1d0]
0x6684aa8	f44f5ca9	ldp	x20, x19, [sp, #0x1c0]
0x6684aac	f6575ba9	ldp	x22, x21, [sp, #0x1b0]
0x6684ab0	f85f5aa9	ldp	x24, x23, [sp, #0x1a0]
0x6684ab4	ff830791	add	sp, sp, #0x1e0
0x6684ab8	c0035fd6	ret
0x6684abc	baed2a94	bl	0x71401a4 <_wxam_enc_uninit_10+0x71401a4>
0x6684ac0	64496696	bl	0x17050 <__text+0x50>
0x6684ac4	f40300aa	mov	x20, x0
0x6684ac8	e0030091	mov	x0, sp
0x6684acc	3b240094	bl	0x668dbb8 <_SetWeixinCallbackFunc+0x18a67bc>
0x6684ad0	29000014	b	0x6684b74 <_SetWeixinCallbackFunc+0x189d778>
0x6684ad4	f40300aa	mov	x20, x0
0x6684ad8	0c000014	b	0x6684b08 <_SetWeixinCallbackFunc+0x189d70c>
0x6684adc	f40300aa	mov	x20, x0
0x6684ae0	a08355f8	ldur	x0, [x29, #-0xa8]
0x6684ae4	1f0015eb	cmp	x0, x21
0x6684ae8	81000054	b.ne	0x6684af8 <_SetWeixinCallbackFunc+0x189d6fc>
0x6684aec	080040f9	ldr	x8, [x0]
0x6684af0	081140f9	ldr	x8, [x8, #0x20]
0x6684af4	04000014	b	0x6684b04 <_SetWeixinCallbackFunc+0x189d708>
0x6684af8	800000b4	cbz	x0, 0x6684b08 <_SetWeixinCallbackFunc+0x189d70c>
0x6684afc	080040f9	ldr	x8, [x0]
0x6684b00	081540f9	ldr	x8, [x8, #0x28]
0x6684b04	00013fd6	blr	x8
0x6684b08	a08357f8	ldur	x0, [x29, #-0x88]
0x6684b0c	a88302d1	sub	x8, x29, #0xa0
0x6684b10	1f0008eb	cmp	x0, x8
0x6684b14	81000054	b.ne	0x6684b24 <_SetWeixinCallbackFunc+0x189d728>
0x6684b18	080040f9	ldr	x8, [x0]
0x6684b1c	081140f9	ldr	x8, [x8, #0x20]
0x6684b20	0c000014	b	0x6684b50 <_SetWeixinCallbackFunc+0x189d754>
0x6684b24	200100b5	cbnz	x0, 0x6684b48 <_SetWeixinCallbackFunc+0x189d74c>
0x6684b28	e89fc339	ldrsb	w8, [sp, #0xe7]
0x6684b2c	c802f836	tbz	w8, #0x1f, 0x6684b84 <_SetWeixinCallbackFunc+0x189d788>
0x6684b30	e06b40f9	ldr	x0, [sp, #0xd0]
0x6684b34	e87340f9	ldr	x8, [sp, #0xe0]
0x6684b38	01f94092	and	x1, x8, #0x7fffffffffffffff
0x6684b3c	34ed2a94	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x6684b40	e00314aa	mov	x0, x20
0x6684b44	a5e92a94	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
0x6684b48	080040f9	ldr	x8, [x0]
0x6684b4c	081540f9	ldr	x8, [x8, #0x28]
0x6684b50	00013fd6	blr	x8
0x6684b54	e89fc339	ldrsb	w8, [sp, #0xe7]
0x6684b58	6801f836	tbz	w8, #0x1f, 0x6684b84 <_SetWeixinCallbackFunc+0x189d788>
0x6684b5c	f5ffff17	b	0x6684b30 <_SetWeixinCallbackFunc+0x189d734>
0x6684b60	f40300aa	mov	x20, x0
0x6684b64	e89fc339	ldrsb	w8, [sp, #0xe7]
0x6684b68	e800f836	tbz	w8, #0x1f, 0x6684b84 <_SetWeixinCallbackFunc+0x189d788>
0x6684b6c	f1ffff17	b	0x6684b30 <_SetWeixinCallbackFunc+0x189d734>
0x6684b70	f40300aa	mov	x20, x0
0x6684b74	e00313aa	mov	x0, x19
0x6684b78	4a1dec96	bl	0x218c0a0 <_WeChatMain+0x2172834>
0x6684b7c	e89fc339	ldrsb	w8, [sp, #0xe7]
0x6684b80	88fdff37	tbnz	w8, #0x1f, 0x6684b30 <_SetWeixinCallbackFunc+0x189d734>
0x6684b84	e00314aa	mov	x0, x20
0x6684b88	94e92a94	bl	0x713f1d8 <_wxam_enc_uninit_10+0x713f1d8>
