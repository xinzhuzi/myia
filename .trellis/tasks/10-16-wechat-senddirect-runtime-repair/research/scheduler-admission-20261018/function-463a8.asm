0x463a8	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x463ac	f44f01a9	stp	x20, x19, [sp, #0x10]
0x463b0	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x463b4	fd830091	add	x29, sp, #0x20
0x463b8	68100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x463bc	08210591	add	x8, x8, #0x148
0x463c0	08c1bf38	ldaprb	w8, [x8]
0x463c4	68030036	tbz	w8, #0x0, 0x46430 <_WeChatMain+0x2cbc4>
0x463c8	60100590	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x463cc	00400591	add	x0, x0, #0x150
0x463d0	11780194	bl	0xa4414 <_WeChatMain+0x8aba8>
0x463d4	200200b5	cbnz	x0, 0x46418 <_WeChatMain+0x2cbac>
0x463d8	80008052	mov	w0, #0x4                ; =4
0x463dc	15e7c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x463e0	f30300aa	mov	x19, x0
0x463e4	1f0000b9	str	wzr, [x0]
0x463e8	74100590	adrp	x20, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x463ec	94420591	add	x20, x20, #0x150
0x463f0	e00314aa	mov	x0, x20
0x463f4	08780194	bl	0xa4414 <_WeChatMain+0x8aba8>
0x463f8	f50300aa	mov	x21, x0
0x463fc	e00314aa	mov	x0, x20
0x46400	e10313aa	mov	x1, x19
0x46404	45780194	bl	0xa4518 <_WeChatMain+0x8acac>
0x46408	950000b4	cbz	x21, 0x46418 <_WeChatMain+0x2cbac>
0x4640c	e00315aa	mov	x0, x21
0x46410	81008052	mov	w1, #0x4                ; =4
0x46414	fee6c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46418	60100590	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4641c	00400591	add	x0, x0, #0x150
0x46420	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x46424	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x46428	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4642c	fa770114	b	0xa4414 <_WeChatMain+0x8aba8>
0x46430	880bc295	bl	0x70c9250 <_SetWeixinCallbackFunc+0x22e1e54>
0x46434	e5ffff17	b	0x463c8 <_WeChatMain+0x2cb5c>
0x46438	080040b9	ldr	w8, [x0]
0x4643c	09050011	add	w9, w8, #0x1
0x46440	3f050071	cmp	w9, #0x1
0x46444	29008052	mov	w9, #0x1                ; =1
0x46448	2895881a	csinc	w8, w9, w8, ls
0x4644c	08fc9f88	stlr	w8, [x0]
0x46450	c0035fd6	ret
0x46454	600000b4	cbz	x0, 0x46460 <_WeChatMain+0x2cbf4>
0x46458	81008052	mov	w1, #0x4                ; =4
0x4645c	ece6c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46460	c0035fd6	ret
0x46464	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x46468	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4646c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x46470	fd830091	add	x29, sp, #0x20
0x46474	f30300aa	mov	x19, x0
0x46478	1f7c00a9	stp	xzr, xzr, [x0]
0x4647c	1f0800f9	str	xzr, [x0, #0x10]
0x46480	810100b4	cbz	x1, 0x464b0 <_WeChatMain+0x2cc44>
0x46484	28fc7ed3	lsr	x8, x1, #62
0x46488	080200b5	cbnz	x8, 0x464c8 <_WeChatMain+0x2cc5c>
0x4648c	34f47ed3	lsl	x20, x1, #2
0x46490	e00314aa	mov	x0, x20
0x46494	e7e6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x46498	600200f9	str	x0, [x19]
0x4649c	1500148b	add	x21, x0, x20
0x464a0	750a00f9	str	x21, [x19, #0x10]
0x464a4	e10314aa	mov	x1, x20
0x464a8	bae7c395	bl	0x7140390 <_wxam_enc_uninit_10+0x7140390>
0x464ac	750600f9	str	x21, [x19, #0x8]
0x464b0	7f0e00f9	str	xzr, [x19, #0x18]
0x464b4	e00313aa	mov	x0, x19
0x464b8	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x464bc	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x464c0	f657c3a8	ldp	x22, x21, [sp], #0x30
0x464c4	c0035fd6	ret
0x464c8	e00313aa	mov	x0, x19
0x464cc	4e000094	bl	0x46604 <_WeChatMain+0x2cd98>
0x464d0	080040f9	ldr	x8, [x0]
0x464d4	a80100b4	cbz	x8, 0x46508 <_WeChatMain+0x2cc9c>
0x464d8	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x464dc	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x464e0	fd430091	add	x29, sp, #0x10
0x464e4	080400f9	str	x8, [x0, #0x8]
0x464e8	090840f9	ldr	x9, [x0, #0x10]
0x464ec	210108cb	sub	x1, x9, x8
0x464f0	f30300aa	mov	x19, x0
0x464f4	e00308aa	mov	x0, x8
0x464f8	c5e6c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x464fc	e00313aa	mov	x0, x19
0x46500	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46504	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x46508	c0035fd6	ret
0x4650c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x46510	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x46514	fd430091	add	x29, sp, #0x10
0x46518	f30300aa	mov	x19, x0
0x4651c	012040a9	ldp	x1, x8, [x0]
0x46520	020101eb	subs	x2, x8, x1
0x46524	80000054	b.eq	0x46534 <_WeChatMain+0x2ccc8>
0x46528	40fc42d3	lsr	x0, x2, #2
0x4652c	3e000094	bl	0x46624 <_WeChatMain+0x2cdb8>
0x46530	02000014	b	0x46538 <_WeChatMain+0x2cccc>
0x46534	00008052	mov	w0, #0x0                ; =0
0x46538	681a40b9	ldr	w8, [x19, #0x18]
0x4653c	1f00086b	cmp	w0, w8
0x46540	e0179f1a	cset	w0, eq
0x46544	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46548	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4654c	c0035fd6	ret
0x46550	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x46554	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x46558	fd430091	add	x29, sp, #0x10
0x4655c	f30300aa	mov	x19, x0
0x46560	012040a9	ldp	x1, x8, [x0]
0x46564	020101eb	subs	x2, x8, x1
0x46568	80000054	b.eq	0x46578 <_WeChatMain+0x2cd0c>
0x4656c	40fc42d3	lsr	x0, x2, #2
0x46570	2d000094	bl	0x46624 <_WeChatMain+0x2cdb8>
0x46574	02000014	b	0x4657c <_WeChatMain+0x2cd10>
0x46578	00008052	mov	w0, #0x0                ; =0
0x4657c	601a00b9	str	w0, [x19, #0x18]
0x46580	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46584	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x46588	c0035fd6	ret
0x4658c	081840b9	ldr	w8, [x0, #0x18]
0x46590	291840b9	ldr	w9, [x1, #0x18]
0x46594	1f01096b	cmp	w8, w9
0x46598	e1020054	b.ne	0x465f4 <_WeChatMain+0x2cd88>
0x4659c	082840a9	ldp	x8, x10, [x0]
0x465a0	4b0108cb	sub	x11, x10, x8
0x465a4	293040a9	ldp	x9, x12, [x1]
0x465a8	8c0109cb	sub	x12, x12, x9
0x465ac	7f010ceb	cmp	x11, x12
0x465b0	21020054	b.ne	0x465f4 <_WeChatMain+0x2cd88>
0x465b4	5f0108eb	cmp	x10, x8
0x465b8	20020054	b.eq	0x465fc <_WeChatMain+0x2cd90>
0x465bc	0a0080d2	mov	x10, #0x0               ; =0
0x465c0	6bfd4293	asr	x11, x11, #2
0x465c4	7f0500f1	cmp	x11, #0x1
0x465c8	6c859f9a	csinc	x12, x11, xzr, hi
0x465cc	0d796ab8	ldr	w13, [x8, x10, lsl #2]
0x465d0	2e796ab8	ldr	w14, [x9, x10, lsl #2]
0x465d4	bf010e6b	cmp	w13, w14
0x465d8	e1000054	b.ne	0x465f4 <_WeChatMain+0x2cd88>
0x465dc	4a050091	add	x10, x10, #0x1
0x465e0	9f010aeb	cmp	x12, x10
0x465e4	41ffff54	b.ne	0x465cc <_WeChatMain+0x2cd60>
0x465e8	5f010beb	cmp	x10, x11
0x465ec	e0379f1a	cset	w0, hs
0x465f0	c0035fd6	ret
0x465f4	00008052	mov	w0, #0x0                ; =0
0x465f8	c0035fd6	ret
0x465fc	20008052	mov	w0, #0x1                ; =1
0x46600	c0035fd6	ret
0x46604	68100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46608	09814539	ldrb	w9, [x8, #0x160]
0x4660c	69000037	tbnz	w9, #0x0, 0x46618 <_WeChatMain+0x2cdac>
0x46610	29008052	mov	w9, #0x1                ; =1
0x46614	09810539	strb	w9, [x8, #0x160]
0x46618	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4661c	fd030091	mov	x29, sp
0x46620	14e7c395	bl	0x7140270 <_wxam_enc_uninit_10+0x7140270>
0x46624	420100b4	cbz	x2, 0x4664c <_WeChatMain+0x2cde0>
0x46628	082204d0	adrp	x8, 0x8488000 <_wxam_enc_uninit_10+0x8488000>
0x4662c	08213991	add	x8, x8, #0xe48
0x46630	29144038	ldrb	w9, [x1], #0x1
0x46634	0a1c0012	and	w10, w0, #0xff
0x46638	4901094a	eor	w9, w10, w9
0x4663c	095969b8	ldr	w9, [x8, w9, uxtw #2]
0x46640	2021404a	eor	w0, w9, w0, lsr #8
0x46644	420400f1	subs	x2, x2, #0x1
0x46648	41ffff54	b.ne	0x46630 <_WeChatMain+0x2cdc4>
0x4664c	c0035fd6	ret
0x46650	68100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46654	08210691	add	x8, x8, #0x188
0x46658	08c1bf38	ldaprb	w8, [x8]
0x4665c	88000036	tbz	w8, #0x0, 0x4666c <_WeChatMain+0x2ce00>
0x46660	60100590	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46664	00400691	add	x0, x0, #0x190
0x46668	c0035fd6	ret
0x4666c	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x46670	fd030091	mov	x29, sp
0x46674	0c0bc295	bl	0x70c92a4 <_SetWeixinCallbackFunc+0x22e1ea8>
0x46678	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4667c	f9ffff17	b	0x46660 <_WeChatMain+0x2cdf4>
0x46680	68100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46684	09014639	ldrb	w9, [x8, #0x180]
0x46688	e9000037	tbnz	w9, #0x0, 0x466a4 <_WeChatMain+0x2ce38>
0x4668c	092204f0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x46690	2095c03d	ldr	q0, [x9, #0x250]
0x46694	69100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46698	205d803d	str	q0, [x9, #0x170]
0x4669c	29008052	mov	w9, #0x1                ; =1
0x466a0	09010639	strb	w9, [x8, #0x180]
0x466a4	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x466a8	fd030091	mov	x29, sp
0x466ac	61100590	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x466b0	21c00591	add	x1, x1, #0x170
0x466b4	86130094	bl	0x4b4cc <_WeChatMain+0x31c60>
0x466b8	88d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x466bc	08412f91	add	x8, x8, #0xbd0
0x466c0	080000f9	str	x8, [x0]
0x466c4	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x466c8	c0035fd6	ret
0x466cc	ffc300d1	sub	sp, sp, #0x30
0x466d0	f44f01a9	stp	x20, x19, [sp, #0x10]
0x466d4	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x466d8	fd830091	add	x29, sp, #0x20
0x466dc	130440f9	ldr	x19, [x0, #0x8]
0x466e0	b30000b4	cbz	x19, 0x466f4 <_WeChatMain+0x2ce88>
0x466e4	e00313aa	mov	x0, x19
0x466e8	c4ecc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x466ec	e10300aa	mov	x1, x0
0x466f0	0b000014	b	0x4671c <_WeChatMain+0x2ceb0>
0x466f4	a0bf04d0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x466f8	00800791	add	x0, x0, #0x1e0
0x466fc	a2bf04d0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x46700	42300991	add	x2, x2, #0x24c
0x46704	e8230091	add	x8, sp, #0x8
0x46708	a10f8052	mov	w1, #0x7d               ; =125
0x4670c	ee6bff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x46710	e0230091	add	x0, sp, #0x8
0x46714	5650ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x46718	010080d2	mov	x1, #0x0                ; =0
0x4671c	e00313aa	mov	x0, x19
0x46720	c01a0094	bl	0x4d220 <_WeChatMain+0x339b4>
0x46724	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x46728	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4672c	ffc30091	add	sp, sp, #0x30
0x46730	c0035fd6	ret
0x46734	a0008052	mov	w0, #0x5                ; =5
0x46738	c0035fd6	ret
0x4673c	20008052	mov	w0, #0x1                ; =1
0x46740	c0035fd6	ret
0x46744	20008052	mov	w0, #0x1                ; =1
0x46748	c0035fd6	ret
0x4674c	ffc300d1	sub	sp, sp, #0x30
0x46750	f44f01a9	stp	x20, x19, [sp, #0x10]
0x46754	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x46758	fd830091	add	x29, sp, #0x20
0x4675c	f30308aa	mov	x19, x8
0x46760	00038052	mov	w0, #0x18               ; =24
0x46764	33e6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x46768	f40300aa	mov	x20, x0
0x4676c	00038052	mov	w0, #0x18               ; =24
0x46770	30e6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x46774	d392ff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x46778	e00700f9	str	x0, [sp, #0x8]
0x4677c	e2230091	add	x2, sp, #0x8
0x46780	e00314aa	mov	x0, x20
0x46784	010080d2	mov	x1, #0x0                ; =0
0x46788	be150094	bl	0x4be80 <_WeChatMain+0x32614>
0x4678c	e00740f9	ldr	x0, [sp, #0x8]
0x46790	ff0700f9	str	xzr, [sp, #0x8]
0x46794	600000b4	cbz	x0, 0x467a0 <_WeChatMain+0x2cf34>
0x46798	01038052	mov	w1, #0x18               ; =24
0x4679c	1ce6c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x467a0	88d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x467a4	08413291	add	x8, x8, #0xc90
0x467a8	880200f9	str	x8, [x20]
0x467ac	740200f9	str	x20, [x19]
0x467b0	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x467b4	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x467b8	ffc30091	add	sp, sp, #0x30
0x467bc	c0035fd6	ret
0x467c0	ffc300d1	sub	sp, sp, #0x30
0x467c4	f44f01a9	stp	x20, x19, [sp, #0x10]
0x467c8	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x467cc	fd830091	add	x29, sp, #0x20
0x467d0	f30308aa	mov	x19, x8
0x467d4	00038052	mov	w0, #0x18               ; =24
0x467d8	16e6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x467dc	f40300aa	mov	x20, x0
0x467e0	00038052	mov	w0, #0x18               ; =24
0x467e4	13e6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x467e8	b692ff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x467ec	e00700f9	str	x0, [sp, #0x8]
0x467f0	e2230091	add	x2, sp, #0x8
0x467f4	e00314aa	mov	x0, x20
0x467f8	010080d2	mov	x1, #0x0                ; =0
0x467fc	a1150094	bl	0x4be80 <_WeChatMain+0x32614>
0x46800	e00740f9	ldr	x0, [sp, #0x8]
0x46804	ff0700f9	str	xzr, [sp, #0x8]
0x46808	600000b4	cbz	x0, 0x46814 <_WeChatMain+0x2cfa8>
0x4680c	01038052	mov	w1, #0x18               ; =24
0x46810	ffe5c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46814	88d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x46818	08413291	add	x8, x8, #0xc90
0x4681c	880200f9	str	x8, [x20]
0x46820	740200f9	str	x20, [x19]
0x46824	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x46828	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4682c	ffc30091	add	sp, sp, #0x30
0x46830	c0035fd6	ret
0x46834	ffc300d1	sub	sp, sp, #0x30
0x46838	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4683c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x46840	fd830091	add	x29, sp, #0x20
0x46844	f30308aa	mov	x19, x8
0x46848	00038052	mov	w0, #0x18               ; =24
0x4684c	f9e5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x46850	f40300aa	mov	x20, x0
0x46854	00038052	mov	w0, #0x18               ; =24
0x46858	f6e5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4685c	9992ff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x46860	e00700f9	str	x0, [sp, #0x8]
0x46864	e2230091	add	x2, sp, #0x8
0x46868	e00314aa	mov	x0, x20
0x4686c	010080d2	mov	x1, #0x0                ; =0
0x46870	84150094	bl	0x4be80 <_WeChatMain+0x32614>
0x46874	e00740f9	ldr	x0, [sp, #0x8]
0x46878	ff0700f9	str	xzr, [sp, #0x8]
0x4687c	600000b4	cbz	x0, 0x46888 <_WeChatMain+0x2d01c>
0x46880	01038052	mov	w1, #0x18               ; =24
0x46884	e2e5c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46888	88d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4688c	08413291	add	x8, x8, #0xc90
0x46890	880200f9	str	x8, [x20]
0x46894	740200f9	str	x20, [x19]
0x46898	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4689c	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x468a0	ffc30091	add	sp, sp, #0x30
0x468a4	c0035fd6	ret
0x468a8	e00308aa	mov	x0, x8
0x468ac	8592ff17	b	0x2b2c0 <_WeChatMain+0x11a54>
0x468b0	e00308aa	mov	x0, x8
0x468b4	8392ff17	b	0x2b2c0 <_WeChatMain+0x11a54>
0x468b8	0551ff17	b	0x1accc <_WeChatMain+0x1460>
0x468bc	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x468c0	fd030091	mov	x29, sp
0x468c4	0251ff97	bl	0x1accc <_WeChatMain+0x1460>
0x468c8	01038052	mov	w1, #0x18               ; =24
0x468cc	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x468d0	cfe5c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x468d4	c0035fd6	ret
0x468d8	c0035fd6	ret
0x468dc	c0035fd6	ret
0x468e0	c0035fd6	ret
0x468e4	c0035fd6	ret
0x468e8	c0035fd6	ret
0x468ec	88150014	b	0x4bf0c <_WeChatMain+0x326a0>
0x468f0	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x468f4	fd030091	mov	x29, sp
0x468f8	85150094	bl	0x4bf0c <_WeChatMain+0x326a0>
0x468fc	01038052	mov	w1, #0x18               ; =24
0x46900	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x46904	c2e5c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46908	c0035fd6	ret
0x4690c	00008052	mov	w0, #0x0                ; =0
0x46910	c0035fd6	ret
0x46914	00008052	mov	w0, #0x0                ; =0
0x46918	c0035fd6	ret
0x4691c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x46920	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x46924	fd430091	add	x29, sp, #0x10
0x46928	f30308aa	mov	x19, x8
0x4692c	00018052	mov	w0, #0x8                ; =8
0x46930	c0e5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x46934	88d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x46938	08813491	add	x8, x8, #0xd20
0x4693c	080000f9	str	x8, [x0]
0x46940	600200f9	str	x0, [x19]
0x46944	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46948	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4694c	c0035fd6	ret
0x46950	20008052	mov	w0, #0x1                ; =1
0x46954	c0035fd6	ret
0x46958	dd50ff17	b	0x1accc <_WeChatMain+0x1460>
0x4695c	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x46960	fd030091	mov	x29, sp
0x46964	da50ff97	bl	0x1accc <_WeChatMain+0x1460>
0x46968	01018052	mov	w1, #0x8                ; =8
0x4696c	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x46970	a7e5c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46974	20008052	mov	w0, #0x1                ; =1
0x46978	c0035fd6	ret
0x4697c	c0035fd6	ret
0x46980	c0035fd6	ret
0x46984	ff0304d1	sub	sp, sp, #0x100
0x46988	fc6f0aa9	stp	x28, x27, [sp, #0xa0]
0x4698c	fa670ba9	stp	x26, x25, [sp, #0xb0]
0x46990	f85f0ca9	stp	x24, x23, [sp, #0xc0]
0x46994	f6570da9	stp	x22, x21, [sp, #0xd0]
0x46998	f44f0ea9	stp	x20, x19, [sp, #0xe0]
0x4699c	fd7b0fa9	stp	x29, x30, [sp, #0xf0]
0x469a0	fdc30391	add	x29, sp, #0xf0
0x469a4	f30301aa	mov	x19, x1
0x469a8	e80300aa	mov	x8, x0
0x469ac	e9f301b2	mov	x9, #-0x5555555555555556 ; =-6148914691236517206
0x469b0	e92705a9	stp	x9, x9, [sp, #0x50]
0x469b4	e92700f9	str	x9, [sp, #0x48]
0x469b8	e94300f9	str	x9, [sp, #0x80]
0x469bc	40e5054f	movi.16b	v0, #0xaa
0x469c0	e00303ad	stp	q0, q0, [sp, #0x60]
0x469c4	020440f9	ldr	x2, [x0, #0x8]
0x469c8	e0830191	add	x0, sp, #0x60
0x469cc	01410091	add	x1, x8, #0x10
0x469d0	d8450094	bl	0x58130 <_WeChatMain+0x3e8c4>
0x469d4	e0230191	add	x0, sp, #0x48
0x469d8	e1830191	add	x1, sp, #0x60
0x469dc	5d440094	bl	0x57b50 <_WeChatMain+0x3e2e4>
0x469e0	e0830191	add	x0, sp, #0x60
0x469e4	17460094	bl	0x58240 <_WeChatMain+0x3e9d4>
0x469e8	ffff03a9	stp	xzr, xzr, [sp, #0x38]
0x469ec	e0230191	add	x0, sp, #0x48
0x469f0	e1e30091	add	x1, sp, #0x38
0x469f4	ad440094	bl	0x57ca8 <_WeChatMain+0x3e43c>
0x469f8	400d0034	cbz	w0, 0x46ba0 <_WeChatMain+0x2d334>
0x469fc	e0230191	add	x0, sp, #0x48
0x46a00	e1e30091	add	x1, sp, #0x38
0x46a04	a9440094	bl	0x57ca8 <_WeChatMain+0x3e43c>
0x46a08	c00c0034	cbz	w0, 0x46ba0 <_WeChatMain+0x2d334>
0x46a0c	ffff02a9	stp	xzr, xzr, [sp, #0x28]
0x46a10	ffff01a9	stp	xzr, xzr, [sp, #0x18]
0x46a14	e0230191	add	x0, sp, #0x48
0x46a18	e1a30091	add	x1, sp, #0x28
0x46a1c	a3440094	bl	0x57ca8 <_WeChatMain+0x3e43c>
0x46a20	a00b0034	cbz	w0, 0x46b94 <_WeChatMain+0x2d328>
0x46a24	19018092	mov	x25, #-0x9              ; =-9
0x46a28	f9ffeff2	movk	x25, #0x7fff, lsl #48
0x46a2c	fa030091	mov	x26, sp
0x46a30	3b038052	mov	w27, #0x19              ; =25
0x46a34	b4590490	adrp	x20, 0x8b7a000 <_wxam_enc_uninit_10+0x8b7a000>
0x46a38	94e22291	add	x20, x20, #0x8b8
0x46a3c	07000014	b	0x46a58 <_WeChatMain+0x2d1ec>
0x46a40	ffff02a9	stp	xzr, xzr, [sp, #0x28]
0x46a44	ffff01a9	stp	xzr, xzr, [sp, #0x18]
0x46a48	e0230191	add	x0, sp, #0x48
0x46a4c	e1a30091	add	x1, sp, #0x28
0x46a50	96440094	bl	0x57ca8 <_WeChatMain+0x3e43c>
0x46a54	000a0036	tbz	w0, #0x0, 0x46b94 <_WeChatMain+0x2d328>
0x46a58	e0230191	add	x0, sp, #0x48
0x46a5c	e1630091	add	x1, sp, #0x18
0x46a60	92440094	bl	0x57ca8 <_WeChatMain+0x3e43c>
0x46a64	80090036	tbz	w0, #0x0, 0x46b94 <_WeChatMain+0x2d328>
0x46a68	f51340f9	ldr	x21, [sp, #0x20]
0x46a6c	bf0219eb	cmp	x21, x25
0x46a70	880a0054	b.hi	0x46bc0 <_WeChatMain+0x2d354>
0x46a74	f60f40f9	ldr	x22, [sp, #0x18]
0x46a78	bf5e00f1	cmp	x21, #0x17
0x46a7c	a2000054	b.hs	0x46a90 <_WeChatMain+0x2d224>
0x46a80	f5df0139	strb	w21, [sp, #0x77]
0x46a84	f7830191	add	x23, sp, #0x60
0x46a88	750100b5	cbnz	x21, 0x46ab4 <_WeChatMain+0x2d248>
0x46a8c	0e000014	b	0x46ac4 <_WeChatMain+0x2d258>
0x46a90	a80a40b2	orr	x8, x21, #0x7
0x46a94	1f5d00f1	cmp	x8, #0x17
0x46a98	7807889a	csinc	x24, x27, x8, eq
0x46a9c	e00318aa	mov	x0, x24
0x46aa0	64e5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x46aa4	f70300aa	mov	x23, x0
0x46aa8	080341b2	orr	x8, x24, #0x8000000000000000
0x46aac	f5a306a9	stp	x21, x8, [sp, #0x68]
0x46ab0	e03300f9	str	x0, [sp, #0x60]
0x46ab4	e00317aa	mov	x0, x23
0x46ab8	e10316aa	mov	x1, x22
0x46abc	e20315aa	mov	x2, x21
0x46ac0	f5e8c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x46ac4	ff6a3538	strb	wzr, [x23, x21]
0x46ac8	f51b40f9	ldr	x21, [sp, #0x30]
0x46acc	bf0219eb	cmp	x21, x25
0x46ad0	c8070054	b.hi	0x46bc8 <_WeChatMain+0x2d35c>
0x46ad4	f61740f9	ldr	x22, [sp, #0x28]
0x46ad8	bf5e00f1	cmp	x21, #0x17
0x46adc	a2000054	b.hs	0x46af0 <_WeChatMain+0x2d284>
0x46ae0	f55f0039	strb	w21, [sp, #0x17]
0x46ae4	f7030091	mov	x23, sp
0x46ae8	750100b5	cbnz	x21, 0x46b14 <_WeChatMain+0x2d2a8>
0x46aec	0e000014	b	0x46b24 <_WeChatMain+0x2d2b8>
0x46af0	a80a40b2	orr	x8, x21, #0x7
0x46af4	1f5d00f1	cmp	x8, #0x17
0x46af8	7807889a	csinc	x24, x27, x8, eq
0x46afc	e00318aa	mov	x0, x24
0x46b00	4ce5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x46b04	f70300aa	mov	x23, x0
0x46b08	080341b2	orr	x8, x24, #0x8000000000000000
0x46b0c	f5a300a9	stp	x21, x8, [sp, #0x8]
0x46b10	e00300f9	str	x0, [sp]
0x46b14	e00317aa	mov	x0, x23
0x46b18	e10316aa	mov	x1, x22
0x46b1c	e20315aa	mov	x2, x21
0x46b20	dde8c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x46b24	ff6a3538	strb	wzr, [x23, x21]
0x46b28	ba831af8	stur	x26, [x29, #-0x58]
0x46b2c	e1030091	mov	x1, sp
0x46b30	a36301d1	sub	x3, x29, #0x58
0x46b34	a46701d1	sub	x4, x29, #0x59
0x46b38	e00313aa	mov	x0, x19
0x46b3c	e20314aa	mov	x2, x20
0x46b40	5776ff97	bl	0x2449c <_WeChatMain+0xac30>
0x46b44	083cc139	ldrsb	w8, [x0, #0x4f]
0x46b48	0801f836	tbz	w8, #0x1f, 0x46b68 <_WeChatMain+0x2d2fc>
0x46b4c	081c40f9	ldr	x8, [x0, #0x38]
0x46b50	092440f9	ldr	x9, [x0, #0x48]
0x46b54	21f94092	and	x1, x9, #0x7fffffffffffffff
0x46b58	f50300aa	mov	x21, x0
0x46b5c	e00308aa	mov	x0, x8
0x46b60	2be5c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46b64	e00315aa	mov	x0, x21
0x46b68	e01bc03d	ldr	q0, [sp, #0x60]
0x46b6c	0080833c	stur	q0, [x0, #0x38]
0x46b70	e83b40f9	ldr	x8, [sp, #0x70]
0x46b74	088004f8	stur	x8, [x0, #0x48]
0x46b78	e85fc039	ldrsb	w8, [sp, #0x17]
0x46b7c	28f6ff36	tbz	w8, #0x1f, 0x46a40 <_WeChatMain+0x2d1d4>
0x46b80	e00340f9	ldr	x0, [sp]
0x46b84	e80b40f9	ldr	x8, [sp, #0x10]
0x46b88	01f94092	and	x1, x8, #0x7fffffffffffffff
0x46b8c	20e5c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46b90	acffff17	b	0x46a40 <_WeChatMain+0x2d1d4>
0x46b94	e81b40f9	ldr	x8, [sp, #0x30]
0x46b98	1f0100f1	cmp	x8, #0x0
0x46b9c	e0179f1a	cset	w0, eq
0x46ba0	fd7b4fa9	ldp	x29, x30, [sp, #0xf0]
0x46ba4	f44f4ea9	ldp	x20, x19, [sp, #0xe0]
0x46ba8	f6574da9	ldp	x22, x21, [sp, #0xd0]
0x46bac	f85f4ca9	ldp	x24, x23, [sp, #0xc0]
0x46bb0	fa674ba9	ldp	x26, x25, [sp, #0xb0]
0x46bb4	fc6f4aa9	ldp	x28, x27, [sp, #0xa0]
0x46bb8	ff030491	add	sp, sp, #0x100
0x46bbc	c0035fd6	ret
0x46bc0	e0830191	add	x0, sp, #0x60
0x46bc4	2e50ff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x46bc8	e0030091	mov	x0, sp
0x46bcc	2c50ff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x46bd0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x46bd4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x46bd8	fd430091	add	x29, sp, #0x10
0x46bdc	f30300aa	mov	x19, x0
0x46be0	0b000094	bl	0x46c0c <_WeChatMain+0x2d3a0>
0x46be4	68ca4139	ldrb	w8, [x19, #0x72]
0x46be8	1f050071	cmp	w8, #0x1
0x46bec	a1000054	b.ne	0x46c00 <_WeChatMain+0x2d394>
0x46bf0	e00313aa	mov	x0, x19
0x46bf4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46bf8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x46bfc	38000014	b	0x46cdc <_WeChatMain+0x2d470>
0x46c00	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46c04	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x46c08	c0035fd6	ret
0x46c0c	085440b9	ldr	w8, [x0, #0x54]
0x46c10	1f050031	cmn	w8, #0x1
0x46c14	40000054	b.eq	0x46c1c <_WeChatMain+0x2d3b0>
0x46c18	c0035fd6	ret
0x46c1c	082840b9	ldr	w8, [x0, #0x28]
0x46c20	084c00b9	str	w8, [x0, #0x4c]
0x46c24	1f5400b9	str	wzr, [x0, #0x54]
0x46c28	081c4139	ldrb	w8, [x0, #0x47]
0x46c2c	0a1d0013	sxtb	w10, w8
0x46c30	021c40f9	ldr	x2, [x0, #0x38]
0x46c34	5f010071	cmp	w10, #0x0
0x46c38	48b0889a	csel	x8, x2, x8, lt
0x46c3c	480100b4	cbz	x8, 0x46c64 <_WeChatMain+0x2d3f8>
0x46c40	09c00091	add	x9, x0, #0x30
0x46c44	0bbcc139	ldrsb	w11, [x0, #0x6f]
0x46c48	8b03f837	tbnz	w11, #0x1f, 0x46cb8 <_WeChatMain+0x2d44c>
0x46c4c	2a04f837	tbnz	w10, #0x1f, 0x46cd0 <_WeChatMain+0x2d464>
0x46c50	2001c03d	ldr	q0, [x9]
0x46c54	0080853c	stur	q0, [x0, #0x58]
0x46c58	280940f9	ldr	x8, [x9, #0x10]
0x46c5c	088006f8	stur	x8, [x0, #0x68]
0x46c60	c0035fd6	ret
0x46c64	68100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46c68	09cd4639	ldrb	w9, [x8, #0x1b3]
0x46c6c	09010037	tbnz	w9, #0x0, 0x46c8c <_WeChatMain+0x2d420>
0x46c70	69100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46c74	29c10691	add	x9, x9, #0x1b0
0x46c78	aa848c52	mov	w10, #0x6425            ; =25637
0x46c7c	2a010079	strh	w10, [x9]
0x46c80	3f090039	strb	wzr, [x9, #0x2]
0x46c84	29008052	mov	w9, #0x1                ; =1
0x46c88	09cd0639	strb	w9, [x8, #0x1b3]
0x46c8c	ff8300d1	sub	sp, sp, #0x20
0x46c90	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x46c94	fd430091	add	x29, sp, #0x10
0x46c98	ff0300f9	str	xzr, [sp]
0x46c9c	61100590	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x46ca0	21c00691	add	x1, x1, #0x1b0
0x46ca4	00600191	add	x0, x0, #0x58
0x46ca8	7c850094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x46cac	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46cb0	ff830091	add	sp, sp, #0x20
0x46cb4	c0035fd6	ret
0x46cb8	2b0140f9	ldr	x11, [x9]
0x46cbc	5f010071	cmp	w10, #0x0
0x46cc0	61b1899a	csel	x1, x11, x9, lt
0x46cc4	00600191	add	x0, x0, #0x58
0x46cc8	e20308aa	mov	x2, x8
0x46ccc	d373ff17	b	0x23c18 <_WeChatMain+0xa3ac>
0x46cd0	210140f9	ldr	x1, [x9]
0x46cd4	00600191	add	x0, x0, #0x58
0x46cd8	a073ff17	b	0x23b58 <_WeChatMain+0xa2ec>
0x46cdc	ff4301d1	sub	sp, sp, #0x50
0x46ce0	f65702a9	stp	x22, x21, [sp, #0x20]
0x46ce4	f44f03a9	stp	x20, x19, [sp, #0x30]
0x46ce8	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x46cec	fd030191	add	x29, sp, #0x40
0x46cf0	b52605d0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x46cf4	b4e245f9	ldr	x20, [x21, #0xbc0]
0x46cf8	d40800b4	cbz	x20, 0x46e10 <_WeChatMain+0x2d5a4>
0x46cfc	f30300aa	mov	x19, x0
0x46d00	ffff00a9	stp	xzr, xzr, [sp, #0x8]
0x46d04	ff0f00f9	str	xzr, [sp, #0x18]
0x46d08	e00314aa	mov	x0, x20
0x46d0c	fae9c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x46d10	c0000035	cbnz	w0, 0x46d28 <_WeChatMain+0x2d4bc>
0x46d14	68c64139	ldrb	w8, [x19, #0x71]
0x46d18	08010036	tbz	w8, #0x0, 0x46d38 <_WeChatMain+0x2d4cc>
0x46d1c	e00314aa	mov	x0, x20
0x46d20	f8e9c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x46d24	3b000014	b	0x46e10 <_WeChatMain+0x2d5a4>
0x46d28	e00314aa	mov	x0, x20
0x46d2c	d68d0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x46d30	68c64139	ldrb	w8, [x19, #0x71]
0x46d34	48ff0737	tbnz	w8, #0x0, 0x46d1c <_WeChatMain+0x2d4b0>
0x46d38	28008052	mov	w8, #0x1                ; =1
0x46d3c	68c60139	strb	w8, [x19, #0x71]
0x46d40	a9e245f9	ldr	x9, [x21, #0xbc0]
0x46d44	29e10191	add	x9, x9, #0x78
0x46d48	2801e8b8	ldaddal	w8, w8, [x9]
0x46d4c	a8e245f9	ldr	x8, [x21, #0xbc0]
0x46d50	004140f9	ldr	x0, [x8, #0x80]
0x46d54	c00100b4	cbz	x0, 0x46d8c <_WeChatMain+0x2d520>
0x46d58	08a04039	ldrb	w8, [x0, #0x28]
0x46d5c	88010037	tbnz	w8, #0x0, 0x46d8c <_WeChatMain+0x2d520>
0x46d60	617640b9	ldr	w1, [x19, #0x74]
0x46d64	01010034	cbz	w1, 0x46d84 <_WeChatMain+0x2d518>
0x46d68	c2c28f52	mov	w2, #0x7e16             ; =32278
0x46d6c	2274b572	movk	w2, #0xaba1, lsl #16
0x46d70	03028052	mov	w3, #0x10               ; =16
0x46d74	451f0094	bl	0x4ea88 <_WeChatMain+0x3521c>
0x46d78	28008052	mov	w8, #0x1                ; =1
0x46d7c	080000b9	str	w8, [x0]
0x46d80	03000014	b	0x46d8c <_WeChatMain+0x2d520>
0x46d84	e10313aa	mov	x1, x19
0x46d88	8f000094	bl	0x46fc4 <_WeChatMain+0x2d758>
0x46d8c	a8e245f9	ldr	x8, [x21, #0xbc0]
0x46d90	09810191	add	x9, x8, #0x60
0x46d94	ea230091	add	x10, sp, #0x8
0x46d98	5f0109eb	cmp	x10, x9
0x46d9c	c0000054	b.eq	0x46db4 <_WeChatMain+0x2d548>
0x46da0	010946a9	ldp	x1, x2, [x8, #0x60]
0x46da4	480001cb	sub	x8, x2, x1
0x46da8	03fd4393	asr	x3, x8, #3
0x46dac	e0230091	add	x0, sp, #0x8
0x46db0	92010094	bl	0x473f8 <_WeChatMain+0x2db8c>
0x46db4	e00314aa	mov	x0, x20
0x46db8	d2e9c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x46dbc	f4db40a9	ldp	x20, x22, [sp, #0x8]
0x46dc0	9f0216eb	cmp	x20, x22
0x46dc4	20010054	b.eq	0x46de8 <_WeChatMain+0x2d57c>
0x46dc8	808640f8	ldr	x0, [x20], #0x8
0x46dcc	080040f9	ldr	x8, [x0]
0x46dd0	080140f9	ldr	x8, [x8]
0x46dd4	61420091	add	x1, x19, #0x10
0x46dd8	62620191	add	x2, x19, #0x58
0x46ddc	00013fd6	blr	x8
0x46de0	9f0216eb	cmp	x20, x22
0x46de4	21ffff54	b.ne	0x46dc8 <_WeChatMain+0x2d55c>
0x46de8	a8e245f9	ldr	x8, [x21, #0xbc0]
0x46dec	08e10191	add	x8, x8, #0x78
0x46df0	09008012	mov	w9, #-0x1               ; =-1
0x46df4	0801e9b8	ldaddal	w9, w8, [x8]
0x46df8	e00740f9	ldr	x0, [sp, #0x8]
0x46dfc	a00000b4	cbz	x0, 0x46e10 <_WeChatMain+0x2d5a4>
0x46e00	e00b00f9	str	x0, [sp, #0x10]
0x46e04	e80f40f9	ldr	x8, [sp, #0x18]
0x46e08	010100cb	sub	x1, x8, x0
0x46e0c	80e4c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x46e10	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x46e14	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x46e18	f65742a9	ldp	x22, x21, [sp, #0x20]
0x46e1c	ff430191	add	sp, sp, #0x50
0x46e20	c0035fd6	ret
0x46e24	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x46e28	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x46e2c	fd430091	add	x29, sp, #0x10
0x46e30	f30300aa	mov	x19, x0
0x46e34	76ffff97	bl	0x46c0c <_WeChatMain+0x2d3a0>
0x46e38	68ca4139	ldrb	w8, [x19, #0x72]
0x46e3c	1f050071	cmp	w8, #0x1
0x46e40	61000054	b.ne	0x46e4c <_WeChatMain+0x2d5e0>
0x46e44	e00313aa	mov	x0, x19
0x46e48	a5ffff97	bl	0x46cdc <_WeChatMain+0x2d470>
0x46e4c	60620191	add	x0, x19, #0x58
0x46e50	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x46e54	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x46e58	c0035fd6	ret
0x46e5c	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x46e60	f44f01a9	stp	x20, x19, [sp, #0x10]
0x46e64	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x46e68	fd830091	add	x29, sp, #0x20
0x46e6c	f30301aa	mov	x19, x1
0x46e70	f40300aa	mov	x20, x0
0x46e74	66ffff97	bl	0x46c0c <_WeChatMain+0x2d3a0>
0x46e78	95420091	add	x21, x20, #0x10
0x46e7c	600240f9	ldr	x0, [x19]
0x46e80	08745e92	and	x8, x0, #0xfffffffc00000000
0x46e84	b6fd0490	adrp	x22, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x46e88	d6023b91	add	x22, x22, #0xec0
0x46e8c	c90640f9	ldr	x9, [x22, #0x8]
0x46e90	1f0109eb	cmp	x8, x9
0x46e94	41000054	b.ne	0x46e9c <_WeChatMain+0x2d630>
0x46e98	0ae3ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x46e9c	a8765e92	and	x8, x21, #0xfffffffc00000000
0x46ea0	c90640f9	ldr	x9, [x22, #0x8]
0x46ea4	1f0109eb	cmp	x8, x9
0x46ea8	61000054	b.ne	0x46eb4 <_WeChatMain+0x2d648>
0x46eac	e00315aa	mov	x0, x21
0x46eb0	67e2ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x46eb4	750200f9	str	x21, [x19]
0x46eb8	95620191	add	x21, x20, #0x58
0x46ebc	600640f9	ldr	x0, [x19, #0x8]
0x46ec0	08745e92	and	x8, x0, #0xfffffffc00000000
0x46ec4	c90640f9	ldr	x9, [x22, #0x8]
0x46ec8	1f0109eb	cmp	x8, x9
0x46ecc	41000054	b.ne	0x46ed4 <_WeChatMain+0x2d668>
0x46ed0	fce2ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x46ed4	a8765e92	and	x8, x21, #0xfffffffc00000000
0x46ed8	c90640f9	ldr	x9, [x22, #0x8]
0x46edc	1f0109eb	cmp	x8, x9
0x46ee0	61000054	b.ne	0x46eec <_WeChatMain+0x2d680>
0x46ee4	e00315aa	mov	x0, x21
0x46ee8	59e2ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x46eec	750600f9	str	x21, [x19, #0x8]
0x46ef0	88c64139	ldrb	w8, [x20, #0x71]
0x46ef4	68420039	strb	w8, [x19, #0x10]
0x46ef8	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x46efc	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x46f00	f657c3a8	ldp	x22, x21, [sp], #0x30
0x46f04	c0035fd6	ret
0x46f08	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x46f0c	f65701a9	stp	x22, x21, [sp, #0x10]
0x46f10	f44f02a9	stp	x20, x19, [sp, #0x20]
0x46f14	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x46f18	fdc30091	add	x29, sp, #0x30
0x46f1c	f40301aa	mov	x20, x1
0x46f20	f50300aa	mov	x21, x0
0x46f24	b72605d0	adrp	x23, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x46f28	f3e245f9	ldr	x19, [x23, #0xbc0]
0x46f2c	e00313aa	mov	x0, x19
0x46f30	71e9c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x46f34	20040035	cbnz	w0, 0x46fb8 <_WeChatMain+0x2d74c>
0x46f38	e8e245f9	ldr	x8, [x23, #0xbc0]
0x46f3c	004140f9	ldr	x0, [x8, #0x80]
0x46f40	000200b4	cbz	x0, 0x46f80 <_WeChatMain+0x2d714>
0x46f44	a17640b9	ldr	w1, [x21, #0x74]
0x46f48	c1010034	cbz	w1, 0x46f80 <_WeChatMain+0x2d714>
0x46f4c	c2c28f52	mov	w2, #0x7e16             ; =32278
0x46f50	2274b572	movk	w2, #0xaba1, lsl #16
0x46f54	03028052	mov	w3, #0x10               ; =16
0x46f58	cc1e0094	bl	0x4ea88 <_WeChatMain+0x3521c>
0x46f5c	f60300aa	mov	x22, x0
0x46f60	e8e245f9	ldr	x8, [x23, #0xbc0]
0x46f64	004140f9	ldr	x0, [x8, #0x80]
0x46f68	a17640b9	ldr	w1, [x21, #0x74]
0x46f6c	781e0094	bl	0x4e94c <_WeChatMain+0x350e0>
0x46f70	c90640f9	ldr	x9, [x22, #0x8]
0x46f74	29410091	add	x9, x9, #0x10
0x46f78	1f0009eb	cmp	x0, x9
0x46f7c	42010054	b.hs	0x46fa4 <_WeChatMain+0x2d738>
0x46f80	14008052	mov	w20, #0x0               ; =0
0x46f84	e00313aa	mov	x0, x19
0x46f88	5ee9c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x46f8c	e00314aa	mov	x0, x20
0x46f90	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x46f94	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x46f98	f65741a9	ldp	x22, x21, [sp, #0x10]
0x46f9c	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x46fa0	c0035fd6	ret
0x46fa4	e00316aa	mov	x0, x22
0x46fa8	e10314aa	mov	x1, x20
0x46fac	76feff97	bl	0x46984 <_WeChatMain+0x2d118>
0x46fb0	f40300aa	mov	x20, x0
0x46fb4	f4ffff17	b	0x46f84 <_WeChatMain+0x2d718>
0x46fb8	e00313aa	mov	x0, x19
0x46fbc	328d0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x46fc0	deffff17	b	0x46f38 <_WeChatMain+0x2d6cc>
0x46fc4	802000b4	cbz	x0, 0x473d4 <_WeChatMain+0x2db68>
0x46fc8	08a04039	ldrb	w8, [x0, #0x28]
0x46fcc	48200037	tbnz	w8, #0x0, 0x473d4 <_WeChatMain+0x2db68>
0x46fd0	ff4303d1	sub	sp, sp, #0xd0
0x46fd4	fa6708a9	stp	x26, x25, [sp, #0x80]
0x46fd8	f85f09a9	stp	x24, x23, [sp, #0x90]
0x46fdc	f6570aa9	stp	x22, x21, [sp, #0xa0]
0x46fe0	f44f0ba9	stp	x20, x19, [sp, #0xb0]
0x46fe4	fd7b0ca9	stp	x29, x30, [sp, #0xc0]
0x46fe8	fd030391	add	x29, sp, #0xc0
0x46fec	f30301aa	mov	x19, x1
0x46ff0	f40300aa	mov	x20, x0
0x46ff4	f5f301b2	mov	x21, #-0x5555555555555556 ; =-6148914691236517206
0x46ff8	ffd703a9	stp	xzr, x21, [sp, #0x38]
0x46ffc	ff1b00f9	str	xzr, [sp, #0x30]
0x47000	ff030139	strb	wzr, [sp, #0x40]
0x47004	e1c30091	add	x1, sp, #0x30
0x47008	e00313aa	mov	x0, x19
0x4700c	94ffff97	bl	0x46e5c <_WeChatMain+0x2d5f0>
0x47010	687640b9	ldr	w8, [x19, #0x74]
0x47014	68000034	cbz	w8, 0x47020 <_WeChatMain+0x2d7b4>
0x47018	f51f40f9	ldr	x21, [sp, #0x38]
0x4701c	da000014	b	0x47384 <_WeChatMain+0x2db18>
0x47020	f7030091	mov	x23, sp
0x47024	f51300f9	str	x21, [sp, #0x20]
0x47028	40e5054f	movi.16b	v0, #0xaa
0x4702c	e00300ad	stp	q0, q0, [sp]
0x47030	e0030091	mov	x0, sp
0x47034	02440094	bl	0x5803c <_WeChatMain+0x3e7d0>
0x47038	f65743a9	ldp	x22, x21, [sp, #0x30]
0x4703c	c85e8039	ldrsb	x8, [x22, #0x17]
0x47040	c92a40a9	ldp	x9, x10, [x22]
0x47044	1f0100f1	cmp	x8, #0x0
0x47048	29b1969a	csel	x9, x9, x22, lt
0x4704c	1f010071	cmp	w8, #0x0
0x47050	48b1889a	csel	x8, x10, x8, lt
0x47054	e9a305a9	stp	x9, x8, [sp, #0x58]
0x47058	a85e8039	ldrsb	x8, [x21, #0x17]
0x4705c	a92a40a9	ldp	x9, x10, [x21]
0x47060	1f0100f1	cmp	x8, #0x0
0x47064	29b1959a	csel	x9, x9, x21, lt
0x47068	1f010071	cmp	w8, #0x0
0x4706c	48b1889a	csel	x8, x10, x8, lt
0x47070	a9233ba9	stp	x9, x8, [x29, #-0x50]
0x47074	f8630191	add	x24, sp, #0x58
0x47078	e0030091	mov	x0, sp
0x4707c	e1630191	add	x1, sp, #0x58
0x47080	e7440094	bl	0x5841c <_WeChatMain+0x3ebb0>
0x47084	e0030091	mov	x0, sp
0x47088	a14301d1	sub	x1, x29, #0x50
0x4708c	e4440094	bl	0x5841c <_WeChatMain+0x3ebb0>
0x47090	18230091	add	x24, x24, #0x8
0x47094	ff7f06a9	stp	xzr, xzr, [sp, #0x60]
0x47098	f82f00f9	str	x24, [sp, #0x58]
0x4709c	26010094	bl	0x47534 <_WeChatMain+0x2dcc8>
0x470a0	e3630191	add	x3, sp, #0x58
0x470a4	e10316aa	mov	x1, x22
0x470a8	e20315aa	mov	x2, x21
0x470ac	60010094	bl	0x4762c <_WeChatMain+0x2ddc0>
0x470b0	f62f40f9	ldr	x22, [sp, #0x58]
0x470b4	df0218eb	cmp	x22, x24
0x470b8	81070054	b.ne	0x471a8 <_WeChatMain+0x2d93c>
0x470bc	e13340f9	ldr	x1, [sp, #0x60]
0x470c0	e0630191	add	x0, sp, #0x58
0x470c4	fe73ff97	bl	0x240bc <_WeChatMain+0xa850>
0x470c8	591005f0	adrp	x25, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x470cc	284b4739	ldrb	w8, [x25, #0x1d2]
0x470d0	48010037	tbnz	w8, #0x0, 0x470f8 <_WeChatMain+0x2d88c>
0x470d4	481005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x470d8	08010791	add	x8, x8, #0x1c0
0x470dc	c92104f0	adrp	x9, 0x8482000 <_wxam_enc_uninit_10+0x8482000>
0x470e0	2051c23d	ldr	q0, [x9, #0x940]
0x470e4	0001803d	str	q0, [x8]
0x470e8	c90d8052	mov	w9, #0x6e               ; =110
0x470ec	09210079	strh	w9, [x8, #0x10]
0x470f0	28008052	mov	w8, #0x1                ; =1
0x470f4	284b0739	strb	w8, [x25, #0x1d2]
0x470f8	f7027db2	orr	x23, x23, #0x8
0x470fc	581005f0	adrp	x24, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x47100	08fb4839	ldrb	w8, [x24, #0x23e]
0x47104	e00314aa	mov	x0, x20
0x47108	a8030037	tbnz	w8, #0x0, 0x4717c <_WeChatMain+0x2d910>
0x4710c	080080d2	mov	x8, #0x0                ; =0
0x47110	e9e702b2	mov	x9, #-0x3333333333333334 ; =-3689348814741910324
0x47114	a99999f2	movk	x9, #0xcccd
0x47118	6a028092	mov	x10, #-0x14             ; =-20
0x4711c	0b2204d0	adrp	x11, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x47120	6b410c91	add	x11, x11, #0x310
0x47124	4085040f	movi.4h	v0, #0x8a
0x47128	4c1005f0	adrp	x12, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4712c	8c810791	add	x12, x12, #0x1e0
0x47130	0d7dc99b	umulh	x13, x8, x9
0x47134	adfd44d3	lsr	x13, x13, #4
0x47138	6e01088b	add	x14, x11, x8
0x4713c	ad390a9b	madd	x13, x13, x10, x14
0x47140	c1e942bd	ldr	s1, [x14, #0x2e8]
0x47144	0110212e	uaddw.8h	v1, v0, v1
0x47148	a2d542bd	ldr	s2, [x13, #0x2d4]
0x4714c	42a4082f	ushll.8h	v2, v2, #0x0
0x47150	211c222e	eor.8b	v1, v1, v2
0x47154	2118000e	uzp1.8b	v1, v1, v0
0x47158	816928bc	str	s1, [x12, x8]
0x4715c	08110091	add	x8, x8, #0x4
0x47160	1f7101f1	cmp	x8, #0x5c
0x47164	61feff54	b.ne	0x47130 <_WeChatMain+0x2d8c4>
0x47168	080d8052	mov	w8, #0x68               ; =104
0x4716c	491005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x47170	28790479	strh	w8, [x9, #0x23c]
0x47174	28008052	mov	w8, #0x1                ; =1
0x47178	08fb0839	strb	w8, [x24, #0x23e]
0x4717c	e80240f9	ldr	x8, [x23]
0x47180	c80500b4	cbz	x8, 0x47238 <_WeChatMain+0x2d9cc>
0x47184	e80b40f9	ldr	x8, [sp, #0x10]
0x47188	e90240f9	ldr	x9, [x23]
0x4718c	290140b9	ldr	w9, [x9]
0x47190	0801098b	add	x8, x8, x9
0x47194	01410091	add	x1, x8, #0x10
0x47198	29000014	b	0x4723c <_WeChatMain+0x2d9d0>
0x4719c	f60308aa	mov	x22, x8
0x471a0	1f0118eb	cmp	x8, x24
0x471a4	c0f8ff54	b.eq	0x470bc <_WeChatMain+0x2d850>
0x471a8	c8de8039	ldrsb	x8, [x22, #0x37]
0x471ac	e90316aa	mov	x9, x22
0x471b0	2a0d42f8	ldr	x10, [x9, #0x20]!
0x471b4	1f0100f1	cmp	x8, #0x0
0x471b8	49b1899a	csel	x9, x10, x9, lt
0x471bc	ca1640f9	ldr	x10, [x22, #0x28]
0x471c0	1f010071	cmp	w8, #0x0
0x471c4	48b1889a	csel	x8, x10, x8, lt
0x471c8	a9233ba9	stp	x9, x8, [x29, #-0x50]
0x471cc	f90316aa	mov	x25, x22
0x471d0	288f43f8	ldr	x8, [x25, #0x38]!
0x471d4	295f8039	ldrsb	x9, [x25, #0x17]
0x471d8	3f0100f1	cmp	x9, #0x0
0x471dc	08b1999a	csel	x8, x8, x25, lt
0x471e0	2a0740f9	ldr	x10, [x25, #0x8]
0x471e4	3f010071	cmp	w9, #0x0
0x471e8	49b1899a	csel	x9, x10, x9, lt
0x471ec	e8a704a9	stp	x8, x9, [sp, #0x48]
0x471f0	e0030091	mov	x0, sp
0x471f4	a14301d1	sub	x1, x29, #0x50
0x471f8	89440094	bl	0x5841c <_WeChatMain+0x3ebb0>
0x471fc	e0030091	mov	x0, sp
0x47200	e1230191	add	x1, sp, #0x48
0x47204	86440094	bl	0x5841c <_WeChatMain+0x3ebb0>
0x47208	29035df8	ldur	x9, [x25, #-0x30]
0x4720c	a90000b4	cbz	x9, 0x47220 <_WeChatMain+0x2d9b4>
0x47210	e80309aa	mov	x8, x9
0x47214	290140f9	ldr	x9, [x9]
0x47218	c9ffffb5	cbnz	x9, 0x47210 <_WeChatMain+0x2d9a4>
0x4721c	e0ffff17	b	0x4719c <_WeChatMain+0x2d930>
0x47220	c80a40f9	ldr	x8, [x22, #0x10]
0x47224	090140f9	ldr	x9, [x8]
0x47228	3f0116eb	cmp	x9, x22
0x4722c	f60308aa	mov	x22, x8
0x47230	81ffff54	b.ne	0x47220 <_WeChatMain+0x2d9b4>
0x47234	daffff17	b	0x4719c <_WeChatMain+0x2d930>
0x47238	01028052	mov	w1, #0x10               ; =16
0x4723c	c2c28f52	mov	w2, #0x7e16             ; =32278
0x47240	2274b572	movk	w2, #0xaba1, lsl #16
0x47244	aa1d0094	bl	0x4e8ec <_WeChatMain+0x35080>
0x47248	a0090034	cbz	w0, 0x4737c <_WeChatMain+0x2db10>
0x4724c	f60300aa	mov	x22, x0
0x47250	e00314aa	mov	x0, x20
0x47254	e10316aa	mov	x1, x22
0x47258	c2c28f52	mov	w2, #0x7e16             ; =32278
0x4725c	2274b572	movk	w2, #0xaba1, lsl #16
0x47260	03028052	mov	w3, #0x10               ; =16
0x47264	091e0094	bl	0x4ea88 <_WeChatMain+0x3521c>
0x47268	e8034139	ldrb	w8, [sp, #0x40]
0x4726c	080000b9	str	w8, [x0]
0x47270	284b4739	ldrb	w8, [x25, #0x1d2]
0x47274	28020036	tbz	w8, #0x0, 0x472b8 <_WeChatMain+0x2da4c>
0x47278	08fb4839	ldrb	w8, [x24, #0x23e]
0x4727c	48030036	tbz	w8, #0x0, 0x472e4 <_WeChatMain+0x2da78>
0x47280	e80240f9	ldr	x8, [x23]
0x47284	a80000b4	cbz	x8, 0x47298 <_WeChatMain+0x2da2c>
0x47288	e80b40f9	ldr	x8, [sp, #0x10]
0x4728c	e90240f9	ldr	x9, [x23]
0x47290	290140b9	ldr	w9, [x9]
0x47294	0801098b	add	x8, x8, x9
0x47298	080400f9	str	x8, [x0, #0x8]
0x4729c	e10240f9	ldr	x1, [x23]
0x472a0	010600b4	cbz	x1, 0x47360 <_WeChatMain+0x2daf4>
0x472a4	e80b40f9	ldr	x8, [sp, #0x10]
0x472a8	e90240f9	ldr	x9, [x23]
0x472ac	290140b9	ldr	w9, [x9]
0x472b0	0201098b	add	x2, x8, x9
0x472b4	2c000014	b	0x47364 <_WeChatMain+0x2daf8>
0x472b8	481005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x472bc	08010791	add	x8, x8, #0x1c0
0x472c0	c92104f0	adrp	x9, 0x8482000 <_wxam_enc_uninit_10+0x8482000>
0x472c4	2051c23d	ldr	q0, [x9, #0x940]
0x472c8	0001803d	str	q0, [x8]
0x472cc	c90d8052	mov	w9, #0x6e               ; =110
0x472d0	09210079	strh	w9, [x8, #0x10]
0x472d4	28008052	mov	w8, #0x1                ; =1
0x472d8	284b0739	strb	w8, [x25, #0x1d2]
0x472dc	08fb4839	ldrb	w8, [x24, #0x23e]
0x472e0	08fd0737	tbnz	w8, #0x0, 0x47280 <_WeChatMain+0x2da14>
0x472e4	080080d2	mov	x8, #0x0                ; =0
0x472e8	e9e702b2	mov	x9, #-0x3333333333333334 ; =-3689348814741910324
0x472ec	a99999f2	movk	x9, #0xcccd
0x472f0	6a028092	mov	x10, #-0x14             ; =-20
0x472f4	0b2204d0	adrp	x11, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x472f8	6b410c91	add	x11, x11, #0x310
0x472fc	4085040f	movi.4h	v0, #0x8a
0x47300	4c1005f0	adrp	x12, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x47304	8c810791	add	x12, x12, #0x1e0
0x47308	0d7dc99b	umulh	x13, x8, x9
0x4730c	adfd44d3	lsr	x13, x13, #4
0x47310	6e01088b	add	x14, x11, x8
0x47314	ad390a9b	madd	x13, x13, x10, x14
0x47318	c1e942bd	ldr	s1, [x14, #0x2e8]
0x4731c	0110212e	uaddw.8h	v1, v0, v1
0x47320	a2d542bd	ldr	s2, [x13, #0x2d4]
0x47324	42a4082f	ushll.8h	v2, v2, #0x0
0x47328	211c222e	eor.8b	v1, v1, v2
0x4732c	2118000e	uzp1.8b	v1, v1, v0
0x47330	816928bc	str	s1, [x12, x8]
0x47334	08110091	add	x8, x8, #0x4
0x47338	1f7101f1	cmp	x8, #0x5c
0x4733c	61feff54	b.ne	0x47308 <_WeChatMain+0x2da9c>
0x47340	080d8052	mov	w8, #0x68               ; =104
0x47344	491005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x47348	28790479	strh	w8, [x9, #0x23c]
0x4734c	28008052	mov	w8, #0x1                ; =1
0x47350	08fb0839	strb	w8, [x24, #0x23e]
0x47354	e80240f9	ldr	x8, [x23]
0x47358	88f9ffb5	cbnz	x8, 0x47288 <_WeChatMain+0x2da1c>
0x4735c	cfffff17	b	0x47298 <_WeChatMain+0x2da2c>
0x47360	020080d2	mov	x2, #0x0                ; =0
0x47364	00400091	add	x0, x0, #0x10
0x47368	c8e6c395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x4736c	e00314aa	mov	x0, x20
0x47370	e10316aa	mov	x1, x22
0x47374	ad1e0094	bl	0x4ee28 <_WeChatMain+0x355bc>
0x47378	767600b9	str	w22, [x19, #0x74]
0x4737c	e0030091	mov	x0, sp
0x47380	b0430094	bl	0x58240 <_WeChatMain+0x3e9d4>
0x47384	a8765e92	and	x8, x21, #0xfffffffc00000000
0x47388	93fd04f0	adrp	x19, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4738c	73023b91	add	x19, x19, #0xec0
0x47390	690640f9	ldr	x9, [x19, #0x8]
0x47394	1f0109eb	cmp	x8, x9
0x47398	61000054	b.ne	0x473a4 <_WeChatMain+0x2db38>
0x4739c	e00315aa	mov	x0, x21
0x473a0	c8e1ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x473a4	e01b40f9	ldr	x0, [sp, #0x30]
0x473a8	08745e92	and	x8, x0, #0xfffffffc00000000
0x473ac	690640f9	ldr	x9, [x19, #0x8]
0x473b0	1f0109eb	cmp	x8, x9
0x473b4	41000054	b.ne	0x473bc <_WeChatMain+0x2db50>
0x473b8	c2e1ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x473bc	fd7b4ca9	ldp	x29, x30, [sp, #0xc0]
0x473c0	f44f4ba9	ldp	x20, x19, [sp, #0xb0]
0x473c4	f6574aa9	ldp	x22, x21, [sp, #0xa0]
0x473c8	f85f49a9	ldp	x24, x23, [sp, #0x90]
0x473cc	fa6748a9	ldp	x26, x25, [sp, #0x80]
0x473d0	ff430391	add	sp, sp, #0xd0
0x473d4	c0035fd6	ret
0x473d8	481005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x473dc	09fd4639	ldrb	w9, [x8, #0x1bf]
0x473e0	69000037	tbnz	w9, #0x0, 0x473ec <_WeChatMain+0x2db80>
0x473e4	29008052	mov	w9, #0x1                ; =1
0x473e8	09fd0639	strb	w9, [x8, #0x1bf]
0x473ec	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x473f0	fd030091	mov	x29, sp
0x473f4	9fe3c395	bl	0x7140270 <_wxam_enc_uninit_10+0x7140270>
0x473f8	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x473fc	f65701a9	stp	x22, x21, [sp, #0x10]
0x47400	f44f02a9	stp	x20, x19, [sp, #0x20]
0x47404	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x47408	fdc30091	add	x29, sp, #0x30
0x4740c	f40302aa	mov	x20, x2
0x47410	f30300aa	mov	x19, x0
0x47414	090840f9	ldr	x9, [x0, #0x10]
0x47418	000040f9	ldr	x0, [x0]
0x4741c	280100cb	sub	x8, x9, x0
0x47420	7f0c88eb	cmp	x3, x8, asr #3
0x47424	89040054	b.ls	0x474b4 <_WeChatMain+0x2dc48>
0x47428	f70301aa	mov	x23, x1
0x4742c	200100b4	cbz	x0, 0x47450 <_WeChatMain+0x2dbe4>
0x47430	600600f9	str	x0, [x19, #0x8]
0x47434	e10308aa	mov	x1, x8
0x47438	f50303aa	mov	x21, x3
0x4743c	f4e2c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x47440	e30315aa	mov	x3, x21
0x47444	090080d2	mov	x9, #0x0                ; =0
0x47448	7f7e00a9	stp	xzr, xzr, [x19]
0x4744c	7f0a00f9	str	xzr, [x19, #0x10]
0x47450	68fc7dd3	lsr	x8, x3, #61
0x47454	c80600b5	cbnz	x8, 0x4752c <_WeChatMain+0x2dcc0>
0x47458	28fd4293	asr	x8, x9, #2
0x4745c	1f0103eb	cmp	x8, x3
0x47460	0881839a	csel	x8, x8, x3, hi
0x47464	eaef7db2	mov	x10, #0x7ffffffffffffff8 ; =9223372036854775800
0x47468	0b00fc92	mov	x11, #0x1fffffffffffffff ; =2305843009213693951
0x4746c	3f010aeb	cmp	x9, x10
0x47470	08318b9a	csel	x8, x8, x11, lo
0x47474	09fd7dd3	lsr	x9, x8, #61
0x47478	a90500b5	cbnz	x9, 0x4752c <_WeChatMain+0x2dcc0>
0x4747c	16f17dd3	lsl	x22, x8, #3
0x47480	e00316aa	mov	x0, x22
0x47484	ebe2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x47488	f50300aa	mov	x21, x0
0x4748c	600200a9	stp	x0, x0, [x19]
0x47490	0800168b	add	x8, x0, x22
0x47494	680a00f9	str	x8, [x19, #0x10]
0x47498	940217eb	subs	x20, x20, x23
0x4749c	a0020054	b.eq	0x474f0 <_WeChatMain+0x2dc84>
0x474a0	e10317aa	mov	x1, x23
0x474a4	e00315aa	mov	x0, x21
0x474a8	e20314aa	mov	x2, x20
0x474ac	77e6c395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x474b0	10000014	b	0x474f0 <_WeChatMain+0x2dc84>
0x474b4	750640f9	ldr	x21, [x19, #0x8]
0x474b8	a20200cb	sub	x2, x21, x0
0x474bc	7f0c82eb	cmp	x3, x2, asr #3
0x474c0	c9010054	b.ls	0x474f8 <_WeChatMain+0x2dc8c>
0x474c4	3600028b	add	x22, x1, x2
0x474c8	bf0200eb	cmp	x21, x0
0x474cc	60000054	b.eq	0x474d8 <_WeChatMain+0x2dc6c>
0x474d0	71e6c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x474d4	750640f9	ldr	x21, [x19, #0x8]
0x474d8	940216eb	subs	x20, x20, x22
0x474dc	a0000054	b.eq	0x474f0 <_WeChatMain+0x2dc84>
0x474e0	e00315aa	mov	x0, x21
0x474e4	e10316aa	mov	x1, x22
0x474e8	e20314aa	mov	x2, x20
0x474ec	6ae6c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x474f0	a802148b	add	x8, x21, x20
0x474f4	08000014	b	0x47514 <_WeChatMain+0x2dca8>
0x474f8	940201eb	subs	x20, x20, x1
0x474fc	a0000054	b.eq	0x47510 <_WeChatMain+0x2dca4>
0x47500	f50300aa	mov	x21, x0
0x47504	e20314aa	mov	x2, x20
0x47508	63e6c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4750c	e00315aa	mov	x0, x21
0x47510	0800148b	add	x8, x0, x20
0x47514	680600f9	str	x8, [x19, #0x8]
0x47518	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4751c	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x47520	f65741a9	ldp	x22, x21, [sp, #0x10]
0x47524	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x47528	c0035fd6	ret
0x4752c	e00313aa	mov	x0, x19
0x47530	aaffff97	bl	0x473d8 <_WeChatMain+0x2db6c>
0x47534	e8fd04f0	adrp	x8, 0xa006000 <_wxam_enc_uninit_10+0xa006000>
0x47538	08813f91	add	x8, x8, #0xfe0
0x4753c	00c1bff8	ldapr	x0, [x8]
0x47540	1f0400f1	cmp	x0, #0x1
0x47544	88030054	b.hi	0x475b4 <_WeChatMain+0x2dd48>
0x47548	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4754c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x47550	fd430091	add	x29, sp, #0x10
0x47554	f3fd04f0	adrp	x19, 0xa006000 <_wxam_enc_uninit_10+0xa006000>
0x47558	73823f91	add	x19, x19, #0xfe0
0x4755c	e00313aa	mov	x0, x19
0x47560	c9cfff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x47564	20020034	cbz	w0, 0x475a8 <_WeChatMain+0x2dd3c>
0x47568	000b8052	mov	w0, #0x58               ; =88
0x4756c	b1e2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x47570	f30300aa	mov	x19, x0
0x47574	9a8b0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x47578	1f2800f9	str	xzr, [x0, #0x50]
0x4757c	e80300aa	mov	x8, x0
0x47580	1f8d04f8	str	xzr, [x8, #0x48]!
0x47584	082000f9	str	x8, [x0, #0x40]
0x47588	e0fd04f0	adrp	x0, 0xa006000 <_wxam_enc_uninit_10+0xa006000>
0x4758c	00803f91	add	x0, x0, #0xfe0
0x47590	e10313aa	mov	x1, x19
0x47594	020080d2	mov	x2, #0x0                ; =0
0x47598	030080d2	mov	x3, #0x0                ; =0
0x4759c	decfff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x475a0	e00313aa	mov	x0, x19
0x475a4	02000014	b	0x475ac <_WeChatMain+0x2dd40>
0x475a8	60c2bff8	ldapr	x0, [x19]
0x475ac	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x475b0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x475b4	c0035fd6	ret
0x475b8	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x475bc	f44f01a9	stp	x20, x19, [sp, #0x10]
0x475c0	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x475c4	fd830091	add	x29, sp, #0x20
0x475c8	c10100b4	cbz	x1, 0x47600 <_WeChatMain+0x2dd94>
0x475cc	f30302aa	mov	x19, x2
0x475d0	f40301aa	mov	x20, x1
0x475d4	f50300aa	mov	x21, x0
0x475d8	e00301aa	mov	x0, x1
0x475dc	12feff97	bl	0x46e24 <_WeChatMain+0x2d5b8>
0x475e0	e20300aa	mov	x2, x0
0x475e4	81420091	add	x1, x20, #0x10
0x475e8	e00315aa	mov	x0, x21
0x475ec	e30313aa	mov	x3, x19
0x475f0	0f000094	bl	0x4762c <_WeChatMain+0x2ddc0>
0x475f4	00010036	tbz	w0, #0x0, 0x47614 <_WeChatMain+0x2dda8>
0x475f8	20008052	mov	w0, #0x1                ; =1
0x475fc	02000014	b	0x47604 <_WeChatMain+0x2dd98>
0x47600	00008052	mov	w0, #0x0                ; =0
0x47604	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x47608	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4760c	f657c3a8	ldp	x22, x21, [sp], #0x30
0x47610	c0035fd6	ret
0x47614	e00314aa	mov	x0, x20
0x47618	e10313aa	mov	x1, x19
0x4761c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x47620	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x47624	f657c3a8	ldp	x22, x21, [sp], #0x30
0x47628	38feff17	b	0x46f08 <_WeChatMain+0x2d69c>
0x4762c	ffc301d1	sub	sp, sp, #0x70
0x47630	f85f03a9	stp	x24, x23, [sp, #0x30]
0x47634	f65704a9	stp	x22, x21, [sp, #0x40]
0x47638	f44f05a9	stp	x20, x19, [sp, #0x50]
0x4763c	fd7b06a9	stp	x29, x30, [sp, #0x60]
0x47640	fd830191	add	x29, sp, #0x60
0x47644	f40303aa	mov	x20, x3
0x47648	f50302aa	mov	x21, x2
0x4764c	f60301aa	mov	x22, x1
0x47650	f30300aa	mov	x19, x0
0x47654	a8e7c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x47658	00010035	cbnz	w0, 0x47678 <_WeChatMain+0x2de0c>
0x4765c	c85ec039	ldrsb	w8, [x22, #0x17]
0x47660	4801f837	tbnz	w8, #0x1f, 0x47688 <_WeChatMain+0x2de1c>
0x47664	c002c03d	ldr	q0, [x22]
0x47668	e003803d	str	q0, [sp]
0x4766c	c80a40f9	ldr	x8, [x22, #0x10]
0x47670	e80b00f9	str	x8, [sp, #0x10]
0x47674	08000014	b	0x47694 <_WeChatMain+0x2de28>
0x47678	e00313aa	mov	x0, x19
0x4767c	828b0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x47680	c85ec039	ldrsb	w8, [x22, #0x17]
0x47684	08ffff36	tbz	w8, #0x1f, 0x47664 <_WeChatMain+0x2ddf8>
0x47688	c10a40a9	ldp	x1, x2, [x22]
0x4768c	e0030091	mov	x0, sp
0x47690	a445ff97	bl	0x18d20 <__text+0x1d20>
0x47694	e8030091	mov	x8, sp
0x47698	a95ec039	ldrsb	w9, [x21, #0x17]
0x4769c	c900f837	tbnz	w9, #0x1f, 0x476b4 <_WeChatMain+0x2de48>
0x476a0	a002c03d	ldr	q0, [x21]
0x476a4	0081813c	stur	q0, [x8, #0x18]
0x476a8	a90a40f9	ldr	x9, [x21, #0x10]
0x476ac	098102f8	stur	x9, [x8, #0x28]
0x476b0	04000014	b	0x476c0 <_WeChatMain+0x2de54>
0x476b4	a10a40a9	ldp	x1, x2, [x21]
0x476b8	00610091	add	x0, x8, #0x18
0x476bc	9945ff97	bl	0x18d20 <__text+0x1d20>
0x476c0	f50313aa	mov	x21, x19
0x476c4	b68e44f8	ldr	x22, [x21, #0x48]!
0x476c8	960300b4	cbz	x22, 0x47738 <_WeChatMain+0x2decc>
0x476cc	f70315aa	mov	x23, x21
0x476d0	c0820091	add	x0, x22, #0x20
0x476d4	e1030091	mov	x1, sp
0x476d8	39000094	bl	0x477bc <_WeChatMain+0x2df50>
0x476dc	081c0013	sxtb	w8, w0
0x476e0	097c0453	lsr	w9, w0, #4
0x476e4	29017d92	and	x9, x9, #0x8
0x476e8	1f010071	cmp	w8, #0x0
0x476ec	f7b2969a	csel	x23, x23, x22, lt
0x476f0	d66a69f8	ldr	x22, [x22, x9]
0x476f4	f6feffb5	cbnz	x22, 0x476d0 <_WeChatMain+0x2de64>
0x476f8	f60315aa	mov	x22, x21
0x476fc	ff0215eb	cmp	x23, x21
0x47700	e0000054	b.eq	0x4771c <_WeChatMain+0x2deb0>
0x47704	e0030091	mov	x0, sp
0x47708	e1820091	add	x1, x23, #0x20
0x4770c	2c000094	bl	0x477bc <_WeChatMain+0x2df50>
0x47710	081c0013	sxtb	w8, w0
0x47714	1f010071	cmp	w8, #0x0
0x47718	b6b2979a	csel	x22, x21, x23, lt
0x4771c	e8bfc039	ldrsb	w8, [sp, #0x2f]
0x47720	2801f837	tbnz	w8, #0x1f, 0x47744 <_WeChatMain+0x2ded8>
0x47724	e85fc039	ldrsb	w8, [sp, #0x17]
0x47728	a801f837	tbnz	w8, #0x1f, 0x4775c <_WeChatMain+0x2def0>
0x4772c	df0215eb	cmp	x22, x21
0x47730	21020054	b.ne	0x47774 <_WeChatMain+0x2df08>
0x47734	17000014	b	0x47790 <_WeChatMain+0x2df24>
0x47738	f60315aa	mov	x22, x21
0x4773c	e8bfc039	ldrsb	w8, [sp, #0x2f]
0x47740	28ffff36	tbz	w8, #0x1f, 0x47724 <_WeChatMain+0x2deb8>
0x47744	e00f40f9	ldr	x0, [sp, #0x18]
0x47748	e81740f9	ldr	x8, [sp, #0x28]
0x4774c	01f94092	and	x1, x8, #0x7fffffffffffffff
0x47750	2fe2c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x47754	e85fc039	ldrsb	w8, [sp, #0x17]
0x47758	a8feff36	tbz	w8, #0x1f, 0x4772c <_WeChatMain+0x2dec0>
0x4775c	e00340f9	ldr	x0, [sp]
0x47760	e80b40f9	ldr	x8, [sp, #0x10]
0x47764	01f94092	and	x1, x8, #0x7fffffffffffffff
0x47768	29e2c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4776c	df0215eb	cmp	x22, x21
0x47770	00010054	b.eq	0x47790 <_WeChatMain+0x2df24>
0x47774	c8420191	add	x8, x22, #0x50
0x47778	1f0114eb	cmp	x8, x20
0x4777c	a0000054	b.eq	0x47790 <_WeChatMain+0x2df24>
0x47780	c12a40f9	ldr	x1, [x22, #0x50]
0x47784	c2620191	add	x2, x22, #0x58
0x47788	e00314aa	mov	x0, x20
0x4778c	48000094	bl	0x478ac <_WeChatMain+0x2e040>
0x47790	df0215eb	cmp	x22, x21
0x47794	f4079f1a	cset	w20, ne
0x47798	e00313aa	mov	x0, x19
0x4779c	59e7c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x477a0	e00314aa	mov	x0, x20
0x477a4	fd7b46a9	ldp	x29, x30, [sp, #0x60]
0x477a8	f44f45a9	ldp	x20, x19, [sp, #0x50]
0x477ac	f65744a9	ldp	x22, x21, [sp, #0x40]
0x477b0	f85f43a9	ldp	x24, x23, [sp, #0x30]
0x477b4	ffc30191	add	sp, sp, #0x70
0x477b8	c0035fd6	ret
0x477bc	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x477c0	f44f01a9	stp	x20, x19, [sp, #0x10]
0x477c4	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x477c8	fd830091	add	x29, sp, #0x20
0x477cc	f30301aa	mov	x19, x1
0x477d0	f40300aa	mov	x20, x0
0x477d4	085c4039	ldrb	w8, [x0, #0x17]
0x477d8	091d0013	sxtb	w9, w8
0x477dc	0a2c40a9	ldp	x10, x11, [x0]
0x477e0	3f010071	cmp	w9, #0x0
0x477e4	40b1809a	csel	x0, x10, x0, lt
0x477e8	75b1889a	csel	x21, x11, x8, lt
0x477ec	285c4039	ldrb	w8, [x1, #0x17]
0x477f0	091d0013	sxtb	w9, w8
0x477f4	2a2c40a9	ldp	x10, x11, [x1]
0x477f8	3f010071	cmp	w9, #0x0
0x477fc	41b1819a	csel	x1, x10, x1, lt
0x47800	76b1889a	csel	x22, x11, x8, lt
0x47804	df0215eb	cmp	x22, x21
0x47808	c232959a	csel	x2, x22, x21, lo
0x4780c	9ce5c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x47810	a0000034	cbz	w0, 0x47824 <_WeChatMain+0x2dfb8>
0x47814	1f000071	cmp	w0, #0x0
0x47818	08008012	mov	w8, #-0x1               ; =-1
0x4781c	00b5885a	cneg	w0, w8, ge
0x47820	1f000014	b	0x4789c <_WeChatMain+0x2e030>
0x47824	bf0216eb	cmp	x21, x22
0x47828	61030054	b.ne	0x47894 <_WeChatMain+0x2e028>
0x4782c	888e41f8	ldr	x8, [x20, #0x18]!
0x47830	895e4039	ldrb	w9, [x20, #0x17]
0x47834	2a1d0013	sxtb	w10, w9
0x47838	8b0640f9	ldr	x11, [x20, #0x8]
0x4783c	5f010071	cmp	w10, #0x0
0x47840	00b1949a	csel	x0, x8, x20, lt
0x47844	74b1899a	csel	x20, x11, x9, lt
0x47848	688e41f8	ldr	x8, [x19, #0x18]!
0x4784c	695e4039	ldrb	w9, [x19, #0x17]
0x47850	2a1d0013	sxtb	w10, w9
0x47854	6b0640f9	ldr	x11, [x19, #0x8]
0x47858	5f010071	cmp	w10, #0x0
0x4785c	01b1939a	csel	x1, x8, x19, lt
0x47860	73b1899a	csel	x19, x11, x9, lt
0x47864	7f0214eb	cmp	x19, x20
0x47868	6232949a	csel	x2, x19, x20, lo
0x4786c	84e5c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x47870	1f000071	cmp	w0, #0x0
0x47874	08008012	mov	w8, #-0x1               ; =-1
0x47878	09b5885a	cneg	w9, w8, ge
0x4787c	9f0213eb	cmp	x20, x19
0x47880	0835885a	cneg	w8, w8, hs
0x47884	e803881a	csel	w8, wzr, w8, eq
0x47888	1f000071	cmp	w0, #0x0
0x4788c	2011881a	csel	w0, w9, w8, ne
0x47890	03000014	b	0x4789c <_WeChatMain+0x2e030>
0x47894	08008012	mov	w8, #-0x1               ; =-1
0x47898	0035885a	cneg	w0, w8, hs
0x4789c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x478a0	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x478a4	f657c3a8	ldp	x22, x21, [sp], #0x30
0x478a8	c0035fd6	ret
0x478ac	ff4301d1	sub	sp, sp, #0x50
0x478b0	f85f01a9	stp	x24, x23, [sp, #0x10]
0x478b4	f65702a9	stp	x22, x21, [sp, #0x20]
0x478b8	f44f03a9	stp	x20, x19, [sp, #0x30]
0x478bc	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x478c0	fd030191	add	x29, sp, #0x40
0x478c4	f30302aa	mov	x19, x2
0x478c8	f60301aa	mov	x22, x1
0x478cc	f40300aa	mov	x20, x0
0x478d0	080840f9	ldr	x8, [x0, #0x10]
0x478d4	280500b4	cbz	x8, 0x47978 <_WeChatMain+0x2e10c>
0x478d8	880240f9	ldr	x8, [x20]
0x478dc	e90314aa	mov	x9, x20
0x478e0	2a8d40f8	ldr	x10, [x9, #0x8]!
0x478e4	890200f9	str	x9, [x20]
0x478e8	5f0900f9	str	xzr, [x10, #0x10]
0x478ec	9f0a00f9	str	xzr, [x20, #0x10]
0x478f0	3f0100f9	str	xzr, [x9]
0x478f4	090540f9	ldr	x9, [x8, #0x8]
0x478f8	3f0100f1	cmp	x9, #0x0
0x478fc	1501899a	csel	x21, x8, x9, eq
0x47900	750300b4	cbz	x21, 0x4796c <_WeChatMain+0x2e100>
0x47904	b70a40f9	ldr	x23, [x21, #0x10]
0x47908	770100b4	cbz	x23, 0x47934 <_WeChatMain+0x2e0c8>
0x4790c	e80240f9	ldr	x8, [x23]
0x47910	1f0115eb	cmp	x8, x21
0x47914	800c0054	b.eq	0x47aa4 <_WeChatMain+0x2e238>
0x47918	ff0600f9	str	xzr, [x23, #0x8]
0x4791c	c80000b4	cbz	x8, 0x47934 <_WeChatMain+0x2e0c8>
0x47920	f70308aa	mov	x23, x8
0x47924	080140f9	ldr	x8, [x8]
0x47928	c8ffffb5	cbnz	x8, 0x47920 <_WeChatMain+0x2e0b4>
0x4792c	e80640f9	ldr	x8, [x23, #0x8]
0x47930	88ffffb5	cbnz	x8, 0x47920 <_WeChatMain+0x2e0b4>
0x47934	df0213eb	cmp	x22, x19
0x47938	41050054	b.ne	0x479e0 <_WeChatMain+0x2e174>
0x4793c	e00314aa	mov	x0, x20
0x47940	e10315aa	mov	x1, x21
0x47944	de71ff97	bl	0x240bc <_WeChatMain+0xa850>
0x47948	970100b4	cbz	x23, 0x47978 <_WeChatMain+0x2e10c>
0x4794c	e80a40f9	ldr	x8, [x23, #0x10]
0x47950	880000b4	cbz	x8, 0x47960 <_WeChatMain+0x2e0f4>
0x47954	f70308aa	mov	x23, x8
0x47958	080940f9	ldr	x8, [x8, #0x10]
0x4795c	c8ffffb5	cbnz	x8, 0x47954 <_WeChatMain+0x2e0e8>
0x47960	e00314aa	mov	x0, x20
0x47964	e10317aa	mov	x1, x23
0x47968	03000014	b	0x47974 <_WeChatMain+0x2e108>
0x4796c	e00314aa	mov	x0, x20
0x47970	e10315aa	mov	x1, x21
0x47974	d271ff97	bl	0x240bc <_WeChatMain+0xa850>
0x47978	df0213eb	cmp	x22, x19
0x4797c	41010054	b.ne	0x479a4 <_WeChatMain+0x2e138>
0x47980	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x47984	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x47988	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4798c	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x47990	ff430191	add	sp, sp, #0x50
0x47994	c0035fd6	ret
0x47998	f60308aa	mov	x22, x8
0x4799c	1f0113eb	cmp	x8, x19
0x479a0	00ffff54	b.eq	0x47980 <_WeChatMain+0x2e114>
0x479a4	c1820091	add	x1, x22, #0x20
0x479a8	e00314aa	mov	x0, x20
0x479ac	88000094	bl	0x47bcc <_WeChatMain+0x2e360>
0x479b0	c90640f9	ldr	x9, [x22, #0x8]
0x479b4	a90000b4	cbz	x9, 0x479c8 <_WeChatMain+0x2e15c>
0x479b8	e80309aa	mov	x8, x9
0x479bc	290140f9	ldr	x9, [x9]
0x479c0	c9ffffb5	cbnz	x9, 0x479b8 <_WeChatMain+0x2e14c>
0x479c4	f5ffff17	b	0x47998 <_WeChatMain+0x2e12c>
0x479c8	c80a40f9	ldr	x8, [x22, #0x10]
0x479cc	090140f9	ldr	x9, [x8]
0x479d0	3f0116eb	cmp	x9, x22
0x479d4	f60308aa	mov	x22, x8
0x479d8	81ffff54	b.ne	0x479c8 <_WeChatMain+0x2e15c>
0x479dc	efffff17	b	0x47998 <_WeChatMain+0x2e12c>
0x479e0	f80316aa	mov	x24, x22
0x479e4	f60315aa	mov	x22, x21
0x479e8	f50317aa	mov	x21, x23
0x479ec	c8820091	add	x8, x22, #0x20
0x479f0	c9e20091	add	x9, x22, #0x38
0x479f4	e82700a9	stp	x8, x9, [sp]
0x479f8	e0030091	mov	x0, sp
0x479fc	01830091	add	x1, x24, #0x20
0x47a00	3672ff97	bl	0x242d8 <_WeChatMain+0xaa6c>
0x47a04	e00314aa	mov	x0, x20
0x47a08	e10316aa	mov	x1, x22
0x47a0c	2d000094	bl	0x47ac0 <_WeChatMain+0x2e254>
0x47a10	370200b5	cbnz	x23, 0x47a54 <_WeChatMain+0x2e1e8>
0x47a14	080740f9	ldr	x8, [x24, #0x8]
0x47a18	a80000b4	cbz	x8, 0x47a2c <_WeChatMain+0x2e1c0>
0x47a1c	f60308aa	mov	x22, x8
0x47a20	080140f9	ldr	x8, [x8]
0x47a24	c8ffffb5	cbnz	x8, 0x47a1c <_WeChatMain+0x2e1b0>
0x47a28	06000014	b	0x47a40 <_WeChatMain+0x2e1d4>
0x47a2c	160b40f9	ldr	x22, [x24, #0x10]
0x47a30	c80240f9	ldr	x8, [x22]
0x47a34	1f0118eb	cmp	x8, x24
0x47a38	f80316aa	mov	x24, x22
0x47a3c	81ffff54	b.ne	0x47a2c <_WeChatMain+0x2e1c0>
0x47a40	f5f7ffb4	cbz	x21, 0x4793c <_WeChatMain+0x2e0d0>
0x47a44	f80316aa	mov	x24, x22
0x47a48	df0213eb	cmp	x22, x19
0x47a4c	c1fcff54	b.ne	0x479e4 <_WeChatMain+0x2e178>
0x47a50	bbffff17	b	0x4793c <_WeChatMain+0x2e0d0>
0x47a54	b70a40f9	ldr	x23, [x21, #0x10]
0x47a58	f7fdffb4	cbz	x23, 0x47a14 <_WeChatMain+0x2e1a8>
0x47a5c	e80240f9	ldr	x8, [x23]
0x47a60	1f0115eb	cmp	x8, x21
0x47a64	20010054	b.eq	0x47a88 <_WeChatMain+0x2e21c>
0x47a68	ff0600f9	str	xzr, [x23, #0x8]
0x47a6c	48fdffb4	cbz	x8, 0x47a14 <_WeChatMain+0x2e1a8>
0x47a70	f70308aa	mov	x23, x8
0x47a74	080140f9	ldr	x8, [x8]
0x47a78	c8ffffb5	cbnz	x8, 0x47a70 <_WeChatMain+0x2e204>
0x47a7c	e80640f9	ldr	x8, [x23, #0x8]
0x47a80	88ffffb5	cbnz	x8, 0x47a70 <_WeChatMain+0x2e204>
0x47a84	e4ffff17	b	0x47a14 <_WeChatMain+0x2e1a8>
0x47a88	ff0200f9	str	xzr, [x23]
0x47a8c	e80640f9	ldr	x8, [x23, #0x8]
0x47a90	28fcffb4	cbz	x8, 0x47a14 <_WeChatMain+0x2e1a8>
0x47a94	f70308aa	mov	x23, x8
0x47a98	080140f9	ldr	x8, [x8]
0x47a9c	c8ffffb5	cbnz	x8, 0x47a94 <_WeChatMain+0x2e228>
0x47aa0	fbffff17	b	0x47a8c <_WeChatMain+0x2e220>
0x47aa4	ff0200f9	str	xzr, [x23]
0x47aa8	e80640f9	ldr	x8, [x23, #0x8]
0x47aac	48f4ffb4	cbz	x8, 0x47934 <_WeChatMain+0x2e0c8>
0x47ab0	f70308aa	mov	x23, x8
0x47ab4	080140f9	ldr	x8, [x8]
0x47ab8	c8ffffb5	cbnz	x8, 0x47ab0 <_WeChatMain+0x2e244>
0x47abc	fbffff17	b	0x47aa8 <_WeChatMain+0x2e23c>
0x47ac0	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x47ac4	f65701a9	stp	x22, x21, [sp, #0x10]
0x47ac8	f44f02a9	stp	x20, x19, [sp, #0x20]
0x47acc	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x47ad0	fdc30091	add	x29, sp, #0x30
0x47ad4	f30301aa	mov	x19, x1
0x47ad8	f40300aa	mov	x20, x0
0x47adc	f60300aa	mov	x22, x0
0x47ae0	c88e40f8	ldr	x8, [x22, #0x8]!
0x47ae4	680400b4	cbz	x8, 0x47b70 <_WeChatMain+0x2e304>
0x47ae8	e90313aa	mov	x9, x19
0x47aec	2a0d42f8	ldr	x10, [x9, #0x20]!
0x47af0	2b5d4039	ldrb	w11, [x9, #0x17]
0x47af4	6c1d0013	sxtb	w12, w11
0x47af8	2d0540f9	ldr	x13, [x9, #0x8]
0x47afc	9f010071	cmp	w12, #0x0
0x47b00	55b1899a	csel	x21, x10, x9, lt
0x47b04	b7b18b9a	csel	x23, x13, x11, lt
0x47b08	03000014	b	0x47b14 <_WeChatMain+0x2e2a8>
0x47b0c	c80640f9	ldr	x8, [x22, #0x8]
0x47b10	480300b4	cbz	x8, 0x47b78 <_WeChatMain+0x2e30c>
0x47b14	f60308aa	mov	x22, x8
0x47b18	090d42f8	ldr	x9, [x8, #0x20]!
0x47b1c	0a5d4039	ldrb	w10, [x8, #0x17]
0x47b20	4b1d0013	sxtb	w11, w10
0x47b24	0c0540f9	ldr	x12, [x8, #0x8]
0x47b28	7f010071	cmp	w11, #0x0
0x47b2c	21b1889a	csel	x1, x9, x8, lt
0x47b30	98b18a9a	csel	x24, x12, x10, lt
0x47b34	1f0317eb	cmp	x24, x23
0x47b38	0233979a	csel	x2, x24, x23, lo
0x47b3c	e00315aa	mov	x0, x21
0x47b40	cfe4c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x47b44	ff0218eb	cmp	x23, x24
0x47b48	e8279f1a	cset	w8, lo
0x47b4c	1f000071	cmp	w0, #0x0
0x47b50	e9a79f1a	cset	w9, lt
0x47b54	0801891a	csel	w8, w8, w9, eq
0x47b58	1f050071	cmp	w8, #0x1
0x47b5c	81fdff54	b.ne	0x47b0c <_WeChatMain+0x2e2a0>
0x47b60	c80240f9	ldr	x8, [x22]
0x47b64	e90316aa	mov	x9, x22
0x47b68	68fdffb5	cbnz	x8, 0x47b14 <_WeChatMain+0x2e2a8>
0x47b6c	04000014	b	0x47b7c <_WeChatMain+0x2e310>
0x47b70	e90316aa	mov	x9, x22
0x47b74	02000014	b	0x47b7c <_WeChatMain+0x2e310>
0x47b78	c9220091	add	x9, x22, #0x8
0x47b7c	7f7e00a9	stp	xzr, xzr, [x19]
0x47b80	760a00f9	str	x22, [x19, #0x10]
0x47b84	330100f9	str	x19, [x9]
0x47b88	880240f9	ldr	x8, [x20]
0x47b8c	080140f9	ldr	x8, [x8]
0x47b90	e10313aa	mov	x1, x19
0x47b94	680000b4	cbz	x8, 0x47ba0 <_WeChatMain+0x2e334>
0x47b98	880200f9	str	x8, [x20]
0x47b9c	210140f9	ldr	x1, [x9]
0x47ba0	800640f9	ldr	x0, [x20, #0x8]
0x47ba4	6671ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x47ba8	880a40f9	ldr	x8, [x20, #0x10]
0x47bac	08050091	add	x8, x8, #0x1
0x47bb0	880a00f9	str	x8, [x20, #0x10]
0x47bb4	e00313aa	mov	x0, x19
0x47bb8	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x47bbc	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x47bc0	f65741a9	ldp	x22, x21, [sp, #0x10]
0x47bc4	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x47bc8	c0035fd6	ret
0x47bcc	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x47bd0	f65701a9	stp	x22, x21, [sp, #0x10]
0x47bd4	f44f02a9	stp	x20, x19, [sp, #0x20]
0x47bd8	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x47bdc	fdc30091	add	x29, sp, #0x30
0x47be0	f60301aa	mov	x22, x1
0x47be4	f30300aa	mov	x19, x0
0x47be8	000a8052	mov	w0, #0x50               ; =80
0x47bec	11e1c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x47bf0	f40300aa	mov	x20, x0
0x47bf4	15800091	add	x21, x0, #0x20
0x47bf8	c85ec039	ldrsb	w8, [x22, #0x17]
0x47bfc	8801f837	tbnz	w8, #0x1f, 0x47c2c <_WeChatMain+0x2e3c0>
0x47c00	c002c03d	ldr	q0, [x22]
0x47c04	a002803d	str	q0, [x21]
0x47c08	c80a40f9	ldr	x8, [x22, #0x10]
0x47c0c	a80a00f9	str	x8, [x21, #0x10]
0x47c10	c8bec039	ldrsb	w8, [x22, #0x2f]
0x47c14	6801f837	tbnz	w8, #0x1f, 0x47c40 <_WeChatMain+0x2e3d4>
0x47c18	c082c13c	ldur	q0, [x22, #0x18]
0x47c1c	8082833c	stur	q0, [x20, #0x38]
0x47c20	c88242f8	ldur	x8, [x22, #0x28]
0x47c24	888204f8	stur	x8, [x20, #0x48]
0x47c28	09000014	b	0x47c4c <_WeChatMain+0x2e3e0>
0x47c2c	c10a40a9	ldp	x1, x2, [x22]
0x47c30	e00315aa	mov	x0, x21
0x47c34	3b44ff97	bl	0x18d20 <__text+0x1d20>
0x47c38	c8bec039	ldrsb	w8, [x22, #0x2f]
0x47c3c	e8feff36	tbz	w8, #0x1f, 0x47c18 <_WeChatMain+0x2e3ac>
0x47c40	c18a41a9	ldp	x1, x2, [x22, #0x18]
0x47c44	80e20091	add	x0, x20, #0x38
0x47c48	3644ff97	bl	0x18d20 <__text+0x1d20>
0x47c4c	f60313aa	mov	x22, x19
0x47c50	c88e40f8	ldr	x8, [x22, #0x8]!
0x47c54	280400b4	cbz	x8, 0x47cd8 <_WeChatMain+0x2e46c>
0x47c58	89de4039	ldrb	w9, [x20, #0x37]
0x47c5c	2a1d0013	sxtb	w10, w9
0x47c60	8b3242a9	ldp	x11, x12, [x20, #0x20]
0x47c64	5f010071	cmp	w10, #0x0
0x47c68	75b1959a	csel	x21, x11, x21, lt
0x47c6c	97b1899a	csel	x23, x12, x9, lt
0x47c70	03000014	b	0x47c7c <_WeChatMain+0x2e410>
0x47c74	c80640f9	ldr	x8, [x22, #0x8]
0x47c78	480300b4	cbz	x8, 0x47ce0 <_WeChatMain+0x2e474>
0x47c7c	f60308aa	mov	x22, x8
0x47c80	090d42f8	ldr	x9, [x8, #0x20]!
0x47c84	0a5d4039	ldrb	w10, [x8, #0x17]
0x47c88	4b1d0013	sxtb	w11, w10
0x47c8c	0c0540f9	ldr	x12, [x8, #0x8]
0x47c90	7f010071	cmp	w11, #0x0
0x47c94	21b1889a	csel	x1, x9, x8, lt
0x47c98	98b18a9a	csel	x24, x12, x10, lt
0x47c9c	1f0317eb	cmp	x24, x23
0x47ca0	0233979a	csel	x2, x24, x23, lo
0x47ca4	e00315aa	mov	x0, x21
0x47ca8	75e4c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x47cac	ff0218eb	cmp	x23, x24
0x47cb0	e8279f1a	cset	w8, lo
0x47cb4	1f000071	cmp	w0, #0x0
0x47cb8	e9a79f1a	cset	w9, lt
0x47cbc	0801891a	csel	w8, w8, w9, eq
0x47cc0	1f050071	cmp	w8, #0x1
0x47cc4	81fdff54	b.ne	0x47c74 <_WeChatMain+0x2e408>
0x47cc8	c80240f9	ldr	x8, [x22]
0x47ccc	e90316aa	mov	x9, x22
0x47cd0	68fdffb5	cbnz	x8, 0x47c7c <_WeChatMain+0x2e410>
0x47cd4	04000014	b	0x47ce4 <_WeChatMain+0x2e478>
0x47cd8	e90316aa	mov	x9, x22
0x47cdc	02000014	b	0x47ce4 <_WeChatMain+0x2e478>
0x47ce0	c9220091	add	x9, x22, #0x8
0x47ce4	9f7e00a9	stp	xzr, xzr, [x20]
0x47ce8	960a00f9	str	x22, [x20, #0x10]
0x47cec	340100f9	str	x20, [x9]
0x47cf0	680240f9	ldr	x8, [x19]
0x47cf4	080140f9	ldr	x8, [x8]
0x47cf8	e10314aa	mov	x1, x20
0x47cfc	680000b4	cbz	x8, 0x47d08 <_WeChatMain+0x2e49c>
0x47d00	680200f9	str	x8, [x19]
0x47d04	210140f9	ldr	x1, [x9]
0x47d08	600640f9	ldr	x0, [x19, #0x8]
0x47d0c	0c71ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x47d10	680a40f9	ldr	x8, [x19, #0x10]
0x47d14	08050091	add	x8, x8, #0x1
0x47d18	680a00f9	str	x8, [x19, #0x10]
0x47d1c	e00314aa	mov	x0, x20
0x47d20	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x47d24	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x47d28	f65741a9	ldp	x22, x21, [sp, #0x10]
0x47d2c	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x47d30	c0035fd6	ret
0x47d34	ff4301d1	sub	sp, sp, #0x50
0x47d38	f65702a9	stp	x22, x21, [sp, #0x20]
0x47d3c	f44f03a9	stp	x20, x19, [sp, #0x30]
0x47d40	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x47d44	fd030191	add	x29, sp, #0x40
0x47d48	f40301aa	mov	x20, x1
0x47d4c	f50300aa	mov	x21, x0
0x47d50	f30308aa	mov	x19, x8
0x47d54	e8230091	add	x8, sp, #0x8
0x47d58	ff7f01a9	stp	xzr, xzr, [sp, #0x10]
0x47d5c	16210091	add	x22, x8, #0x8
0x47d60	f60700f9	str	x22, [sp, #0x8]
0x47d64	e182ff97	bl	0x288e8 <_WeChatMain+0xf07c>
0x47d68	a0020034	cbz	w0, 0x47dbc <_WeChatMain+0x2e550>
0x47d6c	e00315aa	mov	x0, x21
0x47d70	f782ff97	bl	0x2894c <_WeChatMain+0xf0e0>
0x47d74	f50300aa	mov	x21, x0
0x47d78	effdff97	bl	0x47534 <_WeChatMain+0x2dcc8>
0x47d7c	e2230091	add	x2, sp, #0x8
0x47d80	e10315aa	mov	x1, x21
0x47d84	0dfeff97	bl	0x475b8 <_WeChatMain+0x2dd4c>
0x47d88	a0010034	cbz	w0, 0x47dbc <_WeChatMain+0x2e550>
0x47d8c	e0230091	add	x0, sp, #0x8
0x47d90	e10314aa	mov	x1, x20
0x47d94	ed000094	bl	0x48148 <_WeChatMain+0x2e8dc>
0x47d98	df0200eb	cmp	x22, x0
0x47d9c	00010054	b.eq	0x47dbc <_WeChatMain+0x2e550>
0x47da0	083cc139	ldrsb	w8, [x0, #0x4f]
0x47da4	0802f837	tbnz	w8, #0x1f, 0x47de4 <_WeChatMain+0x2e578>
0x47da8	0080c33c	ldur	q0, [x0, #0x38]
0x47dac	088044f8	ldur	x8, [x0, #0x48]
0x47db0	680a00f9	str	x8, [x19, #0x10]
0x47db4	6002803d	str	q0, [x19]
0x47db8	03000014	b	0x47dc4 <_WeChatMain+0x2e558>
0x47dbc	7f7e00a9	stp	xzr, xzr, [x19]
0x47dc0	7f0a00f9	str	xzr, [x19, #0x10]
0x47dc4	e10b40f9	ldr	x1, [sp, #0x10]
0x47dc8	e0230091	add	x0, sp, #0x8
0x47dcc	bc70ff97	bl	0x240bc <_WeChatMain+0xa850>
0x47dd0	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x47dd4	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x47dd8	f65742a9	ldp	x22, x21, [sp, #0x20]
0x47ddc	ff430191	add	sp, sp, #0x50
0x47de0	c0035fd6	ret
0x47de4	018843a9	ldp	x1, x2, [x0, #0x38]
0x47de8	e00313aa	mov	x0, x19
0x47dec	cd43ff97	bl	0x18d20 <__text+0x1d20>
0x47df0	f5ffff17	b	0x47dc4 <_WeChatMain+0x2e558>
0x47df4	ff4301d1	sub	sp, sp, #0x50
0x47df8	f65702a9	stp	x22, x21, [sp, #0x20]
0x47dfc	f44f03a9	stp	x20, x19, [sp, #0x30]
0x47e00	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x47e04	fd030191	add	x29, sp, #0x40
0x47e08	f30302aa	mov	x19, x2
0x47e0c	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x47e10	e82301a9	stp	x8, x8, [sp, #0x10]
0x47e14	e80700f9	str	x8, [sp, #0x8]
0x47e18	f4230091	add	x20, sp, #0x8
0x47e1c	e8230091	add	x8, sp, #0x8
0x47e20	c5ffff97	bl	0x47d34 <_WeChatMain+0x2e4c8>
0x47e24	ff0700b9	str	wzr, [sp, #0x4]
0x47e28	e87f8039	ldrsb	x8, [sp, #0x1f]
0x47e2c	e9ab40a9	ldp	x9, x10, [sp, #0x8]
0x47e30	1f0100f1	cmp	x8, #0x0
0x47e34	20b1949a	csel	x0, x9, x20, lt
0x47e38	1f010071	cmp	w8, #0x0
0x47e3c	41b1889a	csel	x1, x10, x8, lt
0x47e40	e2130091	add	x2, sp, #0x4
0x47e44	ad690094	bl	0x624f8 <_WeChatMain+0x48c8c>
0x47e48	f40300aa	mov	x20, x0
0x47e4c	f50740b9	ldr	w21, [sp, #0x4]
0x47e50	e87fc039	ldrsb	w8, [sp, #0x1f]
0x47e54	a800f836	tbz	w8, #0x1f, 0x47e68 <_WeChatMain+0x2e5fc>
0x47e58	e00740f9	ldr	x0, [sp, #0x8]
0x47e5c	e80f40f9	ldr	x8, [sp, #0x18]
0x47e60	01f94092	and	x1, x8, #0x7fffffffffffffff
0x47e64	6ae0c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x47e68	9f020071	cmp	w20, #0x0
0x47e6c	a012931a	csel	w0, w21, w19, ne
0x47e70	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x47e74	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x47e78	f65742a9	ldp	x22, x21, [sp, #0x20]
0x47e7c	ff430191	add	sp, sp, #0x50
0x47e80	c0035fd6	ret
0x47e84	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x47e88	f65701a9	stp	x22, x21, [sp, #0x10]
0x47e8c	f44f02a9	stp	x20, x19, [sp, #0x20]
0x47e90	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x47e94	fdc30091	add	x29, sp, #0x30
0x47e98	f40302aa	mov	x20, x2
0x47e9c	f30300aa	mov	x19, x0
0x47ea0	f60300aa	mov	x22, x0
0x47ea4	c88e40f8	ldr	x8, [x22, #0x8]!
0x47ea8	680200b4	cbz	x8, 0x47ef4 <_WeChatMain+0x2e688>
0x47eac	f50301aa	mov	x21, x1
0x47eb0	04000014	b	0x47ec0 <_WeChatMain+0x2e654>
0x47eb4	e80240f9	ldr	x8, [x23]
0x47eb8	f60317aa	mov	x22, x23
0x47ebc	e80100b4	cbz	x8, 0x47ef8 <_WeChatMain+0x2e68c>
0x47ec0	f70308aa	mov	x23, x8
0x47ec4	01810091	add	x1, x8, #0x20
0x47ec8	e00315aa	mov	x0, x21
0x47ecc	3cfeff97	bl	0x477bc <_WeChatMain+0x2df50>
0x47ed0	20ff3f37	tbnz	w0, #0x7, 0x47eb4 <_WeChatMain+0x2e648>
0x47ed4	e0820091	add	x0, x23, #0x20
0x47ed8	e10315aa	mov	x1, x21
0x47edc	38feff97	bl	0x477bc <_WeChatMain+0x2df50>
0x47ee0	60063836	tbz	w0, #0x7, 0x47fac <_WeChatMain+0x2e740>
0x47ee4	f60317aa	mov	x22, x23
0x47ee8	c88e40f8	ldr	x8, [x22, #0x8]!
0x47eec	a8feffb5	cbnz	x8, 0x47ec0 <_WeChatMain+0x2e654>
0x47ef0	02000014	b	0x47ef8 <_WeChatMain+0x2e68c>
0x47ef4	f70316aa	mov	x23, x22
0x47ef8	000a8052	mov	w0, #0x50               ; =80
0x47efc	4de0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x47f00	f50300aa	mov	x21, x0
0x47f04	885ec039	ldrsb	w8, [x20, #0x17]
0x47f08	8801f837	tbnz	w8, #0x1f, 0x47f38 <_WeChatMain+0x2e6cc>
0x47f0c	8002c03d	ldr	q0, [x20]
0x47f10	a002823c	stur	q0, [x21, #0x20]
0x47f14	880a40f9	ldr	x8, [x20, #0x10]
0x47f18	a80203f8	stur	x8, [x21, #0x30]
0x47f1c	88bec039	ldrsb	w8, [x20, #0x2f]
0x47f20	6801f837	tbnz	w8, #0x1f, 0x47f4c <_WeChatMain+0x2e6e0>
0x47f24	8082c13c	ldur	q0, [x20, #0x18]
0x47f28	a082833c	stur	q0, [x21, #0x38]
0x47f2c	888242f8	ldur	x8, [x20, #0x28]
0x47f30	a88204f8	stur	x8, [x21, #0x48]
0x47f34	09000014	b	0x47f58 <_WeChatMain+0x2e6ec>
0x47f38	810a40a9	ldp	x1, x2, [x20]
0x47f3c	a0820091	add	x0, x21, #0x20
0x47f40	7843ff97	bl	0x18d20 <__text+0x1d20>
0x47f44	88bec039	ldrsb	w8, [x20, #0x2f]
0x47f48	e8feff36	tbz	w8, #0x1f, 0x47f24 <_WeChatMain+0x2e6b8>
0x47f4c	818a41a9	ldp	x1, x2, [x20, #0x18]
0x47f50	a0e20091	add	x0, x21, #0x38
0x47f54	7343ff97	bl	0x18d20 <__text+0x1d20>
0x47f58	bf7e00a9	stp	xzr, xzr, [x21]
0x47f5c	b70a00f9	str	x23, [x21, #0x10]
0x47f60	d50200f9	str	x21, [x22]
0x47f64	680240f9	ldr	x8, [x19]
0x47f68	080140f9	ldr	x8, [x8]
0x47f6c	e10315aa	mov	x1, x21
0x47f70	680000b4	cbz	x8, 0x47f7c <_WeChatMain+0x2e710>
0x47f74	680200f9	str	x8, [x19]
0x47f78	c10240f9	ldr	x1, [x22]
0x47f7c	600640f9	ldr	x0, [x19, #0x8]
0x47f80	6f70ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x47f84	680a40f9	ldr	x8, [x19, #0x10]
0x47f88	08050091	add	x8, x8, #0x1
0x47f8c	680a00f9	str	x8, [x19, #0x10]
0x47f90	21008052	mov	w1, #0x1                ; =1
0x47f94	e00315aa	mov	x0, x21
0x47f98	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x47f9c	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x47fa0	f65741a9	ldp	x22, x21, [sp, #0x10]
0x47fa4	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x47fa8	c0035fd6	ret
0x47fac	d50240f9	ldr	x21, [x22]
0x47fb0	55faffb4	cbz	x21, 0x47ef8 <_WeChatMain+0x2e68c>
0x47fb4	010080d2	mov	x1, #0x0                ; =0
0x47fb8	f7ffff17	b	0x47f94 <_WeChatMain+0x2e728>
0x47fbc	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x47fc0	f85f01a9	stp	x24, x23, [sp, #0x10]
0x47fc4	f65702a9	stp	x22, x21, [sp, #0x20]
0x47fc8	f44f03a9	stp	x20, x19, [sp, #0x30]
0x47fcc	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x47fd0	fd030191	add	x29, sp, #0x40
0x47fd4	f40303aa	mov	x20, x3
0x47fd8	f30300aa	mov	x19, x0
0x47fdc	f60300aa	mov	x22, x0
0x47fe0	c88e40f8	ldr	x8, [x22, #0x8]!
0x47fe4	e80500b4	cbz	x8, 0x480a0 <_WeChatMain+0x2e834>
0x47fe8	295c4039	ldrb	w9, [x1, #0x17]
0x47fec	2a1d0013	sxtb	w10, w9
0x47ff0	2b3040a9	ldp	x11, x12, [x1]
0x47ff4	5f010071	cmp	w10, #0x0
0x47ff8	75b1819a	csel	x21, x11, x1, lt
0x47ffc	99b1899a	csel	x25, x12, x9, lt
0x48000	04000014	b	0x48010 <_WeChatMain+0x2e7a4>
0x48004	080340f9	ldr	x8, [x24]
0x48008	f60318aa	mov	x22, x24
0x4800c	c80400b4	cbz	x8, 0x480a4 <_WeChatMain+0x2e838>
0x48010	f80308aa	mov	x24, x8
0x48014	090d42f8	ldr	x9, [x8, #0x20]!
0x48018	0a5d4039	ldrb	w10, [x8, #0x17]
0x4801c	4b1d0013	sxtb	w11, w10
0x48020	0c0540f9	ldr	x12, [x8, #0x8]
0x48024	7f010071	cmp	w11, #0x0
0x48028	36b1889a	csel	x22, x9, x8, lt
0x4802c	9ab18a9a	csel	x26, x12, x10, lt
0x48030	5f0319eb	cmp	x26, x25
0x48034	5733999a	csel	x23, x26, x25, lo
0x48038	e00315aa	mov	x0, x21
0x4803c	e10316aa	mov	x1, x22
0x48040	e20317aa	mov	x2, x23
0x48044	8ee3c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x48048	3f031aeb	cmp	x25, x26
0x4804c	e8279f1a	cset	w8, lo
0x48050	1f000071	cmp	w0, #0x0
0x48054	e9a79f1a	cset	w9, lt
0x48058	0801891a	csel	w8, w8, w9, eq
0x4805c	1f050071	cmp	w8, #0x1
0x48060	20fdff54	b.eq	0x48004 <_WeChatMain+0x2e798>
0x48064	e00316aa	mov	x0, x22
0x48068	e10315aa	mov	x1, x21
0x4806c	e20317aa	mov	x2, x23
0x48070	83e3c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x48074	5f0319eb	cmp	x26, x25
0x48078	e8279f1a	cset	w8, lo
0x4807c	1f000071	cmp	w0, #0x0
0x48080	e9a79f1a	cset	w9, lt
0x48084	0801891a	csel	w8, w8, w9, eq
0x48088	1f050071	cmp	w8, #0x1
0x4808c	c1040054	b.ne	0x48124 <_WeChatMain+0x2e8b8>
0x48090	080740f9	ldr	x8, [x24, #0x8]
0x48094	e8fbffb5	cbnz	x8, 0x48010 <_WeChatMain+0x2e7a4>
0x48098	16230091	add	x22, x24, #0x8
0x4809c	02000014	b	0x480a4 <_WeChatMain+0x2e838>
0x480a0	f80316aa	mov	x24, x22
0x480a4	000a8052	mov	w0, #0x50               ; =80
0x480a8	e2dfc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x480ac	f50300aa	mov	x21, x0
0x480b0	880240f9	ldr	x8, [x20]
0x480b4	095dc039	ldrsb	w9, [x8, #0x17]
0x480b8	c900f837	tbnz	w9, #0x1f, 0x480d0 <_WeChatMain+0x2e864>
0x480bc	0001c03d	ldr	q0, [x8]
0x480c0	080940f9	ldr	x8, [x8, #0x10]
0x480c4	a80203f8	stur	x8, [x21, #0x30]
0x480c8	a002823c	stur	q0, [x21, #0x20]
0x480cc	04000014	b	0x480dc <_WeChatMain+0x2e870>
0x480d0	010940a9	ldp	x1, x2, [x8]
0x480d4	a0820091	add	x0, x21, #0x20
0x480d8	1243ff97	bl	0x18d20 <__text+0x1d20>
0x480dc	bffe03a9	stp	xzr, xzr, [x21, #0x38]
0x480e0	bf2600f9	str	xzr, [x21, #0x48]
0x480e4	bf7e00a9	stp	xzr, xzr, [x21]
0x480e8	b80a00f9	str	x24, [x21, #0x10]
0x480ec	d50200f9	str	x21, [x22]
0x480f0	680240f9	ldr	x8, [x19]
0x480f4	080140f9	ldr	x8, [x8]
0x480f8	e10315aa	mov	x1, x21
0x480fc	680000b4	cbz	x8, 0x48108 <_WeChatMain+0x2e89c>
0x48100	680200f9	str	x8, [x19]
0x48104	c10240f9	ldr	x1, [x22]
0x48108	600640f9	ldr	x0, [x19, #0x8]
0x4810c	0c70ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x48110	680a40f9	ldr	x8, [x19, #0x10]
0x48114	08050091	add	x8, x8, #0x1
0x48118	680a00f9	str	x8, [x19, #0x10]
0x4811c	21008052	mov	w1, #0x1                ; =1
0x48120	03000014	b	0x4812c <_WeChatMain+0x2e8c0>
0x48124	010080d2	mov	x1, #0x0                ; =0
0x48128	f50318aa	mov	x21, x24
0x4812c	e00315aa	mov	x0, x21
0x48130	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x48134	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x48138	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4813c	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x48140	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x48144	c0035fd6	ret
0x48148	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x4814c	f85f01a9	stp	x24, x23, [sp, #0x10]
0x48150	f65702a9	stp	x22, x21, [sp, #0x20]
0x48154	f44f03a9	stp	x20, x19, [sp, #0x30]
0x48158	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4815c	fd030191	add	x29, sp, #0x40
0x48160	f30300aa	mov	x19, x0
0x48164	778e40f8	ldr	x23, [x19, #0x8]!
0x48168	970600b4	cbz	x23, 0x48238 <_WeChatMain+0x2e9cc>
0x4816c	285c4039	ldrb	w8, [x1, #0x17]
0x48170	091d0013	sxtb	w9, w8
0x48174	3f010071	cmp	w9, #0x0
0x48178	292840a9	ldp	x9, x10, [x1]
0x4817c	34b1819a	csel	x20, x9, x1, lt
0x48180	56b1889a	csel	x22, x10, x8, lt
0x48184	18018052	mov	w24, #0x8               ; =8
0x48188	f50313aa	mov	x21, x19
0x4818c	e8de4039	ldrb	w8, [x23, #0x37]
0x48190	091d0013	sxtb	w9, w8
0x48194	ea0317aa	mov	x10, x23
0x48198	4b0d42f8	ldr	x11, [x10, #0x20]!
0x4819c	ec1640f9	ldr	x12, [x23, #0x28]
0x481a0	3f010071	cmp	w9, #0x0
0x481a4	60b18a9a	csel	x0, x11, x10, lt
0x481a8	99b1889a	csel	x25, x12, x8, lt
0x481ac	df0219eb	cmp	x22, x25
0x481b0	c232999a	csel	x2, x22, x25, lo
0x481b4	e10314aa	mov	x1, x20
0x481b8	31e3c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x481bc	3f0316eb	cmp	x25, x22
0x481c0	e8279f1a	cset	w8, lo
0x481c4	1f000071	cmp	w0, #0x0
0x481c8	e9a79f1a	cset	w9, lt
0x481cc	0801891a	csel	w8, w8, w9, eq
0x481d0	1f010071	cmp	w8, #0x0
0x481d4	08139f9a	csel	x8, x24, xzr, ne
0x481d8	b512979a	csel	x21, x21, x23, ne
0x481dc	f76a68f8	ldr	x23, [x23, x8]
0x481e0	77fdffb5	cbnz	x23, 0x4818c <_WeChatMain+0x2e920>
0x481e4	bf0213eb	cmp	x21, x19
0x481e8	80020054	b.eq	0x48238 <_WeChatMain+0x2e9cc>
0x481ec	a8de4039	ldrb	w8, [x21, #0x37]
0x481f0	091d0013	sxtb	w9, w8
0x481f4	ea0315aa	mov	x10, x21
0x481f8	4b0d42f8	ldr	x11, [x10, #0x20]!
0x481fc	ac1640f9	ldr	x12, [x21, #0x28]
0x48200	3f010071	cmp	w9, #0x0
0x48204	61b18a9a	csel	x1, x11, x10, lt
0x48208	97b1889a	csel	x23, x12, x8, lt
0x4820c	ff0216eb	cmp	x23, x22
0x48210	e232969a	csel	x2, x23, x22, lo
0x48214	e00314aa	mov	x0, x20
0x48218	19e3c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x4821c	df0217eb	cmp	x22, x23
0x48220	e8279f1a	cset	w8, lo
0x48224	1f000071	cmp	w0, #0x0
0x48228	e9a79f1a	cset	w9, lt
0x4822c	0801891a	csel	w8, w8, w9, eq
0x48230	1f010071	cmp	w8, #0x0
0x48234	7312959a	csel	x19, x19, x21, ne
0x48238	e00313aa	mov	x0, x19
0x4823c	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x48240	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x48244	f65742a9	ldp	x22, x21, [sp, #0x20]
0x48248	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x4824c	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x48250	c0035fd6	ret
0x48254	ff0301d1	sub	sp, sp, #0x40
0x48258	f65701a9	stp	x22, x21, [sp, #0x10]
0x4825c	f44f02a9	stp	x20, x19, [sp, #0x20]
0x48260	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x48264	fdc30091	add	x29, sp, #0x30
0x48268	f30300aa	mov	x19, x0
0x4826c	080440f9	ldr	x8, [x0, #0x8]
0x48270	a80700b5	cbnz	x8, 0x48364 <_WeChatMain+0x2eaf8>
0x48274	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48278	09614d39	ldrb	w9, [x8, #0x358]
0x4827c	09040037	tbnz	w9, #0x0, 0x482fc <_WeChatMain+0x2ea90>
0x48280	090080d2	mov	x9, #0x0                ; =0
0x48284	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x48288	aa9999f2	movk	x10, #0xcccd
0x4828c	6b028092	mov	x11, #-0x14             ; =-20
0x48290	0c2204b0	adrp	x12, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48294	8c812391	add	x12, x12, #0x8e0
0x48298	4085040f	movi.4h	v0, #0x8a
0x4829c	4d1005d0	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x482a0	adc90b91	add	x13, x13, #0x2f2
0x482a4	2e7dca9b	umulh	x14, x9, x10
0x482a8	cefd44d3	lsr	x14, x14, #4
0x482ac	8f01098b	add	x15, x12, x9
0x482b0	ce3d0b9b	madd	x14, x14, x11, x15
0x482b4	efe51791	add	x15, x15, #0x5f9
0x482b8	ce951791	add	x14, x14, #0x5e5
0x482bc	e10140bd	ldr	s1, [x15]
0x482c0	0110212e	uaddw.8h	v1, v0, v1
0x482c4	c20140bd	ldr	s2, [x14]
0x482c8	42a4082f	ushll.8h	v2, v2, #0x0
0x482cc	211c222e	eor.8b	v1, v1, v2
0x482d0	2118000e	uzp1.8b	v1, v1, v0
0x482d4	a16929bc	str	s1, [x13, x9]
0x482d8	29110091	add	x9, x9, #0x4
0x482dc	3f9101f1	cmp	x9, #0x64
0x482e0	21feff54	b.ne	0x482a4 <_WeChatMain+0x2ea38>
0x482e4	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x482e8	29590d91	add	x9, x9, #0x356
0x482ec	0a0d8052	mov	w10, #0x68              ; =104
0x482f0	2a010079	strh	w10, [x9]
0x482f4	29008052	mov	w9, #0x1                ; =1
0x482f8	09610d39	strb	w9, [x8, #0x358]
0x482fc	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48300	09b54d39	ldrb	w9, [x8, #0x36d]
0x48304	89010037	tbnz	w9, #0x0, 0x48334 <_WeChatMain+0x2eac8>
0x48308	c92104f0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4830c	209d47fd	ldr	d0, [x9, #0xf38]
0x48310	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48314	29810d91	add	x9, x9, #0x360
0x48318	200100fd	str	d0, [x9]
0x4831c	ca2104f0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x48320	40a147fd	ldr	d0, [x10, #0xf40]
0x48324	200900bd	str	s0, [x9, #0x8]
0x48328	3f310039	strb	wzr, [x9, #0xc]
0x4832c	29008052	mov	w9, #0x1                ; =1
0x48330	09b50d39	strb	w9, [x8, #0x36d]
0x48334	401005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48338	00c80b91	add	x0, x0, #0x2f2
0x4833c	421005d0	adrp	x2, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48340	42800d91	add	x2, x2, #0x360
0x48344	e8230091	add	x8, sp, #0x8
0x48348	a1128052	mov	w1, #0x95               ; =149
0x4834c	fe48ff97	bl	0x1a744 <_WeChatMain+0xed8>
0x48350	e0230091	add	x0, sp, #0x8
0x48354	4349ff97	bl	0x1a860 <_WeChatMain+0xff4>
0x48358	e0230091	add	x0, sp, #0x8
0x4835c	4449ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x48360	680640f9	ldr	x8, [x19, #0x8]
0x48364	095d8039	ldrsb	x9, [x8, #0x17]
0x48368	0a2d40a9	ldp	x10, x11, [x8]
0x4836c	3f0100f1	cmp	x9, #0x0
0x48370	40b1889a	csel	x0, x10, x8, lt
0x48374	3f010071	cmp	w9, #0x0
0x48378	61b1899a	csel	x1, x11, x9, lt
0x4837c	af2d0094	bl	0x53a38 <_WeChatMain+0x3a1cc>
0x48380	f50300aa	mov	x21, x0
0x48384	001000b4	cbz	x0, 0x48584 <_WeChatMain+0x2ed18>
0x48388	741240b9	ldr	w20, [x19, #0x10]
0x4838c	a80240f9	ldr	x8, [x21]
0x48390	081140f9	ldr	x8, [x8, #0x20]
0x48394	e00315aa	mov	x0, x21
0x48398	00013fd6	blr	x8
0x4839c	9f02006b	cmp	w20, w0
0x483a0	21010054	b.ne	0x483c4 <_WeChatMain+0x2eb58>
0x483a4	631240f9	ldr	x3, [x19, #0x20]
0x483a8	432700b4	cbz	x3, 0x48890 <_WeChatMain+0x2f024>
0x483ac	618a4229	ldp	w1, w2, [x19, #0x14]
0x483b0	a80240f9	ldr	x8, [x21]
0x483b4	081540f9	ldr	x8, [x8, #0x28]
0x483b8	e00315aa	mov	x0, x21
0x483bc	00013fd6	blr	x8
0x483c0	80260037	tbnz	w0, #0x0, 0x48890 <_WeChatMain+0x2f024>
0x483c4	680640f9	ldr	x8, [x19, #0x8]
0x483c8	a80700b5	cbnz	x8, 0x484bc <_WeChatMain+0x2ec50>
0x483cc	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x483d0	09614d39	ldrb	w9, [x8, #0x358]
0x483d4	09040037	tbnz	w9, #0x0, 0x48454 <_WeChatMain+0x2ebe8>
0x483d8	090080d2	mov	x9, #0x0                ; =0
0x483dc	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x483e0	aa9999f2	movk	x10, #0xcccd
0x483e4	6b028092	mov	x11, #-0x14             ; =-20
0x483e8	0c2204b0	adrp	x12, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x483ec	8c812391	add	x12, x12, #0x8e0
0x483f0	4085040f	movi.4h	v0, #0x8a
0x483f4	4d1005d0	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x483f8	adc90b91	add	x13, x13, #0x2f2
0x483fc	2e7dca9b	umulh	x14, x9, x10
0x48400	cefd44d3	lsr	x14, x14, #4
0x48404	8f01098b	add	x15, x12, x9
0x48408	ce3d0b9b	madd	x14, x14, x11, x15
0x4840c	efe51791	add	x15, x15, #0x5f9
0x48410	ce951791	add	x14, x14, #0x5e5
0x48414	e10140bd	ldr	s1, [x15]
0x48418	0110212e	uaddw.8h	v1, v0, v1
0x4841c	c20140bd	ldr	s2, [x14]
0x48420	42a4082f	ushll.8h	v2, v2, #0x0
0x48424	211c222e	eor.8b	v1, v1, v2
0x48428	2118000e	uzp1.8b	v1, v1, v0
0x4842c	a16929bc	str	s1, [x13, x9]
0x48430	29110091	add	x9, x9, #0x4
0x48434	3f9101f1	cmp	x9, #0x64
0x48438	21feff54	b.ne	0x483fc <_WeChatMain+0x2eb90>
0x4843c	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48440	29590d91	add	x9, x9, #0x356
0x48444	0a0d8052	mov	w10, #0x68              ; =104
0x48448	2a010079	strh	w10, [x9]
0x4844c	29008052	mov	w9, #0x1                ; =1
0x48450	09610d39	strb	w9, [x8, #0x358]
0x48454	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48458	09b54d39	ldrb	w9, [x8, #0x36d]
0x4845c	89010037	tbnz	w9, #0x0, 0x4848c <_WeChatMain+0x2ec20>
0x48460	c92104f0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x48464	209d47fd	ldr	d0, [x9, #0xf38]
0x48468	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4846c	29810d91	add	x9, x9, #0x360
0x48470	200100fd	str	d0, [x9]
0x48474	ca2104f0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x48478	40a147fd	ldr	d0, [x10, #0xf40]
0x4847c	200900bd	str	s0, [x9, #0x8]
0x48480	3f310039	strb	wzr, [x9, #0xc]
0x48484	29008052	mov	w9, #0x1                ; =1
0x48488	09b50d39	strb	w9, [x8, #0x36d]
0x4848c	401005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48490	00c80b91	add	x0, x0, #0x2f2
0x48494	421005d0	adrp	x2, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48498	42800d91	add	x2, x2, #0x360
0x4849c	e8230091	add	x8, sp, #0x8
0x484a0	a1128052	mov	w1, #0x95               ; =149
0x484a4	a848ff97	bl	0x1a744 <_WeChatMain+0xed8>
0x484a8	e0230091	add	x0, sp, #0x8
0x484ac	ed48ff97	bl	0x1a860 <_WeChatMain+0xff4>
0x484b0	e0230091	add	x0, sp, #0x8
0x484b4	ee48ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x484b8	680640f9	ldr	x8, [x19, #0x8]
0x484bc	095d8039	ldrsb	x9, [x8, #0x17]
0x484c0	0a2d40a9	ldp	x10, x11, [x8]
0x484c4	3f0100f1	cmp	x9, #0x0
0x484c8	40b1889a	csel	x0, x10, x8, lt
0x484cc	3f010071	cmp	w9, #0x0
0x484d0	61b1899a	csel	x1, x11, x9, lt
0x484d4	53130094	bl	0x4d220 <_WeChatMain+0x339b4>
0x484d8	e10300aa	mov	x1, x0
0x484dc	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x484e0	09a94939	ldrb	w9, [x8, #0x26a]
0x484e4	89040037	tbnz	w9, #0x0, 0x48574 <_WeChatMain+0x2ed08>
0x484e8	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x484ec	207943fd	ldr	d0, [x9, #0x6f0]
0x484f0	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x484f4	217d43fd	ldr	d1, [x9, #0x6f8]
0x484f8	20040c6e	mov.s	v0[1], v1[0]
0x484fc	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48500	218143fd	ldr	d1, [x9, #0x700]
0x48504	2004146e	mov.s	v0[2], v1[0]
0x48508	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4850c	218543fd	ldr	d1, [x9, #0x708]
0x48510	20041c6e	mov.s	v0[3], v1[0]
0x48514	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48518	218943fd	ldr	d1, [x9, #0x710]
0x4851c	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48520	228d43fd	ldr	d2, [x9, #0x718]
0x48524	41040c6e	mov.s	v1[1], v2[0]
0x48528	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4852c	229143fd	ldr	d2, [x9, #0x720]
0x48530	4104146e	mov.s	v1[2], v2[0]
0x48534	c92104d0	adrp	x9, 0x8482000 <_wxam_enc_uninit_10+0x8482000>
0x48538	229147fd	ldr	d2, [x9, #0xf20]
0x4853c	41041c6e	mov.s	v1[3], v2[0]
0x48540	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48544	229543fd	ldr	d2, [x9, #0x728]
0x48548	c92104f0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4854c	231141fd	ldr	d3, [x9, #0x220]
0x48550	62040c6e	mov.s	v2[1], v3[0]
0x48554	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48558	29010991	add	x9, x9, #0x240
0x4855c	200500ad	stp	q0, q1, [x9]
0x48560	221100fd	str	d2, [x9, #0x20]
0x48564	6a0e8052	mov	w10, #0x73              ; =115
0x48568	2a510079	strh	w10, [x9, #0x28]
0x4856c	29008052	mov	w9, #0x1                ; =1
0x48570	09a90939	strb	w9, [x8, #0x26a]
0x48574	401005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48578	00000991	add	x0, x0, #0x240
0x4857c	df0d0094	bl	0x4bcf8 <_WeChatMain+0x3248c>
0x48580	c2000014	b	0x48888 <_WeChatMain+0x2f01c>
0x48584	680640f9	ldr	x8, [x19, #0x8]
0x48588	a80700b5	cbnz	x8, 0x4867c <_WeChatMain+0x2ee10>
0x4858c	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48590	09614d39	ldrb	w9, [x8, #0x358]
0x48594	09040037	tbnz	w9, #0x0, 0x48614 <_WeChatMain+0x2eda8>
0x48598	090080d2	mov	x9, #0x0                ; =0
0x4859c	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x485a0	aa9999f2	movk	x10, #0xcccd
0x485a4	6b028092	mov	x11, #-0x14             ; =-20
0x485a8	0c2204b0	adrp	x12, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x485ac	8c812391	add	x12, x12, #0x8e0
0x485b0	4085040f	movi.4h	v0, #0x8a
0x485b4	4d1005d0	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x485b8	adc90b91	add	x13, x13, #0x2f2
0x485bc	2e7dca9b	umulh	x14, x9, x10
0x485c0	cefd44d3	lsr	x14, x14, #4
0x485c4	8f01098b	add	x15, x12, x9
0x485c8	ce3d0b9b	madd	x14, x14, x11, x15
0x485cc	efe51791	add	x15, x15, #0x5f9
0x485d0	ce951791	add	x14, x14, #0x5e5
0x485d4	e10140bd	ldr	s1, [x15]
0x485d8	0110212e	uaddw.8h	v1, v0, v1
0x485dc	c20140bd	ldr	s2, [x14]
0x485e0	42a4082f	ushll.8h	v2, v2, #0x0
0x485e4	211c222e	eor.8b	v1, v1, v2
0x485e8	2118000e	uzp1.8b	v1, v1, v0
0x485ec	a16929bc	str	s1, [x13, x9]
0x485f0	29110091	add	x9, x9, #0x4
0x485f4	3f9101f1	cmp	x9, #0x64
0x485f8	21feff54	b.ne	0x485bc <_WeChatMain+0x2ed50>
0x485fc	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48600	29590d91	add	x9, x9, #0x356
0x48604	0a0d8052	mov	w10, #0x68              ; =104
0x48608	2a010079	strh	w10, [x9]
0x4860c	29008052	mov	w9, #0x1                ; =1
0x48610	09610d39	strb	w9, [x8, #0x358]
0x48614	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48618	09b54d39	ldrb	w9, [x8, #0x36d]
0x4861c	89010037	tbnz	w9, #0x0, 0x4864c <_WeChatMain+0x2ede0>
0x48620	c92104f0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x48624	209d47fd	ldr	d0, [x9, #0xf38]
0x48628	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4862c	29810d91	add	x9, x9, #0x360
0x48630	200100fd	str	d0, [x9]
0x48634	ca2104f0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x48638	40a147fd	ldr	d0, [x10, #0xf40]
0x4863c	200900bd	str	s0, [x9, #0x8]
0x48640	3f310039	strb	wzr, [x9, #0xc]
0x48644	29008052	mov	w9, #0x1                ; =1
0x48648	09b50d39	strb	w9, [x8, #0x36d]
0x4864c	401005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48650	00c80b91	add	x0, x0, #0x2f2
0x48654	421005d0	adrp	x2, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48658	42800d91	add	x2, x2, #0x360
0x4865c	e8230091	add	x8, sp, #0x8
0x48660	a1128052	mov	w1, #0x95               ; =149
0x48664	3848ff97	bl	0x1a744 <_WeChatMain+0xed8>
0x48668	e0230091	add	x0, sp, #0x8
0x4866c	7d48ff97	bl	0x1a860 <_WeChatMain+0xff4>
0x48670	e0230091	add	x0, sp, #0x8
0x48674	7e48ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x48678	680640f9	ldr	x8, [x19, #0x8]
0x4867c	095d8039	ldrsb	x9, [x8, #0x17]
0x48680	0a2d40a9	ldp	x10, x11, [x8]
0x48684	3f0100f1	cmp	x9, #0x0
0x48688	40b1889a	csel	x0, x10, x8, lt
0x4868c	3f010071	cmp	w9, #0x0
0x48690	61b1899a	csel	x1, x11, x9, lt
0x48694	fa120094	bl	0x4d27c <_WeChatMain+0x33a10>
0x48698	af2e0094	bl	0x54154 <_WeChatMain+0x3a8e8>
0x4869c	600f0034	cbz	w0, 0x48888 <_WeChatMain+0x2f01c>
0x486a0	680240f9	ldr	x8, [x19]
0x486a4	080140f9	ldr	x8, [x8]
0x486a8	e00313aa	mov	x0, x19
0x486ac	00013fd6	blr	x8
0x486b0	b12a0094	bl	0x53174 <_WeChatMain+0x39908>
0x486b4	f50300aa	mov	x21, x0
0x486b8	681240f9	ldr	x8, [x19, #0x20]
0x486bc	480100b5	cbnz	x8, 0x486e4 <_WeChatMain+0x2ee78>
0x486c0	a92240a9	ldp	x9, x8, [x21]
0x486c4	0a0109cb	sub	x10, x8, x9
0x486c8	4afd4293	asr	x10, x10, #2
0x486cc	4a0500d1	sub	x10, x10, #0x1
0x486d0	6a1200f9	str	x10, [x19, #0x20]
0x486d4	290540b9	ldr	w9, [x9, #0x4]
0x486d8	691600b9	str	w9, [x19, #0x14]
0x486dc	08815fb8	ldur	w8, [x8, #-0x8]
0x486e0	681a00b9	str	w8, [x19, #0x18]
0x486e4	ff0700b9	str	wzr, [sp, #0x4]
0x486e8	8d160094	bl	0x4e11c <_WeChatMain+0x348b0>
0x486ec	f40300aa	mov	x20, x0
0x486f0	400900b4	cbz	x0, 0x48818 <_WeChatMain+0x2efac>
0x486f4	761240b9	ldr	w22, [x19, #0x10]
0x486f8	620640f9	ldr	x2, [x19, #0x8]
0x486fc	a20700b5	cbnz	x2, 0x487f0 <_WeChatMain+0x2ef84>
0x48700	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48704	09614d39	ldrb	w9, [x8, #0x358]
0x48708	09040037	tbnz	w9, #0x0, 0x48788 <_WeChatMain+0x2ef1c>
0x4870c	090080d2	mov	x9, #0x0                ; =0
0x48710	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x48714	aa9999f2	movk	x10, #0xcccd
0x48718	6b028092	mov	x11, #-0x14             ; =-20
0x4871c	0c2204b0	adrp	x12, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48720	8c812391	add	x12, x12, #0x8e0
0x48724	4085040f	movi.4h	v0, #0x8a
0x48728	4d1005d0	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4872c	adc90b91	add	x13, x13, #0x2f2
0x48730	2e7dca9b	umulh	x14, x9, x10
0x48734	cefd44d3	lsr	x14, x14, #4
0x48738	8f01098b	add	x15, x12, x9
0x4873c	ce3d0b9b	madd	x14, x14, x11, x15
0x48740	efe51791	add	x15, x15, #0x5f9
0x48744	ce951791	add	x14, x14, #0x5e5
0x48748	e10140bd	ldr	s1, [x15]
0x4874c	0110212e	uaddw.8h	v1, v0, v1
0x48750	c20140bd	ldr	s2, [x14]
0x48754	42a4082f	ushll.8h	v2, v2, #0x0
0x48758	211c222e	eor.8b	v1, v1, v2
0x4875c	2118000e	uzp1.8b	v1, v1, v0
0x48760	a16929bc	str	s1, [x13, x9]
0x48764	29110091	add	x9, x9, #0x4
0x48768	3f9101f1	cmp	x9, #0x64
0x4876c	21feff54	b.ne	0x48730 <_WeChatMain+0x2eec4>
0x48770	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48774	29590d91	add	x9, x9, #0x356
0x48778	0a0d8052	mov	w10, #0x68              ; =104
0x4877c	2a010079	strh	w10, [x9]
0x48780	29008052	mov	w9, #0x1                ; =1
0x48784	09610d39	strb	w9, [x8, #0x358]
0x48788	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4878c	09b54d39	ldrb	w9, [x8, #0x36d]
0x48790	89010037	tbnz	w9, #0x0, 0x487c0 <_WeChatMain+0x2ef54>
0x48794	c92104f0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x48798	209d47fd	ldr	d0, [x9, #0xf38]
0x4879c	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x487a0	29810d91	add	x9, x9, #0x360
0x487a4	200100fd	str	d0, [x9]
0x487a8	ca2104f0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x487ac	40a147fd	ldr	d0, [x10, #0xf40]
0x487b0	200900bd	str	s0, [x9, #0x8]
0x487b4	3f310039	strb	wzr, [x9, #0xc]
0x487b8	29008052	mov	w9, #0x1                ; =1
0x487bc	09b50d39	strb	w9, [x8, #0x36d]
0x487c0	401005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x487c4	00c80b91	add	x0, x0, #0x2f2
0x487c8	421005d0	adrp	x2, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x487cc	42800d91	add	x2, x2, #0x360
0x487d0	e8230091	add	x8, sp, #0x8
0x487d4	a1128052	mov	w1, #0x95               ; =149
0x487d8	db47ff97	bl	0x1a744 <_WeChatMain+0xed8>
0x487dc	e0230091	add	x0, sp, #0x8
0x487e0	2048ff97	bl	0x1a860 <_WeChatMain+0xff4>
0x487e4	e0230091	add	x0, sp, #0x8
0x487e8	2148ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x487ec	620640f9	ldr	x2, [x19, #0x8]
0x487f0	63924229	ldp	w3, w4, [x19, #0x14]
0x487f4	662a40b9	ldr	w6, [x19, #0x28]
0x487f8	e8230091	add	x8, sp, #0x8
0x487fc	e7130091	add	x7, sp, #0x4
0x48800	e00314aa	mov	x0, x20
0x48804	e10316aa	mov	x1, x22
0x48808	e50315aa	mov	x5, x21
0x4880c	a1150094	bl	0x4de90 <_WeChatMain+0x34624>
0x48810	f60740f9	ldr	x22, [sp, #0x8]
0x48814	d60100b5	cbnz	x22, 0x4884c <_WeChatMain+0x2efe0>
0x48818	682a40b9	ldr	w8, [x19, #0x28]
0x4881c	08791912	and	w8, w8, #0xffffffbf
0x48820	682a00b9	str	w8, [x19, #0x28]
0x48824	680240f9	ldr	x8, [x19]
0x48828	090540f9	ldr	x9, [x8, #0x8]
0x4882c	e8230091	add	x8, sp, #0x8
0x48830	e00313aa	mov	x0, x19
0x48834	e10315aa	mov	x1, x21
0x48838	20013fd6	blr	x9
0x4883c	f60740f9	ldr	x22, [sp, #0x8]
0x48840	612a40b9	ldr	w1, [x19, #0x28]
0x48844	e00316aa	mov	x0, x22
0x48848	290b0094	bl	0x4b4ec <_WeChatMain+0x31c80>
0x4884c	680240f9	ldr	x8, [x19]
0x48850	080940f9	ldr	x8, [x8, #0x10]
0x48854	e00313aa	mov	x0, x19
0x48858	e10316aa	mov	x1, x22
0x4885c	00013fd6	blr	x8
0x48860	e00316aa	mov	x0, x22
0x48864	d4290094	bl	0x52fb4 <_WeChatMain+0x39748>
0x48868	f50300aa	mov	x21, x0
0x4886c	e10740b9	ldr	w1, [sp, #0x4]
0x48870	c1d8ff34	cbz	w1, 0x48388 <_WeChatMain+0x2eb1c>
0x48874	bf0216eb	cmp	x21, x22
0x48878	e2179f1a	cset	w2, eq
0x4887c	e00314aa	mov	x0, x20
0x48880	1e160094	bl	0x4e0f8 <_WeChatMain+0x3488c>
0x48884	c1feff17	b	0x48388 <_WeChatMain+0x2eb1c>
0x48888	72f7ff97	bl	0x46650 <_WeChatMain+0x2cde4>
0x4888c	f50300aa	mov	x21, x0
0x48890	e00315aa	mov	x0, x21
0x48894	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x48898	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4889c	f65741a9	ldp	x22, x21, [sp, #0x10]
0x488a0	ff030191	add	sp, sp, #0x40
0x488a4	c0035fd6	ret
0x488a8	ff4302d1	sub	sp, sp, #0x90
0x488ac	fa6704a9	stp	x26, x25, [sp, #0x40]
0x488b0	f85f05a9	stp	x24, x23, [sp, #0x50]
0x488b4	f65706a9	stp	x22, x21, [sp, #0x60]
0x488b8	f44f07a9	stp	x20, x19, [sp, #0x70]
0x488bc	fd7b08a9	stp	x29, x30, [sp, #0x80]
0x488c0	fd030291	add	x29, sp, #0x80
0x488c4	f30304aa	mov	x19, x4
0x488c8	f40300aa	mov	x20, x0
0x488cc	e2070729	stp	w2, w1, [sp, #0x38]
0x488d0	e31b00f9	str	x3, [sp, #0x30]
0x488d4	085c8039	ldrsb	x8, [x0, #0x17]
0x488d8	092840a9	ldp	x9, x10, [x0]
0x488dc	1f0100f1	cmp	x8, #0x0
0x488e0	20b1809a	csel	x0, x9, x0, lt
0x488e4	1f010071	cmp	w8, #0x0
0x488e8	41b1889a	csel	x1, x10, x8, lt
0x488ec	e2f30091	add	x2, sp, #0x3c
0x488f0	e3e30091	add	x3, sp, #0x38
0x488f4	e4c30091	add	x4, sp, #0x30
0x488f8	2e000094	bl	0x489b0 <_WeChatMain+0x2f144>
0x488fc	c0040036	tbz	w0, #0x0, 0x48994 <_WeChatMain+0x2f128>
0x48900	f85f4729	ldp	w24, w23, [sp, #0x38]
0x48904	f91b40f9	ldr	x25, [sp, #0x30]
0x48908	95d704b0	adrp	x21, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4890c	b5620391	add	x21, x21, #0xd8
0x48910	f50300f9	str	x21, [sp]
0x48914	88765e92	and	x8, x20, #0xfffffffc00000000
0x48918	96fd04d0	adrp	x22, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4891c	d6023b91	add	x22, x22, #0xec0
0x48920	c90640f9	ldr	x9, [x22, #0x8]
0x48924	1f0109eb	cmp	x8, x9
0x48928	61000054	b.ne	0x48934 <_WeChatMain+0x2f0c8>
0x4892c	e00314aa	mov	x0, x20
0x48930	c7dbff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x48934	f40700f9	str	x20, [sp, #0x8]
0x48938	ff5f0229	stp	wzr, w23, [sp, #0x10]
0x4893c	f81b00b9	str	w24, [sp, #0x18]
0x48940	f91300f9	str	x25, [sp, #0x20]
0x48944	f32b00b9	str	w19, [sp, #0x28]
0x48948	e0030091	mov	x0, sp
0x4894c	42feff97	bl	0x48254 <_WeChatMain+0x2e9e8>
0x48950	f50300f9	str	x21, [sp]
0x48954	e80740f9	ldr	x8, [sp, #0x8]
0x48958	09755e92	and	x9, x8, #0xfffffffc00000000
0x4895c	ca0640f9	ldr	x10, [x22, #0x8]
0x48960	3f010aeb	cmp	x9, x10
0x48964	a1000054	b.ne	0x48978 <_WeChatMain+0x2f10c>
0x48968	f30300aa	mov	x19, x0
0x4896c	e00308aa	mov	x0, x8
0x48970	54dcff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x48974	e00313aa	mov	x0, x19
0x48978	fd7b48a9	ldp	x29, x30, [sp, #0x80]
0x4897c	f44f47a9	ldp	x20, x19, [sp, #0x70]
0x48980	f65746a9	ldp	x22, x21, [sp, #0x60]
0x48984	f85f45a9	ldp	x24, x23, [sp, #0x50]
0x48988	fa6744a9	ldp	x26, x25, [sp, #0x40]
0x4898c	ff430291	add	sp, sp, #0x90
0x48990	c0035fd6	ret
0x48994	fd7b48a9	ldp	x29, x30, [sp, #0x80]
0x48998	f44f47a9	ldp	x20, x19, [sp, #0x70]
0x4899c	f65746a9	ldp	x22, x21, [sp, #0x60]
0x489a0	f85f45a9	ldp	x24, x23, [sp, #0x50]
0x489a4	fa6744a9	ldp	x26, x25, [sp, #0x40]
0x489a8	ff430291	add	sp, sp, #0x90
0x489ac	29f7ff17	b	0x46650 <_WeChatMain+0x2cde4>
0x489b0	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x489b4	f85f01a9	stp	x24, x23, [sp, #0x10]
0x489b8	f65702a9	stp	x22, x21, [sp, #0x20]
0x489bc	f44f03a9	stp	x20, x19, [sp, #0x30]
0x489c0	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x489c4	fd030191	add	x29, sp, #0x40
0x489c8	f50304aa	mov	x21, x4
0x489cc	f70303aa	mov	x23, x3
0x489d0	f60302aa	mov	x22, x2
0x489d4	f30301aa	mov	x19, x1
0x489d8	f40300aa	mov	x20, x0
0x489dc	490040b9	ldr	w9, [x2]
0x489e0	680040b9	ldr	w8, [x3]
0x489e4	3f01086b	cmp	w9, w8
0x489e8	f9c79f1a	cset	w25, le
0x489ec	ad000054	b.le	0x48a00 <_WeChatMain+0x2f194>
0x489f0	c80200b9	str	w8, [x22]
0x489f4	e90200b9	str	w9, [x23]
0x489f8	e80309aa	mov	x8, x9
0x489fc	c90240b9	ldr	w9, [x22]
0x48a00	3f010071	cmp	w9, #0x0
0x48a04	0c010054	b.gt	0x48a24 <_WeChatMain+0x2f1b8>
0x48a08	29008052	mov	w9, #0x1                ; =1
0x48a0c	c90200b9	str	w9, [x22]
0x48a10	e80240b9	ldr	w8, [x23]
0x48a14	1f010071	cmp	w8, #0x0
0x48a18	6c000054	b.gt	0x48a24 <_WeChatMain+0x2f1b8>
0x48a1c	e90200b9	str	w9, [x23]
0x48a20	28008052	mov	w8, #0x1                ; =1
0x48a24	092204d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x48a28	29410091	add	x9, x9, #0x10
0x48a2c	290140b9	ldr	w9, [x9]
0x48a30	1f01096b	cmp	w8, w9
0x48a34	6b000054	b.lt	0x48a40 <_WeChatMain+0x2f1d4>
0x48a38	28050051	sub	w8, w9, #0x1
0x48a3c	e80200b9	str	w8, [x23]
0x48a40	a80240f9	ldr	x8, [x21]
0x48a44	1fad0ff1	cmp	x8, #0x3eb
0x48a48	e3070054	b.lo	0x48b44 <_WeChatMain+0x2f2d8>
0x48a4c	e00314aa	mov	x0, x20
0x48a50	e10313aa	mov	x1, x19
0x48a54	f3110094	bl	0x4d220 <_WeChatMain+0x339b4>
0x48a58	e10300aa	mov	x1, x0
0x48a5c	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48a60	09294a39	ldrb	w9, [x8, #0x28a]
0x48a64	89030037	tbnz	w9, #0x0, 0x48ad4 <_WeChatMain+0x2f268>
0x48a68	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48a6c	207943fd	ldr	d0, [x9, #0x6f0]
0x48a70	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48a74	217d43fd	ldr	d1, [x9, #0x6f8]
0x48a78	20040c6e	mov.s	v0[1], v1[0]
0x48a7c	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48a80	219943fd	ldr	d1, [x9, #0x730]
0x48a84	2004146e	mov.s	v0[2], v1[0]
0x48a88	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48a8c	219d43fd	ldr	d1, [x9, #0x738]
0x48a90	20041c6e	mov.s	v0[3], v1[0]
0x48a94	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48a98	29b10991	add	x9, x9, #0x26c
0x48a9c	2001803d	str	q0, [x9]
0x48aa0	0a2204b0	adrp	x10, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48aa4	40a143fd	ldr	d0, [x10, #0x740]
0x48aa8	0a2204b0	adrp	x10, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48aac	41a543fd	ldr	d1, [x10, #0x748]
0x48ab0	20040c6e	mov.s	v0[1], v1[0]
0x48ab4	200900fd	str	d0, [x9, #0x10]
0x48ab8	0a2204b0	adrp	x10, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48abc	40a943fd	ldr	d0, [x10, #0x750]
0x48ac0	201900bd	str	s0, [x9, #0x18]
0x48ac4	0a068052	mov	w10, #0x30              ; =48
0x48ac8	2a390079	strh	w10, [x9, #0x1c]
0x48acc	29008052	mov	w9, #0x1                ; =1
0x48ad0	09290a39	strb	w9, [x8, #0x28a]
0x48ad4	401005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48ad8	00b00991	add	x0, x0, #0x26c
0x48adc	870c0094	bl	0x4bcf8 <_WeChatMain+0x3248c>
0x48ae0	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48ae4	09854a39	ldrb	w9, [x8, #0x2a1]
0x48ae8	29010037	tbnz	w9, #0x0, 0x48b0c <_WeChatMain+0x2f2a0>
0x48aec	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48af0	2015c23d	ldr	q0, [x9, #0x850]
0x48af4	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48af8	29410a91	add	x9, x9, #0x290
0x48afc	2001803d	str	q0, [x9]
0x48b00	3f410039	strb	wzr, [x9, #0x10]
0x48b04	29008052	mov	w9, #0x1                ; =1
0x48b08	09850a39	strb	w9, [x8, #0x2a1]
0x48b0c	581005d0	adrp	x24, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48b10	18430a91	add	x24, x24, #0x290
0x48b14	e00318aa	mov	x0, x24
0x48b18	b8e3c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x48b1c	e30300aa	mov	x3, x0
0x48b20	e00314aa	mov	x0, x20
0x48b24	e10313aa	mov	x1, x19
0x48b28	e20318aa	mov	x2, x24
0x48b2c	04008052	mov	w4, #0x0                ; =0
0x48b30	bb750094	bl	0x6621c <_WeChatMain+0x4c9b0>
0x48b34	80000037	tbnz	w0, #0x0, 0x48b44 <_WeChatMain+0x2f2d8>
0x48b38	19008052	mov	w25, #0x0               ; =0
0x48b3c	c80c8052	mov	w8, #0x66               ; =102
0x48b40	a80200f9	str	x8, [x21]
0x48b44	e80240b9	ldr	w8, [x23]
0x48b48	c90240b9	ldr	w9, [x22]
0x48b4c	1f01096b	cmp	w8, w9
0x48b50	81000054	b.ne	0x48b60 <_WeChatMain+0x2f2f4>
0x48b54	19008052	mov	w25, #0x0               ; =0
0x48b58	08050011	add	w8, w8, #0x1
0x48b5c	e80200b9	str	w8, [x23]
0x48b60	a90240f9	ldr	x9, [x21]
0x48b64	3f0d00f1	cmp	x9, #0x3
0x48b68	42010054	b.hs	0x48b90 <_WeChatMain+0x2f324>
0x48b6c	69008052	mov	w9, #0x3                ; =3
0x48b70	a90200f9	str	x9, [x21]
0x48b74	c90240b9	ldr	w9, [x22]
0x48b78	0801094b	sub	w8, w8, w9
0x48b7c	08090011	add	w8, w8, #0x2
0x48b80	1f090071	cmp	w8, #0x2
0x48b84	48010054	b.hi	0x48bac <_WeChatMain+0x2f340>
0x48b88	087d4093	sxtw	x8, w8
0x48b8c	07000014	b	0x48ba8 <_WeChatMain+0x2f33c>
0x48b90	ca0240b9	ldr	w10, [x22]
0x48b94	08010a4b	sub	w8, w8, w10
0x48b98	08090011	add	w8, w8, #0x2
0x48b9c	087d4093	sxtw	x8, w8
0x48ba0	3f0108eb	cmp	x9, x8
0x48ba4	29060054	b.ls	0x48c68 <_WeChatMain+0x2f3fc>
0x48ba8	a80200f9	str	x8, [x21]
0x48bac	e00314aa	mov	x0, x20
0x48bb0	e10313aa	mov	x1, x19
0x48bb4	9b110094	bl	0x4d220 <_WeChatMain+0x339b4>
0x48bb8	e10300aa	mov	x1, x0
0x48bbc	481005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48bc0	091d4b39	ldrb	w9, [x8, #0x2c7]
0x48bc4	e9030037	tbnz	w9, #0x0, 0x48c40 <_WeChatMain+0x2f3d4>
0x48bc8	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48bcc	207943fd	ldr	d0, [x9, #0x6f0]
0x48bd0	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48bd4	217d43fd	ldr	d1, [x9, #0x6f8]
0x48bd8	20040c6e	mov.s	v0[1], v1[0]
0x48bdc	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48be0	21ad43fd	ldr	d1, [x9, #0x758]
0x48be4	2004146e	mov.s	v0[2], v1[0]
0x48be8	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48bec	21b143fd	ldr	d1, [x9, #0x760]
0x48bf0	20041c6e	mov.s	v0[3], v1[0]
0x48bf4	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48bf8	21b543fd	ldr	d1, [x9, #0x768]
0x48bfc	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48c00	22b943fd	ldr	d2, [x9, #0x770]
0x48c04	41040c6e	mov.s	v1[1], v2[0]
0x48c08	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48c0c	22bd43fd	ldr	d2, [x9, #0x778]
0x48c10	4104146e	mov.s	v1[2], v2[0]
0x48c14	092204b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x48c18	22c143fd	ldr	d2, [x9, #0x780]
0x48c1c	41041c6e	mov.s	v1[3], v2[0]
0x48c20	491005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48c24	29910a91	add	x9, x9, #0x2a4
0x48c28	200500ad	stp	q0, q1, [x9]
0x48c2c	8a6e8e52	mov	w10, #0x7374            ; =29556
0x48c30	2a410079	strh	w10, [x9, #0x20]
0x48c34	3f890039	strb	wzr, [x9, #0x22]
0x48c38	29008052	mov	w9, #0x1                ; =1
0x48c3c	091d0b39	strb	w9, [x8, #0x2c7]
0x48c40	401005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x48c44	00900a91	add	x0, x0, #0x2a4
0x48c48	2c0c0094	bl	0x4bcf8 <_WeChatMain+0x3248c>
0x48c4c	00008052	mov	w0, #0x0                ; =0
0x48c50	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x48c54	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x48c58	f65742a9	ldp	x22, x21, [sp, #0x20]
0x48c5c	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x48c60	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x48c64	c0035fd6	ret
0x48c68	39fa0736	tbz	w25, #0x0, 0x48bac <_WeChatMain+0x2f340>
0x48c6c	20008052	mov	w0, #0x1                ; =1
0x48c70	f8ffff17	b	0x48c50 <_WeChatMain+0x2f3e4>
0x48c74	ffc301d1	sub	sp, sp, #0x70
0x48c78	fa6702a9	stp	x26, x25, [sp, #0x20]
0x48c7c	f85f03a9	stp	x24, x23, [sp, #0x30]
0x48c80	f65704a9	stp	x22, x21, [sp, #0x40]
0x48c84	f44f05a9	stp	x20, x19, [sp, #0x50]
0x48c88	fd7b06a9	stp	x29, x30, [sp, #0x60]
0x48c8c	fd830191	add	x29, sp, #0x60
0x48c90	f30304aa	mov	x19, x4
0x48c94	f40303aa	mov	x20, x3
0x48c98	f50302aa	mov	x21, x2
0x48c9c	f60301aa	mov	x22, x1
0x48ca0	f80300aa	mov	x24, x0
0x48ca4	55e3c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x48ca8	e8ef7db2	mov	x8, #0x7ffffffffffffff8 ; =9223372036854775800
0x48cac	1f0008eb	cmp	x0, x8
0x48cb0	a2050054	b.hs	0x48d64 <_WeChatMain+0x2f4f8>
0x48cb4	f70300aa	mov	x23, x0
0x48cb8	1f5c00f1	cmp	x0, #0x17
0x48cbc	a2000054	b.hs	0x48cd0 <_WeChatMain+0x2f464>
0x48cc0	f77f0039	strb	w23, [sp, #0x1f]
0x48cc4	f9230091	add	x25, sp, #0x8
0x48cc8	970100b5	cbnz	x23, 0x48cf8 <_WeChatMain+0x2f48c>
0x48ccc	0f000014	b	0x48d08 <_WeChatMain+0x2f49c>
0x48cd0	e80a40b2	orr	x8, x23, #0x7
0x48cd4	1f5d00f1	cmp	x8, #0x17
0x48cd8	29038052	mov	w9, #0x19               ; =25
0x48cdc	3a05889a	csinc	x26, x9, x8, eq
0x48ce0	e0031aaa	mov	x0, x26
0x48ce4	d3dcc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x48ce8	f90300aa	mov	x25, x0
0x48cec	480341b2	orr	x8, x26, #0x8000000000000000
0x48cf0	f72301a9	stp	x23, x8, [sp, #0x10]
0x48cf4	e00700f9	str	x0, [sp, #0x8]
0x48cf8	e00319aa	mov	x0, x25
0x48cfc	e10318aa	mov	x1, x24
0x48d00	e20317aa	mov	x2, x23
0x48d04	61e0c395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x48d08	3f6b3738	strb	wzr, [x25, x23]
0x48d0c	e0230091	add	x0, sp, #0x8
0x48d10	e10316aa	mov	x1, x22
0x48d14	e20315aa	mov	x2, x21
0x48d18	e30314aa	mov	x3, x20
0x48d1c	e40313aa	mov	x4, x19
0x48d20	e2feff97	bl	0x488a8 <_WeChatMain+0x2f03c>
0x48d24	e87fc039	ldrsb	w8, [sp, #0x1f]
0x48d28	0801f836	tbz	w8, #0x1f, 0x48d48 <_WeChatMain+0x2f4dc>
0x48d2c	e80740f9	ldr	x8, [sp, #0x8]
0x48d30	e90f40f9	ldr	x9, [sp, #0x18]
0x48d34	21f94092	and	x1, x9, #0x7fffffffffffffff
0x48d38	f30300aa	mov	x19, x0
0x48d3c	e00308aa	mov	x0, x8
0x48d40	b3dcc395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x48d44	e00313aa	mov	x0, x19
0x48d48	fd7b46a9	ldp	x29, x30, [sp, #0x60]
0x48d4c	f44f45a9	ldp	x20, x19, [sp, #0x50]
0x48d50	f65744a9	ldp	x22, x21, [sp, #0x40]
0x48d54	f85f43a9	ldp	x24, x23, [sp, #0x30]
0x48d58	fa6742a9	ldp	x26, x25, [sp, #0x20]
0x48d5c	ffc30191	add	sp, sp, #0x70
0x48d60	c0035fd6	ret
0x48d64	e0230091	add	x0, sp, #0x8
0x48d68	c547ff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x48d6c	ff0302d1	sub	sp, sp, #0x80
0x48d70	fa6703a9	stp	x26, x25, [sp, #0x30]
0x48d74	f85f04a9	stp	x24, x23, [sp, #0x40]
0x48d78	f65705a9	stp	x22, x21, [sp, #0x50]
0x48d7c	f44f06a9	stp	x20, x19, [sp, #0x60]
0x48d80	fd7b07a9	stp	x29, x30, [sp, #0x70]
0x48d84	fdc30191	add	x29, sp, #0x70
0x48d88	f30304aa	mov	x19, x4
0x48d8c	f40303aa	mov	x20, x3
0x48d90	f50302aa	mov	x21, x2
0x48d94	f60301aa	mov	x22, x1
0x48d98	f80300aa	mov	x24, x0
0x48d9c	17e3c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x48da0	e8ef7db2	mov	x8, #0x7ffffffffffffff8 ; =9223372036854775800
0x48da4	1f0008eb	cmp	x0, x8
0x48da8	62060054	b.hs	0x48e74 <_WeChatMain+0x2f608>
0x48dac	f70300aa	mov	x23, x0
0x48db0	1f5c00f1	cmp	x0, #0x17
0x48db4	a2000054	b.hs	0x48dc8 <_WeChatMain+0x2f55c>
0x48db8	f77f0039	strb	w23, [sp, #0x1f]
0x48dbc	f9230091	add	x25, sp, #0x8
0x48dc0	970100b5	cbnz	x23, 0x48df0 <_WeChatMain+0x2f584>
0x48dc4	0f000014	b	0x48e00 <_WeChatMain+0x2f594>
0x48dc8	e80a40b2	orr	x8, x23, #0x7
0x48dcc	1f5d00f1	cmp	x8, #0x17
0x48dd0	29038052	mov	w9, #0x19               ; =25
0x48dd4	3a05889a	csinc	x26, x9, x8, eq
0x48dd8	e0031aaa	mov	x0, x26
0x48ddc	95dcc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x48de0	f90300aa	mov	x25, x0
0x48de4	480341b2	orr	x8, x26, #0x8000000000000000
0x48de8	f72301a9	stp	x23, x8, [sp, #0x10]
0x48dec	e00700f9	str	x0, [sp, #0x8]
0x48df0	e00319aa	mov	x0, x25
0x48df4	e10318aa	mov	x1, x24
0x48df8	e20317aa	mov	x2, x23
0x48dfc	23e0c395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x48e00	3f6b3738	strb	wzr, [x25, x23]
0x48e04	f55b02a9	stp	x21, x22, [sp, #0x20]
0x48e08	e0a30091	add	x0, sp, #0x28
0x48e0c	37700194	bl	0xa4ee8 <_WeChatMain+0x8b67c>
0x48e10	f50300aa	mov	x21, x0
0x48e14	e0830091	add	x0, sp, #0x20
0x48e18	34700194	bl	0xa4ee8 <_WeChatMain+0x8b67c>
0x48e1c	e20300aa	mov	x2, x0
0x48e20	e0230091	add	x0, sp, #0x8
0x48e24	e10315aa	mov	x1, x21
0x48e28	e30314aa	mov	x3, x20
0x48e2c	e40313aa	mov	x4, x19
0x48e30	9efeff97	bl	0x488a8 <_WeChatMain+0x2f03c>
0x48e34	e87fc039	ldrsb	w8, [sp, #0x1f]
0x48e38	0801f836	tbz	w8, #0x1f, 0x48e58 <_WeChatMain+0x2f5ec>
0x48e3c	e80740f9	ldr	x8, [sp, #0x8]
0x48e40	e90f40f9	ldr	x9, [sp, #0x18]
0x48e44	21f94092	and	x1, x9, #0x7fffffffffffffff
0x48e48	f30300aa	mov	x19, x0
0x48e4c	e00308aa	mov	x0, x8
0x48e50	6fdcc395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x48e54	e00313aa	mov	x0, x19
0x48e58	fd7b47a9	ldp	x29, x30, [sp, #0x70]
0x48e5c	f44f46a9	ldp	x20, x19, [sp, #0x60]
0x48e60	f65745a9	ldp	x22, x21, [sp, #0x50]
0x48e64	f85f44a9	ldp	x24, x23, [sp, #0x40]
0x48e68	fa6743a9	ldp	x26, x25, [sp, #0x30]
0x48e6c	ff030291	add	sp, sp, #0x80
0x48e70	c0035fd6	ret
0x48e74	e0230091	add	x0, sp, #0x8
0x48e78	8147ff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x48e7c	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x48e80	f85f01a9	stp	x24, x23, [sp, #0x10]
0x48e84	f65702a9	stp	x22, x21, [sp, #0x20]
0x48e88	f44f03a9	stp	x20, x19, [sp, #0x30]
0x48e8c	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x48e90	fd030191	add	x29, sp, #0x40
0x48e94	f30305aa	mov	x19, x5
0x48e98	f40304aa	mov	x20, x4
0x48e9c	f50303aa	mov	x21, x3
0x48ea0	f60302aa	mov	x22, x2
0x48ea4	f70301aa	mov	x23, x1
0x48ea8	f80300aa	mov	x24, x0
0x48eac	f90308aa	mov	x25, x8
0x48eb0	00058052	mov	w0, #0x28               ; =40
0x48eb4	5fdcc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x48eb8	e10318aa	mov	x1, x24
0x48ebc	e20317aa	mov	x2, x23
0x48ec0	e30316aa	mov	x3, x22
0x48ec4	e40315aa	mov	x4, x21
0x48ec8	e50314aa	mov	x5, x20
0x48ecc	e60313aa	mov	x6, x19
0x48ed0	c0010094	bl	0x495d0 <_WeChatMain+0x2fd64>
0x48ed4	200300f9	str	x0, [x25]
0x48ed8	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x48edc	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x48ee0	f65742a9	ldp	x22, x21, [sp, #0x20]
0x48ee4	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x48ee8	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x48eec	c0035fd6	ret
0x48ef0	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x48ef4	f65701a9	stp	x22, x21, [sp, #0x10]
0x48ef8	f44f02a9	stp	x20, x19, [sp, #0x20]
0x48efc	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x48f00	fdc30091	add	x29, sp, #0x30
0x48f04	f30301aa	mov	x19, x1
0x48f08	f40300aa	mov	x20, x0
0x48f0c	080040f9	ldr	x8, [x0]
0x48f10	085140f9	ldr	x8, [x8, #0xa0]
0x48f14	00013fd6	blr	x8
0x48f18	17008052	mov	w23, #0x0               ; =0
0x48f1c	800200b4	cbz	x0, 0x48f6c <_WeChatMain+0x2f700>
0x48f20	150080d2	mov	x21, #0x0               ; =0
0x48f24	18008012	mov	w24, #-0x1              ; =-1
0x48f28	880240f9	ldr	x8, [x20]
0x48f2c	084d40f9	ldr	x8, [x8, #0x98]
0x48f30	e00314aa	mov	x0, x20
0x48f34	e10315aa	mov	x1, x21
0x48f38	00013fd6	blr	x8
0x48f3c	f60300aa	mov	x22, x0
0x48f40	e8021f32	orr	w8, w23, #0x2
0x48f44	1f03006b	cmp	w24, w0
0x48f48	f7b2881a	csel	w23, w23, w8, lt
0x48f4c	b5060091	add	x21, x21, #0x1
0x48f50	880240f9	ldr	x8, [x20]
0x48f54	085140f9	ldr	x8, [x8, #0xa0]
0x48f58	e00314aa	mov	x0, x20
0x48f5c	00013fd6	blr	x8
0x48f60	f80316aa	mov	x24, x22
0x48f64	bf0200eb	cmp	x21, x0
0x48f68	03feff54	b.lo	0x48f28 <_WeChatMain+0x2f6bc>
0x48f6c	880e40f9	ldr	x8, [x20, #0x18]
0x48f70	001140f9	ldr	x0, [x8, #0x20]
0x48f74	66f5ff97	bl	0x4650c <_WeChatMain+0x2cca0>
0x48f78	08000052	eor	w8, w0, #0x1
0x48f7c	f402082a	orr	w20, w23, w8
0x48f80	680a40f9	ldr	x8, [x19, #0x10]
0x48f84	151140b9	ldr	w21, [x8, #0x10]
0x48f88	680240f9	ldr	x8, [x19]
0x48f8c	081140f9	ldr	x8, [x8, #0x20]
0x48f90	e00313aa	mov	x0, x19
0x48f94	00013fd6	blr	x8
0x48f98	a802006b	subs	w8, w21, w0
0x48f9c	20010054	b.eq	0x48fc0 <_WeChatMain+0x2f754>
0x48fa0	89021d32	orr	w9, w20, #0x8
0x48fa4	1f150031	cmn	w8, #0x5
0x48fa8	29b1941a	csel	w9, w9, w20, lt
0x48fac	8a021e32	orr	w10, w20, #0x4
0x48fb0	1f150071	cmp	w8, #0x5
0x48fb4	4a81941a	csel	w10, w10, w20, hi
0x48fb8	1f050071	cmp	w8, #0x1
0x48fbc	34b18a1a	csel	w20, w9, w10, lt
0x48fc0	e00314aa	mov	x0, x20
0x48fc4	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x48fc8	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x48fcc	f65741a9	ldp	x22, x21, [sp, #0x10]
0x48fd0	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x48fd4	c0035fd6	ret
0x48fd8	080c40f9	ldr	x8, [x0, #0x18]
0x48fdc	081140f9	ldr	x8, [x8, #0x20]
0x48fe0	080140f9	ldr	x8, [x8]
0x48fe4	007961b8	ldr	w0, [x8, x1, lsl #2]
0x48fe8	c0035fd6	ret
0x48fec	080c40f9	ldr	x8, [x0, #0x18]
0x48ff0	081140f9	ldr	x8, [x8, #0x20]
0x48ff4	082540a9	ldp	x8, x9, [x8]
0x48ff8	280108cb	sub	x8, x9, x8
0x48ffc	08fd4293	asr	x8, x8, #2
0x49000	000500d1	sub	x0, x8, #0x1
0x49004	c0035fd6	ret
0x49008	080c40f9	ldr	x8, [x0, #0x18]
0x4900c	080940f9	ldr	x8, [x8, #0x10]
0x49010	000140f9	ldr	x0, [x8]
0x49014	c0035fd6	ret
0x49018	00008052	mov	w0, #0x0                ; =0
0x4901c	c0035fd6	ret
0x49020	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x49024	f44f01a9	stp	x20, x19, [sp, #0x10]
0x49028	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4902c	fd830091	add	x29, sp, #0x20
0x49030	f60303aa	mov	x22, x3
0x49034	f30302aa	mov	x19, x2
0x49038	f40301aa	mov	x20, x1
0x4903c	f50300aa	mov	x21, x0
0x49040	080040f9	ldr	x8, [x0]
0x49044	085140f9	ldr	x8, [x8, #0xa0]
0x49048	00013fd6	blr	x8
0x4904c	1f0016eb	cmp	x0, x22
0x49050	a1020054	b.ne	0x490a4 <_WeChatMain+0x2f838>
0x49054	a80e40f9	ldr	x8, [x21, #0x18]
0x49058	081140f9	ldr	x8, [x8, #0x20]
0x4905c	082540a9	ldp	x8, x9, [x8]
0x49060	290108cb	sub	x9, x9, x8
0x49064	2afd4293	asr	x10, x9, #2
0x49068	4a0500d1	sub	x10, x10, #0x1
0x4906c	5f0500f1	cmp	x10, #0x1
0x49070	a8000054	b.hi	0x49084 <_WeChatMain+0x2f818>
0x49074	9f060031	cmn	w20, #0x1
0x49078	61010054	b.ne	0x490a4 <_WeChatMain+0x2f838>
0x4907c	08008012	mov	w8, #-0x1               ; =-1
0x49080	06000014	b	0x49098 <_WeChatMain+0x2f82c>
0x49084	0a0540b9	ldr	w10, [x8, #0x4]
0x49088	5f01146b	cmp	w10, w20
0x4908c	c1000054	b.ne	0x490a4 <_WeChatMain+0x2f838>
0x49090	0801098b	add	x8, x8, x9
0x49094	08815fb8	ldur	w8, [x8, #-0x8]
0x49098	1f01136b	cmp	w8, w19
0x4909c	e0179f1a	cset	w0, eq
0x490a0	02000014	b	0x490a8 <_WeChatMain+0x2f83c>
0x490a4	00008052	mov	w0, #0x0                ; =0
0x490a8	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x490ac	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x490b0	f657c3a8	ldp	x22, x21, [sp], #0x30
0x490b4	c0035fd6	ret
0x490b8	080040f9	ldr	x8, [x0]
0x490bc	031d40f9	ldr	x3, [x8, #0x38]
0x490c0	22008052	mov	w2, #0x1                ; =1
0x490c4	60001fd6	br	x3
0x490c8	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x490cc	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x490d0	fd430091	add	x29, sp, #0x10
0x490d4	082204b0	adrp	x8, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x490d8	08410091	add	x8, x8, #0x10
0x490dc	080140b9	ldr	w8, [x8]
0x490e0	09050051	sub	w9, w8, #0x1
0x490e4	1f01016b	cmp	w8, w1
0x490e8	28c0891a	csel	w8, w1, w9, gt
0x490ec	5f040071	cmp	w2, #0x1
0x490f0	8b010054	b.lt	0x49120 <_WeChatMain+0x2f8b4>
0x490f4	f30300aa	mov	x19, x0
0x490f8	147da80a	bic	w20, w8, w8, asr #31
0x490fc	000c40f9	ldr	x0, [x0, #0x18]
0x49100	080040f9	ldr	x8, [x0]
0x49104	080940f9	ldr	x8, [x8, #0x10]
0x49108	e10314aa	mov	x1, x20
0x4910c	00013fd6	blr	x8
0x49110	882605f0	adrp	x8, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x49114	08653091	add	x8, x8, #0xc19
0x49118	08014039	ldrb	w8, [x8]
0x4911c	88000037	tbnz	w8, #0x0, 0x4912c <_WeChatMain+0x2f8c0>
0x49120	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x49124	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x49128	c0035fd6	ret
0x4912c	e00313aa	mov	x0, x19
0x49130	e10314aa	mov	x1, x20
0x49134	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x49138	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4913c	07090014	b	0x4b558 <_WeChatMain+0x31cec>
0x49140	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x49144	f44f01a9	stp	x20, x19, [sp, #0x10]
0x49148	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4914c	fd830091	add	x29, sp, #0x20
0x49150	f30300aa	mov	x19, x0
0x49154	f40308aa	mov	x20, x8
0x49158	00088052	mov	w0, #0x40               ; =64
0x4915c	b5dbc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x49160	f50300aa	mov	x21, x0
0x49164	680e40f9	ldr	x8, [x19, #0x18]
0x49168	090940f9	ldr	x9, [x8, #0x10]
0x4916c	210140f9	ldr	x1, [x9]
0x49170	021140f9	ldr	x2, [x8, #0x20]
0x49174	8f200094	bl	0x513b0 <_WeChatMain+0x37b44>
0x49178	610e40f9	ldr	x1, [x19, #0x18]
0x4917c	080040f9	ldr	x8, [x0]
0x49180	081540f9	ldr	x8, [x8, #0x28]
0x49184	00013fd6	blr	x8
0x49188	611240f9	ldr	x1, [x19, #0x20]
0x4918c	a80240f9	ldr	x8, [x21]
0x49190	081540f9	ldr	x8, [x8, #0x28]
0x49194	e00315aa	mov	x0, x21
0x49198	00013fd6	blr	x8
0x4919c	950200f9	str	x21, [x20]
0x491a0	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x491a4	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x491a8	f657c3a8	ldp	x22, x21, [sp], #0x30
0x491ac	c0035fd6	ret
0x491b0	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x491b4	f44f01a9	stp	x20, x19, [sp, #0x10]
0x491b8	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x491bc	fd830091	add	x29, sp, #0x20
0x491c0	f30300aa	mov	x19, x0
0x491c4	f40308aa	mov	x20, x8
0x491c8	00088052	mov	w0, #0x40               ; =64
0x491cc	99dbc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x491d0	f50300aa	mov	x21, x0
0x491d4	680e40f9	ldr	x8, [x19, #0x18]
0x491d8	090940f9	ldr	x9, [x8, #0x10]
0x491dc	210140f9	ldr	x1, [x9]
0x491e0	021140f9	ldr	x2, [x8, #0x20]
0x491e4	73200094	bl	0x513b0 <_WeChatMain+0x37b44>
0x491e8	610e40f9	ldr	x1, [x19, #0x18]
0x491ec	080040f9	ldr	x8, [x0]
0x491f0	081540f9	ldr	x8, [x8, #0x28]
0x491f4	00013fd6	blr	x8
0x491f8	950200f9	str	x21, [x20]
0x491fc	600e40f9	ldr	x0, [x19, #0x18]
0x49200	080040f9	ldr	x8, [x0]
0x49204	081d40f9	ldr	x8, [x8, #0x38]
0x49208	e10315aa	mov	x1, x21
0x4920c	00013fd6	blr	x8
0x49210	601240f9	ldr	x0, [x19, #0x20]
0x49214	080040f9	ldr	x8, [x0]
0x49218	021540f9	ldr	x2, [x8, #0x28]
0x4921c	e10315aa	mov	x1, x21
0x49220	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x49224	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x49228	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4922c	40001fd6	br	x2
0x49230	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x49234	f44f01a9	stp	x20, x19, [sp, #0x10]
0x49238	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4923c	fd830091	add	x29, sp, #0x20
0x49240	f30300aa	mov	x19, x0
0x49244	f40308aa	mov	x20, x8
0x49248	00088052	mov	w0, #0x40               ; =64
0x4924c	79dbc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x49250	f50300aa	mov	x21, x0
0x49254	680e40f9	ldr	x8, [x19, #0x18]
0x49258	090940f9	ldr	x9, [x8, #0x10]
0x4925c	210140f9	ldr	x1, [x9]
0x49260	021140f9	ldr	x2, [x8, #0x20]
0x49264	53200094	bl	0x513b0 <_WeChatMain+0x37b44>
0x49268	610e40f9	ldr	x1, [x19, #0x18]
0x4926c	080040f9	ldr	x8, [x0]
0x49270	081540f9	ldr	x8, [x8, #0x28]
0x49274	00013fd6	blr	x8
0x49278	950200f9	str	x21, [x20]
0x4927c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x49280	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x49284	f657c3a8	ldp	x22, x21, [sp], #0x30
0x49288	c0035fd6	ret
0x4928c	000c40f9	ldr	x0, [x0, #0x18]
0x49290	080040f9	ldr	x8, [x0]
0x49294	021540f9	ldr	x2, [x8, #0x28]
0x49298	40001fd6	br	x2
0x4929c	000c40f9	ldr	x0, [x0, #0x18]
0x492a0	080040f9	ldr	x8, [x0]
0x492a4	021940f9	ldr	x2, [x8, #0x30]
0x492a8	40001fd6	br	x2
0x492ac	ff0301d1	sub	sp, sp, #0x40
0x492b0	f65701a9	stp	x22, x21, [sp, #0x10]
0x492b4	f44f02a9	stp	x20, x19, [sp, #0x20]
0x492b8	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x492bc	fdc30091	add	x29, sp, #0x30
0x492c0	f50300aa	mov	x21, x0
0x492c4	f40308aa	mov	x20, x8
0x492c8	00088052	mov	w0, #0x40               ; =64
0x492cc	59dbc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x492d0	f30300aa	mov	x19, x0
0x492d4	a80e40f9	ldr	x8, [x21, #0x18]
0x492d8	090940f9	ldr	x9, [x8, #0x10]
0x492dc	210140f9	ldr	x1, [x9]
0x492e0	021140f9	ldr	x2, [x8, #0x20]
0x492e4	33200094	bl	0x513b0 <_WeChatMain+0x37b44>
0x492e8	a10e40f9	ldr	x1, [x21, #0x18]
0x492ec	080040f9	ldr	x8, [x0]
0x492f0	081540f9	ldr	x8, [x8, #0x28]
0x492f4	00013fd6	blr	x8
0x492f8	a11240f9	ldr	x1, [x21, #0x20]
0x492fc	680240f9	ldr	x8, [x19]
0x49300	081540f9	ldr	x8, [x8, #0x28]
0x49304	e00313aa	mov	x0, x19
0x49308	00013fd6	blr	x8
0x4930c	b60640f9	ldr	x22, [x21, #0x8]
0x49310	b60000b4	cbz	x22, 0x49324 <_WeChatMain+0x2fab8>
0x49314	e00316aa	mov	x0, x22
0x49318	b8e1c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4931c	e20300aa	mov	x2, x0
0x49320	0b000014	b	0x4934c <_WeChatMain+0x2fae0>
0x49324	80bf04f0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x49328	00800791	add	x0, x0, #0x1e0
0x4932c	82bf04f0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x49330	42300991	add	x2, x2, #0x24c
0x49334	e8230091	add	x8, sp, #0x8
0x49338	a10f8052	mov	w1, #0x7d               ; =125
0x4933c	e260ff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x49340	e0230091	add	x0, sp, #0x8
0x49344	4a45ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x49348	020080d2	mov	x2, #0x0                ; =0
0x4934c	a31240b9	ldr	w3, [x21, #0x10]
0x49350	e80314aa	mov	x8, x20
0x49354	e00313aa	mov	x0, x19
0x49358	e10316aa	mov	x1, x22
0x4935c	8e0c0094	bl	0x4c594 <_WeChatMain+0x32d28>
0x49360	b30000b4	cbz	x19, 0x49374 <_WeChatMain+0x2fb08>
0x49364	680240f9	ldr	x8, [x19]
0x49368	080540f9	ldr	x8, [x8, #0x8]
0x4936c	e00313aa	mov	x0, x19
0x49370	00013fd6	blr	x8
0x49374	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x49378	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4937c	f65741a9	ldp	x22, x21, [sp, #0x10]
0x49380	ff030191	add	sp, sp, #0x40
0x49384	c0035fd6	ret
0x49388	ff0301d1	sub	sp, sp, #0x40
0x4938c	f44f02a9	stp	x20, x19, [sp, #0x20]
0x49390	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x49394	fdc30091	add	x29, sp, #0x30
0x49398	f30301aa	mov	x19, x1
0x4939c	f40300aa	mov	x20, x0
0x493a0	000440f9	ldr	x0, [x0, #0x8]
0x493a4	e00700f9	str	x0, [sp, #0x8]
0x493a8	800000b4	cbz	x0, 0x493b8 <_WeChatMain+0x2fb4c>
0x493ac	93e1c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x493b0	e00b00f9	str	x0, [sp, #0x10]
0x493b4	0b000014	b	0x493e0 <_WeChatMain+0x2fb74>
0x493b8	ff0b00f9	str	xzr, [sp, #0x10]
0x493bc	80bf04f0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x493c0	00800791	add	x0, x0, #0x1e0
0x493c4	82bf04f0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x493c8	42300991	add	x2, x2, #0x24c
0x493cc	e8630091	add	x8, sp, #0x18
0x493d0	a10f8052	mov	w1, #0x7d               ; =125
0x493d4	bc60ff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x493d8	e0630091	add	x0, sp, #0x18
0x493dc	2445ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x493e0	e1230091	add	x1, sp, #0x8
0x493e4	e00313aa	mov	x0, x19
0x493e8	0d3c0094	bl	0x5841c <_WeChatMain+0x3ebb0>
0x493ec	881240b9	ldr	w8, [x20, #0x10]
0x493f0	e80b00b9	str	w8, [sp, #0x8]
0x493f4	e1230091	add	x1, sp, #0x8
0x493f8	e00313aa	mov	x0, x19
0x493fc	43390094	bl	0x57908 <_WeChatMain+0x3e09c>
0x49400	880e40f9	ldr	x8, [x20, #0x18]
0x49404	081140f9	ldr	x8, [x8, #0x20]
0x49408	082540a9	ldp	x8, x9, [x8]
0x4940c	290108cb	sub	x9, x9, x8
0x49410	29fd4293	asr	x9, x9, #2
0x49414	290500d1	sub	x9, x9, #0x1
0x49418	3f0900f1	cmp	x9, #0x2
0x4941c	62000054	b.hs	0x49428 <_WeChatMain+0x2fbbc>
0x49420	08008012	mov	w8, #-0x1               ; =-1
0x49424	02000014	b	0x4942c <_WeChatMain+0x2fbc0>
0x49428	080540b9	ldr	w8, [x8, #0x4]
0x4942c	e80b00b9	str	w8, [sp, #0x8]
0x49430	e1230091	add	x1, sp, #0x8
0x49434	e00313aa	mov	x0, x19
0x49438	34390094	bl	0x57908 <_WeChatMain+0x3e09c>
0x4943c	880e40f9	ldr	x8, [x20, #0x18]
0x49440	081140f9	ldr	x8, [x8, #0x20]
0x49444	082540a9	ldp	x8, x9, [x8]
0x49448	290108cb	sub	x9, x9, x8
0x4944c	2afd4293	asr	x10, x9, #2
0x49450	4a0500d1	sub	x10, x10, #0x1
0x49454	5f0900f1	cmp	x10, #0x2
0x49458	62000054	b.hs	0x49464 <_WeChatMain+0x2fbf8>
0x4945c	08008012	mov	w8, #-0x1               ; =-1
0x49460	03000014	b	0x4946c <_WeChatMain+0x2fc00>
0x49464	0801098b	add	x8, x8, x9
0x49468	08815fb8	ldur	w8, [x8, #-0x8]
0x4946c	e80b00b9	str	w8, [sp, #0x8]
0x49470	e1230091	add	x1, sp, #0x8
0x49474	e00313aa	mov	x0, x19
0x49478	24390094	bl	0x57908 <_WeChatMain+0x3e09c>
0x4947c	880240f9	ldr	x8, [x20]
0x49480	085140f9	ldr	x8, [x8, #0xa0]
0x49484	e00314aa	mov	x0, x20
0x49488	00013fd6	blr	x8
0x4948c	e00b00b9	str	w0, [sp, #0x8]
0x49490	e1230091	add	x1, sp, #0x8
0x49494	e00313aa	mov	x0, x19
0x49498	1c390094	bl	0x57908 <_WeChatMain+0x3e09c>
0x4949c	880e40f9	ldr	x8, [x20, #0x18]
0x494a0	081140f9	ldr	x8, [x8, #0x20]
0x494a4	081940b9	ldr	w8, [x8, #0x18]
0x494a8	e80b00b9	str	w8, [sp, #0x8]
0x494ac	e1230091	add	x1, sp, #0x8
0x494b0	e00313aa	mov	x0, x19
0x494b4	15390094	bl	0x57908 <_WeChatMain+0x3e09c>
0x494b8	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x494bc	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x494c0	ff030191	add	sp, sp, #0x40
0x494c4	c0035fd6	ret
0x494c8	ff0301d1	sub	sp, sp, #0x40
0x494cc	f65701a9	stp	x22, x21, [sp, #0x10]
0x494d0	f44f02a9	stp	x20, x19, [sp, #0x20]
0x494d4	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x494d8	fdc30091	add	x29, sp, #0x30
0x494dc	f40302aa	mov	x20, x2
0x494e0	f50301aa	mov	x21, x1
0x494e4	f30300aa	mov	x19, x0
0x494e8	f9070094	bl	0x4b4cc <_WeChatMain+0x31c60>
0x494ec	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x494f0	08e13591	add	x8, x8, #0xd78
0x494f4	080000f9	str	x8, [x0]
0x494f8	f60300aa	mov	x22, x0
0x494fc	df8e01f8	str	xzr, [x22, #0x18]!
0x49500	1f1000f9	str	xzr, [x0, #0x20]
0x49504	b50000b4	cbz	x21, 0x49518 <_WeChatMain+0x2fcac>
0x49508	e00315aa	mov	x0, x21
0x4950c	3be1c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x49510	e10300aa	mov	x1, x0
0x49514	0b000014	b	0x49540 <_WeChatMain+0x2fcd4>
0x49518	80bf04f0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x4951c	00800791	add	x0, x0, #0x1e0
0x49520	82bf04f0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x49524	42300991	add	x2, x2, #0x24c
0x49528	e8230091	add	x8, sp, #0x8
0x4952c	a10f8052	mov	w1, #0x7d               ; =125
0x49530	6560ff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x49534	e0230091	add	x0, sp, #0x8
0x49538	cd44ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x4953c	010080d2	mov	x1, #0x0                ; =0
0x49540	e00315aa	mov	x0, x21
0x49544	370f0094	bl	0x4d220 <_WeChatMain+0x339b4>
0x49548	f50300aa	mov	x21, x0
0x4954c	00088052	mov	w0, #0x40               ; =64
0x49550	b8dac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x49554	e10315aa	mov	x1, x21
0x49558	e20314aa	mov	x2, x20
0x4955c	951f0094	bl	0x513b0 <_WeChatMain+0x37b44>
0x49560	c80240f9	ldr	x8, [x22]
0x49564	c00200f9	str	x0, [x22]
0x49568	c80000b4	cbz	x8, 0x49580 <_WeChatMain+0x2fd14>
0x4956c	090140f9	ldr	x9, [x8]
0x49570	290540f9	ldr	x9, [x9, #0x8]
0x49574	e00308aa	mov	x0, x8
0x49578	20013fd6	blr	x9
0x4957c	c00240f9	ldr	x0, [x22]
0x49580	080840f9	ldr	x8, [x0, #0x10]
0x49584	150140f9	ldr	x21, [x8]
0x49588	00088052	mov	w0, #0x40               ; =64
0x4958c	a9dac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x49590	f60300aa	mov	x22, x0
0x49594	e10315aa	mov	x1, x21
0x49598	e20314aa	mov	x2, x20
0x4959c	851f0094	bl	0x513b0 <_WeChatMain+0x37b44>
0x495a0	601240f9	ldr	x0, [x19, #0x20]
0x495a4	761200f9	str	x22, [x19, #0x20]
0x495a8	800000b4	cbz	x0, 0x495b8 <_WeChatMain+0x2fd4c>
0x495ac	080040f9	ldr	x8, [x0]
0x495b0	080540f9	ldr	x8, [x8, #0x8]
0x495b4	00013fd6	blr	x8
0x495b8	e00313aa	mov	x0, x19
0x495bc	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x495c0	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x495c4	f65741a9	ldp	x22, x21, [sp, #0x10]
0x495c8	ff030191	add	sp, sp, #0x40
0x495cc	c0035fd6	ret
0x495d0	ff8301d1	sub	sp, sp, #0x60
0x495d4	fa6701a9	stp	x26, x25, [sp, #0x10]
0x495d8	f85f02a9	stp	x24, x23, [sp, #0x20]
0x495dc	f65703a9	stp	x22, x21, [sp, #0x30]
0x495e0	f44f04a9	stp	x20, x19, [sp, #0x40]
0x495e4	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x495e8	fd430191	add	x29, sp, #0x50
0x495ec	f40306aa	mov	x20, x6
0x495f0	f70305aa	mov	x23, x5
0x495f4	f50304aa	mov	x21, x4
0x495f8	f80303aa	mov	x24, x3
0x495fc	f60302aa	mov	x22, x2
0x49600	f90301aa	mov	x25, x1
0x49604	f30300aa	mov	x19, x0
0x49608	b1070094	bl	0x4b4cc <_WeChatMain+0x31c60>
0x4960c	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x49610	08e13591	add	x8, x8, #0xd78
0x49614	080000f9	str	x8, [x0]
0x49618	fa0300aa	mov	x26, x0
0x4961c	5f8f01f8	str	xzr, [x26, #0x18]!
0x49620	1f1000f9	str	xzr, [x0, #0x20]
0x49624	b90000b4	cbz	x25, 0x49638 <_WeChatMain+0x2fdcc>
0x49628	e00319aa	mov	x0, x25
0x4962c	f3e0c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x49630	e10300aa	mov	x1, x0
0x49634	0b000014	b	0x49660 <_WeChatMain+0x2fdf4>
0x49638	80bf04f0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x4963c	00800791	add	x0, x0, #0x1e0
0x49640	82bf04f0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x49644	42300991	add	x2, x2, #0x24c
0x49648	e8230091	add	x8, sp, #0x8
0x4964c	a10f8052	mov	w1, #0x7d               ; =125
0x49650	1d60ff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x49654	e0230091	add	x0, sp, #0x8
0x49658	8544ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x4965c	010080d2	mov	x1, #0x0                ; =0
0x49660	e00319aa	mov	x0, x25
0x49664	ef0e0094	bl	0x4d220 <_WeChatMain+0x339b4>
0x49668	f90300aa	mov	x25, x0
0x4966c	00098052	mov	w0, #0x48               ; =72
0x49670	70dac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x49674	e10319aa	mov	x1, x25
0x49678	e20316aa	mov	x2, x22
0x4967c	e30317aa	mov	x3, x23
0x49680	e40318aa	mov	x4, x24
0x49684	0b220094	bl	0x51eb0 <_WeChatMain+0x38644>
0x49688	480340f9	ldr	x8, [x26]
0x4968c	400300f9	str	x0, [x26]
0x49690	c80000b4	cbz	x8, 0x496a8 <_WeChatMain+0x2fe3c>
0x49694	090140f9	ldr	x9, [x8]
0x49698	290540f9	ldr	x9, [x9, #0x8]
0x4969c	e00308aa	mov	x0, x8
0x496a0	20013fd6	blr	x9
0x496a4	400340f9	ldr	x0, [x26]
0x496a8	080840f9	ldr	x8, [x0, #0x10]
0x496ac	170140f9	ldr	x23, [x8]
0x496b0	00098052	mov	w0, #0x48               ; =72
0x496b4	5fdac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x496b8	f80300aa	mov	x24, x0
0x496bc	e10317aa	mov	x1, x23
0x496c0	e20316aa	mov	x2, x22
0x496c4	e30314aa	mov	x3, x20
0x496c8	e40315aa	mov	x4, x21
0x496cc	f9210094	bl	0x51eb0 <_WeChatMain+0x38644>
0x496d0	601240f9	ldr	x0, [x19, #0x20]
0x496d4	781200f9	str	x24, [x19, #0x20]
0x496d8	800000b4	cbz	x0, 0x496e8 <_WeChatMain+0x2fe7c>
0x496dc	080040f9	ldr	x8, [x0]
0x496e0	080540f9	ldr	x8, [x8, #0x8]
0x496e4	00013fd6	blr	x8
0x496e8	e00313aa	mov	x0, x19
0x496ec	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x496f0	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x496f4	f65743a9	ldp	x22, x21, [sp, #0x30]
0x496f8	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x496fc	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x49700	ff830191	add	sp, sp, #0x60
0x49704	c0035fd6	ret
0x49708	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4970c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x49710	fd430091	add	x29, sp, #0x10
0x49714	f30300aa	mov	x19, x0
0x49718	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4971c	08e13591	add	x8, x8, #0xd78
0x49720	080000f9	str	x8, [x0]
0x49724	001040f9	ldr	x0, [x0, #0x20]
0x49728	7f1200f9	str	xzr, [x19, #0x20]
0x4972c	800000b4	cbz	x0, 0x4973c <_WeChatMain+0x2fed0>
0x49730	080040f9	ldr	x8, [x0]
0x49734	080540f9	ldr	x8, [x8, #0x8]
0x49738	00013fd6	blr	x8
0x4973c	600e40f9	ldr	x0, [x19, #0x18]
0x49740	7f0e00f9	str	xzr, [x19, #0x18]
0x49744	800000b4	cbz	x0, 0x49754 <_WeChatMain+0x2fee8>
0x49748	080040f9	ldr	x8, [x0]
0x4974c	080540f9	ldr	x8, [x8, #0x8]
0x49750	00013fd6	blr	x8
0x49754	e00313aa	mov	x0, x19
0x49758	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4975c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x49760	5b45ff17	b	0x1accc <_WeChatMain+0x1460>
0x49764	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x49768	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4976c	fd430091	add	x29, sp, #0x10
0x49770	f30300aa	mov	x19, x0
0x49774	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x49778	08e13591	add	x8, x8, #0xd78
0x4977c	080000f9	str	x8, [x0]
0x49780	001040f9	ldr	x0, [x0, #0x20]
0x49784	7f1200f9	str	xzr, [x19, #0x20]
0x49788	800000b4	cbz	x0, 0x49798 <_WeChatMain+0x2ff2c>
0x4978c	080040f9	ldr	x8, [x0]
0x49790	080540f9	ldr	x8, [x8, #0x8]
0x49794	00013fd6	blr	x8
0x49798	600e40f9	ldr	x0, [x19, #0x18]
0x4979c	7f0e00f9	str	xzr, [x19, #0x18]
0x497a0	800000b4	cbz	x0, 0x497b0 <_WeChatMain+0x2ff44>
0x497a4	080040f9	ldr	x8, [x0]
0x497a8	080540f9	ldr	x8, [x8, #0x8]
0x497ac	00013fd6	blr	x8
0x497b0	e00313aa	mov	x0, x19
0x497b4	4645ff97	bl	0x1accc <_WeChatMain+0x1460>
0x497b8	01058052	mov	w1, #0x28               ; =40
0x497bc	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x497c0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x497c4	12dac315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x497c8	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x497cc	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x497d0	fd430091	add	x29, sp, #0x10
0x497d4	f30300aa	mov	x19, x0
0x497d8	f40308aa	mov	x20, x8
0x497dc	080040f9	ldr	x8, [x0]
0x497e0	084d40f9	ldr	x8, [x8, #0x98]
0x497e4	00013fd6	blr	x8
0x497e8	e10300aa	mov	x1, x0
0x497ec	e80314aa	mov	x8, x20
0x497f0	e00313aa	mov	x0, x19
0x497f4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x497f8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x497fc	7a070014	b	0x4b5e4 <_WeChatMain+0x31d78>
0x49800	ff4301d1	sub	sp, sp, #0x50
0x49804	f65702a9	stp	x22, x21, [sp, #0x20]
0x49808	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4980c	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x49810	fd030191	add	x29, sp, #0x40
0x49814	f40300aa	mov	x20, x0
0x49818	f30308aa	mov	x19, x8
0x4981c	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x49820	68a200a9	stp	x8, x8, [x19, #0x8]
0x49824	680200f9	str	x8, [x19]
0x49828	e00313aa	mov	x0, x19
0x4982c	a586ff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x49830	481005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x49834	09354b39	ldrb	w9, [x8, #0x2cd]
0x49838	29010037	tbnz	w9, #0x0, 0x4985c <_WeChatMain+0x2fff0>
0x4983c	09220490	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x49840	20c543fd	ldr	d0, [x9, #0x788]
0x49844	491005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x49848	29210b91	add	x9, x9, #0x2c8
0x4984c	200100bd	str	s0, [x9]
0x49850	3f110039	strb	wzr, [x9, #0x4]
0x49854	29008052	mov	w9, #0x1                ; =1
0x49858	09350b39	strb	w9, [x8, #0x2cd]
0x4985c	551005b0	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x49860	b5220b91	add	x21, x21, #0x2c8
0x49864	e00315aa	mov	x0, x21
0x49868	64e0c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4986c	f60300aa	mov	x22, x0
0x49870	880240f9	ldr	x8, [x20]
0x49874	081140f9	ldr	x8, [x8, #0x20]
0x49878	e00314aa	mov	x0, x20
0x4987c	00013fd6	blr	x8
0x49880	e8230091	add	x8, sp, #0x8
0x49884	f5050094	bl	0x4b058 <_WeChatMain+0x317ec>
0x49888	e3230091	add	x3, sp, #0x8
0x4988c	e00313aa	mov	x0, x19
0x49890	e10315aa	mov	x1, x21
0x49894	e20316aa	mov	x2, x22
0x49898	75780194	bl	0xa7a6c <_WeChatMain+0x8e200>
0x4989c	e87fc039	ldrsb	w8, [sp, #0x1f]
0x498a0	a800f836	tbz	w8, #0x1f, 0x498b4 <_WeChatMain+0x30048>
0x498a4	e00740f9	ldr	x0, [sp, #0x8]
0x498a8	e80f40f9	ldr	x8, [sp, #0x18]
0x498ac	01f94092	and	x1, x8, #0x7fffffffffffffff
0x498b0	d7d9c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x498b4	481005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x498b8	09514b39	ldrb	w9, [x8, #0x2d4]
0x498bc	e9000037	tbnz	w9, #0x0, 0x498d8 <_WeChatMain+0x3006c>
0x498c0	e9210490	adrp	x9, 0x8485000 <_wxam_enc_uninit_10+0x8485000>
0x498c4	20b941fd	ldr	d0, [x9, #0x370]
0x498c8	491005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x498cc	20d102bd	str	s0, [x9, #0x2d0]
0x498d0	29008052	mov	w9, #0x1                ; =1
0x498d4	09510b39	strb	w9, [x8, #0x2d4]
0x498d8	401005b0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x498dc	00400b91	add	x0, x0, #0x2d0
0x498e0	46e0c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x498e4	e20300aa	mov	x2, x0
0x498e8	880e40f9	ldr	x8, [x20, #0x18]
0x498ec	081140f9	ldr	x8, [x8, #0x20]
0x498f0	082540a9	ldp	x8, x9, [x8]
0x498f4	290108cb	sub	x9, x9, x8
0x498f8	29fd4293	asr	x9, x9, #2
0x498fc	290500d1	sub	x9, x9, #0x1
0x49900	3f0900f1	cmp	x9, #0x2
0x49904	62000054	b.hs	0x49910 <_WeChatMain+0x300a4>
0x49908	03008012	mov	w3, #-0x1               ; =-1
0x4990c	02000014	b	0x49914 <_WeChatMain+0x300a8>
0x49910	030540b9	ldr	w3, [x8, #0x4]
0x49914	411005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x49918	21400b91	add	x1, x1, #0x2d0
0x4991c	e00313aa	mov	x0, x19
0x49920	a8770194	bl	0xa77c0 <_WeChatMain+0x8df54>
0x49924	481005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x49928	09714b39	ldrb	w9, [x8, #0x2dc]
0x4992c	e9000037	tbnz	w9, #0x0, 0x49948 <_WeChatMain+0x300dc>
0x49930	09220490	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x49934	20c943fd	ldr	d0, [x9, #0x790]
0x49938	491005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4993c	20d902bd	str	s0, [x9, #0x2d8]
0x49940	29008052	mov	w9, #0x1                ; =1
0x49944	09710b39	strb	w9, [x8, #0x2dc]
0x49948	401005b0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4994c	00600b91	add	x0, x0, #0x2d8
0x49950	2ae0c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x49954	e20300aa	mov	x2, x0
0x49958	880e40f9	ldr	x8, [x20, #0x18]
0x4995c	081140f9	ldr	x8, [x8, #0x20]
0x49960	082540a9	ldp	x8, x9, [x8]
0x49964	290108cb	sub	x9, x9, x8
0x49968	2afd4293	asr	x10, x9, #2
0x4996c	4a0500d1	sub	x10, x10, #0x1
0x49970	5f0900f1	cmp	x10, #0x2
0x49974	62000054	b.hs	0x49980 <_WeChatMain+0x30114>
0x49978	03008012	mov	w3, #-0x1               ; =-1
0x4997c	03000014	b	0x49988 <_WeChatMain+0x3011c>
0x49980	0801098b	add	x8, x8, x9
0x49984	03815fb8	ldur	w3, [x8, #-0x8]
0x49988	411005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4998c	21600b91	add	x1, x1, #0x2d8
0x49990	e00313aa	mov	x0, x19
0x49994	8b770194	bl	0xa77c0 <_WeChatMain+0x8df54>
0x49998	481005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4999c	09b54b39	ldrb	w9, [x8, #0x2ed]
0x499a0	89010037	tbnz	w9, #0x0, 0x499d0 <_WeChatMain+0x30164>
0x499a4	09220490	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x499a8	20cd43fd	ldr	d0, [x9, #0x798]
0x499ac	491005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x499b0	29810b91	add	x9, x9, #0x2e0
0x499b4	200100fd	str	d0, [x9]
0x499b8	aa2104f0	adrp	x10, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x499bc	40a545fd	ldr	d0, [x10, #0xb48]
0x499c0	200900bd	str	s0, [x9, #0x8]
0x499c4	3f310039	strb	wzr, [x9, #0xc]
0x499c8	29008052	mov	w9, #0x1                ; =1
0x499cc	09b50b39	strb	w9, [x8, #0x2ed]
0x499d0	551005b0	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x499d4	b5820b91	add	x21, x21, #0x2e0
0x499d8	e00315aa	mov	x0, x21
0x499dc	07e0c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x499e0	f60300aa	mov	x22, x0
0x499e4	880240f9	ldr	x8, [x20]
0x499e8	085140f9	ldr	x8, [x8, #0xa0]
0x499ec	e00314aa	mov	x0, x20
0x499f0	00013fd6	blr	x8
0x499f4	e30300aa	mov	x3, x0
0x499f8	e00313aa	mov	x0, x19
0x499fc	e10315aa	mov	x1, x21
0x49a00	e20316aa	mov	x2, x22
0x49a04	6f770194	bl	0xa77c0 <_WeChatMain+0x8df54>
0x49a08	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x49a0c	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x49a10	f65742a9	ldp	x22, x21, [sp, #0x20]
0x49a14	ff430191	add	sp, sp, #0x50
0x49a18	c0035fd6	ret
0x49a1c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x49a20	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x49a24	fd430091	add	x29, sp, #0x10
0x49a28	f30300aa	mov	x19, x0
0x49a2c	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x49a30	08e13891	add	x8, x8, #0xe38
0x49a34	080000f9	str	x8, [x0]
0x49a38	011840f9	ldr	x1, [x0, #0x30]
0x49a3c	00a00091	add	x0, x0, #0x28
0x49a40	7377ff97	bl	0x2780c <_WeChatMain+0xdfa0>
0x49a44	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x49a48	08e13591	add	x8, x8, #0xd78
0x49a4c	680200f9	str	x8, [x19]
0x49a50	601240f9	ldr	x0, [x19, #0x20]
0x49a54	7f1200f9	str	xzr, [x19, #0x20]
0x49a58	800000b4	cbz	x0, 0x49a68 <_WeChatMain+0x301fc>
0x49a5c	080040f9	ldr	x8, [x0]
0x49a60	080540f9	ldr	x8, [x8, #0x8]
0x49a64	00013fd6	blr	x8
0x49a68	600e40f9	ldr	x0, [x19, #0x18]
0x49a6c	7f0e00f9	str	xzr, [x19, #0x18]
0x49a70	800000b4	cbz	x0, 0x49a80 <_WeChatMain+0x30214>
0x49a74	080040f9	ldr	x8, [x0]
0x49a78	080540f9	ldr	x8, [x8, #0x8]
0x49a7c	00013fd6	blr	x8
0x49a80	e00313aa	mov	x0, x19
0x49a84	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x49a88	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x49a8c	9044ff17	b	0x1accc <_WeChatMain+0x1460>
0x49a90	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x49a94	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x49a98	fd430091	add	x29, sp, #0x10
0x49a9c	f30300aa	mov	x19, x0
0x49aa0	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x49aa4	08e13891	add	x8, x8, #0xe38
0x49aa8	080000f9	str	x8, [x0]
0x49aac	011840f9	ldr	x1, [x0, #0x30]
0x49ab0	00a00091	add	x0, x0, #0x28
0x49ab4	5677ff97	bl	0x2780c <_WeChatMain+0xdfa0>
0x49ab8	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x49abc	08e13591	add	x8, x8, #0xd78
0x49ac0	680200f9	str	x8, [x19]
0x49ac4	601240f9	ldr	x0, [x19, #0x20]
0x49ac8	7f1200f9	str	xzr, [x19, #0x20]
0x49acc	800000b4	cbz	x0, 0x49adc <_WeChatMain+0x30270>
0x49ad0	080040f9	ldr	x8, [x0]
0x49ad4	080540f9	ldr	x8, [x8, #0x8]
0x49ad8	00013fd6	blr	x8
0x49adc	600e40f9	ldr	x0, [x19, #0x18]
0x49ae0	7f0e00f9	str	xzr, [x19, #0x18]
0x49ae4	800000b4	cbz	x0, 0x49af4 <_WeChatMain+0x30288>
0x49ae8	080040f9	ldr	x8, [x0]
0x49aec	080540f9	ldr	x8, [x8, #0x8]
0x49af0	00013fd6	blr	x8
0x49af4	e00313aa	mov	x0, x19
0x49af8	7544ff97	bl	0x1accc <_WeChatMain+0x1460>
0x49afc	01088052	mov	w1, #0x40               ; =64
0x49b00	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x49b04	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x49b08	41d9c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x49b0c	ff8302d1	sub	sp, sp, #0xa0
0x49b10	fa6705a9	stp	x26, x25, [sp, #0x50]
0x49b14	f85f06a9	stp	x24, x23, [sp, #0x60]
0x49b18	f65707a9	stp	x22, x21, [sp, #0x70]
0x49b1c	f44f08a9	stp	x20, x19, [sp, #0x80]
0x49b20	fd7b09a9	stp	x29, x30, [sp, #0x90]
0x49b24	fd430291	add	x29, sp, #0x90
0x49b28	f30305aa	mov	x19, x5
0x49b2c	f40304aa	mov	x20, x4
0x49b30	f50300aa	mov	x21, x0
0x49b34	a1c31bb8	stur	w1, [x29, #-0x44]
0x49b38	e24b00b9	str	w2, [sp, #0x48]
0x49b3c	e32300f9	str	x3, [sp, #0x40]
0x49b40	5f040071	cmp	w2, #0x1
0x49b44	e1000054	b.ne	0x49b60 <_WeChatMain+0x302f4>
0x49b48	7f0800f1	cmp	x3, #0x2
0x49b4c	a1000054	b.ne	0x49b60 <_WeChatMain+0x302f4>
0x49b50	48008052	mov	w8, #0x2                ; =2
0x49b54	e84b00b9	str	w8, [sp, #0x48]
0x49b58	68008052	mov	w8, #0x3                ; =3
0x49b5c	e82300f9	str	x8, [sp, #0x40]
0x49b60	a85e8039	ldrsb	x8, [x21, #0x17]
0x49b64	a92a40a9	ldp	x9, x10, [x21]
0x49b68	1f0100f1	cmp	x8, #0x0
0x49b6c	20b1959a	csel	x0, x9, x21, lt
0x49b70	1f010071	cmp	w8, #0x0
0x49b74	41b1889a	csel	x1, x10, x8, lt
0x49b78	a21301d1	sub	x2, x29, #0x44
0x49b7c	e3230191	add	x3, sp, #0x48
0x49b80	e4030191	add	x4, sp, #0x40
0x49b84	8bfbff97	bl	0x489b0 <_WeChatMain+0x2f144>
0x49b88	e0060036	tbz	w0, #0x0, 0x49c64 <_WeChatMain+0x303f8>
0x49b8c	b7c35bb8	ldur	w23, [x29, #-0x44]
0x49b90	f84b40b9	ldr	w24, [sp, #0x48]
0x49b94	f92340f9	ldr	x25, [sp, #0x40]
0x49b98	a8765e92	and	x8, x21, #0xfffffffc00000000
0x49b9c	96fd04b0	adrp	x22, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x49ba0	d6023b91	add	x22, x22, #0xec0
0x49ba4	c90640f9	ldr	x9, [x22, #0x8]
0x49ba8	1f0109eb	cmp	x8, x9
0x49bac	61000054	b.ne	0x49bb8 <_WeChatMain+0x3034c>
0x49bb0	e00315aa	mov	x0, x21
0x49bb4	26d7ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x49bb8	28008052	mov	w8, #0x1                ; =1
0x49bbc	e85f0329	stp	w8, w23, [sp, #0x18]
0x49bc0	f82300b9	str	w24, [sp, #0x20]
0x49bc4	f91700f9	str	x25, [sp, #0x28]
0x49bc8	97d70490	adrp	x23, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x49bcc	f7420491	add	x23, x23, #0x110
0x49bd0	f43300b9	str	w20, [sp, #0x30]
0x49bd4	f7d700a9	stp	x23, x21, [sp, #0x8]
0x49bd8	68765e92	and	x8, x19, #0xfffffffc00000000
0x49bdc	c90640f9	ldr	x9, [x22, #0x8]
0x49be0	1f0109eb	cmp	x8, x9
0x49be4	61000054	b.ne	0x49bf0 <_WeChatMain+0x30384>
0x49be8	e00313aa	mov	x0, x19
0x49bec	18d7ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x49bf0	f31f00f9	str	x19, [sp, #0x38]
0x49bf4	e0230091	add	x0, sp, #0x8
0x49bf8	97f9ff97	bl	0x48254 <_WeChatMain+0x2e9e8>
0x49bfc	f30300aa	mov	x19, x0
0x49c00	f70700f9	str	x23, [sp, #0x8]
0x49c04	e01f40f9	ldr	x0, [sp, #0x38]
0x49c08	08745e92	and	x8, x0, #0xfffffffc00000000
0x49c0c	c90640f9	ldr	x9, [x22, #0x8]
0x49c10	1f0109eb	cmp	x8, x9
0x49c14	41000054	b.ne	0x49c1c <_WeChatMain+0x303b0>
0x49c18	aad7ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x49c1c	88d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x49c20	08610391	add	x8, x8, #0xd8
0x49c24	ff1f00f9	str	xzr, [sp, #0x38]
0x49c28	e80700f9	str	x8, [sp, #0x8]
0x49c2c	e00b40f9	ldr	x0, [sp, #0x10]
0x49c30	08745e92	and	x8, x0, #0xfffffffc00000000
0x49c34	c90640f9	ldr	x9, [x22, #0x8]
0x49c38	1f0109eb	cmp	x8, x9
0x49c3c	41000054	b.ne	0x49c44 <_WeChatMain+0x303d8>
0x49c40	a0d7ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x49c44	e00313aa	mov	x0, x19
0x49c48	fd7b49a9	ldp	x29, x30, [sp, #0x90]
0x49c4c	f44f48a9	ldp	x20, x19, [sp, #0x80]
0x49c50	f65747a9	ldp	x22, x21, [sp, #0x70]
0x49c54	f85f46a9	ldp	x24, x23, [sp, #0x60]
0x49c58	fa6745a9	ldp	x26, x25, [sp, #0x50]
0x49c5c	ff830291	add	sp, sp, #0xa0
0x49c60	c0035fd6	ret
0x49c64	fd7b49a9	ldp	x29, x30, [sp, #0x90]
0x49c68	f44f48a9	ldp	x20, x19, [sp, #0x80]
0x49c6c	f65747a9	ldp	x22, x21, [sp, #0x70]
0x49c70	f85f46a9	ldp	x24, x23, [sp, #0x60]
0x49c74	fa6745a9	ldp	x26, x25, [sp, #0x50]
0x49c78	ff830291	add	sp, sp, #0xa0
0x49c7c	75f2ff17	b	0x46650 <_WeChatMain+0x2cde4>
0x49c80	ffc301d1	sub	sp, sp, #0x70
0x49c84	fa6702a9	stp	x26, x25, [sp, #0x20]
0x49c88	f85f03a9	stp	x24, x23, [sp, #0x30]
0x49c8c	f65704a9	stp	x22, x21, [sp, #0x40]
0x49c90	f44f05a9	stp	x20, x19, [sp, #0x50]
0x49c94	fd7b06a9	stp	x29, x30, [sp, #0x60]
0x49c98	fd830191	add	x29, sp, #0x60
0x49c9c	f30304aa	mov	x19, x4
0x49ca0	f40303aa	mov	x20, x3
0x49ca4	f50302aa	mov	x21, x2
0x49ca8	f60301aa	mov	x22, x1
0x49cac	f80300aa	mov	x24, x0
0x49cb0	52dfc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x49cb4	e8ef7db2	mov	x8, #0x7ffffffffffffff8 ; =9223372036854775800
0x49cb8	1f0008eb	cmp	x0, x8
0x49cbc	c2050054	b.hs	0x49d74 <_WeChatMain+0x30508>
0x49cc0	f70300aa	mov	x23, x0
0x49cc4	1f5c00f1	cmp	x0, #0x17
0x49cc8	a2000054	b.hs	0x49cdc <_WeChatMain+0x30470>
0x49ccc	f77f0039	strb	w23, [sp, #0x1f]
0x49cd0	f9230091	add	x25, sp, #0x8
0x49cd4	970100b5	cbnz	x23, 0x49d04 <_WeChatMain+0x30498>
0x49cd8	0f000014	b	0x49d14 <_WeChatMain+0x304a8>
0x49cdc	e80a40b2	orr	x8, x23, #0x7
0x49ce0	1f5d00f1	cmp	x8, #0x17
0x49ce4	29038052	mov	w9, #0x19               ; =25
0x49ce8	3a05889a	csinc	x26, x9, x8, eq
0x49cec	e0031aaa	mov	x0, x26
0x49cf0	d0d8c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x49cf4	f90300aa	mov	x25, x0
0x49cf8	480341b2	orr	x8, x26, #0x8000000000000000
0x49cfc	f72301a9	stp	x23, x8, [sp, #0x10]
0x49d00	e00700f9	str	x0, [sp, #0x8]
0x49d04	e00319aa	mov	x0, x25
0x49d08	e10318aa	mov	x1, x24
0x49d0c	e20317aa	mov	x2, x23
0x49d10	5edcc395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x49d14	3f6b3738	strb	wzr, [x25, x23]
0x49d18	e0230091	add	x0, sp, #0x8
0x49d1c	e10316aa	mov	x1, x22
0x49d20	e20315aa	mov	x2, x21
0x49d24	e30314aa	mov	x3, x20
0x49d28	e40313aa	mov	x4, x19
0x49d2c	050080d2	mov	x5, #0x0                ; =0
0x49d30	77ffff97	bl	0x49b0c <_WeChatMain+0x302a0>
0x49d34	e87fc039	ldrsb	w8, [sp, #0x1f]
0x49d38	0801f836	tbz	w8, #0x1f, 0x49d58 <_WeChatMain+0x304ec>
0x49d3c	e80740f9	ldr	x8, [sp, #0x8]
0x49d40	e90f40f9	ldr	x9, [sp, #0x18]
0x49d44	21f94092	and	x1, x9, #0x7fffffffffffffff
0x49d48	f30300aa	mov	x19, x0
0x49d4c	e00308aa	mov	x0, x8
0x49d50	afd8c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x49d54	e00313aa	mov	x0, x19
0x49d58	fd7b46a9	ldp	x29, x30, [sp, #0x60]
0x49d5c	f44f45a9	ldp	x20, x19, [sp, #0x50]
0x49d60	f65744a9	ldp	x22, x21, [sp, #0x40]
0x49d64	f85f43a9	ldp	x24, x23, [sp, #0x30]
0x49d68	fa6742a9	ldp	x26, x25, [sp, #0x20]
0x49d6c	ffc30191	add	sp, sp, #0x70
0x49d70	c0035fd6	ret
0x49d74	e0230091	add	x0, sp, #0x8
0x49d78	c143ff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x49d7c	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x49d80	f85f01a9	stp	x24, x23, [sp, #0x10]
0x49d84	f65702a9	stp	x22, x21, [sp, #0x20]
0x49d88	f44f03a9	stp	x20, x19, [sp, #0x30]
0x49d8c	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x49d90	fd030191	add	x29, sp, #0x40
0x49d94	f30305aa	mov	x19, x5
0x49d98	f40304aa	mov	x20, x4
0x49d9c	f50303aa	mov	x21, x3
0x49da0	f60302aa	mov	x22, x2
0x49da4	f70301aa	mov	x23, x1
0x49da8	f80300aa	mov	x24, x0
0x49dac	f90308aa	mov	x25, x8
0x49db0	00088052	mov	w0, #0x40               ; =64
0x49db4	9fd8c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x49db8	e10318aa	mov	x1, x24
0x49dbc	e20317aa	mov	x2, x23
0x49dc0	e30316aa	mov	x3, x22
0x49dc4	e40315aa	mov	x4, x21
0x49dc8	e50314aa	mov	x5, x20
0x49dcc	e60313aa	mov	x6, x19
0x49dd0	00feff97	bl	0x495d0 <_WeChatMain+0x2fd64>
0x49dd4	68d704f0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x49dd8	08e13891	add	x8, x8, #0xe38
0x49ddc	080000f9	str	x8, [x0]
0x49de0	1f1c00f9	str	xzr, [x0, #0x38]
0x49de4	e80300aa	mov	x8, x0
0x49de8	1f0d03f8	str	xzr, [x8, #0x30]!
0x49dec	081400f9	str	x8, [x0, #0x28]
0x49df0	200300f9	str	x0, [x25]
0x49df4	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x49df8	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x49dfc	f65742a9	ldp	x22, x21, [sp, #0x20]
0x49e00	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x49e04	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x49e08	c0035fd6	ret
0x49e0c	20008052	mov	w0, #0x1                ; =1
0x49e10	c0035fd6	ret
0x49e14	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x49e18	f44f01a9	stp	x20, x19, [sp, #0x10]
0x49e1c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x49e20	fd830091	add	x29, sp, #0x20
0x49e24	f50301aa	mov	x21, x1
0x49e28	f40300aa	mov	x20, x0
0x49e2c	f30308aa	mov	x19, x8
0x49e30	080040f9	ldr	x8, [x0]
0x49e34	084d40f9	ldr	x8, [x8, #0x98]
0x49e38	00013fd6	blr	x8
0x49e3c	e80314aa	mov	x8, x20
0x49e40	0a0d43f8	ldr	x10, [x8, #0x30]!
0x49e44	ca0100b4	cbz	x10, 0x49e7c <_WeChatMain+0x30610>
0x49e48	e90308aa	mov	x9, x8
0x49e4c	4b2140b9	ldr	w11, [x10, #0x20]
0x49e50	7f01006b	cmp	w11, w0
0x49e54	eba79f1a	cset	w11, lt
0x49e58	29b18a9a	csel	x9, x9, x10, lt
0x49e5c	4a596bf8	ldr	x10, [x10, w11, uxtw #3]
0x49e60	6affffb5	cbnz	x10, 0x49e4c <_WeChatMain+0x305e0>
0x49e64	3f0108eb	cmp	x9, x8
0x49e68	a0000054	b.eq	0x49e7c <_WeChatMain+0x30610>
0x49e6c	2a2140b9	ldr	w10, [x9, #0x20]
0x49e70	1f000a6b	cmp	w0, w10
0x49e74	08b1899a	csel	x8, x8, x9, lt
0x49e78	aa010054	b.ge	0x49eac <_WeChatMain+0x30640>
0x49e7c	880240f9	ldr	x8, [x20]
0x49e80	084d40f9	ldr	x8, [x8, #0x98]
0x49e84	e00314aa	mov	x0, x20
0x49e88	e10315aa	mov	x1, x21
0x49e8c	00013fd6	blr	x8
0x49e90	e10300aa	mov	x1, x0
0x49e94	e80313aa	mov	x8, x19
0x49e98	e00314aa	mov	x0, x20
0x49e9c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x49ea0	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x49ea4	f657c3a8	ldp	x22, x21, [sp], #0x30
0x49ea8	cf050014	b	0x4b5e4 <_WeChatMain+0x31d78>
0x49eac	09fdc039	ldrsb	w9, [x8, #0x3f]
0x49eb0	2901f837	tbnz	w9, #0x1f, 0x49ed4 <_WeChatMain+0x30668>
0x49eb4	0081c23c	ldur	q0, [x8, #0x28]
0x49eb8	088143f8	ldur	x8, [x8, #0x38]
0x49ebc	680a00f9	str	x8, [x19, #0x10]
0x49ec0	6002803d	str	q0, [x19]
0x49ec4	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x49ec8	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x49ecc	f657c3a8	ldp	x22, x21, [sp], #0x30
0x49ed0	c0035fd6	ret
0x49ed4	018942a9	ldp	x1, x2, [x8, #0x28]
0x49ed8	e00313aa	mov	x0, x19
0x49edc	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x49ee0	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x49ee4	f657c3a8	ldp	x22, x21, [sp], #0x30
0x49ee8	8e3bff17	b	0x18d20 <__text+0x1d20>
0x49eec	ff8301d1	sub	sp, sp, #0x60
0x49ef0	f65703a9	stp	x22, x21, [sp, #0x30]
0x49ef4	f44f04a9	stp	x20, x19, [sp, #0x40]
0x49ef8	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x49efc	fd430191	add	x29, sp, #0x50
0x49f00	f40301aa	mov	x20, x1
0x49f04	f30300aa	mov	x19, x0
0x49f08	08745e92	and	x8, x0, #0xfffffffc00000000
0x49f0c	95fd04b0	adrp	x21, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x49f10	b5023b91	add	x21, x21, #0xec0
0x49f14	a90640f9	ldr	x9, [x21, #0x8]
0x49f18	1f0109eb	cmp	x8, x9
0x49f1c	61000054	b.ne	0x49f28 <_WeChatMain+0x306bc>
0x49f20	e00313aa	mov	x0, x19
0x49f24	4ad6ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x49f28	08220490	adrp	x8, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x49f2c	000144fd	ldr	d0, [x8, #0x800]
0x49f30	e00b00fd	str	d0, [sp, #0x10]
0x49f34	48008052	mov	w8, #0x2                ; =2
0x49f38	e81b00b9	str	w8, [sp, #0x18]
0x49f3c	68008052	mov	w8, #0x3                ; =3
0x49f40	e81300f9	str	x8, [sp, #0x20]
0x49f44	f42b00b9	str	w20, [sp, #0x28]
0x49f48	88d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x49f4c	08410591	add	x8, x8, #0x150
0x49f50	e84f00a9	stp	x8, x19, [sp]
0x49f54	e0030091	mov	x0, sp
0x49f58	bff8ff97	bl	0x48254 <_WeChatMain+0x2e9e8>
0x49f5c	88d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x49f60	08610391	add	x8, x8, #0xd8
0x49f64	e80300f9	str	x8, [sp]
0x49f68	e80740f9	ldr	x8, [sp, #0x8]
0x49f6c	09755e92	and	x9, x8, #0xfffffffc00000000
0x49f70	aa0640f9	ldr	x10, [x21, #0x8]
0x49f74	3f010aeb	cmp	x9, x10
0x49f78	a1000054	b.ne	0x49f8c <_WeChatMain+0x30720>
0x49f7c	f30300aa	mov	x19, x0
0x49f80	e00308aa	mov	x0, x8
0x49f84	cfd6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x49f88	e00313aa	mov	x0, x19
0x49f8c	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x49f90	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x49f94	f65743a9	ldp	x22, x21, [sp, #0x30]
0x49f98	ff830191	add	sp, sp, #0x60
0x49f9c	c0035fd6	ret
0x49fa0	ff4302d1	sub	sp, sp, #0x90
0x49fa4	f85f05a9	stp	x24, x23, [sp, #0x50]
0x49fa8	f65706a9	stp	x22, x21, [sp, #0x60]
0x49fac	f44f07a9	stp	x20, x19, [sp, #0x70]
0x49fb0	fd7b08a9	stp	x29, x30, [sp, #0x80]
0x49fb4	fd030291	add	x29, sp, #0x80
0x49fb8	f30301aa	mov	x19, x1
0x49fbc	f50300aa	mov	x21, x0
0x49fc0	8edec395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x49fc4	e8ef7db2	mov	x8, #0x7ffffffffffffff8 ; =9223372036854775800
0x49fc8	1f0008eb	cmp	x0, x8
0x49fcc	82080054	b.hs	0x4a0dc <_WeChatMain+0x30870>
0x49fd0	f40300aa	mov	x20, x0
0x49fd4	1f5c00f1	cmp	x0, #0x17
0x49fd8	a2000054	b.hs	0x49fec <_WeChatMain+0x30780>
0x49fdc	f47f0039	strb	w20, [sp, #0x1f]
0x49fe0	f6230091	add	x22, sp, #0x8
0x49fe4	940100b5	cbnz	x20, 0x4a014 <_WeChatMain+0x307a8>
0x49fe8	0f000014	b	0x4a024 <_WeChatMain+0x307b8>
0x49fec	880a40b2	orr	x8, x20, #0x7
0x49ff0	1f5d00f1	cmp	x8, #0x17
0x49ff4	29038052	mov	w9, #0x19               ; =25
0x49ff8	3705889a	csinc	x23, x9, x8, eq
0x49ffc	e00317aa	mov	x0, x23
0x4a000	0cd8c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4a004	f60300aa	mov	x22, x0
0x4a008	e80241b2	orr	x8, x23, #0x8000000000000000
0x4a00c	f42301a9	stp	x20, x8, [sp, #0x10]
0x4a010	e00700f9	str	x0, [sp, #0x8]
0x4a014	e00316aa	mov	x0, x22
0x4a018	e10315aa	mov	x1, x21
0x4a01c	e20314aa	mov	x2, x20
0x4a020	9adbc395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x4a024	df6a3438	strb	wzr, [x22, x20]
0x4a028	f5230091	add	x21, sp, #0x8
0x4a02c	a8765e92	and	x8, x21, #0xfffffffc00000000
0x4a030	94fd0490	adrp	x20, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4a034	94023b91	add	x20, x20, #0xec0
0x4a038	890640f9	ldr	x9, [x20, #0x8]
0x4a03c	1f0109eb	cmp	x8, x9
0x4a040	61000054	b.ne	0x4a04c <_WeChatMain+0x307e0>
0x4a044	e0230091	add	x0, sp, #0x8
0x4a048	01d6ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4a04c	e82104f0	adrp	x8, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4a050	000144fd	ldr	d0, [x8, #0x800]
0x4a054	e01b00fd	str	d0, [sp, #0x30]
0x4a058	48008052	mov	w8, #0x2                ; =2
0x4a05c	e83b00b9	str	w8, [sp, #0x38]
0x4a060	68008052	mov	w8, #0x3                ; =3
0x4a064	e82300f9	str	x8, [sp, #0x40]
0x4a068	f34b00b9	str	w19, [sp, #0x48]
0x4a06c	68d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4a070	08410591	add	x8, x8, #0x150
0x4a074	e85702a9	stp	x8, x21, [sp, #0x20]
0x4a078	e0830091	add	x0, sp, #0x20
0x4a07c	76f8ff97	bl	0x48254 <_WeChatMain+0x2e9e8>
0x4a080	f30300aa	mov	x19, x0
0x4a084	68d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4a088	08610391	add	x8, x8, #0xd8
0x4a08c	e81300f9	str	x8, [sp, #0x20]
0x4a090	e01740f9	ldr	x0, [sp, #0x28]
0x4a094	08745e92	and	x8, x0, #0xfffffffc00000000
0x4a098	890640f9	ldr	x9, [x20, #0x8]
0x4a09c	1f0109eb	cmp	x8, x9
0x4a0a0	41000054	b.ne	0x4a0a8 <_WeChatMain+0x3083c>
0x4a0a4	87d6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4a0a8	e87fc039	ldrsb	w8, [sp, #0x1f]
0x4a0ac	a800f836	tbz	w8, #0x1f, 0x4a0c0 <_WeChatMain+0x30854>
0x4a0b0	e00740f9	ldr	x0, [sp, #0x8]
0x4a0b4	e80f40f9	ldr	x8, [sp, #0x18]
0x4a0b8	01f94092	and	x1, x8, #0x7fffffffffffffff
0x4a0bc	d4d7c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4a0c0	e00313aa	mov	x0, x19
0x4a0c4	fd7b48a9	ldp	x29, x30, [sp, #0x80]
0x4a0c8	f44f47a9	ldp	x20, x19, [sp, #0x70]
0x4a0cc	f65746a9	ldp	x22, x21, [sp, #0x60]
0x4a0d0	f85f45a9	ldp	x24, x23, [sp, #0x50]
0x4a0d4	ff430291	add	sp, sp, #0x90
0x4a0d8	c0035fd6	ret
0x4a0dc	e0230091	add	x0, sp, #0x8
0x4a0e0	e742ff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x4a0e4	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x4a0e8	f85f01a9	stp	x24, x23, [sp, #0x10]
0x4a0ec	f65702a9	stp	x22, x21, [sp, #0x20]
0x4a0f0	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4a0f4	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4a0f8	fd030191	add	x29, sp, #0x40
0x4a0fc	f30305aa	mov	x19, x5
0x4a100	f40304aa	mov	x20, x4
0x4a104	f50303aa	mov	x21, x3
0x4a108	f60302aa	mov	x22, x2
0x4a10c	f70301aa	mov	x23, x1
0x4a110	f80300aa	mov	x24, x0
0x4a114	f90308aa	mov	x25, x8
0x4a118	00088052	mov	w0, #0x40               ; =64
0x4a11c	c5d7c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4a120	e10318aa	mov	x1, x24
0x4a124	e20317aa	mov	x2, x23
0x4a128	e30316aa	mov	x3, x22
0x4a12c	e40315aa	mov	x4, x21
0x4a130	e50314aa	mov	x5, x20
0x4a134	e60313aa	mov	x6, x19
0x4a138	26fdff97	bl	0x495d0 <_WeChatMain+0x2fd64>
0x4a13c	e80300aa	mov	x8, x0
0x4a140	1f0d03f8	str	xzr, [x8, #0x30]!
0x4a144	1f1c00f9	str	xzr, [x0, #0x38]
0x4a148	081400f9	str	x8, [x0, #0x28]
0x4a14c	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a150	08e13b91	add	x8, x8, #0xef8
0x4a154	080000f9	str	x8, [x0]
0x4a158	200300f9	str	x0, [x25]
0x4a15c	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4a160	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4a164	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4a168	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x4a16c	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x4a170	c0035fd6	ret
0x4a174	40008052	mov	w0, #0x2                ; =2
0x4a178	c0035fd6	ret
0x4a17c	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x4a180	f85f01a9	stp	x24, x23, [sp, #0x10]
0x4a184	f65702a9	stp	x22, x21, [sp, #0x20]
0x4a188	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4a18c	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4a190	fd030191	add	x29, sp, #0x40
0x4a194	f30305aa	mov	x19, x5
0x4a198	f40304aa	mov	x20, x4
0x4a19c	f50303aa	mov	x21, x3
0x4a1a0	f60302aa	mov	x22, x2
0x4a1a4	f70301aa	mov	x23, x1
0x4a1a8	f80300aa	mov	x24, x0
0x4a1ac	f90308aa	mov	x25, x8
0x4a1b0	00058052	mov	w0, #0x28               ; =40
0x4a1b4	9fd7c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4a1b8	e10318aa	mov	x1, x24
0x4a1bc	e20317aa	mov	x2, x23
0x4a1c0	e30316aa	mov	x3, x22
0x4a1c4	e40315aa	mov	x4, x21
0x4a1c8	e50314aa	mov	x5, x20
0x4a1cc	e60313aa	mov	x6, x19
0x4a1d0	00fdff97	bl	0x495d0 <_WeChatMain+0x2fd64>
0x4a1d4	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a1d8	08e13e91	add	x8, x8, #0xfb8
0x4a1dc	080000f9	str	x8, [x0]
0x4a1e0	200300f9	str	x0, [x25]
0x4a1e4	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4a1e8	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4a1ec	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4a1f0	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x4a1f4	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x4a1f8	c0035fd6	ret
0x4a1fc	60008052	mov	w0, #0x3                ; =3
0x4a200	c0035fd6	ret
0x4a204	ff0301d1	sub	sp, sp, #0x40
0x4a208	f65701a9	stp	x22, x21, [sp, #0x10]
0x4a20c	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4a210	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4a214	fdc30091	add	x29, sp, #0x30
0x4a218	f30301aa	mov	x19, x1
0x4a21c	f40300aa	mov	x20, x0
0x4a220	5afcff97	bl	0x49388 <_WeChatMain+0x2fb1c>
0x4a224	880e40f9	ldr	x8, [x20, #0x18]
0x4a228	081140f9	ldr	x8, [x8, #0x20]
0x4a22c	082540a9	ldp	x8, x9, [x8]
0x4a230	290108cb	sub	x9, x9, x8
0x4a234	29fd4293	asr	x9, x9, #2
0x4a238	290d00d1	sub	x9, x9, #0x3
0x4a23c	3f0d00b1	cmn	x9, #0x3
0x4a240	08020054	b.hi	0x4a280 <_WeChatMain+0x30a14>
0x4a244	35008052	mov	w21, #0x1               ; =1
0x4a248	087975b8	ldr	w8, [x8, x21, lsl #2]
0x4a24c	e80f00b9	str	w8, [sp, #0xc]
0x4a250	e1330091	add	x1, sp, #0xc
0x4a254	e00313aa	mov	x0, x19
0x4a258	ac350094	bl	0x57908 <_WeChatMain+0x3e09c>
0x4a25c	b5060091	add	x21, x21, #0x1
0x4a260	880e40f9	ldr	x8, [x20, #0x18]
0x4a264	081140f9	ldr	x8, [x8, #0x20]
0x4a268	082540a9	ldp	x8, x9, [x8]
0x4a26c	290108cb	sub	x9, x9, x8
0x4a270	29fd4293	asr	x9, x9, #2
0x4a274	290500d1	sub	x9, x9, #0x1
0x4a278	bf0209eb	cmp	x21, x9
0x4a27c	63feff54	b.lo	0x4a248 <_WeChatMain+0x309dc>
0x4a280	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4a284	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4a288	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4a28c	ff030191	add	sp, sp, #0x40
0x4a290	c0035fd6	ret
0x4a294	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4a298	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4a29c	fd430091	add	x29, sp, #0x10
0x4a2a0	f30300aa	mov	x19, x0
0x4a2a4	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a2a8	08e13891	add	x8, x8, #0xe38
0x4a2ac	080000f9	str	x8, [x0]
0x4a2b0	011840f9	ldr	x1, [x0, #0x30]
0x4a2b4	00a00091	add	x0, x0, #0x28
0x4a2b8	5575ff97	bl	0x2780c <_WeChatMain+0xdfa0>
0x4a2bc	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a2c0	08e13591	add	x8, x8, #0xd78
0x4a2c4	680200f9	str	x8, [x19]
0x4a2c8	601240f9	ldr	x0, [x19, #0x20]
0x4a2cc	7f1200f9	str	xzr, [x19, #0x20]
0x4a2d0	800000b4	cbz	x0, 0x4a2e0 <_WeChatMain+0x30a74>
0x4a2d4	080040f9	ldr	x8, [x0]
0x4a2d8	080540f9	ldr	x8, [x8, #0x8]
0x4a2dc	00013fd6	blr	x8
0x4a2e0	600e40f9	ldr	x0, [x19, #0x18]
0x4a2e4	7f0e00f9	str	xzr, [x19, #0x18]
0x4a2e8	800000b4	cbz	x0, 0x4a2f8 <_WeChatMain+0x30a8c>
0x4a2ec	080040f9	ldr	x8, [x0]
0x4a2f0	080540f9	ldr	x8, [x8, #0x8]
0x4a2f4	00013fd6	blr	x8
0x4a2f8	e00313aa	mov	x0, x19
0x4a2fc	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4a300	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4a304	7242ff17	b	0x1accc <_WeChatMain+0x1460>
0x4a308	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4a30c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4a310	fd430091	add	x29, sp, #0x10
0x4a314	f30300aa	mov	x19, x0
0x4a318	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a31c	08e13891	add	x8, x8, #0xe38
0x4a320	080000f9	str	x8, [x0]
0x4a324	011840f9	ldr	x1, [x0, #0x30]
0x4a328	00a00091	add	x0, x0, #0x28
0x4a32c	3875ff97	bl	0x2780c <_WeChatMain+0xdfa0>
0x4a330	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a334	08e13591	add	x8, x8, #0xd78
0x4a338	680200f9	str	x8, [x19]
0x4a33c	601240f9	ldr	x0, [x19, #0x20]
0x4a340	7f1200f9	str	xzr, [x19, #0x20]
0x4a344	800000b4	cbz	x0, 0x4a354 <_WeChatMain+0x30ae8>
0x4a348	080040f9	ldr	x8, [x0]
0x4a34c	080540f9	ldr	x8, [x8, #0x8]
0x4a350	00013fd6	blr	x8
0x4a354	600e40f9	ldr	x0, [x19, #0x18]
0x4a358	7f0e00f9	str	xzr, [x19, #0x18]
0x4a35c	800000b4	cbz	x0, 0x4a36c <_WeChatMain+0x30b00>
0x4a360	080040f9	ldr	x8, [x0]
0x4a364	080540f9	ldr	x8, [x8, #0x8]
0x4a368	00013fd6	blr	x8
0x4a36c	e00313aa	mov	x0, x19
0x4a370	5742ff97	bl	0x1accc <_WeChatMain+0x1460>
0x4a374	01088052	mov	w1, #0x40               ; =64
0x4a378	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4a37c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4a380	23d7c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4a384	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4a388	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4a38c	fd430091	add	x29, sp, #0x10
0x4a390	f30300aa	mov	x19, x0
0x4a394	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a398	08e13591	add	x8, x8, #0xd78
0x4a39c	080000f9	str	x8, [x0]
0x4a3a0	001040f9	ldr	x0, [x0, #0x20]
0x4a3a4	7f1200f9	str	xzr, [x19, #0x20]
0x4a3a8	800000b4	cbz	x0, 0x4a3b8 <_WeChatMain+0x30b4c>
0x4a3ac	080040f9	ldr	x8, [x0]
0x4a3b0	080540f9	ldr	x8, [x8, #0x8]
0x4a3b4	00013fd6	blr	x8
0x4a3b8	600e40f9	ldr	x0, [x19, #0x18]
0x4a3bc	7f0e00f9	str	xzr, [x19, #0x18]
0x4a3c0	800000b4	cbz	x0, 0x4a3d0 <_WeChatMain+0x30b64>
0x4a3c4	080040f9	ldr	x8, [x0]
0x4a3c8	080540f9	ldr	x8, [x8, #0x8]
0x4a3cc	00013fd6	blr	x8
0x4a3d0	e00313aa	mov	x0, x19
0x4a3d4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4a3d8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4a3dc	3c42ff17	b	0x1accc <_WeChatMain+0x1460>
0x4a3e0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4a3e4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4a3e8	fd430091	add	x29, sp, #0x10
0x4a3ec	f30300aa	mov	x19, x0
0x4a3f0	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a3f4	08e13591	add	x8, x8, #0xd78
0x4a3f8	080000f9	str	x8, [x0]
0x4a3fc	001040f9	ldr	x0, [x0, #0x20]
0x4a400	7f1200f9	str	xzr, [x19, #0x20]
0x4a404	800000b4	cbz	x0, 0x4a414 <_WeChatMain+0x30ba8>
0x4a408	080040f9	ldr	x8, [x0]
0x4a40c	080540f9	ldr	x8, [x8, #0x8]
0x4a410	00013fd6	blr	x8
0x4a414	600e40f9	ldr	x0, [x19, #0x18]
0x4a418	7f0e00f9	str	xzr, [x19, #0x18]
0x4a41c	800000b4	cbz	x0, 0x4a42c <_WeChatMain+0x30bc0>
0x4a420	080040f9	ldr	x8, [x0]
0x4a424	080540f9	ldr	x8, [x8, #0x8]
0x4a428	00013fd6	blr	x8
0x4a42c	e00313aa	mov	x0, x19
0x4a430	2742ff97	bl	0x1accc <_WeChatMain+0x1460>
0x4a434	01058052	mov	w1, #0x28               ; =40
0x4a438	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4a43c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4a440	f3d6c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4a444	ff4301d1	sub	sp, sp, #0x50
0x4a448	e923016d	stp	d9, d8, [sp, #0x10]
0x4a44c	f65702a9	stp	x22, x21, [sp, #0x20]
0x4a450	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4a454	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4a458	fd030191	add	x29, sp, #0x40
0x4a45c	f40300aa	mov	x20, x0
0x4a460	00048052	mov	w0, #0x20               ; =32
0x4a464	f3d6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4a468	f30300aa	mov	x19, x0
0x4a46c	881240f9	ldr	x8, [x20, #0x20]
0x4a470	01050091	add	x1, x8, #0x1
0x4a474	fcefff97	bl	0x46464 <_WeChatMain+0x2cbf8>
0x4a478	951640b9	ldr	w21, [x20, #0x14]
0x4a47c	801a40bd	ldr	s0, [x20, #0x18]
0x4a480	00a4200f	sshll.2d	v0, v0, #0x0
0x4a484	00d8615e	scvtf	d0, d0
0x4a488	1adac395	bl	0x7140cf0 <_wxam_enc_uninit_10+0x7140cf0>
0x4a48c	682640a9	ldp	x8, x9, [x19]
0x4a490	150500b9	str	w21, [x8, #0x4]
0x4a494	290108cb	sub	x9, x9, x8
0x4a498	2afd4293	asr	x10, x9, #2
0x4a49c	4b0500d1	sub	x11, x10, #0x1
0x4a4a0	7f0d00f1	cmp	x11, #0x3
0x4a4a4	23030054	b.lo	0x4a508 <_WeChatMain+0x30c9c>
0x4a4a8	0840601e	fmov	d8, d0
0x4a4ac	540d00d1	sub	x20, x10, #0x3
0x4a4b0	16018052	mov	w22, #0x8               ; =8
0x4a4b4	a002621e	scvtf	d0, w21
0x4a4b8	0edac395	bl	0x7140cf0 <_wxam_enc_uninit_10+0x7140cf0>
0x4a4bc	e00700fd	str	d0, [sp, #0x8]
0x4a4c0	e0230091	add	x0, sp, #0x8
0x4a4c4	0242ff97	bl	0x1accc <_WeChatMain+0x1460>
0x4a4c8	e00740fd	ldr	d0, [sp, #0x8]
0x4a4cc	0139601e	fsub	d1, d8, d0
0x4a4d0	8202639e	ucvtf	d2, x20
0x4a4d4	2118621e	fdiv	d1, d1, d2
0x4a4d8	0028611e	fadd	d0, d0, d1
0x4a4dc	b2d8c395	bl	0x71407a4 <_wxam_enc_uninit_10+0x71407a4>
0x4a4e0	0800641e	fcvtas	w8, d0
0x4a4e4	bf02086b	cmp	w21, w8
0x4a4e8	15b5951a	csinc	w21, w8, w21, lt
0x4a4ec	680240f9	ldr	x8, [x19]
0x4a4f0	156936b8	str	w21, [x8, x22]
0x4a4f4	d6120091	add	x22, x22, #0x4
0x4a4f8	940600f1	subs	x20, x20, #0x1
0x4a4fc	c1fdff54	b.ne	0x4a4b4 <_WeChatMain+0x30c48>
0x4a500	690640f9	ldr	x9, [x19, #0x8]
0x4a504	290108cb	sub	x9, x9, x8
0x4a508	0a220490	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4a50c	4a410091	add	x10, x10, #0x10
0x4a510	4a0140b9	ldr	w10, [x10]
0x4a514	0801098b	add	x8, x8, x9
0x4a518	0ac11fb8	stur	w10, [x8, #-0x4]
0x4a51c	e00313aa	mov	x0, x19
0x4a520	0cf0ff97	bl	0x46550 <_WeChatMain+0x2cce4>
0x4a524	e00313aa	mov	x0, x19
0x4a528	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4a52c	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4a530	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4a534	e923416d	ldp	d9, d8, [sp, #0x10]
0x4a538	ff430191	add	sp, sp, #0x50
0x4a53c	c0035fd6	ret
0x4a540	ff0301d1	sub	sp, sp, #0x40
0x4a544	f65701a9	stp	x22, x21, [sp, #0x10]
0x4a548	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4a54c	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4a550	fdc30091	add	x29, sp, #0x30
0x4a554	f40301aa	mov	x20, x1
0x4a558	f60300aa	mov	x22, x0
0x4a55c	f30308aa	mov	x19, x8
0x4a560	00058052	mov	w0, #0x28               ; =40
0x4a564	b3d6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4a568	f50300aa	mov	x21, x0
0x4a56c	c00640f9	ldr	x0, [x22, #0x8]
0x4a570	a00700b5	cbnz	x0, 0x4a664 <_WeChatMain+0x30df8>
0x4a574	48100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a578	09614d39	ldrb	w9, [x8, #0x358]
0x4a57c	09040037	tbnz	w9, #0x0, 0x4a5fc <_WeChatMain+0x30d90>
0x4a580	090080d2	mov	x9, #0x0                ; =0
0x4a584	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x4a588	aa9999f2	movk	x10, #0xcccd
0x4a58c	6b028092	mov	x11, #-0x14             ; =-20
0x4a590	ec2104f0	adrp	x12, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4a594	8c812391	add	x12, x12, #0x8e0
0x4a598	4085040f	movi.4h	v0, #0x8a
0x4a59c	4d100590	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a5a0	adc90b91	add	x13, x13, #0x2f2
0x4a5a4	2e7dca9b	umulh	x14, x9, x10
0x4a5a8	cefd44d3	lsr	x14, x14, #4
0x4a5ac	8f01098b	add	x15, x12, x9
0x4a5b0	ce3d0b9b	madd	x14, x14, x11, x15
0x4a5b4	efe51791	add	x15, x15, #0x5f9
0x4a5b8	ce951791	add	x14, x14, #0x5e5
0x4a5bc	e10140bd	ldr	s1, [x15]
0x4a5c0	0110212e	uaddw.8h	v1, v0, v1
0x4a5c4	c20140bd	ldr	s2, [x14]
0x4a5c8	42a4082f	ushll.8h	v2, v2, #0x0
0x4a5cc	211c222e	eor.8b	v1, v1, v2
0x4a5d0	2118000e	uzp1.8b	v1, v1, v0
0x4a5d4	a16929bc	str	s1, [x13, x9]
0x4a5d8	29110091	add	x9, x9, #0x4
0x4a5dc	3f9101f1	cmp	x9, #0x64
0x4a5e0	21feff54	b.ne	0x4a5a4 <_WeChatMain+0x30d38>
0x4a5e4	49100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a5e8	29590d91	add	x9, x9, #0x356
0x4a5ec	0a0d8052	mov	w10, #0x68              ; =104
0x4a5f0	2a010079	strh	w10, [x9]
0x4a5f4	29008052	mov	w9, #0x1                ; =1
0x4a5f8	09610d39	strb	w9, [x8, #0x358]
0x4a5fc	48100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a600	09b54d39	ldrb	w9, [x8, #0x36d]
0x4a604	89010037	tbnz	w9, #0x0, 0x4a634 <_WeChatMain+0x30dc8>
0x4a608	c92104b0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4a60c	209d47fd	ldr	d0, [x9, #0xf38]
0x4a610	49100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a614	29810d91	add	x9, x9, #0x360
0x4a618	200100fd	str	d0, [x9]
0x4a61c	ca2104b0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4a620	40a147fd	ldr	d0, [x10, #0xf40]
0x4a624	200900bd	str	s0, [x9, #0x8]
0x4a628	3f310039	strb	wzr, [x9, #0xc]
0x4a62c	29008052	mov	w9, #0x1                ; =1
0x4a630	09b50d39	strb	w9, [x8, #0x36d]
0x4a634	40100590	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a638	00c80b91	add	x0, x0, #0x2f2
0x4a63c	42100590	adrp	x2, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a640	42800d91	add	x2, x2, #0x360
0x4a644	e8230091	add	x8, sp, #0x8
0x4a648	a1128052	mov	w1, #0x95               ; =149
0x4a64c	3e40ff97	bl	0x1a744 <_WeChatMain+0xed8>
0x4a650	e0230091	add	x0, sp, #0x8
0x4a654	8340ff97	bl	0x1a860 <_WeChatMain+0xff4>
0x4a658	e0230091	add	x0, sp, #0x8
0x4a65c	8440ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x4a660	c00640f9	ldr	x0, [x22, #0x8]
0x4a664	b8040094	bl	0x4b944 <_WeChatMain+0x320d8>
0x4a668	e10300aa	mov	x1, x0
0x4a66c	e00315aa	mov	x0, x21
0x4a670	e20314aa	mov	x2, x20
0x4a674	95fbff97	bl	0x494c8 <_WeChatMain+0x2fc5c>
0x4a678	750200f9	str	x21, [x19]
0x4a67c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4a680	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4a684	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4a688	ff030191	add	sp, sp, #0x40
0x4a68c	c0035fd6	ret
0x4a690	c0035fd6	ret
0x4a694	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4a698	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4a69c	fd430091	add	x29, sp, #0x10
0x4a6a0	f40300aa	mov	x20, x0
0x4a6a4	00048052	mov	w0, #0x20               ; =32
0x4a6a8	62d6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4a6ac	f30300aa	mov	x19, x0
0x4a6b0	881240f9	ldr	x8, [x20, #0x20]
0x4a6b4	01050091	add	x1, x8, #0x1
0x4a6b8	6befff97	bl	0x46464 <_WeChatMain+0x2cbf8>
0x4a6bc	082440a9	ldp	x8, x9, [x0]
0x4a6c0	290108cb	sub	x9, x9, x8
0x4a6c4	2afd4293	asr	x10, x9, #2
0x4a6c8	490500d1	sub	x9, x10, #0x1
0x4a6cc	3f0900f1	cmp	x9, #0x2
0x4a6d0	030d0054	b.lo	0x4a870 <_WeChatMain+0x31004>
0x4a6d4	8086422d	ldp	s0, s1, [x20, #0x14]
0x4a6d8	00a4200f	sshll.2d	v0, v0, #0x0
0x4a6dc	00d8615e	scvtf	d0, d0
0x4a6e0	21a4200f	sshll.2d	v1, v1, #0x0
0x4a6e4	21d8615e	scvtf	d1, d1
0x4a6e8	4b0d00d1	sub	x11, x10, #0x3
0x4a6ec	6201639e	ucvtf	d2, x11
0x4a6f0	4c0900d1	sub	x12, x10, #0x2
0x4a6f4	9f2100f1	cmp	x12, #0x8
0x4a6f8	62000054	b.hs	0x4a704 <_WeChatMain+0x30e98>
0x4a6fc	2b008052	mov	w11, #0x1               ; =1
0x4a700	4b000014	b	0x4a82c <_WeChatMain+0x30fc0>
0x4a704	8df17d92	and	x13, x12, #0xfffffffffffffff8
0x4a708	230d084e	dup.2d	v3, x9
0x4a70c	0404084e	dup.2d	v4, v0[0]
0x4a710	ab0140b2	orr	x11, x13, #0x1
0x4a714	4504084e	dup.2d	v5, v2[0]
0x4a718	ee2104f0	adrp	x14, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4a71c	c619c23d	ldr	q6, [x14, #0x860]
0x4a720	0e510091	add	x14, x8, #0x14
0x4a724	4f008092	mov	x15, #-0x3              ; =-3
0x4a728	e70d084e	dup.2d	v7, x15
0x4a72c	8f008092	mov	x15, #-0x5              ; =-5
0x4a730	f00d084e	dup.2d	v16, x15
0x4a734	cf008092	mov	x15, #-0x7              ; =-7
0x4a738	f10d084e	dup.2d	v17, x15
0x4a73c	2f008052	mov	w15, #0x1               ; =1
0x4a740	f20d084e	dup.2d	v18, x15
0x4a744	6f008052	mov	w15, #0x3               ; =3
0x4a748	f30d084e	dup.2d	v19, x15
0x4a74c	af008052	mov	w15, #0x5               ; =5
0x4a750	f40d084e	dup.2d	v20, x15
0x4a754	f5e7076f	movi.2d	v21, #0xffffffffffffffff
0x4a758	16f4036f	fmov.2d	v22, #0.50000000
0x4a75c	0f018052	mov	w15, #0x8               ; =8
0x4a760	f70d084e	dup.2d	v23, x15
0x4a764	ef030daa	mov	x15, x13
0x4a768	d858206e	mvn.16b	v24, v6
0x4a76c	7884f84e	add.2d	v24, v3, v24
0x4a770	7984e66e	sub.2d	v25, v3, v6
0x4a774	3a87e74e	add.2d	v26, v25, v7
0x4a778	3b87f04e	add.2d	v27, v25, v16
0x4a77c	3987f14e	add.2d	v25, v25, v17
0x4a780	18db616e	ucvtf.2d	v24, v24
0x4a784	5adb616e	ucvtf.2d	v26, v26
0x4a788	7bdb616e	ucvtf.2d	v27, v27
0x4a78c	39db616e	ucvtf.2d	v25, v25
0x4a790	dc84f54e	add.2d	v28, v6, v21
0x4a794	dd84f24e	add.2d	v29, v6, v18
0x4a798	de84f34e	add.2d	v30, v6, v19
0x4a79c	df84f44e	add.2d	v31, v6, v20
0x4a7a0	9cdb616e	ucvtf.2d	v28, v28
0x4a7a4	bddb616e	ucvtf.2d	v29, v29
0x4a7a8	dedb616e	ucvtf.2d	v30, v30
0x4a7ac	ffdb616e	ucvtf.2d	v31, v31
0x4a7b0	9c93c14f	fmul.2d	v28, v28, v1[0]
0x4a7b4	bd93c14f	fmul.2d	v29, v29, v1[0]
0x4a7b8	de93c14f	fmul.2d	v30, v30, v1[0]
0x4a7bc	ff93c14f	fmul.2d	v31, v31, v1[0]
0x4a7c0	1ccf644e	fmla.2d	v28, v24, v4
0x4a7c4	5dcf644e	fmla.2d	v29, v26, v4
0x4a7c8	7ecf644e	fmla.2d	v30, v27, v4
0x4a7cc	3fcf644e	fmla.2d	v31, v25, v4
0x4a7d0	98ff656e	fdiv.2d	v24, v28, v5
0x4a7d4	b9ff656e	fdiv.2d	v25, v29, v5
0x4a7d8	daff656e	fdiv.2d	v26, v30, v5
0x4a7dc	fbff656e	fdiv.2d	v27, v31, v5
0x4a7e0	18d7764e	fadd.2d	v24, v24, v22
0x4a7e4	39d7764e	fadd.2d	v25, v25, v22
0x4a7e8	5ad7764e	fadd.2d	v26, v26, v22
0x4a7ec	7bd7764e	fadd.2d	v27, v27, v22
0x4a7f0	18bbe14e	fcvtzs.2d	v24, v24
0x4a7f4	182ba10e	xtn.2s	v24, v24
0x4a7f8	39bbe14e	fcvtzs.2d	v25, v25
0x4a7fc	392ba10e	xtn.2s	v25, v25
0x4a800	5abbe14e	fcvtzs.2d	v26, v26
0x4a804	5a2ba10e	xtn.2s	v26, v26
0x4a808	7bbbe14e	fcvtzs.2d	v27, v27
0x4a80c	7b2ba10e	xtn.2s	v27, v27
0x4a810	d8653f6d	stp	d24, d25, [x14, #-0x10]
0x4a814	da6d826c	stp	d26, d27, [x14], #0x20
0x4a818	c684f74e	add.2d	v6, v6, v23
0x4a81c	ef2100f1	subs	x15, x15, #0x8
0x4a820	41faff54	b.ne	0x4a768 <_WeChatMain+0x30efc>
0x4a824	9f010deb	cmp	x12, x13
0x4a828	40020054	b.eq	0x4a870 <_WeChatMain+0x31004>
0x4a82c	4a010bcb	sub	x10, x10, x11
0x4a830	4a0900d1	sub	x10, x10, #0x2
0x4a834	0c090b8b	add	x12, x8, x11, lsl #2
0x4a838	6b0500d1	sub	x11, x11, #0x1
0x4a83c	03106c1e	fmov	d3, #0.50000000
0x4a840	4401639e	ucvtf	d4, x10
0x4a844	6501639e	ucvtf	d5, x11
0x4a848	2508651e	fmul	d5, d1, d5
0x4a84c	0414441f	fmadd	d4, d0, d4, d5
0x4a850	8418621e	fdiv	d4, d4, d2
0x4a854	8428631e	fadd	d4, d4, d3
0x4a858	8d00781e	fcvtzs	w13, d4
0x4a85c	8d4500b8	str	w13, [x12], #0x4
0x4a860	4a0500d1	sub	x10, x10, #0x1
0x4a864	6b050091	add	x11, x11, #0x1
0x4a868	5f0500b1	cmn	x10, #0x1
0x4a86c	a1feff54	b.ne	0x4a840 <_WeChatMain+0x30fd4>
0x4a870	0a220490	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4a874	4a410091	add	x10, x10, #0x10
0x4a878	4a0140b9	ldr	w10, [x10]
0x4a87c	0a7929b8	str	w10, [x8, x9, lsl #2]
0x4a880	e00313aa	mov	x0, x19
0x4a884	33efff97	bl	0x46550 <_WeChatMain+0x2cce4>
0x4a888	e00313aa	mov	x0, x19
0x4a88c	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4a890	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4a894	c0035fd6	ret
0x4a898	ff0301d1	sub	sp, sp, #0x40
0x4a89c	f65701a9	stp	x22, x21, [sp, #0x10]
0x4a8a0	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4a8a4	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4a8a8	fdc30091	add	x29, sp, #0x30
0x4a8ac	f50301aa	mov	x21, x1
0x4a8b0	f60300aa	mov	x22, x0
0x4a8b4	f30308aa	mov	x19, x8
0x4a8b8	00088052	mov	w0, #0x40               ; =64
0x4a8bc	ddd5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4a8c0	f40300aa	mov	x20, x0
0x4a8c4	c00640f9	ldr	x0, [x22, #0x8]
0x4a8c8	a00700b5	cbnz	x0, 0x4a9bc <_WeChatMain+0x31150>
0x4a8cc	48100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a8d0	09614d39	ldrb	w9, [x8, #0x358]
0x4a8d4	09040037	tbnz	w9, #0x0, 0x4a954 <_WeChatMain+0x310e8>
0x4a8d8	090080d2	mov	x9, #0x0                ; =0
0x4a8dc	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x4a8e0	aa9999f2	movk	x10, #0xcccd
0x4a8e4	6b028092	mov	x11, #-0x14             ; =-20
0x4a8e8	ec2104f0	adrp	x12, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4a8ec	8c812391	add	x12, x12, #0x8e0
0x4a8f0	4085040f	movi.4h	v0, #0x8a
0x4a8f4	4d100590	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a8f8	adc90b91	add	x13, x13, #0x2f2
0x4a8fc	2e7dca9b	umulh	x14, x9, x10
0x4a900	cefd44d3	lsr	x14, x14, #4
0x4a904	8f01098b	add	x15, x12, x9
0x4a908	ce3d0b9b	madd	x14, x14, x11, x15
0x4a90c	efe51791	add	x15, x15, #0x5f9
0x4a910	ce951791	add	x14, x14, #0x5e5
0x4a914	e10140bd	ldr	s1, [x15]
0x4a918	0110212e	uaddw.8h	v1, v0, v1
0x4a91c	c20140bd	ldr	s2, [x14]
0x4a920	42a4082f	ushll.8h	v2, v2, #0x0
0x4a924	211c222e	eor.8b	v1, v1, v2
0x4a928	2118000e	uzp1.8b	v1, v1, v0
0x4a92c	a16929bc	str	s1, [x13, x9]
0x4a930	29110091	add	x9, x9, #0x4
0x4a934	3f9101f1	cmp	x9, #0x64
0x4a938	21feff54	b.ne	0x4a8fc <_WeChatMain+0x31090>
0x4a93c	49100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a940	29590d91	add	x9, x9, #0x356
0x4a944	0a0d8052	mov	w10, #0x68              ; =104
0x4a948	2a010079	strh	w10, [x9]
0x4a94c	29008052	mov	w9, #0x1                ; =1
0x4a950	09610d39	strb	w9, [x8, #0x358]
0x4a954	48100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a958	09b54d39	ldrb	w9, [x8, #0x36d]
0x4a95c	89010037	tbnz	w9, #0x0, 0x4a98c <_WeChatMain+0x31120>
0x4a960	c92104b0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4a964	209d47fd	ldr	d0, [x9, #0xf38]
0x4a968	49100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a96c	29810d91	add	x9, x9, #0x360
0x4a970	200100fd	str	d0, [x9]
0x4a974	ca2104b0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4a978	40a147fd	ldr	d0, [x10, #0xf40]
0x4a97c	200900bd	str	s0, [x9, #0x8]
0x4a980	3f310039	strb	wzr, [x9, #0xc]
0x4a984	29008052	mov	w9, #0x1                ; =1
0x4a988	09b50d39	strb	w9, [x8, #0x36d]
0x4a98c	40100590	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a990	00c80b91	add	x0, x0, #0x2f2
0x4a994	42100590	adrp	x2, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4a998	42800d91	add	x2, x2, #0x360
0x4a99c	e8230091	add	x8, sp, #0x8
0x4a9a0	a1128052	mov	w1, #0x95               ; =149
0x4a9a4	683fff97	bl	0x1a744 <_WeChatMain+0xed8>
0x4a9a8	e0230091	add	x0, sp, #0x8
0x4a9ac	ad3fff97	bl	0x1a860 <_WeChatMain+0xff4>
0x4a9b0	e0230091	add	x0, sp, #0x8
0x4a9b4	ae3fff97	bl	0x1a86c <_WeChatMain+0x1000>
0x4a9b8	c00640f9	ldr	x0, [x22, #0x8]
0x4a9bc	e2030094	bl	0x4b944 <_WeChatMain+0x320d8>
0x4a9c0	e10300aa	mov	x1, x0
0x4a9c4	e00314aa	mov	x0, x20
0x4a9c8	e20315aa	mov	x2, x21
0x4a9cc	bffaff97	bl	0x494c8 <_WeChatMain+0x2fc5c>
0x4a9d0	68d704d0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4a9d4	08e13891	add	x8, x8, #0xe38
0x4a9d8	880200f9	str	x8, [x20]
0x4a9dc	9f1e00f9	str	xzr, [x20, #0x38]
0x4a9e0	e80314aa	mov	x8, x20
0x4a9e4	1f0d03f8	str	xzr, [x8, #0x30]!
0x4a9e8	881600f9	str	x8, [x20, #0x28]
0x4a9ec	740200f9	str	x20, [x19]
0x4a9f0	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4a9f4	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4a9f8	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4a9fc	ff030191	add	sp, sp, #0x40
0x4aa00	c0035fd6	ret
0x4aa04	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x4aa08	fa6701a9	stp	x26, x25, [sp, #0x10]
0x4aa0c	f85f02a9	stp	x24, x23, [sp, #0x20]
0x4aa10	f65703a9	stp	x22, x21, [sp, #0x30]
0x4aa14	f44f04a9	stp	x20, x19, [sp, #0x40]
0x4aa18	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x4aa1c	fd430191	add	x29, sp, #0x50
0x4aa20	f30301aa	mov	x19, x1
0x4aa24	f40300aa	mov	x20, x0
0x4aa28	280040f9	ldr	x8, [x1]
0x4aa2c	081140f9	ldr	x8, [x8, #0x20]
0x4aa30	e00301aa	mov	x0, x1
0x4aa34	00013fd6	blr	x8
0x4aa38	1f140071	cmp	w0, #0x5
0x4aa3c	20070054	b.eq	0x4ab20 <_WeChatMain+0x312b4>
0x4aa40	881a40f9	ldr	x8, [x20, #0x30]
0x4aa44	e80600b4	cbz	x8, 0x4ab20 <_WeChatMain+0x312b4>
0x4aa48	150540f9	ldr	x21, [x8, #0x8]
0x4aa4c	b50600b4	cbz	x21, 0x4ab20 <_WeChatMain+0x312b4>
0x4aa50	170080d2	mov	x23, #0x0               ; =0
0x4aa54	78c20091	add	x24, x19, #0x30
0x4aa58	0e000014	b	0x4aa90 <_WeChatMain+0x31224>
0x4aa5c	601a40f9	ldr	x0, [x19, #0x30]
0x4aa60	b765ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x4aa64	681e40f9	ldr	x8, [x19, #0x38]
0x4aa68	08050091	add	x8, x8, #0x1
0x4aa6c	681e00f9	str	x8, [x19, #0x38]
0x4aa70	c0a20091	add	x0, x22, #0x28
0x4aa74	e10315aa	mov	x1, x21
0x4aa78	4cccff97	bl	0x3dba8 <_WeChatMain+0x2433c>
0x4aa7c	f7060091	add	x23, x23, #0x1
0x4aa80	881a40f9	ldr	x8, [x20, #0x30]
0x4aa84	0911178b	add	x9, x8, x23, lsl #4
0x4aa88	350540f9	ldr	x21, [x9, #0x8]
0x4aa8c	b50400b4	cbz	x21, 0x4ab20 <_WeChatMain+0x312b4>
0x4aa90	eaee7cd3	lsl	x10, x23, #4
0x4aa94	090340f9	ldr	x9, [x24]
0x4aa98	19696ab8	ldr	w25, [x8, x10]
0x4aa9c	fa0318aa	mov	x26, x24
0x4aaa0	f60318aa	mov	x22, x24
0x4aaa4	a90000b5	cbnz	x9, 0x4aab8 <_WeChatMain+0x3124c>
0x4aaa8	0d000014	b	0x4aadc <_WeChatMain+0x31270>
0x4aaac	c90240f9	ldr	x9, [x22]
0x4aab0	fa0316aa	mov	x26, x22
0x4aab4	490100b4	cbz	x9, 0x4aadc <_WeChatMain+0x31270>
0x4aab8	f60309aa	mov	x22, x9
0x4aabc	282140b9	ldr	w8, [x9, #0x20]
0x4aac0	3f03086b	cmp	w25, w8
0x4aac4	4bffff54	b.lt	0x4aaac <_WeChatMain+0x31240>
0x4aac8	1f01196b	cmp	w8, w25
0x4aacc	2afdff54	b.ge	0x4aa70 <_WeChatMain+0x31204>
0x4aad0	c90640f9	ldr	x9, [x22, #0x8]
0x4aad4	29ffffb5	cbnz	x9, 0x4aab8 <_WeChatMain+0x3124c>
0x4aad8	da220091	add	x26, x22, #0x8
0x4aadc	fb0316aa	mov	x27, x22
0x4aae0	00088052	mov	w0, #0x40               ; =64
0x4aae4	53d5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4aae8	f60300aa	mov	x22, x0
0x4aaec	192000b9	str	w25, [x0, #0x20]
0x4aaf0	1f7c03a9	stp	xzr, xzr, [x0, #0x30]
0x4aaf4	1f1400f9	str	xzr, [x0, #0x28]
0x4aaf8	1f7c00a9	stp	xzr, xzr, [x0]
0x4aafc	1b0800f9	str	x27, [x0, #0x10]
0x4ab00	400300f9	str	x0, [x26]
0x4ab04	681640f9	ldr	x8, [x19, #0x28]
0x4ab08	080140f9	ldr	x8, [x8]
0x4ab0c	e10300aa	mov	x1, x0
0x4ab10	68faffb4	cbz	x8, 0x4aa5c <_WeChatMain+0x311f0>
0x4ab14	681600f9	str	x8, [x19, #0x28]
0x4ab18	410340f9	ldr	x1, [x26]
0x4ab1c	d0ffff17	b	0x4aa5c <_WeChatMain+0x311f0>
0x4ab20	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x4ab24	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x4ab28	f65743a9	ldp	x22, x21, [sp, #0x30]
0x4ab2c	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x4ab30	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x4ab34	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x4ab38	c0035fd6	ret
0x4ab3c	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x4ab40	fa6701a9	stp	x26, x25, [sp, #0x10]
0x4ab44	f85f02a9	stp	x24, x23, [sp, #0x20]
0x4ab48	f65703a9	stp	x22, x21, [sp, #0x30]
0x4ab4c	f44f04a9	stp	x20, x19, [sp, #0x40]
0x4ab50	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x4ab54	fd430191	add	x29, sp, #0x50
0x4ab58	16a040a9	ldp	x22, x8, [x0, #0x8]
0x4ab5c	f50316aa	mov	x21, x22
0x4ab60	090116cb	sub	x9, x8, x22
0x4ab64	3f0889eb	cmp	x1, x9, asr #2
0x4ab68	89030054	b.ls	0x4abd8 <_WeChatMain+0x3136c>
0x4ab6c	130040f9	ldr	x19, [x0]
0x4ab70	d70213cb	sub	x23, x22, x19
0x4ab74	f9fe4293	asr	x25, x23, #2
0x4ab78	2903018b	add	x9, x25, x1
0x4ab7c	2afd7ed3	lsr	x10, x9, #62
0x4ab80	ea0f00b5	cbnz	x10, 0x4ad7c <_WeChatMain+0x31510>
0x4ab84	eaf37eb2	mov	x10, #0x7ffffffffffffffc ; =9223372036854775804
0x4ab88	140113cb	sub	x20, x8, x19
0x4ab8c	88fe4193	asr	x8, x20, #1
0x4ab90	1f0109eb	cmp	x8, x9
0x4ab94	0881899a	csel	x8, x8, x9, hi
0x4ab98	9f020aeb	cmp	x20, x10
0x4ab9c	0900f892	mov	x9, #0x3fffffffffffffff ; =4611686018427387903
0x4aba0	1831899a	csel	x24, x8, x9, lo
0x4aba4	d80400b4	cbz	x24, 0x4ac3c <_WeChatMain+0x313d0>
0x4aba8	08ff7ed3	lsr	x8, x24, #62
0x4abac	a80e00b5	cbnz	x8, 0x4ad80 <_WeChatMain+0x31514>
0x4abb0	fa0302aa	mov	x26, x2
0x4abb4	fb0301aa	mov	x27, x1
0x4abb8	fc0300aa	mov	x28, x0
0x4abbc	00f77ed3	lsl	x0, x24, #2
0x4abc0	1cd5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4abc4	e80300aa	mov	x8, x0
0x4abc8	e0031caa	mov	x0, x28
0x4abcc	e1031baa	mov	x1, x27
0x4abd0	e2031aaa	mov	x2, x26
0x4abd4	1b000014	b	0x4ac40 <_WeChatMain+0x313d4>
0x4abd8	e10200b4	cbz	x1, 0x4ac34 <_WeChatMain+0x313c8>
0x4abdc	c80a018b	add	x8, x22, x1, lsl #2
0x4abe0	490040b9	ldr	w9, [x2]
0x4abe4	2a0400d1	sub	x10, x1, #0x1
0x4abe8	4af54092	and	x10, x10, #0x3fffffffffffffff
0x4abec	5f3d00f1	cmp	x10, #0xf
0x4abf0	a3010054	b.lo	0x4ac24 <_WeChatMain+0x313b8>
0x4abf4	4a050091	add	x10, x10, #0x1
0x4abf8	4be97c92	and	x11, x10, #0x7ffffffffffffff0
0x4abfc	d50a0b8b	add	x21, x22, x11, lsl #2
0x4ac00	200d044e	dup.4s	v0, w9
0x4ac04	cc820091	add	x12, x22, #0x20
0x4ac08	ed030baa	mov	x13, x11
0x4ac0c	80013fad	stp	q0, q0, [x12, #-0x20]
0x4ac10	800182ac	stp	q0, q0, [x12], #0x40
0x4ac14	ad4100f1	subs	x13, x13, #0x10
0x4ac18	a1ffff54	b.ne	0x4ac0c <_WeChatMain+0x313a0>
0x4ac1c	5f010beb	cmp	x10, x11
0x4ac20	80000054	b.eq	0x4ac30 <_WeChatMain+0x313c4>
0x4ac24	a94600b8	str	w9, [x21], #0x4
0x4ac28	bf0208eb	cmp	x21, x8
0x4ac2c	c1ffff54	b.ne	0x4ac24 <_WeChatMain+0x313b8>
0x4ac30	f50308aa	mov	x21, x8
0x4ac34	150400f9	str	x21, [x0, #0x8]
0x4ac38	4a000014	b	0x4ad60 <_WeChatMain+0x314f4>
0x4ac3c	080080d2	mov	x8, #0x0                ; =0
0x4ac40	0a09198b	add	x10, x8, x25, lsl #2
0x4ac44	4909018b	add	x9, x10, x1, lsl #2
0x4ac48	4b0040b9	ldr	w11, [x2]
0x4ac4c	2c0400d1	sub	x12, x1, #0x1
0x4ac50	8df54092	and	x13, x12, #0x3fffffffffffffff
0x4ac54	ec030aaa	mov	x12, x10
0x4ac58	bf3d00f1	cmp	x13, #0xf
0x4ac5c	a3010054	b.lo	0x4ac90 <_WeChatMain+0x31424>
0x4ac60	ad050091	add	x13, x13, #0x1
0x4ac64	aee97c92	and	x14, x13, #0x7ffffffffffffff0
0x4ac68	4c090e8b	add	x12, x10, x14, lsl #2
0x4ac6c	600d044e	dup.4s	v0, w11
0x4ac70	4f810091	add	x15, x10, #0x20
0x4ac74	f0030eaa	mov	x16, x14
0x4ac78	e0013fad	stp	q0, q0, [x15, #-0x20]
0x4ac7c	e00182ac	stp	q0, q0, [x15], #0x40
0x4ac80	104200f1	subs	x16, x16, #0x10
0x4ac84	a1ffff54	b.ne	0x4ac78 <_WeChatMain+0x3140c>
0x4ac88	bf010eeb	cmp	x13, x14
0x4ac8c	80000054	b.eq	0x4ac9c <_WeChatMain+0x31430>
0x4ac90	8b4500b8	str	w11, [x12], #0x4
0x4ac94	9f0109eb	cmp	x12, x9
0x4ac98	c1ffff54	b.ne	0x4ac90 <_WeChatMain+0x31424>
0x4ac9c	0b09188b	add	x11, x8, x24, lsl #2
0x4aca0	cc0213eb	subs	x12, x22, x19
0x4aca4	40040054	b.eq	0x4ad2c <_WeChatMain+0x314c0>
0x4aca8	8c1100d1	sub	x12, x12, #0x4
0x4acac	9ff100f1	cmp	x12, #0x3c
0x4acb0	23030054	b.lo	0x4ad14 <_WeChatMain+0x314a8>
0x4acb4	e802088b	add	x8, x23, x8
0x4acb8	c80208cb	sub	x8, x22, x8
0x4acbc	1f0101f1	cmp	x8, #0x40
0x4acc0	a3020054	b.lo	0x4ad14 <_WeChatMain+0x314a8>
0x4acc4	88fd42d3	lsr	x8, x12, #2
0x4acc8	0c050091	add	x12, x8, #0x1
0x4accc	8de97c92	and	x13, x12, #0x7ffffffffffffff0
0x4acd0	a8f57ed3	lsl	x8, x13, #2
0x4acd4	d50208cb	sub	x21, x22, x8
0x4acd8	480108cb	sub	x8, x10, x8
0x4acdc	ce8200d1	sub	x14, x22, #0x20
0x4ace0	4a8100d1	sub	x10, x10, #0x20
0x4ace4	ef030daa	mov	x15, x13
0x4ace8	c10140ad	ldp	q1, q0, [x14]
0x4acec	c3097fad	ldp	q3, q2, [x14, #-0x20]
0x4acf0	410100ad	stp	q1, q0, [x10]
0x4acf4	43093fad	stp	q3, q2, [x10, #-0x20]
0x4acf8	ce0101d1	sub	x14, x14, #0x40
0x4acfc	4a0101d1	sub	x10, x10, #0x40
0x4ad00	ef4100d1	sub	x15, x15, #0x10
0x4ad04	2fffffb5	cbnz	x15, 0x4ace8 <_WeChatMain+0x3147c>
0x4ad08	ea0308aa	mov	x10, x8
0x4ad0c	9f010deb	cmp	x12, x13
0x4ad10	00010054	b.eq	0x4ad30 <_WeChatMain+0x314c4>
0x4ad14	e8030aaa	mov	x8, x10
0x4ad18	aace5fb8	ldr	w10, [x21, #-0x4]!
0x4ad1c	0acd1fb8	str	w10, [x8, #-0x4]!
0x4ad20	bf0213eb	cmp	x21, x19
0x4ad24	a1ffff54	b.ne	0x4ad18 <_WeChatMain+0x314ac>
0x4ad28	02000014	b	0x4ad30 <_WeChatMain+0x314c4>
0x4ad2c	e8030aaa	mov	x8, x10
0x4ad30	082400a9	stp	x8, x9, [x0]
0x4ad34	0b0800f9	str	x11, [x0, #0x10]
0x4ad38	530100b4	cbz	x19, 0x4ad60 <_WeChatMain+0x314f4>
0x4ad3c	e00313aa	mov	x0, x19
0x4ad40	e10314aa	mov	x1, x20
0x4ad44	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x4ad48	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x4ad4c	f65743a9	ldp	x22, x21, [sp, #0x30]
0x4ad50	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x4ad54	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x4ad58	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x4ad5c	acd4c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4ad60	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x4ad64	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x4ad68	f65743a9	ldp	x22, x21, [sp, #0x30]
0x4ad6c	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x4ad70	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x4ad74	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x4ad78	c0035fd6	ret
0x4ad7c	22eeff97	bl	0x46604 <_WeChatMain+0x2cd98>
0x4ad80	7363ff97	bl	0x23b4c <_WeChatMain+0xa2e0>
0x4ad84	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4ad88	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4ad8c	fd430091	add	x29, sp, #0x10
0x4ad90	00048052	mov	w0, #0x20               ; =32
0x4ad94	a7d4c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4ad98	f30300aa	mov	x19, x0
0x4ad9c	81008052	mov	w1, #0x4                ; =4
0x4ada0	b1edff97	bl	0x46464 <_WeChatMain+0x2cbf8>
0x4ada4	082440a9	ldp	x8, x9, [x0]
0x4ada8	290108cb	sub	x9, x9, x8
0x4adac	2afd4293	asr	x10, x9, #2
0x4adb0	490500d1	sub	x9, x10, #0x1
0x4adb4	3f0900f1	cmp	x9, #0x2
0x4adb8	63080054	b.lo	0x4aec4 <_WeChatMain+0x31658>
0x4adbc	4b0d00d1	sub	x11, x10, #0x3
0x4adc0	6001639e	ucvtf	d0, x11
0x4adc4	4c0900d1	sub	x12, x10, #0x2
0x4adc8	9f1100f1	cmp	x12, #0x4
0x4adcc	62000054	b.hs	0x4add8 <_WeChatMain+0x3156c>
0x4add0	2b008052	mov	w11, #0x1               ; =1
0x4add4	2b000014	b	0x4ae80 <_WeChatMain+0x31614>
0x4add8	8df57e92	and	x13, x12, #0xfffffffffffffffc
0x4addc	210d084e	dup.2d	v1, x9
0x4ade0	0204084e	dup.2d	v2, v0[0]
0x4ade4	ab0140b2	orr	x11, x13, #0x1
0x4ade8	ee2104f0	adrp	x14, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4adec	c31dc23d	ldr	q3, [x14, #0x870]
0x4adf0	ee2104f0	adrp	x14, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4adf4	c419c23d	ldr	q4, [x14, #0x860]
0x4adf8	0e110091	add	x14, x8, #0x4
0x4adfc	e5e7076f	movi.2d	v5, #0xffffffffffffffff
0x4ae00	06f4036f	fmov.2d	v6, #0.50000000
0x4ae04	8f008052	mov	w15, #0x4               ; =4
0x4ae08	e70d084e	dup.2d	v7, x15
0x4ae0c	ef030daa	mov	x15, x13
0x4ae10	9058206e	mvn.16b	v16, v4
0x4ae14	7158206e	mvn.16b	v17, v3
0x4ae18	3184f14e	add.2d	v17, v1, v17
0x4ae1c	3084f04e	add.2d	v16, v1, v16
0x4ae20	10da616e	ucvtf.2d	v16, v16
0x4ae24	31da616e	ucvtf.2d	v17, v17
0x4ae28	9284e54e	add.2d	v18, v4, v5
0x4ae2c	7384e54e	add.2d	v19, v3, v5
0x4ae30	73da616e	ucvtf.2d	v19, v19
0x4ae34	52da616e	ucvtf.2d	v18, v18
0x4ae38	52d6724e	fadd.2d	v18, v18, v18
0x4ae3c	73d6734e	fadd.2d	v19, v19, v19
0x4ae40	71d6714e	fadd.2d	v17, v19, v17
0x4ae44	50d6704e	fadd.2d	v16, v18, v16
0x4ae48	10fe626e	fdiv.2d	v16, v16, v2
0x4ae4c	31fe626e	fdiv.2d	v17, v17, v2
0x4ae50	31d6664e	fadd.2d	v17, v17, v6
0x4ae54	10d6664e	fadd.2d	v16, v16, v6
0x4ae58	10bae14e	fcvtzs.2d	v16, v16
0x4ae5c	31bae14e	fcvtzs.2d	v17, v17
0x4ae60	101a914e	uzp1.4s	v16, v16, v17
0x4ae64	d005813c	str	q16, [x14], #0x10
0x4ae68	6384e74e	add.2d	v3, v3, v7
0x4ae6c	8484e74e	add.2d	v4, v4, v7
0x4ae70	ef1100f1	subs	x15, x15, #0x4
0x4ae74	e1fcff54	b.ne	0x4ae10 <_WeChatMain+0x315a4>
0x4ae78	9f010deb	cmp	x12, x13
0x4ae7c	40020054	b.eq	0x4aec4 <_WeChatMain+0x31658>
0x4ae80	4a010bcb	sub	x10, x10, x11
0x4ae84	4a0900d1	sub	x10, x10, #0x2
0x4ae88	0c090b8b	add	x12, x8, x11, lsl #2
0x4ae8c	6b0500d1	sub	x11, x11, #0x1
0x4ae90	01106c1e	fmov	d1, #0.50000000
0x4ae94	4201639e	ucvtf	d2, x10
0x4ae98	6301639e	ucvtf	d3, x11
0x4ae9c	6328631e	fadd	d3, d3, d3
0x4aea0	6228621e	fadd	d2, d3, d2
0x4aea4	4218601e	fdiv	d2, d2, d0
0x4aea8	4228611e	fadd	d2, d2, d1
0x4aeac	4d00781e	fcvtzs	w13, d2
0x4aeb0	8d4500b8	str	w13, [x12], #0x4
0x4aeb4	4a0500d1	sub	x10, x10, #0x1
0x4aeb8	6b050091	add	x11, x11, #0x1
0x4aebc	5f0500b1	cmn	x10, #0x1
0x4aec0	a1feff54	b.ne	0x4ae94 <_WeChatMain+0x31628>
0x4aec4	0a220490	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4aec8	4a410091	add	x10, x10, #0x10
0x4aecc	4a0140b9	ldr	w10, [x10]
0x4aed0	0a7929b8	str	w10, [x8, x9, lsl #2]
0x4aed4	e00313aa	mov	x0, x19
0x4aed8	9eedff97	bl	0x46550 <_WeChatMain+0x2cce4>
0x4aedc	e00313aa	mov	x0, x19
0x4aee0	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4aee4	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4aee8	c0035fd6	ret
0x4aeec	ff0301d1	sub	sp, sp, #0x40
0x4aef0	f65701a9	stp	x22, x21, [sp, #0x10]
0x4aef4	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4aef8	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4aefc	fdc30091	add	x29, sp, #0x30
0x4af00	f50301aa	mov	x21, x1
0x4af04	f60300aa	mov	x22, x0
0x4af08	f30308aa	mov	x19, x8
0x4af0c	00088052	mov	w0, #0x40               ; =64
0x4af10	48d4c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4af14	f40300aa	mov	x20, x0
0x4af18	c00640f9	ldr	x0, [x22, #0x8]
0x4af1c	a00700b5	cbnz	x0, 0x4b010 <_WeChatMain+0x317a4>
0x4af20	48100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4af24	09614d39	ldrb	w9, [x8, #0x358]
0x4af28	09040037	tbnz	w9, #0x0, 0x4afa8 <_WeChatMain+0x3173c>
0x4af2c	090080d2	mov	x9, #0x0                ; =0
0x4af30	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x4af34	aa9999f2	movk	x10, #0xcccd
0x4af38	6b028092	mov	x11, #-0x14             ; =-20
0x4af3c	ec2104f0	adrp	x12, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4af40	8c812391	add	x12, x12, #0x8e0
0x4af44	4085040f	movi.4h	v0, #0x8a
0x4af48	4d100590	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4af4c	adc90b91	add	x13, x13, #0x2f2
0x4af50	2e7dca9b	umulh	x14, x9, x10
0x4af54	cefd44d3	lsr	x14, x14, #4
0x4af58	8f01098b	add	x15, x12, x9
0x4af5c	ce3d0b9b	madd	x14, x14, x11, x15
0x4af60	efe51791	add	x15, x15, #0x5f9
0x4af64	ce951791	add	x14, x14, #0x5e5
0x4af68	e10140bd	ldr	s1, [x15]
0x4af6c	0110212e	uaddw.8h	v1, v0, v1
0x4af70	c20140bd	ldr	s2, [x14]
0x4af74	42a4082f	ushll.8h	v2, v2, #0x0
0x4af78	211c222e	eor.8b	v1, v1, v2
0x4af7c	2118000e	uzp1.8b	v1, v1, v0
0x4af80	a16929bc	str	s1, [x13, x9]
0x4af84	29110091	add	x9, x9, #0x4
0x4af88	3f9101f1	cmp	x9, #0x64
0x4af8c	21feff54	b.ne	0x4af50 <_WeChatMain+0x316e4>
0x4af90	49100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4af94	29590d91	add	x9, x9, #0x356
0x4af98	0a0d8052	mov	w10, #0x68              ; =104
0x4af9c	2a010079	strh	w10, [x9]
0x4afa0	29008052	mov	w9, #0x1                ; =1
0x4afa4	09610d39	strb	w9, [x8, #0x358]
0x4afa8	48100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4afac	09b54d39	ldrb	w9, [x8, #0x36d]
0x4afb0	89010037	tbnz	w9, #0x0, 0x4afe0 <_WeChatMain+0x31774>
0x4afb4	c92104b0	adrp	x9, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4afb8	209d47fd	ldr	d0, [x9, #0xf38]
0x4afbc	49100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4afc0	29810d91	add	x9, x9, #0x360
0x4afc4	200100fd	str	d0, [x9]
0x4afc8	ca2104b0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4afcc	40a147fd	ldr	d0, [x10, #0xf40]
0x4afd0	200900bd	str	s0, [x9, #0x8]
0x4afd4	3f310039	strb	wzr, [x9, #0xc]
0x4afd8	29008052	mov	w9, #0x1                ; =1
0x4afdc	09b50d39	strb	w9, [x8, #0x36d]
0x4afe0	40100590	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4afe4	00c80b91	add	x0, x0, #0x2f2
0x4afe8	42100590	adrp	x2, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4afec	42800d91	add	x2, x2, #0x360
0x4aff0	e8230091	add	x8, sp, #0x8
0x4aff4	a1128052	mov	w1, #0x95               ; =149
0x4aff8	d33dff97	bl	0x1a744 <_WeChatMain+0xed8>
0x4affc	e0230091	add	x0, sp, #0x8
0x4b000	183eff97	bl	0x1a860 <_WeChatMain+0xff4>
0x4b004	e0230091	add	x0, sp, #0x8
0x4b008	193eff97	bl	0x1a86c <_WeChatMain+0x1000>
0x4b00c	c00640f9	ldr	x0, [x22, #0x8]
0x4b010	4d020094	bl	0x4b944 <_WeChatMain+0x320d8>
0x4b014	e10300aa	mov	x1, x0
0x4b018	e00314aa	mov	x0, x20
0x4b01c	e20315aa	mov	x2, x21
0x4b020	2af9ff97	bl	0x494c8 <_WeChatMain+0x2fc5c>
0x4b024	e80314aa	mov	x8, x20
0x4b028	1f0d03f8	str	xzr, [x8, #0x30]!
0x4b02c	9f1e00f9	str	xzr, [x20, #0x38]
0x4b030	881600f9	str	x8, [x20, #0x28]
0x4b034	68d704b0	adrp	x8, 0x9b38000 <_wxam_enc_uninit_10+0x9b38000>
0x4b038	08e13b91	add	x8, x8, #0xef8
0x4b03c	880200f9	str	x8, [x20]
0x4b040	740200f9	str	x20, [x19]
0x4b044	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4b048	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4b04c	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4b050	ff030191	add	sp, sp, #0x40
0x4b054	c0035fd6	ret
0x4b058	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4b05c	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4b060	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4b064	fd830091	add	x29, sp, #0x20
0x4b068	f30308aa	mov	x19, x8
0x4b06c	1f080071	cmp	w0, #0x2
0x4b070	ec030054	b.gt	0x4b0ec <_WeChatMain+0x31880>
0x4b074	40070034	cbz	w0, 0x4b15c <_WeChatMain+0x318f0>
0x4b078	1f040071	cmp	w0, #0x1
0x4b07c	e00f0054	b.eq	0x4b278 <_WeChatMain+0x31a0c>
0x4b080	1f080071	cmp	w0, #0x2
0x4b084	e10c0054	b.ne	0x4b220 <_WeChatMain+0x319b4>
0x4b088	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b08c	09c94e39	ldrb	w9, [x8, #0x3b2]
0x4b090	49010037	tbnz	w9, #0x0, 0x4b0b8 <_WeChatMain+0x3184c>
0x4b094	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b098	29810e91	add	x9, x9, #0x3a0
0x4b09c	ea2104d0	adrp	x10, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4b0a0	40e5c33d	ldr	q0, [x10, #0xf90]
0x4b0a4	2001803d	str	q0, [x9]
0x4b0a8	aa098052	mov	w10, #0x4d              ; =77
0x4b0ac	2a210079	strh	w10, [x9, #0x10]
0x4b0b0	29008052	mov	w9, #0x1                ; =1
0x4b0b4	09c90e39	strb	w9, [x8, #0x3b2]
0x4b0b8	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b0bc	00800e91	add	x0, x0, #0x3a0
0x4b0c0	4edac395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b0c4	08018092	mov	x8, #-0x9               ; =-9
0x4b0c8	e8ffeff2	movk	x8, #0x7fff, lsl #48
0x4b0cc	1f0008eb	cmp	x0, x8
0x4b0d0	a81f0054	b.hi	0x4b4c4 <_WeChatMain+0x31c58>
0x4b0d4	f40300aa	mov	x20, x0
0x4b0d8	1f5c00f1	cmp	x0, #0x17
0x4b0dc	c2170054	b.hs	0x4b3d4 <_WeChatMain+0x31b68>
0x4b0e0	745e0039	strb	w20, [x19, #0x17]
0x4b0e4	d41800b5	cbnz	x20, 0x4b3fc <_WeChatMain+0x31b90>
0x4b0e8	f1000014	b	0x4b4ac <_WeChatMain+0x31c40>
0x4b0ec	1f0c0071	cmp	w0, #0x3
0x4b0f0	80060054	b.eq	0x4b1c0 <_WeChatMain+0x31954>
0x4b0f4	1f100071	cmp	w0, #0x4
0x4b0f8	000f0054	b.eq	0x4b2d8 <_WeChatMain+0x31a6c>
0x4b0fc	1f140071	cmp	w0, #0x5
0x4b100	01090054	b.ne	0x4b220 <_WeChatMain+0x319b4>
0x4b104	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b108	09415039	ldrb	w9, [x8, #0x410]
0x4b10c	e9000037	tbnz	w9, #0x0, 0x4b128 <_WeChatMain+0x318bc>
0x4b110	e92104d0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4b114	20d9c33d	ldr	q0, [x9, #0xf60]
0x4b118	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b11c	2001813d	str	q0, [x9, #0x400]
0x4b120	29008052	mov	w9, #0x1                ; =1
0x4b124	09411039	strb	w9, [x8, #0x410]
0x4b128	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b12c	00001091	add	x0, x0, #0x400
0x4b130	32dac395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b134	08018092	mov	x8, #-0x9               ; =-9
0x4b138	e8ffeff2	movk	x8, #0x7fff, lsl #48
0x4b13c	1f0008eb	cmp	x0, x8
0x4b140	281c0054	b.hi	0x4b4c4 <_WeChatMain+0x31c58>
0x4b144	f40300aa	mov	x20, x0
0x4b148	1f5c00f1	cmp	x0, #0x17
0x4b14c	e2150054	b.hs	0x4b408 <_WeChatMain+0x31b9c>
0x4b150	745e0039	strb	w20, [x19, #0x17]
0x4b154	f41600b5	cbnz	x20, 0x4b430 <_WeChatMain+0x31bc4>
0x4b158	d5000014	b	0x4b4ac <_WeChatMain+0x31c40>
0x4b15c	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b160	09e94d39	ldrb	w9, [x8, #0x37a]
0x4b164	49010037	tbnz	w9, #0x0, 0x4b18c <_WeChatMain+0x31920>
0x4b168	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b16c	29c10d91	add	x9, x9, #0x370
0x4b170	ea2104d0	adrp	x10, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4b174	40e147fd	ldr	d0, [x10, #0xfc0]
0x4b178	200100fd	str	d0, [x9]
0x4b17c	aa098052	mov	w10, #0x4d              ; =77
0x4b180	2a110079	strh	w10, [x9, #0x8]
0x4b184	29008052	mov	w9, #0x1                ; =1
0x4b188	09e90d39	strb	w9, [x8, #0x37a]
0x4b18c	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b190	00c00d91	add	x0, x0, #0x370
0x4b194	19dac395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b198	08018092	mov	x8, #-0x9               ; =-9
0x4b19c	e8ffeff2	movk	x8, #0x7fff, lsl #48
0x4b1a0	1f0008eb	cmp	x0, x8
0x4b1a4	08190054	b.hi	0x4b4c4 <_WeChatMain+0x31c58>
0x4b1a8	f40300aa	mov	x20, x0
0x4b1ac	1f5c00f1	cmp	x0, #0x17
0x4b1b0	420c0054	b.hs	0x4b338 <_WeChatMain+0x31acc>
0x4b1b4	745e0039	strb	w20, [x19, #0x17]
0x4b1b8	540d00b5	cbnz	x20, 0x4b360 <_WeChatMain+0x31af4>
0x4b1bc	bc000014	b	0x4b4ac <_WeChatMain+0x31c40>
0x4b1c0	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b1c4	09454f39	ldrb	w9, [x8, #0x3d1]
0x4b1c8	29010037	tbnz	w9, #0x0, 0x4b1ec <_WeChatMain+0x31980>
0x4b1cc	e92104d0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4b1d0	20e1c33d	ldr	q0, [x9, #0xf80]
0x4b1d4	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b1d8	29010f91	add	x9, x9, #0x3c0
0x4b1dc	2001803d	str	q0, [x9]
0x4b1e0	3f410039	strb	wzr, [x9, #0x10]
0x4b1e4	29008052	mov	w9, #0x1                ; =1
0x4b1e8	09450f39	strb	w9, [x8, #0x3d1]
0x4b1ec	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b1f0	00000f91	add	x0, x0, #0x3c0
0x4b1f4	01dac395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b1f8	08018092	mov	x8, #-0x9               ; =-9
0x4b1fc	e8ffeff2	movk	x8, #0x7fff, lsl #48
0x4b200	1f0008eb	cmp	x0, x8
0x4b204	08160054	b.hi	0x4b4c4 <_WeChatMain+0x31c58>
0x4b208	f40300aa	mov	x20, x0
0x4b20c	1f5c00f1	cmp	x0, #0x17
0x4b210	e20a0054	b.hs	0x4b36c <_WeChatMain+0x31b00>
0x4b214	745e0039	strb	w20, [x19, #0x17]
0x4b218	f40b00b5	cbnz	x20, 0x4b394 <_WeChatMain+0x31b28>
0x4b21c	a4000014	b	0x4b4ac <_WeChatMain+0x31c40>
0x4b220	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b224	09815039	ldrb	w9, [x8, #0x420]
0x4b228	e9000037	tbnz	w9, #0x0, 0x4b244 <_WeChatMain+0x319d8>
0x4b22c	a92104b0	adrp	x9, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x4b230	20bd44fd	ldr	d0, [x9, #0x978]
0x4b234	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b238	200d02fd	str	d0, [x9, #0x418]
0x4b23c	29008052	mov	w9, #0x1                ; =1
0x4b240	09811039	strb	w9, [x8, #0x420]
0x4b244	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b248	00601091	add	x0, x0, #0x418
0x4b24c	ebd9c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b250	08018092	mov	x8, #-0x9               ; =-9
0x4b254	e8ffeff2	movk	x8, #0x7fff, lsl #48
0x4b258	1f0008eb	cmp	x0, x8
0x4b25c	48130054	b.hi	0x4b4c4 <_WeChatMain+0x31c58>
0x4b260	f40300aa	mov	x20, x0
0x4b264	1f5c00f1	cmp	x0, #0x17
0x4b268	c2090054	b.hs	0x4b3a0 <_WeChatMain+0x31b34>
0x4b26c	745e0039	strb	w20, [x19, #0x17]
0x4b270	d40a00b5	cbnz	x20, 0x4b3c8 <_WeChatMain+0x31b5c>
0x4b274	8e000014	b	0x4b4ac <_WeChatMain+0x31c40>
0x4b278	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b27c	09454e39	ldrb	w9, [x8, #0x391]
0x4b280	29010037	tbnz	w9, #0x0, 0x4b2a4 <_WeChatMain+0x31a38>
0x4b284	e92104d0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4b288	20e9c33d	ldr	q0, [x9, #0xfa0]
0x4b28c	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b290	29010e91	add	x9, x9, #0x380
0x4b294	2001803d	str	q0, [x9]
0x4b298	3f410039	strb	wzr, [x9, #0x10]
0x4b29c	29008052	mov	w9, #0x1                ; =1
0x4b2a0	09450e39	strb	w9, [x8, #0x391]
0x4b2a4	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b2a8	00000e91	add	x0, x0, #0x380
0x4b2ac	d3d9c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b2b0	08018092	mov	x8, #-0x9               ; =-9
0x4b2b4	e8ffeff2	movk	x8, #0x7fff, lsl #48
0x4b2b8	1f0008eb	cmp	x0, x8
0x4b2bc	48100054	b.hi	0x4b4c4 <_WeChatMain+0x31c58>
0x4b2c0	f40300aa	mov	x20, x0
0x4b2c4	1f5c00f1	cmp	x0, #0x17
0x4b2c8	a20b0054	b.hs	0x4b43c <_WeChatMain+0x31bd0>
0x4b2cc	745e0039	strb	w20, [x19, #0x17]
0x4b2d0	b40c00b5	cbnz	x20, 0x4b464 <_WeChatMain+0x31bf8>
0x4b2d4	76000014	b	0x4b4ac <_WeChatMain+0x31c40>
0x4b2d8	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b2dc	09c54f39	ldrb	w9, [x8, #0x3f1]
0x4b2e0	29010037	tbnz	w9, #0x0, 0x4b304 <_WeChatMain+0x31a98>
0x4b2e4	e92104d0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4b2e8	20ddc33d	ldr	q0, [x9, #0xf70]
0x4b2ec	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b2f0	29810f91	add	x9, x9, #0x3e0
0x4b2f4	2001803d	str	q0, [x9]
0x4b2f8	3f410039	strb	wzr, [x9, #0x10]
0x4b2fc	29008052	mov	w9, #0x1                ; =1
0x4b300	09c50f39	strb	w9, [x8, #0x3f1]
0x4b304	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b308	00800f91	add	x0, x0, #0x3e0
0x4b30c	bbd9c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b310	08018092	mov	x8, #-0x9               ; =-9
0x4b314	e8ffeff2	movk	x8, #0x7fff, lsl #48
0x4b318	1f0008eb	cmp	x0, x8
0x4b31c	480d0054	b.hi	0x4b4c4 <_WeChatMain+0x31c58>
0x4b320	f40300aa	mov	x20, x0
0x4b324	1f5c00f1	cmp	x0, #0x17
0x4b328	420a0054	b.hs	0x4b470 <_WeChatMain+0x31c04>
0x4b32c	745e0039	strb	w20, [x19, #0x17]
0x4b330	540b00b5	cbnz	x20, 0x4b498 <_WeChatMain+0x31c2c>
0x4b334	5e000014	b	0x4b4ac <_WeChatMain+0x31c40>
0x4b338	880a40b2	orr	x8, x20, #0x7
0x4b33c	1f5d00f1	cmp	x8, #0x17
0x4b340	29038052	mov	w9, #0x19               ; =25
0x4b344	3505889a	csinc	x21, x9, x8, eq
0x4b348	e00315aa	mov	x0, x21
0x4b34c	39d3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4b350	a80241b2	orr	x8, x21, #0x8000000000000000
0x4b354	74a200a9	stp	x20, x8, [x19, #0x8]
0x4b358	600200f9	str	x0, [x19]
0x4b35c	f30300aa	mov	x19, x0
0x4b360	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b364	21c00d91	add	x1, x1, #0x370
0x4b368	4e000014	b	0x4b4a0 <_WeChatMain+0x31c34>
0x4b36c	880a40b2	orr	x8, x20, #0x7
0x4b370	1f5d00f1	cmp	x8, #0x17
0x4b374	29038052	mov	w9, #0x19               ; =25
0x4b378	3505889a	csinc	x21, x9, x8, eq
0x4b37c	e00315aa	mov	x0, x21
0x4b380	2cd3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4b384	a80241b2	orr	x8, x21, #0x8000000000000000
0x4b388	74a200a9	stp	x20, x8, [x19, #0x8]
0x4b38c	600200f9	str	x0, [x19]
0x4b390	f30300aa	mov	x19, x0
0x4b394	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b398	21000f91	add	x1, x1, #0x3c0
0x4b39c	41000014	b	0x4b4a0 <_WeChatMain+0x31c34>
0x4b3a0	880a40b2	orr	x8, x20, #0x7
0x4b3a4	1f5d00f1	cmp	x8, #0x17
0x4b3a8	29038052	mov	w9, #0x19               ; =25
0x4b3ac	3505889a	csinc	x21, x9, x8, eq
0x4b3b0	e00315aa	mov	x0, x21
0x4b3b4	1fd3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4b3b8	a80241b2	orr	x8, x21, #0x8000000000000000
0x4b3bc	74a200a9	stp	x20, x8, [x19, #0x8]
0x4b3c0	600200f9	str	x0, [x19]
0x4b3c4	f30300aa	mov	x19, x0
0x4b3c8	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b3cc	21601091	add	x1, x1, #0x418
0x4b3d0	34000014	b	0x4b4a0 <_WeChatMain+0x31c34>
0x4b3d4	880a40b2	orr	x8, x20, #0x7
0x4b3d8	1f5d00f1	cmp	x8, #0x17
0x4b3dc	29038052	mov	w9, #0x19               ; =25
0x4b3e0	3505889a	csinc	x21, x9, x8, eq
0x4b3e4	e00315aa	mov	x0, x21
0x4b3e8	12d3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4b3ec	a80241b2	orr	x8, x21, #0x8000000000000000
0x4b3f0	74a200a9	stp	x20, x8, [x19, #0x8]
0x4b3f4	600200f9	str	x0, [x19]
0x4b3f8	f30300aa	mov	x19, x0
0x4b3fc	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b400	21800e91	add	x1, x1, #0x3a0
0x4b404	27000014	b	0x4b4a0 <_WeChatMain+0x31c34>
0x4b408	880a40b2	orr	x8, x20, #0x7
0x4b40c	1f5d00f1	cmp	x8, #0x17
0x4b410	29038052	mov	w9, #0x19               ; =25
0x4b414	3505889a	csinc	x21, x9, x8, eq
0x4b418	e00315aa	mov	x0, x21
0x4b41c	05d3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4b420	a80241b2	orr	x8, x21, #0x8000000000000000
0x4b424	74a200a9	stp	x20, x8, [x19, #0x8]
0x4b428	600200f9	str	x0, [x19]
0x4b42c	f30300aa	mov	x19, x0
0x4b430	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b434	21001091	add	x1, x1, #0x400
0x4b438	1a000014	b	0x4b4a0 <_WeChatMain+0x31c34>
0x4b43c	880a40b2	orr	x8, x20, #0x7
0x4b440	1f5d00f1	cmp	x8, #0x17
0x4b444	29038052	mov	w9, #0x19               ; =25
0x4b448	3505889a	csinc	x21, x9, x8, eq
0x4b44c	e00315aa	mov	x0, x21
0x4b450	f8d2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4b454	a80241b2	orr	x8, x21, #0x8000000000000000
0x4b458	74a200a9	stp	x20, x8, [x19, #0x8]
0x4b45c	600200f9	str	x0, [x19]
0x4b460	f30300aa	mov	x19, x0
0x4b464	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b468	21000e91	add	x1, x1, #0x380
0x4b46c	0d000014	b	0x4b4a0 <_WeChatMain+0x31c34>
0x4b470	880a40b2	orr	x8, x20, #0x7
0x4b474	1f5d00f1	cmp	x8, #0x17
0x4b478	29038052	mov	w9, #0x19               ; =25
0x4b47c	3505889a	csinc	x21, x9, x8, eq
0x4b480	e00315aa	mov	x0, x21
0x4b484	ebd2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4b488	a80241b2	orr	x8, x21, #0x8000000000000000
0x4b48c	74a200a9	stp	x20, x8, [x19, #0x8]
0x4b490	600200f9	str	x0, [x19]
0x4b494	f30300aa	mov	x19, x0
0x4b498	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b49c	21800f91	add	x1, x1, #0x3e0
0x4b4a0	e00313aa	mov	x0, x19
0x4b4a4	e20314aa	mov	x2, x20
0x4b4a8	78d6c395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x4b4ac	6802148b	add	x8, x19, x20
0x4b4b0	1f010039	strb	wzr, [x8]
0x4b4b4	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4b4b8	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4b4bc	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4b4c0	c0035fd6	ret
0x4b4c4	e00313aa	mov	x0, x19
0x4b4c8	ed3dff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x4b4cc	68d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4b4d0	08410691	add	x8, x8, #0x190
0x4b4d4	080400a9	stp	x8, x1, [x0]
0x4b4d8	1f1000b9	str	wzr, [x0, #0x10]
0x4b4dc	c0035fd6	ret
0x4b4e0	200020d4	brk	#0x1
0x4b4e4	200020d4	brk	#0x1
0x4b4e8	c0035fd6	ret
0x4b4ec	08400091	add	x8, x0, #0x10
0x4b4f0	083121b8	ldset	w1, w8, [x8]
0x4b4f4	c0035fd6	ret
0x4b4f8	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4b4fc	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4b500	fd430091	add	x29, sp, #0x10
0x4b504	f30300aa	mov	x19, x0
0x4b508	e00301aa	mov	x0, x1
0x4b50c	77660194	bl	0xa4ee8 <_WeChatMain+0x8b67c>
0x4b510	e88361b2	mov	x8, #-0x80000000        ; =-2147483648
0x4b514	1f0008eb	cmp	x0, x8
0x4b518	08c0889a	csel	x8, x0, x8, gt
0x4b51c	0900b012	mov	w9, #0x7fffffff         ; =2147483647
0x4b520	1f0109eb	cmp	x8, x9
0x4b524	01b1899a	csel	x1, x8, x9, lt
0x4b528	680240f9	ldr	x8, [x19]
0x4b52c	021940f9	ldr	x2, [x8, #0x30]
0x4b530	e00313aa	mov	x0, x19
0x4b534	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4b538	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4b53c	40001fd6	br	x2
0x4b540	080040f9	ldr	x8, [x0]
0x4b544	021940f9	ldr	x2, [x8, #0x30]
0x4b548	40001fd6	br	x2
0x4b54c	00008052	mov	w0, #0x0                ; =0
0x4b550	c0035fd6	ret
0x4b554	c0035fd6	ret
0x4b558	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4b55c	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4b560	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4b564	fd830091	add	x29, sp, #0x20
0x4b568	f30301aa	mov	x19, x1
0x4b56c	f40300aa	mov	x20, x0
0x4b570	882605b0	adrp	x8, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x4b574	08813091	add	x8, x8, #0xc20
0x4b578	160140f9	ldr	x22, [x8]
0x4b57c	360100b4	cbz	x22, 0x4b5a0 <_WeChatMain+0x31d34>
0x4b580	885640a9	ldp	x8, x21, [x20]
0x4b584	080d40f9	ldr	x8, [x8, #0x18]
0x4b588	e00314aa	mov	x0, x20
0x4b58c	00013fd6	blr	x8
0x4b590	e10300aa	mov	x1, x0
0x4b594	e00315aa	mov	x0, x21
0x4b598	e20313aa	mov	x2, x19
0x4b59c	c0023fd6	blr	x22
0x4b5a0	881240b9	ldr	w8, [x20, #0x10]
0x4b5a4	a8002837	tbnz	w8, #0x5, 0x4b5b8 <_WeChatMain+0x31d4c>
0x4b5a8	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4b5ac	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4b5b0	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4b5b4	c0035fd6	ret
0x4b5b8	885640a9	ldp	x8, x21, [x20]
0x4b5bc	080d40f9	ldr	x8, [x8, #0x18]
0x4b5c0	e00314aa	mov	x0, x20
0x4b5c4	00013fd6	blr	x8
0x4b5c8	e10300aa	mov	x1, x0
0x4b5cc	e00315aa	mov	x0, x21
0x4b5d0	e20313aa	mov	x2, x19
0x4b5d4	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4b5d8	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4b5dc	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4b5e0	a6210014	b	0x53c78 <_WeChatMain+0x3a40c>
0x4b5e4	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b5e8	2ab95039	ldrb	w10, [x9, #0x42e]
0x4b5ec	0a010037	tbnz	w10, #0x0, 0x4b60c <_WeChatMain+0x31da0>
0x4b5f0	2a1005f0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b5f4	4aad1091	add	x10, x10, #0x42b
0x4b5f8	ab848c52	mov	w11, #0x6425            ; =25637
0x4b5fc	4b010079	strh	w11, [x10]
0x4b600	5f090039	strb	wzr, [x10, #0x2]
0x4b604	2a008052	mov	w10, #0x1               ; =1
0x4b608	2ab91039	strb	w10, [x9, #0x42e]
0x4b60c	ff8300d1	sub	sp, sp, #0x20
0x4b610	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4b614	fd430091	add	x29, sp, #0x10
0x4b618	e10300f9	str	x1, [sp]
0x4b61c	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b620	00ac1091	add	x0, x0, #0x42b
0x4b624	57720094	bl	0x67f80 <_WeChatMain+0x4e714>
0x4b628	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4b62c	ff830091	add	sp, sp, #0x20
0x4b630	c0035fd6	ret
0x4b634	ff4301d1	sub	sp, sp, #0x50
0x4b638	f65702a9	stp	x22, x21, [sp, #0x20]
0x4b63c	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4b640	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4b644	fd030191	add	x29, sp, #0x40
0x4b648	f30301aa	mov	x19, x1
0x4b64c	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4b650	e82301a9	stp	x8, x8, [sp, #0x10]
0x4b654	e80700f9	str	x8, [sp, #0x8]
0x4b658	080040f9	ldr	x8, [x0]
0x4b65c	093d40f9	ldr	x9, [x8, #0x78]
0x4b660	e8230091	add	x8, sp, #0x8
0x4b664	20013fd6	blr	x9
0x4b668	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b66c	09ed5039	ldrb	w9, [x8, #0x43b]
0x4b670	69010037	tbnz	w9, #0x0, 0x4b69c <_WeChatMain+0x31e30>
0x4b674	e92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4b678	200140fd	ldr	d0, [x9]
0x4b67c	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b680	29d11091	add	x9, x9, #0x434
0x4b684	200100bd	str	s0, [x9]
0x4b688	aa4c8e52	mov	w10, #0x7265            ; =29285
0x4b68c	2a090079	strh	w10, [x9, #0x4]
0x4b690	3f190039	strb	wzr, [x9, #0x6]
0x4b694	29008052	mov	w9, #0x1                ; =1
0x4b698	09ed1039	strb	w9, [x8, #0x43b]
0x4b69c	341005f0	adrp	x20, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b6a0	94d21091	add	x20, x20, #0x434
0x4b6a4	e00314aa	mov	x0, x20
0x4b6a8	d4d8c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b6ac	e20300aa	mov	x2, x0
0x4b6b0	e0230091	add	x0, sp, #0x8
0x4b6b4	e10314aa	mov	x1, x20
0x4b6b8	af6f0194	bl	0xa7574 <_WeChatMain+0x8dd08>
0x4b6bc	085c4039	ldrb	w8, [x0, #0x17]
0x4b6c0	091d0013	sxtb	w9, w8
0x4b6c4	0a2c40a9	ldp	x10, x11, [x0]
0x4b6c8	3f010071	cmp	w9, #0x0
0x4b6cc	47b1809a	csel	x7, x10, x0, lt
0x4b6d0	66b1889a	csel	x6, x11, x8, lt
0x4b6d4	685e8039	ldrsb	x8, [x19, #0x17]
0x4b6d8	8800f8b7	tbnz	x8, #0x3f, 0x4b6e8 <_WeChatMain+0x31e7c>
0x4b6dc	c1028052	mov	w1, #0x16               ; =22
0x4b6e0	f40308aa	mov	x20, x8
0x4b6e4	04000014	b	0x4b6f4 <_WeChatMain+0x31e88>
0x4b6e8	74a640a9	ldp	x20, x9, [x19, #0x8]
0x4b6ec	29f94092	and	x9, x9, #0x7fffffffffffffff
0x4b6f0	210500d1	sub	x1, x9, #0x1
0x4b6f4	290014cb	sub	x9, x1, x20
0x4b6f8	3f0106eb	cmp	x9, x6
0x4b6fc	22010054	b.hs	0x4b720 <_WeChatMain+0x31eb4>
0x4b700	c80001cb	sub	x8, x6, x1
0x4b704	0201148b	add	x2, x8, x20
0x4b708	e00313aa	mov	x0, x19
0x4b70c	e30314aa	mov	x3, x20
0x4b710	e40314aa	mov	x4, x20
0x4b714	050080d2	mov	x5, #0x0                ; =0
0x4b718	27d0c395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x4b71c	12000014	b	0x4b764 <_WeChatMain+0x31ef8>
0x4b720	260200b4	cbz	x6, 0x4b764 <_WeChatMain+0x31ef8>
0x4b724	f50313aa	mov	x21, x19
0x4b728	4800f836	tbz	w8, #0x1f, 0x4b730 <_WeChatMain+0x31ec4>
0x4b72c	750240f9	ldr	x21, [x19]
0x4b730	a002148b	add	x0, x21, x20
0x4b734	e10307aa	mov	x1, x7
0x4b738	e20306aa	mov	x2, x6
0x4b73c	f60306aa	mov	x22, x6
0x4b740	d5d5c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4b744	8802168b	add	x8, x20, x22
0x4b748	695ec039	ldrsb	w9, [x19, #0x17]
0x4b74c	8900f837	tbnz	w9, #0x1f, 0x4b75c <_WeChatMain+0x31ef0>
0x4b750	09190012	and	w9, w8, #0x7f
0x4b754	695e0039	strb	w9, [x19, #0x17]
0x4b758	02000014	b	0x4b760 <_WeChatMain+0x31ef4>
0x4b75c	680600f9	str	x8, [x19, #0x8]
0x4b760	bf6a2838	strb	wzr, [x21, x8]
0x4b764	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b768	09f95039	ldrb	w9, [x8, #0x43e]
0x4b76c	e9000037	tbnz	w9, #0x0, 0x4b788 <_WeChatMain+0x31f1c>
0x4b770	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b774	29f11091	add	x9, x9, #0x43c
0x4b778	4a018052	mov	w10, #0xa               ; =10
0x4b77c	2a010079	strh	w10, [x9]
0x4b780	29008052	mov	w9, #0x1                ; =1
0x4b784	09f91039	strb	w9, [x8, #0x43e]
0x4b788	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b78c	00f01091	add	x0, x0, #0x43c
0x4b790	9ad8c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b794	f40300aa	mov	x20, x0
0x4b798	685e8039	ldrsb	x8, [x19, #0x17]
0x4b79c	8800f8b7	tbnz	x8, #0x3f, 0x4b7ac <_WeChatMain+0x31f40>
0x4b7a0	c1028052	mov	w1, #0x16               ; =22
0x4b7a4	f50308aa	mov	x21, x8
0x4b7a8	04000014	b	0x4b7b8 <_WeChatMain+0x31f4c>
0x4b7ac	75a640a9	ldp	x21, x9, [x19, #0x8]
0x4b7b0	29f94092	and	x9, x9, #0x7fffffffffffffff
0x4b7b4	210500d1	sub	x1, x9, #0x1
0x4b7b8	290015cb	sub	x9, x1, x21
0x4b7bc	3f0114eb	cmp	x9, x20
0x4b7c0	82010054	b.hs	0x4b7f0 <_WeChatMain+0x31f84>
0x4b7c4	880201cb	sub	x8, x20, x1
0x4b7c8	271005f0	adrp	x7, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b7cc	e7f01091	add	x7, x7, #0x43c
0x4b7d0	0201158b	add	x2, x8, x21
0x4b7d4	e00313aa	mov	x0, x19
0x4b7d8	e30315aa	mov	x3, x21
0x4b7dc	e40315aa	mov	x4, x21
0x4b7e0	050080d2	mov	x5, #0x0                ; =0
0x4b7e4	e60314aa	mov	x6, x20
0x4b7e8	f3cfc395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x4b7ec	12000014	b	0x4b834 <_WeChatMain+0x31fc8>
0x4b7f0	340200b4	cbz	x20, 0x4b834 <_WeChatMain+0x31fc8>
0x4b7f4	f60313aa	mov	x22, x19
0x4b7f8	4800f836	tbz	w8, #0x1f, 0x4b800 <_WeChatMain+0x31f94>
0x4b7fc	760240f9	ldr	x22, [x19]
0x4b800	211005f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b804	21f01091	add	x1, x1, #0x43c
0x4b808	c002158b	add	x0, x22, x21
0x4b80c	e20314aa	mov	x2, x20
0x4b810	a1d5c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4b814	a802148b	add	x8, x21, x20
0x4b818	695ec039	ldrsb	w9, [x19, #0x17]
0x4b81c	8900f837	tbnz	w9, #0x1f, 0x4b82c <_WeChatMain+0x31fc0>
0x4b820	09190012	and	w9, w8, #0x7f
0x4b824	695e0039	strb	w9, [x19, #0x17]
0x4b828	02000014	b	0x4b830 <_WeChatMain+0x31fc4>
0x4b82c	680600f9	str	x8, [x19, #0x8]
0x4b830	df6a2838	strb	wzr, [x22, x8]
0x4b834	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b838	09155139	ldrb	w9, [x8, #0x445]
0x4b83c	29010037	tbnz	w9, #0x0, 0x4b860 <_WeChatMain+0x31ff4>
0x4b840	e92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4b844	200540fd	ldr	d0, [x9, #0x8]
0x4b848	291005f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b84c	29011191	add	x9, x9, #0x440
0x4b850	200100bd	str	s0, [x9]
0x4b854	3f110039	strb	wzr, [x9, #0x4]
0x4b858	29008052	mov	w9, #0x1                ; =1
0x4b85c	09151139	strb	w9, [x8, #0x445]
0x4b860	341005f0	adrp	x20, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b864	94021191	add	x20, x20, #0x440
0x4b868	e00314aa	mov	x0, x20
0x4b86c	63d8c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4b870	e20300aa	mov	x2, x0
0x4b874	e0230091	add	x0, sp, #0x8
0x4b878	e10314aa	mov	x1, x20
0x4b87c	3e6f0194	bl	0xa7574 <_WeChatMain+0x8dd08>
0x4b880	085c4039	ldrb	w8, [x0, #0x17]
0x4b884	091d0013	sxtb	w9, w8
0x4b888	0a2c40a9	ldp	x10, x11, [x0]
0x4b88c	3f010071	cmp	w9, #0x0
0x4b890	47b1809a	csel	x7, x10, x0, lt
0x4b894	66b1889a	csel	x6, x11, x8, lt
0x4b898	685e8039	ldrsb	x8, [x19, #0x17]
0x4b89c	8800f8b7	tbnz	x8, #0x3f, 0x4b8ac <_WeChatMain+0x32040>
0x4b8a0	c1028052	mov	w1, #0x16               ; =22
0x4b8a4	f40308aa	mov	x20, x8
0x4b8a8	04000014	b	0x4b8b8 <_WeChatMain+0x3204c>
0x4b8ac	74a640a9	ldp	x20, x9, [x19, #0x8]
0x4b8b0	29f94092	and	x9, x9, #0x7fffffffffffffff
0x4b8b4	210500d1	sub	x1, x9, #0x1
0x4b8b8	290014cb	sub	x9, x1, x20
0x4b8bc	3f0106eb	cmp	x9, x6
0x4b8c0	22010054	b.hs	0x4b8e4 <_WeChatMain+0x32078>
0x4b8c4	c80001cb	sub	x8, x6, x1
0x4b8c8	0201148b	add	x2, x8, x20
0x4b8cc	e00313aa	mov	x0, x19
0x4b8d0	e30314aa	mov	x3, x20
0x4b8d4	e40314aa	mov	x4, x20
0x4b8d8	050080d2	mov	x5, #0x0                ; =0
0x4b8dc	b6cfc395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x4b8e0	12000014	b	0x4b928 <_WeChatMain+0x320bc>
0x4b8e4	260200b4	cbz	x6, 0x4b928 <_WeChatMain+0x320bc>
0x4b8e8	f50313aa	mov	x21, x19
0x4b8ec	4800f836	tbz	w8, #0x1f, 0x4b8f4 <_WeChatMain+0x32088>
0x4b8f0	750240f9	ldr	x21, [x19]
0x4b8f4	a002148b	add	x0, x21, x20
0x4b8f8	e10307aa	mov	x1, x7
0x4b8fc	e20306aa	mov	x2, x6
0x4b900	f60306aa	mov	x22, x6
0x4b904	64d5c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4b908	8802168b	add	x8, x20, x22
0x4b90c	695ec039	ldrsb	w9, [x19, #0x17]
0x4b910	8900f837	tbnz	w9, #0x1f, 0x4b920 <_WeChatMain+0x320b4>
0x4b914	09190012	and	w9, w8, #0x7f
0x4b918	695e0039	strb	w9, [x19, #0x17]
0x4b91c	02000014	b	0x4b924 <_WeChatMain+0x320b8>
0x4b920	680600f9	str	x8, [x19, #0x8]
0x4b924	bf6a2838	strb	wzr, [x21, x8]
0x4b928	e0230091	add	x0, sp, #0x8
0x4b92c	106e0194	bl	0xa716c <_WeChatMain+0x8d900>
0x4b930	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4b934	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4b938	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4b93c	ff430191	add	sp, sp, #0x50
0x4b940	c0035fd6	ret
0x4b944	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4b948	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4b94c	fd430091	add	x29, sp, #0x10
0x4b950	f30300aa	mov	x19, x0
0x4b954	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b958	08211191	add	x8, x8, #0x448
0x4b95c	08c1bf38	ldaprb	w8, [x8]
0x4b960	a8030036	tbz	w8, #0x0, 0x4b9d4 <_WeChatMain+0x32168>
0x4b964	281005f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b968	08411191	add	x8, x8, #0x450
0x4b96c	08c1bf38	ldaprb	w8, [x8]
0x4b970	68030036	tbz	w8, #0x0, 0x4b9dc <_WeChatMain+0x32170>
0x4b974	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b978	00c01191	add	x0, x0, #0x470
0x4b97c	ded6c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x4b980	20020035	cbnz	w0, 0x4b9c4 <_WeChatMain+0x32158>
0x4b984	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b988	00601191	add	x0, x0, #0x458
0x4b98c	e10313aa	mov	x1, x19
0x4b990	e20313aa	mov	x2, x19
0x4b994	14000094	bl	0x4b9e4 <_WeChatMain+0x32178>
0x4b998	13800091	add	x19, x0, #0x20
0x4b99c	08dcc039	ldrsb	w8, [x0, #0x37]
0x4b9a0	4800f836	tbz	w8, #0x1f, 0x4b9a8 <_WeChatMain+0x3213c>
0x4b9a4	730240f9	ldr	x19, [x19]
0x4b9a8	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b9ac	00c01191	add	x0, x0, #0x470
0x4b9b0	d4d6c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x4b9b4	e00313aa	mov	x0, x19
0x4b9b8	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4b9bc	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4b9c0	c0035fd6	ret
0x4b9c4	201005f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4b9c8	00c01191	add	x0, x0, #0x470
0x4b9cc	ae7a0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x4b9d0	edffff17	b	0x4b984 <_WeChatMain+0x32118>
0x4b9d4	45f6c195	bl	0x70c92e8 <_SetWeixinCallbackFunc+0x22e1eec>
0x4b9d8	e3ffff17	b	0x4b964 <_WeChatMain+0x320f8>
0x4b9dc	56f6c195	bl	0x70c9334 <_SetWeixinCallbackFunc+0x22e1f38>
0x4b9e0	e5ffff17	b	0x4b974 <_WeChatMain+0x32108>
0x4b9e4	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x4b9e8	f85f01a9	stp	x24, x23, [sp, #0x10]
0x4b9ec	f65702a9	stp	x22, x21, [sp, #0x20]
0x4b9f0	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4b9f4	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4b9f8	fd030191	add	x29, sp, #0x40
0x4b9fc	f40302aa	mov	x20, x2
0x4ba00	f30300aa	mov	x19, x0
0x4ba04	f60300aa	mov	x22, x0
0x4ba08	c88e40f8	ldr	x8, [x22, #0x8]!
0x4ba0c	e80500b4	cbz	x8, 0x4bac8 <_WeChatMain+0x3225c>
0x4ba10	295c4039	ldrb	w9, [x1, #0x17]
0x4ba14	2a1d0013	sxtb	w10, w9
0x4ba18	2b3040a9	ldp	x11, x12, [x1]
0x4ba1c	5f010071	cmp	w10, #0x0
0x4ba20	75b1819a	csel	x21, x11, x1, lt
0x4ba24	99b1899a	csel	x25, x12, x9, lt
0x4ba28	04000014	b	0x4ba38 <_WeChatMain+0x321cc>
0x4ba2c	080340f9	ldr	x8, [x24]
0x4ba30	f60318aa	mov	x22, x24
0x4ba34	c80400b4	cbz	x8, 0x4bacc <_WeChatMain+0x32260>
0x4ba38	f80308aa	mov	x24, x8
0x4ba3c	090d42f8	ldr	x9, [x8, #0x20]!
0x4ba40	0a5d4039	ldrb	w10, [x8, #0x17]
0x4ba44	4b1d0013	sxtb	w11, w10
0x4ba48	0c0540f9	ldr	x12, [x8, #0x8]
0x4ba4c	7f010071	cmp	w11, #0x0
0x4ba50	36b1889a	csel	x22, x9, x8, lt
0x4ba54	9ab18a9a	csel	x26, x12, x10, lt
0x4ba58	5f0319eb	cmp	x26, x25
0x4ba5c	5733999a	csel	x23, x26, x25, lo
0x4ba60	e00315aa	mov	x0, x21
0x4ba64	e10316aa	mov	x1, x22
0x4ba68	e20317aa	mov	x2, x23
0x4ba6c	04d5c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x4ba70	3f031aeb	cmp	x25, x26
0x4ba74	e8279f1a	cset	w8, lo
0x4ba78	1f000071	cmp	w0, #0x0
0x4ba7c	e9a79f1a	cset	w9, lt
0x4ba80	0801891a	csel	w8, w8, w9, eq
0x4ba84	1f050071	cmp	w8, #0x1
0x4ba88	20fdff54	b.eq	0x4ba2c <_WeChatMain+0x321c0>
0x4ba8c	e00316aa	mov	x0, x22
0x4ba90	e10315aa	mov	x1, x21
0x4ba94	e20317aa	mov	x2, x23
0x4ba98	f9d4c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x4ba9c	5f0319eb	cmp	x26, x25
0x4baa0	e8279f1a	cset	w8, lo
0x4baa4	1f000071	cmp	w0, #0x0
0x4baa8	e9a79f1a	cset	w9, lt
0x4baac	0801891a	csel	w8, w8, w9, eq
0x4bab0	1f050071	cmp	w8, #0x1
0x4bab4	61040054	b.ne	0x4bb40 <_WeChatMain+0x322d4>
0x4bab8	080740f9	ldr	x8, [x24, #0x8]
0x4babc	e8fbffb5	cbnz	x8, 0x4ba38 <_WeChatMain+0x321cc>
0x4bac0	16230091	add	x22, x24, #0x8
0x4bac4	02000014	b	0x4bacc <_WeChatMain+0x32260>
0x4bac8	f80316aa	mov	x24, x22
0x4bacc	00078052	mov	w0, #0x38               ; =56
0x4bad0	58d1c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4bad4	f50300aa	mov	x21, x0
0x4bad8	885ec039	ldrsb	w8, [x20, #0x17]
0x4badc	c800f837	tbnz	w8, #0x1f, 0x4baf4 <_WeChatMain+0x32288>
0x4bae0	8002c03d	ldr	q0, [x20]
0x4bae4	a002823c	stur	q0, [x21, #0x20]
0x4bae8	880a40f9	ldr	x8, [x20, #0x10]
0x4baec	a80203f8	stur	x8, [x21, #0x30]
0x4baf0	04000014	b	0x4bb00 <_WeChatMain+0x32294>
0x4baf4	810a40a9	ldp	x1, x2, [x20]
0x4baf8	a0820091	add	x0, x21, #0x20
0x4bafc	8934ff97	bl	0x18d20 <__text+0x1d20>
0x4bb00	bf7e00a9	stp	xzr, xzr, [x21]
0x4bb04	b80a00f9	str	x24, [x21, #0x10]
0x4bb08	d50200f9	str	x21, [x22]
0x4bb0c	680240f9	ldr	x8, [x19]
0x4bb10	080140f9	ldr	x8, [x8]
0x4bb14	e10315aa	mov	x1, x21
0x4bb18	680000b4	cbz	x8, 0x4bb24 <_WeChatMain+0x322b8>
0x4bb1c	680200f9	str	x8, [x19]
0x4bb20	c10240f9	ldr	x1, [x22]
0x4bb24	600640f9	ldr	x0, [x19, #0x8]
0x4bb28	8561ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x4bb2c	680a40f9	ldr	x8, [x19, #0x10]
0x4bb30	08050091	add	x8, x8, #0x1
0x4bb34	680a00f9	str	x8, [x19, #0x10]
0x4bb38	21008052	mov	w1, #0x1                ; =1
0x4bb3c	03000014	b	0x4bb48 <_WeChatMain+0x322dc>
0x4bb40	010080d2	mov	x1, #0x0                ; =0
0x4bb44	f50318aa	mov	x21, x24
0x4bb48	e00315aa	mov	x0, x21
0x4bb4c	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4bb50	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4bb54	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4bb58	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x4bb5c	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x4bb60	c0035fd6	ret
0x4bb64	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bb68	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bb6c	fd430091	add	x29, sp, #0x10
0x4bb70	f30301aa	mov	x19, x1
0x4bb74	21008052	mov	w1, #0x1                ; =1
0x4bb78	ddf8ff97	bl	0x49eec <_WeChatMain+0x30680>
0x4bb7c	080040f9	ldr	x8, [x0]
0x4bb80	021940f9	ldr	x2, [x8, #0x30]
0x4bb84	e10313aa	mov	x1, x19
0x4bb88	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bb8c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bb90	40001fd6	br	x2
0x4bb94	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bb98	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bb9c	fd430091	add	x29, sp, #0x10
0x4bba0	f30301aa	mov	x19, x1
0x4bba4	21008052	mov	w1, #0x1                ; =1
0x4bba8	fef8ff97	bl	0x49fa0 <_WeChatMain+0x30734>
0x4bbac	080040f9	ldr	x8, [x0]
0x4bbb0	021940f9	ldr	x2, [x8, #0x30]
0x4bbb4	e10313aa	mov	x1, x19
0x4bbb8	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bbbc	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bbc0	40001fd6	br	x2
0x4bbc4	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bbc8	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bbcc	fd430091	add	x29, sp, #0x10
0x4bbd0	f30301aa	mov	x19, x1
0x4bbd4	48040011	add	w8, w2, #0x1
0x4bbd8	037d4093	sxtw	x3, w8
0x4bbdc	21008052	mov	w1, #0x1                ; =1
0x4bbe0	24008052	mov	w4, #0x1                ; =1
0x4bbe4	27f8ff97	bl	0x49c80 <_WeChatMain+0x30414>
0x4bbe8	080040f9	ldr	x8, [x0]
0x4bbec	021940f9	ldr	x2, [x8, #0x30]
0x4bbf0	e10313aa	mov	x1, x19
0x4bbf4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bbf8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bbfc	40001fd6	br	x2
0x4bc00	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bc04	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bc08	fd430091	add	x29, sp, #0x10
0x4bc0c	f30301aa	mov	x19, x1
0x4bc10	21008052	mov	w1, #0x1                ; =1
0x4bc14	027d8052	mov	w2, #0x3e8              ; =1000
0x4bc18	43068052	mov	w3, #0x32               ; =50
0x4bc1c	24008052	mov	w4, #0x1                ; =1
0x4bc20	22f3ff97	bl	0x488a8 <_WeChatMain+0x2f03c>
0x4bc24	080040f9	ldr	x8, [x0]
0x4bc28	021940f9	ldr	x2, [x8, #0x30]
0x4bc2c	e10313aa	mov	x1, x19
0x4bc30	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bc34	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bc38	40001fd6	br	x2
0x4bc3c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bc40	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bc44	fd430091	add	x29, sp, #0x10
0x4bc48	f30301aa	mov	x19, x1
0x4bc4c	21008052	mov	w1, #0x1                ; =1
0x4bc50	02e28452	mov	w2, #0x2710             ; =10000
0x4bc54	43068052	mov	w3, #0x32               ; =50
0x4bc58	24008052	mov	w4, #0x1                ; =1
0x4bc5c	06f4ff97	bl	0x48c74 <_WeChatMain+0x2f408>
0x4bc60	080040f9	ldr	x8, [x0]
0x4bc64	021940f9	ldr	x2, [x8, #0x30]
0x4bc68	e10313aa	mov	x1, x19
0x4bc6c	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bc70	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bc74	40001fd6	br	x2
0x4bc78	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bc7c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bc80	fd430091	add	x29, sp, #0x10
0x4bc84	f30301aa	mov	x19, x1
0x4bc88	21008052	mov	w1, #0x1                ; =1
0x4bc8c	02488852	mov	w2, #0x4240             ; =16960
0x4bc90	e201a072	movk	w2, #0xf, lsl #16
0x4bc94	43068052	mov	w3, #0x32               ; =50
0x4bc98	24008052	mov	w4, #0x1                ; =1
0x4bc9c	03f3ff97	bl	0x488a8 <_WeChatMain+0x2f03c>
0x4bca0	080040f9	ldr	x8, [x0]
0x4bca4	021940f9	ldr	x2, [x8, #0x30]
0x4bca8	e10313aa	mov	x1, x19
0x4bcac	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bcb0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bcb4	40001fd6	br	x2
0x4bcb8	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bcbc	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bcc0	fd430091	add	x29, sp, #0x10
0x4bcc4	f30301aa	mov	x19, x1
0x4bcc8	21008052	mov	w1, #0x1                ; =1
0x4bccc	02488852	mov	w2, #0x4240             ; =16960
0x4bcd0	e201a072	movk	w2, #0xf, lsl #16
0x4bcd4	43068052	mov	w3, #0x32               ; =50
0x4bcd8	24008052	mov	w4, #0x1                ; =1
0x4bcdc	e6f3ff97	bl	0x48c74 <_WeChatMain+0x2f408>
0x4bce0	080040f9	ldr	x8, [x0]
0x4bce4	021940f9	ldr	x2, [x8, #0x30]
0x4bce8	e10313aa	mov	x1, x19
0x4bcec	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bcf0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bcf4	40001fd6	br	x2
0x4bcf8	ff8301d1	sub	sp, sp, #0x60
0x4bcfc	f85f02a9	stp	x24, x23, [sp, #0x20]
0x4bd00	f65703a9	stp	x22, x21, [sp, #0x30]
0x4bd04	f44f04a9	stp	x20, x19, [sp, #0x40]
0x4bd08	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x4bd0c	fd430191	add	x29, sp, #0x50
0x4bd10	f30301aa	mov	x19, x1
0x4bd14	f50300aa	mov	x21, x0
0x4bd18	38d7c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4bd1c	e8ef7db2	mov	x8, #0x7ffffffffffffff8 ; =9223372036854775800
0x4bd20	1f0008eb	cmp	x0, x8
0x4bd24	a2050054	b.hs	0x4bdd8 <_WeChatMain+0x3256c>
0x4bd28	f40300aa	mov	x20, x0
0x4bd2c	1f5c00f1	cmp	x0, #0x17
0x4bd30	a2000054	b.hs	0x4bd44 <_WeChatMain+0x324d8>
0x4bd34	f47f0039	strb	w20, [sp, #0x1f]
0x4bd38	f6230091	add	x22, sp, #0x8
0x4bd3c	940100b5	cbnz	x20, 0x4bd6c <_WeChatMain+0x32500>
0x4bd40	0f000014	b	0x4bd7c <_WeChatMain+0x32510>
0x4bd44	880a40b2	orr	x8, x20, #0x7
0x4bd48	1f5d00f1	cmp	x8, #0x17
0x4bd4c	29038052	mov	w9, #0x19               ; =25
0x4bd50	3705889a	csinc	x23, x9, x8, eq
0x4bd54	e00317aa	mov	x0, x23
0x4bd58	b6d0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4bd5c	f60300aa	mov	x22, x0
0x4bd60	e80241b2	orr	x8, x23, #0x8000000000000000
0x4bd64	f42301a9	stp	x20, x8, [sp, #0x10]
0x4bd68	e00700f9	str	x0, [sp, #0x8]
0x4bd6c	e00316aa	mov	x0, x22
0x4bd70	e10315aa	mov	x1, x21
0x4bd74	e20314aa	mov	x2, x20
0x4bd78	44d4c395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x4bd7c	df6a3438	strb	wzr, [x22, x20]
0x4bd80	e0230091	add	x0, sp, #0x8
0x4bd84	21008052	mov	w1, #0x1                ; =1
0x4bd88	9c190094	bl	0x523f8 <_WeChatMain+0x38b8c>
0x4bd8c	e87fc039	ldrsb	w8, [sp, #0x1f]
0x4bd90	0801f836	tbz	w8, #0x1f, 0x4bdb0 <_WeChatMain+0x32544>
0x4bd94	e80740f9	ldr	x8, [sp, #0x8]
0x4bd98	e90f40f9	ldr	x9, [sp, #0x18]
0x4bd9c	21f94092	and	x1, x9, #0x7fffffffffffffff
0x4bda0	f40300aa	mov	x20, x0
0x4bda4	e00308aa	mov	x0, x8
0x4bda8	99d0c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4bdac	e00314aa	mov	x0, x20
0x4bdb0	080040f9	ldr	x8, [x0]
0x4bdb4	081940f9	ldr	x8, [x8, #0x30]
0x4bdb8	e10313aa	mov	x1, x19
0x4bdbc	00013fd6	blr	x8
0x4bdc0	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x4bdc4	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x4bdc8	f65743a9	ldp	x22, x21, [sp, #0x30]
0x4bdcc	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x4bdd0	ff830191	add	sp, sp, #0x60
0x4bdd4	c0035fd6	ret
0x4bdd8	e0230091	add	x0, sp, #0x8
0x4bddc	a83bff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x4bde0	08c0bfb8	ldapr	w8, [x0]
0x4bde4	1f050031	cmn	w8, #0x1
0x4bde8	e003881a	csel	w0, wzr, w8, eq
0x4bdec	c0035fd6	ret
0x4bdf0	28000013	sbfx	w8, w1, #0, #1
0x4bdf4	088028b8	swp	w8, w8, [x0]
0x4bdf8	1f050031	cmn	w8, #0x1
0x4bdfc	e003881a	csel	w0, wzr, w8, eq
0x4be00	c0035fd6	ret
0x4be04	08c0bfb8	ldapr	w8, [x0]
0x4be08	1f050031	cmn	w8, #0x1
0x4be0c	e0179f1a	cset	w0, eq
0x4be10	c0035fd6	ret
0x4be14	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4be18	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4be1c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4be20	fd830091	add	x29, sp, #0x20
0x4be24	f30302aa	mov	x19, x2
0x4be28	f40301aa	mov	x20, x1
0x4be2c	68d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4be30	08210991	add	x8, x8, #0x248
0x4be34	087c00a9	stp	x8, xzr, [x0]
0x4be38	48745e92	and	x8, x2, #0xfffffffc00000000
0x4be3c	69fd04f0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4be40	29013b91	add	x9, x9, #0xec0
0x4be44	290540f9	ldr	x9, [x9, #0x8]
0x4be48	1f0109eb	cmp	x8, x9
0x4be4c	a1000054	b.ne	0x4be60 <_WeChatMain+0x325f4>
0x4be50	f50300aa	mov	x21, x0
0x4be54	e00313aa	mov	x0, x19
0x4be58	7dceff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4be5c	e00315aa	mov	x0, x21
0x4be60	130800f9	str	x19, [x0, #0x10]
0x4be64	680240f9	ldr	x8, [x19]
0x4be68	480000b5	cbnz	x8, 0x4be70 <_WeChatMain+0x32604>
0x4be6c	740200f9	str	x20, [x19]
0x4be70	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4be74	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4be78	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4be7c	c0035fd6	ret
0x4be80	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4be84	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4be88	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4be8c	fd830091	add	x29, sp, #0x20
0x4be90	f40302aa	mov	x20, x2
0x4be94	f50301aa	mov	x21, x1
0x4be98	f30300aa	mov	x19, x0
0x4be9c	560040f9	ldr	x22, [x2]
0x4bea0	68d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4bea4	08210991	add	x8, x8, #0x248
0x4bea8	087c00a9	stp	x8, xzr, [x0]
0x4beac	c8765e92	and	x8, x22, #0xfffffffc00000000
0x4beb0	69fd04f0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4beb4	29013b91	add	x9, x9, #0xec0
0x4beb8	290540f9	ldr	x9, [x9, #0x8]
0x4bebc	1f0109eb	cmp	x8, x9
0x4bec0	61000054	b.ne	0x4becc <_WeChatMain+0x32660>
0x4bec4	e00316aa	mov	x0, x22
0x4bec8	61ceff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4becc	760a00f9	str	x22, [x19, #0x10]
0x4bed0	c80240f9	ldr	x8, [x22]
0x4bed4	480000b5	cbnz	x8, 0x4bedc <_WeChatMain+0x32670>
0x4bed8	d50200f9	str	x21, [x22]
0x4bedc	880240f9	ldr	x8, [x20]
0x4bee0	9f0200f9	str	xzr, [x20]
0x4bee4	600640f9	ldr	x0, [x19, #0x8]
0x4bee8	680600f9	str	x8, [x19, #0x8]
0x4beec	600000b4	cbz	x0, 0x4bef8 <_WeChatMain+0x3268c>
0x4bef0	01038052	mov	w1, #0x18               ; =24
0x4bef4	46d0c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4bef8	e00313aa	mov	x0, x19
0x4befc	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4bf00	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4bf04	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4bf08	c0035fd6	ret
0x4bf0c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4bf10	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4bf14	fd430091	add	x29, sp, #0x10
0x4bf18	f30300aa	mov	x19, x0
0x4bf1c	68d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4bf20	08210991	add	x8, x8, #0x248
0x4bf24	080000f9	str	x8, [x0]
0x4bf28	000840f9	ldr	x0, [x0, #0x10]
0x4bf2c	08745e92	and	x8, x0, #0xfffffffc00000000
0x4bf30	69fd04f0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4bf34	29013b91	add	x9, x9, #0xec0
0x4bf38	290540f9	ldr	x9, [x9, #0x8]
0x4bf3c	1f0109eb	cmp	x8, x9
0x4bf40	41000054	b.ne	0x4bf48 <_WeChatMain+0x326dc>
0x4bf44	dfceff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4bf48	600640f9	ldr	x0, [x19, #0x8]
0x4bf4c	7ffe00a9	stp	xzr, xzr, [x19, #0x8]
0x4bf50	600000b4	cbz	x0, 0x4bf5c <_WeChatMain+0x326f0>
0x4bf54	01038052	mov	w1, #0x18               ; =24
0x4bf58	2dd0c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4bf5c	e00313aa	mov	x0, x19
0x4bf60	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4bf64	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4bf68	c0035fd6	ret
0x4bf6c	200020d4	brk	#0x1
0x4bf70	200020d4	brk	#0x1
0x4bf74	ffc300d1	sub	sp, sp, #0x30
0x4bf78	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4bf7c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4bf80	fd830091	add	x29, sp, #0x20
0x4bf84	f30300aa	mov	x19, x0
0x4bf88	280840f9	ldr	x8, [x1, #0x10]
0x4bf8c	090540f9	ldr	x9, [x8, #0x8]
0x4bf90	081140b9	ldr	w8, [x8, #0x10]
0x4bf94	0a0840f9	ldr	x10, [x0, #0x10]
0x4bf98	4a210091	add	x10, x10, #0x8
0x4bf9c	490129f8	ldadd	x9, x9, [x10]
0x4bfa0	090840f9	ldr	x9, [x0, #0x10]
0x4bfa4	29410091	add	x9, x9, #0x10
0x4bfa8	280128b8	ldadd	w8, w8, [x9]
0x4bfac	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4bfb0	e80700f9	str	x8, [sp, #0x8]
0x4bfb4	280040f9	ldr	x8, [x1]
0x4bfb8	092140f9	ldr	x9, [x8, #0x40]
0x4bfbc	e8230091	add	x8, sp, #0x8
0x4bfc0	e00301aa	mov	x0, x1
0x4bfc4	20013fd6	blr	x9
0x4bfc8	e10740f9	ldr	x1, [sp, #0x8]
0x4bfcc	680240f9	ldr	x8, [x19]
0x4bfd0	082940f9	ldr	x8, [x8, #0x50]
0x4bfd4	e00313aa	mov	x0, x19
0x4bfd8	02008052	mov	w2, #0x0                ; =0
0x4bfdc	00013fd6	blr	x8
0x4bfe0	e00740f9	ldr	x0, [sp, #0x8]
0x4bfe4	ff0700f9	str	xzr, [sp, #0x8]
0x4bfe8	800000b4	cbz	x0, 0x4bff8 <_WeChatMain+0x3278c>
0x4bfec	080040f9	ldr	x8, [x0]
0x4bff0	080540f9	ldr	x8, [x8, #0x8]
0x4bff4	00013fd6	blr	x8
0x4bff8	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4bffc	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4c000	ffc30091	add	sp, sp, #0x30
0x4c004	c0035fd6	ret
0x4c008	080840f9	ldr	x8, [x0, #0x10]
0x4c00c	08210091	add	x8, x8, #0x8
0x4c010	080121f8	ldadd	x1, x8, [x8]
0x4c014	080840f9	ldr	x8, [x0, #0x10]
0x4c018	08410091	add	x8, x8, #0x10
0x4c01c	080122b8	ldadd	w2, w8, [x8]
0x4c020	c0035fd6	ret
0x4c024	ff0302d1	sub	sp, sp, #0x80
0x4c028	f85f04a9	stp	x24, x23, [sp, #0x40]
0x4c02c	f65705a9	stp	x22, x21, [sp, #0x50]
0x4c030	f44f06a9	stp	x20, x19, [sp, #0x60]
0x4c034	fd7b07a9	stp	x29, x30, [sp, #0x70]
0x4c038	fdc30191	add	x29, sp, #0x70
0x4c03c	f40301aa	mov	x20, x1
0x4c040	f30300aa	mov	x19, x0
0x4c044	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4c048	e81f00f9	str	x8, [sp, #0x38]
0x4c04c	e8f30132	mov	w8, #-0x55555556        ; =-1431655766
0x4c050	e83700b9	str	w8, [sp, #0x34]
0x4c054	e1e30091	add	x1, sp, #0x38
0x4c058	e00314aa	mov	x0, x20
0x4c05c	012f0094	bl	0x57c60 <_WeChatMain+0x3e3f4>
0x4c060	a0070034	cbz	w0, 0x4c154 <_WeChatMain+0x328e8>
0x4c064	e1d30091	add	x1, sp, #0x34
0x4c068	e00314aa	mov	x0, x20
0x4c06c	eb2e0094	bl	0x57c18 <_WeChatMain+0x3e3ac>
0x4c070	20070034	cbz	w0, 0x4c154 <_WeChatMain+0x328e8>
0x4c074	e81f40f9	ldr	x8, [sp, #0x38]
0x4c078	e93740b9	ldr	w9, [sp, #0x34]
0x4c07c	6a0a40f9	ldr	x10, [x19, #0x10]
0x4c080	4a210091	add	x10, x10, #0x8
0x4c084	480128f8	ldadd	x8, x8, [x10]
0x4c088	680a40f9	ldr	x8, [x19, #0x10]
0x4c08c	08410091	add	x8, x8, #0x10
0x4c090	080129b8	ldadd	w9, w8, [x8]
0x4c094	f7230091	add	x23, sp, #0x8
0x4c098	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4c09c	e82302a9	stp	x8, x8, [sp, #0x20]
0x4c0a0	75d704b0	adrp	x21, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4c0a4	b5e20c91	add	x21, x21, #0x338
0x4c0a8	e80f00f9	str	x8, [sp, #0x18]
0x4c0ac	f50700f9	str	x21, [sp, #0x8]
0x4c0b0	88765e92	and	x8, x20, #0xfffffffc00000000
0x4c0b4	76fd04d0	adrp	x22, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4c0b8	d6023b91	add	x22, x22, #0xec0
0x4c0bc	c90640f9	ldr	x9, [x22, #0x8]
0x4c0c0	1f0109eb	cmp	x8, x9
0x4c0c4	61000054	b.ne	0x4c0d0 <_WeChatMain+0x32864>
0x4c0c8	e00314aa	mov	x0, x20
0x4c0cc	e0cdff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4c0d0	f40b00f9	str	x20, [sp, #0x10]
0x4c0d4	ffb30039	strb	wzr, [sp, #0x2c]
0x4c0d8	e1420091	add	x1, x23, #0x10
0x4c0dc	e00314aa	mov	x0, x20
0x4c0e0	ce2e0094	bl	0x57c18 <_WeChatMain+0x3e3ac>
0x4c0e4	40010034	cbz	w0, 0x4c10c <_WeChatMain+0x328a0>
0x4c0e8	e00b40f9	ldr	x0, [sp, #0x10]
0x4c0ec	f4230091	add	x20, sp, #0x8
0x4c0f0	81620091	add	x1, x20, #0x18
0x4c0f4	db2e0094	bl	0x57c60 <_WeChatMain+0x3e3f4>
0x4c0f8	a0000034	cbz	w0, 0x4c10c <_WeChatMain+0x328a0>
0x4c0fc	e00b40f9	ldr	x0, [sp, #0x10]
0x4c100	81820091	add	x1, x20, #0x20
0x4c104	c52e0094	bl	0x57c18 <_WeChatMain+0x3e3ac>
0x4c108	60000037	tbnz	w0, #0x0, 0x4c114 <_WeChatMain+0x328a8>
0x4c10c	28008052	mov	w8, #0x1                ; =1
0x4c110	e8b30039	strb	w8, [sp, #0x2c]
0x4c114	680240f9	ldr	x8, [x19]
0x4c118	082940f9	ldr	x8, [x8, #0x50]
0x4c11c	e1230091	add	x1, sp, #0x8
0x4c120	e00313aa	mov	x0, x19
0x4c124	02008052	mov	w2, #0x0                ; =0
0x4c128	00013fd6	blr	x8
0x4c12c	f50700f9	str	x21, [sp, #0x8]
0x4c130	e80b40f9	ldr	x8, [sp, #0x10]
0x4c134	09755e92	and	x9, x8, #0xfffffffc00000000
0x4c138	ca0640f9	ldr	x10, [x22, #0x8]
0x4c13c	3f010aeb	cmp	x9, x10
0x4c140	a1000054	b.ne	0x4c154 <_WeChatMain+0x328e8>
0x4c144	f30300aa	mov	x19, x0
0x4c148	e00308aa	mov	x0, x8
0x4c14c	5dceff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4c150	e00313aa	mov	x0, x19
0x4c154	fd7b47a9	ldp	x29, x30, [sp, #0x70]
0x4c158	f44f46a9	ldp	x20, x19, [sp, #0x60]
0x4c15c	f65745a9	ldp	x22, x21, [sp, #0x50]
0x4c160	f85f44a9	ldp	x24, x23, [sp, #0x40]
0x4c164	ff030291	add	sp, sp, #0x80
0x4c168	c0035fd6	ret
0x4c16c	68d704b0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4c170	08e10c91	add	x8, x8, #0x338
0x4c174	080000f9	str	x8, [x0]
0x4c178	080440f9	ldr	x8, [x0, #0x8]
0x4c17c	09755e92	and	x9, x8, #0xfffffffc00000000
0x4c180	6afd04d0	adrp	x10, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4c184	4a013b91	add	x10, x10, #0xec0
0x4c188	4a0540f9	ldr	x10, [x10, #0x8]
0x4c18c	3f010aeb	cmp	x9, x10
0x4c190	41010054	b.ne	0x4c1b8 <_WeChatMain+0x3294c>
0x4c194	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4c198	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4c19c	fd430091	add	x29, sp, #0x10
0x4c1a0	f30300aa	mov	x19, x0
0x4c1a4	e00308aa	mov	x0, x8
0x4c1a8	46ceff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4c1ac	e00313aa	mov	x0, x19
0x4c1b0	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4c1b4	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4c1b8	1f0400f9	str	xzr, [x0, #0x8]
0x4c1bc	c0035fd6	ret
0x4c1c0	ffc300d1	sub	sp, sp, #0x30
0x4c1c4	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4c1c8	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4c1cc	fd830091	add	x29, sp, #0x20
0x4c1d0	f30300aa	mov	x19, x0
0x4c1d4	280840f9	ldr	x8, [x1, #0x10]
0x4c1d8	090540f9	ldr	x9, [x8, #0x8]
0x4c1dc	e90309cb	neg	x9, x9
0x4c1e0	081140b9	ldr	w8, [x8, #0x10]
0x4c1e4	e803084b	neg	w8, w8
0x4c1e8	0a0840f9	ldr	x10, [x0, #0x10]
0x4c1ec	4a210091	add	x10, x10, #0x8
0x4c1f0	490129f8	ldadd	x9, x9, [x10]
0x4c1f4	090840f9	ldr	x9, [x0, #0x10]
0x4c1f8	29410091	add	x9, x9, #0x10
0x4c1fc	280128b8	ldadd	w8, w8, [x9]
0x4c200	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4c204	e80700f9	str	x8, [sp, #0x8]
0x4c208	280040f9	ldr	x8, [x1]
0x4c20c	092140f9	ldr	x9, [x8, #0x40]
0x4c210	e8230091	add	x8, sp, #0x8
0x4c214	e00301aa	mov	x0, x1
0x4c218	20013fd6	blr	x9
0x4c21c	e10740f9	ldr	x1, [sp, #0x8]
0x4c220	680240f9	ldr	x8, [x19]
0x4c224	082940f9	ldr	x8, [x8, #0x50]
0x4c228	e00313aa	mov	x0, x19
0x4c22c	22008052	mov	w2, #0x1                ; =1
0x4c230	00013fd6	blr	x8
0x4c234	e00740f9	ldr	x0, [sp, #0x8]
0x4c238	ff0700f9	str	xzr, [sp, #0x8]
0x4c23c	800000b4	cbz	x0, 0x4c24c <_WeChatMain+0x329e0>
0x4c240	080040f9	ldr	x8, [x0]
0x4c244	080540f9	ldr	x8, [x8, #0x8]
0x4c248	00013fd6	blr	x8
0x4c24c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4c250	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4c254	ffc30091	add	sp, sp, #0x30
0x4c258	c0035fd6	ret
0x4c25c	ff4301d1	sub	sp, sp, #0x50
0x4c260	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4c264	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4c268	fd030191	add	x29, sp, #0x40
0x4c26c	f30301aa	mov	x19, x1
0x4c270	f40300aa	mov	x20, x0
0x4c274	080840f9	ldr	x8, [x0, #0x10]
0x4c278	080540f9	ldr	x8, [x8, #0x8]
0x4c27c	a8831ef8	stur	x8, [x29, #-0x18]
0x4c280	a16300d1	sub	x1, x29, #0x18
0x4c284	e00313aa	mov	x0, x19
0x4c288	e92d0094	bl	0x57a2c <_WeChatMain+0x3e1c0>
0x4c28c	880a40f9	ldr	x8, [x20, #0x10]
0x4c290	081140b9	ldr	w8, [x8, #0x10]
0x4c294	a8831eb8	stur	w8, [x29, #-0x18]
0x4c298	a16300d1	sub	x1, x29, #0x18
0x4c29c	e00313aa	mov	x0, x19
0x4c2a0	9a2d0094	bl	0x57908 <_WeChatMain+0x3e09c>
0x4c2a4	e8f30132	mov	w8, #-0x55555556        ; =-1431655766
0x4c2a8	a8431eb8	stur	w8, [x29, #-0x1c]
0x4c2ac	e9f301b2	mov	x9, #-0x5555555555555556 ; =-6148914691236517206
0x4c2b0	e90f00f9	str	x9, [sp, #0x18]
0x4c2b4	e81700b9	str	w8, [sp, #0x14]
0x4c2b8	e90700f9	str	x9, [sp, #0x8]
0x4c2bc	880240f9	ldr	x8, [x20]
0x4c2c0	092140f9	ldr	x9, [x8, #0x40]
0x4c2c4	e8230091	add	x8, sp, #0x8
0x4c2c8	e00314aa	mov	x0, x20
0x4c2cc	20013fd6	blr	x9
0x4c2d0	e00740f9	ldr	x0, [sp, #0x8]
0x4c2d4	080040f9	ldr	x8, [x0]
0x4c2d8	080940f9	ldr	x8, [x8, #0x10]
0x4c2dc	00013fd6	blr	x8
0x4c2e0	80030037	tbnz	w0, #0x0, 0x4c350 <_WeChatMain+0x32ae4>
0x4c2e4	e00740f9	ldr	x0, [sp, #0x8]
0x4c2e8	080040f9	ldr	x8, [x0]
0x4c2ec	081140f9	ldr	x8, [x8, #0x20]
0x4c2f0	a17300d1	sub	x1, x29, #0x1c
0x4c2f4	e2630091	add	x2, sp, #0x18
0x4c2f8	e3530091	add	x3, sp, #0x14
0x4c2fc	00013fd6	blr	x8
0x4c300	a8435eb8	ldur	w8, [x29, #-0x1c]
0x4c304	a8831eb8	stur	w8, [x29, #-0x18]
0x4c308	a16300d1	sub	x1, x29, #0x18
0x4c30c	e00313aa	mov	x0, x19
0x4c310	7e2d0094	bl	0x57908 <_WeChatMain+0x3e09c>
0x4c314	e80f40f9	ldr	x8, [sp, #0x18]
0x4c318	a8831ef8	stur	x8, [x29, #-0x18]
0x4c31c	a16300d1	sub	x1, x29, #0x18
0x4c320	e00313aa	mov	x0, x19
0x4c324	c22d0094	bl	0x57a2c <_WeChatMain+0x3e1c0>
0x4c328	e81740b9	ldr	w8, [sp, #0x14]
0x4c32c	a8831eb8	stur	w8, [x29, #-0x18]
0x4c330	a16300d1	sub	x1, x29, #0x18
0x4c334	e00313aa	mov	x0, x19
0x4c338	742d0094	bl	0x57908 <_WeChatMain+0x3e09c>
0x4c33c	e00740f9	ldr	x0, [sp, #0x8]
0x4c340	080040f9	ldr	x8, [x0]
0x4c344	080d40f9	ldr	x8, [x8, #0x18]
0x4c348	00013fd6	blr	x8
0x4c34c	e1ffff17	b	0x4c2d0 <_WeChatMain+0x32a64>
0x4c350	e00740f9	ldr	x0, [sp, #0x8]
0x4c354	ff0700f9	str	xzr, [sp, #0x8]
0x4c358	800000b4	cbz	x0, 0x4c368 <_WeChatMain+0x32afc>
0x4c35c	080040f9	ldr	x8, [x0]
0x4c360	080540f9	ldr	x8, [x8, #0x8]
0x4c364	00013fd6	blr	x8
0x4c368	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4c36c	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4c370	ff430191	add	sp, sp, #0x50
0x4c374	c0035fd6	ret
0x4c378	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4c37c	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4c380	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4c384	fd830091	add	x29, sp, #0x20
0x4c388	f40302aa	mov	x20, x2
0x4c38c	f30300aa	mov	x19, x0
0x4c390	351005d0	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c394	b5c21291	add	x21, x21, #0x4b0
0x4c398	a0c2bff8	ldapr	x0, [x21]
0x4c39c	e00400b5	cbnz	x0, 0x4c438 <_WeChatMain+0x32bcc>
0x4c3a0	f60301aa	mov	x22, x1
0x4c3a4	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c3a8	096d5339	ldrb	w9, [x8, #0x4db]
0x4c3ac	49030037	tbnz	w9, #0x0, 0x4c414 <_WeChatMain+0x32ba8>
0x4c3b0	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c3b4	201140fd	ldr	d0, [x9, #0x20]
0x4c3b8	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c3bc	211540fd	ldr	d1, [x9, #0x28]
0x4c3c0	20040c6e	mov.s	v0[1], v1[0]
0x4c3c4	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c3c8	211940fd	ldr	d1, [x9, #0x30]
0x4c3cc	2004146e	mov.s	v0[2], v1[0]
0x4c3d0	e92104b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c3d4	21dd43fd	ldr	d1, [x9, #0x7b8]
0x4c3d8	20041c6e	mov.s	v0[3], v1[0]
0x4c3dc	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c3e0	29011391	add	x9, x9, #0x4c0
0x4c3e4	2001803d	str	q0, [x9]
0x4c3e8	ea2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c3ec	401d40fd	ldr	d0, [x10, #0x38]
0x4c3f0	ea2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c3f4	412140fd	ldr	d1, [x10, #0x40]
0x4c3f8	20040c6e	mov.s	v0[1], v1[0]
0x4c3fc	200900fd	str	d0, [x9, #0x10]
0x4c400	eacd8d52	mov	w10, #0x6e6f            ; =28271
0x4c404	2a310079	strh	w10, [x9, #0x18]
0x4c408	3f690039	strb	wzr, [x9, #0x1a]
0x4c40c	29008052	mov	w9, #0x1                ; =1
0x4c410	096d1339	strb	w9, [x8, #0x4db]
0x4c414	201005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c418	00001391	add	x0, x0, #0x4c0
0x4c41c	21008052	mov	w1, #0x1                ; =1
0x4c420	22018052	mov	w2, #0x9                ; =9
0x4c424	43018052	mov	w3, #0xa                ; =10
0x4c428	24008052	mov	w4, #0x1                ; =1
0x4c42c	15f6ff97	bl	0x49c80 <_WeChatMain+0x30414>
0x4c430	a0fe9fc8	stlr	x0, [x21]
0x4c434	e10316aa	mov	x1, x22
0x4c438	080040f9	ldr	x8, [x0]
0x4c43c	081940f9	ldr	x8, [x8, #0x30]
0x4c440	00013fd6	blr	x8
0x4c444	351005d0	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c448	b5e21291	add	x21, x21, #0x4b8
0x4c44c	a0c2bff8	ldapr	x0, [x21]
0x4c450	e00400b5	cbnz	x0, 0x4c4ec <_WeChatMain+0x32c80>
0x4c454	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c458	09e95339	ldrb	w9, [x8, #0x4fa]
0x4c45c	89030037	tbnz	w9, #0x0, 0x4c4cc <_WeChatMain+0x32c60>
0x4c460	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c464	201140fd	ldr	d0, [x9, #0x20]
0x4c468	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c46c	211540fd	ldr	d1, [x9, #0x28]
0x4c470	20040c6e	mov.s	v0[1], v1[0]
0x4c474	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c478	211940fd	ldr	d1, [x9, #0x30]
0x4c47c	2004146e	mov.s	v0[2], v1[0]
0x4c480	e92104b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c484	21dd43fd	ldr	d1, [x9, #0x7b8]
0x4c488	20041c6e	mov.s	v0[3], v1[0]
0x4c48c	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c490	29711391	add	x9, x9, #0x4dc
0x4c494	2001803d	str	q0, [x9]
0x4c498	ea2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c49c	401d40fd	ldr	d0, [x10, #0x38]
0x4c4a0	ea2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c4a4	412540fd	ldr	d1, [x10, #0x48]
0x4c4a8	20040c6e	mov.s	v0[1], v1[0]
0x4c4ac	200900fd	str	d0, [x9, #0x10]
0x4c4b0	aa210490	adrp	x10, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x4c4b4	40a944fd	ldr	d0, [x10, #0x950]
0x4c4b8	201900bd	str	s0, [x9, #0x18]
0x4c4bc	8a0e8052	mov	w10, #0x74              ; =116
0x4c4c0	2a390079	strh	w10, [x9, #0x1c]
0x4c4c4	29008052	mov	w9, #0x1                ; =1
0x4c4c8	09e91339	strb	w9, [x8, #0x4fa]
0x4c4cc	201005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c4d0	00701391	add	x0, x0, #0x4dc
0x4c4d4	21008052	mov	w1, #0x1                ; =1
0x4c4d8	0200a852	mov	w2, #0x40000000         ; =1073741824
0x4c4dc	830c8052	mov	w3, #0x64               ; =100
0x4c4e0	24008052	mov	w4, #0x1                ; =1
0x4c4e4	e4f1ff97	bl	0x48c74 <_WeChatMain+0x2f408>
0x4c4e8	a0fe9fc8	stlr	x0, [x21]
0x4c4ec	080040f9	ldr	x8, [x0]
0x4c4f0	081940f9	ldr	x8, [x8, #0x30]
0x4c4f4	e10314aa	mov	x1, x20
0x4c4f8	00013fd6	blr	x8
0x4c4fc	680a40f9	ldr	x8, [x19, #0x10]
0x4c500	010140f9	ldr	x1, [x8]
0x4c504	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c508	09695439	ldrb	w9, [x8, #0x51a]
0x4c50c	89030037	tbnz	w9, #0x0, 0x4c57c <_WeChatMain+0x32d10>
0x4c510	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c514	201140fd	ldr	d0, [x9, #0x20]
0x4c518	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c51c	211540fd	ldr	d1, [x9, #0x28]
0x4c520	20040c6e	mov.s	v0[1], v1[0]
0x4c524	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c528	211940fd	ldr	d1, [x9, #0x30]
0x4c52c	2004146e	mov.s	v0[2], v1[0]
0x4c530	e92104b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c534	21dd43fd	ldr	d1, [x9, #0x7b8]
0x4c538	20041c6e	mov.s	v0[3], v1[0]
0x4c53c	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c540	29f11391	add	x9, x9, #0x4fc
0x4c544	2001803d	str	q0, [x9]
0x4c548	ea2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c54c	401d40fd	ldr	d0, [x10, #0x38]
0x4c550	ea2104b0	adrp	x10, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c554	417943fd	ldr	d1, [x10, #0x6f0]
0x4c558	20040c6e	mov.s	v0[1], v1[0]
0x4c55c	200900fd	str	d0, [x9, #0x10]
0x4c560	ea2104b0	adrp	x10, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c564	407d43fd	ldr	d0, [x10, #0x6f8]
0x4c568	201900bd	str	s0, [x9, #0x18]
0x4c56c	aa0d8052	mov	w10, #0x6d              ; =109
0x4c570	2a390079	strh	w10, [x9, #0x1c]
0x4c574	29008052	mov	w9, #0x1                ; =1
0x4c578	09691439	strb	w9, [x8, #0x51a]
0x4c57c	201005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c580	00f01391	add	x0, x0, #0x4fc
0x4c584	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4c588	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4c58c	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4c590	dafdff17	b	0x4bcf8 <_WeChatMain+0x3248c>
0x4c594	ffc301d1	sub	sp, sp, #0x70
0x4c598	fa6702a9	stp	x26, x25, [sp, #0x20]
0x4c59c	f85f03a9	stp	x24, x23, [sp, #0x30]
0x4c5a0	f65704a9	stp	x22, x21, [sp, #0x40]
0x4c5a4	f44f05a9	stp	x20, x19, [sp, #0x50]
0x4c5a8	fd7b06a9	stp	x29, x30, [sp, #0x60]
0x4c5ac	fd830191	add	x29, sp, #0x60
0x4c5b0	f50303aa	mov	x21, x3
0x4c5b4	f60302aa	mov	x22, x2
0x4c5b8	f70301aa	mov	x23, x1
0x4c5bc	f40300aa	mov	x20, x0
0x4c5c0	f30308aa	mov	x19, x8
0x4c5c4	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4c5c8	68a200a9	stp	x8, x8, [x19, #0x8]
0x4c5cc	680200f9	str	x8, [x19]
0x4c5d0	e00313aa	mov	x0, x19
0x4c5d4	3b7bff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x4c5d8	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c5dc	09855439	ldrb	w9, [x8, #0x521]
0x4c5e0	29010037	tbnz	w9, #0x0, 0x4c604 <_WeChatMain+0x32d98>
0x4c5e4	e92104b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c5e8	20e547fd	ldr	d0, [x9, #0xfc8]
0x4c5ec	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c5f0	29711491	add	x9, x9, #0x51c
0x4c5f4	200100bd	str	s0, [x9]
0x4c5f8	3f110039	strb	wzr, [x9, #0x4]
0x4c5fc	29008052	mov	w9, #0x1                ; =1
0x4c600	09851439	strb	w9, [x8, #0x521]
0x4c604	381005d0	adrp	x24, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c608	18731491	add	x24, x24, #0x51c
0x4c60c	e00318aa	mov	x0, x24
0x4c610	fad4c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4c614	e20300aa	mov	x2, x0
0x4c618	e00313aa	mov	x0, x19
0x4c61c	e10318aa	mov	x1, x24
0x4c620	e30317aa	mov	x3, x23
0x4c624	e40316aa	mov	x4, x22
0x4c628	936c0194	bl	0xa7874 <_WeChatMain+0x8e008>
0x4c62c	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c630	09ad5439	ldrb	w9, [x8, #0x52b]
0x4c634	69010037	tbnz	w9, #0x0, 0x4c660 <_WeChatMain+0x32df4>
0x4c638	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c63c	200140fd	ldr	d0, [x9]
0x4c640	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c644	29911491	add	x9, x9, #0x524
0x4c648	200100bd	str	s0, [x9]
0x4c64c	aa4c8e52	mov	w10, #0x7265            ; =29285
0x4c650	2a090079	strh	w10, [x9, #0x4]
0x4c654	3f190039	strb	wzr, [x9, #0x6]
0x4c658	29008052	mov	w9, #0x1                ; =1
0x4c65c	09ad1439	strb	w9, [x8, #0x52b]
0x4c660	381005d0	adrp	x24, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c664	18931491	add	x24, x24, #0x524
0x4c668	e00318aa	mov	x0, x24
0x4c66c	e3d4c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4c670	f90300aa	mov	x25, x0
0x4c674	880240f9	ldr	x8, [x20]
0x4c678	093140f9	ldr	x9, [x8, #0x60]
0x4c67c	e8230091	add	x8, sp, #0x8
0x4c680	e00314aa	mov	x0, x20
0x4c684	e10317aa	mov	x1, x23
0x4c688	e20316aa	mov	x2, x22
0x4c68c	e30315aa	mov	x3, x21
0x4c690	20013fd6	blr	x9
0x4c694	e3230091	add	x3, sp, #0x8
0x4c698	e00313aa	mov	x0, x19
0x4c69c	e10318aa	mov	x1, x24
0x4c6a0	e20319aa	mov	x2, x25
0x4c6a4	f26c0194	bl	0xa7a6c <_WeChatMain+0x8e200>
0x4c6a8	e87fc039	ldrsb	w8, [sp, #0x1f]
0x4c6ac	a800f836	tbz	w8, #0x1f, 0x4c6c0 <_WeChatMain+0x32e54>
0x4c6b0	e00740f9	ldr	x0, [sp, #0x8]
0x4c6b4	e80f40f9	ldr	x8, [sp, #0x18]
0x4c6b8	01f94092	and	x1, x8, #0x7fffffffffffffff
0x4c6bc	54cec395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4c6c0	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c6c4	09c55439	ldrb	w9, [x8, #0x531]
0x4c6c8	29010037	tbnz	w9, #0x0, 0x4c6ec <_WeChatMain+0x32e80>
0x4c6cc	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c6d0	200540fd	ldr	d0, [x9, #0x8]
0x4c6d4	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c6d8	29b11491	add	x9, x9, #0x52c
0x4c6dc	200100bd	str	s0, [x9]
0x4c6e0	3f110039	strb	wzr, [x9, #0x4]
0x4c6e4	29008052	mov	w9, #0x1                ; =1
0x4c6e8	09c51439	strb	w9, [x8, #0x531]
0x4c6ec	351005d0	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c6f0	b5b21491	add	x21, x21, #0x52c
0x4c6f4	e00315aa	mov	x0, x21
0x4c6f8	c0d4c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4c6fc	f60300aa	mov	x22, x0
0x4c700	880240f9	ldr	x8, [x20]
0x4c704	092d40f9	ldr	x9, [x8, #0x58]
0x4c708	e8230091	add	x8, sp, #0x8
0x4c70c	e00314aa	mov	x0, x20
0x4c710	20013fd6	blr	x9
0x4c714	e3230091	add	x3, sp, #0x8
0x4c718	e00313aa	mov	x0, x19
0x4c71c	e10315aa	mov	x1, x21
0x4c720	e20316aa	mov	x2, x22
0x4c724	d26c0194	bl	0xa7a6c <_WeChatMain+0x8e200>
0x4c728	e87fc039	ldrsb	w8, [sp, #0x1f]
0x4c72c	a800f836	tbz	w8, #0x1f, 0x4c740 <_WeChatMain+0x32ed4>
0x4c730	e00740f9	ldr	x0, [sp, #0x8]
0x4c734	e80f40f9	ldr	x8, [sp, #0x18]
0x4c738	01f94092	and	x1, x8, #0x7fffffffffffffff
0x4c73c	34cec395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4c740	fd7b46a9	ldp	x29, x30, [sp, #0x60]
0x4c744	f44f45a9	ldp	x20, x19, [sp, #0x50]
0x4c748	f65744a9	ldp	x22, x21, [sp, #0x40]
0x4c74c	f85f43a9	ldp	x24, x23, [sp, #0x30]
0x4c750	fa6742a9	ldp	x26, x25, [sp, #0x20]
0x4c754	ffc30191	add	sp, sp, #0x70
0x4c758	c0035fd6	ret
0x4c75c	ff4301d1	sub	sp, sp, #0x50
0x4c760	f65702a9	stp	x22, x21, [sp, #0x20]
0x4c764	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4c768	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4c76c	fd030191	add	x29, sp, #0x40
0x4c770	f30303aa	mov	x19, x3
0x4c774	f50301aa	mov	x21, x1
0x4c778	f40308aa	mov	x20, x8
0x4c77c	1f7d00a9	stp	xzr, xzr, [x8]
0x4c780	1f0900f9	str	xzr, [x8, #0x10]
0x4c784	f60302aa	mov	x22, x2
0x4c788	080040f9	ldr	x8, [x0]
0x4c78c	081140f9	ldr	x8, [x8, #0x20]
0x4c790	00013fd6	blr	x8
0x4c794	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c798	09615539	ldrb	w9, [x8, #0x558]
0x4c79c	e9030037	tbnz	w9, #0x0, 0x4c818 <_WeChatMain+0x32fac>
0x4c7a0	e92104b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c7a4	207943fd	ldr	d0, [x9, #0x6f0]
0x4c7a8	e92104b0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4c7ac	217d43fd	ldr	d1, [x9, #0x6f8]
0x4c7b0	20040c6e	mov.s	v0[1], v1[0]
0x4c7b4	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c7b8	212940fd	ldr	d1, [x9, #0x50]
0x4c7bc	2004146e	mov.s	v0[2], v1[0]
0x4c7c0	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c7c4	212d40fd	ldr	d1, [x9, #0x58]
0x4c7c8	20041c6e	mov.s	v0[3], v1[0]
0x4c7cc	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c7d0	213140fd	ldr	d1, [x9, #0x60]
0x4c7d4	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c7d8	223540fd	ldr	d2, [x9, #0x68]
0x4c7dc	41040c6e	mov.s	v1[1], v2[0]
0x4c7e0	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c7e4	223940fd	ldr	d2, [x9, #0x70]
0x4c7e8	4104146e	mov.s	v1[2], v2[0]
0x4c7ec	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c7f0	223d40fd	ldr	d2, [x9, #0x78]
0x4c7f4	41041c6e	mov.s	v1[3], v2[0]
0x4c7f8	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c7fc	29d11491	add	x9, x9, #0x534
0x4c800	200500ad	stp	q0, q1, [x9]
0x4c804	ea2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c808	404140fd	ldr	d0, [x10, #0x80]
0x4c80c	202100bd	str	s0, [x9, #0x20]
0x4c810	29008052	mov	w9, #0x1                ; =1
0x4c814	09611539	strb	w9, [x8, #0x558]
0x4c818	f58300a9	stp	x21, x0, [sp, #0x8]
0x4c81c	f60300f9	str	x22, [sp]
0x4c820	211005d0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c824	21d01491	add	x1, x1, #0x534
0x4c828	e00314aa	mov	x0, x20
0x4c82c	9b6e0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x4c830	f3010034	cbz	w19, 0x4c86c <_WeChatMain+0x33000>
0x4c834	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c838	09c15539	ldrb	w9, [x8, #0x570]
0x4c83c	e9000037	tbnz	w9, #0x0, 0x4c858 <_WeChatMain+0x32fec>
0x4c840	e92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4c844	2025c03d	ldr	q0, [x9, #0x90]
0x4c848	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c84c	2059813d	str	q0, [x9, #0x560]
0x4c850	29008052	mov	w9, #0x1                ; =1
0x4c854	09c11539	strb	w9, [x8, #0x570]
0x4c858	f30300f9	str	x19, [sp]
0x4c85c	211005d0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c860	21801591	add	x1, x1, #0x560
0x4c864	e00314aa	mov	x0, x20
0x4c868	8c6e0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x4c86c	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4c870	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4c874	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4c878	ff430191	add	sp, sp, #0x50
0x4c87c	c0035fd6	ret
0x4c880	ff4303d1	sub	sp, sp, #0xd0
0x4c884	e923066d	stp	d9, d8, [sp, #0x60]
0x4c888	fc6f07a9	stp	x28, x27, [sp, #0x70]
0x4c88c	fa6708a9	stp	x26, x25, [sp, #0x80]
0x4c890	f85f09a9	stp	x24, x23, [sp, #0x90]
0x4c894	f6570aa9	stp	x22, x21, [sp, #0xa0]
0x4c898	f44f0ba9	stp	x20, x19, [sp, #0xb0]
0x4c89c	fd7b0ca9	stp	x29, x30, [sp, #0xc0]
0x4c8a0	fd030391	add	x29, sp, #0xc0
0x4c8a4	f60300aa	mov	x22, x0
0x4c8a8	f30308aa	mov	x19, x8
0x4c8ac	f8f30132	mov	w24, #-0x55555556       ; =-1431655766
0x4c8b0	080040f9	ldr	x8, [x0]
0x4c8b4	081140f9	ldr	x8, [x8, #0x20]
0x4c8b8	00013fd6	blr	x8
0x4c8bc	f50300aa	mov	x21, x0
0x4c8c0	f7f301b2	mov	x23, #-0x5555555555555556 ; =-6148914691236517206
0x4c8c4	f72f00f9	str	x23, [sp, #0x58]
0x4c8c8	c80240f9	ldr	x8, [x22]
0x4c8cc	092140f9	ldr	x9, [x8, #0x40]
0x4c8d0	e8630191	add	x8, sp, #0x58
0x4c8d4	e00316aa	mov	x0, x22
0x4c8d8	20013fd6	blr	x9
0x4c8dc	e02f40f9	ldr	x0, [sp, #0x58]
0x4c8e0	080040f9	ldr	x8, [x0]
0x4c8e4	080940f9	ldr	x8, [x8, #0x10]
0x4c8e8	00013fd6	blr	x8
0x4c8ec	08106e1e	fmov	d8, #1.00000000
0x4c8f0	60000036	tbz	w0, #0x0, 0x4c8fc <_WeChatMain+0x33090>
0x4c8f4	14008052	mov	w20, #0x0               ; =0
0x4c8f8	22000014	b	0x4c980 <_WeChatMain+0x33114>
0x4c8fc	19008052	mov	w25, #0x0               ; =0
0x4c900	14008052	mov	w20, #0x0               ; =0
0x4c904	f83300b9	str	w24, [sp, #0x30]
0x4c908	f71f00f9	str	x23, [sp, #0x38]
0x4c90c	f85700b9	str	w24, [sp, #0x54]
0x4c910	e02f40f9	ldr	x0, [sp, #0x58]
0x4c914	080040f9	ldr	x8, [x0]
0x4c918	081140f9	ldr	x8, [x8, #0x20]
0x4c91c	e1c30091	add	x1, sp, #0x30
0x4c920	e2e30091	add	x2, sp, #0x38
0x4c924	e3530191	add	x3, sp, #0x54
0x4c928	00013fd6	blr	x8
0x4c92c	e83340b9	ldr	w8, [sp, #0x30]
0x4c930	1f01146b	cmp	w8, w20
0x4c934	14c1941a	csel	w20, w8, w20, gt
0x4c938	e85740b9	ldr	w8, [sp, #0x54]
0x4c93c	1f01196b	cmp	w8, w25
0x4c940	19c1991a	csel	w25, w8, w25, gt
0x4c944	e02f40f9	ldr	x0, [sp, #0x58]
0x4c948	080040f9	ldr	x8, [x0]
0x4c94c	080d40f9	ldr	x8, [x8, #0x18]
0x4c950	00013fd6	blr	x8
0x4c954	e02f40f9	ldr	x0, [sp, #0x58]
0x4c958	080040f9	ldr	x8, [x0]
0x4c95c	080940f9	ldr	x8, [x8, #0x10]
0x4c960	00013fd6	blr	x8
0x4c964	00fdff34	cbz	w0, 0x4c904 <_WeChatMain+0x33098>
0x4c968	3f270171	cmp	w25, #0x49
0x4c96c	a3000054	b.lo	0x4c980 <_WeChatMain+0x33114>
0x4c970	2003631e	ucvtf	d0, w25
0x4c974	480ae8d2	mov	x8, #0x4052000000000000 ; =4634766966517661696
0x4c978	0101679e	fmov	d1, x8
0x4c97c	2818601e	fdiv	d8, d1, d0
0x4c980	3c1005d0	adrp	x28, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c984	88535639	ldrb	w8, [x28, #0x594]
0x4c988	08010037	tbnz	w8, #0x0, 0x4c9a8 <_WeChatMain+0x3313c>
0x4c98c	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c990	08451691	add	x8, x8, #0x591
0x4c994	a9848c52	mov	w9, #0x6425             ; =25637
0x4c998	09010079	strh	w9, [x8]
0x4c99c	1f090039	strb	wzr, [x8, #0x2]
0x4c9a0	28008052	mov	w8, #0x1                ; =1
0x4c9a4	88531639	strb	w8, [x28, #0x594]
0x4c9a8	f40300f9	str	x20, [sp]
0x4c9ac	341005d0	adrp	x20, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4c9b0	94461691	add	x20, x20, #0x591
0x4c9b4	e8e30091	add	x8, sp, #0x38
0x4c9b8	e00314aa	mov	x0, x20
0x4c9bc	716d0094	bl	0x67f80 <_WeChatMain+0x4e714>
0x4c9c0	f73f8139	ldrsb	x23, [sp, #0x4f]
0x4c9c4	b700f8b6	tbz	x23, #0x3f, 0x4c9d8 <_WeChatMain+0x3316c>
0x4c9c8	e0df43a9	ldp	x0, x23, [sp, #0x38]
0x4c9cc	e82740f9	ldr	x8, [sp, #0x48]
0x4c9d0	01f94092	and	x1, x8, #0x7fffffffffffffff
0x4c9d4	8ecdc395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4c9d8	c80240f9	ldr	x8, [x22]
0x4c9dc	092140f9	ldr	x9, [x8, #0x40]
0x4c9e0	e8e30091	add	x8, sp, #0x38
0x4c9e4	e00316aa	mov	x0, x22
0x4c9e8	20013fd6	blr	x9
0x4c9ec	e81f40f9	ldr	x8, [sp, #0x38]
0x4c9f0	ff1f00f9	str	xzr, [sp, #0x38]
0x4c9f4	e02f40f9	ldr	x0, [sp, #0x58]
0x4c9f8	e82f00f9	str	x8, [sp, #0x58]
0x4c9fc	400100b4	cbz	x0, 0x4ca24 <_WeChatMain+0x331b8>
0x4ca00	080040f9	ldr	x8, [x0]
0x4ca04	080540f9	ldr	x8, [x8, #0x8]
0x4ca08	00013fd6	blr	x8
0x4ca0c	e01f40f9	ldr	x0, [sp, #0x38]
0x4ca10	ff1f00f9	str	xzr, [sp, #0x38]
0x4ca14	800000b4	cbz	x0, 0x4ca24 <_WeChatMain+0x331b8>
0x4ca18	080040f9	ldr	x8, [x0]
0x4ca1c	080540f9	ldr	x8, [x8, #0x8]
0x4ca20	00013fd6	blr	x8
0x4ca24	7f7e00a9	stp	xzr, xzr, [x19]
0x4ca28	7f0a00f9	str	xzr, [x19, #0x10]
0x4ca2c	e02f40f9	ldr	x0, [sp, #0x58]
0x4ca30	080040f9	ldr	x8, [x0]
0x4ca34	080940f9	ldr	x8, [x8, #0x10]
0x4ca38	00013fd6	blr	x8
0x4ca3c	00020036	tbz	w0, #0x0, 0x4ca7c <_WeChatMain+0x33210>
0x4ca40	e02f40f9	ldr	x0, [sp, #0x58]
0x4ca44	ff2f00f9	str	xzr, [sp, #0x58]
0x4ca48	800000b4	cbz	x0, 0x4ca58 <_WeChatMain+0x331ec>
0x4ca4c	080040f9	ldr	x8, [x0]
0x4ca50	080540f9	ldr	x8, [x8, #0x8]
0x4ca54	00013fd6	blr	x8
0x4ca58	fd7b4ca9	ldp	x29, x30, [sp, #0xc0]
0x4ca5c	f44f4ba9	ldp	x20, x19, [sp, #0xb0]
0x4ca60	f6574aa9	ldp	x22, x21, [sp, #0xa0]
0x4ca64	f85f49a9	ldp	x24, x23, [sp, #0x90]
0x4ca68	fa6748a9	ldp	x26, x25, [sp, #0x80]
0x4ca6c	fc6f47a9	ldp	x28, x27, [sp, #0x70]
0x4ca70	e923466d	ldp	d9, d8, [sp, #0x60]
0x4ca74	ff430391	add	sp, sp, #0xd0
0x4ca78	c0035fd6	ret
0x4ca7c	280be8d2	mov	x8, #0x4059000000000000 ; =4636737291354636288
0x4ca80	a002621e	scvtf	d0, w21
0x4ca84	0101679e	fmov	d1, x8
0x4ca88	0918611e	fdiv	d9, d0, d1
0x4ca8c	fa0a0091	add	x26, x23, #0x2
0x4ca90	fbf301b2	mov	x27, #-0x5555555555555556 ; =-6148914691236517206
0x4ca94	f5e30091	add	x21, sp, #0x38
0x4ca98	d9028052	mov	w25, #0x16              ; =22
0x4ca9c	361005d0	adrp	x22, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4caa0	d6c61591	add	x22, x22, #0x571
0x4caa4	e82104b0	adrp	x8, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4caa8	00edc33d	ldr	q0, [x8, #0xfb0]
0x4caac	e007803d	str	q0, [sp, #0x10]
0x4cab0	0f000014	b	0x4caec <_WeChatMain+0x33280>
0x4cab4	e00313aa	mov	x0, x19
0x4cab8	e10316aa	mov	x1, x22
0x4cabc	f76d0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x4cac0	e02f40f9	ldr	x0, [sp, #0x58]
0x4cac4	080040f9	ldr	x8, [x0]
0x4cac8	080d40f9	ldr	x8, [x8, #0x18]
0x4cacc	00013fd6	blr	x8
0x4cad0	e83fc139	ldrsb	w8, [sp, #0x4f]
0x4cad4	e808f837	tbnz	w8, #0x1f, 0x4cbf0 <_WeChatMain+0x33384>
0x4cad8	e02f40f9	ldr	x0, [sp, #0x58]
0x4cadc	080040f9	ldr	x8, [x0]
0x4cae0	080940f9	ldr	x8, [x8, #0x10]
0x4cae4	00013fd6	blr	x8
0x4cae8	c0fa0737	tbnz	w0, #0x0, 0x4ca40 <_WeChatMain+0x331d4>
0x4caec	f85700b9	str	w24, [sp, #0x54]
0x4caf0	fb1b00f9	str	x27, [sp, #0x30]
0x4caf4	f82f00b9	str	w24, [sp, #0x2c]
0x4caf8	e02f40f9	ldr	x0, [sp, #0x58]
0x4cafc	080040f9	ldr	x8, [x0]
0x4cb00	081140f9	ldr	x8, [x8, #0x20]
0x4cb04	e1530191	add	x1, sp, #0x54
0x4cb08	e2c30091	add	x2, sp, #0x30
0x4cb0c	e3b30091	add	x3, sp, #0x2c
0x4cb10	00013fd6	blr	x8
0x4cb14	fb6f04a9	stp	x27, x27, [sp, #0x40]
0x4cb18	fb1f00f9	str	x27, [sp, #0x38]
0x4cb1c	88535639	ldrb	w8, [x28, #0x594]
0x4cb20	c8000037	tbnz	w8, #0x0, 0x4cb38 <_WeChatMain+0x332cc>
0x4cb24	a8848c52	mov	w8, #0x6425             ; =25637
0x4cb28	88020079	strh	w8, [x20]
0x4cb2c	9f0a0039	strb	wzr, [x20, #0x2]
0x4cb30	28008052	mov	w8, #0x1                ; =1
0x4cb34	88531639	strb	w8, [x28, #0x594]
0x4cb38	e85740b9	ldr	w8, [sp, #0x54]
0x4cb3c	e80300f9	str	x8, [sp]
0x4cb40	e8e30091	add	x8, sp, #0x38
0x4cb44	e00314aa	mov	x0, x20
0x4cb48	0e6d0094	bl	0x67f80 <_WeChatMain+0x4e714>
0x4cb4c	e83f4139	ldrb	w8, [sp, #0x4f]
0x4cb50	091d0013	sxtb	w9, w8
0x4cb54	eaaf43a9	ldp	x10, x11, [sp, #0x38]
0x4cb58	3f010071	cmp	w9, #0x0
0x4cb5c	47b1959a	csel	x7, x10, x21, lt
0x4cb60	66b1889a	csel	x6, x11, x8, lt
0x4cb64	695e4039	ldrb	w9, [x19, #0x17]
0x4cb68	281d0013	sxtb	w8, w9
0x4cb6c	6baa40a9	ldp	x11, x10, [x19, #0x8]
0x4cb70	4af94092	and	x10, x10, #0x7fffffffffffffff
0x4cb74	4a0500d1	sub	x10, x10, #0x1
0x4cb78	1f010071	cmp	w8, #0x0
0x4cb7c	41b1999a	csel	x1, x10, x25, lt
0x4cb80	77b1899a	csel	x23, x11, x9, lt
0x4cb84	290017cb	sub	x9, x1, x23
0x4cb88	3f0106eb	cmp	x9, x6
0x4cb8c	22010054	b.hs	0x4cbb0 <_WeChatMain+0x33344>
0x4cb90	e802068b	add	x8, x23, x6
0x4cb94	020101cb	sub	x2, x8, x1
0x4cb98	e00313aa	mov	x0, x19
0x4cb9c	e30317aa	mov	x3, x23
0x4cba0	e40317aa	mov	x4, x23
0x4cba4	050080d2	mov	x5, #0x0                ; =0
0x4cba8	03cbc395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x4cbac	1b000014	b	0x4cc18 <_WeChatMain+0x333ac>
0x4cbb0	460300b4	cbz	x6, 0x4cc18 <_WeChatMain+0x333ac>
0x4cbb4	f9031caa	mov	x25, x28
0x4cbb8	690240f9	ldr	x9, [x19]
0x4cbbc	1f010071	cmp	w8, #0x0
0x4cbc0	3cb1939a	csel	x28, x9, x19, lt
0x4cbc4	8003178b	add	x0, x28, x23
0x4cbc8	e10307aa	mov	x1, x7
0x4cbcc	e20306aa	mov	x2, x6
0x4cbd0	f50306aa	mov	x21, x6
0x4cbd4	b0d0c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4cbd8	e802158b	add	x8, x23, x21
0x4cbdc	695ec039	ldrsb	w9, [x19, #0x17]
0x4cbe0	2901f837	tbnz	w9, #0x1f, 0x4cc04 <_WeChatMain+0x33398>
0x4cbe4	09190012	and	w9, w8, #0x7f
0x4cbe8	695e0039	strb	w9, [x19, #0x17]
0x4cbec	07000014	b	0x4cc08 <_WeChatMain+0x3339c>
0x4cbf0	e01f40f9	ldr	x0, [sp, #0x38]
0x4cbf4	e82740f9	ldr	x8, [sp, #0x48]
0x4cbf8	01f94092	and	x1, x8, #0x7fffffffffffffff
0x4cbfc	04cdc395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4cc00	b6ffff17	b	0x4cad8 <_WeChatMain+0x3326c>
0x4cc04	680600f9	str	x8, [x19, #0x8]
0x4cc08	9f6b2838	strb	wzr, [x28, x8]
0x4cc0c	fc0319aa	mov	x28, x25
0x4cc10	f5e30091	add	x21, sp, #0x38
0x4cc14	d9028052	mov	w25, #0x16              ; =22
0x4cc18	e83f4139	ldrb	w8, [sp, #0x4f]
0x4cc1c	091d0013	sxtb	w9, w8
0x4cc20	ea2340f9	ldr	x10, [sp, #0x40]
0x4cc24	3f010071	cmp	w9, #0x0
0x4cc28	48b1889a	csel	x8, x10, x8, lt
0x4cc2c	1f011aeb	cmp	x8, x26
0x4cc30	c2010054	b.hs	0x4cc68 <_WeChatMain+0x333fc>
0x4cc34	170080d2	mov	x23, #0x0               ; =0
0x4cc38	e00313aa	mov	x0, x19
0x4cc3c	01048052	mov	w1, #0x20               ; =32
0x4cc40	1ccbc395	bl	0x713f8b0 <_wxam_enc_uninit_10+0x713f8b0>
0x4cc44	f7060091	add	x23, x23, #0x1
0x4cc48	e83f4139	ldrb	w8, [sp, #0x4f]
0x4cc4c	091d0013	sxtb	w9, w8
0x4cc50	ea2340f9	ldr	x10, [sp, #0x40]
0x4cc54	3f010071	cmp	w9, #0x0
0x4cc58	48b1889a	csel	x8, x10, x8, lt
0x4cc5c	0801178b	add	x8, x8, x23
0x4cc60	1f011aeb	cmp	x8, x26
0x4cc64	a3feff54	b.lo	0x4cc38 <_WeChatMain+0x333cc>
0x4cc68	e02f40bd	ldr	s0, [sp, #0x2c]
0x4cc6c	00a4200f	sshll.2d	v0, v0, #0x0
0x4cc70	00d8615e	scvtf	d0, d0
0x4cc74	0009601e	fmul	d0, d8, d0
0x4cc78	0800641e	fcvtas	w8, d0
0x4cc7c	0001621e	scvtf	d0, w8
0x4cc80	01098052	mov	w1, #0x48               ; =72
0x4cc84	e20313aa	mov	x2, x19
0x4cc88	30000094	bl	0x4cd48 <_WeChatMain+0x334dc>
0x4cc8c	e82f40b9	ldr	w8, [sp, #0x2c]
0x4cc90	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cc94	29415639	ldrb	w9, [x9, #0x590]
0x4cc98	e9000037	tbnz	w9, #0x0, 0x4ccb4 <_WeChatMain+0x33448>
0x4cc9c	e007c03d	ldr	q0, [sp, #0x10]
0x4cca0	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cca4	2061813d	str	q0, [x9, #0x580]
0x4cca8	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4ccac	2a008052	mov	w10, #0x1               ; =1
0x4ccb0	2a411639	strb	w10, [x9, #0x590]
0x4ccb4	0001621e	scvtf	d0, w8
0x4ccb8	0018691e	fdiv	d0, d0, d9
0x4ccbc	e80300f9	str	x8, [sp]
0x4ccc0	e00700fd	str	d0, [sp, #0x8]
0x4ccc4	e00313aa	mov	x0, x19
0x4ccc8	211005d0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cccc	21001691	add	x1, x1, #0x580
0x4ccd0	726d0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x4ccd4	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4ccd8	08cd5539	ldrb	w8, [x8, #0x573]
0x4ccdc	c8ee0737	tbnz	w8, #0x0, 0x4cab4 <_WeChatMain+0x33248>
0x4cce0	48018052	mov	w8, #0xa                ; =10
0x4cce4	c8020079	strh	w8, [x22]
0x4cce8	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4ccec	29008052	mov	w9, #0x1                ; =1
0x4ccf0	09cd1539	strb	w9, [x8, #0x573]
0x4ccf4	70ffff17	b	0x4cab4 <_WeChatMain+0x33248>
0x4ccf8	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4ccfc	2a515639	ldrb	w10, [x9, #0x594]
0x4cd00	0a010037	tbnz	w10, #0x0, 0x4cd20 <_WeChatMain+0x334b4>
0x4cd04	2a1005d0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cd08	4a451691	add	x10, x10, #0x591
0x4cd0c	ab848c52	mov	w11, #0x6425            ; =25637
0x4cd10	4b010079	strh	w11, [x10]
0x4cd14	5f090039	strb	wzr, [x10, #0x2]
0x4cd18	2a008052	mov	w10, #0x1               ; =1
0x4cd1c	2a511639	strb	w10, [x9, #0x594]
0x4cd20	ff8300d1	sub	sp, sp, #0x20
0x4cd24	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4cd28	fd430091	add	x29, sp, #0x10
0x4cd2c	e10300f9	str	x1, [sp]
0x4cd30	201005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cd34	00441691	add	x0, x0, #0x591
0x4cd38	926c0094	bl	0x67f80 <_WeChatMain+0x4e714>
0x4cd3c	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4cd40	ff830091	add	sp, sp, #0x20
0x4cd44	c0035fd6	ret
0x4cd48	eb2bb86d	stp	d11, d10, [sp, #-0x80]!
0x4cd4c	e923016d	stp	d9, d8, [sp, #0x10]
0x4cd50	fc6f02a9	stp	x28, x27, [sp, #0x20]
0x4cd54	fa6703a9	stp	x26, x25, [sp, #0x30]
0x4cd58	f85f04a9	stp	x24, x23, [sp, #0x40]
0x4cd5c	f65705a9	stp	x22, x21, [sp, #0x50]
0x4cd60	f44f06a9	stp	x20, x19, [sp, #0x60]
0x4cd64	fd7b07a9	stp	x29, x30, [sp, #0x70]
0x4cd68	fdc30191	add	x29, sp, #0x70
0x4cd6c	f30302aa	mov	x19, x2
0x4cd70	f40301aa	mov	x20, x1
0x4cd74	0840601e	fmov	d8, d0
0x4cd78	0820601e	fcmp	d0, #0.0
0x4cd7c	8d070054	b.le	0x4ce6c <_WeChatMain+0x33600>
0x4cd80	381005d0	adrp	x24, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cd84	08db5539	ldrb	w8, [x24, #0x576]
0x4cd88	09107e1e	fmov	d9, #-1.00000000
0x4cd8c	b9058052	mov	w25, #0x2d              ; =45
0x4cd90	3a008052	mov	w26, #0x1               ; =1
0x4cd94	0a41601e	fmov	d10, d8
0x4cd98	351005d0	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cd9c	b5d21591	add	x21, x21, #0x574
0x4cda0	0e000014	b	0x4cdd8 <_WeChatMain+0x3356c>
0x4cda4	c80201cb	sub	x8, x22, x1
0x4cda8	0201178b	add	x2, x8, x23
0x4cdac	e00313aa	mov	x0, x19
0x4cdb0	e30317aa	mov	x3, x23
0x4cdb4	e40317aa	mov	x4, x23
0x4cdb8	050080d2	mov	x5, #0x0                ; =0
0x4cdbc	e60316aa	mov	x6, x22
0x4cdc0	e70315aa	mov	x7, x21
0x4cdc4	7ccac395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x4cdc8	08db5539	ldrb	w8, [x24, #0x576]
0x4cdcc	4a29691e	fadd	d10, d10, d9
0x4cdd0	4821601e	fcmp	d10, #0.0
0x4cdd4	cd040054	b.le	0x4ce6c <_WeChatMain+0x33600>
0x4cdd8	68000037	tbnz	w8, #0x0, 0x4cde4 <_WeChatMain+0x33578>
0x4cddc	b9020079	strh	w25, [x21]
0x4cde0	1adb1539	strb	w26, [x24, #0x576]
0x4cde4	e00315aa	mov	x0, x21
0x4cde8	04d3c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4cdec	f60300aa	mov	x22, x0
0x4cdf0	685e8039	ldrsb	x8, [x19, #0x17]
0x4cdf4	8800f8b7	tbnz	x8, #0x3f, 0x4ce04 <_WeChatMain+0x33598>
0x4cdf8	c1028052	mov	w1, #0x16               ; =22
0x4cdfc	f70308aa	mov	x23, x8
0x4ce00	04000014	b	0x4ce10 <_WeChatMain+0x335a4>
0x4ce04	77a640a9	ldp	x23, x9, [x19, #0x8]
0x4ce08	29f94092	and	x9, x9, #0x7fffffffffffffff
0x4ce0c	210500d1	sub	x1, x9, #0x1
0x4ce10	290017cb	sub	x9, x1, x23
0x4ce14	3f0116eb	cmp	x9, x22
0x4ce18	63fcff54	b.lo	0x4cda4 <_WeChatMain+0x33538>
0x4ce1c	d60100b4	cbz	x22, 0x4ce54 <_WeChatMain+0x335e8>
0x4ce20	fb0313aa	mov	x27, x19
0x4ce24	4800f836	tbz	w8, #0x1f, 0x4ce2c <_WeChatMain+0x335c0>
0x4ce28	7b0240f9	ldr	x27, [x19]
0x4ce2c	6003178b	add	x0, x27, x23
0x4ce30	e10315aa	mov	x1, x21
0x4ce34	e20316aa	mov	x2, x22
0x4ce38	17d0c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4ce3c	e802168b	add	x8, x23, x22
0x4ce40	695ec039	ldrsb	w9, [x19, #0x17]
0x4ce44	c900f837	tbnz	w9, #0x1f, 0x4ce5c <_WeChatMain+0x335f0>
0x4ce48	09190012	and	w9, w8, #0x7f
0x4ce4c	695e0039	strb	w9, [x19, #0x17]
0x4ce50	04000014	b	0x4ce60 <_WeChatMain+0x335f4>
0x4ce54	28008052	mov	w8, #0x1                ; =1
0x4ce58	ddffff17	b	0x4cdcc <_WeChatMain+0x33560>
0x4ce5c	680600f9	str	x8, [x19, #0x8]
0x4ce60	7f6b2838	strb	wzr, [x27, x8]
0x4ce64	28008052	mov	w8, #0x1                ; =1
0x4ce68	d9ffff17	b	0x4cdcc <_WeChatMain+0x33560>
0x4ce6c	8002621e	scvtf	d0, w20
0x4ce70	281005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4ce74	09e55539	ldrb	w9, [x8, #0x579]
0x4ce78	e9000037	tbnz	w9, #0x0, 0x4ce94 <_WeChatMain+0x33628>
0x4ce7c	291005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4ce80	29dd1591	add	x9, x9, #0x577
0x4ce84	ea098052	mov	w10, #0x4f              ; =79
0x4ce88	2a010079	strh	w10, [x9]
0x4ce8c	29008052	mov	w9, #0x1                ; =1
0x4ce90	09e51539	strb	w9, [x8, #0x579]
0x4ce94	0838681e	fsub	d8, d0, d8
0x4ce98	201005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4ce9c	00dc1591	add	x0, x0, #0x577
0x4cea0	d6d2c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4cea4	f40300aa	mov	x20, x0
0x4cea8	685e8039	ldrsb	x8, [x19, #0x17]
0x4ceac	8800f8b7	tbnz	x8, #0x3f, 0x4cebc <_WeChatMain+0x33650>
0x4ceb0	c1028052	mov	w1, #0x16               ; =22
0x4ceb4	f50308aa	mov	x21, x8
0x4ceb8	04000014	b	0x4cec8 <_WeChatMain+0x3365c>
0x4cebc	75a640a9	ldp	x21, x9, [x19, #0x8]
0x4cec0	29f94092	and	x9, x9, #0x7fffffffffffffff
0x4cec4	210500d1	sub	x1, x9, #0x1
0x4cec8	1601781e	fcvtzs	w22, d8
0x4cecc	290015cb	sub	x9, x1, x21
0x4ced0	3f0114eb	cmp	x9, x20
0x4ced4	c2010054	b.hs	0x4cf0c <_WeChatMain+0x336a0>
0x4ced8	880201cb	sub	x8, x20, x1
0x4cedc	271005d0	adrp	x7, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cee0	e7dc1591	add	x7, x7, #0x577
0x4cee4	0201158b	add	x2, x8, x21
0x4cee8	e00313aa	mov	x0, x19
0x4ceec	e30315aa	mov	x3, x21
0x4cef0	e40315aa	mov	x4, x21
0x4cef4	050080d2	mov	x5, #0x0                ; =0
0x4cef8	e60314aa	mov	x6, x20
0x4cefc	2ecac395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x4cf00	df060071	cmp	w22, #0x1
0x4cf04	6a020054	b.ge	0x4cf50 <_WeChatMain+0x336e4>
0x4cf08	50000014	b	0x4d048 <_WeChatMain+0x337dc>
0x4cf0c	f40100b4	cbz	x20, 0x4cf48 <_WeChatMain+0x336dc>
0x4cf10	f70313aa	mov	x23, x19
0x4cf14	4800f836	tbz	w8, #0x1f, 0x4cf1c <_WeChatMain+0x336b0>
0x4cf18	770240f9	ldr	x23, [x19]
0x4cf1c	211005d0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cf20	21dc1591	add	x1, x1, #0x577
0x4cf24	e002158b	add	x0, x23, x21
0x4cf28	e20314aa	mov	x2, x20
0x4cf2c	dacfc395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4cf30	a802148b	add	x8, x21, x20
0x4cf34	695ec039	ldrsb	w9, [x19, #0x17]
0x4cf38	0908f837	tbnz	w9, #0x1f, 0x4d038 <_WeChatMain+0x337cc>
0x4cf3c	09190012	and	w9, w8, #0x7f
0x4cf40	695e0039	strb	w9, [x19, #0x17]
0x4cf44	ff6a2838	strb	wzr, [x23, x8]
0x4cf48	df060071	cmp	w22, #0x1
0x4cf4c	eb070054	b.lt	0x4d048 <_WeChatMain+0x337dc>
0x4cf50	371005d0	adrp	x23, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cf54	e8f25539	ldrb	w8, [x23, #0x57c]
0x4cf58	d8060011	add	w24, w22, #0x1
0x4cf5c	19048052	mov	w25, #0x20              ; =32
0x4cf60	3a008052	mov	w26, #0x1               ; =1
0x4cf64	341005d0	adrp	x20, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4cf68	94ea1591	add	x20, x20, #0x57a
0x4cf6c	0e000014	b	0x4cfa4 <_WeChatMain+0x33738>
0x4cf70	a80201cb	sub	x8, x21, x1
0x4cf74	0201168b	add	x2, x8, x22
0x4cf78	e00313aa	mov	x0, x19
0x4cf7c	e30316aa	mov	x3, x22
0x4cf80	e40316aa	mov	x4, x22
0x4cf84	050080d2	mov	x5, #0x0                ; =0
0x4cf88	e60315aa	mov	x6, x21
0x4cf8c	e70314aa	mov	x7, x20
0x4cf90	09cac395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x4cf94	e8f25539	ldrb	w8, [x23, #0x57c]
0x4cf98	18070051	sub	w24, w24, #0x1
0x4cf9c	1f070071	cmp	w24, #0x1
0x4cfa0	49050054	b.ls	0x4d048 <_WeChatMain+0x337dc>
0x4cfa4	68000037	tbnz	w8, #0x0, 0x4cfb0 <_WeChatMain+0x33744>
0x4cfa8	99020079	strh	w25, [x20]
0x4cfac	faf21539	strb	w26, [x23, #0x57c]
0x4cfb0	e00314aa	mov	x0, x20
0x4cfb4	91d2c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4cfb8	f50300aa	mov	x21, x0
0x4cfbc	685e8039	ldrsb	x8, [x19, #0x17]
0x4cfc0	8800f8b7	tbnz	x8, #0x3f, 0x4cfd0 <_WeChatMain+0x33764>
0x4cfc4	c1028052	mov	w1, #0x16               ; =22
0x4cfc8	f60308aa	mov	x22, x8
0x4cfcc	04000014	b	0x4cfdc <_WeChatMain+0x33770>
0x4cfd0	76a640a9	ldp	x22, x9, [x19, #0x8]
0x4cfd4	29f94092	and	x9, x9, #0x7fffffffffffffff
0x4cfd8	210500d1	sub	x1, x9, #0x1
0x4cfdc	290016cb	sub	x9, x1, x22
0x4cfe0	3f0115eb	cmp	x9, x21
0x4cfe4	63fcff54	b.lo	0x4cf70 <_WeChatMain+0x33704>
0x4cfe8	d50100b4	cbz	x21, 0x4d020 <_WeChatMain+0x337b4>
0x4cfec	fb0313aa	mov	x27, x19
0x4cff0	4800f836	tbz	w8, #0x1f, 0x4cff8 <_WeChatMain+0x3378c>
0x4cff4	7b0240f9	ldr	x27, [x19]
0x4cff8	6003168b	add	x0, x27, x22
0x4cffc	e10314aa	mov	x1, x20
0x4d000	e20315aa	mov	x2, x21
0x4d004	a4cfc395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4d008	c802158b	add	x8, x22, x21
0x4d00c	695ec039	ldrsb	w9, [x19, #0x17]
0x4d010	c900f837	tbnz	w9, #0x1f, 0x4d028 <_WeChatMain+0x337bc>
0x4d014	09190012	and	w9, w8, #0x7f
0x4d018	695e0039	strb	w9, [x19, #0x17]
0x4d01c	04000014	b	0x4d02c <_WeChatMain+0x337c0>
0x4d020	28008052	mov	w8, #0x1                ; =1
0x4d024	ddffff17	b	0x4cf98 <_WeChatMain+0x3372c>
0x4d028	680600f9	str	x8, [x19, #0x8]
0x4d02c	7f6b2838	strb	wzr, [x27, x8]
0x4d030	28008052	mov	w8, #0x1                ; =1
0x4d034	d9ffff17	b	0x4cf98 <_WeChatMain+0x3372c>
0x4d038	680600f9	str	x8, [x19, #0x8]
0x4d03c	ff6a2838	strb	wzr, [x23, x8]
0x4d040	df060071	cmp	w22, #0x1
0x4d044	6af8ff54	b.ge	0x4cf50 <_WeChatMain+0x336e4>
0x4d048	fd7b47a9	ldp	x29, x30, [sp, #0x70]
0x4d04c	f44f46a9	ldp	x20, x19, [sp, #0x60]
0x4d050	f65745a9	ldp	x22, x21, [sp, #0x50]
0x4d054	f85f44a9	ldp	x24, x23, [sp, #0x40]
0x4d058	fa6743a9	ldp	x26, x25, [sp, #0x30]
0x4d05c	fc6f42a9	ldp	x28, x27, [sp, #0x20]
0x4d060	e923416d	ldp	d9, d8, [sp, #0x10]
0x4d064	eb2bc86c	ldp	d11, d10, [sp], #0x80
0x4d068	c0035fd6	ret
0x4d06c	e00302aa	mov	x0, x2
0x4d070	281005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4d074	09415639	ldrb	w9, [x8, #0x590]
0x4d078	e9000037	tbnz	w9, #0x0, 0x4d094 <_WeChatMain+0x33828>
0x4d07c	e9210490	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x4d080	21edc33d	ldr	q1, [x9, #0xfb0]
0x4d084	291005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4d088	2161813d	str	q1, [x9, #0x580]
0x4d08c	29008052	mov	w9, #0x1                ; =1
0x4d090	09411639	strb	w9, [x8, #0x590]
0x4d094	ff8300d1	sub	sp, sp, #0x20
0x4d098	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4d09c	fd430091	add	x29, sp, #0x10
0x4d0a0	2100621e	scvtf	d1, w1
0x4d0a4	2018601e	fdiv	d0, d1, d0
0x4d0a8	e10300f9	str	x1, [sp]
0x4d0ac	e00700fd	str	d0, [sp, #0x8]
0x4d0b0	211005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4d0b4	21001691	add	x1, x1, #0x580
0x4d0b8	786c0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x4d0bc	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4d0c0	ff830091	add	sp, sp, #0x20
0x4d0c4	c0035fd6	ret
0x4d0c8	00008052	mov	w0, #0x0                ; =0
0x4d0cc	c0035fd6	ret
0x4d0d0	010800b9	str	w1, [x0, #0x8]
0x4d0d4	68d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4d0d8	08010b91	add	x8, x8, #0x2c0
0x4d0dc	080000f9	str	x8, [x0]
0x4d0e0	021001a9	stp	x2, x4, [x0, #0x10]
0x4d0e4	032000b9	str	w3, [x0, #0x20]
0x4d0e8	c0035fd6	ret
0x4d0ec	c0035fd6	ret
0x4d0f0	01058052	mov	w1, #0x28               ; =40
0x4d0f4	c6cbc315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d0f8	082040b9	ldr	w8, [x0, #0x20]
0x4d0fc	1f010071	cmp	w8, #0x0
0x4d100	e0179f1a	cset	w0, eq
0x4d104	c0035fd6	ret
0x4d108	1f2000b9	str	wzr, [x0, #0x20]
0x4d10c	c0035fd6	ret
0x4d110	610000b4	cbz	x1, 0x4d11c <_WeChatMain+0x338b0>
0x4d114	080840b9	ldr	w8, [x0, #0x8]
0x4d118	280000b9	str	w8, [x1]
0x4d11c	620000b4	cbz	x2, 0x4d128 <_WeChatMain+0x338bc>
0x4d120	080840f9	ldr	x8, [x0, #0x10]
0x4d124	480000f9	str	x8, [x2]
0x4d128	630000b4	cbz	x3, 0x4d134 <_WeChatMain+0x338c8>
0x4d12c	082040b9	ldr	w8, [x0, #0x20]
0x4d130	680000b9	str	w8, [x3]
0x4d134	c0035fd6	ret
0x4d138	080c40f9	ldr	x8, [x0, #0x18]
0x4d13c	1f0500b1	cmn	x8, #0x1
0x4d140	40000054	b.eq	0x4d148 <_WeChatMain+0x338dc>
0x4d144	280000f9	str	x8, [x1]
0x4d148	1f0500b1	cmn	x8, #0x1
0x4d14c	e0079f1a	cset	w0, ne
0x4d150	c0035fd6	ret
0x4d154	68d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4d158	08e10c91	add	x8, x8, #0x338
0x4d15c	080000f9	str	x8, [x0]
0x4d160	080440f9	ldr	x8, [x0, #0x8]
0x4d164	09755e92	and	x9, x8, #0xfffffffc00000000
0x4d168	6afd04b0	adrp	x10, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4d16c	4a013b91	add	x10, x10, #0xec0
0x4d170	4a0540f9	ldr	x10, [x10, #0x8]
0x4d174	3f010aeb	cmp	x9, x10
0x4d178	41010054	b.ne	0x4d1a0 <_WeChatMain+0x33934>
0x4d17c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4d180	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4d184	fd430091	add	x29, sp, #0x10
0x4d188	f30300aa	mov	x19, x0
0x4d18c	e00308aa	mov	x0, x8
0x4d190	4ccaff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4d194	e00313aa	mov	x0, x19
0x4d198	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4d19c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4d1a0	01058052	mov	w1, #0x28               ; =40
0x4d1a4	9acbc315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d1a8	00904039	ldrb	w0, [x0, #0x24]
0x4d1ac	c0035fd6	ret
0x4d1b0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4d1b4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4d1b8	fd430091	add	x29, sp, #0x10
0x4d1bc	f30300aa	mov	x19, x0
0x4d1c0	000440f9	ldr	x0, [x0, #0x8]
0x4d1c4	61420091	add	x1, x19, #0x10
0x4d1c8	942a0094	bl	0x57c18 <_WeChatMain+0x3e3ac>
0x4d1cc	20010034	cbz	w0, 0x4d1f0 <_WeChatMain+0x33984>
0x4d1d0	600640f9	ldr	x0, [x19, #0x8]
0x4d1d4	61620091	add	x1, x19, #0x18
0x4d1d8	a22a0094	bl	0x57c60 <_WeChatMain+0x3e3f4>
0x4d1dc	a0000034	cbz	w0, 0x4d1f0 <_WeChatMain+0x33984>
0x4d1e0	600640f9	ldr	x0, [x19, #0x8]
0x4d1e4	61820091	add	x1, x19, #0x20
0x4d1e8	8c2a0094	bl	0x57c18 <_WeChatMain+0x3e3ac>
0x4d1ec	60000037	tbnz	w0, #0x0, 0x4d1f8 <_WeChatMain+0x3398c>
0x4d1f0	28008052	mov	w8, #0x1                ; =1
0x4d1f4	68920039	strb	w8, [x19, #0x24]
0x4d1f8	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4d1fc	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4d200	c0035fd6	ret
0x4d204	081040b9	ldr	w8, [x0, #0x10]
0x4d208	280000b9	str	w8, [x1]
0x4d20c	080c40f9	ldr	x8, [x0, #0x18]
0x4d210	480000f9	str	x8, [x2]
0x4d214	082040b9	ldr	w8, [x0, #0x20]
0x4d218	680000b9	str	w8, [x3]
0x4d21c	c0035fd6	ret
0x4d220	ffc300d1	sub	sp, sp, #0x30
0x4d224	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4d228	fd830091	add	x29, sp, #0x20
0x4d22c	48d704b0	adrp	x8, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x4d230	084d46f9	ldr	x8, [x8, #0xc98]
0x4d234	080140f9	ldr	x8, [x8]
0x4d238	a8831ff8	stur	x8, [x29, #-0x8]
0x4d23c	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4d240	e8a300a9	stp	x8, x8, [sp, #0x8]
0x4d244	e2230091	add	x2, sp, #0x8
0x4d248	8b9bff97	bl	0x34074 <_WeChatMain+0x1a808>
0x4d24c	e80740f9	ldr	x8, [sp, #0x8]
0x4d250	a9835ff8	ldur	x9, [x29, #-0x8]
0x4d254	4ad704b0	adrp	x10, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x4d258	4a4d46f9	ldr	x10, [x10, #0xc98]
0x4d25c	4a0140f9	ldr	x10, [x10]
0x4d260	5f0109eb	cmp	x10, x9
0x4d264	a1000054	b.ne	0x4d278 <_WeChatMain+0x33a0c>
0x4d268	000dc0da	rev	x0, x8
0x4d26c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4d270	ffc30091	add	sp, sp, #0x30
0x4d274	c0035fd6	ret
0x4d278	cbcbc395	bl	0x71401a4 <_wxam_enc_uninit_10+0x71401a4>
0x4d27c	ffc300d1	sub	sp, sp, #0x30
0x4d280	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4d284	fd830091	add	x29, sp, #0x20
0x4d288	48d704b0	adrp	x8, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x4d28c	084d46f9	ldr	x8, [x8, #0xc98]
0x4d290	080140f9	ldr	x8, [x8]
0x4d294	a8831ff8	stur	x8, [x29, #-0x8]
0x4d298	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4d29c	e8a300a9	stp	x8, x8, [sp, #0x8]
0x4d2a0	e2230091	add	x2, sp, #0x8
0x4d2a4	749bff97	bl	0x34074 <_WeChatMain+0x1a808>
0x4d2a8	e80b40b9	ldr	w8, [sp, #0x8]
0x4d2ac	a9835ff8	ldur	x9, [x29, #-0x8]
0x4d2b0	4ad704b0	adrp	x10, 0x9b36000 <_wxam_enc_uninit_10+0x9b36000>
0x4d2b4	4a4d46f9	ldr	x10, [x10, #0xc98]
0x4d2b8	4a0140f9	ldr	x10, [x10]
0x4d2bc	5f0109eb	cmp	x10, x9
0x4d2c0	a1000054	b.ne	0x4d2d4 <_WeChatMain+0x33a68>
0x4d2c4	0009c05a	rev	w0, w8
0x4d2c8	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4d2cc	ffc30091	add	sp, sp, #0x30
0x4d2d0	c0035fd6	ret
0x4d2d4	b4cbc395	bl	0x71401a4 <_wxam_enc_uninit_10+0x71401a4>
0x4d2d8	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4d2dc	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4d2e0	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4d2e4	fd830091	add	x29, sp, #0x20
0x4d2e8	f40302aa	mov	x20, x2
0x4d2ec	f50301aa	mov	x21, x1
0x4d2f0	f30300aa	mov	x19, x0
0x4d2f4	00c00091	add	x0, x0, #0x30
0x4d2f8	7fd0c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x4d2fc	60030035	cbnz	w0, 0x4d368 <_WeChatMain+0x33afc>
0x4d300	e00313aa	mov	x0, x19
0x4d304	e10315aa	mov	x1, x21
0x4d308	1b000094	bl	0x4d374 <_WeChatMain+0x33b08>
0x4d30c	f50300aa	mov	x21, x0
0x4d310	000840f9	ldr	x0, [x0, #0x10]
0x4d314	08745e92	and	x8, x0, #0xfffffffc00000000
0x4d318	76fd04b0	adrp	x22, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4d31c	d6023b91	add	x22, x22, #0xec0
0x4d320	c90640f9	ldr	x9, [x22, #0x8]
0x4d324	1f0109eb	cmp	x8, x9
0x4d328	41000054	b.ne	0x4d330 <_WeChatMain+0x33ac4>
0x4d32c	e5c9ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4d330	88765e92	and	x8, x20, #0xfffffffc00000000
0x4d334	c90640f9	ldr	x9, [x22, #0x8]
0x4d338	1f0109eb	cmp	x8, x9
0x4d33c	61000054	b.ne	0x4d348 <_WeChatMain+0x33adc>
0x4d340	e00314aa	mov	x0, x20
0x4d344	42c9ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4d348	b47e01a9	stp	x20, xzr, [x21, #0x10]
0x4d34c	60c20091	add	x0, x19, #0x30
0x4d350	6cd0c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x4d354	e00315aa	mov	x0, x21
0x4d358	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4d35c	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4d360	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4d364	c0035fd6	ret
0x4d368	60c20091	add	x0, x19, #0x30
0x4d36c	46740094	bl	0x6a484 <_WeChatMain+0x50c18>
0x4d370	e4ffff17	b	0x4d300 <_WeChatMain+0x33a94>
0x4d374	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x4d378	f65701a9	stp	x22, x21, [sp, #0x10]
0x4d37c	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4d380	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4d384	fdc30091	add	x29, sp, #0x30
0x4d388	f30301aa	mov	x19, x1
0x4d38c	f40300aa	mov	x20, x0
0x4d390	f60300aa	mov	x22, x0
0x4d394	c80e42f8	ldr	x8, [x22, #0x20]!
0x4d398	880300b4	cbz	x8, 0x4d408 <_WeChatMain+0x33b9c>
0x4d39c	e90316aa	mov	x9, x22
0x4d3a0	ea0308aa	mov	x10, x8
0x4d3a4	4b1140f9	ldr	x11, [x10, #0x20]
0x4d3a8	7f0113eb	cmp	x11, x19
0x4d3ac	29318a9a	csel	x9, x9, x10, lo
0x4d3b0	eb279f1a	cset	w11, lo
0x4d3b4	4a596bf8	ldr	x10, [x10, w11, uxtw #3]
0x4d3b8	6affffb5	cbnz	x10, 0x4d3a4 <_WeChatMain+0x33b38>
0x4d3bc	3f0116eb	cmp	x9, x22
0x4d3c0	20010054	b.eq	0x4d3e4 <_WeChatMain+0x33b78>
0x4d3c4	2a1140f9	ldr	x10, [x9, #0x20]
0x4d3c8	5f0113eb	cmp	x10, x19
0x4d3cc	c8000054	b.hi	0x4d3e4 <_WeChatMain+0x33b78>
0x4d3d0	36a10091	add	x22, x9, #0x28
0x4d3d4	37000014	b	0x4d4b0 <_WeChatMain+0x33c44>
0x4d3d8	a80240f9	ldr	x8, [x21]
0x4d3dc	f60315aa	mov	x22, x21
0x4d3e0	680100b4	cbz	x8, 0x4d40c <_WeChatMain+0x33ba0>
0x4d3e4	f50308aa	mov	x21, x8
0x4d3e8	081140f9	ldr	x8, [x8, #0x20]
0x4d3ec	1f0113eb	cmp	x8, x19
0x4d3f0	48ffff54	b.hi	0x4d3d8 <_WeChatMain+0x33b6c>
0x4d3f4	22030054	b.hs	0x4d458 <_WeChatMain+0x33bec>
0x4d3f8	a80640f9	ldr	x8, [x21, #0x8]
0x4d3fc	48ffffb5	cbnz	x8, 0x4d3e4 <_WeChatMain+0x33b78>
0x4d400	b6220091	add	x22, x21, #0x8
0x4d404	02000014	b	0x4d40c <_WeChatMain+0x33ba0>
0x4d408	f50316aa	mov	x21, x22
0x4d40c	f70315aa	mov	x23, x21
0x4d410	00068052	mov	w0, #0x30               ; =48
0x4d414	07cbc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4d418	f50300aa	mov	x21, x0
0x4d41c	137c02a9	stp	x19, xzr, [x0, #0x20]
0x4d420	1f7c00a9	stp	xzr, xzr, [x0]
0x4d424	170800f9	str	x23, [x0, #0x10]
0x4d428	c00200f9	str	x0, [x22]
0x4d42c	880e40f9	ldr	x8, [x20, #0x18]
0x4d430	080140f9	ldr	x8, [x8]
0x4d434	e10300aa	mov	x1, x0
0x4d438	680000b4	cbz	x8, 0x4d444 <_WeChatMain+0x33bd8>
0x4d43c	880e00f9	str	x8, [x20, #0x18]
0x4d440	c10240f9	ldr	x1, [x22]
0x4d444	801240f9	ldr	x0, [x20, #0x20]
0x4d448	3d5bff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x4d44c	881640f9	ldr	x8, [x20, #0x28]
0x4d450	08050091	add	x8, x8, #0x1
0x4d454	881600f9	str	x8, [x20, #0x28]
0x4d458	b6a20091	add	x22, x21, #0x28
0x4d45c	000a8052	mov	w0, #0x50               ; =80
0x4d460	f4cac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4d464	f50300aa	mov	x21, x0
0x4d468	88765e92	and	x8, x20, #0xfffffffc00000000
0x4d46c	69fd04b0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4d470	29013b91	add	x9, x9, #0xec0
0x4d474	290540f9	ldr	x9, [x9, #0x8]
0x4d478	1f0109eb	cmp	x8, x9
0x4d47c	61000054	b.ne	0x4d488 <_WeChatMain+0x33c1c>
0x4d480	e00314aa	mov	x0, x20
0x4d484	f2c8ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4d488	b44e00a9	stp	x20, x19, [x21]
0x4d48c	00e4006f	movi.2d	v0, #0000000000000000
0x4d490	a08200ad	stp	q0, q0, [x21, #0x10]
0x4d494	a08201ad	stp	q0, q0, [x21, #0x30]
0x4d498	c00240f9	ldr	x0, [x22]
0x4d49c	d50200f9	str	x21, [x22]
0x4d4a0	800000b4	cbz	x0, 0x4d4b0 <_WeChatMain+0x33c44>
0x4d4a4	3b010094	bl	0x4d990 <_WeChatMain+0x34124>
0x4d4a8	010a8052	mov	w1, #0x50               ; =80
0x4d4ac	d8cac395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d4b0	c00240f9	ldr	x0, [x22]
0x4d4b4	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4d4b8	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4d4bc	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4d4c0	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x4d4c4	c0035fd6	ret
0x4d4c8	ff4302d1	sub	sp, sp, #0x90
0x4d4cc	fc6f03a9	stp	x28, x27, [sp, #0x30]
0x4d4d0	fa6704a9	stp	x26, x25, [sp, #0x40]
0x4d4d4	f85f05a9	stp	x24, x23, [sp, #0x50]
0x4d4d8	f65706a9	stp	x22, x21, [sp, #0x60]
0x4d4dc	f44f07a9	stp	x20, x19, [sp, #0x70]
0x4d4e0	fd7b08a9	stp	x29, x30, [sp, #0x80]
0x4d4e4	fd030291	add	x29, sp, #0x80
0x4d4e8	f40301aa	mov	x20, x1
0x4d4ec	fb0300aa	mov	x27, x0
0x4d4f0	00c00091	add	x0, x0, #0x30
0x4d4f4	00d0c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x4d4f8	80230035	cbnz	w0, 0x4d968 <_WeChatMain+0x340fc>
0x4d4fc	96de43a9	ldp	x22, x23, [x20, #0x38]
0x4d500	df0217eb	cmp	x22, x23
0x4d504	fa079f1a	cset	w26, ne
0x4d508	000a0054	b.eq	0x4d648 <_WeChatMain+0x33ddc>
0x4d50c	fa2300b9	str	w26, [sp, #0x20]
0x4d510	fa031baa	mov	x26, x27
0x4d514	f50314aa	mov	x21, x20
0x4d518	b96ec2a9	ldp	x25, x27, [x21, #0x20]!
0x4d51c	a90a40f9	ldr	x9, [x21, #0x10]
0x4d520	730319cb	sub	x19, x27, x25
0x4d524	e80216cb	sub	x8, x23, x22
0x4d528	18fd4293	asr	x24, x8, #2
0x4d52c	080b938b	add	x8, x24, x19, asr #2
0x4d530	290119cb	sub	x9, x9, x25
0x4d534	1f0989eb	cmp	x8, x9, asr #2
0x4d538	49070054	b.ls	0x4d620 <_WeChatMain+0x33db4>
0x4d53c	e90700f9	str	x9, [sp, #0x8]
0x4d540	09fd7ed3	lsr	x9, x8, #62
0x4d544	292200b5	cbnz	x9, 0x4d988 <_WeChatMain+0x3411c>
0x4d548	1cf57ed3	lsl	x28, x8, #2
0x4d54c	e0031caa	mov	x0, x28
0x4d550	b8cac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4d554	0800138b	add	x8, x0, x19
0x4d558	09001c8b	add	x9, x0, x28
0x4d55c	ea0308aa	mov	x10, x8
0x4d560	6b0319eb	subs	x11, x27, x25
0x4d564	60040054	b.eq	0x4d5f0 <_WeChatMain+0x33d84>
0x4d568	6b1100d1	sub	x11, x11, #0x4
0x4d56c	7ff100f1	cmp	x11, #0x3c
0x4d570	63030054	b.lo	0x4d5dc <_WeChatMain+0x33d70>
0x4d574	2c0300cb	sub	x12, x25, x0
0x4d578	ea0308aa	mov	x10, x8
0x4d57c	9f0101f1	cmp	x12, #0x40
0x4d580	03030054	b.lo	0x4d5e0 <_WeChatMain+0x33d74>
0x4d584	6afd42d3	lsr	x10, x11, #2
0x4d588	4b050091	add	x11, x10, #0x1
0x4d58c	6ce97c92	and	x12, x11, #0x7ffffffffffffff0
0x4d590	8af57ed3	lsl	x10, x12, #2
0x4d594	6d030acb	sub	x13, x27, x10
0x4d598	0a010acb	sub	x10, x8, x10
0x4d59c	6e8300d1	sub	x14, x27, #0x20
0x4d5a0	cf0119cb	sub	x15, x14, x25
0x4d5a4	0f000f8b	add	x15, x0, x15
0x4d5a8	f0030caa	mov	x16, x12
0x4d5ac	c10140ad	ldp	q1, q0, [x14]
0x4d5b0	c3097fad	ldp	q3, q2, [x14, #-0x20]
0x4d5b4	e10100ad	stp	q1, q0, [x15]
0x4d5b8	e3093fad	stp	q3, q2, [x15, #-0x20]
0x4d5bc	ce0101d1	sub	x14, x14, #0x40
0x4d5c0	ef0101d1	sub	x15, x15, #0x40
0x4d5c4	104200d1	sub	x16, x16, #0x10
0x4d5c8	30ffffb5	cbnz	x16, 0x4d5ac <_WeChatMain+0x33d40>
0x4d5cc	fb030daa	mov	x27, x13
0x4d5d0	7f010ceb	cmp	x11, x12
0x4d5d4	61000054	b.ne	0x4d5e0 <_WeChatMain+0x33d74>
0x4d5d8	06000014	b	0x4d5f0 <_WeChatMain+0x33d84>
0x4d5dc	ea0308aa	mov	x10, x8
0x4d5e0	6bcf5fb8	ldr	w11, [x27, #-0x4]!
0x4d5e4	4bcd1fb8	str	w11, [x10, #-0x4]!
0x4d5e8	7f0319eb	cmp	x27, x25
0x4d5ec	a1ffff54	b.ne	0x4d5e0 <_WeChatMain+0x33d74>
0x4d5f0	8a2202a9	stp	x10, x8, [x20, #0x20]
0x4d5f4	891a00f9	str	x9, [x20, #0x30]
0x4d5f8	390100b4	cbz	x25, 0x4d61c <_WeChatMain+0x33db0>
0x4d5fc	e00319aa	mov	x0, x25
0x4d600	e10740f9	ldr	x1, [sp, #0x8]
0x4d604	82cac395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d608	9b1640f9	ldr	x27, [x20, #0x28]
0x4d60c	96de43a9	ldp	x22, x23, [x20, #0x38]
0x4d610	e80216cb	sub	x8, x23, x22
0x4d614	18fd4293	asr	x24, x8, #2
0x4d618	02000014	b	0x4d620 <_WeChatMain+0x33db4>
0x4d61c	fb0308aa	mov	x27, x8
0x4d620	e00315aa	mov	x0, x21
0x4d624	e1031baa	mov	x1, x27
0x4d628	e20316aa	mov	x2, x22
0x4d62c	e30317aa	mov	x3, x23
0x4d630	e40318aa	mov	x4, x24
0x4d634	e2020094	bl	0x4e1bc <_WeChatMain+0x34950>
0x4d638	881e40f9	ldr	x8, [x20, #0x38]
0x4d63c	882200f9	str	x8, [x20, #0x40]
0x4d640	fb031aaa	mov	x27, x26
0x4d644	fa2340b9	ldr	w26, [sp, #0x20]
0x4d648	08008052	mov	w8, #0x0                ; =0
0x4d64c	960640f9	ldr	x22, [x20, #0x8]
0x4d650	f7f301b2	mov	x23, #-0x5555555555555556 ; =-6148914691236517206
0x4d654	f4db01a9	stp	x20, x22, [sp, #0x18]
0x4d658	fb0b00f9	str	x27, [sp, #0x10]
0x4d65c	fc0308aa	mov	x28, x8
0x4d660	f71700f9	str	x23, [sp, #0x28]
0x4d664	60230091	add	x0, x27, #0x8
0x4d668	e1a30091	add	x1, sp, #0x28
0x4d66c	74080094	bl	0x4f83c <_WeChatMain+0x35fd0>
0x4d670	60160034	cbz	w0, 0x4d93c <_WeChatMain+0x340d0>
0x4d674	f80300aa	mov	x24, x0
0x4d678	e11740f9	ldr	x1, [sp, #0x28]
0x4d67c	3f0016eb	cmp	x1, x22
0x4d680	e1000054	b.ne	0x4d69c <_WeChatMain+0x33e30>
0x4d684	99a242a9	ldp	x25, x8, [x20, #0x28]
0x4d688	3f0308eb	cmp	x25, x8
0x4d68c	a2010054	b.hs	0x4d6c0 <_WeChatMain+0x33e54>
0x4d690	384700b8	str	w24, [x25], #0x4
0x4d694	fa0319aa	mov	x26, x25
0x4d698	71000014	b	0x4d85c <_WeChatMain+0x33ff0>
0x4d69c	e0031baa	mov	x0, x27
0x4d6a0	35ffff97	bl	0x4d374 <_WeChatMain+0x33b08>
0x4d6a4	f50300aa	mov	x21, x0
0x4d6a8	192044a9	ldp	x25, x8, [x0, #0x40]
0x4d6ac	3f0308eb	cmp	x25, x8
0x4d6b0	02030054	b.hs	0x4d710 <_WeChatMain+0x33ea4>
0x4d6b4	384700b8	str	w24, [x25], #0x4
0x4d6b8	f30319aa	mov	x19, x25
0x4d6bc	9a000014	b	0x4d924 <_WeChatMain+0x340b8>
0x4d6c0	950242f8	ldur	x21, [x20, #0x20]
0x4d6c4	330315cb	sub	x19, x25, x21
0x4d6c8	7afe4293	asr	x26, x19, #2
0x4d6cc	49070091	add	x9, x26, #0x1
0x4d6d0	2afd7ed3	lsr	x10, x9, #62
0x4d6d4	6a1500b5	cbnz	x10, 0x4d980 <_WeChatMain+0x34114>
0x4d6d8	160115cb	sub	x22, x8, x21
0x4d6dc	c8fe4193	asr	x8, x22, #1
0x4d6e0	1f0109eb	cmp	x8, x9
0x4d6e4	0881899a	csel	x8, x8, x9, hi
0x4d6e8	e9f37eb2	mov	x9, #0x7ffffffffffffffc ; =9223372036854775804
0x4d6ec	df0209eb	cmp	x22, x9
0x4d6f0	0900f892	mov	x9, #0x3fffffffffffffff ; =4611686018427387903
0x4d6f4	1731899a	csel	x23, x8, x9, lo
0x4d6f8	770300b4	cbz	x23, 0x4d764 <_WeChatMain+0x33ef8>
0x4d6fc	e8fe7ed3	lsr	x8, x23, #62
0x4d700	a81300b5	cbnz	x8, 0x4d974 <_WeChatMain+0x34108>
0x4d704	e0f67ed3	lsl	x0, x23, #2
0x4d708	4acac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4d70c	17000014	b	0x4d768 <_WeChatMain+0x33efc>
0x4d710	f7031aaa	mov	x23, x26
0x4d714	b68243f8	ldur	x22, [x21, #0x38]
0x4d718	3a0316cb	sub	x26, x25, x22
0x4d71c	53ff4293	asr	x19, x26, #2
0x4d720	69060091	add	x9, x19, #0x1
0x4d724	2afd7ed3	lsr	x10, x9, #62
0x4d728	8a1200b5	cbnz	x10, 0x4d978 <_WeChatMain+0x3410c>
0x4d72c	140116cb	sub	x20, x8, x22
0x4d730	88fe4193	asr	x8, x20, #1
0x4d734	1f0109eb	cmp	x8, x9
0x4d738	0881899a	csel	x8, x8, x9, hi
0x4d73c	e9f37eb2	mov	x9, #0x7ffffffffffffffc ; =9223372036854775804
0x4d740	9f0209eb	cmp	x20, x9
0x4d744	0900f892	mov	x9, #0x3fffffffffffffff ; =4611686018427387903
0x4d748	1b31899a	csel	x27, x8, x9, lo
0x4d74c	db0500b4	cbz	x27, 0x4d804 <_WeChatMain+0x33f98>
0x4d750	68ff7ed3	lsr	x8, x27, #62
0x4d754	081100b5	cbnz	x8, 0x4d974 <_WeChatMain+0x34108>
0x4d758	60f77ed3	lsl	x0, x27, #2
0x4d75c	35cac395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4d760	2a000014	b	0x4d808 <_WeChatMain+0x33f9c>
0x4d764	000080d2	mov	x0, #0x0                ; =0
0x4d768	09081a8b	add	x9, x0, x26, lsl #2
0x4d76c	fa0309aa	mov	x26, x9
0x4d770	584700b8	str	w24, [x26], #0x4
0x4d774	280315eb	subs	x8, x25, x21
0x4d778	e0050054	b.eq	0x4d834 <_WeChatMain+0x33fc8>
0x4d77c	081100d1	sub	x8, x8, #0x4
0x4d780	1ff100f1	cmp	x8, #0x3c
0x4d784	43030054	b.lo	0x4d7ec <_WeChatMain+0x33f80>
0x4d788	2a0300cb	sub	x10, x25, x0
0x4d78c	4a0113cb	sub	x10, x10, x19
0x4d790	5f0101f1	cmp	x10, #0x40
0x4d794	c3020054	b.lo	0x4d7ec <_WeChatMain+0x33f80>
0x4d798	08fd42d3	lsr	x8, x8, #2
0x4d79c	0a050091	add	x10, x8, #0x1
0x4d7a0	4be97c92	and	x11, x10, #0x7ffffffffffffff0
0x4d7a4	68f57ed3	lsl	x8, x11, #2
0x4d7a8	2c0308cb	sub	x12, x25, x8
0x4d7ac	280108cb	sub	x8, x9, x8
0x4d7b0	2d8300d1	sub	x13, x25, #0x20
0x4d7b4	298100d1	sub	x9, x9, #0x20
0x4d7b8	ee030baa	mov	x14, x11
0x4d7bc	a10140ad	ldp	q1, q0, [x13]
0x4d7c0	a3097fad	ldp	q3, q2, [x13, #-0x20]
0x4d7c4	210100ad	stp	q1, q0, [x9]
0x4d7c8	23093fad	stp	q3, q2, [x9, #-0x20]
0x4d7cc	ad0101d1	sub	x13, x13, #0x40
0x4d7d0	290101d1	sub	x9, x9, #0x40
0x4d7d4	ce4100d1	sub	x14, x14, #0x10
0x4d7d8	2effffb5	cbnz	x14, 0x4d7bc <_WeChatMain+0x33f50>
0x4d7dc	f9030caa	mov	x25, x12
0x4d7e0	e90308aa	mov	x9, x8
0x4d7e4	5f010beb	cmp	x10, x11
0x4d7e8	80020054	b.eq	0x4d838 <_WeChatMain+0x33fcc>
0x4d7ec	e80309aa	mov	x8, x9
0x4d7f0	29cf5fb8	ldr	w9, [x25, #-0x4]!
0x4d7f4	09cd1fb8	str	w9, [x8, #-0x4]!
0x4d7f8	3f0315eb	cmp	x25, x21
0x4d7fc	a1ffff54	b.ne	0x4d7f0 <_WeChatMain+0x33f84>
0x4d800	0e000014	b	0x4d838 <_WeChatMain+0x33fcc>
0x4d804	000080d2	mov	x0, #0x0                ; =0
0x4d808	0908138b	add	x9, x0, x19, lsl #2
0x4d80c	f30309aa	mov	x19, x9
0x4d810	784600b8	str	w24, [x19], #0x4
0x4d814	280316eb	subs	x8, x25, x22
0x4d818	c0020054	b.eq	0x4d870 <_WeChatMain+0x34004>
0x4d81c	081100d1	sub	x8, x8, #0x4
0x4d820	1ff100f1	cmp	x8, #0x3c
0x4d824	e2020054	b.hs	0x4d880 <_WeChatMain+0x34014>
0x4d828	fa0317aa	mov	x26, x23
0x4d82c	f7f301b2	mov	x23, #-0x5555555555555556 ; =-6148914691236517206
0x4d830	2f000014	b	0x4d8ec <_WeChatMain+0x34080>
0x4d834	e80309aa	mov	x8, x9
0x4d838	0908178b	add	x9, x0, x23, lsl #2
0x4d83c	886a02a9	stp	x8, x26, [x20, #0x20]
0x4d840	891a00f9	str	x9, [x20, #0x30]
0x4d844	950000b4	cbz	x21, 0x4d854 <_WeChatMain+0x33fe8>
0x4d848	e00315aa	mov	x0, x21
0x4d84c	e10316aa	mov	x1, x22
0x4d850	efc9c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d854	f61340f9	ldr	x22, [sp, #0x20]
0x4d858	f7f301b2	mov	x23, #-0x5555555555555556 ; =-6148914691236517206
0x4d85c	9a1600f9	str	x26, [x20, #0x28]
0x4d860	3a008052	mov	w26, #0x1               ; =1
0x4d864	88070011	add	w8, w28, #0x1
0x4d868	5a060037	tbnz	w26, #0x0, 0x4d930 <_WeChatMain+0x340c4>
0x4d86c	7cffff17	b	0x4d65c <_WeChatMain+0x33df0>
0x4d870	e80309aa	mov	x8, x9
0x4d874	fa0317aa	mov	x26, x23
0x4d878	f7f301b2	mov	x23, #-0x5555555555555556 ; =-6148914691236517206
0x4d87c	21000014	b	0x4d900 <_WeChatMain+0x34094>
0x4d880	2a0300cb	sub	x10, x25, x0
0x4d884	4a011acb	sub	x10, x10, x26
0x4d888	5f0101f1	cmp	x10, #0x40
0x4d88c	fa0317aa	mov	x26, x23
0x4d890	f7f301b2	mov	x23, #-0x5555555555555556 ; =-6148914691236517206
0x4d894	c3020054	b.lo	0x4d8ec <_WeChatMain+0x34080>
0x4d898	08fd42d3	lsr	x8, x8, #2
0x4d89c	0a050091	add	x10, x8, #0x1
0x4d8a0	4be97c92	and	x11, x10, #0x7ffffffffffffff0
0x4d8a4	68f57ed3	lsl	x8, x11, #2
0x4d8a8	2c0308cb	sub	x12, x25, x8
0x4d8ac	280108cb	sub	x8, x9, x8
0x4d8b0	2d8300d1	sub	x13, x25, #0x20
0x4d8b4	298100d1	sub	x9, x9, #0x20
0x4d8b8	ee030baa	mov	x14, x11
0x4d8bc	a10140ad	ldp	q1, q0, [x13]
0x4d8c0	a3097fad	ldp	q3, q2, [x13, #-0x20]
0x4d8c4	210100ad	stp	q1, q0, [x9]
0x4d8c8	23093fad	stp	q3, q2, [x9, #-0x20]
0x4d8cc	ad0101d1	sub	x13, x13, #0x40
0x4d8d0	290101d1	sub	x9, x9, #0x40
0x4d8d4	ce4100d1	sub	x14, x14, #0x10
0x4d8d8	2effffb5	cbnz	x14, 0x4d8bc <_WeChatMain+0x34050>
0x4d8dc	f9030caa	mov	x25, x12
0x4d8e0	e90308aa	mov	x9, x8
0x4d8e4	5f010beb	cmp	x10, x11
0x4d8e8	c0000054	b.eq	0x4d900 <_WeChatMain+0x34094>
0x4d8ec	e80309aa	mov	x8, x9
0x4d8f0	29cf5fb8	ldr	w9, [x25, #-0x4]!
0x4d8f4	09cd1fb8	str	w9, [x8, #-0x4]!
0x4d8f8	3f0316eb	cmp	x25, x22
0x4d8fc	a1ffff54	b.ne	0x4d8f0 <_WeChatMain+0x34084>
0x4d900	09081b8b	add	x9, x0, x27, lsl #2
0x4d904	a8ce03a9	stp	x8, x19, [x21, #0x38]
0x4d908	a92600f9	str	x9, [x21, #0x48]
0x4d90c	960000b4	cbz	x22, 0x4d91c <_WeChatMain+0x340b0>
0x4d910	e00316aa	mov	x0, x22
0x4d914	e10314aa	mov	x1, x20
0x4d918	bdc9c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d91c	fb5341a9	ldp	x27, x20, [sp, #0x10]
0x4d920	f61340f9	ldr	x22, [sp, #0x20]
0x4d924	b32200f9	str	x19, [x21, #0x40]
0x4d928	88070011	add	w8, w28, #0x1
0x4d92c	9ae90736	tbz	w26, #0x0, 0x4d65c <_WeChatMain+0x33df0>
0x4d930	9f270071	cmp	w28, #0x9
0x4d934	43e9ff54	b.lo	0x4d65c <_WeChatMain+0x33df0>
0x4d938	3a008052	mov	w26, #0x1               ; =1
0x4d93c	60c30091	add	x0, x27, #0x30
0x4d940	f0cec395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x4d944	40030012	and	w0, w26, #0x1
0x4d948	fd7b48a9	ldp	x29, x30, [sp, #0x80]
0x4d94c	f44f47a9	ldp	x20, x19, [sp, #0x70]
0x4d950	f65746a9	ldp	x22, x21, [sp, #0x60]
0x4d954	f85f45a9	ldp	x24, x23, [sp, #0x50]
0x4d958	fa6744a9	ldp	x26, x25, [sp, #0x40]
0x4d95c	fc6f43a9	ldp	x28, x27, [sp, #0x30]
0x4d960	ff430291	add	sp, sp, #0x90
0x4d964	c0035fd6	ret
0x4d968	60c30091	add	x0, x27, #0x30
0x4d96c	c6720094	bl	0x6a484 <_WeChatMain+0x50c18>
0x4d970	e3feff17	b	0x4d4fc <_WeChatMain+0x33c90>
0x4d974	7658ff97	bl	0x23b4c <_WeChatMain+0xa2e0>
0x4d978	a0e20091	add	x0, x21, #0x38
0x4d97c	72d1ff97	bl	0x41f44 <_WeChatMain+0x286d8>
0x4d980	80820091	add	x0, x20, #0x20
0x4d984	70d1ff97	bl	0x41f44 <_WeChatMain+0x286d8>
0x4d988	e00315aa	mov	x0, x21
0x4d98c	6ed1ff97	bl	0x41f44 <_WeChatMain+0x286d8>
0x4d990	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4d994	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4d998	fd430091	add	x29, sp, #0x10
0x4d99c	f30300aa	mov	x19, x0
0x4d9a0	001c40f9	ldr	x0, [x0, #0x38]
0x4d9a4	a00000b4	cbz	x0, 0x4d9b8 <_WeChatMain+0x3414c>
0x4d9a8	602200f9	str	x0, [x19, #0x40]
0x4d9ac	682640f9	ldr	x8, [x19, #0x48]
0x4d9b0	010100cb	sub	x1, x8, x0
0x4d9b4	96c9c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d9b8	601240f9	ldr	x0, [x19, #0x20]
0x4d9bc	a00000b4	cbz	x0, 0x4d9d0 <_WeChatMain+0x34164>
0x4d9c0	601600f9	str	x0, [x19, #0x28]
0x4d9c4	681a40f9	ldr	x8, [x19, #0x30]
0x4d9c8	010100cb	sub	x1, x8, x0
0x4d9cc	90c9c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4d9d0	600a40f9	ldr	x0, [x19, #0x10]
0x4d9d4	08745e92	and	x8, x0, #0xfffffffc00000000
0x4d9d8	74fd04b0	adrp	x20, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4d9dc	94023b91	add	x20, x20, #0xec0
0x4d9e0	890640f9	ldr	x9, [x20, #0x8]
0x4d9e4	1f0109eb	cmp	x8, x9
0x4d9e8	41000054	b.ne	0x4d9f0 <_WeChatMain+0x34184>
0x4d9ec	35c8ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4d9f0	7f0a00f9	str	xzr, [x19, #0x10]
0x4d9f4	600240f9	ldr	x0, [x19]
0x4d9f8	08745e92	and	x8, x0, #0xfffffffc00000000
0x4d9fc	890640f9	ldr	x9, [x20, #0x8]
0x4da00	1f0109eb	cmp	x8, x9
0x4da04	41000054	b.ne	0x4da0c <_WeChatMain+0x341a0>
0x4da08	2ec8ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4da0c	7f0200f9	str	xzr, [x19]
0x4da10	e00313aa	mov	x0, x19
0x4da14	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4da18	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4da1c	c0035fd6	ret
0x4da20	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4da24	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4da28	fd430091	add	x29, sp, #0x10
0x4da2c	f30300aa	mov	x19, x0
0x4da30	000840f9	ldr	x0, [x0, #0x10]
0x4da34	08745e92	and	x8, x0, #0xfffffffc00000000
0x4da38	69fd04b0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4da3c	29013b91	add	x9, x9, #0xec0
0x4da40	290540f9	ldr	x9, [x9, #0x8]
0x4da44	1f0109eb	cmp	x8, x9
0x4da48	41000054	b.ne	0x4da50 <_WeChatMain+0x341e4>
0x4da4c	1dc8ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4da50	7f0a00f9	str	xzr, [x19, #0x10]
0x4da54	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4da58	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4da5c	c0035fd6	ret
0x4da60	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4da64	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4da68	fd430091	add	x29, sp, #0x10
0x4da6c	f30300aa	mov	x19, x0
0x4da70	082842a9	ldp	x8, x10, [x0, #0x20]
0x4da74	090c40f9	ldr	x9, [x0, #0x18]
0x4da78	4a0108cb	sub	x10, x10, x8
0x4da7c	3f098aeb	cmp	x9, x10, asr #2
0x4da80	c1000054	b.ne	0x4da98 <_WeChatMain+0x3422c>
0x4da84	600240f9	ldr	x0, [x19]
0x4da88	e10313aa	mov	x1, x19
0x4da8c	8ffeff97	bl	0x4d4c8 <_WeChatMain+0x33c5c>
0x4da90	a0000034	cbz	w0, 0x4daa4 <_WeChatMain+0x34238>
0x4da94	69a241a9	ldp	x9, x8, [x19, #0x18]
0x4da98	2a050091	add	x10, x9, #0x1
0x4da9c	6a0e00f9	str	x10, [x19, #0x18]
0x4daa0	007969b8	ldr	w0, [x8, x9, lsl #2]
0x4daa4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4daa8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4daac	c0035fd6	ret
0x4dab0	e20301aa	mov	x2, x1
0x4dab4	080440a9	ldp	x8, x1, [x0]
0x4dab8	000140f9	ldr	x0, [x8]
0x4dabc	7b070014	b	0x4f8a8 <_WeChatMain+0x3603c>
0x4dac0	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4dac4	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4dac8	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4dacc	fd830091	add	x29, sp, #0x20
0x4dad0	f60301aa	mov	x22, x1
0x4dad4	f40300aa	mov	x20, x0
0x4dad8	f30308aa	mov	x19, x8
0x4dadc	000440f9	ldr	x0, [x0, #0x8]
0x4dae0	62228b52	mov	w2, #0x5913             ; =22803
0x4dae4	822cbe72	movk	w2, #0xf164, lsl #16
0x4dae8	030b8052	mov	w3, #0x58               ; =88
0x4daec	e7030094	bl	0x4ea88 <_WeChatMain+0x3521c>
0x4daf0	f50300aa	mov	x21, x0
0x4daf4	800640f9	ldr	x0, [x20, #0x8]
0x4daf8	e10316aa	mov	x1, x22
0x4dafc	94030094	bl	0x4e94c <_WeChatMain+0x350e0>
0x4db00	f50000b4	cbz	x21, 0x4db1c <_WeChatMain+0x342b0>
0x4db04	f60315aa	mov	x22, x21
0x4db08	c80e4538	ldrb	w8, [x22, #0x50]!
0x4db0c	88000034	cbz	w8, 0x4db1c <_WeChatMain+0x342b0>
0x4db10	a802008b	add	x8, x21, x0
0x4db14	08f15f38	ldurb	w8, [x8, #-0x1]
0x4db18	c8000034	cbz	w8, 0x4db30 <_WeChatMain+0x342c4>
0x4db1c	7f0200f9	str	xzr, [x19]
0x4db20	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4db24	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4db28	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4db2c	c0035fd6	ret
0x4db30	a81240f9	ldr	x8, [x21, #0x20]
0x4db34	48ffffb4	cbz	x8, 0x4db1c <_WeChatMain+0x342b0>
0x4db38	a91e40f9	ldr	x9, [x21, #0x38]
0x4db3c	09ffffb4	cbz	x9, 0x4db1c <_WeChatMain+0x342b0>
0x4db40	0a050091	add	x10, x8, #0x1
0x4db44	3f0108eb	cmp	x9, x8
0x4db48	24114afa	ccmp	x9, x10, #0x4, ne
0x4db4c	81feff54	b.ne	0x4db1c <_WeChatMain+0x342b0>
0x4db50	e00316aa	mov	x0, x22
0x4db54	a9cfc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4db58	e10300aa	mov	x1, x0
0x4db5c	e00316aa	mov	x0, x22
0x4db60	b0fdff97	bl	0x4d220 <_WeChatMain+0x339b4>
0x4db64	a81240f9	ldr	x8, [x21, #0x20]
0x4db68	1f0008eb	cmp	x0, x8
0x4db6c	81fdff54	b.ne	0x4db1c <_WeChatMain+0x342b0>
0x4db70	e80313aa	mov	x8, x19
0x4db74	e00314aa	mov	x0, x20
0x4db78	e10315aa	mov	x1, x21
0x4db7c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4db80	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4db84	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4db88	01000014	b	0x4db8c <_WeChatMain+0x34320>
0x4db8c	ffc302d1	sub	sp, sp, #0xb0
0x4db90	fc6f05a9	stp	x28, x27, [sp, #0x50]
0x4db94	fa6706a9	stp	x26, x25, [sp, #0x60]
0x4db98	f85f07a9	stp	x24, x23, [sp, #0x70]
0x4db9c	f65708a9	stp	x22, x21, [sp, #0x80]
0x4dba0	f44f09a9	stp	x20, x19, [sp, #0x90]
0x4dba4	fd7b0aa9	stp	x29, x30, [sp, #0xa0]
0x4dba8	fd830291	add	x29, sp, #0xa0
0x4dbac	f30308aa	mov	x19, x8
0x4dbb0	010c00b4	cbz	x1, 0x4dd30 <_WeChatMain+0x344c4>
0x4dbb4	390040b9	ldr	w25, [x1]
0x4dbb8	3f130071	cmp	w25, #0x4
0x4dbbc	61020054	b.ne	0x4dc08 <_WeChatMain+0x3439c>
0x4dbc0	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4dbc4	680200f9	str	x8, [x19]
0x4dbc8	f40301aa	mov	x20, x1
0x4dbcc	21400191	add	x1, x1, #0x50
0x4dbd0	82820091	add	x2, x20, #0x20
0x4dbd4	83e20091	add	x3, x20, #0x38
0x4dbd8	e80313aa	mov	x8, x19
0x4dbdc	be120094	bl	0x526d4 <_WeChatMain+0x38e68>
0x4dbe0	600240f9	ldr	x0, [x19]
0x4dbe4	810640b9	ldr	w1, [x20, #0x4]
0x4dbe8	fd7b4aa9	ldp	x29, x30, [sp, #0xa0]
0x4dbec	f44f49a9	ldp	x20, x19, [sp, #0x90]
0x4dbf0	f65748a9	ldp	x22, x21, [sp, #0x80]
0x4dbf4	f85f47a9	ldp	x24, x23, [sp, #0x70]
0x4dbf8	fa6746a9	ldp	x26, x25, [sp, #0x60]
0x4dbfc	fc6f45a9	ldp	x28, x27, [sp, #0x50]
0x4dc00	ffc30291	add	sp, sp, #0xb0
0x4dc04	3af6ff17	b	0x4b4ec <_WeChatMain+0x31c80>
0x4dc08	340440b9	ldr	w20, [x1, #0x4]
0x4dc0c	3a584229	ldp	w26, w22, [x1, #0x10]
0x4dc10	f80301aa	mov	x24, x1
0x4dc14	3c1840b9	ldr	w28, [x1, #0x18]
0x4dc18	080440f9	ldr	x8, [x0, #0x8]
0x4dc1c	f70300aa	mov	x23, x0
0x4dc20	e00308aa	mov	x0, x8
0x4dc24	e10316aa	mov	x1, x22
0x4dc28	624b8452	mov	w2, #0x225b             ; =8795
0x4dc2c	429db772	movk	w2, #0xbcea, lsl #16
0x4dc30	83008052	mov	w3, #0x4                ; =4
0x4dc34	95030094	bl	0x4ea88 <_WeChatMain+0x3521c>
0x4dc38	f50300aa	mov	x21, x0
0x4dc3c	fb0317aa	mov	x27, x23
0x4dc40	e00640f9	ldr	x0, [x23, #0x8]
0x4dc44	e10316aa	mov	x1, x22
0x4dc48	41030094	bl	0x4e94c <_WeChatMain+0x350e0>
0x4dc4c	350700b4	cbz	x21, 0x4dd30 <_WeChatMain+0x344c4>
0x4dc50	57070011	add	w23, w26, #0x1
0x4dc54	e80b0232	mov	w8, #-0x3fffffff        ; =-1073741823
0x4dc58	e97e7ed3	ubfiz	x9, x23, #2, #32
0x4dc5c	ea0f0232	mov	w10, #-0x3ffffffd       ; =-1073741821
0x4dc60	4803080b	add	w8, w26, w8
0x4dc64	1f010a6b	cmp	w8, w10
0x4dc68	002049fa	ccmp	x0, x9, #0x0, hs
0x4dc6c	23060054	b.lo	0x4dd30 <_WeChatMain+0x344c4>
0x4dc70	00048052	mov	w0, #0x20               ; =32
0x4dc74	efc8c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4dc78	f60300aa	mov	x22, x0
0x4dc7c	e10317aa	mov	x1, x23
0x4dc80	f9e1ff97	bl	0x46464 <_WeChatMain+0x2cbf8>
0x4dc84	a94640b8	ldr	w9, [x21], #0x4
0x4dc88	080040f9	ldr	x8, [x0]
0x4dc8c	094500b8	str	w9, [x8], #0x4
0x4dc90	e90600d1	sub	x9, x23, #0x1
0x4dc94	abaa7f29	ldp	w11, w10, [x21, #-0x4]
0x4dc98	5f010b6b	cmp	w10, w11
0x4dc9c	0d020054	b.le	0x4dcdc <_WeChatMain+0x34470>
0x4dca0	b5120091	add	x21, x21, #0x4
0x4dca4	0a4500b8	str	w10, [x8], #0x4
0x4dca8	290500f1	subs	x9, x9, #0x1
0x4dcac	41ffff54	b.ne	0x4dc94 <_WeChatMain+0x34428>
0x4dcb0	e00316aa	mov	x0, x22
0x4dcb4	27e2ff97	bl	0x46550 <_WeChatMain+0x2cce4>
0x4dcb8	c81a40b9	ldr	w8, [x22, #0x18]
0x4dcbc	1f011c6b	cmp	w8, w28
0x4dcc0	e1000054	b.ne	0x4dcdc <_WeChatMain+0x34470>
0x4dcc4	760300b4	cbz	x22, 0x4dd30 <_WeChatMain+0x344c4>
0x4dcc8	600b40f9	ldr	x0, [x27, #0x10]
0x4dccc	600100b4	cbz	x0, 0x4dcf8 <_WeChatMain+0x3448c>
0x4dcd0	e10316aa	mov	x1, x22
0x4dcd4	b3070094	bl	0x4fba0 <_WeChatMain+0x36334>
0x4dcd8	0a000014	b	0x4dd00 <_WeChatMain+0x34494>
0x4dcdc	b60200b4	cbz	x22, 0x4dd30 <_WeChatMain+0x344c4>
0x4dce0	e00316aa	mov	x0, x22
0x4dce4	fbe1ff97	bl	0x464d0 <_WeChatMain+0x2cc64>
0x4dce8	01048052	mov	w1, #0x20               ; =32
0x4dcec	c8c8c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4dcf0	7f0200f9	str	xzr, [x19]
0x4dcf4	10000014	b	0x4dd34 <_WeChatMain+0x344c8>
0x4dcf8	e00316aa	mov	x0, x22
0x4dcfc	1e150094	bl	0x53174 <_WeChatMain+0x39908>
0x4dd00	f50300aa	mov	x21, x0
0x4dd04	56f37dd3	lsl	x22, x26, #3
0x4dd08	e80318aa	mov	x8, x24
0x4dd0c	01c34199	ldapur	w1, [x24, #0x1c]
0x4dd10	e9031baa	mov	x9, x27
0x4dd14	01020034	cbz	w1, 0x4dd54 <_WeChatMain+0x344e8>
0x4dd18	200540f9	ldr	x0, [x9, #0x8]
0x4dd1c	0c030094	bl	0x4e94c <_WeChatMain+0x350e0>
0x4dd20	e80318aa	mov	x8, x24
0x4dd24	e9031baa	mov	x9, x27
0x4dd28	1f0016eb	cmp	x0, x22
0x4dd2c	42010054	b.hs	0x4dd54 <_WeChatMain+0x344e8>
0x4dd30	7f0200f9	str	xzr, [x19]
0x4dd34	fd7b4aa9	ldp	x29, x30, [sp, #0xa0]
0x4dd38	f44f49a9	ldp	x20, x19, [sp, #0x90]
0x4dd3c	f65748a9	ldp	x22, x21, [sp, #0x80]
0x4dd40	f85f47a9	ldp	x24, x23, [sp, #0x70]
0x4dd44	fa6746a9	ldp	x26, x25, [sp, #0x60]
0x4dd48	fc6f45a9	ldp	x28, x27, [sp, #0x50]
0x4dd4c	ffc30291	add	sp, sp, #0xb0
0x4dd50	c0035fd6	ret
0x4dd54	40e5054f	movi.16b	v0, #0xaa
0x4dd58	e08301ad	stp	q0, q0, [sp, #0x30]
0x4dd5c	210540f9	ldr	x1, [x9, #0x8]
0x4dd60	f70309aa	mov	x23, x9
0x4dd64	e0c30091	add	x0, sp, #0x30
0x4dd68	02710091	add	x2, x8, #0x1c
0x4dd6c	fb0308aa	mov	x27, x8
0x4dd70	23a68a52	mov	w3, #0x5531             ; =21809
0x4dd74	2364aa72	movk	w3, #0x5321, lsl #16
0x4dd78	e40316aa	mov	x4, x22
0x4dd7c	05008052	mov	w5, #0x0                ; =0
0x4dd80	78040094	bl	0x4ef60 <_WeChatMain+0x356f4>
0x4dd84	40e5054f	movi.16b	v0, #0xaa
0x4dd88	e08300ad	stp	q0, q0, [sp, #0x10]
0x4dd8c	45f77ed3	lsl	x5, x26, #2
0x4dd90	e10640f9	ldr	x1, [x23, #0x8]
0x4dd94	e0430091	add	x0, sp, #0x10
0x4dd98	62730091	add	x2, x27, #0x1c
0x4dd9c	23a68a52	mov	w3, #0x5531             ; =21809
0x4dda0	2364aa72	movk	w3, #0x5321, lsl #16
0x4dda4	e40316aa	mov	x4, x22
0x4dda8	06008052	mov	w6, #0x0                ; =0
0x4ddac	76040094	bl	0x4ef84 <_WeChatMain+0x35718>
0x4ddb0	160080d2	mov	x22, #0x0               ; =0
0x4ddb4	3f070071	cmp	w25, #0x1
0x4ddb8	ac010054	b.gt	0x4ddec <_WeChatMain+0x34580>
0x4ddbc	39030034	cbz	w25, 0x4de20 <_WeChatMain+0x345b4>
0x4ddc0	3f070071	cmp	w25, #0x1
0x4ddc4	a1050054	b.ne	0x4de78 <_WeChatMain+0x3460c>
0x4ddc8	e8230091	add	x8, sp, #0x8
0x4ddcc	00430191	add	x0, x24, #0x50
0x4ddd0	e2c30091	add	x2, sp, #0x30
0x4ddd4	e3430091	add	x3, sp, #0x10
0x4ddd8	04830091	add	x4, x24, #0x20
0x4dddc	05e30091	add	x5, x24, #0x38
0x4dde0	e10315aa	mov	x1, x21
0x4dde4	e6efff97	bl	0x49d7c <_WeChatMain+0x30510>
0x4dde8	1f000014	b	0x4de64 <_WeChatMain+0x345f8>
0x4ddec	3f0b0071	cmp	w25, #0x2
0x4ddf0	a0020054	b.eq	0x4de44 <_WeChatMain+0x345d8>
0x4ddf4	3f0f0071	cmp	w25, #0x3
0x4ddf8	01040054	b.ne	0x4de78 <_WeChatMain+0x3460c>
0x4ddfc	e8230091	add	x8, sp, #0x8
0x4de00	00430191	add	x0, x24, #0x50
0x4de04	e2c30091	add	x2, sp, #0x30
0x4de08	e3430091	add	x3, sp, #0x10
0x4de0c	04830091	add	x4, x24, #0x20
0x4de10	05e30091	add	x5, x24, #0x38
0x4de14	e10315aa	mov	x1, x21
0x4de18	d9f0ff97	bl	0x4a17c <_WeChatMain+0x30910>
0x4de1c	12000014	b	0x4de64 <_WeChatMain+0x345f8>
0x4de20	e8230091	add	x8, sp, #0x8
0x4de24	00430191	add	x0, x24, #0x50
0x4de28	e2c30091	add	x2, sp, #0x30
0x4de2c	e3430091	add	x3, sp, #0x10
0x4de30	04830091	add	x4, x24, #0x20
0x4de34	05e30091	add	x5, x24, #0x38
0x4de38	e10315aa	mov	x1, x21
0x4de3c	10ecff97	bl	0x48e7c <_WeChatMain+0x2f610>
0x4de40	09000014	b	0x4de64 <_WeChatMain+0x345f8>
0x4de44	e8230091	add	x8, sp, #0x8
0x4de48	00430191	add	x0, x24, #0x50
0x4de4c	e2c30091	add	x2, sp, #0x30
0x4de50	e3430091	add	x3, sp, #0x10
0x4de54	04830091	add	x4, x24, #0x20
0x4de58	05e30091	add	x5, x24, #0x38
0x4de5c	e10315aa	mov	x1, x21
0x4de60	a1f0ff97	bl	0x4a0e4 <_WeChatMain+0x30878>
0x4de64	f60740f9	ldr	x22, [sp, #0x8]
0x4de68	960000b4	cbz	x22, 0x4de78 <_WeChatMain+0x3460c>
0x4de6c	e00316aa	mov	x0, x22
0x4de70	e10314aa	mov	x1, x20
0x4de74	9ef5ff97	bl	0x4b4ec <_WeChatMain+0x31c80>
0x4de78	760200f9	str	x22, [x19]
0x4de7c	e0430091	add	x0, sp, #0x10
0x4de80	9333ff97	bl	0x1accc <_WeChatMain+0x1460>
0x4de84	e0c30091	add	x0, sp, #0x30
0x4de88	9133ff97	bl	0x1accc <_WeChatMain+0x1460>
0x4de8c	aaffff17	b	0x4dd34 <_WeChatMain+0x344c8>
0x4de90	ffc301d1	sub	sp, sp, #0x70
0x4de94	fc6f01a9	stp	x28, x27, [sp, #0x10]
0x4de98	fa6702a9	stp	x26, x25, [sp, #0x20]
0x4de9c	f85f03a9	stp	x24, x23, [sp, #0x30]
0x4dea0	f65704a9	stp	x22, x21, [sp, #0x40]
0x4dea4	f44f05a9	stp	x20, x19, [sp, #0x50]
0x4dea8	fd7b06a9	stp	x29, x30, [sp, #0x60]
0x4deac	fd830191	add	x29, sp, #0x60
0x4deb0	f30307aa	mov	x19, x7
0x4deb4	fb0306aa	mov	x27, x6
0x4deb8	f60305aa	mov	x22, x5
0x4debc	f70304aa	mov	x23, x4
0x4dec0	f80303aa	mov	x24, x3
0x4dec4	fc0302aa	mov	x28, x2
0x4dec8	fa0301aa	mov	x26, x1
0x4decc	f40300aa	mov	x20, x0
0x4ded0	f50308aa	mov	x21, x8
0x4ded4	000440f9	ldr	x0, [x0, #0x8]
0x4ded8	c7030094	bl	0x4edf4 <_WeChatMain+0x35588>
0x4dedc	60000034	cbz	w0, 0x4dee8 <_WeChatMain+0x3467c>
0x4dee0	bf0200f9	str	xzr, [x21]
0x4dee4	4c000014	b	0x4e014 <_WeChatMain+0x347a8>
0x4dee8	f70f00b9	str	w23, [sp, #0xc]
0x4deec	990640f9	ldr	x25, [x20, #0x8]
0x4def0	885f4039	ldrb	w8, [x28, #0x17]
0x4def4	091d0013	sxtb	w9, w8
0x4def8	8a0740f9	ldr	x10, [x28, #0x8]
0x4defc	3f010071	cmp	w9, #0x0
0x4df00	48b1889a	csel	x8, x10, x8, lt
0x4df04	08450191	add	x8, x8, #0x51
0x4df08	090b8052	mov	w9, #0x58               ; =88
0x4df0c	1f6101f1	cmp	x8, #0x58
0x4df10	1781899a	csel	x23, x8, x9, hi
0x4df14	e00319aa	mov	x0, x25
0x4df18	e10317aa	mov	x1, x23
0x4df1c	62228b52	mov	w2, #0x5913             ; =22803
0x4df20	822cbe72	movk	w2, #0xf164, lsl #16
0x4df24	72020094	bl	0x4e8ec <_WeChatMain+0x35080>
0x4df28	e10300aa	mov	x1, x0
0x4df2c	e00319aa	mov	x0, x25
0x4df30	62228b52	mov	w2, #0x5913             ; =22803
0x4df34	822cbe72	movk	w2, #0xf164, lsl #16
0x4df38	e30317aa	mov	x3, x23
0x4df3c	d3020094	bl	0x4ea88 <_WeChatMain+0x3521c>
0x4df40	f90300aa	mov	x25, x0
0x4df44	200200b4	cbz	x0, 0x4df88 <_WeChatMain+0x3471c>
0x4df48	00e4006f	movi.2d	v0, #0000000000000000
0x4df4c	208301ad	stp	q0, q0, [x25, #0x30]
0x4df50	208300ad	stp	q0, q0, [x25, #0x10]
0x4df54	2003803d	str	q0, [x25]
0x4df58	e00319aa	mov	x0, x25
0x4df5c	1f0c05f8	str	xzr, [x0, #0x50]!
0x4df60	885f4039	ldrb	w8, [x28, #0x17]
0x4df64	091d0013	sxtb	w9, w8
0x4df68	8a2f40a9	ldp	x10, x11, [x28]
0x4df6c	3f010071	cmp	w9, #0x0
0x4df70	41b19c9a	csel	x1, x10, x28, lt
0x4df74	68b1889a	csel	x8, x11, x8, lt
0x4df78	02050091	add	x2, x8, #0x1
0x4df7c	c3cbc395	bl	0x7140e88 <_wxam_enc_uninit_10+0x7140e88>
0x4df80	68031a32	orr	w8, w27, #0x40
0x4df84	3a230029	stp	w26, w8, [x25]
0x4df88	5f130071	cmp	w26, #0x4
0x4df8c	61000054	b.ne	0x4df98 <_WeChatMain+0x3472c>
0x4df90	790200b5	cbnz	x25, 0x4dfdc <_WeChatMain+0x34770>
0x4df94	d3ffff17	b	0x4dee0 <_WeChatMain+0x34674>
0x4df98	c92240a9	ldp	x9, x8, [x22]
0x4df9c	1a0109cb	sub	x26, x8, x9
0x4dfa0	0800e492	mov	x8, #-0x2000000000000001 ; =-2305843009213693953
0x4dfa4	08099a8b	add	x8, x8, x26, asr #2
0x4dfa8	0900fcd2	mov	x9, #-0x2000000000000000 ; =-2305843009213693952
0x4dfac	1f0109eb	cmp	x8, x9
0x4dfb0	89f9ff54	b.ls	0x4dee0 <_WeChatMain+0x34674>
0x4dfb4	dbc24199	ldapur	w27, [x22, #0x1c]
0x4dfb8	fb030034	cbz	w27, 0x4e034 <_WeChatMain+0x347c8>
0x4dfbc	39f9ffb4	cbz	x25, 0x4dee0 <_WeChatMain+0x34674>
0x4dfc0	48ff42d3	lsr	x8, x26, #2
0x4dfc4	e90f40b9	ldr	w9, [sp, #0xc]
0x4dfc8	38270129	stp	w24, w9, [x25, #0x8]
0x4dfcc	08050051	sub	w8, w8, #0x1
0x4dfd0	286f0229	stp	w8, w27, [x25, #0x10]
0x4dfd4	c81a40b9	ldr	w8, [x22, #0x18]
0x4dfd8	281b00b9	str	w8, [x25, #0x18]
0x4dfdc	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x4dfe0	a80200f9	str	x8, [x21]
0x4dfe4	e80315aa	mov	x8, x21
0x4dfe8	e00314aa	mov	x0, x20
0x4dfec	e10319aa	mov	x1, x25
0x4dff0	e7feff97	bl	0x4db8c <_WeChatMain+0x34320>
0x4dff4	800640f9	ldr	x0, [x20, #0x8]
0x4dff8	e10319aa	mov	x1, x25
0x4dffc	62228b52	mov	w2, #0x5913             ; =22803
0x4e000	822cbe72	movk	w2, #0xf164, lsl #16
0x4e004	7c020094	bl	0x4e9f4 <_WeChatMain+0x35188>
0x4e008	530000b4	cbz	x19, 0x4e010 <_WeChatMain+0x347a4>
0x4e00c	600200b9	str	w0, [x19]
0x4e010	808a00b9	str	w0, [x20, #0x88]
0x4e014	fd7b46a9	ldp	x29, x30, [sp, #0x60]
0x4e018	f44f45a9	ldp	x20, x19, [sp, #0x50]
0x4e01c	f65744a9	ldp	x22, x21, [sp, #0x40]
0x4e020	f85f43a9	ldp	x24, x23, [sp, #0x30]
0x4e024	fa6742a9	ldp	x26, x25, [sp, #0x20]
0x4e028	fc6f41a9	ldp	x28, x27, [sp, #0x10]
0x4e02c	ffc30191	add	sp, sp, #0x70
0x4e030	c0035fd6	ret
0x4e034	800640f9	ldr	x0, [x20, #0x8]
0x4e038	e1031aaa	mov	x1, x26
0x4e03c	624b8452	mov	w2, #0x225b             ; =8795
0x4e040	429db772	movk	w2, #0xbcea, lsl #16
0x4e044	2a020094	bl	0x4e8ec <_WeChatMain+0x35080>
0x4e048	c0f4ff34	cbz	w0, 0x4dee0 <_WeChatMain+0x34674>
0x4e04c	fb0300aa	mov	x27, x0
0x4e050	800640f9	ldr	x0, [x20, #0x8]
0x4e054	e1031baa	mov	x1, x27
0x4e058	624b8452	mov	w2, #0x225b             ; =8795
0x4e05c	429db772	movk	w2, #0xbcea, lsl #16
0x4e060	e3031aaa	mov	x3, x26
0x4e064	89020094	bl	0x4ea88 <_WeChatMain+0x3521c>
0x4e068	c0f3ffb4	cbz	x0, 0x4dee0 <_WeChatMain+0x34674>
0x4e06c	c82640a9	ldp	x8, x9, [x22]
0x4e070	2a0108eb	subs	x10, x9, x8
0x4e074	c0030054	b.eq	0x4e0ec <_WeChatMain+0x34880>
0x4e078	090080d2	mov	x9, #0x0                ; =0
0x4e07c	4bfd4293	asr	x11, x10, #2
0x4e080	7f0500f1	cmp	x11, #0x1
0x4e084	6a859f9a	csinc	x10, x11, xzr, hi
0x4e088	7f4100f1	cmp	x11, #0x10
0x4e08c	03020054	b.lo	0x4e0cc <_WeChatMain+0x34860>
0x4e090	0c0008cb	sub	x12, x0, x8
0x4e094	9ffd00f1	cmp	x12, #0x3f
0x4e098	a9010054	b.ls	0x4e0cc <_WeChatMain+0x34860>
0x4e09c	49ed7c92	and	x9, x10, #0xfffffffffffffff0
0x4e0a0	0c800091	add	x12, x0, #0x20
0x4e0a4	0d810091	add	x13, x8, #0x20
0x4e0a8	ee0309aa	mov	x14, x9
0x4e0ac	a0057fad	ldp	q0, q1, [x13, #-0x20]
0x4e0b0	a20dc2ac	ldp	q2, q3, [x13], #0x40
0x4e0b4	80053fad	stp	q0, q1, [x12, #-0x20]
0x4e0b8	820d82ac	stp	q2, q3, [x12], #0x40
0x4e0bc	ce4100f1	subs	x14, x14, #0x10
0x4e0c0	61ffff54	b.ne	0x4e0ac <_WeChatMain+0x34840>
0x4e0c4	7f0109eb	cmp	x11, x9
0x4e0c8	20010054	b.eq	0x4e0ec <_WeChatMain+0x34880>
0x4e0cc	4a0109cb	sub	x10, x10, x9
0x4e0d0	2bf57ed3	lsl	x11, x9, #2
0x4e0d4	09000b8b	add	x9, x0, x11
0x4e0d8	08010b8b	add	x8, x8, x11
0x4e0dc	0b4540b8	ldr	w11, [x8], #0x4
0x4e0e0	2b4500b8	str	w11, [x9], #0x4
0x4e0e4	4a0500f1	subs	x10, x10, #0x1
0x4e0e8	a1ffff54	b.ne	0x4e0dc <_WeChatMain+0x34870>
0x4e0ec	dbc20199	stlur	w27, [x22, #0x1c]
0x4e0f0	99f6ffb5	cbnz	x25, 0x4dfc0 <_WeChatMain+0x34754>
0x4e0f4	7bffff17	b	0x4dee0 <_WeChatMain+0x34674>
0x4e0f8	000440f9	ldr	x0, [x0, #0x8]
0x4e0fc	42000034	cbz	w2, 0x4e104 <_WeChatMain+0x34898>
0x4e100	4a030014	b	0x4ee28 <_WeChatMain+0x355bc>
0x4e104	63228b52	mov	w3, #0x5913             ; =22803
0x4e108	832cbe72	movk	w3, #0xf164, lsl #16
0x4e10c	04008052	mov	w4, #0x0                ; =0
0x4e110	80020014	b	0x4eb10 <_WeChatMain+0x352a4>
0x4e114	00600091	add	x0, x0, #0x18
0x4e118	70fcff17	b	0x4d2d8 <_WeChatMain+0x33a6c>
0x4e11c	28100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4e120	08811691	add	x8, x8, #0x5a0
0x4e124	00c1bff8	ldapr	x0, [x8]
0x4e128	c0035fd6	ret
0x4e12c	ff0301d1	sub	sp, sp, #0x40
0x4e130	f65701a9	stp	x22, x21, [sp, #0x10]
0x4e134	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4e138	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4e13c	fdc30091	add	x29, sp, #0x30
0x4e140	f30300aa	mov	x19, x0
0x4e144	148840b9	ldr	w20, [x0, #0x88]
0x4e148	f5f301b2	mov	x21, #-0x5555555555555556 ; =-6148914691236517206
0x4e14c	f50700f9	str	x21, [sp, #0x8]
0x4e150	60620291	add	x0, x19, #0x98
0x4e154	61228b52	mov	w1, #0x5913             ; =22803
0x4e158	812cbe72	movk	w1, #0xf164, lsl #16
0x4e15c	d1010094	bl	0x4e8a0 <_WeChatMain+0x35034>
0x4e160	40020034	cbz	w0, 0x4e1a8 <_WeChatMain+0x3493c>
0x4e164	e10300aa	mov	x1, x0
0x4e168	1f00146b	cmp	w0, w20
0x4e16c	20ffff54	b.eq	0x4e150 <_WeChatMain+0x348e4>
0x4e170	604a40f9	ldr	x0, [x19, #0x90]
0x4e174	e8230091	add	x8, sp, #0x8
0x4e178	52feff97	bl	0x4dac0 <_WeChatMain+0x34254>
0x4e17c	e00740f9	ldr	x0, [sp, #0x8]
0x4e180	400100b4	cbz	x0, 0x4e1a8 <_WeChatMain+0x3493c>
0x4e184	ff0700f9	str	xzr, [sp, #0x8]
0x4e188	8b130094	bl	0x52fb4 <_WeChatMain+0x39748>
0x4e18c	e00740f9	ldr	x0, [sp, #0x8]
0x4e190	ff0700f9	str	xzr, [sp, #0x8]
0x4e194	c0fdffb4	cbz	x0, 0x4e14c <_WeChatMain+0x348e0>
0x4e198	080040f9	ldr	x8, [x0]
0x4e19c	080540f9	ldr	x8, [x8, #0x8]
0x4e1a0	00013fd6	blr	x8
0x4e1a4	eaffff17	b	0x4e14c <_WeChatMain+0x348e0>
0x4e1a8	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4e1ac	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4e1b0	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4e1b4	ff030191	add	sp, sp, #0x40
0x4e1b8	c0035fd6	ret
0x4e1bc	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x4e1c0	fa6701a9	stp	x26, x25, [sp, #0x10]
0x4e1c4	f85f02a9	stp	x24, x23, [sp, #0x20]
0x4e1c8	f65703a9	stp	x22, x21, [sp, #0x30]
0x4e1cc	f44f04a9	stp	x20, x19, [sp, #0x40]
0x4e1d0	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x4e1d4	fd430191	add	x29, sp, #0x50
0x4e1d8	f30301aa	mov	x19, x1
0x4e1dc	9c0400f1	subs	x28, x4, #0x1
0x4e1e0	2b180054	b.lt	0x4e4e4 <_WeChatMain+0x34c78>
0x4e1e4	f60302aa	mov	x22, x2
0x4e1e8	f40300aa	mov	x20, x0
0x4e1ec	15e440a9	ldp	x21, x25, [x0, #0x8]
0x4e1f0	280315cb	sub	x8, x25, x21
0x4e1f4	9f0888eb	cmp	x4, x8, asr #2
0x4e1f8	cd020054	b.le	0x4e250 <_WeChatMain+0x349e4>
0x4e1fc	970240f9	ldr	x23, [x20]
0x4e200	a80217cb	sub	x8, x21, x23
0x4e204	8808888b	add	x8, x4, x8, asr #2
0x4e208	09fd7ed3	lsr	x9, x8, #62
0x4e20c	c91700b5	cbnz	x9, 0x4e504 <_WeChatMain+0x34c98>
0x4e210	e9f37eb2	mov	x9, #0x7ffffffffffffffc ; =9223372036854775804
0x4e214	2a0317cb	sub	x10, x25, x23
0x4e218	4bfd4193	asr	x11, x10, #1
0x4e21c	7f0108eb	cmp	x11, x8
0x4e220	6881889a	csel	x8, x11, x8, hi
0x4e224	5f0109eb	cmp	x10, x9
0x4e228	0900f892	mov	x9, #0x3fffffffffffffff ; =4611686018427387903
0x4e22c	1b31899a	csel	x27, x8, x9, lo
0x4e230	9b0500b4	cbz	x27, 0x4e2e0 <_WeChatMain+0x34a74>
0x4e234	68ff7ed3	lsr	x8, x27, #62
0x4e238	a81600b5	cbnz	x8, 0x4e50c <_WeChatMain+0x34ca0>
0x4e23c	f80304aa	mov	x24, x4
0x4e240	60f77ed3	lsl	x0, x27, #2
0x4e244	7bc7c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4e248	e40318aa	mov	x4, x24
0x4e24c	26000014	b	0x4e2e4 <_WeChatMain+0x34a78>
0x4e250	a80213cb	sub	x8, x21, x19
0x4e254	19fd4293	asr	x25, x8, #2
0x4e258	3f0304eb	cmp	x25, x4
0x4e25c	ea010054	b.ge	0x4e298 <_WeChatMain+0x34a2c>
0x4e260	d702088b	add	x23, x22, x8
0x4e264	780017eb	subs	x24, x3, x23
0x4e268	e0000054	b.eq	0x4e284 <_WeChatMain+0x34a18>
0x4e26c	e00315aa	mov	x0, x21
0x4e270	e10317aa	mov	x1, x23
0x4e274	e20318aa	mov	x2, x24
0x4e278	fa0304aa	mov	x26, x4
0x4e27c	06cbc395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4e280	e4031aaa	mov	x4, x26
0x4e284	a802188b	add	x8, x21, x24
0x4e288	880600f9	str	x8, [x20, #0x8]
0x4e28c	3f0700f1	cmp	x25, #0x1
0x4e290	8a000054	b.ge	0x4e2a0 <_WeChatMain+0x34a34>
0x4e294	94000014	b	0x4e4e4 <_WeChatMain+0x34c78>
0x4e298	d70a048b	add	x23, x22, x4, lsl #2
0x4e29c	e80315aa	mov	x8, x21
0x4e2a0	8cf47ed3	lsl	x12, x4, #2
0x4e2a4	69020c8b	add	x9, x19, x12
0x4e2a8	0b010ccb	sub	x11, x8, x12
0x4e2ac	7f0115eb	cmp	x11, x21
0x4e2b0	ea0308aa	mov	x10, x8
0x4e2b4	02100054	b.hs	0x4e4b4 <_WeChatMain+0x34c48>
0x4e2b8	6a110091	add	x10, x11, #0x4
0x4e2bc	bf020aeb	cmp	x21, x10
0x4e2c0	aa828a9a	csel	x10, x21, x10, hi
0x4e2c4	ed0328aa	mvn	x13, x8
0x4e2c8	8c010d8b	add	x12, x12, x13
0x4e2cc	4c010c8b	add	x12, x10, x12
0x4e2d0	9fed00f1	cmp	x12, #0x3b
0x4e2d4	a80b0054	b.hi	0x4e448 <_WeChatMain+0x34bdc>
0x4e2d8	ea0308aa	mov	x10, x8
0x4e2dc	72000014	b	0x4e4a4 <_WeChatMain+0x34c38>
0x4e2e0	000080d2	mov	x0, #0x0                ; =0
0x4e2e4	680217cb	sub	x8, x19, x23
0x4e2e8	09fd4293	asr	x9, x8, #2
0x4e2ec	1a08098b	add	x26, x0, x9, lsl #2
0x4e2f0	580b048b	add	x24, x26, x4, lsl #2
0x4e2f4	89f74092	and	x9, x28, #0x3fffffffffffffff
0x4e2f8	3f3d00f1	cmp	x9, #0xf
0x4e2fc	a3000054	b.lo	0x4e310 <_WeChatMain+0x34aa4>
0x4e300	0a01008b	add	x10, x8, x0
0x4e304	4a0116cb	sub	x10, x10, x22
0x4e308	5f0101f1	cmp	x10, #0x40
0x4e30c	c2070054	b.hs	0x4e404 <_WeChatMain+0x34b98>
0x4e310	e9031aaa	mov	x9, x26
0x4e314	ea0316aa	mov	x10, x22
0x4e318	4b4540b8	ldr	w11, [x10], #0x4
0x4e31c	2b4500b8	str	w11, [x9], #0x4
0x4e320	3f0118eb	cmp	x9, x24
0x4e324	a1ffff54	b.ne	0x4e318 <_WeChatMain+0x34aac>
0x4e328	f6031aaa	mov	x22, x26
0x4e32c	ff0213eb	cmp	x23, x19
0x4e330	60040054	b.eq	0x4e3bc <_WeChatMain+0x34b50>
0x4e334	0a1100d1	sub	x10, x8, #0x4
0x4e338	e90313aa	mov	x9, x19
0x4e33c	f6031aaa	mov	x22, x26
0x4e340	5ff100f1	cmp	x10, #0x3c
0x4e344	43030054	b.lo	0x4e3ac <_WeChatMain+0x34b40>
0x4e348	0801008b	add	x8, x8, x0
0x4e34c	680208cb	sub	x8, x19, x8
0x4e350	e90313aa	mov	x9, x19
0x4e354	f6031aaa	mov	x22, x26
0x4e358	1f0101f1	cmp	x8, #0x40
0x4e35c	83020054	b.lo	0x4e3ac <_WeChatMain+0x34b40>
0x4e360	48fd42d3	lsr	x8, x10, #2
0x4e364	08050091	add	x8, x8, #0x1
0x4e368	0ae97c92	and	x10, x8, #0x7ffffffffffffff0
0x4e36c	4bf57ed3	lsl	x11, x10, #2
0x4e370	69020bcb	sub	x9, x19, x11
0x4e374	56030bcb	sub	x22, x26, x11
0x4e378	6b8200d1	sub	x11, x19, #0x20
0x4e37c	4c8300d1	sub	x12, x26, #0x20
0x4e380	ed030aaa	mov	x13, x10
0x4e384	610140ad	ldp	q1, q0, [x11]
0x4e388	63097fad	ldp	q3, q2, [x11, #-0x20]
0x4e38c	810100ad	stp	q1, q0, [x12]
0x4e390	83093fad	stp	q3, q2, [x12, #-0x20]
0x4e394	6b0101d1	sub	x11, x11, #0x40
0x4e398	8c0101d1	sub	x12, x12, #0x40
0x4e39c	ad4100d1	sub	x13, x13, #0x10
0x4e3a0	2dffffb5	cbnz	x13, 0x4e384 <_WeChatMain+0x34b18>
0x4e3a4	1f010aeb	cmp	x8, x10
0x4e3a8	a0000054	b.eq	0x4e3bc <_WeChatMain+0x34b50>
0x4e3ac	28cd5fb8	ldr	w8, [x9, #-0x4]!
0x4e3b0	c8ce1fb8	str	w8, [x22, #-0x4]!
0x4e3b4	3f0117eb	cmp	x9, x23
0x4e3b8	a1ffff54	b.ne	0x4e3ac <_WeChatMain+0x34b40>
0x4e3bc	1b081b8b	add	x27, x0, x27, lsl #2
0x4e3c0	b50213eb	subs	x21, x21, x19
0x4e3c4	e0000054	b.eq	0x4e3e0 <_WeChatMain+0x34b74>
0x4e3c8	e00318aa	mov	x0, x24
0x4e3cc	e10313aa	mov	x1, x19
0x4e3d0	e20315aa	mov	x2, x21
0x4e3d4	b0cac395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4e3d8	970240f9	ldr	x23, [x20]
0x4e3dc	990a40f9	ldr	x25, [x20, #0x10]
0x4e3e0	0803158b	add	x8, x24, x21
0x4e3e4	962200a9	stp	x22, x8, [x20]
0x4e3e8	9b0a00f9	str	x27, [x20, #0x10]
0x4e3ec	970000b4	cbz	x23, 0x4e3fc <_WeChatMain+0x34b90>
0x4e3f0	210317cb	sub	x1, x25, x23
0x4e3f4	e00317aa	mov	x0, x23
0x4e3f8	05c7c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4e3fc	f3031aaa	mov	x19, x26
0x4e400	39000014	b	0x4e4e4 <_WeChatMain+0x34c78>
0x4e404	2b050091	add	x11, x9, #0x1
0x4e408	6ce97c92	and	x12, x11, #0x7ffffffffffffff0
0x4e40c	8af57ed3	lsl	x10, x12, #2
0x4e410	49030a8b	add	x9, x26, x10
0x4e414	ca020a8b	add	x10, x22, x10
0x4e418	4d830091	add	x13, x26, #0x20
0x4e41c	ce820091	add	x14, x22, #0x20
0x4e420	ef030caa	mov	x15, x12
0x4e424	c0057fad	ldp	q0, q1, [x14, #-0x20]
0x4e428	c20dc2ac	ldp	q2, q3, [x14], #0x40
0x4e42c	a0053fad	stp	q0, q1, [x13, #-0x20]
0x4e430	a20d82ac	stp	q2, q3, [x13], #0x40
0x4e434	ef4100f1	subs	x15, x15, #0x10
0x4e438	61ffff54	b.ne	0x4e424 <_WeChatMain+0x34bb8>
0x4e43c	7f010ceb	cmp	x11, x12
0x4e440	c1f6ff54	b.ne	0x4e318 <_WeChatMain+0x34aac>
0x4e444	b9ffff17	b	0x4e328 <_WeChatMain+0x34abc>
0x4e448	0a09048b	add	x10, x8, x4, lsl #2
0x4e44c	4d0108cb	sub	x13, x10, x8
0x4e450	ea0308aa	mov	x10, x8
0x4e454	bf0101f1	cmp	x13, #0x40
0x4e458	63020054	b.lo	0x4e4a4 <_WeChatMain+0x34c38>
0x4e45c	8afd42d3	lsr	x10, x12, #2
0x4e460	4c050091	add	x12, x10, #0x1
0x4e464	8de97c92	and	x13, x12, #0x7ffffffffffffff0
0x4e468	aaf57ed3	lsl	x10, x13, #2
0x4e46c	6e010a8b	add	x14, x11, x10
0x4e470	0a010a8b	add	x10, x8, x10
0x4e474	6b810091	add	x11, x11, #0x20
0x4e478	0f810091	add	x15, x8, #0x20
0x4e47c	f0030daa	mov	x16, x13
0x4e480	60057fad	ldp	q0, q1, [x11, #-0x20]
0x4e484	620dc2ac	ldp	q2, q3, [x11], #0x40
0x4e488	e0053fad	stp	q0, q1, [x15, #-0x20]
0x4e48c	e20d82ac	stp	q2, q3, [x15], #0x40
0x4e490	104200f1	subs	x16, x16, #0x10
0x4e494	61ffff54	b.ne	0x4e480 <_WeChatMain+0x34c14>
0x4e498	eb030eaa	mov	x11, x14
0x4e49c	9f010deb	cmp	x12, x13
0x4e4a0	a0000054	b.eq	0x4e4b4 <_WeChatMain+0x34c48>
0x4e4a4	6c4540b8	ldr	w12, [x11], #0x4
0x4e4a8	4c4500b8	str	w12, [x10], #0x4
0x4e4ac	7f0115eb	cmp	x11, x21
0x4e4b0	a3ffff54	b.lo	0x4e4a4 <_WeChatMain+0x34c38>
0x4e4b4	8a0600f9	str	x10, [x20, #0x8]
0x4e4b8	1f0109eb	cmp	x8, x9
0x4e4bc	a0000054	b.eq	0x4e4d0 <_WeChatMain+0x34c64>
0x4e4c0	020109cb	sub	x2, x8, x9
0x4e4c4	000102cb	sub	x0, x8, x2
0x4e4c8	e10313aa	mov	x1, x19
0x4e4cc	72cac395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4e4d0	e20216eb	subs	x2, x23, x22
0x4e4d4	80000054	b.eq	0x4e4e4 <_WeChatMain+0x34c78>
0x4e4d8	e00313aa	mov	x0, x19
0x4e4dc	e10316aa	mov	x1, x22
0x4e4e0	6dcac395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x4e4e4	e00313aa	mov	x0, x19
0x4e4e8	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x4e4ec	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x4e4f0	f65743a9	ldp	x22, x21, [sp, #0x30]
0x4e4f4	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x4e4f8	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x4e4fc	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x4e500	c0035fd6	ret
0x4e504	e00314aa	mov	x0, x20
0x4e508	8fceff97	bl	0x41f44 <_WeChatMain+0x286d8>
0x4e50c	9055ff97	bl	0x23b4c <_WeChatMain+0xa2e0>
0x4e510	08068052	mov	w8, #0x30               ; =48
0x4e514	080800b9	str	w8, [x0, #0x8]
0x4e518	1f0c00b9	str	wzr, [x0, #0xc]
0x4e51c	c0035fd6	ret
0x4e520	080840b9	ldr	w8, [x0, #0x8]
0x4e524	1fc10071	cmp	w8, #0x30
0x4e528	e003881a	csel	w0, wzr, w8, eq
0x4e52c	c0035fd6	ret
0x4e530	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4e534	fd030091	mov	x29, sp
0x4e538	2b4d9252	mov	w11, #0x9269            ; =37481
0x4e53c	2b0fb972	movk	w11, #0xc879, lsl #16
0x4e540	0ac04099	ldapur	w10, [x0, #0xc]
0x4e544	0c804099	ldapur	w12, [x0, #0x8]
0x4e548	090040f9	ldr	x9, [x0]
0x4e54c	9fc10071	cmp	w12, #0x30
0x4e550	81000054	b.ne	0x4e560 <_WeChatMain+0x34cf4>
0x4e554	280540f9	ldr	x8, [x9, #0x8]
0x4e558	08c10091	add	x8, x8, #0x30
0x4e55c	17000014	b	0x4e5b8 <_WeChatMain+0x34d4c>
0x4e560	08008052	mov	w8, #0x0                ; =0
0x4e564	9f010171	cmp	w12, #0x40
0x4e568	c3080054	b.lo	0x4e680 <_WeChatMain+0x34e14>
0x4e56c	ee030c2a	mov	w14, w12
0x4e570	cd094092	and	x13, x14, #0x7
0x4e574	6d0800b5	cbnz	x13, 0x4e680 <_WeChatMain+0x34e14>
0x4e578	c8410091	add	x8, x14, #0x10
0x4e57c	2d1540b9	ldr	w13, [x9, #0x14]
0x4e580	1f010deb	cmp	x8, x13
0x4e584	c8070054	b.hi	0x4e67c <_WeChatMain+0x34e10>
0x4e588	280540f9	ldr	x8, [x9, #0x8]
0x4e58c	08010e8b	add	x8, x8, x14
0x4e590	090540b9	ldr	w9, [x8, #0x4]
0x4e594	3f010b6b	cmp	w9, w11
0x4e598	21070054	b.ne	0x4e67c <_WeChatMain+0x34e10>
0x4e59c	090140b9	ldr	w9, [x8]
0x4e5a0	3f410071	cmp	w9, #0x10
0x4e5a4	c3060054	b.lo	0x4e67c <_WeChatMain+0x34e10>
0x4e5a8	090140b9	ldr	w9, [x8]
0x4e5ac	29010c0b	add	w9, w9, w12
0x4e5b0	3f010d6b	cmp	w9, w13
0x4e5b4	48060054	b.hi	0x4e67c <_WeChatMain+0x34e10>
0x4e5b8	480600b4	cbz	x8, 0x4e680 <_WeChatMain+0x34e14>
0x4e5bc	08c14099	ldapur	w8, [x8, #0xc]
0x4e5c0	1fc10071	cmp	w8, #0x30
0x4e5c4	c0050054	b.eq	0x4e67c <_WeChatMain+0x34e10>
0x4e5c8	090040f9	ldr	x9, [x0]
0x4e5cc	0d094092	and	x13, x8, #0x7
0x4e5d0	1f010171	cmp	w8, #0x40
0x4e5d4	a02940fa	ccmp	x13, #0x0, #0x0, hs
0x4e5d8	e1040054	b.ne	0x4e674 <_WeChatMain+0x34e08>
0x4e5dc	0d410091	add	x13, x8, #0x10
0x4e5e0	2e1540b9	ldr	w14, [x9, #0x14]
0x4e5e4	bf010eeb	cmp	x13, x14
0x4e5e8	68040054	b.hi	0x4e674 <_WeChatMain+0x34e08>
0x4e5ec	2d0540f9	ldr	x13, [x9, #0x8]
0x4e5f0	ad01088b	add	x13, x13, x8
0x4e5f4	af0540b9	ldr	w15, [x13, #0x4]
0x4e5f8	ff010b6b	cmp	w15, w11
0x4e5fc	c1030054	b.ne	0x4e674 <_WeChatMain+0x34e08>
0x4e600	af0140b9	ldr	w15, [x13]
0x4e604	ff410071	cmp	w15, #0x10
0x4e608	63030054	b.lo	0x4e674 <_WeChatMain+0x34e08>
0x4e60c	af0140b9	ldr	w15, [x13]
0x4e610	ef01080b	add	w15, w15, w8
0x4e614	bf0100f1	cmp	x13, #0x0
0x4e618	e2114e7a	ccmp	w15, w14, #0x2, ne
0x4e61c	c8020054	b.hi	0x4e674 <_WeChatMain+0x34e08>
0x4e620	0e200091	add	x14, x0, #0x8
0x4e624	e9030caa	mov	x9, x12
0x4e628	c8fde988	casal	w9, w8, [x14]
0x4e62c	3f010c6b	cmp	w9, w12
0x4e630	60000054	b.eq	0x4e63c <_WeChatMain+0x34dd0>
0x4e634	ec0309aa	mov	x12, x9
0x4e638	c4ffff17	b	0x4e548 <_WeChatMain+0x34cdc>
0x4e63c	a90940b9	ldr	w9, [x13, #0x8]
0x4e640	290000b9	str	w9, [x1]
0x4e644	090040f9	ldr	x9, [x0]
0x4e648	2b0540f9	ldr	x11, [x9, #0x8]
0x4e64c	6b2940b9	ldr	w11, [x11, #0x28]
0x4e650	2c1540b9	ldr	w12, [x9, #0x14]
0x4e654	9f010b6b	cmp	w12, w11
0x4e658	8b318b1a	csel	w11, w12, w11, lo
0x4e65c	6c559552	mov	w12, #0xaaab            ; =43691
0x4e660	4c55b572	movk	w12, #0xaaaa, lsl #16
0x4e664	6b7dac9b	umull	x11, w11, w12
0x4e668	6bfd64d3	lsr	x11, x11, #36
0x4e66c	5f010b6b	cmp	w10, w11
0x4e670	e9000054	b.ls	0x4e68c <_WeChatMain+0x34e20>
0x4e674	e00309aa	mov	x0, x9
0x4e678	09000094	bl	0x4e69c <_WeChatMain+0x34e30>
0x4e67c	08008052	mov	w8, #0x0                ; =0
0x4e680	e00308aa	mov	x0, x8
0x4e684	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4e688	c0035fd6	ret
0x4e68c	09300091	add	x9, x0, #0xc
0x4e690	2a008052	mov	w10, #0x1               ; =1
0x4e694	29016ab8	ldaddl	w10, w9, [x9]
0x4e698	faffff17	b	0x4e680 <_WeChatMain+0x34e14>
0x4e69c	ff8305d1	sub	sp, sp, #0x160
0x4e6a0	f65713a9	stp	x22, x21, [sp, #0x130]
0x4e6a4	f44f14a9	stp	x20, x19, [sp, #0x140]
0x4e6a8	fd7b15a9	stp	x29, x30, [sp, #0x150]
0x4e6ac	fd430591	add	x29, sp, #0x150
0x4e6b0	f30300aa	mov	x19, x0
0x4e6b4	08a44039	ldrb	w8, [x0, #0x29]
0x4e6b8	680c0037	tbnz	w8, #0x0, 0x4e844 <_WeChatMain+0x34fd8>
0x4e6bc	680640f9	ldr	x8, [x19, #0x8]
0x4e6c0	082540b9	ldr	w8, [x8, #0x24]
0x4e6c4	080c0037	tbnz	w8, #0x0, 0x4e844 <_WeChatMain+0x34fd8>
0x4e6c8	40008052	mov	w0, #0x2                ; =2
0x4e6cc	39b6ff97	bl	0x3bfb0 <_WeChatMain+0x22744>
0x4e6d0	e00a0034	cbz	w0, 0x4e82c <_WeChatMain+0x34fc0>
0x4e6d4	28100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4e6d8	09915839	ldrb	w9, [x8, #0x624]
0x4e6dc	49030037	tbnz	w9, #0x0, 0x4e744 <_WeChatMain+0x34ed8>
0x4e6e0	090080d2	mov	x9, #0x0                ; =0
0x4e6e4	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x4e6e8	aa9999f2	movk	x10, #0xcccd
0x4e6ec	6b028092	mov	x11, #-0x14             ; =-20
0x4e6f0	ec210490	adrp	x12, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e6f4	8c410791	add	x12, x12, #0x1d0
0x4e6f8	4085040f	movi.4h	v0, #0x8a
0x4e6fc	2d100590	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4e700	ada11691	add	x13, x13, #0x5a8
0x4e704	2e7dca9b	umulh	x14, x9, x10
0x4e708	cefd44d3	lsr	x14, x14, #4
0x4e70c	ce7d0b9b	mul	x14, x14, x11
0x4e710	8f01098b	add	x15, x12, x9
0x4e714	e11540bd	ldr	s1, [x15, #0x14]
0x4e718	0110212e	uaddw.8h	v1, v0, v1
0x4e71c	e2696ebc	ldr	s2, [x15, x14]
0x4e720	42a4082f	ushll.8h	v2, v2, #0x0
0x4e724	211c222e	eor.8b	v1, v1, v2
0x4e728	2118000e	uzp1.8b	v1, v1, v0
0x4e72c	a16929bc	str	s1, [x13, x9]
0x4e730	29110091	add	x9, x9, #0x4
0x4e734	3ff101f1	cmp	x9, #0x7c
0x4e738	61feff54	b.ne	0x4e704 <_WeChatMain+0x34e98>
0x4e73c	29008052	mov	w9, #0x1                ; =1
0x4e740	09911839	strb	w9, [x8, #0x624]
0x4e744	21100590	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4e748	21a01691	add	x1, x1, #0x5a8
0x4e74c	f5030091	mov	x21, sp
0x4e750	e0030091	mov	x0, sp
0x4e754	e2688052	mov	w2, #0x347              ; =839
0x4e758	43008052	mov	w3, #0x2                ; =2
0x4e75c	35b6ff97	bl	0x3c030 <_WeChatMain+0x227c4>
0x4e760	28100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4e764	09695939	ldrb	w9, [x8, #0x65a]
0x4e768	e9040037	tbnz	w9, #0x0, 0x4e804 <_WeChatMain+0x34f98>
0x4e76c	e9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e770	209140fd	ldr	d0, [x9, #0x120]
0x4e774	e9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e778	217540fd	ldr	d1, [x9, #0xe8]
0x4e77c	20040c6e	mov.s	v0[1], v1[0]
0x4e780	e9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e784	219540fd	ldr	d1, [x9, #0x128]
0x4e788	2004146e	mov.s	v0[2], v1[0]
0x4e78c	e9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e790	219940fd	ldr	d1, [x9, #0x130]
0x4e794	20041c6e	mov.s	v0[3], v1[0]
0x4e798	892104d0	adrp	x9, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x4e79c	21ad44fd	ldr	d1, [x9, #0x958]
0x4e7a0	e9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e7a4	229d40fd	ldr	d2, [x9, #0x138]
0x4e7a8	41040c6e	mov.s	v1[1], v2[0]
0x4e7ac	c92104b0	adrp	x9, 0x8487000 <_wxam_enc_uninit_10+0x8487000>
0x4e7b0	22c946fd	ldr	d2, [x9, #0xd90]
0x4e7b4	4104146e	mov.s	v1[2], v2[0]
0x4e7b8	e9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e7bc	22a140fd	ldr	d2, [x9, #0x140]
0x4e7c0	41041c6e	mov.s	v1[3], v2[0]
0x4e7c4	29100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4e7c8	29b11891	add	x9, x9, #0x62c
0x4e7cc	200500ad	stp	q0, q1, [x9]
0x4e7d0	aa2104b0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4e7d4	403941fd	ldr	d0, [x10, #0x270]
0x4e7d8	ea210490	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x4e7dc	41a540fd	ldr	d1, [x10, #0x148]
0x4e7e0	20040c6e	mov.s	v0[1], v1[0]
0x4e7e4	201100fd	str	d0, [x9, #0x20]
0x4e7e8	aa2104b0	adrp	x10, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x4e7ec	401141fd	ldr	d0, [x10, #0x220]
0x4e7f0	202900bd	str	s0, [x9, #0x28]
0x4e7f4	ca058052	mov	w10, #0x2e              ; =46
0x4e7f8	2a590079	strh	w10, [x9, #0x2c]
0x4e7fc	29008052	mov	w9, #0x1                ; =1
0x4e800	09691939	strb	w9, [x8, #0x65a]
0x4e804	34100590	adrp	x20, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x4e808	94b21891	add	x20, x20, #0x62c
0x4e80c	e00314aa	mov	x0, x20
0x4e810	7accc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x4e814	e20300aa	mov	x2, x0
0x4e818	a0420091	add	x0, x21, #0x10
0x4e81c	e10314aa	mov	x1, x20
0x4e820	6b30ff97	bl	0x1a9cc <_WeChatMain+0x1160>
0x4e824	e0030091	mov	x0, sp
0x4e828	36bbff97	bl	0x3d500 <_WeChatMain+0x23c94>
0x4e82c	602240f9	ldr	x0, [x19, #0x40]
0x4e830	a00000b4	cbz	x0, 0x4e844 <_WeChatMain+0x34fd8>
0x4e834	080040f9	ldr	x8, [x0]
0x4e838	081940f9	ldr	x8, [x8, #0x30]
0x4e83c	21008052	mov	w1, #0x1                ; =1
0x4e840	00013fd6	blr	x8
0x4e844	28008052	mov	w8, #0x1                ; =1
0x4e848	68a60039	strb	w8, [x19, #0x29]
0x4e84c	68a24039	ldrb	w8, [x19, #0x28]
0x4e850	e8010037	tbnz	w8, #0x0, 0x4e88c <_WeChatMain+0x35020>
0x4e854	690640f9	ldr	x9, [x19, #0x8]
0x4e858	28910091	add	x8, x9, #0x24
0x4e85c	2a2540b9	ldr	w10, [x9, #0x24]
0x4e860	4b010032	orr	w11, w10, #0x1
0x4e864	e9030aaa	mov	x9, x10
0x4e868	0b7da988	cas	w9, w11, [x8]
0x4e86c	3f010a6b	cmp	w9, w10
0x4e870	e0000054	b.eq	0x4e88c <_WeChatMain+0x35020>
0x4e874	ea0309aa	mov	x10, x9
0x4e878	2b010032	orr	w11, w9, #0x1
0x4e87c	0b7daa88	cas	w10, w11, [x8]
0x4e880	5f01096b	cmp	w10, w9
0x4e884	e9030aaa	mov	x9, x10
0x4e888	81ffff54	b.ne	0x4e878 <_WeChatMain+0x3500c>
0x4e88c	fd7b55a9	ldp	x29, x30, [sp, #0x150]
0x4e890	f44f54a9	ldp	x20, x19, [sp, #0x140]
0x4e894	f65753a9	ldp	x22, x21, [sp, #0x130]
0x4e898	ff830591	add	sp, sp, #0x160
0x4e89c	c0035fd6	ret
0x4e8a0	ffc300d1	sub	sp, sp, #0x30
0x4e8a4	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4e8a8	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4e8ac	fd830091	add	x29, sp, #0x20
0x4e8b0	f30301aa	mov	x19, x1
0x4e8b4	f40300aa	mov	x20, x0
0x4e8b8	e8f30132	mov	w8, #-0x55555556        ; =-1431655766
0x4e8bc	e80f00b9	str	w8, [sp, #0xc]
0x4e8c0	e1330091	add	x1, sp, #0xc
0x4e8c4	e00314aa	mov	x0, x20
0x4e8c8	1affff97	bl	0x4e530 <_WeChatMain+0x34cc4>
0x4e8cc	80000034	cbz	w0, 0x4e8dc <_WeChatMain+0x35070>
0x4e8d0	e80f40b9	ldr	w8, [sp, #0xc]
0x4e8d4	1f01136b	cmp	w8, w19
0x4e8d8	41ffff54	b.ne	0x4e8c0 <_WeChatMain+0x35054>
0x4e8dc	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4e8e0	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4e8e4	ffc30091	add	sp, sp, #0x30
0x4e8e8	c0035fd6	ret
0x4e8ec	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4e8f0	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4e8f4	fd430091	add	x29, sp, #0x10
0x4e8f8	f30301aa	mov	x19, x1
0x4e8fc	f40300aa	mov	x20, x0
0x4e900	c2000094	bl	0x4ec08 <_WeChatMain+0x3539c>
0x4e904	e80300aa	mov	x8, x0
0x4e908	801a40f9	ldr	x0, [x20, #0x30]
0x4e90c	88000034	cbz	w8, 0x4e91c <_WeChatMain+0x350b0>
0x4e910	600100b4	cbz	x0, 0x4e93c <_WeChatMain+0x350d0>
0x4e914	f40308aa	mov	x20, x8
0x4e918	04000014	b	0x4e928 <_WeChatMain+0x350bc>
0x4e91c	000100b4	cbz	x0, 0x4e93c <_WeChatMain+0x350d0>
0x4e920	f40308aa	mov	x20, x8
0x4e924	13008052	mov	w19, #0x0               ; =0
0x4e928	080040f9	ldr	x8, [x0]
0x4e92c	081940f9	ldr	x8, [x8, #0x30]
0x4e930	e10313aa	mov	x1, x19
0x4e934	00013fd6	blr	x8
0x4e938	e80314aa	mov	x8, x20
0x4e93c	e00308aa	mov	x0, x8
0x4e940	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4e944	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4e948	c0035fd6	ret
0x4e94c	080080d2	mov	x8, #0x0                ; =0
0x4e950	3f000171	cmp	w1, #0x40
0x4e954	c3040054	b.lo	0x4e9ec <_WeChatMain+0x35180>
0x4e958	ea03012a	mov	w10, w1
0x4e95c	49094092	and	x9, x10, #0x7
0x4e960	690400b5	cbnz	x9, 0x4e9ec <_WeChatMain+0x35180>
0x4e964	48410091	add	x8, x10, #0x10
0x4e968	091440b9	ldr	w9, [x0, #0x14]
0x4e96c	1f0109eb	cmp	x8, x9
0x4e970	68010054	b.hi	0x4e99c <_WeChatMain+0x35130>
0x4e974	080440f9	ldr	x8, [x0, #0x8]
0x4e978	0a010a8b	add	x10, x8, x10
0x4e97c	480540b9	ldr	w8, [x10, #0x4]
0x4e980	2b4d9252	mov	w11, #0x9269            ; =37481
0x4e984	2b0fb972	movk	w11, #0xc879, lsl #16
0x4e988	1f010b6b	cmp	w8, w11
0x4e98c	81000054	b.ne	0x4e99c <_WeChatMain+0x35130>
0x4e990	480140b9	ldr	w8, [x10]
0x4e994	1f410071	cmp	w8, #0x10
0x4e998	62000054	b.hs	0x4e9a4 <_WeChatMain+0x35138>
0x4e99c	000080d2	mov	x0, #0x0                ; =0
0x4e9a0	c0035fd6	ret
0x4e9a4	080080d2	mov	x8, #0x0                ; =0
0x4e9a8	4b0140b9	ldr	w11, [x10]
0x4e9ac	0a0200b4	cbz	x10, 0x4e9ec <_WeChatMain+0x35180>
0x4e9b0	6b01010b	add	w11, w11, w1
0x4e9b4	7f01096b	cmp	w11, w9
0x4e9b8	a8010054	b.hi	0x4e9ec <_WeChatMain+0x35180>
0x4e9bc	480140b9	ldr	w8, [x10]
0x4e9c0	0a01010b	add	w10, w8, w1
0x4e9c4	1f450071	cmp	w8, #0x11
0x4e9c8	4221497a	ccmp	w10, w9, #0x2, hs
0x4e9cc	e9000054	b.ls	0x4e9e8 <_WeChatMain+0x3517c>
0x4e9d0	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4e9d4	fd030091	mov	x29, sp
0x4e9d8	31ffff97	bl	0x4e69c <_WeChatMain+0x34e30>
0x4e9dc	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4e9e0	000080d2	mov	x0, #0x0                ; =0
0x4e9e4	c0035fd6	ret
0x4e9e8	084100d1	sub	x8, x8, #0x10
0x4e9ec	e00308aa	mov	x0, x8
0x4e9f0	c0035fd6	ret
0x4e9f4	0a0440f9	ldr	x10, [x0, #0x8]
0x4e9f8	5f0101eb	cmp	x10, x1
0x4e9fc	28040054	b.hi	0x4ea80 <_WeChatMain+0x35214>
0x4ea00	28000acb	sub	x8, x1, x10
0x4ea04	091440b9	ldr	w9, [x0, #0x14]
0x4ea08	1f4100f1	cmp	x8, #0x10
0x4ea0c	022149fa	ccmp	x8, x9, #0x2, hs
0x4ea10	82030054	b.hs	0x4ea80 <_WeChatMain+0x35214>
0x4ea14	08410051	sub	w8, w8, #0x10
0x4ea18	0b094092	and	x11, x8, #0x7
0x4ea1c	0c450091	add	x12, x8, #0x11
0x4ea20	1f010171	cmp	w8, #0x40
0x4ea24	602940fa	ccmp	x11, #0x0, #0x0, hs
0x4ea28	820149fa	ccmp	x12, x9, #0x2, eq
0x4ea2c	a8020054	b.hi	0x4ea80 <_WeChatMain+0x35214>
0x4ea30	4a01088b	add	x10, x10, x8
0x4ea34	4b0540b9	ldr	w11, [x10, #0x4]
0x4ea38	2c4d9252	mov	w12, #0x9269            ; =37481
0x4ea3c	2c0fb972	movk	w12, #0xc879, lsl #16
0x4ea40	7f010c6b	cmp	w11, w12
0x4ea44	e1010054	b.ne	0x4ea80 <_WeChatMain+0x35214>
0x4ea48	4b0140b9	ldr	w11, [x10]
0x4ea4c	7f450071	cmp	w11, #0x11
0x4ea50	83010054	b.lo	0x4ea80 <_WeChatMain+0x35214>
0x4ea54	4b0140b9	ldr	w11, [x10]
0x4ea58	6b01080b	add	w11, w11, w8
0x4ea5c	7f01096b	cmp	w11, w9
0x4ea60	08010054	b.hi	0x4ea80 <_WeChatMain+0x35214>
0x4ea64	82000034	cbz	w2, 0x4ea74 <_WeChatMain+0x35208>
0x4ea68	490940b9	ldr	w9, [x10, #0x8]
0x4ea6c	3f01026b	cmp	w9, w2
0x4ea70	81000054	b.ne	0x4ea80 <_WeChatMain+0x35214>
0x4ea74	5f0100f1	cmp	x10, #0x0
0x4ea78	e003881a	csel	w0, wzr, w8, eq
0x4ea7c	c0035fd6	ret
0x4ea80	00008052	mov	w0, #0x0                ; =0
0x4ea84	c0035fd6	ret
0x4ea88	080080d2	mov	x8, #0x0                ; =0
0x4ea8c	3f000171	cmp	w1, #0x40
0x4ea90	83030054	b.lo	0x4eb00 <_WeChatMain+0x35294>
0x4ea94	eb03012a	mov	w11, w1
0x4ea98	69094092	and	x9, x11, #0x7
0x4ea9c	290300b5	cbnz	x9, 0x4eb00 <_WeChatMain+0x35294>
0x4eaa0	6a400091	add	x10, x3, #0x10
0x4eaa4	091440b9	ldr	w9, [x0, #0x14]
0x4eaa8	48010b8b	add	x8, x10, x11
0x4eaac	1f0109eb	cmp	x8, x9
0x4eab0	68020054	b.hi	0x4eafc <_WeChatMain+0x35290>
0x4eab4	080440f9	ldr	x8, [x0, #0x8]
0x4eab8	08010b8b	add	x8, x8, x11
0x4eabc	0b0540b9	ldr	w11, [x8, #0x4]
0x4eac0	2c4d9252	mov	w12, #0x9269            ; =37481
0x4eac4	2c0fb972	movk	w12, #0xc879, lsl #16
0x4eac8	7f010c6b	cmp	w11, w12
0x4eacc	81010054	b.ne	0x4eafc <_WeChatMain+0x35290>
0x4ead0	0b0140b9	ldr	w11, [x8]
0x4ead4	5f010beb	cmp	x10, x11
0x4ead8	28010054	b.hi	0x4eafc <_WeChatMain+0x35290>
0x4eadc	0a0140b9	ldr	w10, [x8]
0x4eae0	4a01010b	add	w10, w10, w1
0x4eae4	5f01096b	cmp	w10, w9
0x4eae8	a8000054	b.hi	0x4eafc <_WeChatMain+0x35290>
0x4eaec	a2000034	cbz	w2, 0x4eb00 <_WeChatMain+0x35294>
0x4eaf0	090940b9	ldr	w9, [x8, #0x8]
0x4eaf4	3f01026b	cmp	w9, w2
0x4eaf8	40000054	b.eq	0x4eb00 <_WeChatMain+0x35294>
0x4eafc	080080d2	mov	x8, #0x0                ; =0
0x4eb00	09410091	add	x9, x8, #0x10
0x4eb04	1f0100f1	cmp	x8, #0x0
0x4eb08	e003899a	csel	x0, xzr, x9, eq
0x4eb0c	c0035fd6	ret
0x4eb10	e80300aa	mov	x8, x0
0x4eb14	00008052	mov	w0, #0x0                ; =0
0x4eb18	3f000171	cmp	w1, #0x40
0x4eb1c	63020054	b.lo	0x4eb68 <_WeChatMain+0x352fc>
0x4eb20	ea03012a	mov	w10, w1
0x4eb24	49094092	and	x9, x10, #0x7
0x4eb28	090200b5	cbnz	x9, 0x4eb68 <_WeChatMain+0x352fc>
0x4eb2c	4b410091	add	x11, x10, #0x10
0x4eb30	091540b9	ldr	w9, [x8, #0x14]
0x4eb34	7f0109eb	cmp	x11, x9
0x4eb38	68010054	b.hi	0x4eb64 <_WeChatMain+0x352f8>
0x4eb3c	080540f9	ldr	x8, [x8, #0x8]
0x4eb40	08010a8b	add	x8, x8, x10
0x4eb44	0a0540b9	ldr	w10, [x8, #0x4]
0x4eb48	2b4d9252	mov	w11, #0x9269            ; =37481
0x4eb4c	2b0fb972	movk	w11, #0xc879, lsl #16
0x4eb50	5f010b6b	cmp	w10, w11
0x4eb54	81000054	b.ne	0x4eb64 <_WeChatMain+0x352f8>
0x4eb58	0a0140b9	ldr	w10, [x8]
0x4eb5c	5f410071	cmp	w10, #0x10
0x4eb60	62000054	b.hs	0x4eb6c <_WeChatMain+0x35300>
0x4eb64	00008052	mov	w0, #0x0                ; =0
0x4eb68	c0035fd6	ret
0x4eb6c	00008052	mov	w0, #0x0                ; =0
0x4eb70	0a0140b9	ldr	w10, [x8]
0x4eb74	a8ffffb4	cbz	x8, 0x4eb68 <_WeChatMain+0x352fc>
0x4eb78	4a01010b	add	w10, w10, w1
0x4eb7c	5f01096b	cmp	w10, w9
0x4eb80	48ffff54	b.hi	0x4eb68 <_WeChatMain+0x352fc>
0x4eb84	24030034	cbz	w4, 0x4ebe8 <_WeChatMain+0x3537c>
0x4eb88	09210091	add	x9, x8, #0x8
0x4eb8c	0a008012	mov	w10, #-0x1              ; =-1
0x4eb90	eb0303aa	mov	x11, x3
0x4eb94	2a7deb88	casa	w11, w10, [x9]
0x4eb98	7f01036b	cmp	w11, w3
0x4eb9c	41feff54	b.ne	0x4eb64 <_WeChatMain+0x352f8>
0x4eba0	090140b9	ldr	w9, [x8]
0x4eba4	ea777cb2	mov	x10, #0x3fffffff0       ; =17179869168
0x4eba8	29010a8b	add	x9, x9, x10
0x4ebac	29fd42d3	lsr	x9, x9, #2
0x4ebb0	c9000034	cbz	w9, 0x4ebc8 <_WeChatMain+0x3535c>
0x4ebb4	0a410091	add	x10, x8, #0x10
0x4ebb8	5ffd9f88	stlr	wzr, [x10]
0x4ebbc	4a110091	add	x10, x10, #0x4
0x4ebc0	29050071	subs	w9, w9, #0x1
0x4ebc4	a1ffff54	b.ne	0x4ebb8 <_WeChatMain+0x3534c>
0x4ebc8	5f040031	cmn	w2, #0x1
0x4ebcc	a0010054	b.eq	0x4ec00 <_WeChatMain+0x35394>
0x4ebd0	08210091	add	x8, x8, #0x8
0x4ebd4	09008012	mov	w9, #-0x1               ; =-1
0x4ebd8	02fda988	casl	w9, w2, [x8]
0x4ebdc	3f050031	cmn	w9, #0x1
0x4ebe0	e0179f1a	cset	w0, eq
0x4ebe4	c0035fd6	ret
0x4ebe8	08210091	add	x8, x8, #0x8
0x4ebec	e90303aa	mov	x9, x3
0x4ebf0	02fde988	casal	w9, w2, [x8]
0x4ebf4	3f01036b	cmp	w9, w3
0x4ebf8	e0179f1a	cset	w0, eq
0x4ebfc	c0035fd6	ret
0x4ec00	20008052	mov	w0, #0x1                ; =1
0x4ec04	c0035fd6	ret
0x4ec08	e9671c32	mov	w9, #0x3ffffff0         ; =1073741808
0x4ec0c	3f0009eb	cmp	x1, x9
0x4ec10	28010054	b.hi	0x4ec34 <_WeChatMain+0x353c8>
0x4ec14	295c0011	add	w9, w1, #0x17
0x4ec18	296d7d92	and	x9, x9, #0x7ffffff8
0x4ec1c	3f4500f1	cmp	x9, #0x11
0x4ec20	a3000054	b.lo	0x4ec34 <_WeChatMain+0x353c8>
0x4ec24	e80300aa	mov	x8, x0
0x4ec28	0a1840b9	ldr	w10, [x0, #0x18]
0x4ec2c	3f010aeb	cmp	x9, x10
0x4ec30	69000054	b.ls	0x4ec3c <_WeChatMain+0x353d0>
0x4ec34	00008052	mov	w0, #0x0                ; =0
0x4ec38	c0035fd6	ret
0x4ec3c	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4ec40	fd030091	mov	x29, sp
0x4ec44	0a0540f9	ldr	x10, [x8, #0x8]
0x4ec48	40814299	ldapur	w0, [x10, #0x28]
0x4ec4c	0aa54039	ldrb	w10, [x8, #0x29]
0x4ec50	ca000036	tbz	w10, #0x0, 0x4ec68 <_WeChatMain+0x353fc>
0x4ec54	e00308aa	mov	x0, x8
0x4ec58	91feff97	bl	0x4e69c <_WeChatMain+0x34e30>
0x4ec5c	00008052	mov	w0, #0x0                ; =0
0x4ec60	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4ec64	c0035fd6	ret
0x4ec68	0a008012	mov	w10, #-0x1              ; =-1
0x4ec6c	0c0540f9	ldr	x12, [x8, #0x8]
0x4ec70	8b2540b9	ldr	w11, [x12, #0x24]
0x4ec74	0bff0737	tbnz	w11, #0x0, 0x4ec54 <_WeChatMain+0x353e8>
0x4ec78	ed03002a	mov	w13, w0
0x4ec7c	0e1540b9	ldr	w14, [x8, #0x14]
0x4ec80	2b010d8b	add	x11, x9, x13
0x4ec84	7f010eeb	cmp	x11, x14
0x4ec88	c8050054	b.hi	0x4ed40 <_WeChatMain+0x354d4>
0x4ec8c	1f000171	cmp	w0, #0x40
0x4ec90	23feff54	b.lo	0x4ec54 <_WeChatMain+0x353e8>
0x4ec94	ab094092	and	x11, x13, #0x7
0x4ec98	ebfdffb5	cbnz	x11, 0x4ec54 <_WeChatMain+0x353e8>
0x4ec9c	ab410091	add	x11, x13, #0x10
0x4eca0	7f010eeb	cmp	x11, x14
0x4eca4	88fdff54	b.hi	0x4ec54 <_WeChatMain+0x353e8>
0x4eca8	8b010dab	adds	x11, x12, x13
0x4ecac	40fdff54	b.eq	0x4ec54 <_WeChatMain+0x353e8>
0x4ecb0	0f1940b9	ldr	w15, [x8, #0x18]
0x4ecb4	1008cf1a	udiv	w16, w0, w15
0x4ecb8	f103004b	neg	w17, w0
0x4ecbc	10460f1b	madd	w16, w16, w15, w17
0x4ecc0	ef01100b	add	w15, w15, w16
0x4ecc4	f00109eb	subs	x16, x15, x9
0x4ecc8	c2010054	b.hs	0x4ed00 <_WeChatMain+0x35494>
0x4eccc	ff410071	cmp	w15, #0x10
0x4ecd0	29fcff54	b.ls	0x4ec54 <_WeChatMain+0x353e8>
0x4ecd4	ed01000b	add	w13, w15, w0
0x4ecd8	8ea10091	add	x14, x12, #0x28
0x4ecdc	ec0300aa	mov	x12, x0
0x4ece0	cdfdec88	casal	w12, w13, [x14]
0x4ece4	9f01006b	cmp	w12, w0
0x4ece8	41020054	b.ne	0x4ed30 <_WeChatMain+0x354c4>
0x4ecec	6f0100b9	str	w15, [x11]
0x4ecf0	6a0500b9	str	w10, [x11, #0x4]
0x4ecf4	0ba54039	ldrb	w11, [x8, #0x29]
0x4ecf8	abfb0736	tbz	w11, #0x0, 0x4ec6c <_WeChatMain+0x35400>
0x4ecfc	d6ffff17	b	0x4ec54 <_WeChatMain+0x353e8>
0x4ed00	1f5e00f1	cmp	x16, #0x17
0x4ed04	a8000054	b.hi	0x4ed18 <_WeChatMain+0x354ac>
0x4ed08	e9010d8b	add	x9, x15, x13
0x4ed0c	3f010eeb	cmp	x9, x14
0x4ed10	e9030faa	mov	x9, x15
0x4ed14	08faff54	b.hi	0x4ec54 <_WeChatMain+0x353e8>
0x4ed18	0d00090b	add	w13, w0, w9
0x4ed1c	8ea10091	add	x14, x12, #0x28
0x4ed20	ec0300aa	mov	x12, x0
0x4ed24	cdfdec88	casal	w12, w13, [x14]
0x4ed28	9f01006b	cmp	w12, w0
0x4ed2c	c0020054	b.eq	0x4ed84 <_WeChatMain+0x35518>
0x4ed30	e0030caa	mov	x0, x12
0x4ed34	0ba54039	ldrb	w11, [x8, #0x29]
0x4ed38	abf90736	tbz	w11, #0x0, 0x4ec6c <_WeChatMain+0x35400>
0x4ed3c	c6ffff17	b	0x4ec54 <_WeChatMain+0x353e8>
0x4ed40	89910091	add	x9, x12, #0x24
0x4ed44	8a2540b9	ldr	w10, [x12, #0x24]
0x4ed48	4b011f32	orr	w11, w10, #0x2
0x4ed4c	e8030aaa	mov	x8, x10
0x4ed50	2b7da888	cas	w8, w11, [x9]
0x4ed54	1f010a6b	cmp	w8, w10
0x4ed58	20f8ff54	b.eq	0x4ec5c <_WeChatMain+0x353f0>
0x4ed5c	e90308aa	mov	x9, x8
0x4ed60	00008052	mov	w0, #0x0                ; =0
0x4ed64	0a011f32	orr	w10, w8, #0x2
0x4ed68	8b910091	add	x11, x12, #0x24
0x4ed6c	6a7da988	cas	w9, w10, [x11]
0x4ed70	3f01086b	cmp	w9, w8
0x4ed74	e80309aa	mov	x8, x9
0x4ed78	41ffff54	b.ne	0x4ed60 <_WeChatMain+0x354f4>
0x4ed7c	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4ed80	c0035fd6	ret
0x4ed84	6a0140b9	ldr	w10, [x11]
0x4ed88	6af6ff35	cbnz	w10, 0x4ec54 <_WeChatMain+0x353e8>
0x4ed8c	6a0540b9	ldr	w10, [x11, #0x4]
0x4ed90	2af6ff35	cbnz	w10, 0x4ec54 <_WeChatMain+0x353e8>
0x4ed94	6a0940b9	ldr	w10, [x11, #0x8]
0x4ed98	eaf5ff35	cbnz	w10, 0x4ec54 <_WeChatMain+0x353e8>
0x4ed9c	6a0d40b9	ldr	w10, [x11, #0xc]
0x4eda0	aaf5ff35	cbnz	w10, 0x4ec54 <_WeChatMain+0x353e8>
0x4eda4	0a1140f9	ldr	x10, [x8, #0x20]
0x4eda8	6c010a8b	add	x12, x11, x10
0x4edac	8c3d0091	add	x12, x12, #0xf
0x4edb0	ea030acb	neg	x10, x10
0x4edb4	8a010a8a	and	x10, x12, x10
0x4edb8	6c01098b	add	x12, x11, x9
0x4edbc	9f010aeb	cmp	x12, x10
0x4edc0	c9000054	b.ls	0x4edd8 <_WeChatMain+0x3556c>
0x4edc4	5f010039	strb	wzr, [x10]
0x4edc8	0d1140f9	ldr	x13, [x8, #0x20]
0x4edcc	4a010d8b	add	x10, x10, x13
0x4edd0	5f010ceb	cmp	x10, x12
0x4edd4	83ffff54	b.lo	0x4edc4 <_WeChatMain+0x35558>
0x4edd8	690100b9	str	w9, [x11]
0x4eddc	284d9252	mov	w8, #0x9269             ; =37481
0x4ede0	280fb972	movk	w8, #0xc879, lsl #16
0x4ede4	680500b9	str	w8, [x11, #0x4]
0x4ede8	620900b9	str	w2, [x11, #0x8]
0x4edec	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4edf0	c0035fd6	ret
0x4edf4	08a44039	ldrb	w8, [x0, #0x29]
0x4edf8	c8000037	tbnz	w8, #0x0, 0x4ee10 <_WeChatMain+0x355a4>
0x4edfc	080440f9	ldr	x8, [x0, #0x8]
0x4ee00	082540b9	ldr	w8, [x8, #0x24]
0x4ee04	68000037	tbnz	w8, #0x0, 0x4ee10 <_WeChatMain+0x355a4>
0x4ee08	00008052	mov	w0, #0x0                ; =0
0x4ee0c	c0035fd6	ret
0x4ee10	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4ee14	fd030091	mov	x29, sp
0x4ee18	21feff97	bl	0x4e69c <_WeChatMain+0x34e30>
0x4ee1c	20008052	mov	w0, #0x1                ; =1
0x4ee20	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4ee24	c0035fd6	ret
0x4ee28	08a44039	ldrb	w8, [x0, #0x29]
0x4ee2c	08090037	tbnz	w8, #0x0, 0x4ef4c <_WeChatMain+0x356e0>
0x4ee30	090440f9	ldr	x9, [x0, #0x8]
0x4ee34	282540b9	ldr	w8, [x9, #0x24]
0x4ee38	a8080037	tbnz	w8, #0x0, 0x4ef4c <_WeChatMain+0x356e0>
0x4ee3c	3f000171	cmp	w1, #0x40
0x4ee40	03030054	b.lo	0x4eea0 <_WeChatMain+0x35634>
0x4ee44	eb03012a	mov	w11, w1
0x4ee48	68094092	and	x8, x11, #0x7
0x4ee4c	a80200b5	cbnz	x8, 0x4eea0 <_WeChatMain+0x35634>
0x4ee50	68410091	add	x8, x11, #0x10
0x4ee54	0a1440b9	ldr	w10, [x0, #0x14]
0x4ee58	1f010aeb	cmp	x8, x10
0x4ee5c	28020054	b.hi	0x4eea0 <_WeChatMain+0x35634>
0x4ee60	284d9252	mov	w8, #0x9269             ; =37481
0x4ee64	280fb972	movk	w8, #0xc879, lsl #16
0x4ee68	29010b8b	add	x9, x9, x11
0x4ee6c	2b0540b9	ldr	w11, [x9, #0x4]
0x4ee70	7f01086b	cmp	w11, w8
0x4ee74	61010054	b.ne	0x4eea0 <_WeChatMain+0x35634>
0x4ee78	2b0140b9	ldr	w11, [x9]
0x4ee7c	7f410071	cmp	w11, #0x10
0x4ee80	03010054	b.lo	0x4eea0 <_WeChatMain+0x35634>
0x4ee84	2b0140b9	ldr	w11, [x9]
0x4ee88	c90000b4	cbz	x9, 0x4eea0 <_WeChatMain+0x35634>
0x4ee8c	6b01010b	add	w11, w11, w1
0x4ee90	7f010a6b	cmp	w11, w10
0x4ee94	68000054	b.hi	0x4eea0 <_WeChatMain+0x35634>
0x4ee98	2ac14099	ldapur	w10, [x9, #0xc]
0x4ee9c	4a000034	cbz	w10, 0x4eea4 <_WeChatMain+0x35638>
0x4eea0	c0035fd6	ret
0x4eea4	0a068052	mov	w10, #0x30              ; =48
0x4eea8	2ac10099	stlur	w10, [x9, #0xc]
0x4eeac	090440f9	ldr	x9, [x0, #0x8]
0x4eeb0	29c14299	ldapur	w9, [x9, #0x2c]
0x4eeb4	3fc10071	cmp	w9, #0x30
0x4eeb8	81000054	b.ne	0x4eec8 <_WeChatMain+0x3565c>
0x4eebc	0a0440f9	ldr	x10, [x0, #0x8]
0x4eec0	4ac10091	add	x10, x10, #0x30
0x4eec4	16000014	b	0x4ef1c <_WeChatMain+0x356b0>
0x4eec8	3f010171	cmp	w9, #0x40
0x4eecc	03040054	b.lo	0x4ef4c <_WeChatMain+0x356e0>
0x4eed0	ea03092a	mov	w10, w9
0x4eed4	4b094092	and	x11, x10, #0x7
0x4eed8	ab0300b5	cbnz	x11, 0x4ef4c <_WeChatMain+0x356e0>
0x4eedc	4c410091	add	x12, x10, #0x10
0x4eee0	0b1440b9	ldr	w11, [x0, #0x14]
0x4eee4	9f010beb	cmp	x12, x11
0x4eee8	28030054	b.hi	0x4ef4c <_WeChatMain+0x356e0>
0x4eeec	0c0440f9	ldr	x12, [x0, #0x8]
0x4eef0	8a010a8b	add	x10, x12, x10
0x4eef4	4c0540b9	ldr	w12, [x10, #0x4]
0x4eef8	9f01086b	cmp	w12, w8
0x4eefc	81020054	b.ne	0x4ef4c <_WeChatMain+0x356e0>
0x4ef00	4c0140b9	ldr	w12, [x10]
0x4ef04	9f410071	cmp	w12, #0x10
0x4ef08	23020054	b.lo	0x4ef4c <_WeChatMain+0x356e0>
0x4ef0c	4c0140b9	ldr	w12, [x10]
0x4ef10	8c01090b	add	w12, w12, w9
0x4ef14	9f010b6b	cmp	w12, w11
0x4ef18	a8010054	b.hi	0x4ef4c <_WeChatMain+0x356e0>
0x4ef1c	8a0100b4	cbz	x10, 0x4ef4c <_WeChatMain+0x356e0>
0x4ef20	4b310091	add	x11, x10, #0xc
0x4ef24	0a068052	mov	w10, #0x30              ; =48
0x4ef28	61fdea88	casal	w10, w1, [x11]
0x4ef2c	5fc10071	cmp	w10, #0x30
0x4ef30	00010054	b.eq	0x4ef50 <_WeChatMain+0x356e4>
0x4ef34	0b0440f9	ldr	x11, [x0, #0x8]
0x4ef38	6bb10091	add	x11, x11, #0x2c
0x4ef3c	6afde988	casal	w9, w10, [x11]
0x4ef40	3fc10071	cmp	w9, #0x30
0x4ef44	21fcff54	b.ne	0x4eec8 <_WeChatMain+0x3565c>
0x4ef48	ddffff17	b	0x4eebc <_WeChatMain+0x35650>
0x4ef4c	d4fdff17	b	0x4e69c <_WeChatMain+0x34e30>
0x4ef50	080440f9	ldr	x8, [x0, #0x8]
0x4ef54	08b10091	add	x8, x8, #0x2c
0x4ef58	01fda988	casl	w9, w1, [x8]
0x4ef5c	c0035fd6	ret
0x4ef60	010000f9	str	x1, [x0]
0x4ef64	030800b9	str	w3, [x0, #0x8]
0x4ef68	88fc60d3	lsr	x8, x4, #32
0x4ef6c	a80000b5	cbnz	x8, 0x4ef80 <_WeChatMain+0x35714>
0x4ef70	04fc0129	stp	w4, wzr, [x0, #0xc]
0x4ef74	05500039	strb	w5, [x0, #0x14]
0x4ef78	020c00f9	str	x2, [x0, #0x18]
0x4ef7c	c0035fd6	ret
0x4ef80	200020d4	brk	#0x1
0x4ef84	010000f9	str	x1, [x0]
0x4ef88	030800b9	str	w3, [x0, #0x8]
0x4ef8c	88fc60d3	lsr	x8, x4, #32
0x4ef90	080100b5	cbnz	x8, 0x4efb0 <_WeChatMain+0x35744>
0x4ef94	040c00b9	str	w4, [x0, #0xc]
0x4ef98	a8fc60d3	lsr	x8, x5, #32
0x4ef9c	a80000b5	cbnz	x8, 0x4efb0 <_WeChatMain+0x35744>
0x4efa0	051000b9	str	w5, [x0, #0x10]
0x4efa4	06500039	strb	w6, [x0, #0x14]
0x4efa8	020c00f9	str	x2, [x0, #0x18]
0x4efac	c0035fd6	ret
0x4efb0	200020d4	brk	#0x1
0x4efb4	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4efb8	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4efbc	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4efc0	fd830091	add	x29, sp, #0x20
0x4efc4	080c40f9	ldr	x8, [x0, #0x18]
0x4efc8	13c1bfb8	ldapr	w19, [x8]
0x4efcc	53040034	cbz	w19, 0x4f054 <_WeChatMain+0x357e8>
0x4efd0	e803132a	mov	w8, w19
0x4efd4	09094092	and	x9, x8, #0x7
0x4efd8	7f020171	cmp	w19, #0x40
0x4efdc	202940fa	ccmp	x9, #0x0, #0x0, hs
0x4efe0	c1070054	b.ne	0x4f0d8 <_WeChatMain+0x3586c>
0x4efe4	090040f9	ldr	x9, [x0]
0x4efe8	0a0c40b9	ldr	w10, [x0, #0xc]
0x4efec	4c410091	add	x12, x10, #0x10
0x4eff0	2b1540b9	ldr	w11, [x9, #0x14]
0x4eff4	8a01088b	add	x10, x12, x8
0x4eff8	5f010beb	cmp	x10, x11
0x4effc	e8060054	b.hi	0x4f0d8 <_WeChatMain+0x3586c>
0x4f000	0a0840b9	ldr	w10, [x0, #0x8]
0x4f004	290540f9	ldr	x9, [x9, #0x8]
0x4f008	2901088b	add	x9, x9, x8
0x4f00c	2d0540b9	ldr	w13, [x9, #0x4]
0x4f010	2e4d9252	mov	w14, #0x9269            ; =37481
0x4f014	2e0fb972	movk	w14, #0xc879, lsl #16
0x4f018	bf010e6b	cmp	w13, w14
0x4f01c	e1050054	b.ne	0x4f0d8 <_WeChatMain+0x3586c>
0x4f020	2d0140b9	ldr	w13, [x9]
0x4f024	9f010deb	cmp	x12, x13
0x4f028	88050054	b.hi	0x4f0d8 <_WeChatMain+0x3586c>
0x4f02c	2c0140b9	ldr	w12, [x9]
0x4f030	8801080b	add	w8, w12, w8
0x4f034	1f010b6b	cmp	w8, w11
0x4f038	08050054	b.hi	0x4f0d8 <_WeChatMain+0x3586c>
0x4f03c	4a090034	cbz	w10, 0x4f164 <_WeChatMain+0x358f8>
0x4f040	280940b9	ldr	w8, [x9, #0x8]
0x4f044	1f010a6b	cmp	w8, w10
0x4f048	240940fa	ccmp	x9, #0x0, #0x4, eq
0x4f04c	60040054	b.eq	0x4f0d8 <_WeChatMain+0x3586c>
0x4f050	46000014	b	0x4f168 <_WeChatMain+0x358fc>
0x4f054	150040f9	ldr	x21, [x0]
0x4f058	02504129	ldp	w2, w20, [x0, #0x8]
0x4f05c	f60300aa	mov	x22, x0
0x4f060	e00315aa	mov	x0, x21
0x4f064	e10314aa	mov	x1, x20
0x4f068	e8feff97	bl	0x4ec08 <_WeChatMain+0x3539c>
0x4f06c	f30300aa	mov	x19, x0
0x4f070	a01a40f9	ldr	x0, [x21, #0x30]
0x4f074	93020034	cbz	w19, 0x4f0c4 <_WeChatMain+0x35858>
0x4f078	a00000b4	cbz	x0, 0x4f08c <_WeChatMain+0x35820>
0x4f07c	080040f9	ldr	x8, [x0]
0x4f080	081940f9	ldr	x8, [x8, #0x30]
0x4f084	e10314aa	mov	x1, x20
0x4f088	00013fd6	blr	x8
0x4f08c	08008052	mov	w8, #0x0                ; =0
0x4f090	e00316aa	mov	x0, x22
0x4f094	c90e40f9	ldr	x9, [x22, #0x18]
0x4f098	33fda888	casl	w8, w19, [x9]
0x4f09c	1f010071	cmp	w8, #0x0
0x4f0a0	61020054	b.ne	0x4f0ec <_WeChatMain+0x35880>
0x4f0a4	08504039	ldrb	w8, [x0, #0x14]
0x4f0a8	1f050071	cmp	w8, #0x1
0x4f0ac	21f9ff54	b.ne	0x4efd0 <_WeChatMain+0x35764>
0x4f0b0	000040f9	ldr	x0, [x0]
0x4f0b4	e10313aa	mov	x1, x19
0x4f0b8	5cffff97	bl	0x4ee28 <_WeChatMain+0x355bc>
0x4f0bc	e00316aa	mov	x0, x22
0x4f0c0	c4ffff17	b	0x4efd0 <_WeChatMain+0x35764>
0x4f0c4	c00000b4	cbz	x0, 0x4f0dc <_WeChatMain+0x35870>
0x4f0c8	080040f9	ldr	x8, [x0]
0x4f0cc	081940f9	ldr	x8, [x8, #0x30]
0x4f0d0	01008052	mov	w1, #0x0                ; =0
0x4f0d4	00013fd6	blr	x8
0x4f0d8	000080d2	mov	x0, #0x0                ; =0
0x4f0dc	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4f0e0	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4f0e4	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4f0e8	c0035fd6	ret
0x4f0ec	eb03132a	mov	w11, w19
0x4f0f0	69094092	and	x9, x11, #0x7
0x4f0f4	7f020171	cmp	w19, #0x40
0x4f0f8	202940fa	ccmp	x9, #0x0, #0x0, hs
0x4f0fc	01030054	b.ne	0x4f15c <_WeChatMain+0x358f0>
0x4f100	0c0040f9	ldr	x12, [x0]
0x4f104	69410091	add	x9, x11, #0x10
0x4f108	8a1540b9	ldr	w10, [x12, #0x14]
0x4f10c	3f010aeb	cmp	x9, x10
0x4f110	68020054	b.hi	0x4f15c <_WeChatMain+0x358f0>
0x4f114	090840b9	ldr	w9, [x0, #0x8]
0x4f118	8c0540f9	ldr	x12, [x12, #0x8]
0x4f11c	8b010b8b	add	x11, x12, x11
0x4f120	6c0540b9	ldr	w12, [x11, #0x4]
0x4f124	2d4d9252	mov	w13, #0x9269            ; =37481
0x4f128	2d0fb972	movk	w13, #0xc879, lsl #16
0x4f12c	9f010d6b	cmp	w12, w13
0x4f130	61010054	b.ne	0x4f15c <_WeChatMain+0x358f0>
0x4f134	6c0140b9	ldr	w12, [x11]
0x4f138	9f410071	cmp	w12, #0x10
0x4f13c	03010054	b.lo	0x4f15c <_WeChatMain+0x358f0>
0x4f140	6c0140b9	ldr	w12, [x11]
0x4f144	cb0000b4	cbz	x11, 0x4f15c <_WeChatMain+0x358f0>
0x4f148	8c01130b	add	w12, w12, w19
0x4f14c	9f010a6b	cmp	w12, w10
0x4f150	68000054	b.hi	0x4f15c <_WeChatMain+0x358f0>
0x4f154	6a210091	add	x10, x11, #0x8
0x4f158	5ffde988	casal	w9, wzr, [x10]
0x4f15c	f30308aa	mov	x19, x8
0x4f160	9cffff17	b	0x4efd0 <_WeChatMain+0x35764>
0x4f164	a9fbffb4	cbz	x9, 0x4f0d8 <_WeChatMain+0x3586c>
0x4f168	081040b9	ldr	w8, [x0, #0x10]
0x4f16c	2801088b	add	x8, x9, x8
0x4f170	00410091	add	x0, x8, #0x10
0x4f174	daffff17	b	0x4f0dc <_WeChatMain+0x35870>
0x4f178	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4f17c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4f180	fd430091	add	x29, sp, #0x10
0x4f184	f40302aa	mov	x20, x2
0x4f188	f30300aa	mov	x19, x0
0x4f18c	e20303aa	mov	x2, x3
0x4f190	21f3ff97	bl	0x4be14 <_WeChatMain+0x325a8>
0x4f194	48d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4f198	08410e91	add	x8, x8, #0x390
0x4f19c	080000f9	str	x8, [x0]
0x4f1a0	1f1400f9	str	xzr, [x0, #0x28]
0x4f1a4	e80300aa	mov	x8, x0
0x4f1a8	1f0d02f8	str	xzr, [x8, #0x20]!
0x4f1ac	080c00f9	str	x8, [x0, #0x18]
0x4f1b0	88765e92	and	x8, x20, #0xfffffffc00000000
0x4f1b4	49fd04f0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4f1b8	29013b91	add	x9, x9, #0xec0
0x4f1bc	290540f9	ldr	x9, [x9, #0x8]
0x4f1c0	1f0109eb	cmp	x8, x9
0x4f1c4	61000054	b.ne	0x4f1d0 <_WeChatMain+0x35964>
0x4f1c8	e00314aa	mov	x0, x20
0x4f1cc	a0c1ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4f1d0	747e03a9	stp	x20, xzr, [x19, #0x30]
0x4f1d4	e00313aa	mov	x0, x19
0x4f1d8	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4f1dc	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4f1e0	c0035fd6	ret
0x4f1e4	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4f1e8	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4f1ec	fd430091	add	x29, sp, #0x10
0x4f1f0	f30300aa	mov	x19, x0
0x4f1f4	48d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4f1f8	08410e91	add	x8, x8, #0x390
0x4f1fc	080000f9	str	x8, [x0]
0x4f200	001c40f9	ldr	x0, [x0, #0x38]
0x4f204	800000b4	cbz	x0, 0x4f214 <_WeChatMain+0x359a8>
0x4f208	e10313aa	mov	x1, x19
0x4f20c	05faff97	bl	0x4da20 <_WeChatMain+0x341b4>
0x4f210	601e40f9	ldr	x0, [x19, #0x38]
0x4f214	08745e92	and	x8, x0, #0xfffffffc00000000
0x4f218	54fd04f0	adrp	x20, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4f21c	94023b91	add	x20, x20, #0xec0
0x4f220	890640f9	ldr	x9, [x20, #0x8]
0x4f224	1f0109eb	cmp	x8, x9
0x4f228	41000054	b.ne	0x4f230 <_WeChatMain+0x359c4>
0x4f22c	25c2ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4f230	7f1e00f9	str	xzr, [x19, #0x38]
0x4f234	601a40f9	ldr	x0, [x19, #0x30]
0x4f238	08745e92	and	x8, x0, #0xfffffffc00000000
0x4f23c	890640f9	ldr	x9, [x20, #0x8]
0x4f240	1f0109eb	cmp	x8, x9
0x4f244	41000054	b.ne	0x4f24c <_WeChatMain+0x359e0>
0x4f248	1ec2ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4f24c	7f1a00f9	str	xzr, [x19, #0x30]
0x4f250	611240f9	ldr	x1, [x19, #0x20]
0x4f254	60620091	add	x0, x19, #0x18
0x4f258	f1010094	bl	0x4fa1c <_WeChatMain+0x361b0>
0x4f25c	e00313aa	mov	x0, x19
0x4f260	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4f264	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4f268	29f3ff17	b	0x4bf0c <_WeChatMain+0x326a0>
0x4f26c	deffff17	b	0x4f1e4 <_WeChatMain+0x35978>
0x4f270	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4f274	fd030091	mov	x29, sp
0x4f278	dbffff97	bl	0x4f1e4 <_WeChatMain+0x35978>
0x4f27c	01088052	mov	w1, #0x40               ; =64
0x4f280	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4f284	62c3c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4f288	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4f28c	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4f290	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4f294	fd830091	add	x29, sp, #0x20
0x4f298	f30302aa	mov	x19, x2
0x4f29c	f50301aa	mov	x21, x1
0x4f2a0	f40300aa	mov	x20, x0
0x4f2a4	1d000094	bl	0x4f318 <_WeChatMain+0x35aac>
0x4f2a8	f60300aa	mov	x22, x0
0x4f2ac	080040b9	ldr	w8, [x0]
0x4f2b0	5301f837	tbnz	w19, #0x1f, 0x4f2d8 <_WeChatMain+0x35a6c>
0x4f2b4	0901130b	add	w9, w8, w19
0x4f2b8	2801084a	eor	w8, w9, w8
0x4f2bc	c90200b9	str	w9, [x22]
0x4f2c0	e801f836	tbz	w8, #0x1f, 0x4f2fc <_WeChatMain+0x35a90>
0x4f2c4	e00314aa	mov	x0, x20
0x4f2c8	01018052	mov	w1, #0x8                ; =8
0x4f2cc	e20313aa	mov	x2, x19
0x4f2d0	2af4ff97	bl	0x4c378 <_WeChatMain+0x32b0c>
0x4f2d4	0a000014	b	0x4f2fc <_WeChatMain+0x35a90>
0x4f2d8	e203134b	neg	w2, w19
0x4f2dc	1f01026b	cmp	w8, w2
0x4f2e0	a8008052	mov	w8, #0x5                ; =5
0x4f2e4	01a5881a	cinc	w1, w8, lt
0x4f2e8	e00314aa	mov	x0, x20
0x4f2ec	23f4ff97	bl	0x4c378 <_WeChatMain+0x32b0c>
0x4f2f0	c80240b9	ldr	w8, [x22]
0x4f2f4	0801130b	add	w8, w8, w19
0x4f2f8	c80200b9	str	w8, [x22]
0x4f2fc	617e359b	smull	x1, w19, w21
0x4f300	e00314aa	mov	x0, x20
0x4f304	e20313aa	mov	x2, x19
0x4f308	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4f30c	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4f310	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4f314	3df3ff17	b	0x4c008 <_WeChatMain+0x3279c>
0x4f318	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x4f31c	f65701a9	stp	x22, x21, [sp, #0x10]
0x4f320	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4f324	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4f328	fdc30091	add	x29, sp, #0x30
0x4f32c	f40301aa	mov	x20, x1
0x4f330	f30300aa	mov	x19, x0
0x4f334	f60300aa	mov	x22, x0
0x4f338	c90e42f8	ldr	x9, [x22, #0x20]!
0x4f33c	a90100b4	cbz	x9, 0x4f370 <_WeChatMain+0x35b04>
0x4f340	e80316aa	mov	x8, x22
0x4f344	2a2140b9	ldr	w10, [x9, #0x20]
0x4f348	5f01146b	cmp	w10, w20
0x4f34c	eaa79f1a	cset	w10, lt
0x4f350	08b1899a	csel	x8, x8, x9, lt
0x4f354	29596af8	ldr	x9, [x9, w10, uxtw #3]
0x4f358	69ffffb5	cbnz	x9, 0x4f344 <_WeChatMain+0x35ad8>
0x4f35c	1f0116eb	cmp	x8, x22
0x4f360	80000054	b.eq	0x4f370 <_WeChatMain+0x35b04>
0x4f364	092140b9	ldr	w9, [x8, #0x20]
0x4f368	3f01146b	cmp	w9, w20
0x4f36c	4d020054	b.le	0x4f3b4 <_WeChatMain+0x35b48>
0x4f370	e00313aa	mov	x0, x19
0x4f374	e10314aa	mov	x1, x20
0x4f378	02008052	mov	w2, #0x0                ; =0
0x4f37c	7d000094	bl	0x4f570 <_WeChatMain+0x35d04>
0x4f380	200700b5	cbnz	x0, 0x4f464 <_WeChatMain+0x35bf8>
0x4f384	601e40f9	ldr	x0, [x19, #0x38]
0x4f388	e10314aa	mov	x1, x20
0x4f38c	c9f9ff97	bl	0x4dab0 <_WeChatMain+0x34244>
0x4f390	80010034	cbz	w0, 0x4f3c0 <_WeChatMain+0x35b54>
0x4f394	e00313aa	mov	x0, x19
0x4f398	e10314aa	mov	x1, x20
0x4f39c	02008052	mov	w2, #0x0                ; =0
0x4f3a0	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4f3a4	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4f3a8	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4f3ac	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x4f3b0	70000014	b	0x4f570 <_WeChatMain+0x35d04>
0x4f3b4	001540f9	ldr	x0, [x8, #0x28]
0x4f3b8	600500b5	cbnz	x0, 0x4f464 <_WeChatMain+0x35bf8>
0x4f3bc	f2ffff17	b	0x4f384 <_WeChatMain+0x35b18>
0x4f3c0	80008052	mov	w0, #0x4                ; =4
0x4f3c4	1bc3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4f3c8	1f0000b9	str	wzr, [x0]
0x4f3cc	681240f9	ldr	x8, [x19, #0x20]
0x4f3d0	f50316aa	mov	x21, x22
0x4f3d4	a80000b5	cbnz	x8, 0x4f3e8 <_WeChatMain+0x35b7c>
0x4f3d8	0c000014	b	0x4f408 <_WeChatMain+0x35b9c>
0x4f3dc	a80240f9	ldr	x8, [x21]
0x4f3e0	f60315aa	mov	x22, x21
0x4f3e4	280100b4	cbz	x8, 0x4f408 <_WeChatMain+0x35b9c>
0x4f3e8	f50308aa	mov	x21, x8
0x4f3ec	082140b9	ldr	w8, [x8, #0x20]
0x4f3f0	1f01146b	cmp	w8, w20
0x4f3f4	4cffff54	b.gt	0x4f3dc <_WeChatMain+0x35b70>
0x4f3f8	4a030054	b.ge	0x4f460 <_WeChatMain+0x35bf4>
0x4f3fc	a80640f9	ldr	x8, [x21, #0x8]
0x4f400	48ffffb5	cbnz	x8, 0x4f3e8 <_WeChatMain+0x35b7c>
0x4f404	b6220091	add	x22, x21, #0x8
0x4f408	f70300aa	mov	x23, x0
0x4f40c	f80315aa	mov	x24, x21
0x4f410	00068052	mov	w0, #0x30               ; =48
0x4f414	07c3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4f418	f50300aa	mov	x21, x0
0x4f41c	142000b9	str	w20, [x0, #0x20]
0x4f420	1f1400f9	str	xzr, [x0, #0x28]
0x4f424	1f7c00a9	stp	xzr, xzr, [x0]
0x4f428	180800f9	str	x24, [x0, #0x10]
0x4f42c	c00200f9	str	x0, [x22]
0x4f430	680e40f9	ldr	x8, [x19, #0x18]
0x4f434	080140f9	ldr	x8, [x8]
0x4f438	e10300aa	mov	x1, x0
0x4f43c	680000b4	cbz	x8, 0x4f448 <_WeChatMain+0x35bdc>
0x4f440	680e00f9	str	x8, [x19, #0x18]
0x4f444	c10240f9	ldr	x1, [x22]
0x4f448	601240f9	ldr	x0, [x19, #0x20]
0x4f44c	3c53ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x4f450	681640f9	ldr	x8, [x19, #0x28]
0x4f454	08050091	add	x8, x8, #0x1
0x4f458	681600f9	str	x8, [x19, #0x28]
0x4f45c	e00317aa	mov	x0, x23
0x4f460	a01600f9	str	x0, [x21, #0x28]
0x4f464	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x4f468	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x4f46c	f65741a9	ldp	x22, x21, [sp, #0x10]
0x4f470	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x4f474	c0035fd6	ret
0x4f478	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4f47c	fd030091	mov	x29, sp
0x4f480	e90300aa	mov	x9, x0
0x4f484	2a0d42f8	ldr	x10, [x9, #0x20]!
0x4f488	aa0100b4	cbz	x10, 0x4f4bc <_WeChatMain+0x35c50>
0x4f48c	e80309aa	mov	x8, x9
0x4f490	4b2140b9	ldr	w11, [x10, #0x20]
0x4f494	7f01016b	cmp	w11, w1
0x4f498	eba79f1a	cset	w11, lt
0x4f49c	08b18a9a	csel	x8, x8, x10, lt
0x4f4a0	4a596bf8	ldr	x10, [x10, w11, uxtw #3]
0x4f4a4	6affffb5	cbnz	x10, 0x4f490 <_WeChatMain+0x35c24>
0x4f4a8	1f0109eb	cmp	x8, x9
0x4f4ac	80000054	b.eq	0x4f4bc <_WeChatMain+0x35c50>
0x4f4b0	092140b9	ldr	w9, [x8, #0x20]
0x4f4b4	3f01016b	cmp	w9, w1
0x4f4b8	ed000054	b.le	0x4f4d4 <_WeChatMain+0x35c68>
0x4f4bc	02008052	mov	w2, #0x0                ; =0
0x4f4c0	2c000094	bl	0x4f570 <_WeChatMain+0x35d04>
0x4f4c4	400000b4	cbz	x0, 0x4f4cc <_WeChatMain+0x35c60>
0x4f4c8	000040b9	ldr	w0, [x0]
0x4f4cc	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4f4d0	c0035fd6	ret
0x4f4d4	001540f9	ldr	x0, [x8, #0x28]
0x4f4d8	80ffffb5	cbnz	x0, 0x4f4c8 <_WeChatMain+0x35c5c>
0x4f4dc	fcffff17	b	0x4f4cc <_WeChatMain+0x35c60>
0x4f4e0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4f4e4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4f4e8	fd430091	add	x29, sp, #0x10
0x4f4ec	f30300aa	mov	x19, x0
0x4f4f0	01008012	mov	w1, #-0x1               ; =-1
0x4f4f4	22008052	mov	w2, #0x1                ; =1
0x4f4f8	1e000094	bl	0x4f570 <_WeChatMain+0x35d04>
0x4f4fc	690e40f9	ldr	x9, [x19, #0x18]
0x4f500	68820091	add	x8, x19, #0x20
0x4f504	3f0108eb	cmp	x9, x8
0x4f508	c0020054	b.eq	0x4f560 <_WeChatMain+0x35cf4>
0x4f50c	00008052	mov	w0, #0x0                ; =0
0x4f510	07000014	b	0x4f52c <_WeChatMain+0x35cc0>
0x4f514	291540f9	ldr	x9, [x9, #0x28]
0x4f518	290140b9	ldr	w9, [x9]
0x4f51c	2001000b	add	w0, w9, w0
0x4f520	e9030aaa	mov	x9, x10
0x4f524	5f0108eb	cmp	x10, x8
0x4f528	e0010054	b.eq	0x4f564 <_WeChatMain+0x35cf8>
0x4f52c	2b0540f9	ldr	x11, [x9, #0x8]
0x4f530	ec0309aa	mov	x12, x9
0x4f534	ab0000b4	cbz	x11, 0x4f548 <_WeChatMain+0x35cdc>
0x4f538	ea030baa	mov	x10, x11
0x4f53c	6b0140f9	ldr	x11, [x11]
0x4f540	cbffffb5	cbnz	x11, 0x4f538 <_WeChatMain+0x35ccc>
0x4f544	f4ffff17	b	0x4f514 <_WeChatMain+0x35ca8>
0x4f548	8a0940f9	ldr	x10, [x12, #0x10]
0x4f54c	4b0140f9	ldr	x11, [x10]
0x4f550	7f010ceb	cmp	x11, x12
0x4f554	ec030aaa	mov	x12, x10
0x4f558	81ffff54	b.ne	0x4f548 <_WeChatMain+0x35cdc>
0x4f55c	eeffff17	b	0x4f514 <_WeChatMain+0x35ca8>
0x4f560	00008052	mov	w0, #0x0                ; =0
0x4f564	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4f568	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4f56c	c0035fd6	ret
0x4f570	ffc301d1	sub	sp, sp, #0x70
0x4f574	fc6f01a9	stp	x28, x27, [sp, #0x10]
0x4f578	fa6702a9	stp	x26, x25, [sp, #0x20]
0x4f57c	f85f03a9	stp	x24, x23, [sp, #0x30]
0x4f580	f65704a9	stp	x22, x21, [sp, #0x40]
0x4f584	f44f05a9	stp	x20, x19, [sp, #0x50]
0x4f588	fd7b06a9	stp	x29, x30, [sp, #0x60]
0x4f58c	fd830191	add	x29, sp, #0x60
0x4f590	f70302aa	mov	x23, x2
0x4f594	e10f00b9	str	w1, [sp, #0xc]
0x4f598	f40300aa	mov	x20, x0
0x4f59c	151c40f9	ldr	x21, [x0, #0x38]
0x4f5a0	d50200b5	cbnz	x21, 0x4f5f8 <_WeChatMain+0x35d8c>
0x4f5a4	801a40f9	ldr	x0, [x20, #0x30]
0x4f5a8	880a40f9	ldr	x8, [x20, #0x10]
0x4f5ac	010140f9	ldr	x1, [x8]
0x4f5b0	e20314aa	mov	x2, x20
0x4f5b4	d8faff97	bl	0x4e114 <_WeChatMain+0x348a8>
0x4f5b8	f50300aa	mov	x21, x0
0x4f5bc	801e40f9	ldr	x0, [x20, #0x38]
0x4f5c0	08745e92	and	x8, x0, #0xfffffffc00000000
0x4f5c4	53fd04f0	adrp	x19, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x4f5c8	73023b91	add	x19, x19, #0xec0
0x4f5cc	690640f9	ldr	x9, [x19, #0x8]
0x4f5d0	1f0109eb	cmp	x8, x9
0x4f5d4	41000054	b.ne	0x4f5dc <_WeChatMain+0x35d70>
0x4f5d8	3ac1ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x4f5dc	a8765e92	and	x8, x21, #0xfffffffc00000000
0x4f5e0	690640f9	ldr	x9, [x19, #0x8]
0x4f5e4	1f0109eb	cmp	x8, x9
0x4f5e8	61000054	b.ne	0x4f5f4 <_WeChatMain+0x35d88>
0x4f5ec	e00315aa	mov	x0, x21
0x4f5f0	97c0ff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x4f5f4	951e00f9	str	x21, [x20, #0x38]
0x4f5f8	160080d2	mov	x22, #0x0               ; =0
0x4f5fc	93820091	add	x19, x20, #0x20
0x4f600	68008052	mov	w8, #0x3                ; =3
0x4f604	ff020071	cmp	w23, #0x0
0x4f608	e813881a	csel	w8, wzr, w8, ne
0x4f60c	e80b00b9	str	w8, [sp, #0x8]
0x4f610	04000014	b	0x4f620 <_WeChatMain+0x35db4>
0x4f614	48008052	mov	w8, #0x2                ; =2
0x4f618	1f0d0071	cmp	w8, #0x3
0x4f61c	000a0054	b.eq	0x4f75c <_WeChatMain+0x35ef0>
0x4f620	e00315aa	mov	x0, x21
0x4f624	0ff9ff97	bl	0x4da60 <_WeChatMain+0x341f4>
0x4f628	a0090034	cbz	w0, 0x4f75c <_WeChatMain+0x35ef0>
0x4f62c	e10300aa	mov	x1, x0
0x4f630	a80240f9	ldr	x8, [x21]
0x4f634	000140f9	ldr	x0, [x8]
0x4f638	02d49452	mov	w2, #0xa6a0             ; =42656
0x4f63c	c2fcb172	movk	w2, #0x8fe6, lsl #16
0x4f640	03028052	mov	w3, #0x10               ; =16
0x4f644	11fdff97	bl	0x4ea88 <_WeChatMain+0x3521c>
0x4f648	60feffb4	cbz	x0, 0x4f614 <_WeChatMain+0x35da8>
0x4f64c	f70300aa	mov	x23, x0
0x4f650	680240f9	ldr	x8, [x19]
0x4f654	a80300b4	cbz	x8, 0x4f6c8 <_WeChatMain+0x35e5c>
0x4f658	fb0a40b9	ldr	w27, [x23, #0x8]
0x4f65c	e90313aa	mov	x9, x19
0x4f660	ea0308aa	mov	x10, x8
0x4f664	4b2140b9	ldr	w11, [x10, #0x20]
0x4f668	7f011b6b	cmp	w11, w27
0x4f66c	eba79f1a	cset	w11, lt
0x4f670	29b18a9a	csel	x9, x9, x10, lt
0x4f674	4a596bf8	ldr	x10, [x10, w11, uxtw #3]
0x4f678	6affffb5	cbnz	x10, 0x4f664 <_WeChatMain+0x35df8>
0x4f67c	3f0113eb	cmp	x9, x19
0x4f680	80000054	b.eq	0x4f690 <_WeChatMain+0x35e24>
0x4f684	292140b9	ldr	w9, [x9, #0x20]
0x4f688	7f03096b	cmp	w27, w9
0x4f68c	6a050054	b.ge	0x4f738 <_WeChatMain+0x35ecc>
0x4f690	fc320091	add	x28, x23, #0xc
0x4f694	03000014	b	0x4f6a0 <_WeChatMain+0x35e34>
0x4f698	080340f9	ldr	x8, [x24]
0x4f69c	080200b4	cbz	x8, 0x4f6dc <_WeChatMain+0x35e70>
0x4f6a0	f80308aa	mov	x24, x8
0x4f6a4	082140b9	ldr	w8, [x8, #0x20]
0x4f6a8	7f03086b	cmp	w27, w8
0x4f6ac	6bffff54	b.lt	0x4f698 <_WeChatMain+0x35e2c>
0x4f6b0	1f011b6b	cmp	w8, w27
0x4f6b4	0a040054	b.ge	0x4f734 <_WeChatMain+0x35ec8>
0x4f6b8	080740f9	ldr	x8, [x24, #0x8]
0x4f6bc	28ffffb5	cbnz	x8, 0x4f6a0 <_WeChatMain+0x35e34>
0x4f6c0	19230091	add	x25, x24, #0x8
0x4f6c4	07000014	b	0x4f6e0 <_WeChatMain+0x35e74>
0x4f6c8	fc320091	add	x28, x23, #0xc
0x4f6cc	fb0a40b9	ldr	w27, [x23, #0x8]
0x4f6d0	f90313aa	mov	x25, x19
0x4f6d4	f80313aa	mov	x24, x19
0x4f6d8	02000014	b	0x4f6e0 <_WeChatMain+0x35e74>
0x4f6dc	f90318aa	mov	x25, x24
0x4f6e0	fa0318aa	mov	x26, x24
0x4f6e4	00068052	mov	w0, #0x30               ; =48
0x4f6e8	52c2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4f6ec	f80300aa	mov	x24, x0
0x4f6f0	1b2000b9	str	w27, [x0, #0x20]
0x4f6f4	1f1400f9	str	xzr, [x0, #0x28]
0x4f6f8	1f7c00a9	stp	xzr, xzr, [x0]
0x4f6fc	1a0800f9	str	x26, [x0, #0x10]
0x4f700	200300f9	str	x0, [x25]
0x4f704	880e40f9	ldr	x8, [x20, #0x18]
0x4f708	080140f9	ldr	x8, [x8]
0x4f70c	e10300aa	mov	x1, x0
0x4f710	680000b4	cbz	x8, 0x4f71c <_WeChatMain+0x35eb0>
0x4f714	880e00f9	str	x8, [x20, #0x18]
0x4f718	210340f9	ldr	x1, [x25]
0x4f71c	801240f9	ldr	x0, [x20, #0x20]
0x4f720	8752ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x4f724	881640f9	ldr	x8, [x20, #0x28]
0x4f728	08050091	add	x8, x8, #0x1
0x4f72c	881600f9	str	x8, [x20, #0x28]
0x4f730	fb0a40b9	ldr	w27, [x23, #0x8]
0x4f734	1c1700f9	str	x28, [x24, #0x28]
0x4f738	e8320091	add	x8, x23, #0xc
0x4f73c	df0200f1	cmp	x22, #0x0
0x4f740	0901969a	csel	x9, x8, x22, eq
0x4f744	e82b4129	ldp	w8, w10, [sp, #0x8]
0x4f748	7f030a6b	cmp	w27, w10
0x4f74c	e813881a	csel	w8, wzr, w8, ne
0x4f750	d612899a	csel	x22, x22, x9, ne
0x4f754	1f0d0071	cmp	w8, #0x3
0x4f758	41f6ff54	b.ne	0x4f620 <_WeChatMain+0x35db4>
0x4f75c	e00316aa	mov	x0, x22
0x4f760	fd7b46a9	ldp	x29, x30, [sp, #0x60]
0x4f764	f44f45a9	ldp	x20, x19, [sp, #0x50]
0x4f768	f65744a9	ldp	x22, x21, [sp, #0x40]
0x4f76c	f85f43a9	ldp	x24, x23, [sp, #0x30]
0x4f770	fa6742a9	ldp	x26, x25, [sp, #0x20]
0x4f774	fc6f41a9	ldp	x28, x27, [sp, #0x10]
0x4f778	ffc30191	add	sp, sp, #0x70
0x4f77c	c0035fd6	ret
0x4f780	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4f784	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4f788	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4f78c	fd830091	add	x29, sp, #0x20
0x4f790	f50300aa	mov	x21, x0
0x4f794	f30308aa	mov	x19, x8
0x4f798	01008012	mov	w1, #-0x1               ; =-1
0x4f79c	22008052	mov	w2, #0x1                ; =1
0x4f7a0	74ffff97	bl	0x4f570 <_WeChatMain+0x35d04>
0x4f7a4	00038052	mov	w0, #0x18               ; =24
0x4f7a8	22c2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4f7ac	f40300aa	mov	x20, x0
0x4f7b0	48d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4f7b4	08811091	add	x8, x8, #0x420
0x4f7b8	a90e40f9	ldr	x9, [x21, #0x18]
0x4f7bc	082400a9	stp	x8, x9, [x0]
0x4f7c0	a8820091	add	x8, x21, #0x20
0x4f7c4	080800f9	str	x8, [x0, #0x10]
0x4f7c8	3f0108eb	cmp	x9, x8
0x4f7cc	81010054	b.ne	0x4f7fc <_WeChatMain+0x35f90>
0x4f7d0	740200f9	str	x20, [x19]
0x4f7d4	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4f7d8	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4f7dc	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4f7e0	c0035fd6	ret
0x4f7e4	890600f9	str	x9, [x20, #0x8]
0x4f7e8	880240f9	ldr	x8, [x20]
0x4f7ec	080940f9	ldr	x8, [x8, #0x10]
0x4f7f0	e00314aa	mov	x0, x20
0x4f7f4	00013fd6	blr	x8
0x4f7f8	c0feff35	cbnz	w0, 0x4f7d0 <_WeChatMain+0x35f64>
0x4f7fc	880640f9	ldr	x8, [x20, #0x8]
0x4f800	091540f9	ldr	x9, [x8, #0x28]
0x4f804	290140b9	ldr	w9, [x9]
0x4f808	49feff35	cbnz	w9, 0x4f7d0 <_WeChatMain+0x35f64>
0x4f80c	0a0540f9	ldr	x10, [x8, #0x8]
0x4f810	aa0000b4	cbz	x10, 0x4f824 <_WeChatMain+0x35fb8>
0x4f814	e9030aaa	mov	x9, x10
0x4f818	4a0140f9	ldr	x10, [x10]
0x4f81c	caffffb5	cbnz	x10, 0x4f814 <_WeChatMain+0x35fa8>
0x4f820	f1ffff17	b	0x4f7e4 <_WeChatMain+0x35f78>
0x4f824	090940f9	ldr	x9, [x8, #0x10]
0x4f828	2a0140f9	ldr	x10, [x9]
0x4f82c	5f0108eb	cmp	x10, x8
0x4f830	e80309aa	mov	x8, x9
0x4f834	81ffff54	b.ne	0x4f824 <_WeChatMain+0x35fb8>
0x4f838	ebffff17	b	0x4f7e4 <_WeChatMain+0x35f78>
0x4f83c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4f840	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4f844	fd430091	add	x29, sp, #0x10
0x4f848	f40301aa	mov	x20, x1
0x4f84c	f30300aa	mov	x19, x0
0x4f850	01d49452	mov	w1, #0xa6a0             ; =42656
0x4f854	c1fcb172	movk	w1, #0x8fe6, lsl #16
0x4f858	12fcff97	bl	0x4e8a0 <_WeChatMain+0x35034>
0x4f85c	e10300aa	mov	x1, x0
0x4f860	600240f9	ldr	x0, [x19]
0x4f864	02d49452	mov	w2, #0xa6a0             ; =42656
0x4f868	c2fcb172	movk	w2, #0x8fe6, lsl #16
0x4f86c	03028052	mov	w3, #0x10               ; =16
0x4f870	86fcff97	bl	0x4ea88 <_WeChatMain+0x3521c>
0x4f874	400100b4	cbz	x0, 0x4f89c <_WeChatMain+0x36030>
0x4f878	e10300aa	mov	x1, x0
0x4f87c	080040f9	ldr	x8, [x0]
0x4f880	880200f9	str	x8, [x20]
0x4f884	600240f9	ldr	x0, [x19]
0x4f888	02d49452	mov	w2, #0xa6a0             ; =42656
0x4f88c	c2fcb172	movk	w2, #0x8fe6, lsl #16
0x4f890	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4f894	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4f898	57fcff17	b	0x4e9f4 <_WeChatMain+0x35188>
0x4f89c	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4f8a0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4f8a4	c0035fd6	ret
0x4f8a8	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x4f8ac	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4f8b0	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4f8b4	fd830091	add	x29, sp, #0x20
0x4f8b8	f40302aa	mov	x20, x2
0x4f8bc	f50301aa	mov	x21, x1
0x4f8c0	f30300aa	mov	x19, x0
0x4f8c4	01028052	mov	w1, #0x10               ; =16
0x4f8c8	02d49452	mov	w2, #0xa6a0             ; =42656
0x4f8cc	c2fcb172	movk	w2, #0x8fe6, lsl #16
0x4f8d0	07fcff97	bl	0x4e8ec <_WeChatMain+0x35080>
0x4f8d4	e10300aa	mov	x1, x0
0x4f8d8	e00313aa	mov	x0, x19
0x4f8dc	02d49452	mov	w2, #0xa6a0             ; =42656
0x4f8e0	c2fcb172	movk	w2, #0x8fe6, lsl #16
0x4f8e4	03028052	mov	w3, #0x10               ; =16
0x4f8e8	68fcff97	bl	0x4ea88 <_WeChatMain+0x3521c>
0x4f8ec	a00100b4	cbz	x0, 0x4f920 <_WeChatMain+0x360b4>
0x4f8f0	e10300aa	mov	x1, x0
0x4f8f4	150000f9	str	x21, [x0]
0x4f8f8	147c0129	stp	w20, wzr, [x0, #0x8]
0x4f8fc	e00313aa	mov	x0, x19
0x4f900	02d49452	mov	w2, #0xa6a0             ; =42656
0x4f904	c2fcb172	movk	w2, #0x8fe6, lsl #16
0x4f908	3bfcff97	bl	0x4e9f4 <_WeChatMain+0x35188>
0x4f90c	f40300aa	mov	x20, x0
0x4f910	e00313aa	mov	x0, x19
0x4f914	e10314aa	mov	x1, x20
0x4f918	44fdff97	bl	0x4ee28 <_WeChatMain+0x355bc>
0x4f91c	02000014	b	0x4f924 <_WeChatMain+0x360b8>
0x4f920	14008052	mov	w20, #0x0               ; =0
0x4f924	e00314aa	mov	x0, x20
0x4f928	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4f92c	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4f930	f657c3a8	ldp	x22, x21, [sp], #0x30
0x4f934	c0035fd6	ret
0x4f938	ff4301d1	sub	sp, sp, #0x50
0x4f93c	f65702a9	stp	x22, x21, [sp, #0x20]
0x4f940	f44f03a9	stp	x20, x19, [sp, #0x30]
0x4f944	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x4f948	fd030191	add	x29, sp, #0x40
0x4f94c	f30302aa	mov	x19, x2
0x4f950	f40301aa	mov	x20, x1
0x4f954	f50300aa	mov	x21, x0
0x4f958	e8f30132	mov	w8, #-0x55555556        ; =-1431655766
0x4f95c	e81f00b9	str	w8, [sp, #0x1c]
0x4f960	e9f301b2	mov	x9, #-0x5555555555555556 ; =-6148914691236517206
0x4f964	e90b00f9	str	x9, [sp, #0x10]
0x4f968	e80f00b9	str	w8, [sp, #0xc]
0x4f96c	280040f9	ldr	x8, [x1]
0x4f970	080940f9	ldr	x8, [x8, #0x10]
0x4f974	e00301aa	mov	x0, x1
0x4f978	00013fd6	blr	x8
0x4f97c	00020036	tbz	w0, #0x0, 0x4f9bc <_WeChatMain+0x36150>
0x4f980	20008052	mov	w0, #0x1                ; =1
0x4f984	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x4f988	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x4f98c	f65742a9	ldp	x22, x21, [sp, #0x20]
0x4f990	ff430191	add	sp, sp, #0x50
0x4f994	c0035fd6	ret
0x4f998	880240f9	ldr	x8, [x20]
0x4f99c	080d40f9	ldr	x8, [x8, #0x18]
0x4f9a0	e00314aa	mov	x0, x20
0x4f9a4	00013fd6	blr	x8
0x4f9a8	880240f9	ldr	x8, [x20]
0x4f9ac	080940f9	ldr	x8, [x8, #0x10]
0x4f9b0	e00314aa	mov	x0, x20
0x4f9b4	00013fd6	blr	x8
0x4f9b8	40feff35	cbnz	w0, 0x4f980 <_WeChatMain+0x36114>
0x4f9bc	880240f9	ldr	x8, [x20]
0x4f9c0	081140f9	ldr	x8, [x8, #0x20]
0x4f9c4	e1730091	add	x1, sp, #0x1c
0x4f9c8	e2430091	add	x2, sp, #0x10
0x4f9cc	e3330091	add	x3, sp, #0xc
0x4f9d0	e00314aa	mov	x0, x20
0x4f9d4	00013fd6	blr	x8
0x4f9d8	e80f40b9	ldr	w8, [sp, #0xc]
0x4f9dc	e8fdff34	cbz	w8, 0x4f998 <_WeChatMain+0x3612c>
0x4f9e0	e11f80b9	ldrsw	x1, [sp, #0x1c]
0x4f9e4	29040091	add	x9, x1, #0x1
0x4f9e8	ea0b40f9	ldr	x10, [sp, #0x10]
0x4f9ec	3f010aeb	cmp	x9, x10
0x4f9f0	21010054	b.ne	0x4fa14 <_WeChatMain+0x361a8>
0x4f9f4	7f020071	cmp	w19, #0x0
0x4f9f8	1605885a	cneg	w22, w8, ne
0x4f9fc	e00315aa	mov	x0, x21
0x4fa00	46feff97	bl	0x4f318 <_WeChatMain+0x35aac>
0x4fa04	080040b9	ldr	w8, [x0]
0x4fa08	0801160b	add	w8, w8, w22
0x4fa0c	080000b9	str	w8, [x0]
0x4fa10	e2ffff17	b	0x4f998 <_WeChatMain+0x3612c>
0x4fa14	00008052	mov	w0, #0x0                ; =0
0x4fa18	dbffff17	b	0x4f984 <_WeChatMain+0x36118>
0x4fa1c	210200b4	cbz	x1, 0x4fa60 <_WeChatMain+0x361f4>
0x4fa20	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4fa24	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4fa28	fd430091	add	x29, sp, #0x10
0x4fa2c	280040f9	ldr	x8, [x1]
0x4fa30	f30300aa	mov	x19, x0
0x4fa34	f40301aa	mov	x20, x1
0x4fa38	e10308aa	mov	x1, x8
0x4fa3c	f8ffff97	bl	0x4fa1c <_WeChatMain+0x361b0>
0x4fa40	810640f9	ldr	x1, [x20, #0x8]
0x4fa44	e00313aa	mov	x0, x19
0x4fa48	f5ffff97	bl	0x4fa1c <_WeChatMain+0x361b0>
0x4fa4c	e00314aa	mov	x0, x20
0x4fa50	01068052	mov	w1, #0x30               ; =48
0x4fa54	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4fa58	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4fa5c	6cc1c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4fa60	c0035fd6	ret
0x4fa64	9a2cff17	b	0x1accc <_WeChatMain+0x1460>
0x4fa68	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x4fa6c	fd030091	mov	x29, sp
0x4fa70	972cff97	bl	0x1accc <_WeChatMain+0x1460>
0x4fa74	01038052	mov	w1, #0x18               ; =24
0x4fa78	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x4fa7c	64c1c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4fa80	08a440a9	ldp	x8, x9, [x0, #0x8]
0x4fa84	1f0109eb	cmp	x8, x9
0x4fa88	e0179f1a	cset	w0, eq
0x4fa8c	c0035fd6	ret
0x4fa90	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4fa94	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4fa98	fd430091	add	x29, sp, #0x10
0x4fa9c	f30300aa	mov	x19, x0
0x4faa0	090440f9	ldr	x9, [x0, #0x8]
0x4faa4	2a0540f9	ldr	x10, [x9, #0x8]
0x4faa8	aa0000b4	cbz	x10, 0x4fabc <_WeChatMain+0x36250>
0x4faac	e8030aaa	mov	x8, x10
0x4fab0	4a0140f9	ldr	x10, [x10]
0x4fab4	caffffb5	cbnz	x10, 0x4faac <_WeChatMain+0x36240>
0x4fab8	06000014	b	0x4fad0 <_WeChatMain+0x36264>
0x4fabc	280940f9	ldr	x8, [x9, #0x10]
0x4fac0	0a0140f9	ldr	x10, [x8]
0x4fac4	5f0109eb	cmp	x10, x9
0x4fac8	e90308aa	mov	x9, x8
0x4facc	81ffff54	b.ne	0x4fabc <_WeChatMain+0x36250>
0x4fad0	680600f9	str	x8, [x19, #0x8]
0x4fad4	680240f9	ldr	x8, [x19]
0x4fad8	080940f9	ldr	x8, [x8, #0x10]
0x4fadc	e00313aa	mov	x0, x19
0x4fae0	00013fd6	blr	x8
0x4fae4	40010036	tbz	w0, #0x0, 0x4fb0c <_WeChatMain+0x362a0>
0x4fae8	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4faec	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4faf0	c0035fd6	ret
0x4faf4	690600f9	str	x9, [x19, #0x8]
0x4faf8	680240f9	ldr	x8, [x19]
0x4fafc	080940f9	ldr	x8, [x8, #0x10]
0x4fb00	e00313aa	mov	x0, x19
0x4fb04	00013fd6	blr	x8
0x4fb08	00ffff35	cbnz	w0, 0x4fae8 <_WeChatMain+0x3627c>
0x4fb0c	680640f9	ldr	x8, [x19, #0x8]
0x4fb10	091540f9	ldr	x9, [x8, #0x28]
0x4fb14	290140b9	ldr	w9, [x9]
0x4fb18	89feff35	cbnz	w9, 0x4fae8 <_WeChatMain+0x3627c>
0x4fb1c	0a0540f9	ldr	x10, [x8, #0x8]
0x4fb20	aa0000b4	cbz	x10, 0x4fb34 <_WeChatMain+0x362c8>
0x4fb24	e9030aaa	mov	x9, x10
0x4fb28	4a0140f9	ldr	x10, [x10]
0x4fb2c	caffffb5	cbnz	x10, 0x4fb24 <_WeChatMain+0x362b8>
0x4fb30	f1ffff17	b	0x4faf4 <_WeChatMain+0x36288>
0x4fb34	090940f9	ldr	x9, [x8, #0x10]
0x4fb38	2a0140f9	ldr	x10, [x9]
0x4fb3c	5f0108eb	cmp	x10, x8
0x4fb40	e80309aa	mov	x8, x9
0x4fb44	81ffff54	b.ne	0x4fb34 <_WeChatMain+0x362c8>
0x4fb48	ebffff17	b	0x4faf4 <_WeChatMain+0x36288>
0x4fb4c	810000b4	cbz	x1, 0x4fb5c <_WeChatMain+0x362f0>
0x4fb50	080440f9	ldr	x8, [x0, #0x8]
0x4fb54	082140b9	ldr	w8, [x8, #0x20]
0x4fb58	280000b9	str	w8, [x1]
0x4fb5c	a20000b4	cbz	x2, 0x4fb70 <_WeChatMain+0x36304>
0x4fb60	080440f9	ldr	x8, [x0, #0x8]
0x4fb64	082180b9	ldrsw	x8, [x8, #0x20]
0x4fb68	08050091	add	x8, x8, #0x1
0x4fb6c	480000f9	str	x8, [x2]
0x4fb70	a30000b4	cbz	x3, 0x4fb84 <_WeChatMain+0x36318>
0x4fb74	080440f9	ldr	x8, [x0, #0x8]
0x4fb78	081540f9	ldr	x8, [x8, #0x28]
0x4fb7c	080140b9	ldr	w8, [x8]
0x4fb80	680000b9	str	w8, [x3]
0x4fb84	c0035fd6	ret
0x4fb88	00e4006f	movi.2d	v0, #0000000000000000
0x4fb8c	000000ad	stp	q0, q0, [x0]
0x4fb90	08f0a752	mov	w8, #0x3f800000         ; =1065353216
0x4fb94	082000b9	str	w8, [x0, #0x20]
0x4fb98	1fa00039	strb	wzr, [x0, #0x28]
0x4fb9c	c0035fd6	ret
0x4fba0	ffc300d1	sub	sp, sp, #0x30
0x4fba4	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4fba8	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4fbac	fd830091	add	x29, sp, #0x20
0x4fbb0	e10700f9	str	x1, [sp, #0x8]
0x4fbb4	e1230091	add	x1, sp, #0x8
0x4fbb8	e2230091	add	x2, sp, #0x8
0x4fbbc	0e000094	bl	0x4fbf4 <_WeChatMain+0x36388>
0x4fbc0	130840f9	ldr	x19, [x0, #0x10]
0x4fbc4	e00740f9	ldr	x0, [sp, #0x8]
0x4fbc8	7f0200eb	cmp	x19, x0
0x4fbcc	041840fa	ccmp	x0, #0x0, #0x4, ne
0x4fbd0	80000054	b.eq	0x4fbe0 <_WeChatMain+0x36374>
0x4fbd4	3fdaff97	bl	0x464d0 <_WeChatMain+0x2cc64>
0x4fbd8	01048052	mov	w1, #0x20               ; =32
0x4fbdc	0cc1c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4fbe0	e00313aa	mov	x0, x19
0x4fbe4	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4fbe8	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4fbec	ffc30091	add	sp, sp, #0x30
0x4fbf0	c0035fd6	ret
0x4fbf4	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x4fbf8	fa6701a9	stp	x26, x25, [sp, #0x10]
0x4fbfc	f85f02a9	stp	x24, x23, [sp, #0x20]
0x4fc00	f65703a9	stp	x22, x21, [sp, #0x30]
0x4fc04	f44f04a9	stp	x20, x19, [sp, #0x40]
0x4fc08	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x4fc0c	fd430191	add	x29, sp, #0x50
0x4fc10	f50302aa	mov	x21, x2
0x4fc14	f30300aa	mov	x19, x0
0x4fc18	280040f9	ldr	x8, [x1]
0x4fc1c	171940b9	ldr	w23, [x8, #0x18]
0x4fc20	180440f9	ldr	x24, [x0, #0x8]
0x4fc24	780100b4	cbz	x24, 0x4fc50 <_WeChatMain+0x363e4>
0x4fc28	f60301aa	mov	x22, x1
0x4fc2c	0003679e	fmov	d0, x24
0x4fc30	0058200e	cnt.8b	v0, v0
0x4fc34	0038302e	uaddlv.8b	h0, v0
0x4fc38	1a00261e	fmov	w26, s0
0x4fc3c	5f0700f1	cmp	x26, #0x1
0x4fc40	c8000054	b.hi	0x4fc58 <_WeChatMain+0x363ec>
0x4fc44	08070051	sub	w8, w24, #0x1
0x4fc48	1901178a	and	x25, x8, x23
0x4fc4c	08000014	b	0x4fc6c <_WeChatMain+0x36400>
0x4fc50	f9f301b2	mov	x25, #-0x5555555555555556 ; =-6148914691236517206
0x4fc54	20000014	b	0x4fcd4 <_WeChatMain+0x36468>
0x4fc58	f90317aa	mov	x25, x23
0x4fc5c	1f0317eb	cmp	x24, x23
0x4fc60	68000054	b.hi	0x4fc6c <_WeChatMain+0x36400>
0x4fc64	e80ad81a	udiv	w8, w23, w24
0x4fc68	19dd181b	msub	w25, w8, w24, w23
0x4fc6c	680240f9	ldr	x8, [x19]
0x4fc70	087979f8	ldr	x8, [x8, x25, lsl #3]
0x4fc74	080300b4	cbz	x8, 0x4fcd4 <_WeChatMain+0x36468>
0x4fc78	140140f9	ldr	x20, [x8]
0x4fc7c	d40200b4	cbz	x20, 0x4fcd4 <_WeChatMain+0x36468>
0x4fc80	1b0700d1	sub	x27, x24, #0x1
0x4fc84	07000014	b	0x4fca0 <_WeChatMain+0x36434>
0x4fc88	800a40f9	ldr	x0, [x20, #0x10]
0x4fc8c	c10240f9	ldr	x1, [x22]
0x4fc90	3fdaff97	bl	0x4658c <_WeChatMain+0x2cd20>
0x4fc94	000a0037	tbnz	w0, #0x0, 0x4fdd4 <_WeChatMain+0x36568>
0x4fc98	940240f9	ldr	x20, [x20]
0x4fc9c	d40100b4	cbz	x20, 0x4fcd4 <_WeChatMain+0x36468>
0x4fca0	880640f9	ldr	x8, [x20, #0x8]
0x4fca4	1f0117eb	cmp	x8, x23
0x4fca8	00ffff54	b.eq	0x4fc88 <_WeChatMain+0x3641c>
0x4fcac	5f0700f1	cmp	x26, #0x1
0x4fcb0	68000054	b.hi	0x4fcbc <_WeChatMain+0x36450>
0x4fcb4	08011b8a	and	x8, x8, x27
0x4fcb8	05000014	b	0x4fccc <_WeChatMain+0x36460>
0x4fcbc	1f0118eb	cmp	x8, x24
0x4fcc0	63000054	b.lo	0x4fccc <_WeChatMain+0x36460>
0x4fcc4	0909d89a	udiv	x9, x8, x24
0x4fcc8	28a1189b	msub	x8, x9, x24, x8
0x4fccc	1f0119eb	cmp	x8, x25
0x4fcd0	40feff54	b.eq	0x4fc98 <_WeChatMain+0x3642c>
0x4fcd4	00038052	mov	w0, #0x18               ; =24
0x4fcd8	d6c0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4fcdc	f40300aa	mov	x20, x0
0x4fce0	1f5c00a9	stp	xzr, x23, [x0]
0x4fce4	a80240f9	ldr	x8, [x21]
0x4fce8	080800f9	str	x8, [x0, #0x10]
0x4fcec	680e40f9	ldr	x8, [x19, #0x18]
0x4fcf0	08050091	add	x8, x8, #0x1
0x4fcf4	0001239e	ucvtf	s0, x8
0x4fcf8	612240bd	ldr	s1, [x19, #0x20]
0x4fcfc	b80000b4	cbz	x24, 0x4fd10 <_WeChatMain+0x364a4>
0x4fd00	0203239e	ucvtf	s2, x24
0x4fd04	2208221e	fmul	s2, s1, s2
0x4fd08	4020201e	fcmp	s2, s0
0x4fd0c	05090054	b.pl	0x4fe2c <_WeChatMain+0x365c0>
0x4fd10	08fb7fd3	lsl	x8, x24, #1
0x4fd14	29008052	mov	w9, #0x1                ; =1
0x4fd18	0a0700d1	sub	x10, x24, #0x1
0x4fd1c	1f030aea	tst	x24, x10
0x4fd20	ea079f1a	cset	w10, ne
0x4fd24	1f0f00f1	cmp	x24, #0x3
0x4fd28	29318a9a	csel	x9, x9, x10, lo
0x4fd2c	280108aa	orr	x8, x9, x8
0x4fd30	0018211e	fdiv	s0, s0, s1
0x4fd34	0900299e	fcvtpu	x9, s0
0x4fd38	1f0109eb	cmp	x8, x9
0x4fd3c	0181899a	csel	x1, x8, x9, hi
0x4fd40	280400f1	subs	x8, x1, #0x1
0x4fd44	61000054	b.ne	0x4fd50 <_WeChatMain+0x364e4>
0x4fd48	41008052	mov	w1, #0x2                ; =2
0x4fd4c	06000014	b	0x4fd64 <_WeChatMain+0x364f8>
0x4fd50	3f0008ea	tst	x1, x8
0x4fd54	80000054	b.eq	0x4fd64 <_WeChatMain+0x364f8>
0x4fd58	e00301aa	mov	x0, x1
0x4fd5c	93bec395	bl	0x713f7a8 <_wxam_enc_uninit_10+0x713f7a8>
0x4fd60	e10300aa	mov	x1, x0
0x4fd64	750640f9	ldr	x21, [x19, #0x8]
0x4fd68	3f0015eb	cmp	x1, x21
0x4fd6c	89000054	b.ls	0x4fd7c <_WeChatMain+0x36510>
0x4fd70	e00313aa	mov	x0, x19
0x4fd74	bc6aff97	bl	0x2a864 <_WeChatMain+0x10ff8>
0x4fd78	20000014	b	0x4fdf8 <_WeChatMain+0x3658c>
0x4fd7c	e2030054	b.hs	0x4fdf8 <_WeChatMain+0x3658c>
0x4fd80	680e40f9	ldr	x8, [x19, #0x18]
0x4fd84	0001239e	ucvtf	s0, x8
0x4fd88	612240bd	ldr	s1, [x19, #0x20]
0x4fd8c	0018211e	fdiv	s0, s0, s1
0x4fd90	0000299e	fcvtpu	x0, s0
0x4fd94	bf0e00f1	cmp	x21, #0x3
0x4fd98	23020054	b.lo	0x4fddc <_WeChatMain+0x36570>
0x4fd9c	a002679e	fmov	d0, x21
0x4fda0	0058200e	cnt.8b	v0, v0
0x4fda4	0038302e	uaddlv.8b	h0, v0
0x4fda8	0800261e	fmov	w8, s0
0x4fdac	1f0500f1	cmp	x8, #0x1
0x4fdb0	68010054	b.hi	0x4fddc <_WeChatMain+0x36570>
0x4fdb4	080400d1	sub	x8, x0, #0x1
0x4fdb8	0811c0da	clz	x8, x8
0x4fdbc	e80308cb	neg	x8, x8
0x4fdc0	29008052	mov	w9, #0x1                ; =1
0x4fdc4	2821c89a	lsl	x8, x9, x8
0x4fdc8	1f0800f1	cmp	x0, #0x2
0x4fdcc	0030889a	csel	x0, x0, x8, lo
0x4fdd0	06000014	b	0x4fde8 <_WeChatMain+0x3657c>
0x4fdd4	010080d2	mov	x1, #0x0                ; =0
0x4fdd8	33000014	b	0x4fea4 <_WeChatMain+0x36638>
0x4fddc	f60301aa	mov	x22, x1
0x4fde0	72bec395	bl	0x713f7a8 <_wxam_enc_uninit_10+0x713f7a8>
0x4fde4	e10316aa	mov	x1, x22
0x4fde8	3f0000eb	cmp	x1, x0
0x4fdec	2180809a	csel	x1, x1, x0, hi
0x4fdf0	3f0015eb	cmp	x1, x21
0x4fdf4	e3fbff54	b.lo	0x4fd70 <_WeChatMain+0x36504>
0x4fdf8	780640f9	ldr	x24, [x19, #0x8]
0x4fdfc	080700d1	sub	x8, x24, #0x1
0x4fe00	1f0308ea	tst	x24, x8
0x4fe04	81000054	b.ne	0x4fe14 <_WeChatMain+0x365a8>
0x4fe08	08070051	sub	w8, w24, #0x1
0x4fe0c	1901178a	and	x25, x8, x23
0x4fe10	07000014	b	0x4fe2c <_WeChatMain+0x365c0>
0x4fe14	1f0317eb	cmp	x24, x23
0x4fe18	69000054	b.ls	0x4fe24 <_WeChatMain+0x365b8>
0x4fe1c	f90317aa	mov	x25, x23
0x4fe20	03000014	b	0x4fe2c <_WeChatMain+0x365c0>
0x4fe24	e80ad89a	udiv	x8, x23, x24
0x4fe28	19dd189b	msub	x25, x8, x24, x23
0x4fe2c	690240f9	ldr	x9, [x19]
0x4fe30	287979f8	ldr	x8, [x9, x25, lsl #3]
0x4fe34	880000b4	cbz	x8, 0x4fe44 <_WeChatMain+0x365d8>
0x4fe38	090140f9	ldr	x9, [x8]
0x4fe3c	890200f9	str	x9, [x20]
0x4fe40	14000014	b	0x4fe90 <_WeChatMain+0x36624>
0x4fe44	e80313aa	mov	x8, x19
0x4fe48	0a0d41f8	ldr	x10, [x8, #0x10]!
0x4fe4c	8a0200f9	str	x10, [x20]
0x4fe50	140100f9	str	x20, [x8]
0x4fe54	287939f8	str	x8, [x9, x25, lsl #3]
0x4fe58	880240f9	ldr	x8, [x20]
0x4fe5c	c80100b4	cbz	x8, 0x4fe94 <_WeChatMain+0x36628>
0x4fe60	080540f9	ldr	x8, [x8, #0x8]
0x4fe64	090700d1	sub	x9, x24, #0x1
0x4fe68	1f0309ea	tst	x24, x9
0x4fe6c	61000054	b.ne	0x4fe78 <_WeChatMain+0x3660c>
0x4fe70	0801098a	and	x8, x8, x9
0x4fe74	05000014	b	0x4fe88 <_WeChatMain+0x3661c>
0x4fe78	1f0118eb	cmp	x8, x24
0x4fe7c	63000054	b.lo	0x4fe88 <_WeChatMain+0x3661c>
0x4fe80	0909d89a	udiv	x9, x8, x24
0x4fe84	28a1189b	msub	x8, x9, x24, x8
0x4fe88	690240f9	ldr	x9, [x19]
0x4fe8c	280d088b	add	x8, x9, x8, lsl #3
0x4fe90	140100f9	str	x20, [x8]
0x4fe94	680e40f9	ldr	x8, [x19, #0x18]
0x4fe98	08050091	add	x8, x8, #0x1
0x4fe9c	680e00f9	str	x8, [x19, #0x18]
0x4fea0	21008052	mov	w1, #0x1                ; =1
0x4fea4	e00314aa	mov	x0, x20
0x4fea8	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x4feac	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x4feb0	f65743a9	ldp	x22, x21, [sp, #0x30]
0x4feb4	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x4feb8	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x4febc	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x4fec0	c0035fd6	ret
0x4fec4	ffc300d1	sub	sp, sp, #0x30
0x4fec8	f44f01a9	stp	x20, x19, [sp, #0x10]
0x4fecc	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x4fed0	fd830091	add	x29, sp, #0x20
0x4fed4	f40301aa	mov	x20, x1
0x4fed8	f30300aa	mov	x19, x0
0x4fedc	00038052	mov	w0, #0x18               ; =24
0x4fee0	54c0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x4fee4	f76cff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x4fee8	e00700f9	str	x0, [sp, #0x8]
0x4feec	e2230091	add	x2, sp, #0x8
0x4fef0	e00313aa	mov	x0, x19
0x4fef4	e10314aa	mov	x1, x20
0x4fef8	e2efff97	bl	0x4be80 <_WeChatMain+0x32614>
0x4fefc	e00740f9	ldr	x0, [sp, #0x8]
0x4ff00	ff0700f9	str	xzr, [sp, #0x8]
0x4ff04	600000b4	cbz	x0, 0x4ff10 <_WeChatMain+0x366a4>
0x4ff08	01038052	mov	w1, #0x18               ; =24
0x4ff0c	40c0c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4ff10	48d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4ff14	08e11191	add	x8, x8, #0x478
0x4ff18	680200f9	str	x8, [x19]
0x4ff1c	7f1600f9	str	xzr, [x19, #0x28]
0x4ff20	e80313aa	mov	x8, x19
0x4ff24	1f0d02f8	str	xzr, [x8, #0x20]!
0x4ff28	680e00f9	str	x8, [x19, #0x18]
0x4ff2c	e00313aa	mov	x0, x19
0x4ff30	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x4ff34	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x4ff38	ffc30091	add	sp, sp, #0x30
0x4ff3c	c0035fd6	ret
0x4ff40	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4ff44	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4ff48	fd430091	add	x29, sp, #0x10
0x4ff4c	f30300aa	mov	x19, x0
0x4ff50	48d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4ff54	08e11191	add	x8, x8, #0x478
0x4ff58	080000f9	str	x8, [x0]
0x4ff5c	011040f9	ldr	x1, [x0, #0x20]
0x4ff60	00600091	add	x0, x0, #0x18
0x4ff64	06010094	bl	0x5037c <_WeChatMain+0x36b10>
0x4ff68	e00313aa	mov	x0, x19
0x4ff6c	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4ff70	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4ff74	e6efff17	b	0x4bf0c <_WeChatMain+0x326a0>
0x4ff78	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x4ff7c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x4ff80	fd430091	add	x29, sp, #0x10
0x4ff84	f30300aa	mov	x19, x0
0x4ff88	48d704d0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x4ff8c	08e11191	add	x8, x8, #0x478
0x4ff90	080000f9	str	x8, [x0]
0x4ff94	011040f9	ldr	x1, [x0, #0x20]
0x4ff98	00600091	add	x0, x0, #0x18
0x4ff9c	f8000094	bl	0x5037c <_WeChatMain+0x36b10>
0x4ffa0	e00313aa	mov	x0, x19
0x4ffa4	daefff97	bl	0x4bf0c <_WeChatMain+0x326a0>
0x4ffa8	01068052	mov	w1, #0x30               ; =48
0x4ffac	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x4ffb0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x4ffb4	16c0c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x4ffb8	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x4ffbc	f65701a9	stp	x22, x21, [sp, #0x10]
0x4ffc0	f44f02a9	stp	x20, x19, [sp, #0x20]
0x4ffc4	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x4ffc8	fdc30091	add	x29, sp, #0x30
0x4ffcc	f30302aa	mov	x19, x2
0x4ffd0	f50301aa	mov	x21, x1
0x4ffd4	f40300aa	mov	x20, x0
0x4ffd8	f70300aa	mov	x23, x0
0x4ffdc	e80e42f8	ldr	x8, [x23, #0x20]!
0x4ffe0	c80000b5	cbnz	x8, 0x4fff8 <_WeChatMain+0x3678c>
0x4ffe4	f60317aa	mov	x22, x23
0x4ffe8	0c000014	b	0x50018 <_WeChatMain+0x367ac>
0x4ffec	c80240f9	ldr	x8, [x22]
0x4fff0	f70316aa	mov	x23, x22
0x4fff4	280100b4	cbz	x8, 0x50018 <_WeChatMain+0x367ac>
0x4fff8	f60308aa	mov	x22, x8
0x4fffc	081d40b9	ldr	w8, [x8, #0x1c]
0x50000	1f01156b	cmp	w8, w21
0x50004	4cffff54	b.gt	0x4ffec <_WeChatMain+0x36780>
0x50008	ea020054	b.ge	0x50064 <_WeChatMain+0x367f8>
0x5000c	c80640f9	ldr	x8, [x22, #0x8]
0x50010	48ffffb5	cbnz	x8, 0x4fff8 <_WeChatMain+0x3678c>
0x50014	d7220091	add	x23, x22, #0x8
0x50018	f80316aa	mov	x24, x22
0x5001c	00058052	mov	w0, #0x28               ; =40
0x50020	04c0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x50024	f60300aa	mov	x22, x0
0x50028	15fc0329	stp	w21, wzr, [x0, #0x1c]
0x5002c	1f7c00a9	stp	xzr, xzr, [x0]
0x50030	180800f9	str	x24, [x0, #0x10]
0x50034	e00200f9	str	x0, [x23]
0x50038	880e40f9	ldr	x8, [x20, #0x18]
0x5003c	080140f9	ldr	x8, [x8]
0x50040	e10300aa	mov	x1, x0
0x50044	680000b4	cbz	x8, 0x50050 <_WeChatMain+0x367e4>
0x50048	880e00f9	str	x8, [x20, #0x18]
0x5004c	e10240f9	ldr	x1, [x23]
0x50050	801240f9	ldr	x0, [x20, #0x20]
0x50054	3a50ff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x50058	881640f9	ldr	x8, [x20, #0x28]
0x5005c	08050091	add	x8, x8, #0x1
0x50060	881600f9	str	x8, [x20, #0x28]
0x50064	c82240b9	ldr	w8, [x22, #0x20]
0x50068	0801130b	add	w8, w8, w19
0x5006c	c82200b9	str	w8, [x22, #0x20]
0x50070	617e359b	smull	x1, w19, w21
0x50074	e00314aa	mov	x0, x20
0x50078	e20313aa	mov	x2, x19
0x5007c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x50080	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x50084	f65741a9	ldp	x22, x21, [sp, #0x10]
0x50088	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x5008c	dfefff17	b	0x4c008 <_WeChatMain+0x3279c>
0x50090	090c42f8	ldr	x9, [x0, #0x20]!
0x50094	a90100b4	cbz	x9, 0x500c8 <_WeChatMain+0x3685c>
0x50098	e80300aa	mov	x8, x0
0x5009c	2a1d40b9	ldr	w10, [x9, #0x1c]
0x500a0	5f01016b	cmp	w10, w1
0x500a4	eaa79f1a	cset	w10, lt
0x500a8	08b1899a	csel	x8, x8, x9, lt
0x500ac	29596af8	ldr	x9, [x9, w10, uxtw #3]
0x500b0	69ffffb5	cbnz	x9, 0x5009c <_WeChatMain+0x36830>
0x500b4	1f0100eb	cmp	x8, x0
0x500b8	80000054	b.eq	0x500c8 <_WeChatMain+0x3685c>
0x500bc	091d40b9	ldr	w9, [x8, #0x1c]
0x500c0	3f01016b	cmp	w9, w1
0x500c4	6d000054	b.le	0x500d0 <_WeChatMain+0x36864>
0x500c8	00008052	mov	w0, #0x0                ; =0
0x500cc	c0035fd6	ret
0x500d0	002140b9	ldr	w0, [x8, #0x20]
0x500d4	c0035fd6	ret
0x500d8	090c40f9	ldr	x9, [x0, #0x18]
0x500dc	08800091	add	x8, x0, #0x20
0x500e0	3f0108eb	cmp	x9, x8
0x500e4	a0020054	b.eq	0x50138 <_WeChatMain+0x368cc>
0x500e8	00008052	mov	w0, #0x0                ; =0
0x500ec	06000014	b	0x50104 <_WeChatMain+0x36898>
0x500f0	292140b9	ldr	w9, [x9, #0x20]
0x500f4	2001000b	add	w0, w9, w0
0x500f8	e9030aaa	mov	x9, x10
0x500fc	5f0108eb	cmp	x10, x8
0x50100	e0010054	b.eq	0x5013c <_WeChatMain+0x368d0>
0x50104	2b0540f9	ldr	x11, [x9, #0x8]
0x50108	ec0309aa	mov	x12, x9
0x5010c	ab0000b4	cbz	x11, 0x50120 <_WeChatMain+0x368b4>
0x50110	ea030baa	mov	x10, x11
0x50114	6b0140f9	ldr	x11, [x11]
0x50118	cbffffb5	cbnz	x11, 0x50110 <_WeChatMain+0x368a4>
0x5011c	f5ffff17	b	0x500f0 <_WeChatMain+0x36884>
0x50120	8a0940f9	ldr	x10, [x12, #0x10]
0x50124	4b0140f9	ldr	x11, [x10]
0x50128	7f010ceb	cmp	x11, x12
0x5012c	ec030aaa	mov	x12, x10
0x50130	81ffff54	b.ne	0x50120 <_WeChatMain+0x368b4>
0x50134	efffff17	b	0x500f0 <_WeChatMain+0x36884>
0x50138	00008052	mov	w0, #0x0                ; =0
0x5013c	c0035fd6	ret
0x50140	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x50144	f44f01a9	stp	x20, x19, [sp, #0x10]
0x50148	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x5014c	fd830091	add	x29, sp, #0x20
0x50150	f50300aa	mov	x21, x0
0x50154	f30308aa	mov	x19, x8
0x50158	00038052	mov	w0, #0x18               ; =24
0x5015c	b5bfc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x50160	f40300aa	mov	x20, x0
0x50164	48d704b0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x50168	08211491	add	x8, x8, #0x508
0x5016c	a90e40f9	ldr	x9, [x21, #0x18]
0x50170	082400a9	stp	x8, x9, [x0]
0x50174	a8820091	add	x8, x21, #0x20
0x50178	080800f9	str	x8, [x0, #0x10]
0x5017c	3f0108eb	cmp	x9, x8
0x50180	81010054	b.ne	0x501b0 <_WeChatMain+0x36944>
0x50184	740200f9	str	x20, [x19]
0x50188	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x5018c	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x50190	f657c3a8	ldp	x22, x21, [sp], #0x30
0x50194	c0035fd6	ret
0x50198	890600f9	str	x9, [x20, #0x8]
0x5019c	880240f9	ldr	x8, [x20]
0x501a0	080940f9	ldr	x8, [x8, #0x10]
0x501a4	e00314aa	mov	x0, x20
0x501a8	00013fd6	blr	x8
0x501ac	c0feff35	cbnz	w0, 0x50184 <_WeChatMain+0x36918>
0x501b0	880640f9	ldr	x8, [x20, #0x8]
0x501b4	092140b9	ldr	w9, [x8, #0x20]
0x501b8	69feff35	cbnz	w9, 0x50184 <_WeChatMain+0x36918>
0x501bc	0a0540f9	ldr	x10, [x8, #0x8]
0x501c0	aa0000b4	cbz	x10, 0x501d4 <_WeChatMain+0x36968>
0x501c4	e9030aaa	mov	x9, x10
0x501c8	4a0140f9	ldr	x10, [x10]
0x501cc	caffffb5	cbnz	x10, 0x501c4 <_WeChatMain+0x36958>
0x501d0	f2ffff17	b	0x50198 <_WeChatMain+0x3692c>
0x501d4	090940f9	ldr	x9, [x8, #0x10]
0x501d8	2a0140f9	ldr	x10, [x9]
0x501dc	5f0108eb	cmp	x10, x8
0x501e0	e80309aa	mov	x8, x9
0x501e4	81ffff54	b.ne	0x501d4 <_WeChatMain+0x36968>
0x501e8	ecffff17	b	0x50198 <_WeChatMain+0x3692c>
0x501ec	ff0302d1	sub	sp, sp, #0x80
0x501f0	fc6f02a9	stp	x28, x27, [sp, #0x20]
0x501f4	fa6703a9	stp	x26, x25, [sp, #0x30]
0x501f8	f85f04a9	stp	x24, x23, [sp, #0x40]
0x501fc	f65705a9	stp	x22, x21, [sp, #0x50]
0x50200	f44f06a9	stp	x20, x19, [sp, #0x60]
0x50204	fd7b07a9	stp	x29, x30, [sp, #0x70]
0x50208	fdc30191	add	x29, sp, #0x70
0x5020c	f30302aa	mov	x19, x2
0x50210	f40301aa	mov	x20, x1
0x50214	f50300aa	mov	x21, x0
0x50218	e8f30132	mov	w8, #-0x55555556        ; =-1431655766
0x5021c	e81f00b9	str	w8, [sp, #0x1c]
0x50220	e9f301b2	mov	x9, #-0x5555555555555556 ; =-6148914691236517206
0x50224	e90b00f9	str	x9, [sp, #0x10]
0x50228	e80f00b9	str	w8, [sp, #0xc]
0x5022c	280040f9	ldr	x8, [x1]
0x50230	080940f9	ldr	x8, [x8, #0x10]
0x50234	e00301aa	mov	x0, x1
0x50238	00013fd6	blr	x8
0x5023c	60000036	tbz	w0, #0x0, 0x50248 <_WeChatMain+0x369dc>
0x50240	36008052	mov	w22, #0x1               ; =1
0x50244	45000014	b	0x50358 <_WeChatMain+0x36aec>
0x50248	b8820091	add	x24, x21, #0x20
0x5024c	12000014	b	0x50294 <_WeChatMain+0x36a28>
0x50250	a01240f9	ldr	x0, [x21, #0x20]
0x50254	ba4fff97	bl	0x2413c <_WeChatMain+0xa8d0>
0x50258	a81640f9	ldr	x8, [x21, #0x28]
0x5025c	08050091	add	x8, x8, #0x1
0x50260	a81600f9	str	x8, [x21, #0x28]
0x50264	e82240b9	ldr	w8, [x23, #0x20]
0x50268	0801190b	add	w8, w8, w25
0x5026c	e82200b9	str	w8, [x23, #0x20]
0x50270	880240f9	ldr	x8, [x20]
0x50274	080d40f9	ldr	x8, [x8, #0x18]
0x50278	e00314aa	mov	x0, x20
0x5027c	00013fd6	blr	x8
0x50280	880240f9	ldr	x8, [x20]
0x50284	080940f9	ldr	x8, [x8, #0x10]
0x50288	e00314aa	mov	x0, x20
0x5028c	00013fd6	blr	x8
0x50290	40060035	cbnz	w0, 0x50358 <_WeChatMain+0x36aec>
0x50294	880240f9	ldr	x8, [x20]
0x50298	081140f9	ldr	x8, [x8, #0x20]
0x5029c	e1730091	add	x1, sp, #0x1c
0x502a0	e2430091	add	x2, sp, #0x10
0x502a4	e3330091	add	x3, sp, #0xc
0x502a8	e00314aa	mov	x0, x20
0x502ac	00013fd6	blr	x8
0x502b0	fa1f80b9	ldrsw	x26, [sp, #0x1c]
0x502b4	48070091	add	x8, x26, #0x1
0x502b8	e90b40f9	ldr	x9, [sp, #0x10]
0x502bc	1f0109eb	cmp	x8, x9
0x502c0	f6179f1a	cset	w22, eq
0x502c4	81040054	b.ne	0x50354 <_WeChatMain+0x36ae8>
0x502c8	e80f40b9	ldr	w8, [sp, #0xc]
0x502cc	7f020071	cmp	w19, #0x0
0x502d0	1905885a	cneg	w25, w8, ne
0x502d4	080340f9	ldr	x8, [x24]
0x502d8	fb0318aa	mov	x27, x24
0x502dc	f70318aa	mov	x23, x24
0x502e0	a80000b5	cbnz	x8, 0x502f4 <_WeChatMain+0x36a88>
0x502e4	0d000014	b	0x50318 <_WeChatMain+0x36aac>
0x502e8	e80240f9	ldr	x8, [x23]
0x502ec	fb0317aa	mov	x27, x23
0x502f0	480100b4	cbz	x8, 0x50318 <_WeChatMain+0x36aac>
0x502f4	f70308aa	mov	x23, x8
0x502f8	081d40b9	ldr	w8, [x8, #0x1c]
0x502fc	5f03086b	cmp	w26, w8
0x50300	4bffff54	b.lt	0x502e8 <_WeChatMain+0x36a7c>
0x50304	1f011a6b	cmp	w8, w26
0x50308	eafaff54	b.ge	0x50264 <_WeChatMain+0x369f8>
0x5030c	e80640f9	ldr	x8, [x23, #0x8]
0x50310	28ffffb5	cbnz	x8, 0x502f4 <_WeChatMain+0x36a88>
0x50314	fb220091	add	x27, x23, #0x8
0x50318	fc0317aa	mov	x28, x23
0x5031c	00058052	mov	w0, #0x28               ; =40
0x50320	44bfc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x50324	f70300aa	mov	x23, x0
0x50328	1afc0329	stp	w26, wzr, [x0, #0x1c]
0x5032c	1f7c00a9	stp	xzr, xzr, [x0]
0x50330	1c0800f9	str	x28, [x0, #0x10]
0x50334	600300f9	str	x0, [x27]
0x50338	a80e40f9	ldr	x8, [x21, #0x18]
0x5033c	080140f9	ldr	x8, [x8]
0x50340	e10300aa	mov	x1, x0
0x50344	68f8ffb4	cbz	x8, 0x50250 <_WeChatMain+0x369e4>
0x50348	a80e00f9	str	x8, [x21, #0x18]
0x5034c	610340f9	ldr	x1, [x27]
0x50350	c0ffff17	b	0x50250 <_WeChatMain+0x369e4>
0x50354	16008052	mov	w22, #0x0               ; =0
0x50358	e00316aa	mov	x0, x22
0x5035c	fd7b47a9	ldp	x29, x30, [sp, #0x70]
0x50360	f44f46a9	ldp	x20, x19, [sp, #0x60]
0x50364	f65745a9	ldp	x22, x21, [sp, #0x50]
0x50368	f85f44a9	ldp	x24, x23, [sp, #0x40]
0x5036c	fa6743a9	ldp	x26, x25, [sp, #0x30]
0x50370	fc6f42a9	ldp	x28, x27, [sp, #0x20]
0x50374	ff030291	add	sp, sp, #0x80
0x50378	c0035fd6	ret
0x5037c	210200b4	cbz	x1, 0x503c0 <_WeChatMain+0x36b54>
0x50380	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x50384	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x50388	fd430091	add	x29, sp, #0x10
0x5038c	280040f9	ldr	x8, [x1]
0x50390	f30300aa	mov	x19, x0
0x50394	f40301aa	mov	x20, x1
0x50398	e10308aa	mov	x1, x8
0x5039c	f8ffff97	bl	0x5037c <_WeChatMain+0x36b10>
0x503a0	810640f9	ldr	x1, [x20, #0x8]
0x503a4	e00313aa	mov	x0, x19
0x503a8	f5ffff97	bl	0x5037c <_WeChatMain+0x36b10>
0x503ac	e00314aa	mov	x0, x20
0x503b0	01058052	mov	w1, #0x28               ; =40
0x503b4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x503b8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x503bc	14bfc315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x503c0	c0035fd6	ret
0x503c4	422aff17	b	0x1accc <_WeChatMain+0x1460>
0x503c8	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x503cc	fd030091	mov	x29, sp
0x503d0	3f2aff97	bl	0x1accc <_WeChatMain+0x1460>
0x503d4	01038052	mov	w1, #0x18               ; =24
0x503d8	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x503dc	0cbfc315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x503e0	08a440a9	ldp	x8, x9, [x0, #0x8]
0x503e4	1f0109eb	cmp	x8, x9
0x503e8	e0179f1a	cset	w0, eq
0x503ec	c0035fd6	ret
0x503f0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x503f4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x503f8	fd430091	add	x29, sp, #0x10
0x503fc	f30300aa	mov	x19, x0
0x50400	090440f9	ldr	x9, [x0, #0x8]
0x50404	2a0540f9	ldr	x10, [x9, #0x8]
0x50408	aa0000b4	cbz	x10, 0x5041c <_WeChatMain+0x36bb0>
0x5040c	e8030aaa	mov	x8, x10
0x50410	4a0140f9	ldr	x10, [x10]
0x50414	caffffb5	cbnz	x10, 0x5040c <_WeChatMain+0x36ba0>
0x50418	06000014	b	0x50430 <_WeChatMain+0x36bc4>
0x5041c	280940f9	ldr	x8, [x9, #0x10]
0x50420	0a0140f9	ldr	x10, [x8]
0x50424	5f0109eb	cmp	x10, x9
0x50428	e90308aa	mov	x9, x8
0x5042c	81ffff54	b.ne	0x5041c <_WeChatMain+0x36bb0>
0x50430	680600f9	str	x8, [x19, #0x8]
0x50434	680240f9	ldr	x8, [x19]
0x50438	080940f9	ldr	x8, [x8, #0x10]
0x5043c	e00313aa	mov	x0, x19
0x50440	00013fd6	blr	x8
0x50444	40010036	tbz	w0, #0x0, 0x5046c <_WeChatMain+0x36c00>
0x50448	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5044c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x50450	c0035fd6	ret
0x50454	690600f9	str	x9, [x19, #0x8]
0x50458	680240f9	ldr	x8, [x19]
0x5045c	080940f9	ldr	x8, [x8, #0x10]
0x50460	e00313aa	mov	x0, x19
0x50464	00013fd6	blr	x8
0x50468	00ffff35	cbnz	w0, 0x50448 <_WeChatMain+0x36bdc>
0x5046c	680640f9	ldr	x8, [x19, #0x8]
0x50470	092140b9	ldr	w9, [x8, #0x20]
0x50474	a9feff35	cbnz	w9, 0x50448 <_WeChatMain+0x36bdc>
0x50478	0a0540f9	ldr	x10, [x8, #0x8]
0x5047c	aa0000b4	cbz	x10, 0x50490 <_WeChatMain+0x36c24>
0x50480	e9030aaa	mov	x9, x10
0x50484	4a0140f9	ldr	x10, [x10]
0x50488	caffffb5	cbnz	x10, 0x50480 <_WeChatMain+0x36c14>
0x5048c	f2ffff17	b	0x50454 <_WeChatMain+0x36be8>
0x50490	090940f9	ldr	x9, [x8, #0x10]
0x50494	2a0140f9	ldr	x10, [x9]
0x50498	5f0108eb	cmp	x10, x8
0x5049c	e80309aa	mov	x8, x9
0x504a0	81ffff54	b.ne	0x50490 <_WeChatMain+0x36c24>
0x504a4	ecffff17	b	0x50454 <_WeChatMain+0x36be8>
0x504a8	810000b4	cbz	x1, 0x504b8 <_WeChatMain+0x36c4c>
0x504ac	080440f9	ldr	x8, [x0, #0x8]
0x504b0	081d40b9	ldr	w8, [x8, #0x1c]
0x504b4	280000b9	str	w8, [x1]
0x504b8	a20000b4	cbz	x2, 0x504cc <_WeChatMain+0x36c60>
0x504bc	080440f9	ldr	x8, [x0, #0x8]
0x504c0	081d80b9	ldrsw	x8, [x8, #0x1c]
0x504c4	08050091	add	x8, x8, #0x1
0x504c8	480000f9	str	x8, [x2]
0x504cc	830000b4	cbz	x3, 0x504dc <_WeChatMain+0x36c70>
0x504d0	080440f9	ldr	x8, [x0, #0x8]
0x504d4	082140b9	ldr	w8, [x8, #0x20]
0x504d8	680000b9	str	w8, [x3]
0x504dc	c0035fd6	ret
0x504e0	ffc300d1	sub	sp, sp, #0x30
0x504e4	f44f01a9	stp	x20, x19, [sp, #0x10]
0x504e8	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x504ec	fd830091	add	x29, sp, #0x20
0x504f0	f40303aa	mov	x20, x3
0x504f4	f30300aa	mov	x19, x0
0x504f8	47eeff97	bl	0x4be14 <_WeChatMain+0x325a8>
0x504fc	48d704b0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x50500	08811591	add	x8, x8, #0x560
0x50504	080000f9	str	x8, [x0]
0x50508	1f0c00f9	str	xzr, [x0, #0x18]
0x5050c	88765e92	and	x8, x20, #0xfffffffc00000000
0x50510	49fd04d0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x50514	29013b91	add	x9, x9, #0xec0
0x50518	290540f9	ldr	x9, [x9, #0x8]
0x5051c	1f0109eb	cmp	x8, x9
0x50520	61000054	b.ne	0x5052c <_WeChatMain+0x36cc0>
0x50524	e00314aa	mov	x0, x20
0x50528	c9bcff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x5052c	741200f9	str	x20, [x19, #0x20]
0x50530	892240a9	ldp	x9, x8, [x20]
0x50534	080109cb	sub	x8, x8, x9
0x50538	091005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5053c	2a355b39	ldrb	w10, [x9, #0x6cd]
0x50540	ea030037	tbnz	w10, #0x0, 0x505bc <_WeChatMain+0x36d50>
0x50544	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x50548	402942fd	ldr	d0, [x10, #0x450]
0x5054c	8a210490	adrp	x10, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x50550	416d47fd	ldr	d1, [x10, #0xed8]
0x50554	221ca14e	mov.16b	v2, v1
0x50558	02040c6e	mov.s	v2[1], v0[0]
0x5055c	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x50560	402d42fd	ldr	d0, [x10, #0x458]
0x50564	0204146e	mov.s	v2[2], v0[0]
0x50568	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5056c	403142fd	ldr	d0, [x10, #0x460]
0x50570	02041c6e	mov.s	v2[3], v0[0]
0x50574	0a1005d0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50578	4aa11a91	add	x10, x10, #0x6a8
0x5057c	cb2104b0	adrp	x11, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x50580	60e143fd	ldr	d0, [x11, #0x7c0]
0x50584	01040c6e	mov.s	v1[1], v0[0]
0x50588	8b210490	adrp	x11, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x5058c	60a545fd	ldr	d0, [x11, #0xb48]
0x50590	0104146e	mov.s	v1[2], v0[0]
0x50594	8b2104f0	adrp	x11, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x50598	601541fd	ldr	d0, [x11, #0x228]
0x5059c	01041c6e	mov.s	v1[3], v0[0]
0x505a0	420500ad	stp	q2, q1, [x10]
0x505a4	cb2104d0	adrp	x11, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x505a8	603542fd	ldr	d0, [x11, #0x468]
0x505ac	402100bd	str	s0, [x10, #0x20]
0x505b0	5f910039	strb	wzr, [x10, #0x24]
0x505b4	2a008052	mov	w10, #0x1               ; =1
0x505b8	2a351b39	strb	w10, [x9, #0x6cd]
0x505bc	1f1100f1	cmp	x8, #0x4
0x505c0	61050054	b.ne	0x5066c <_WeChatMain+0x36e00>
0x505c4	000080d2	mov	x0, #0x0                ; =0
0x505c8	8245ff97	bl	0x21bd0 <_WeChatMain+0x8364>
0x505cc	f40300aa	mov	x20, x0
0x505d0	20008052	mov	w0, #0x1                ; =1
0x505d4	3045ff97	bl	0x21a94 <_WeChatMain+0x8228>
0x505d8	e30300aa	mov	x3, x0
0x505dc	011005d0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x505e0	21a01a91	add	x1, x1, #0x6a8
0x505e4	e0230091	add	x0, sp, #0x8
0x505e8	e20314aa	mov	x2, x20
0x505ec	6c47ff97	bl	0x2239c <_WeChatMain+0x8b30>
0x505f0	e80740f9	ldr	x8, [sp, #0x8]
0x505f4	e80700f9	str	x8, [sp, #0x8]
0x505f8	a80300b4	cbz	x8, 0x5066c <_WeChatMain+0x36e00>
0x505fc	081005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50600	09f15c39	ldrb	w9, [x8, #0x73c]
0x50604	49020037	tbnz	w9, #0x0, 0x5064c <_WeChatMain+0x36de0>
0x50608	090080d2	mov	x9, #0x0                ; =0
0x5060c	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x50610	4a411391	add	x10, x10, #0x4d0
0x50614	0b1005d0	adrp	x11, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50618	6b391b91	add	x11, x11, #0x6ce
0x5061c	4c01098b	add	x12, x10, x9
0x50620	8c254139	ldrb	w12, [x12, #0x49]
0x50624	2d0d4092	and	x13, x9, #0xf
0x50628	4d010d8b	add	x13, x10, x13
0x5062c	ade54039	ldrb	w13, [x13, #0x39]
0x50630	ac010c4a	eor	w12, w13, w12
0x50634	6c692938	strb	w12, [x11, x9]
0x50638	29050091	add	x9, x9, #0x1
0x5063c	3fb901f1	cmp	x9, #0x6e
0x50640	e1feff54	b.ne	0x5061c <_WeChatMain+0x36db0>
0x50644	29008052	mov	w9, #0x1                ; =1
0x50648	09f11c39	strb	w9, [x8, #0x73c]
0x5064c	001005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50650	00381b91	add	x0, x0, #0x6ce
0x50654	e8030091	mov	x8, sp
0x50658	e2230091	add	x2, sp, #0x8
0x5065c	01048052	mov	w1, #0x20               ; =32
0x50660	6144ff97	bl	0x217e4 <_WeChatMain+0x7f78>
0x50664	e0030091	mov	x0, sp
0x50668	8128ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x5066c	e00313aa	mov	x0, x19
0x50670	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x50674	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x50678	ffc30091	add	sp, sp, #0x30
0x5067c	c0035fd6	ret
0x50680	ff0301d1	sub	sp, sp, #0x40
0x50684	f44f02a9	stp	x20, x19, [sp, #0x20]
0x50688	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x5068c	fdc30091	add	x29, sp, #0x30
0x50690	f40303aa	mov	x20, x3
0x50694	f30300aa	mov	x19, x0
0x50698	480040f9	ldr	x8, [x2]
0x5069c	5f0000f9	str	xzr, [x2]
0x506a0	e80b00f9	str	x8, [sp, #0x10]
0x506a4	e2430091	add	x2, sp, #0x10
0x506a8	f6edff97	bl	0x4be80 <_WeChatMain+0x32614>
0x506ac	e00b40f9	ldr	x0, [sp, #0x10]
0x506b0	ff0b00f9	str	xzr, [sp, #0x10]
0x506b4	600000b4	cbz	x0, 0x506c0 <_WeChatMain+0x36e54>
0x506b8	01038052	mov	w1, #0x18               ; =24
0x506bc	54bec395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x506c0	48d704b0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x506c4	08811591	add	x8, x8, #0x560
0x506c8	680200f9	str	x8, [x19]
0x506cc	7f0e00f9	str	xzr, [x19, #0x18]
0x506d0	88765e92	and	x8, x20, #0xfffffffc00000000
0x506d4	49fd04d0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x506d8	29013b91	add	x9, x9, #0xec0
0x506dc	290540f9	ldr	x9, [x9, #0x8]
0x506e0	1f0109eb	cmp	x8, x9
0x506e4	61000054	b.ne	0x506f0 <_WeChatMain+0x36e84>
0x506e8	e00314aa	mov	x0, x20
0x506ec	58bcff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x506f0	741200f9	str	x20, [x19, #0x20]
0x506f4	892240a9	ldp	x9, x8, [x20]
0x506f8	080109cb	sub	x8, x8, x9
0x506fc	091005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50700	2a355b39	ldrb	w10, [x9, #0x6cd]
0x50704	ea030037	tbnz	w10, #0x0, 0x50780 <_WeChatMain+0x36f14>
0x50708	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5070c	402942fd	ldr	d0, [x10, #0x450]
0x50710	8a210490	adrp	x10, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x50714	416d47fd	ldr	d1, [x10, #0xed8]
0x50718	221ca14e	mov.16b	v2, v1
0x5071c	02040c6e	mov.s	v2[1], v0[0]
0x50720	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x50724	402d42fd	ldr	d0, [x10, #0x458]
0x50728	0204146e	mov.s	v2[2], v0[0]
0x5072c	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x50730	403142fd	ldr	d0, [x10, #0x460]
0x50734	02041c6e	mov.s	v2[3], v0[0]
0x50738	0a1005d0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5073c	4aa11a91	add	x10, x10, #0x6a8
0x50740	cb2104b0	adrp	x11, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x50744	60e143fd	ldr	d0, [x11, #0x7c0]
0x50748	01040c6e	mov.s	v1[1], v0[0]
0x5074c	8b210490	adrp	x11, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x50750	60a545fd	ldr	d0, [x11, #0xb48]
0x50754	0104146e	mov.s	v1[2], v0[0]
0x50758	8b2104f0	adrp	x11, 0x8483000 <_wxam_enc_uninit_10+0x8483000>
0x5075c	601541fd	ldr	d0, [x11, #0x228]
0x50760	01041c6e	mov.s	v1[3], v0[0]
0x50764	420500ad	stp	q2, q1, [x10]
0x50768	cb2104d0	adrp	x11, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5076c	603542fd	ldr	d0, [x11, #0x468]
0x50770	402100bd	str	s0, [x10, #0x20]
0x50774	5f910039	strb	wzr, [x10, #0x24]
0x50778	2a008052	mov	w10, #0x1               ; =1
0x5077c	2a351b39	strb	w10, [x9, #0x6cd]
0x50780	1f1100f1	cmp	x8, #0x4
0x50784	61050054	b.ne	0x50830 <_WeChatMain+0x36fc4>
0x50788	000080d2	mov	x0, #0x0                ; =0
0x5078c	1145ff97	bl	0x21bd0 <_WeChatMain+0x8364>
0x50790	f40300aa	mov	x20, x0
0x50794	20008052	mov	w0, #0x1                ; =1
0x50798	bf44ff97	bl	0x21a94 <_WeChatMain+0x8228>
0x5079c	e30300aa	mov	x3, x0
0x507a0	011005d0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x507a4	21a01a91	add	x1, x1, #0x6a8
0x507a8	e0630091	add	x0, sp, #0x18
0x507ac	e20314aa	mov	x2, x20
0x507b0	fb46ff97	bl	0x2239c <_WeChatMain+0x8b30>
0x507b4	e80f40f9	ldr	x8, [sp, #0x18]
0x507b8	e80f00f9	str	x8, [sp, #0x18]
0x507bc	a80300b4	cbz	x8, 0x50830 <_WeChatMain+0x36fc4>
0x507c0	081005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x507c4	09f15c39	ldrb	w9, [x8, #0x73c]
0x507c8	49020037	tbnz	w9, #0x0, 0x50810 <_WeChatMain+0x36fa4>
0x507cc	090080d2	mov	x9, #0x0                ; =0
0x507d0	ca2104d0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x507d4	4a411391	add	x10, x10, #0x4d0
0x507d8	0b1005d0	adrp	x11, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x507dc	6b391b91	add	x11, x11, #0x6ce
0x507e0	4c01098b	add	x12, x10, x9
0x507e4	8c254139	ldrb	w12, [x12, #0x49]
0x507e8	2d0d4092	and	x13, x9, #0xf
0x507ec	4d010d8b	add	x13, x10, x13
0x507f0	ade54039	ldrb	w13, [x13, #0x39]
0x507f4	ac010c4a	eor	w12, w13, w12
0x507f8	6c692938	strb	w12, [x11, x9]
0x507fc	29050091	add	x9, x9, #0x1
0x50800	3fb901f1	cmp	x9, #0x6e
0x50804	e1feff54	b.ne	0x507e0 <_WeChatMain+0x36f74>
0x50808	29008052	mov	w9, #0x1                ; =1
0x5080c	09f11c39	strb	w9, [x8, #0x73c]
0x50810	001005d0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50814	00381b91	add	x0, x0, #0x6ce
0x50818	e8230091	add	x8, sp, #0x8
0x5081c	e2630091	add	x2, sp, #0x18
0x50820	e1048052	mov	w1, #0x27               ; =39
0x50824	f043ff97	bl	0x217e4 <_WeChatMain+0x7f78>
0x50828	e0230091	add	x0, sp, #0x8
0x5082c	1028ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x50830	e00313aa	mov	x0, x19
0x50834	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x50838	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x5083c	ff030191	add	sp, sp, #0x40
0x50840	c0035fd6	ret
0x50844	200020d4	brk	#0x1
0x50848	200020d4	brk	#0x1
0x5084c	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x50850	f65701a9	stp	x22, x21, [sp, #0x10]
0x50854	f44f02a9	stp	x20, x19, [sp, #0x20]
0x50858	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x5085c	fdc30091	add	x29, sp, #0x30
0x50860	f40302aa	mov	x20, x2
0x50864	f50301aa	mov	x21, x1
0x50868	f30300aa	mov	x19, x0
0x5086c	f70300aa	mov	x23, x0
0x50870	e88641f8	ldr	x8, [x23], #0x18
0x50874	083540f9	ldr	x8, [x8, #0x68]
0x50878	00013fd6	blr	x8
0x5087c	f60300aa	mov	x22, x0
0x50880	e8c2bff8	ldapr	x8, [x23]
0x50884	e80200b5	cbnz	x8, 0x508e0 <_WeChatMain+0x37074>
0x50888	e00313aa	mov	x0, x19
0x5088c	e10315aa	mov	x1, x21
0x50890	e20314aa	mov	x2, x20
0x50894	e30316aa	mov	x3, x22
0x50898	e0e2c195	bl	0x70c9418 <_SetWeixinCallbackFunc+0x22e201c>
0x5089c	e0010034	cbz	w0, 0x508d8 <_WeChatMain+0x3706c>
0x508a0	688241d9	ldapur	x8, [x19, #0x18]
0x508a4	680400b4	cbz	x8, 0x50930 <_WeChatMain+0x370c4>
0x508a8	680a40f9	ldr	x8, [x19, #0x10]
0x508ac	00510091	add	x0, x8, #0x14
0x508b0	21008052	mov	w1, #0x1                ; =1
0x508b4	4fedff97	bl	0x4bdf0 <_WeChatMain+0x32584>
0x508b8	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x508bc	a3030054	b.lo	0x50930 <_WeChatMain+0x370c4>
0x508c0	087c1053	lsr	w8, w0, #16
0x508c4	698241d9	ldapur	x9, [x19, #0x18]
0x508c8	0a3c0012	and	w10, w0, #0xffff
0x508cc	29492a8b	add	x9, x9, w10, uxtw #2
0x508d0	280128b8	ldadd	w8, w8, [x9]
0x508d4	17000014	b	0x50930 <_WeChatMain+0x370c4>
0x508d8	e00313aa	mov	x0, x19
0x508dc	1a000094	bl	0x50944 <_WeChatMain+0x370d8>
0x508e0	688241d9	ldapur	x8, [x19, #0x18]
0x508e4	0809168b	add	x8, x8, x22, lsl #2
0x508e8	160134b8	ldadd	w20, w22, [x8]
0x508ec	817e359b	smull	x1, w20, w21
0x508f0	e00313aa	mov	x0, x19
0x508f4	e20314aa	mov	x2, x20
0x508f8	c4edff97	bl	0x4c008 <_WeChatMain+0x3279c>
0x508fc	9f060071	cmp	w20, #0x1
0x50900	8b010054	b.lt	0x50930 <_WeChatMain+0x370c4>
0x50904	c802140b	add	w8, w22, w20
0x50908	0801164a	eor	w8, w8, w22
0x5090c	2801f836	tbz	w8, #0x1f, 0x50930 <_WeChatMain+0x370c4>
0x50910	e00313aa	mov	x0, x19
0x50914	01018052	mov	w1, #0x8                ; =8
0x50918	e20314aa	mov	x2, x20
0x5091c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x50920	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x50924	f65741a9	ldp	x22, x21, [sp, #0x10]
0x50928	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x5092c	93eeff17	b	0x4c378 <_WeChatMain+0x32b0c>
0x50930	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x50934	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x50938	f65741a9	ldp	x22, x21, [sp, #0x10]
0x5093c	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x50940	c0035fd6	ret
0x50944	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x50948	f44f01a9	stp	x20, x19, [sp, #0x10]
0x5094c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x50950	fd830091	add	x29, sp, #0x20
0x50954	f30300aa	mov	x19, x0
0x50958	080c40f9	ldr	x8, [x0, #0x18]
0x5095c	480400b5	cbnz	x8, 0x509e4 <_WeChatMain+0x37178>
0x50960	081005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50964	08811991	add	x8, x8, #0x660
0x50968	14c1bff8	ldapr	x20, [x8]
0x5096c	9f0600f1	cmp	x20, #0x1
0x50970	08020054	b.hi	0x509b0 <_WeChatMain+0x37144>
0x50974	151005d0	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50978	b5821991	add	x21, x21, #0x660
0x5097c	e00315aa	mov	x0, x21
0x50980	c1aaff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x50984	40010034	cbz	w0, 0x509ac <_WeChatMain+0x37140>
0x50988	b4220091	add	x20, x21, #0x8
0x5098c	e00314aa	mov	x0, x20
0x50990	93660094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x50994	e00315aa	mov	x0, x21
0x50998	e10314aa	mov	x1, x20
0x5099c	020080d2	mov	x2, #0x0                ; =0
0x509a0	e30315aa	mov	x3, x21
0x509a4	dcaaff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x509a8	02000014	b	0x509b0 <_WeChatMain+0x37144>
0x509ac	b4c2bff8	ldapr	x20, [x21]
0x509b0	e00314aa	mov	x0, x20
0x509b4	d0c2c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x509b8	40030035	cbnz	w0, 0x50a20 <_WeChatMain+0x371b4>
0x509bc	680e40f9	ldr	x8, [x19, #0x18]
0x509c0	e80000b5	cbnz	x8, 0x509dc <_WeChatMain+0x37170>
0x509c4	f50313aa	mov	x21, x19
0x509c8	a88641f8	ldr	x8, [x21], #0x18
0x509cc	083d40f9	ldr	x8, [x8, #0x78]
0x509d0	e00313aa	mov	x0, x19
0x509d4	00013fd6	blr	x8
0x509d8	a0fe9fc8	stlr	x0, [x21]
0x509dc	e00314aa	mov	x0, x20
0x509e0	c8c2c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x509e4	680a40f9	ldr	x8, [x19, #0x10]
0x509e8	00510091	add	x0, x8, #0x14
0x509ec	21008052	mov	w1, #0x1                ; =1
0x509f0	00edff97	bl	0x4bdf0 <_WeChatMain+0x32584>
0x509f4	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x509f8	c3000054	b.lo	0x50a10 <_WeChatMain+0x371a4>
0x509fc	087c1053	lsr	w8, w0, #16
0x50a00	698241d9	ldapur	x9, [x19, #0x18]
0x50a04	0a3c0012	and	w10, w0, #0xffff
0x50a08	29492a8b	add	x9, x9, w10, uxtw #2
0x50a0c	280128b8	ldadd	w8, w8, [x9]
0x50a10	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x50a14	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x50a18	f657c3a8	ldp	x22, x21, [sp], #0x30
0x50a1c	c0035fd6	ret
0x50a20	e00314aa	mov	x0, x20
0x50a24	98660094	bl	0x6a484 <_WeChatMain+0x50c18>
0x50a28	680e40f9	ldr	x8, [x19, #0x18]
0x50a2c	88fdffb5	cbnz	x8, 0x509dc <_WeChatMain+0x37170>
0x50a30	e5ffff17	b	0x509c4 <_WeChatMain+0x37158>
0x50a34	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x50a38	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x50a3c	fd430091	add	x29, sp, #0x10
0x50a40	f30300aa	mov	x19, x0
0x50a44	080040f9	ldr	x8, [x0]
0x50a48	083540f9	ldr	x8, [x8, #0x68]
0x50a4c	00013fd6	blr	x8
0x50a50	f40300aa	mov	x20, x0
0x50a54	680a40f9	ldr	x8, [x19, #0x10]
0x50a58	00510091	add	x0, x8, #0x14
0x50a5c	e1ecff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x50a60	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x50a64	62010054	b.hs	0x50a90 <_WeChatMain+0x37224>
0x50a68	688241d9	ldapur	x8, [x19, #0x18]
0x50a6c	c80000b5	cbnz	x8, 0x50a84 <_WeChatMain+0x37218>
0x50a70	680240f9	ldr	x8, [x19]
0x50a74	083940f9	ldr	x8, [x8, #0x70]
0x50a78	e00313aa	mov	x0, x19
0x50a7c	00013fd6	blr	x8
0x50a80	00010034	cbz	w0, 0x50aa0 <_WeChatMain+0x37234>
0x50a84	688241d9	ldapur	x8, [x19, #0x18]
0x50a88	007974b8	ldr	w0, [x8, x20, lsl #2]
0x50a8c	05000014	b	0x50aa0 <_WeChatMain+0x37234>
0x50a90	087c1053	lsr	w8, w0, #16
0x50a94	093c0012	and	w9, w0, #0xffff
0x50a98	9f0209eb	cmp	x20, x9
0x50a9c	00019f1a	csel	w0, w8, wzr, eq
0x50aa0	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x50aa4	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x50aa8	c0035fd6	ret
0x50aac	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x50ab0	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x50ab4	fd430091	add	x29, sp, #0x10
0x50ab8	f30300aa	mov	x19, x0
0x50abc	080840f9	ldr	x8, [x0, #0x10]
0x50ac0	00510091	add	x0, x8, #0x14
0x50ac4	c7ecff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x50ac8	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x50acc	a2020054	b.hs	0x50b20 <_WeChatMain+0x372b4>
0x50ad0	688241d9	ldapur	x8, [x19, #0x18]
0x50ad4	c80000b5	cbnz	x8, 0x50aec <_WeChatMain+0x37280>
0x50ad8	680240f9	ldr	x8, [x19]
0x50adc	083940f9	ldr	x8, [x8, #0x70]
0x50ae0	e00313aa	mov	x0, x19
0x50ae4	00013fd6	blr	x8
0x50ae8	e0010034	cbz	w0, 0x50b24 <_WeChatMain+0x372b8>
0x50aec	681240f9	ldr	x8, [x19, #0x20]
0x50af0	082540a9	ldp	x8, x9, [x8]
0x50af4	280108cb	sub	x8, x9, x8
0x50af8	09fd4293	asr	x9, x8, #2
0x50afc	688241d9	ldapur	x8, [x19, #0x18]
0x50b00	00008052	mov	w0, #0x0                ; =0
0x50b04	290500f1	subs	x9, x9, #0x1
0x50b08	e0000054	b.eq	0x50b24 <_WeChatMain+0x372b8>
0x50b0c	0a4540b8	ldr	w10, [x8], #0x4
0x50b10	4001000b	add	w0, w10, w0
0x50b14	290500f1	subs	x9, x9, #0x1
0x50b18	a1ffff54	b.ne	0x50b0c <_WeChatMain+0x372a0>
0x50b1c	02000014	b	0x50b24 <_WeChatMain+0x372b8>
0x50b20	007c1053	lsr	w0, w0, #16
0x50b24	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x50b28	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x50b2c	c0035fd6	ret
0x50b30	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x50b34	f85f01a9	stp	x24, x23, [sp, #0x10]
0x50b38	f65702a9	stp	x22, x21, [sp, #0x20]
0x50b3c	f44f03a9	stp	x20, x19, [sp, #0x30]
0x50b40	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x50b44	fd030191	add	x29, sp, #0x40
0x50b48	f60300aa	mov	x22, x0
0x50b4c	f30308aa	mov	x19, x8
0x50b50	080840f9	ldr	x8, [x0, #0x10]
0x50b54	00510091	add	x0, x8, #0x14
0x50b58	a2ecff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x50b5c	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x50b60	c2050054	b.hs	0x50c18 <_WeChatMain+0x373ac>
0x50b64	c88241d9	ldapur	x8, [x22, #0x18]
0x50b68	c80000b5	cbnz	x8, 0x50b80 <_WeChatMain+0x37314>
0x50b6c	c80240f9	ldr	x8, [x22]
0x50b70	083940f9	ldr	x8, [x8, #0x70]
0x50b74	e00316aa	mov	x0, x22
0x50b78	00013fd6	blr	x8
0x50b7c	a0070034	cbz	w0, 0x50c70 <_WeChatMain+0x37404>
0x50b80	d58241d9	ldapur	x21, [x22, #0x18]
0x50b84	d61240f9	ldr	x22, [x22, #0x20]
0x50b88	c92240a9	ldp	x9, x8, [x22]
0x50b8c	080109cb	sub	x8, x8, x9
0x50b90	17fd4293	asr	x23, x8, #2
0x50b94	f80600d1	sub	x24, x23, #0x1
0x50b98	00058052	mov	w0, #0x28               ; =40
0x50b9c	25bdc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x50ba0	f40300aa	mov	x20, x0
0x50ba4	48d704b0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x50ba8	08411c91	add	x8, x8, #0x710
0x50bac	080000f9	str	x8, [x0]
0x50bb0	a8765e92	and	x8, x21, #0xfffffffc00000000
0x50bb4	59fd04d0	adrp	x25, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x50bb8	39033b91	add	x25, x25, #0xec0
0x50bbc	290740f9	ldr	x9, [x25, #0x8]
0x50bc0	1f0109eb	cmp	x8, x9
0x50bc4	61000054	b.ne	0x50bd0 <_WeChatMain+0x37364>
0x50bc8	e00315aa	mov	x0, x21
0x50bcc	20bbff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x50bd0	95e200a9	stp	x21, x24, [x20, #0x8]
0x50bd4	c8765e92	and	x8, x22, #0xfffffffc00000000
0x50bd8	290740f9	ldr	x9, [x25, #0x8]
0x50bdc	1f0109eb	cmp	x8, x9
0x50be0	61000054	b.ne	0x50bec <_WeChatMain+0x37380>
0x50be4	e00316aa	mov	x0, x22
0x50be8	19bbff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x50bec	96fe01a9	stp	x22, xzr, [x20, #0x18]
0x50bf0	380300b4	cbz	x24, 0x50c54 <_WeChatMain+0x373e8>
0x50bf4	28008052	mov	w8, #0x1                ; =1
0x50bf8	a90240b9	ldr	w9, [x21]
0x50bfc	c9020035	cbnz	w9, 0x50c54 <_WeChatMain+0x373e8>
0x50c00	b5120091	add	x21, x21, #0x4
0x50c04	881200f9	str	x8, [x20, #0x20]
0x50c08	08050091	add	x8, x8, #0x1
0x50c0c	ff0208eb	cmp	x23, x8
0x50c10	41ffff54	b.ne	0x50bf8 <_WeChatMain+0x3738c>
0x50c14	10000014	b	0x50c54 <_WeChatMain+0x373e8>
0x50c18	157c1053	lsr	w21, w0, #16
0x50c1c	c81240f9	ldr	x8, [x22, #0x20]
0x50c20	163c0012	and	w22, w0, #0xffff
0x50c24	080140f9	ldr	x8, [x8]
0x50c28	0849368b	add	x8, x8, w22, uxtw #2
0x50c2c	17614029	ldp	w23, w24, [x8]
0x50c30	187f4093	sxtw	x24, w24
0x50c34	00058052	mov	w0, #0x28               ; =40
0x50c38	febcc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x50c3c	f40300aa	mov	x20, x0
0x50c40	e10317aa	mov	x1, x23
0x50c44	e20318aa	mov	x2, x24
0x50c48	e30315aa	mov	x3, x21
0x50c4c	e40316aa	mov	x4, x22
0x50c50	20f1ff97	bl	0x4d0d0 <_WeChatMain+0x33864>
0x50c54	740200f9	str	x20, [x19]
0x50c58	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x50c5c	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x50c60	f65742a9	ldp	x22, x21, [sp, #0x20]
0x50c64	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x50c68	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x50c6c	c0035fd6	ret
0x50c70	00058052	mov	w0, #0x28               ; =40
0x50c74	efbcc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x50c78	f40300aa	mov	x20, x0
0x50c7c	d51240f9	ldr	x21, [x22, #0x20]
0x50c80	48d704b0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x50c84	08411c91	add	x8, x8, #0x710
0x50c88	1ffc00a9	stp	xzr, xzr, [x0, #0x8]
0x50c8c	080000f9	str	x8, [x0]
0x50c90	a8765e92	and	x8, x21, #0xfffffffc00000000
0x50c94	49fd04d0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x50c98	29013b91	add	x9, x9, #0xec0
0x50c9c	290540f9	ldr	x9, [x9, #0x8]
0x50ca0	1f0109eb	cmp	x8, x9
0x50ca4	61000054	b.ne	0x50cb0 <_WeChatMain+0x37444>
0x50ca8	e00315aa	mov	x0, x21
0x50cac	e8baff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x50cb0	95fe01a9	stp	x21, xzr, [x20, #0x18]
0x50cb4	e8ffff17	b	0x50c54 <_WeChatMain+0x373e8>
0x50cb8	ff8301d1	sub	sp, sp, #0x60
0x50cbc	f85f02a9	stp	x24, x23, [sp, #0x20]
0x50cc0	f65703a9	stp	x22, x21, [sp, #0x30]
0x50cc4	f44f04a9	stp	x20, x19, [sp, #0x40]
0x50cc8	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x50ccc	fd430191	add	x29, sp, #0x50
0x50cd0	f40302aa	mov	x20, x2
0x50cd4	f50301aa	mov	x21, x1
0x50cd8	f30300aa	mov	x19, x0
0x50cdc	280040f9	ldr	x8, [x1]
0x50ce0	080940f9	ldr	x8, [x8, #0x10]
0x50ce4	e00301aa	mov	x0, x1
0x50ce8	00013fd6	blr	x8
0x50cec	60000036	tbz	w0, #0x0, 0x50cf8 <_WeChatMain+0x3748c>
0x50cf0	20008052	mov	w0, #0x1                ; =1
0x50cf4	82000014	b	0x50efc <_WeChatMain+0x37690>
0x50cf8	e8f30132	mov	w8, #-0x55555556        ; =-1431655766
0x50cfc	e81f00b9	str	w8, [sp, #0x1c]
0x50d00	f7f301b2	mov	x23, #-0x5555555555555556 ; =-6148914691236517206
0x50d04	f70b00f9	str	x23, [sp, #0x10]
0x50d08	e80f00b9	str	w8, [sp, #0xc]
0x50d0c	a80240f9	ldr	x8, [x21]
0x50d10	081140f9	ldr	x8, [x8, #0x20]
0x50d14	e1730091	add	x1, sp, #0x1c
0x50d18	e2430091	add	x2, sp, #0x10
0x50d1c	e3330091	add	x3, sp, #0xc
0x50d20	e00315aa	mov	x0, x21
0x50d24	00013fd6	blr	x8
0x50d28	e11f40b9	ldr	w1, [sp, #0x1c]
0x50d2c	680240f9	ldr	x8, [x19]
0x50d30	083540f9	ldr	x8, [x8, #0x68]
0x50d34	e00313aa	mov	x0, x19
0x50d38	00013fd6	blr	x8
0x50d3c	f60300aa	mov	x22, x0
0x50d40	f70300f9	str	x23, [sp]
0x50d44	a80240f9	ldr	x8, [x21]
0x50d48	081540f9	ldr	x8, [x8, #0x28]
0x50d4c	e1030091	mov	x1, sp
0x50d50	e00315aa	mov	x0, x21
0x50d54	00013fd6	blr	x8
0x50d58	e80340f9	ldr	x8, [sp]
0x50d5c	c80208cb	sub	x8, x22, x8
0x50d60	1f000071	cmp	w0, #0x0
0x50d64	17119f9a	csel	x23, x8, xzr, ne
0x50d68	681240f9	ldr	x8, [x19, #0x20]
0x50d6c	082540a9	ldp	x8, x9, [x8]
0x50d70	280108cb	sub	x8, x9, x8
0x50d74	08fd4293	asr	x8, x8, #2
0x50d78	080500d1	sub	x8, x8, #0x1
0x50d7c	df0208eb	cmp	x22, x8
0x50d80	c20b0054	b.hs	0x50ef8 <_WeChatMain+0x3768c>
0x50d84	a80240f9	ldr	x8, [x21]
0x50d88	080d40f9	ldr	x8, [x8, #0x18]
0x50d8c	e00315aa	mov	x0, x21
0x50d90	00013fd6	blr	x8
0x50d94	688241d9	ldapur	x8, [x19, #0x18]
0x50d98	080400b5	cbnz	x8, 0x50e18 <_WeChatMain+0x375ac>
0x50d9c	a80240f9	ldr	x8, [x21]
0x50da0	080940f9	ldr	x8, [x8, #0x10]
0x50da4	e00315aa	mov	x0, x21
0x50da8	00013fd6	blr	x8
0x50dac	20030034	cbz	w0, 0x50e10 <_WeChatMain+0x375a4>
0x50db0	680a40f9	ldr	x8, [x19, #0x10]
0x50db4	e90f40b9	ldr	w9, [sp, #0xc]
0x50db8	9f020071	cmp	w20, #0x0
0x50dbc	2205895a	cneg	w2, w9, ne
0x50dc0	00510091	add	x0, x8, #0x14
0x50dc4	e10316aa	mov	x1, x22
0x50dc8	6ce1c195	bl	0x70c9378 <_SetWeixinCallbackFunc+0x22e1f7c>
0x50dcc	20020034	cbz	w0, 0x50e10 <_WeChatMain+0x375a4>
0x50dd0	688241d9	ldapur	x8, [x19, #0x18]
0x50dd4	e8f8ffb4	cbz	x8, 0x50cf0 <_WeChatMain+0x37484>
0x50dd8	680a40f9	ldr	x8, [x19, #0x10]
0x50ddc	00510091	add	x0, x8, #0x14
0x50de0	21008052	mov	w1, #0x1                ; =1
0x50de4	03ecff97	bl	0x4bdf0 <_WeChatMain+0x32584>
0x50de8	e80300aa	mov	x8, x0
0x50dec	20008052	mov	w0, #0x1                ; =1
0x50df0	1f414071	cmp	w8, #0x10, lsl #12      ; =0x10000
0x50df4	43080054	b.lo	0x50efc <_WeChatMain+0x37690>
0x50df8	097d1053	lsr	w9, w8, #16
0x50dfc	6a8241d9	ldapur	x10, [x19, #0x18]
0x50e00	083d0012	and	w8, w8, #0xffff
0x50e04	4849288b	add	x8, x10, w8, uxtw #2
0x50e08	080129b8	ldadd	w9, w8, [x8]
0x50e0c	3c000014	b	0x50efc <_WeChatMain+0x37690>
0x50e10	e00313aa	mov	x0, x19
0x50e14	ccfeff97	bl	0x50944 <_WeChatMain+0x370d8>
0x50e18	e91f40b9	ldr	w9, [sp, #0x1c]
0x50e1c	681240f9	ldr	x8, [x19, #0x20]
0x50e20	080140f9	ldr	x8, [x8]
0x50e24	0a7976b8	ldr	w10, [x8, x22, lsl #2]
0x50e28	3f010a6b	cmp	w9, w10
0x50e2c	61060054	b.ne	0x50ef8 <_WeChatMain+0x3768c>
0x50e30	e90b40f9	ldr	x9, [sp, #0x10]
0x50e34	0809168b	add	x8, x8, x22, lsl #2
0x50e38	080580b9	ldrsw	x8, [x8, #0x4]
0x50e3c	3f0108eb	cmp	x9, x8
0x50e40	c1050054	b.ne	0x50ef8 <_WeChatMain+0x3768c>
0x50e44	688241d9	ldapur	x8, [x19, #0x18]
0x50e48	0809168b	add	x8, x8, x22, lsl #2
0x50e4c	e90f40b9	ldr	w9, [sp, #0xc]
0x50e50	9f020071	cmp	w20, #0x0
0x50e54	2905895a	cneg	w9, w9, ne
0x50e58	080129b8	ldadd	w9, w8, [x8]
0x50e5c	a80240f9	ldr	x8, [x21]
0x50e60	080940f9	ldr	x8, [x8, #0x10]
0x50e64	e00315aa	mov	x0, x21
0x50e68	00013fd6	blr	x8
0x50e6c	20f40737	tbnz	w0, #0x0, 0x50cf0 <_WeChatMain+0x37484>
0x50e70	a80240f9	ldr	x8, [x21]
0x50e74	081140f9	ldr	x8, [x8, #0x20]
0x50e78	e1730091	add	x1, sp, #0x1c
0x50e7c	e2430091	add	x2, sp, #0x10
0x50e80	e3330091	add	x3, sp, #0xc
0x50e84	e00315aa	mov	x0, x21
0x50e88	00013fd6	blr	x8
0x50e8c	a80240f9	ldr	x8, [x21]
0x50e90	081540f9	ldr	x8, [x8, #0x28]
0x50e94	e1030091	mov	x1, sp
0x50e98	e00315aa	mov	x0, x21
0x50e9c	00013fd6	blr	x8
0x50ea0	80000034	cbz	w0, 0x50eb0 <_WeChatMain+0x37644>
0x50ea4	e80340f9	ldr	x8, [sp]
0x50ea8	1601178b	add	x22, x8, x23
0x50eac	07000014	b	0x50ec8 <_WeChatMain+0x3765c>
0x50eb0	e11f40b9	ldr	w1, [sp, #0x1c]
0x50eb4	680240f9	ldr	x8, [x19]
0x50eb8	083540f9	ldr	x8, [x8, #0x68]
0x50ebc	e00313aa	mov	x0, x19
0x50ec0	00013fd6	blr	x8
0x50ec4	f60300aa	mov	x22, x0
0x50ec8	681240f9	ldr	x8, [x19, #0x20]
0x50ecc	082540a9	ldp	x8, x9, [x8]
0x50ed0	280108cb	sub	x8, x9, x8
0x50ed4	08fd4293	asr	x8, x8, #2
0x50ed8	080500d1	sub	x8, x8, #0x1
0x50edc	df0208eb	cmp	x22, x8
0x50ee0	c2000054	b.hs	0x50ef8 <_WeChatMain+0x3768c>
0x50ee4	a80240f9	ldr	x8, [x21]
0x50ee8	080d40f9	ldr	x8, [x8, #0x18]
0x50eec	e00315aa	mov	x0, x21
0x50ef0	00013fd6	blr	x8
0x50ef4	c9ffff17	b	0x50e18 <_WeChatMain+0x375ac>
0x50ef8	00008052	mov	w0, #0x0                ; =0
0x50efc	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x50f00	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x50f04	f65743a9	ldp	x22, x21, [sp, #0x30]
0x50f08	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x50f0c	ff830191	add	sp, sp, #0x60
0x50f10	c0035fd6	ret
0x50f14	ff0302d1	sub	sp, sp, #0x80
0x50f18	fa6703a9	stp	x26, x25, [sp, #0x30]
0x50f1c	f85f04a9	stp	x24, x23, [sp, #0x40]
0x50f20	f65705a9	stp	x22, x21, [sp, #0x50]
0x50f24	f44f06a9	stp	x20, x19, [sp, #0x60]
0x50f28	fd7b07a9	stp	x29, x30, [sp, #0x70]
0x50f2c	fdc30191	add	x29, sp, #0x70
0x50f30	f30301aa	mov	x19, x1
0x50f34	f40300aa	mov	x20, x0
0x50f38	081040f9	ldr	x8, [x0, #0x20]
0x50f3c	082540a9	ldp	x8, x9, [x8]
0x50f40	280108cb	sub	x8, x9, x8
0x50f44	19fd4293	asr	x25, x8, #2
0x50f48	380700d1	sub	x24, x25, #0x1
0x50f4c	081005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50f50	094d5d39	ldrb	w9, [x8, #0x753]
0x50f54	69010037	tbnz	w9, #0x0, 0x50f80 <_WeChatMain+0x37714>
0x50f58	c92104d0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x50f5c	2025c13d	ldr	q0, [x9, #0x490]
0x50f60	091005d0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50f64	29011d91	add	x9, x9, #0x740
0x50f68	2001803d	str	q0, [x9]
0x50f6c	2aa68e52	mov	w10, #0x7531            ; =30001
0x50f70	2a210079	strh	w10, [x9, #0x10]
0x50f74	3f490039	strb	wzr, [x9, #0x12]
0x50f78	29008052	mov	w9, #0x1                ; =1
0x50f7c	094d1d39	strb	w9, [x8, #0x753]
0x50f80	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x50f84	e81300f9	str	x8, [sp, #0x20]
0x50f88	d72104d0	adrp	x23, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x50f8c	f7421391	add	x23, x23, #0x4d0
0x50f90	380500b5	cbnz	x24, 0x51034 <_WeChatMain+0x377c8>
0x50f94	000080d2	mov	x0, #0x0                ; =0
0x50f98	0e43ff97	bl	0x21bd0 <_WeChatMain+0x8364>
0x50f9c	f50300aa	mov	x21, x0
0x50fa0	20008052	mov	w0, #0x1                ; =1
0x50fa4	bc42ff97	bl	0x21a94 <_WeChatMain+0x8228>
0x50fa8	e30300aa	mov	x3, x0
0x50fac	011005d0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50fb0	21001d91	add	x1, x1, #0x740
0x50fb4	e0a30091	add	x0, sp, #0x28
0x50fb8	e20315aa	mov	x2, x21
0x50fbc	f844ff97	bl	0x2239c <_WeChatMain+0x8b30>
0x50fc0	e81740f9	ldr	x8, [sp, #0x28]
0x50fc4	e81300f9	str	x8, [sp, #0x20]
0x50fc8	680300b4	cbz	x8, 0x51034 <_WeChatMain+0x377c8>
0x50fcc	081005d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50fd0	09f15c39	ldrb	w9, [x8, #0x73c]
0x50fd4	09020037	tbnz	w9, #0x0, 0x51014 <_WeChatMain+0x377a8>
0x50fd8	090080d2	mov	x9, #0x0                ; =0
0x50fdc	0a1005d0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x50fe0	4a391b91	add	x10, x10, #0x6ce
0x50fe4	eb02098b	add	x11, x23, x9
0x50fe8	6b254139	ldrb	w11, [x11, #0x49]
0x50fec	2c0d4092	and	x12, x9, #0xf
0x50ff0	ec020c8b	add	x12, x23, x12
0x50ff4	8ce54039	ldrb	w12, [x12, #0x39]
0x50ff8	8b010b4a	eor	w11, w12, w11
0x50ffc	4b692938	strb	w11, [x10, x9]
0x51000	29050091	add	x9, x9, #0x1
0x51004	3fb901f1	cmp	x9, #0x6e
0x51008	e1feff54	b.ne	0x50fe4 <_WeChatMain+0x37778>
0x5100c	29008052	mov	w9, #0x1                ; =1
0x51010	09f11c39	strb	w9, [x8, #0x73c]
0x51014	001005b0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51018	00381b91	add	x0, x0, #0x6ce
0x5101c	e8630091	add	x8, sp, #0x18
0x51020	e2830091	add	x2, sp, #0x20
0x51024	a11c8052	mov	w1, #0xe5               ; =229
0x51028	ef41ff97	bl	0x217e4 <_WeChatMain+0x7f78>
0x5102c	e0630091	add	x0, sp, #0x18
0x51030	0f26ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x51034	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x51038	e81300f9	str	x8, [sp, #0x20]
0x5103c	881240f9	ldr	x8, [x20, #0x20]
0x51040	080140f9	ldr	x8, [x8]
0x51044	150140b9	ldr	w21, [x8]
0x51048	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5104c	09d95d39	ldrb	w9, [x8, #0x776]
0x51050	09020037	tbnz	w9, #0x0, 0x51090 <_WeChatMain+0x37824>
0x51054	090080d2	mov	x9, #0x0                ; =0
0x51058	0a1005b0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5105c	4a511d91	add	x10, x10, #0x754
0x51060	eb02098b	add	x11, x23, x9
0x51064	6ba94339	ldrb	w11, [x11, #0xea]
0x51068	2c0d4092	and	x12, x9, #0xf
0x5106c	ec020c8b	add	x12, x23, x12
0x51070	8c694339	ldrb	w12, [x12, #0xda]
0x51074	8b010b4a	eor	w11, w12, w11
0x51078	4b692938	strb	w11, [x10, x9]
0x5107c	29050091	add	x9, x9, #0x1
0x51080	3f8900f1	cmp	x9, #0x22
0x51084	e1feff54	b.ne	0x51060 <_WeChatMain+0x377f4>
0x51088	29008052	mov	w9, #0x1                ; =1
0x5108c	09d91d39	strb	w9, [x8, #0x776]
0x51090	bf02136b	cmp	w21, w19
0x51094	2d050054	b.le	0x51138 <_WeChatMain+0x378cc>
0x51098	e00313aa	mov	x0, x19
0x5109c	5642ff97	bl	0x219f4 <_WeChatMain+0x8188>
0x510a0	f60300aa	mov	x22, x0
0x510a4	e00315aa	mov	x0, x21
0x510a8	5342ff97	bl	0x219f4 <_WeChatMain+0x8188>
0x510ac	e30300aa	mov	x3, x0
0x510b0	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x510b4	21501d91	add	x1, x1, #0x754
0x510b8	e0a30091	add	x0, sp, #0x28
0x510bc	e20316aa	mov	x2, x22
0x510c0	b744ff97	bl	0x2239c <_WeChatMain+0x8b30>
0x510c4	e81740f9	ldr	x8, [sp, #0x28]
0x510c8	e81300f9	str	x8, [sp, #0x20]
0x510cc	680300b4	cbz	x8, 0x51138 <_WeChatMain+0x378cc>
0x510d0	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x510d4	09f15c39	ldrb	w9, [x8, #0x73c]
0x510d8	09020037	tbnz	w9, #0x0, 0x51118 <_WeChatMain+0x378ac>
0x510dc	090080d2	mov	x9, #0x0                ; =0
0x510e0	0a1005b0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x510e4	4a391b91	add	x10, x10, #0x6ce
0x510e8	eb02098b	add	x11, x23, x9
0x510ec	6b254139	ldrb	w11, [x11, #0x49]
0x510f0	2c0d4092	and	x12, x9, #0xf
0x510f4	ec020c8b	add	x12, x23, x12
0x510f8	8ce54039	ldrb	w12, [x12, #0x39]
0x510fc	8b010b4a	eor	w11, w12, w11
0x51100	4b692938	strb	w11, [x10, x9]
0x51104	29050091	add	x9, x9, #0x1
0x51108	3fb901f1	cmp	x9, #0x6e
0x5110c	e1feff54	b.ne	0x510e8 <_WeChatMain+0x3787c>
0x51110	29008052	mov	w9, #0x1                ; =1
0x51114	09f11c39	strb	w9, [x8, #0x73c]
0x51118	001005b0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5111c	00381b91	add	x0, x0, #0x6ce
0x51120	e8430091	add	x8, sp, #0x10
0x51124	e2830091	add	x2, sp, #0x20
0x51128	c11c8052	mov	w1, #0xe6               ; =230
0x5112c	ae41ff97	bl	0x217e4 <_WeChatMain+0x7f78>
0x51130	e0430091	add	x0, sp, #0x10
0x51134	ce25ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x51138	881240f9	ldr	x8, [x20, #0x20]
0x5113c	080140f9	ldr	x8, [x8]
0x51140	157978b8	ldr	w21, [x8, x24, lsl #2]
0x51144	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51148	098d5e39	ldrb	w9, [x8, #0x7a3]
0x5114c	09020037	tbnz	w9, #0x0, 0x5118c <_WeChatMain+0x37920>
0x51150	090080d2	mov	x9, #0x0                ; =0
0x51154	0a1005b0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51158	4add1d91	add	x10, x10, #0x777
0x5115c	eb02098b	add	x11, x23, x9
0x51160	6b714439	ldrb	w11, [x11, #0x11c]
0x51164	2c0d4092	and	x12, x9, #0xf
0x51168	ec020c8b	add	x12, x23, x12
0x5116c	8c314439	ldrb	w12, [x12, #0x10c]
0x51170	8b010b4a	eor	w11, w12, w11
0x51174	4b692938	strb	w11, [x10, x9]
0x51178	29050091	add	x9, x9, #0x1
0x5117c	3fb100f1	cmp	x9, #0x2c
0x51180	e1feff54	b.ne	0x5115c <_WeChatMain+0x378f0>
0x51184	29008052	mov	w9, #0x1                ; =1
0x51188	098d1e39	strb	w9, [x8, #0x7a3]
0x5118c	bf02136b	cmp	w21, w19
0x51190	2c050054	b.gt	0x51234 <_WeChatMain+0x379c8>
0x51194	e00313aa	mov	x0, x19
0x51198	1742ff97	bl	0x219f4 <_WeChatMain+0x8188>
0x5119c	f60300aa	mov	x22, x0
0x511a0	e00315aa	mov	x0, x21
0x511a4	1442ff97	bl	0x219f4 <_WeChatMain+0x8188>
0x511a8	e30300aa	mov	x3, x0
0x511ac	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x511b0	21dc1d91	add	x1, x1, #0x777
0x511b4	e0a30091	add	x0, sp, #0x28
0x511b8	e20316aa	mov	x2, x22
0x511bc	7844ff97	bl	0x2239c <_WeChatMain+0x8b30>
0x511c0	e81740f9	ldr	x8, [sp, #0x28]
0x511c4	e81700f9	str	x8, [sp, #0x28]
0x511c8	680300b4	cbz	x8, 0x51234 <_WeChatMain+0x379c8>
0x511cc	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x511d0	09f15c39	ldrb	w9, [x8, #0x73c]
0x511d4	09020037	tbnz	w9, #0x0, 0x51214 <_WeChatMain+0x379a8>
0x511d8	090080d2	mov	x9, #0x0                ; =0
0x511dc	0a1005b0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x511e0	4a391b91	add	x10, x10, #0x6ce
0x511e4	eb02098b	add	x11, x23, x9
0x511e8	6b254139	ldrb	w11, [x11, #0x49]
0x511ec	2c0d4092	and	x12, x9, #0xf
0x511f0	ec020c8b	add	x12, x23, x12
0x511f4	8ce54039	ldrb	w12, [x12, #0x39]
0x511f8	8b010b4a	eor	w11, w12, w11
0x511fc	4b692938	strb	w11, [x10, x9]
0x51200	29050091	add	x9, x9, #0x1
0x51204	3fb901f1	cmp	x9, #0x6e
0x51208	e1feff54	b.ne	0x511e4 <_WeChatMain+0x37978>
0x5120c	29008052	mov	w9, #0x1                ; =1
0x51210	09f11c39	strb	w9, [x8, #0x73c]
0x51214	001005b0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51218	00381b91	add	x0, x0, #0x6ce
0x5121c	e8230091	add	x8, sp, #0x8
0x51220	e2a30091	add	x2, sp, #0x28
0x51224	e11c8052	mov	w1, #0xe7               ; =231
0x51228	6f41ff97	bl	0x217e4 <_WeChatMain+0x7f78>
0x5122c	e0230091	add	x0, sp, #0x8
0x51230	8f25ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x51234	881240f9	ldr	x8, [x20, #0x20]
0x51238	290b00d1	sub	x9, x25, #0x2
0x5123c	080140f9	ldr	x8, [x8]
0x51240	0a7969b8	ldr	w10, [x8, x9, lsl #2]
0x51244	5f01096b	cmp	w10, w9
0x51248	e1000054	b.ne	0x51264 <_WeChatMain+0x379f8>
0x5124c	7f060071	cmp	w19, #0x1
0x51250	eb090054	b.lt	0x5138c <_WeChatMain+0x37b20>
0x51254	e803132a	mov	w8, w19
0x51258	5f01136b	cmp	w10, w19
0x5125c	34b1889a	csel	x20, x9, x8, lt
0x51260	4c000014	b	0x51390 <_WeChatMain+0x37b24>
0x51264	14ff41d3	lsr	x20, x24, #1
0x51268	1f0b00f1	cmp	x24, #0x2
0x5126c	43010054	b.lo	0x51294 <_WeChatMain+0x37a28>
0x51270	090080d2	mov	x9, #0x0                ; =0
0x51274	0a7974b8	ldr	w10, [x8, x20, lsl #2]
0x51278	5f01136b	cmp	w10, w19
0x5127c	29c1949a	csel	x9, x9, x20, gt
0x51280	98c2989a	csel	x24, x20, x24, gt
0x51284	0a0309cb	sub	x10, x24, x9
0x51288	34054a8b	add	x20, x9, x10, lsr #1
0x5128c	5f0500f1	cmp	x10, #0x1
0x51290	28ffff54	b.hi	0x51274 <_WeChatMain+0x37a08>
0x51294	0809148b	add	x8, x8, x20, lsl #2
0x51298	000540b9	ldr	w0, [x8, #0x4]
0x5129c	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x512a0	092d5f39	ldrb	w9, [x8, #0x7cb]
0x512a4	09020037	tbnz	w9, #0x0, 0x512e4 <_WeChatMain+0x37a78>
0x512a8	090080d2	mov	x9, #0x0                ; =0
0x512ac	0a1005b0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x512b0	4a911e91	add	x10, x10, #0x7a4
0x512b4	eb02098b	add	x11, x23, x9
0x512b8	6b614539	ldrb	w11, [x11, #0x158]
0x512bc	2c0d4092	and	x12, x9, #0xf
0x512c0	ec020c8b	add	x12, x23, x12
0x512c4	8c214539	ldrb	w12, [x12, #0x148]
0x512c8	8b010b4a	eor	w11, w12, w11
0x512cc	4b692938	strb	w11, [x10, x9]
0x512d0	29050091	add	x9, x9, #0x1
0x512d4	3f9d00f1	cmp	x9, #0x27
0x512d8	e1feff54	b.ne	0x512b4 <_WeChatMain+0x37a48>
0x512dc	29008052	mov	w9, #0x1                ; =1
0x512e0	092d1f39	strb	w9, [x8, #0x7cb]
0x512e4	1f00136b	cmp	w0, w19
0x512e8	4c050054	b.gt	0x51390 <_WeChatMain+0x37b24>
0x512ec	c241ff97	bl	0x219f4 <_WeChatMain+0x8188>
0x512f0	f50300aa	mov	x21, x0
0x512f4	e00313aa	mov	x0, x19
0x512f8	bf41ff97	bl	0x219f4 <_WeChatMain+0x8188>
0x512fc	e30300aa	mov	x3, x0
0x51300	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51304	21901e91	add	x1, x1, #0x7a4
0x51308	e0a30091	add	x0, sp, #0x28
0x5130c	e20315aa	mov	x2, x21
0x51310	2344ff97	bl	0x2239c <_WeChatMain+0x8b30>
0x51314	e81740f9	ldr	x8, [sp, #0x28]
0x51318	e81700f9	str	x8, [sp, #0x28]
0x5131c	a80300b4	cbz	x8, 0x51390 <_WeChatMain+0x37b24>
0x51320	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51324	09f15c39	ldrb	w9, [x8, #0x73c]
0x51328	09020037	tbnz	w9, #0x0, 0x51368 <_WeChatMain+0x37afc>
0x5132c	090080d2	mov	x9, #0x0                ; =0
0x51330	0a1005b0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51334	4a391b91	add	x10, x10, #0x6ce
0x51338	eb02098b	add	x11, x23, x9
0x5133c	6b254139	ldrb	w11, [x11, #0x49]
0x51340	2c0d4092	and	x12, x9, #0xf
0x51344	ec020c8b	add	x12, x23, x12
0x51348	8ce54039	ldrb	w12, [x12, #0x39]
0x5134c	8b010b4a	eor	w11, w12, w11
0x51350	4b692938	strb	w11, [x10, x9]
0x51354	29050091	add	x9, x9, #0x1
0x51358	3fb901f1	cmp	x9, #0x6e
0x5135c	e1feff54	b.ne	0x51338 <_WeChatMain+0x37acc>
0x51360	29008052	mov	w9, #0x1                ; =1
0x51364	09f11c39	strb	w9, [x8, #0x73c]
0x51368	001005b0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5136c	00381b91	add	x0, x0, #0x6ce
0x51370	e8030091	mov	x8, sp
0x51374	e2a30091	add	x2, sp, #0x28
0x51378	c1208052	mov	w1, #0x106              ; =262
0x5137c	1a41ff97	bl	0x217e4 <_WeChatMain+0x7f78>
0x51380	e0030091	mov	x0, sp
0x51384	3a25ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x51388	02000014	b	0x51390 <_WeChatMain+0x37b24>
0x5138c	140080d2	mov	x20, #0x0               ; =0
0x51390	e00314aa	mov	x0, x20
0x51394	fd7b47a9	ldp	x29, x30, [sp, #0x70]
0x51398	f44f46a9	ldp	x20, x19, [sp, #0x60]
0x5139c	f65745a9	ldp	x22, x21, [sp, #0x50]
0x513a0	f85f44a9	ldp	x24, x23, [sp, #0x40]
0x513a4	fa6743a9	ldp	x26, x25, [sp, #0x30]
0x513a8	ff030291	add	sp, sp, #0x80
0x513ac	c0035fd6	ret
0x513b0	ff0301d1	sub	sp, sp, #0x40
0x513b4	f65701a9	stp	x22, x21, [sp, #0x10]
0x513b8	f44f02a9	stp	x20, x19, [sp, #0x20]
0x513bc	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x513c0	fdc30091	add	x29, sp, #0x30
0x513c4	f40302aa	mov	x20, x2
0x513c8	f50301aa	mov	x21, x1
0x513cc	f30300aa	mov	x19, x0
0x513d0	00038052	mov	w0, #0x18               ; =24
0x513d4	17bbc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x513d8	ba67ff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x513dc	e00700f9	str	x0, [sp, #0x8]
0x513e0	e2230091	add	x2, sp, #0x8
0x513e4	e00313aa	mov	x0, x19
0x513e8	e10315aa	mov	x1, x21
0x513ec	e30314aa	mov	x3, x20
0x513f0	a4fcff97	bl	0x50680 <_WeChatMain+0x36e14>
0x513f4	e00740f9	ldr	x0, [sp, #0x8]
0x513f8	600000b4	cbz	x0, 0x51404 <_WeChatMain+0x37b98>
0x513fc	01038052	mov	w1, #0x18               ; =24
0x51400	03bbc395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x51404	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51408	08c11791	add	x8, x8, #0x5f0
0x5140c	680200f9	str	x8, [x19]
0x51410	7f7e03a9	stp	xzr, xzr, [x19, #0x30]
0x51414	7f1600f9	str	xzr, [x19, #0x28]
0x51418	e00313aa	mov	x0, x19
0x5141c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x51420	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x51424	f65741a9	ldp	x22, x21, [sp, #0x10]
0x51428	ff030191	add	sp, sp, #0x40
0x5142c	c0035fd6	ret
0x51430	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x51434	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x51438	fd430091	add	x29, sp, #0x10
0x5143c	f30300aa	mov	x19, x0
0x51440	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51444	08c11791	add	x8, x8, #0x5f0
0x51448	080000f9	str	x8, [x0]
0x5144c	001440f9	ldr	x0, [x0, #0x28]
0x51450	a00000b4	cbz	x0, 0x51464 <_WeChatMain+0x37bf8>
0x51454	601a00f9	str	x0, [x19, #0x30]
0x51458	681e40f9	ldr	x8, [x19, #0x38]
0x5145c	010100cb	sub	x1, x8, x0
0x51460	ebbac395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x51464	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51468	08811591	add	x8, x8, #0x560
0x5146c	680200f9	str	x8, [x19]
0x51470	601240f9	ldr	x0, [x19, #0x20]
0x51474	08745e92	and	x8, x0, #0xfffffffc00000000
0x51478	49fd04b0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x5147c	29013b91	add	x9, x9, #0xec0
0x51480	290540f9	ldr	x9, [x9, #0x8]
0x51484	1f0109eb	cmp	x8, x9
0x51488	41000054	b.ne	0x51490 <_WeChatMain+0x37c24>
0x5148c	8db9ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x51490	7f1200f9	str	xzr, [x19, #0x20]
0x51494	e00313aa	mov	x0, x19
0x51498	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5149c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x514a0	9beaff17	b	0x4bf0c <_WeChatMain+0x326a0>
0x514a4	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x514a8	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x514ac	fd430091	add	x29, sp, #0x10
0x514b0	f30300aa	mov	x19, x0
0x514b4	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x514b8	08c11791	add	x8, x8, #0x5f0
0x514bc	080000f9	str	x8, [x0]
0x514c0	001440f9	ldr	x0, [x0, #0x28]
0x514c4	a00000b4	cbz	x0, 0x514d8 <_WeChatMain+0x37c6c>
0x514c8	601a00f9	str	x0, [x19, #0x30]
0x514cc	681e40f9	ldr	x8, [x19, #0x38]
0x514d0	010100cb	sub	x1, x8, x0
0x514d4	cebac395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x514d8	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x514dc	08811591	add	x8, x8, #0x560
0x514e0	680200f9	str	x8, [x19]
0x514e4	601240f9	ldr	x0, [x19, #0x20]
0x514e8	08745e92	and	x8, x0, #0xfffffffc00000000
0x514ec	49fd04b0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x514f0	29013b91	add	x9, x9, #0xec0
0x514f4	290540f9	ldr	x9, [x9, #0x8]
0x514f8	1f0109eb	cmp	x8, x9
0x514fc	41000054	b.ne	0x51504 <_WeChatMain+0x37c98>
0x51500	70b9ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x51504	7f1200f9	str	xzr, [x19, #0x20]
0x51508	e00313aa	mov	x0, x19
0x5150c	80eaff97	bl	0x4bf0c <_WeChatMain+0x326a0>
0x51510	01088052	mov	w1, #0x40               ; =64
0x51514	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x51518	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x5151c	bcbac315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x51520	088041d9	ldapur	x8, [x0, #0x18]
0x51524	1f0100f1	cmp	x8, #0x0
0x51528	e0079f1a	cset	w0, ne
0x5152c	c0035fd6	ret
0x51530	ff8301d1	sub	sp, sp, #0x60
0x51534	f85f02a9	stp	x24, x23, [sp, #0x20]
0x51538	f65703a9	stp	x22, x21, [sp, #0x30]
0x5153c	f44f04a9	stp	x20, x19, [sp, #0x40]
0x51540	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x51544	fd430191	add	x29, sp, #0x50
0x51548	f30303aa	mov	x19, x3
0x5154c	f80302aa	mov	x24, x2
0x51550	f70301aa	mov	x23, x1
0x51554	f50300aa	mov	x21, x0
0x51558	f40308aa	mov	x20, x8
0x5155c	080040f9	ldr	x8, [x0]
0x51560	081140f9	ldr	x8, [x8, #0x20]
0x51564	00013fd6	blr	x8
0x51568	f60300aa	mov	x22, x0
0x5156c	9ffe00a9	stp	xzr, xzr, [x20, #0x8]
0x51570	9f0200f9	str	xzr, [x20]
0x51574	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51578	09c15f39	ldrb	w9, [x8, #0x7f0]
0x5157c	49020037	tbnz	w9, #0x0, 0x515c4 <_WeChatMain+0x37d58>
0x51580	090080d2	mov	x9, #0x0                ; =0
0x51584	ca2104b0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x51588	4a411391	add	x10, x10, #0x4d0
0x5158c	0b1005b0	adrp	x11, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51590	6b311f91	add	x11, x11, #0x7cc
0x51594	4c01098b	add	x12, x10, x9
0x51598	8c3d4639	ldrb	w12, [x12, #0x18f]
0x5159c	2d0d4092	and	x13, x9, #0xf
0x515a0	4d010d8b	add	x13, x10, x13
0x515a4	adfd4539	ldrb	w13, [x13, #0x17f]
0x515a8	ac010c4a	eor	w12, w13, w12
0x515ac	6c692938	strb	w12, [x11, x9]
0x515b0	29050091	add	x9, x9, #0x1
0x515b4	3f9100f1	cmp	x9, #0x24
0x515b8	e1feff54	b.ne	0x51594 <_WeChatMain+0x37d28>
0x515bc	29008052	mov	w9, #0x1                ; =1
0x515c0	09c11f39	strb	w9, [x8, #0x7f0]
0x515c4	f7db00a9	stp	x23, x22, [sp, #0x8]
0x515c8	f80300f9	str	x24, [sp]
0x515cc	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x515d0	21301f91	add	x1, x1, #0x7cc
0x515d4	e00314aa	mov	x0, x20
0x515d8	305b0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x515dc	76030034	cbz	w22, 0x51648 <_WeChatMain+0x37ddc>
0x515e0	a80a40f9	ldr	x8, [x21, #0x10]
0x515e4	080540f9	ldr	x8, [x8, #0x8]
0x515e8	0001229e	scvtf	s0, x8
0x515ec	c102221e	scvtf	s1, w22
0x515f0	0018211e	fdiv	s0, s0, s1
0x515f4	00c0221e	fcvt	d0, s0
0x515f8	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x515fc	09196039	ldrb	w9, [x8, #0x806]
0x51600	a9010037	tbnz	w9, #0x0, 0x51634 <_WeChatMain+0x37dc8>
0x51604	c92104b0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x51608	213942fd	ldr	d1, [x9, #0x470]
0x5160c	091005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51610	29e11f91	add	x9, x9, #0x7f8
0x51614	210100fd	str	d1, [x9]
0x51618	ca2104b0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5161c	413d42fd	ldr	d1, [x10, #0x478]
0x51620	210900bd	str	s1, [x9, #0x8]
0x51624	ca0c8052	mov	w10, #0x66              ; =102
0x51628	2a190079	strh	w10, [x9, #0xc]
0x5162c	29008052	mov	w9, #0x1                ; =1
0x51630	09192039	strb	w9, [x8, #0x806]
0x51634	e00300fd	str	d0, [sp]
0x51638	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5163c	21e01f91	add	x1, x1, #0x7f8
0x51640	e00314aa	mov	x0, x20
0x51644	155b0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x51648	f3010034	cbz	w19, 0x51684 <_WeChatMain+0x37e18>
0x5164c	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51650	09816039	ldrb	w9, [x8, #0x820]
0x51654	e9000037	tbnz	w9, #0x0, 0x51670 <_WeChatMain+0x37e04>
0x51658	c92104b0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5165c	2025c03d	ldr	q0, [x9, #0x90]
0x51660	091005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51664	2005823d	str	q0, [x9, #0x810]
0x51668	29008052	mov	w9, #0x1                ; =1
0x5166c	09812039	strb	w9, [x8, #0x820]
0x51670	f30300f9	str	x19, [sp]
0x51674	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51678	21402091	add	x1, x1, #0x810
0x5167c	e00314aa	mov	x0, x20
0x51680	065b0094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x51684	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x51688	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x5168c	f65743a9	ldp	x22, x21, [sp, #0x30]
0x51690	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x51694	ff830191	add	sp, sp, #0x60
0x51698	c0035fd6	ret
0x5169c	ff0303d1	sub	sp, sp, #0xc0
0x516a0	eb2b046d	stp	d11, d10, [sp, #0x40]
0x516a4	e923056d	stp	d9, d8, [sp, #0x50]
0x516a8	fc6f06a9	stp	x28, x27, [sp, #0x60]
0x516ac	fa6707a9	stp	x26, x25, [sp, #0x70]
0x516b0	f85f08a9	stp	x24, x23, [sp, #0x80]
0x516b4	f65709a9	stp	x22, x21, [sp, #0x90]
0x516b8	f44f0aa9	stp	x20, x19, [sp, #0xa0]
0x516bc	fd7b0ba9	stp	x29, x30, [sp, #0xb0]
0x516c0	fdc30291	add	x29, sp, #0xb0
0x516c4	f30300aa	mov	x19, x0
0x516c8	f40308aa	mov	x20, x8
0x516cc	080040f9	ldr	x8, [x0]
0x516d0	081140f9	ldr	x8, [x8, #0x20]
0x516d4	00013fd6	blr	x8
0x516d8	f50300aa	mov	x21, x0
0x516dc	681240f9	ldr	x8, [x19, #0x20]
0x516e0	0a2540a9	ldp	x10, x9, [x8]
0x516e4	29010acb	sub	x9, x9, x10
0x516e8	3f1100f1	cmp	x9, #0x4
0x516ec	81000054	b.ne	0x516fc <_WeChatMain+0x37e90>
0x516f0	09106e1e	fmov	d9, #1.00000000
0x516f4	5b008052	mov	w27, #0x2               ; =2
0x516f8	63000014	b	0x51884 <_WeChatMain+0x38018>
0x516fc	180080d2	mov	x24, #0x0               ; =0
0x51700	16008052	mov	w22, #0x0               ; =0
0x51704	37008052	mov	w23, #0x1               ; =1
0x51708	10000014	b	0x51748 <_WeChatMain+0x37edc>
0x5170c	e8060051	sub	w8, w23, #0x1
0x51710	097c1053	lsr	w9, w0, #16
0x51714	1f21206b	cmp	w8, w0, uxth
0x51718	28019f1a	csel	w8, w9, wzr, eq
0x5171c	1f01166b	cmp	w8, w22
0x51720	16c1961a	csel	w22, w8, w22, gt
0x51724	f803172a	mov	w24, w23
0x51728	681240f9	ldr	x8, [x19, #0x20]
0x5172c	0a2540a9	ldp	x10, x9, [x8]
0x51730	29010acb	sub	x9, x9, x10
0x51734	2afd4293	asr	x10, x9, #2
0x51738	4a0500d1	sub	x10, x10, #0x1
0x5173c	f7060011	add	w23, w23, #0x1
0x51740	5f0118eb	cmp	x10, x24
0x51744	49020054	b.ls	0x5178c <_WeChatMain+0x37f20>
0x51748	680a40f9	ldr	x8, [x19, #0x10]
0x5174c	00510091	add	x0, x8, #0x14
0x51750	a4e9ff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x51754	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x51758	a2fdff54	b.hs	0x5170c <_WeChatMain+0x37ea0>
0x5175c	688241d9	ldapur	x8, [x19, #0x18]
0x51760	c80000b5	cbnz	x8, 0x51778 <_WeChatMain+0x37f0c>
0x51764	680240f9	ldr	x8, [x19]
0x51768	083940f9	ldr	x8, [x8, #0x70]
0x5176c	e00313aa	mov	x0, x19
0x51770	00013fd6	blr	x8
0x51774	80000034	cbz	w0, 0x51784 <_WeChatMain+0x37f18>
0x51778	688241d9	ldapur	x8, [x19, #0x18]
0x5177c	087978b8	ldr	w8, [x8, x24, lsl #2]
0x51780	e7ffff17	b	0x5171c <_WeChatMain+0x37eb0>
0x51784	08008052	mov	w8, #0x0                ; =0
0x51788	e5ffff17	b	0x5171c <_WeChatMain+0x37eb0>
0x5178c	c002631e	ucvtf	d0, w22
0x51790	4a0ae8d2	mov	x10, #0x4052000000000000 ; =4634766966517661696
0x51794	4101679e	fmov	d1, x10
0x51798	2018601e	fdiv	d0, d1, d0
0x5179c	df220171	cmp	w22, #0x48
0x517a0	01106e1e	fmov	d1, #1.00000000
0x517a4	098c611e	fcsel	d9, d0, d1, hi
0x517a8	3f1100f1	cmp	x9, #0x4
0x517ac	61000054	b.ne	0x517b8 <_WeChatMain+0x37f4c>
0x517b0	5b008052	mov	w27, #0x2               ; =2
0x517b4	34000014	b	0x51884 <_WeChatMain+0x38018>
0x517b8	180080d2	mov	x24, #0x0               ; =0
0x517bc	36008052	mov	w22, #0x1               ; =1
0x517c0	37008052	mov	w23, #0x1               ; =1
0x517c4	11000014	b	0x51808 <_WeChatMain+0x37f9c>
0x517c8	e0a342a9	ldp	x0, x8, [sp, #0x28]
0x517cc	18050091	add	x24, x8, #0x1
0x517d0	e81f40f9	ldr	x8, [sp, #0x38]
0x517d4	01f94092	and	x1, x8, #0x7fffffffffffffff
0x517d8	0dbac395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x517dc	1f0317eb	cmp	x24, x23
0x517e0	1783979a	csel	x23, x24, x23, hi
0x517e4	f803162a	mov	w24, w22
0x517e8	681240f9	ldr	x8, [x19, #0x20]
0x517ec	0a2540a9	ldp	x10, x9, [x8]
0x517f0	29010acb	sub	x9, x9, x10
0x517f4	29fd4293	asr	x9, x9, #2
0x517f8	290500d1	sub	x9, x9, #0x1
0x517fc	d6060011	add	w22, w22, #0x1
0x51800	3f0118eb	cmp	x9, x24
0x51804	e9030054	b.ls	0x51880 <_WeChatMain+0x38014>
0x51808	680a40f9	ldr	x8, [x19, #0x10]
0x5180c	00510091	add	x0, x8, #0x14
0x51810	74e9ff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x51814	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x51818	82010054	b.hs	0x51848 <_WeChatMain+0x37fdc>
0x5181c	688241d9	ldapur	x8, [x19, #0x18]
0x51820	c80000b5	cbnz	x8, 0x51838 <_WeChatMain+0x37fcc>
0x51824	680240f9	ldr	x8, [x19]
0x51828	083940f9	ldr	x8, [x8, #0x70]
0x5182c	e00313aa	mov	x0, x19
0x51830	00013fd6	blr	x8
0x51834	80fdff34	cbz	w0, 0x517e4 <_WeChatMain+0x37f78>
0x51838	688241d9	ldapur	x8, [x19, #0x18]
0x5183c	087978b8	ldr	w8, [x8, x24, lsl #2]
0x51840	a8000035	cbnz	w8, 0x51854 <_WeChatMain+0x37fe8>
0x51844	e8ffff17	b	0x517e4 <_WeChatMain+0x37f78>
0x51848	c8060051	sub	w8, w22, #0x1
0x5184c	1f21206b	cmp	w8, w0, uxth
0x51850	a1fcff54	b.ne	0x517e4 <_WeChatMain+0x37f78>
0x51854	681240f9	ldr	x8, [x19, #0x20]
0x51858	080140f9	ldr	x8, [x8]
0x5185c	017978b8	ldr	w1, [x8, x24, lsl #2]
0x51860	e8a30091	add	x8, sp, #0x28
0x51864	e00313aa	mov	x0, x19
0x51868	24edff97	bl	0x4ccf8 <_WeChatMain+0x3348c>
0x5186c	e8ffc039	ldrsb	w8, [sp, #0x3f]
0x51870	c8faff37	tbnz	w8, #0x1f, 0x517c8 <_WeChatMain+0x37f5c>
0x51874	081d4092	and	x8, x8, #0xff
0x51878	18050091	add	x24, x8, #0x1
0x5187c	d8ffff17	b	0x517dc <_WeChatMain+0x37f70>
0x51880	fb060091	add	x27, x23, #0x1
0x51884	9f7e00a9	stp	xzr, xzr, [x20]
0x51888	9f0a00f9	str	xzr, [x20, #0x10]
0x5188c	082540a9	ldp	x8, x9, [x8]
0x51890	280108cb	sub	x8, x9, x8
0x51894	1f1100f1	cmp	x8, #0x4
0x51898	61010054	b.ne	0x518c4 <_WeChatMain+0x38058>
0x5189c	fd7b4ba9	ldp	x29, x30, [sp, #0xb0]
0x518a0	f44f4aa9	ldp	x20, x19, [sp, #0xa0]
0x518a4	f65749a9	ldp	x22, x21, [sp, #0x90]
0x518a8	f85f48a9	ldp	x24, x23, [sp, #0x80]
0x518ac	fa6747a9	ldp	x26, x25, [sp, #0x70]
0x518b0	fc6f46a9	ldp	x28, x27, [sp, #0x60]
0x518b4	e923456d	ldp	d9, d8, [sp, #0x50]
0x518b8	eb2b446d	ldp	d11, d10, [sp, #0x40]
0x518bc	ff030391	add	sp, sp, #0xc0
0x518c0	c0035fd6	ret
0x518c4	190080d2	mov	x25, #0x0               ; =0
0x518c8	17008052	mov	w23, #0x0               ; =0
0x518cc	1c0080d2	mov	x28, #0x0               ; =0
0x518d0	b57e4093	sxtw	x21, w21
0x518d4	c82104b0	adrp	x8, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x518d8	004542fd	ldr	d0, [x8, #0x488]
0x518dc	e007803d	str	q0, [sp, #0x10]
0x518e0	1a1005b0	adrp	x26, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x518e4	5aaf2091	add	x26, x26, #0x82b
0x518e8	c82104b0	adrp	x8, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x518ec	0a4142fd	ldr	d10, [x8, #0x480]
0x518f0	0b000014	b	0x5191c <_WeChatMain+0x380b0>
0x518f4	b50218cb	sub	x21, x21, x24
0x518f8	d9060011	add	w25, w22, #0x1
0x518fc	681240f9	ldr	x8, [x19, #0x20]
0x51900	082540a9	ldp	x8, x9, [x8]
0x51904	280108cb	sub	x8, x9, x8
0x51908	08fd4293	asr	x8, x8, #2
0x5190c	080500d1	sub	x8, x8, #0x1
0x51910	f70319aa	mov	x23, x25
0x51914	1f0119eb	cmp	x8, x25
0x51918	29fcff54	b.ls	0x5189c <_WeChatMain+0x38030>
0x5191c	680a40f9	ldr	x8, [x19, #0x10]
0x51920	00510091	add	x0, x8, #0x14
0x51924	2fe9ff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x51928	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x5192c	62010054	b.hs	0x51958 <_WeChatMain+0x380ec>
0x51930	688241d9	ldapur	x8, [x19, #0x18]
0x51934	c80000b5	cbnz	x8, 0x5194c <_WeChatMain+0x380e0>
0x51938	680240f9	ldr	x8, [x19]
0x5193c	083940f9	ldr	x8, [x8, #0x70]
0x51940	e00313aa	mov	x0, x19
0x51944	00013fd6	blr	x8
0x51948	400e0034	cbz	w0, 0x51b10 <_WeChatMain+0x382a4>
0x5194c	688241d9	ldapur	x8, [x19, #0x18]
0x51950	167979b8	ldr	w22, [x8, x25, lsl #2]
0x51954	04000014	b	0x51964 <_WeChatMain+0x380f8>
0x51958	087c1053	lsr	w8, w0, #16
0x5195c	ff22206b	cmp	w23, w0, uxth
0x51960	16019f1a	csel	w22, w8, wzr, eq
0x51964	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x51968	e82303a9	stp	x8, x8, [sp, #0x30]
0x5196c	e81700f9	str	x8, [sp, #0x28]
0x51970	681240f9	ldr	x8, [x19, #0x20]
0x51974	080140f9	ldr	x8, [x8]
0x51978	017979b8	ldr	w1, [x8, x25, lsl #2]
0x5197c	e8a30091	add	x8, sp, #0x28
0x51980	e00313aa	mov	x0, x19
0x51984	ddecff97	bl	0x4ccf8 <_WeChatMain+0x3348c>
0x51988	e8ff4039	ldrb	w8, [sp, #0x3f]
0x5198c	091d0013	sxtb	w9, w8
0x51990	eaaf42a9	ldp	x10, x11, [sp, #0x28]
0x51994	3f010071	cmp	w9, #0x0
0x51998	e9a30091	add	x9, sp, #0x28
0x5199c	47b1899a	csel	x7, x10, x9, lt
0x519a0	66b1889a	csel	x6, x11, x8, lt
0x519a4	895e4039	ldrb	w9, [x20, #0x17]
0x519a8	281d0013	sxtb	w8, w9
0x519ac	8baa40a9	ldp	x11, x10, [x20, #0x8]
0x519b0	4af94092	and	x10, x10, #0x7fffffffffffffff
0x519b4	4a0500d1	sub	x10, x10, #0x1
0x519b8	1f010071	cmp	w8, #0x0
0x519bc	cc028052	mov	w12, #0x16              ; =22
0x519c0	41b18c9a	csel	x1, x10, x12, lt
0x519c4	78b1899a	csel	x24, x11, x9, lt
0x519c8	290018cb	sub	x9, x1, x24
0x519cc	3f0106eb	cmp	x9, x6
0x519d0	22010054	b.hs	0x519f4 <_WeChatMain+0x38188>
0x519d4	0803068b	add	x8, x24, x6
0x519d8	020101cb	sub	x2, x8, x1
0x519dc	e00314aa	mov	x0, x20
0x519e0	e30318aa	mov	x3, x24
0x519e4	e40318aa	mov	x4, x24
0x519e8	050080d2	mov	x5, #0x0                ; =0
0x519ec	72b7c395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x519f0	1a000014	b	0x51a58 <_WeChatMain+0x381ec>
0x519f4	260300b4	cbz	x6, 0x51a58 <_WeChatMain+0x381ec>
0x519f8	f61300f9	str	x22, [sp, #0x20]
0x519fc	f60315aa	mov	x22, x21
0x51a00	f5031caa	mov	x21, x28
0x51a04	890240f9	ldr	x9, [x20]
0x51a08	1f010071	cmp	w8, #0x0
0x51a0c	3ab1949a	csel	x26, x9, x20, lt
0x51a10	4003188b	add	x0, x26, x24
0x51a14	e10307aa	mov	x1, x7
0x51a18	e20306aa	mov	x2, x6
0x51a1c	fc0306aa	mov	x28, x6
0x51a20	1dbdc395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x51a24	08031c8b	add	x8, x24, x28
0x51a28	895ec039	ldrsb	w9, [x20, #0x17]
0x51a2c	8900f837	tbnz	w9, #0x1f, 0x51a3c <_WeChatMain+0x381d0>
0x51a30	09190012	and	w9, w8, #0x7f
0x51a34	895e0039	strb	w9, [x20, #0x17]
0x51a38	02000014	b	0x51a40 <_WeChatMain+0x381d4>
0x51a3c	880600f9	str	x8, [x20, #0x8]
0x51a40	5f6b2838	strb	wzr, [x26, x8]
0x51a44	fc0315aa	mov	x28, x21
0x51a48	f50316aa	mov	x21, x22
0x51a4c	1a1005b0	adrp	x26, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51a50	5aaf2091	add	x26, x26, #0x82b
0x51a54	f61340f9	ldr	x22, [sp, #0x20]
0x51a58	e8ff4039	ldrb	w8, [sp, #0x3f]
0x51a5c	091d0013	sxtb	w9, w8
0x51a60	ea1b40f9	ldr	x10, [sp, #0x30]
0x51a64	3f010071	cmp	w9, #0x0
0x51a68	48b1889a	csel	x8, x10, x8, lt
0x51a6c	1f011beb	cmp	x8, x27
0x51a70	c2010054	b.hs	0x51aa8 <_WeChatMain+0x3823c>
0x51a74	180080d2	mov	x24, #0x0               ; =0
0x51a78	e00314aa	mov	x0, x20
0x51a7c	01048052	mov	w1, #0x20               ; =32
0x51a80	8cb7c395	bl	0x713f8b0 <_wxam_enc_uninit_10+0x713f8b0>
0x51a84	18070091	add	x24, x24, #0x1
0x51a88	e8ff4039	ldrb	w8, [sp, #0x3f]
0x51a8c	091d0013	sxtb	w9, w8
0x51a90	ea1b40f9	ldr	x10, [sp, #0x30]
0x51a94	3f010071	cmp	w9, #0x0
0x51a98	48b1889a	csel	x8, x10, x8, lt
0x51a9c	0801188b	add	x8, x8, x24
0x51aa0	1f011beb	cmp	x8, x27
0x51aa4	a3feff54	b.lo	0x51a78 <_WeChatMain+0x3820c>
0x51aa8	d87e4093	sxtw	x24, w22
0x51aac	b8030035	cbnz	w24, 0x51b20 <_WeChatMain+0x382b4>
0x51ab0	681240f9	ldr	x8, [x19, #0x20]
0x51ab4	082540a9	ldp	x8, x9, [x8]
0x51ab8	280108cb	sub	x8, x9, x8
0x51abc	08fd4293	asr	x8, x8, #2
0x51ac0	080900d1	sub	x8, x8, #0x2
0x51ac4	1f0119eb	cmp	x8, x25
0x51ac8	c9020054	b.ls	0x51b20 <_WeChatMain+0x382b4>
0x51acc	f6060011	add	w22, w23, #0x1
0x51ad0	680a40f9	ldr	x8, [x19, #0x10]
0x51ad4	00510091	add	x0, x8, #0x14
0x51ad8	c2e8ff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x51adc	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x51ae0	c2010054	b.hs	0x51b18 <_WeChatMain+0x382ac>
0x51ae4	688241d9	ldapur	x8, [x19, #0x18]
0x51ae8	c80000b5	cbnz	x8, 0x51b00 <_WeChatMain+0x38294>
0x51aec	680240f9	ldr	x8, [x19]
0x51af0	083940f9	ldr	x8, [x8, #0x70]
0x51af4	e00313aa	mov	x0, x19
0x51af8	00013fd6	blr	x8
0x51afc	200c0034	cbz	w0, 0x51c80 <_WeChatMain+0x38414>
0x51b00	688241d9	ldapur	x8, [x19, #0x18]
0x51b04	087976b8	ldr	w8, [x8, x22, lsl #2]
0x51b08	c8000035	cbnz	w8, 0x51b20 <_WeChatMain+0x382b4>
0x51b0c	5d000014	b	0x51c80 <_WeChatMain+0x38414>
0x51b10	16008052	mov	w22, #0x0               ; =0
0x51b14	94ffff17	b	0x51964 <_WeChatMain+0x380f8>
0x51b18	df22206b	cmp	w22, w0, uxth
0x51b1c	210b0054	b.ne	0x51c80 <_WeChatMain+0x38414>
0x51b20	0003621e	scvtf	d0, w24
0x51b24	2009601e	fmul	d0, d9, d0
0x51b28	0800641e	fcvtas	w8, d0
0x51b2c	0001621e	scvtf	d0, w8
0x51b30	e00313aa	mov	x0, x19
0x51b34	01098052	mov	w1, #0x48               ; =72
0x51b38	e20314aa	mov	x2, x20
0x51b3c	83ecff97	bl	0x4cd48 <_WeChatMain+0x334dc>
0x51b40	8803158b	add	x8, x28, x21
0x51b44	0001629e	scvtf	d0, x8
0x51b48	280be8d2	mov	x8, #0x4059000000000000 ; =4636737291354636288
0x51b4c	0101679e	fmov	d1, x8
0x51b50	0818611e	fdiv	d8, d0, d1
0x51b54	e00313aa	mov	x0, x19
0x51b58	e10318aa	mov	x1, x24
0x51b5c	0041601e	fmov	d0, d8
0x51b60	e20314aa	mov	x2, x20
0x51b64	42edff97	bl	0x4d06c <_WeChatMain+0x33800>
0x51b68	97020034	cbz	w23, 0x51bb8 <_WeChatMain+0x3834c>
0x51b6c	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51b70	08ed6039	ldrb	w8, [x8, #0x83b]
0x51b74	48010037	tbnz	w8, #0x0, 0x51b9c <_WeChatMain+0x38330>
0x51b78	091005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51b7c	29c12091	add	x9, x9, #0x830
0x51b80	2a0100fd	str	d10, [x9]
0x51b84	a8a48f52	mov	w8, #0x7d25             ; =32037
0x51b88	28110079	strh	w8, [x9, #0x8]
0x51b8c	3f290039	strb	wzr, [x9, #0xa]
0x51b90	28008052	mov	w8, #0x1                ; =1
0x51b94	091005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51b98	28ed2039	strb	w8, [x9, #0x83b]
0x51b9c	8003629e	scvtf	d0, x28
0x51ba0	0018681e	fdiv	d0, d0, d8
0x51ba4	e00300fd	str	d0, [sp]
0x51ba8	e00314aa	mov	x0, x20
0x51bac	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51bb0	21c02091	add	x1, x1, #0x830
0x51bb4	b9590094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x51bb8	f51300f9	str	x21, [sp, #0x20]
0x51bbc	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51bc0	08b56039	ldrb	w8, [x8, #0x82d]
0x51bc4	c8000037	tbnz	w8, #0x0, 0x51bdc <_WeChatMain+0x38370>
0x51bc8	48018052	mov	w8, #0xa                ; =10
0x51bcc	48030079	strh	w8, [x26]
0x51bd0	28008052	mov	w8, #0x1                ; =1
0x51bd4	091005b0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51bd8	28b52039	strb	w8, [x9, #0x82d]
0x51bdc	9503188b	add	x21, x28, x24
0x51be0	e0031aaa	mov	x0, x26
0x51be4	85bfc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x51be8	f90300aa	mov	x25, x0
0x51bec	895e4039	ldrb	w9, [x20, #0x17]
0x51bf0	281d0013	sxtb	w8, w9
0x51bf4	8baa40a9	ldp	x11, x10, [x20, #0x8]
0x51bf8	4af94092	and	x10, x10, #0x7fffffffffffffff
0x51bfc	4a0500d1	sub	x10, x10, #0x1
0x51c00	1f010071	cmp	w8, #0x0
0x51c04	cc028052	mov	w12, #0x16              ; =22
0x51c08	41b18c9a	csel	x1, x10, x12, lt
0x51c0c	fc031aaa	mov	x28, x26
0x51c10	7ab1899a	csel	x26, x11, x9, lt
0x51c14	29001acb	sub	x9, x1, x26
0x51c18	3f0100eb	cmp	x9, x0
0x51c1c	020a0054	b.hs	0x51d5c <_WeChatMain+0x384f0>
0x51c20	4803198b	add	x8, x26, x25
0x51c24	020101cb	sub	x2, x8, x1
0x51c28	e00314aa	mov	x0, x20
0x51c2c	e3031aaa	mov	x3, x26
0x51c30	e4031aaa	mov	x4, x26
0x51c34	050080d2	mov	x5, #0x0                ; =0
0x51c38	e60319aa	mov	x6, x25
0x51c3c	e7031caa	mov	x7, x28
0x51c40	ddb6c395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x51c44	f60317aa	mov	x22, x23
0x51c48	fa031caa	mov	x26, x28
0x51c4c	57000014	b	0x51da8 <_WeChatMain+0x3853c>
0x51c50	688241d9	ldapur	x8, [x19, #0x18]
0x51c54	a80000b4	cbz	x8, 0x51c68 <_WeChatMain+0x383fc>
0x51c58	688241d9	ldapur	x8, [x19, #0x18]
0x51c5c	085977b8	ldr	w8, [x8, w23, uxtw #2]
0x51c60	08010034	cbz	w8, 0x51c80 <_WeChatMain+0x38414>
0x51c64	19000014	b	0x51cc8 <_WeChatMain+0x3845c>
0x51c68	680240f9	ldr	x8, [x19]
0x51c6c	083940f9	ldr	x8, [x8, #0x70]
0x51c70	e00313aa	mov	x0, x19
0x51c74	00013fd6	blr	x8
0x51c78	00ffff35	cbnz	w0, 0x51c58 <_WeChatMain+0x383ec>
0x51c7c	11000014	b	0x51cc0 <_WeChatMain+0x38454>
0x51c80	f60317aa	mov	x22, x23
0x51c84	681240f9	ldr	x8, [x19, #0x20]
0x51c88	082540a9	ldp	x8, x9, [x8]
0x51c8c	280108cb	sub	x8, x9, x8
0x51c90	08fd4293	asr	x8, x8, #2
0x51c94	080900d1	sub	x8, x8, #0x2
0x51c98	1f4137eb	cmp	x8, w23, uxtw
0x51c9c	69010054	b.ls	0x51cc8 <_WeChatMain+0x3845c>
0x51ca0	d7060011	add	w23, w22, #0x1
0x51ca4	680a40f9	ldr	x8, [x19, #0x10]
0x51ca8	00510091	add	x0, x8, #0x14
0x51cac	4de8ff97	bl	0x4bde0 <_WeChatMain+0x32574>
0x51cb0	1f404071	cmp	w0, #0x10, lsl #12      ; =0x10000
0x51cb4	e3fcff54	b.lo	0x51c50 <_WeChatMain+0x383e4>
0x51cb8	ff22206b	cmp	w23, w0, uxth
0x51cbc	60000054	b.eq	0x51cc8 <_WeChatMain+0x3845c>
0x51cc0	08008052	mov	w8, #0x0                ; =0
0x51cc4	e8fdff34	cbz	w8, 0x51c80 <_WeChatMain+0x38414>
0x51cc8	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51ccc	08a96039	ldrb	w8, [x8, #0x82a]
0x51cd0	171005b0	adrp	x23, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51cd4	f7922091	add	x23, x23, #0x824
0x51cd8	08010037	tbnz	w8, #0x0, 0x51cf8 <_WeChatMain+0x3848c>
0x51cdc	e007c03d	ldr	q0, [sp, #0x10]
0x51ce0	e00200bd	str	s0, [x23]
0x51ce4	48018052	mov	w8, #0xa                ; =10
0x51ce8	e80a0079	strh	w8, [x23, #0x4]
0x51cec	081005b0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51cf0	29008052	mov	w9, #0x1                ; =1
0x51cf4	09a92039	strb	w9, [x8, #0x82a]
0x51cf8	e00317aa	mov	x0, x23
0x51cfc	3fbfc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x51d00	f90300aa	mov	x25, x0
0x51d04	895e4039	ldrb	w9, [x20, #0x17]
0x51d08	281d0013	sxtb	w8, w9
0x51d0c	8baa40a9	ldp	x11, x10, [x20, #0x8]
0x51d10	4af94092	and	x10, x10, #0x7fffffffffffffff
0x51d14	4a0500d1	sub	x10, x10, #0x1
0x51d18	1f010071	cmp	w8, #0x0
0x51d1c	cc028052	mov	w12, #0x16              ; =22
0x51d20	41b18c9a	csel	x1, x10, x12, lt
0x51d24	7ab1899a	csel	x26, x11, x9, lt
0x51d28	29001acb	sub	x9, x1, x26
0x51d2c	3f0100eb	cmp	x9, x0
0x51d30	02060054	b.hs	0x51df0 <_WeChatMain+0x38584>
0x51d34	4803198b	add	x8, x26, x25
0x51d38	020101cb	sub	x2, x8, x1
0x51d3c	e00314aa	mov	x0, x20
0x51d40	e3031aaa	mov	x3, x26
0x51d44	e4031aaa	mov	x4, x26
0x51d48	050080d2	mov	x5, #0x0                ; =0
0x51d4c	e60319aa	mov	x6, x25
0x51d50	e70317aa	mov	x7, x23
0x51d54	98b6c395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x51d58	1d000014	b	0x51dcc <_WeChatMain+0x38560>
0x51d5c	190200b4	cbz	x25, 0x51d9c <_WeChatMain+0x38530>
0x51d60	890240f9	ldr	x9, [x20]
0x51d64	1f010071	cmp	w8, #0x0
0x51d68	36b1949a	csel	x22, x9, x20, lt
0x51d6c	c0021a8b	add	x0, x22, x26
0x51d70	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51d74	21ac2091	add	x1, x1, #0x82b
0x51d78	e20319aa	mov	x2, x25
0x51d7c	46bcc395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x51d80	4803198b	add	x8, x26, x25
0x51d84	895ec039	ldrsb	w9, [x20, #0x17]
0x51d88	fc0315aa	mov	x28, x21
0x51d8c	8901f837	tbnz	w9, #0x1f, 0x51dbc <_WeChatMain+0x38550>
0x51d90	09190012	and	w9, w8, #0x7f
0x51d94	895e0039	strb	w9, [x20, #0x17]
0x51d98	0a000014	b	0x51dc0 <_WeChatMain+0x38554>
0x51d9c	f60317aa	mov	x22, x23
0x51da0	1a1005b0	adrp	x26, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51da4	5aaf2091	add	x26, x26, #0x82b
0x51da8	fc0315aa	mov	x28, x21
0x51dac	f51340f9	ldr	x21, [sp, #0x20]
0x51db0	e8ffc039	ldrsb	w8, [sp, #0x3f]
0x51db4	08daff36	tbz	w8, #0x1f, 0x518f4 <_WeChatMain+0x38088>
0x51db8	09000014	b	0x51ddc <_WeChatMain+0x38570>
0x51dbc	880600f9	str	x8, [x20, #0x8]
0x51dc0	f51340f9	ldr	x21, [sp, #0x20]
0x51dc4	df6a2838	strb	wzr, [x22, x8]
0x51dc8	f60317aa	mov	x22, x23
0x51dcc	1a1005b0	adrp	x26, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51dd0	5aaf2091	add	x26, x26, #0x82b
0x51dd4	e8ffc039	ldrsb	w8, [sp, #0x3f]
0x51dd8	e8d8ff36	tbz	w8, #0x1f, 0x518f4 <_WeChatMain+0x38088>
0x51ddc	e01740f9	ldr	x0, [sp, #0x28]
0x51de0	e81f40f9	ldr	x8, [sp, #0x38]
0x51de4	01f94092	and	x1, x8, #0x7fffffffffffffff
0x51de8	89b8c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x51dec	c2feff17	b	0x518f4 <_WeChatMain+0x38088>
0x51df0	f9feffb4	cbz	x25, 0x51dcc <_WeChatMain+0x38560>
0x51df4	890240f9	ldr	x9, [x20]
0x51df8	1f010071	cmp	w8, #0x0
0x51dfc	37b1949a	csel	x23, x9, x20, lt
0x51e00	e0021a8b	add	x0, x23, x26
0x51e04	011005b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51e08	21902091	add	x1, x1, #0x824
0x51e0c	e20319aa	mov	x2, x25
0x51e10	21bcc395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x51e14	4803198b	add	x8, x26, x25
0x51e18	895ec039	ldrsb	w9, [x20, #0x17]
0x51e1c	8900f837	tbnz	w9, #0x1f, 0x51e2c <_WeChatMain+0x385c0>
0x51e20	09190012	and	w9, w8, #0x7f
0x51e24	895e0039	strb	w9, [x20, #0x17]
0x51e28	02000014	b	0x51e30 <_WeChatMain+0x385c4>
0x51e2c	880600f9	str	x8, [x20, #0x8]
0x51e30	1a1005b0	adrp	x26, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x51e34	5aaf2091	add	x26, x26, #0x82b
0x51e38	ff6a2838	strb	wzr, [x23, x8]
0x51e3c	e8ffc039	ldrsb	w8, [sp, #0x3f]
0x51e40	a8d5ff36	tbz	w8, #0x1f, 0x518f4 <_WeChatMain+0x38088>
0x51e44	e6ffff17	b	0x51ddc <_WeChatMain+0x38570>
0x51e48	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x51e4c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x51e50	fd430091	add	x29, sp, #0x10
0x51e54	e80300aa	mov	x8, x0
0x51e58	f30300aa	mov	x19, x0
0x51e5c	608e42f8	ldr	x0, [x19, #0x28]!
0x51e60	69825ff8	ldur	x9, [x19, #-0x8]
0x51e64	292940a9	ldp	x9, x10, [x9]
0x51e68	490109cb	sub	x9, x10, x9
0x51e6c	29fd4293	asr	x9, x9, #2
0x51e70	290500d1	sub	x9, x9, #0x1
0x51e74	6a0640f9	ldr	x10, [x19, #0x8]
0x51e78	4a0100cb	sub	x10, x10, x0
0x51e7c	4afd4293	asr	x10, x10, #2
0x51e80	21010aeb	subs	x1, x9, x10
0x51e84	a9000054	b.ls	0x51e98 <_WeChatMain+0x3862c>
0x51e88	e00313aa	mov	x0, x19
0x51e8c	ed000094	bl	0x52240 <_WeChatMain+0x389d4>
0x51e90	600240f9	ldr	x0, [x19]
0x51e94	04000014	b	0x51ea4 <_WeChatMain+0x38638>
0x51e98	62000054	b.hs	0x51ea4 <_WeChatMain+0x38638>
0x51e9c	0908098b	add	x9, x0, x9, lsl #2
0x51ea0	091900f9	str	x9, [x8, #0x30]
0x51ea4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x51ea8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x51eac	c0035fd6	ret
0x51eb0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x51eb4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x51eb8	fd430091	add	x29, sp, #0x10
0x51ebc	f40304aa	mov	x20, x4
0x51ec0	e80302aa	mov	x8, x2
0x51ec4	f30300aa	mov	x19, x0
0x51ec8	e20303aa	mov	x2, x3
0x51ecc	e30308aa	mov	x3, x8
0x51ed0	84f9ff97	bl	0x504e0 <_WeChatMain+0x36c74>
0x51ed4	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51ed8	08011a91	add	x8, x8, #0x680
0x51edc	080000f9	str	x8, [x0]
0x51ee0	800640ad	ldp	q0, q1, [x20]
0x51ee4	0180833c	stur	q1, [x0, #0x38]
0x51ee8	0080823c	stur	q0, [x0, #0x28]
0x51eec	080840f9	ldr	x8, [x0, #0x10]
0x51ef0	00510091	add	x0, x8, #0x14
0x51ef4	c4e7ff97	bl	0x4be04 <_WeChatMain+0x32598>
0x51ef8	a0000034	cbz	w0, 0x51f0c <_WeChatMain+0x386a0>
0x51efc	680240f9	ldr	x8, [x19]
0x51f00	083940f9	ldr	x8, [x8, #0x70]
0x51f04	e00313aa	mov	x0, x19
0x51f08	00013fd6	blr	x8
0x51f0c	e00313aa	mov	x0, x19
0x51f10	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x51f14	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x51f18	c0035fd6	ret
0x51f1c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x51f20	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x51f24	fd430091	add	x29, sp, #0x10
0x51f28	f30300aa	mov	x19, x0
0x51f2c	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51f30	08011a91	add	x8, x8, #0x680
0x51f34	088402f8	str	x8, [x0], #0x28
0x51f38	6523ff97	bl	0x1accc <_WeChatMain+0x1460>
0x51f3c	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51f40	08811591	add	x8, x8, #0x560
0x51f44	680200f9	str	x8, [x19]
0x51f48	601240f9	ldr	x0, [x19, #0x20]
0x51f4c	08745e92	and	x8, x0, #0xfffffffc00000000
0x51f50	49fd04b0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x51f54	29013b91	add	x9, x9, #0xec0
0x51f58	290540f9	ldr	x9, [x9, #0x8]
0x51f5c	1f0109eb	cmp	x8, x9
0x51f60	41000054	b.ne	0x51f68 <_WeChatMain+0x386fc>
0x51f64	d7b6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x51f68	7f1200f9	str	xzr, [x19, #0x20]
0x51f6c	e00313aa	mov	x0, x19
0x51f70	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x51f74	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x51f78	e5e7ff17	b	0x4bf0c <_WeChatMain+0x326a0>
0x51f7c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x51f80	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x51f84	fd430091	add	x29, sp, #0x10
0x51f88	f30300aa	mov	x19, x0
0x51f8c	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51f90	08011a91	add	x8, x8, #0x680
0x51f94	088402f8	str	x8, [x0], #0x28
0x51f98	4d23ff97	bl	0x1accc <_WeChatMain+0x1460>
0x51f9c	48d70490	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x51fa0	08811591	add	x8, x8, #0x560
0x51fa4	680200f9	str	x8, [x19]
0x51fa8	601240f9	ldr	x0, [x19, #0x20]
0x51fac	08745e92	and	x8, x0, #0xfffffffc00000000
0x51fb0	49fd04b0	adrp	x9, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x51fb4	29013b91	add	x9, x9, #0xec0
0x51fb8	290540f9	ldr	x9, [x9, #0x8]
0x51fbc	1f0109eb	cmp	x8, x9
0x51fc0	41000054	b.ne	0x51fc8 <_WeChatMain+0x3875c>
0x51fc4	bfb6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x51fc8	7f1200f9	str	xzr, [x19, #0x20]
0x51fcc	e00313aa	mov	x0, x19
0x51fd0	cfe7ff97	bl	0x4bf0c <_WeChatMain+0x326a0>
0x51fd4	01098052	mov	w1, #0x48               ; =72
0x51fd8	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x51fdc	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x51fe0	0bb8c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x51fe4	082040f9	ldr	x8, [x0, #0x40]
0x51fe8	080140b9	ldr	w8, [x8]
0x51fec	c8010034	cbz	w8, 0x52024 <_WeChatMain+0x387b8>
0x51ff0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x51ff4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x51ff8	fd430091	add	x29, sp, #0x10
0x51ffc	f30300aa	mov	x19, x0
0x52000	00a00091	add	x0, x0, #0x28
0x52004	ecf3ff97	bl	0x4efb4 <_WeChatMain+0x35748>
0x52008	608201d9	stlur	x0, [x19, #0x18]
0x5200c	688241d9	ldapur	x8, [x19, #0x18]
0x52010	1f0100f1	cmp	x8, #0x0
0x52014	e0079f1a	cset	w0, ne
0x52018	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5201c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x52020	c0035fd6	ret
0x52024	00008052	mov	w0, #0x0                ; =0
0x52028	c0035fd6	ret
0x5202c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x52030	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x52034	fd430091	add	x29, sp, #0x10
0x52038	f30300aa	mov	x19, x0
0x5203c	00a00091	add	x0, x0, #0x28
0x52040	ddf3ff97	bl	0x4efb4 <_WeChatMain+0x35748>
0x52044	800000b4	cbz	x0, 0x52054 <_WeChatMain+0x387e8>
0x52048	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5204c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x52050	c0035fd6	ret
0x52054	681240f9	ldr	x8, [x19, #0x20]
0x52058	082540a9	ldp	x8, x9, [x8]
0x5205c	280108cb	sub	x8, x9, x8
0x52060	08fd4293	asr	x8, x8, #2
0x52064	080500d1	sub	x8, x8, #0x1
0x52068	09f57ed3	lsl	x9, x8, #2
0x5206c	08fd7ed3	lsr	x8, x8, #62
0x52070	1f0100f1	cmp	x8, #0x0
0x52074	20019fda	csinv	x0, x9, xzr, eq
0x52078	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5207c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x52080	e6b7c315	b	0x7140018 <_wxam_enc_uninit_10+0x7140018>
0x52084	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x52088	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x5208c	fd430091	add	x29, sp, #0x10
0x52090	f30300aa	mov	x19, x0
0x52094	28d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x52098	08411c91	add	x8, x8, #0x710
0x5209c	080000f9	str	x8, [x0]
0x520a0	000c40f9	ldr	x0, [x0, #0x18]
0x520a4	08745e92	and	x8, x0, #0xfffffffc00000000
0x520a8	54fd0490	adrp	x20, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x520ac	94023b91	add	x20, x20, #0xec0
0x520b0	890640f9	ldr	x9, [x20, #0x8]
0x520b4	1f0109eb	cmp	x8, x9
0x520b8	41000054	b.ne	0x520c0 <_WeChatMain+0x38854>
0x520bc	81b6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x520c0	7f0e00f9	str	xzr, [x19, #0x18]
0x520c4	600640f9	ldr	x0, [x19, #0x8]
0x520c8	08745e92	and	x8, x0, #0xfffffffc00000000
0x520cc	890640f9	ldr	x9, [x20, #0x8]
0x520d0	1f0109eb	cmp	x8, x9
0x520d4	41000054	b.ne	0x520dc <_WeChatMain+0x38870>
0x520d8	7ab6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x520dc	7f0600f9	str	xzr, [x19, #0x8]
0x520e0	e00313aa	mov	x0, x19
0x520e4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x520e8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x520ec	f822ff17	b	0x1accc <_WeChatMain+0x1460>
0x520f0	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x520f4	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x520f8	fd430091	add	x29, sp, #0x10
0x520fc	f30300aa	mov	x19, x0
0x52100	28d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x52104	08411c91	add	x8, x8, #0x710
0x52108	080000f9	str	x8, [x0]
0x5210c	000c40f9	ldr	x0, [x0, #0x18]
0x52110	08745e92	and	x8, x0, #0xfffffffc00000000
0x52114	54fd0490	adrp	x20, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x52118	94023b91	add	x20, x20, #0xec0
0x5211c	890640f9	ldr	x9, [x20, #0x8]
0x52120	1f0109eb	cmp	x8, x9
0x52124	41000054	b.ne	0x5212c <_WeChatMain+0x388c0>
0x52128	66b6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x5212c	7f0e00f9	str	xzr, [x19, #0x18]
0x52130	600640f9	ldr	x0, [x19, #0x8]
0x52134	08745e92	and	x8, x0, #0xfffffffc00000000
0x52138	890640f9	ldr	x9, [x20, #0x8]
0x5213c	1f0109eb	cmp	x8, x9
0x52140	41000054	b.ne	0x52148 <_WeChatMain+0x388dc>
0x52144	5fb6ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x52148	7f0600f9	str	xzr, [x19, #0x8]
0x5214c	e00313aa	mov	x0, x19
0x52150	df22ff97	bl	0x1accc <_WeChatMain+0x1460>
0x52154	01058052	mov	w1, #0x28               ; =40
0x52158	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5215c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x52160	abb7c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x52164	081040f9	ldr	x8, [x0, #0x20]
0x52168	090840f9	ldr	x9, [x0, #0x10]
0x5216c	1f0109eb	cmp	x8, x9
0x52170	e0379f1a	cset	w0, hs
0x52174	c0035fd6	ret
0x52178	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x5217c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x52180	fd430091	add	x29, sp, #0x10
0x52184	f30300aa	mov	x19, x0
0x52188	081040f9	ldr	x8, [x0, #0x20]
0x5218c	08050091	add	x8, x8, #0x1
0x52190	081000f9	str	x8, [x0, #0x20]
0x52194	080040f9	ldr	x8, [x0]
0x52198	080940f9	ldr	x8, [x8, #0x10]
0x5219c	00013fd6	blr	x8
0x521a0	e0010037	tbnz	w0, #0x0, 0x521dc <_WeChatMain+0x38970>
0x521a4	680a40f9	ldr	x8, [x19, #0x10]
0x521a8	6a1240f9	ldr	x10, [x19, #0x20]
0x521ac	08010aeb	subs	x8, x8, x10
0x521b0	69010054	b.ls	0x521dc <_WeChatMain+0x38970>
0x521b4	6b0640f9	ldr	x11, [x19, #0x8]
0x521b8	49050091	add	x9, x10, #0x1
0x521bc	6a090a8b	add	x10, x11, x10, lsl #2
0x521c0	4b0140b9	ldr	w11, [x10]
0x521c4	cb000035	cbnz	w11, 0x521dc <_WeChatMain+0x38970>
0x521c8	4a110091	add	x10, x10, #0x4
0x521cc	691200f9	str	x9, [x19, #0x20]
0x521d0	29050091	add	x9, x9, #0x1
0x521d4	080500f1	subs	x8, x8, #0x1
0x521d8	41ffff54	b.ne	0x521c0 <_WeChatMain+0x38954>
0x521dc	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x521e0	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x521e4	c0035fd6	ret
0x521e8	a10000b4	cbz	x1, 0x521fc <_WeChatMain+0x38990>
0x521ec	08a441a9	ldp	x8, x9, [x0, #0x18]
0x521f0	080140f9	ldr	x8, [x8]
0x521f4	087969b8	ldr	w8, [x8, x9, lsl #2]
0x521f8	280000b9	str	w8, [x1]
0x521fc	c20000b4	cbz	x2, 0x52214 <_WeChatMain+0x389a8>
0x52200	08a441a9	ldp	x8, x9, [x0, #0x18]
0x52204	080140f9	ldr	x8, [x8]
0x52208	0809098b	add	x8, x8, x9, lsl #2
0x5220c	080580b9	ldrsw	x8, [x8, #0x4]
0x52210	480000f9	str	x8, [x2]
0x52214	a30000b4	cbz	x3, 0x52228 <_WeChatMain+0x389bc>
0x52218	080440f9	ldr	x8, [x0, #0x8]
0x5221c	091040f9	ldr	x9, [x0, #0x20]
0x52220	087969b8	ldr	w8, [x8, x9, lsl #2]
0x52224	680000b9	str	w8, [x3]
0x52228	c0035fd6	ret
0x5222c	610000b4	cbz	x1, 0x52238 <_WeChatMain+0x389cc>
0x52230	081040f9	ldr	x8, [x0, #0x20]
0x52234	280000f9	str	x8, [x1]
0x52238	20008052	mov	w0, #0x1                ; =1
0x5223c	c0035fd6	ret
0x52240	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x52244	fa6701a9	stp	x26, x25, [sp, #0x10]
0x52248	f85f02a9	stp	x24, x23, [sp, #0x20]
0x5224c	f65703a9	stp	x22, x21, [sp, #0x30]
0x52250	f44f04a9	stp	x20, x19, [sp, #0x40]
0x52254	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x52258	fd430191	add	x29, sp, #0x50
0x5225c	f30300aa	mov	x19, x0
0x52260	1ba040a9	ldp	x27, x8, [x0, #0x8]
0x52264	f4031baa	mov	x20, x27
0x52268	09011bcb	sub	x9, x8, x27
0x5226c	3f0889eb	cmp	x1, x9, asr #2
0x52270	09030054	b.ls	0x522d0 <_WeChatMain+0x38a64>
0x52274	750240f9	ldr	x21, [x19]
0x52278	7c0315cb	sub	x28, x27, x21
0x5227c	97ff4293	asr	x23, x28, #2
0x52280	e902018b	add	x9, x23, x1
0x52284	2afd7ed3	lsr	x10, x9, #62
0x52288	2a0b00b5	cbnz	x10, 0x523ec <_WeChatMain+0x38b80>
0x5228c	eaf37eb2	mov	x10, #0x7ffffffffffffffc ; =9223372036854775804
0x52290	160115cb	sub	x22, x8, x21
0x52294	c8fe4193	asr	x8, x22, #1
0x52298	1f0109eb	cmp	x8, x9
0x5229c	0881899a	csel	x8, x8, x9, hi
0x522a0	df020aeb	cmp	x22, x10
0x522a4	0900f892	mov	x9, #0x3fffffffffffffff ; =4611686018427387903
0x522a8	1a31899a	csel	x26, x8, x9, lo
0x522ac	3a0200b4	cbz	x26, 0x522f0 <_WeChatMain+0x38a84>
0x522b0	48ff7ed3	lsr	x8, x26, #62
0x522b4	080a00b5	cbnz	x8, 0x523f4 <_WeChatMain+0x38b88>
0x522b8	f90301aa	mov	x25, x1
0x522bc	40f77ed3	lsl	x0, x26, #2
0x522c0	5cb7c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x522c4	f80300aa	mov	x24, x0
0x522c8	e10319aa	mov	x1, x25
0x522cc	0a000014	b	0x522f4 <_WeChatMain+0x38a88>
0x522d0	c10000b4	cbz	x1, 0x522e8 <_WeChatMain+0x38a7c>
0x522d4	35f47ed3	lsl	x21, x1, #2
0x522d8	e00314aa	mov	x0, x20
0x522dc	e10315aa	mov	x1, x21
0x522e0	2cb8c395	bl	0x7140390 <_wxam_enc_uninit_10+0x7140390>
0x522e4	7403158b	add	x20, x27, x21
0x522e8	740600f9	str	x20, [x19, #0x8]
0x522ec	39000014	b	0x523d0 <_WeChatMain+0x38b64>
0x522f0	180080d2	mov	x24, #0x0               ; =0
0x522f4	170b178b	add	x23, x24, x23, lsl #2
0x522f8	39f47ed3	lsl	x25, x1, #2
0x522fc	1a0b1a8b	add	x26, x24, x26, lsl #2
0x52300	e00317aa	mov	x0, x23
0x52304	e10319aa	mov	x1, x25
0x52308	22b8c395	bl	0x7140390 <_wxam_enc_uninit_10+0x7140390>
0x5230c	e802198b	add	x8, x23, x25
0x52310	690315eb	subs	x9, x27, x21
0x52314	40040054	b.eq	0x5239c <_WeChatMain+0x38b30>
0x52318	291100d1	sub	x9, x9, #0x4
0x5231c	3ff100f1	cmp	x9, #0x3c
0x52320	23030054	b.lo	0x52384 <_WeChatMain+0x38b18>
0x52324	6a0318cb	sub	x10, x27, x24
0x52328	4a011ccb	sub	x10, x10, x28
0x5232c	5f0101f1	cmp	x10, #0x40
0x52330	a3020054	b.lo	0x52384 <_WeChatMain+0x38b18>
0x52334	29fd42d3	lsr	x9, x9, #2
0x52338	2a050091	add	x10, x9, #0x1
0x5233c	4be97c92	and	x11, x10, #0x7ffffffffffffff0
0x52340	69f57ed3	lsl	x9, x11, #2
0x52344	740309cb	sub	x20, x27, x9
0x52348	e90209cb	sub	x9, x23, x9
0x5234c	6c8300d1	sub	x12, x27, #0x20
0x52350	ed8200d1	sub	x13, x23, #0x20
0x52354	ee030baa	mov	x14, x11
0x52358	810140ad	ldp	q1, q0, [x12]
0x5235c	83097fad	ldp	q3, q2, [x12, #-0x20]
0x52360	a10100ad	stp	q1, q0, [x13]
0x52364	a3093fad	stp	q3, q2, [x13, #-0x20]
0x52368	8c0101d1	sub	x12, x12, #0x40
0x5236c	ad0101d1	sub	x13, x13, #0x40
0x52370	ce4100d1	sub	x14, x14, #0x10
0x52374	2effffb5	cbnz	x14, 0x52358 <_WeChatMain+0x38aec>
0x52378	f70309aa	mov	x23, x9
0x5237c	5f010beb	cmp	x10, x11
0x52380	00010054	b.eq	0x523a0 <_WeChatMain+0x38b34>
0x52384	e90317aa	mov	x9, x23
0x52388	8ace5fb8	ldr	w10, [x20, #-0x4]!
0x5238c	2acd1fb8	str	w10, [x9, #-0x4]!
0x52390	9f0215eb	cmp	x20, x21
0x52394	a1ffff54	b.ne	0x52388 <_WeChatMain+0x38b1c>
0x52398	02000014	b	0x523a0 <_WeChatMain+0x38b34>
0x5239c	e90317aa	mov	x9, x23
0x523a0	692200a9	stp	x9, x8, [x19]
0x523a4	7a0a00f9	str	x26, [x19, #0x10]
0x523a8	550100b4	cbz	x21, 0x523d0 <_WeChatMain+0x38b64>
0x523ac	e00315aa	mov	x0, x21
0x523b0	e10316aa	mov	x1, x22
0x523b4	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x523b8	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x523bc	f65743a9	ldp	x22, x21, [sp, #0x30]
0x523c0	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x523c4	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x523c8	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x523cc	10b7c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x523d0	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x523d4	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x523d8	f65743a9	ldp	x22, x21, [sp, #0x30]
0x523dc	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x523e0	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x523e4	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x523e8	c0035fd6	ret
0x523ec	e00313aa	mov	x0, x19
0x523f0	85d0ff97	bl	0x46604 <_WeChatMain+0x2cd98>
0x523f4	d645ff97	bl	0x23b4c <_WeChatMain+0xa2e0>
0x523f8	ff8301d1	sub	sp, sp, #0x60
0x523fc	f85f02a9	stp	x24, x23, [sp, #0x20]
0x52400	f65703a9	stp	x22, x21, [sp, #0x30]
0x52404	f44f04a9	stp	x20, x19, [sp, #0x40]
0x52408	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x5240c	fd430191	add	x29, sp, #0x50
0x52410	f40301aa	mov	x20, x1
0x52414	f50300aa	mov	x21, x0
0x52418	085c8039	ldrsb	x8, [x0, #0x17]
0x5241c	092840a9	ldp	x9, x10, [x0]
0x52420	1f0100f1	cmp	x8, #0x0
0x52424	20b1809a	csel	x0, x9, x0, lt
0x52428	1f010071	cmp	w8, #0x0
0x5242c	41b1889a	csel	x1, x10, x8, lt
0x52430	82050094	bl	0x53a38 <_WeChatMain+0x3a1cc>
0x52434	f30300aa	mov	x19, x0
0x52438	800e00b4	cbz	x0, 0x52608 <_WeChatMain+0x38d9c>
0x5243c	88008052	mov	w8, #0x4                ; =4
0x52440	e81700b9	str	w8, [sp, #0x14]
0x52444	680240f9	ldr	x8, [x19]
0x52448	081140f9	ldr	x8, [x8, #0x20]
0x5244c	e00313aa	mov	x0, x19
0x52450	00013fd6	blr	x8
0x52454	e01300b9	str	w0, [sp, #0x10]
0x52458	08100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5245c	09b96139	ldrb	w9, [x8, #0x86e]
0x52460	49050037	tbnz	w9, #0x0, 0x52508 <_WeChatMain+0x38c9c>
0x52464	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x52468	20a543fd	ldr	d0, [x9, #0x748]
0x5246c	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x52470	21a943fd	ldr	d1, [x9, #0x750]
0x52474	20040c6e	mov.s	v0[1], v1[0]
0x52478	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5247c	21ad43fd	ldr	d1, [x9, #0x758]
0x52480	2004146e	mov.s	v0[2], v1[0]
0x52484	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x52488	21b143fd	ldr	d1, [x9, #0x760]
0x5248c	20041c6e	mov.s	v0[3], v1[0]
0x52490	692104d0	adrp	x9, 0x8480000 <_wxam_enc_uninit_10+0x8480000>
0x52494	218d44fd	ldr	d1, [x9, #0x918]
0x52498	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5249c	22b543fd	ldr	d2, [x9, #0x768]
0x524a0	41040c6e	mov.s	v1[1], v2[0]
0x524a4	a92104f0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x524a8	227d43fd	ldr	d2, [x9, #0x6f8]
0x524ac	4104146e	mov.s	v1[2], v2[0]
0x524b0	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x524b4	22b943fd	ldr	d2, [x9, #0x770]
0x524b8	41041c6e	mov.s	v1[3], v2[0]
0x524bc	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x524c0	22bd43fd	ldr	d2, [x9, #0x778]
0x524c4	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x524c8	236540fd	ldr	d3, [x9, #0xc8]
0x524cc	62040c6e	mov.s	v2[1], v3[0]
0x524d0	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x524d4	23c143fd	ldr	d3, [x9, #0x780]
0x524d8	6204146e	mov.s	v2[2], v3[0]
0x524dc	c9210490	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x524e0	23c543fd	ldr	d3, [x9, #0x788]
0x524e4	62041c6e	mov.s	v2[3], v3[0]
0x524e8	09100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x524ec	29f12091	add	x9, x9, #0x83c
0x524f0	200500ad	stp	q0, q1, [x9]
0x524f4	2209803d	str	q2, [x9, #0x20]
0x524f8	2a058052	mov	w10, #0x29              ; =41
0x524fc	2a610079	strh	w10, [x9, #0x30]
0x52500	29008052	mov	w9, #0x1                ; =1
0x52504	09b92139	strb	w9, [x8, #0x86e]
0x52508	1f100071	cmp	w0, #0x4
0x5250c	00070054	b.eq	0x525ec <_WeChatMain+0x38d80>
0x52510	14000090	adrp	x20, 0x52000 <_WeChatMain+0x38794>
0x52514	94123c91	add	x20, x20, #0xf04
0x52518	e0530091	add	x0, sp, #0x14
0x5251c	e10314aa	mov	x1, x20
0x52520	083eff97	bl	0x21d40 <_WeChatMain+0x84d4>
0x52524	f50300aa	mov	x21, x0
0x52528	e0430091	add	x0, sp, #0x10
0x5252c	e10314aa	mov	x1, x20
0x52530	043eff97	bl	0x21d40 <_WeChatMain+0x84d4>
0x52534	e30300aa	mov	x3, x0
0x52538	01100590	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5253c	21f02091	add	x1, x1, #0x83c
0x52540	e0630091	add	x0, sp, #0x18
0x52544	e20315aa	mov	x2, x21
0x52548	953fff97	bl	0x2239c <_WeChatMain+0x8b30>
0x5254c	e80f40f9	ldr	x8, [sp, #0x18]
0x52550	e80f00f9	str	x8, [sp, #0x18]
0x52554	c80400b4	cbz	x8, 0x525ec <_WeChatMain+0x38d80>
0x52558	08100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5255c	09816339	ldrb	w9, [x8, #0x8e0]
0x52560	69030037	tbnz	w9, #0x0, 0x525cc <_WeChatMain+0x38d60>
0x52564	090080d2	mov	x9, #0x0                ; =0
0x52568	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x5256c	aa9999f2	movk	x10, #0xcccd
0x52570	6b028092	mov	x11, #-0x14             ; =-20
0x52574	cc210490	adrp	x12, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x52578	8c811e91	add	x12, x12, #0x7a0
0x5257c	0d100590	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x52580	adbd2191	add	x13, x13, #0x86f
0x52584	2e7dca9b	umulh	x14, x9, x10
0x52588	cefd44d3	lsr	x14, x14, #4
0x5258c	8f01098b	add	x15, x12, x9
0x52590	ce3d0b9b	madd	x14, x14, x11, x15
0x52594	e0a145bc	ldur	s0, [x15, #0x5a]
0x52598	00a4082f	ushll.8h	v0, v0, #0x0
0x5259c	c16144bc	ldur	s1, [x14, #0x46]
0x525a0	21a4082f	ushll.8h	v1, v1, #0x0
0x525a4	201c202e	eor.8b	v0, v1, v0
0x525a8	0018000e	uzp1.8b	v0, v0, v0
0x525ac	a06929bc	str	s0, [x13, x9]
0x525b0	29110091	add	x9, x9, #0x4
0x525b4	3fc101f1	cmp	x9, #0x70
0x525b8	61feff54	b.ne	0x52584 <_WeChatMain+0x38d18>
0x525bc	09100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x525c0	3f7d2339	strb	wzr, [x9, #0x8df]
0x525c4	29008052	mov	w9, #0x1                ; =1
0x525c8	09812339	strb	w9, [x8, #0x8e0]
0x525cc	00100590	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x525d0	00bc2191	add	x0, x0, #0x86f
0x525d4	e8230091	add	x8, sp, #0x8
0x525d8	e2630091	add	x2, sp, #0x18
0x525dc	a1098052	mov	w1, #0x4d               ; =77
0x525e0	813cff97	bl	0x217e4 <_WeChatMain+0x7f78>
0x525e4	e0230091	add	x0, sp, #0x8
0x525e8	a120ff97	bl	0x1a86c <_WeChatMain+0x1000>
0x525ec	e00313aa	mov	x0, x19
0x525f0	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x525f4	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x525f8	f65743a9	ldp	x22, x21, [sp, #0x30]
0x525fc	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x52600	ff830191	add	sp, sp, #0x60
0x52604	c0035fd6	ret
0x52608	a85e8039	ldrsb	x8, [x21, #0x17]
0x5260c	a92a40a9	ldp	x9, x10, [x21]
0x52610	1f0100f1	cmp	x8, #0x0
0x52614	20b1959a	csel	x0, x9, x21, lt
0x52618	1f010071	cmp	w8, #0x0
0x5261c	41b1889a	csel	x1, x10, x8, lt
0x52620	17ebff97	bl	0x4d27c <_WeChatMain+0x33a10>
0x52624	cc060094	bl	0x54154 <_WeChatMain+0x3a8e8>
0x52628	a0040034	cbz	w0, 0x526bc <_WeChatMain+0x38e50>
0x5262c	ff1700b9	str	wzr, [sp, #0x14]
0x52630	bbeeff97	bl	0x4e11c <_WeChatMain+0x348b0>
0x52634	f60300aa	mov	x22, x0
0x52638	a00100b4	cbz	x0, 0x5266c <_WeChatMain+0x38e00>
0x5263c	e8630091	add	x8, sp, #0x18
0x52640	e7530091	add	x7, sp, #0x14
0x52644	e00316aa	mov	x0, x22
0x52648	81008052	mov	w1, #0x4                ; =4
0x5264c	e20315aa	mov	x2, x21
0x52650	03008052	mov	w3, #0x0                ; =0
0x52654	04008052	mov	w4, #0x0                ; =0
0x52658	050080d2	mov	x5, #0x0                ; =0
0x5265c	e60314aa	mov	x6, x20
0x52660	0ceeff97	bl	0x4de90 <_WeChatMain+0x34624>
0x52664	f70f40f9	ldr	x23, [sp, #0x18]
0x52668	770100b5	cbnz	x23, 0x52694 <_WeChatMain+0x38e28>
0x5266c	000e8052	mov	w0, #0x70               ; =112
0x52670	70b6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52674	f70300aa	mov	x23, x0
0x52678	e00315aa	mov	x0, x21
0x5267c	b2e4ff97	bl	0x4b944 <_WeChatMain+0x320d8>
0x52680	e10300aa	mov	x1, x0
0x52684	e00317aa	mov	x0, x23
0x52688	80010094	bl	0x52c88 <_WeChatMain+0x3941c>
0x5268c	817a1912	and	w1, w20, #0xffffffbf
0x52690	97e3ff97	bl	0x4b4ec <_WeChatMain+0x31c80>
0x52694	e00317aa	mov	x0, x23
0x52698	47020094	bl	0x52fb4 <_WeChatMain+0x39748>
0x5269c	f30300aa	mov	x19, x0
0x526a0	e11740b9	ldr	w1, [sp, #0x14]
0x526a4	c1ecff34	cbz	w1, 0x5243c <_WeChatMain+0x38bd0>
0x526a8	7f0217eb	cmp	x19, x23
0x526ac	e2179f1a	cset	w2, eq
0x526b0	e00316aa	mov	x0, x22
0x526b4	91eeff97	bl	0x4e0f8 <_WeChatMain+0x3488c>
0x526b8	61ffff17	b	0x5243c <_WeChatMain+0x38bd0>
0x526bc	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x526c0	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x526c4	f65743a9	ldp	x22, x21, [sp, #0x30]
0x526c8	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x526cc	ff830191	add	sp, sp, #0x60
0x526d0	e0cfff17	b	0x46650 <_WeChatMain+0x2cde4>
0x526d4	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x526d8	f65701a9	stp	x22, x21, [sp, #0x10]
0x526dc	f44f02a9	stp	x20, x19, [sp, #0x20]
0x526e0	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x526e4	fdc30091	add	x29, sp, #0x30
0x526e8	f30303aa	mov	x19, x3
0x526ec	f40302aa	mov	x20, x2
0x526f0	f50301aa	mov	x21, x1
0x526f4	f60300aa	mov	x22, x0
0x526f8	f70308aa	mov	x23, x8
0x526fc	000e8052	mov	w0, #0x70               ; =112
0x52700	4cb6c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52704	e10316aa	mov	x1, x22
0x52708	e20315aa	mov	x2, x21
0x5270c	e30314aa	mov	x3, x20
0x52710	e40313aa	mov	x4, x19
0x52714	8e010094	bl	0x52d4c <_WeChatMain+0x394e0>
0x52718	e00200f9	str	x0, [x23]
0x5271c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x52720	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x52724	f65741a9	ldp	x22, x21, [sp, #0x10]
0x52728	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x5272c	c0035fd6	ret
0x52730	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x52734	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x52738	fd430091	add	x29, sp, #0x10
0x5273c	f30300aa	mov	x19, x0
0x52740	28d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x52744	08c11e91	add	x8, x8, #0x7b0
0x52748	080000f9	str	x8, [x0]
0x5274c	003440f9	ldr	x0, [x0, #0x68]
0x52750	7f3600f9	str	xzr, [x19, #0x68]
0x52754	800000b4	cbz	x0, 0x52764 <_WeChatMain+0x38ef8>
0x52758	080040f9	ldr	x8, [x0]
0x5275c	080540f9	ldr	x8, [x8, #0x8]
0x52760	00013fd6	blr	x8
0x52764	603240f9	ldr	x0, [x19, #0x60]
0x52768	7f3200f9	str	xzr, [x19, #0x60]
0x5276c	800000b4	cbz	x0, 0x5277c <_WeChatMain+0x38f10>
0x52770	080040f9	ldr	x8, [x0]
0x52774	080540f9	ldr	x8, [x8, #0x8]
0x52778	00013fd6	blr	x8
0x5277c	60620091	add	x0, x19, #0x18
0x52780	385f0094	bl	0x6a460 <_WeChatMain+0x50bf4>
0x52784	e00313aa	mov	x0, x19
0x52788	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5278c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x52790	4f21ff17	b	0x1accc <_WeChatMain+0x1460>
0x52794	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x52798	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x5279c	fd430091	add	x29, sp, #0x10
0x527a0	f30300aa	mov	x19, x0
0x527a4	28d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x527a8	08c11e91	add	x8, x8, #0x7b0
0x527ac	080000f9	str	x8, [x0]
0x527b0	003440f9	ldr	x0, [x0, #0x68]
0x527b4	7f3600f9	str	xzr, [x19, #0x68]
0x527b8	800000b4	cbz	x0, 0x527c8 <_WeChatMain+0x38f5c>
0x527bc	080040f9	ldr	x8, [x0]
0x527c0	080540f9	ldr	x8, [x8, #0x8]
0x527c4	00013fd6	blr	x8
0x527c8	603240f9	ldr	x0, [x19, #0x60]
0x527cc	7f3200f9	str	xzr, [x19, #0x60]
0x527d0	800000b4	cbz	x0, 0x527e0 <_WeChatMain+0x38f74>
0x527d4	080040f9	ldr	x8, [x0]
0x527d8	080540f9	ldr	x8, [x8, #0x8]
0x527dc	00013fd6	blr	x8
0x527e0	60620091	add	x0, x19, #0x18
0x527e4	1f5f0094	bl	0x6a460 <_WeChatMain+0x50bf4>
0x527e8	e00313aa	mov	x0, x19
0x527ec	3821ff97	bl	0x1accc <_WeChatMain+0x1460>
0x527f0	010e8052	mov	w1, #0x70               ; =112
0x527f4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x527f8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x527fc	04b6c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x52800	083040f9	ldr	x8, [x0, #0x60]
0x52804	080940f9	ldr	x8, [x8, #0x10]
0x52808	000140f9	ldr	x0, [x8]
0x5280c	c0035fd6	ret
0x52810	80008052	mov	w0, #0x4                ; =4
0x52814	c0035fd6	ret
0x52818	00008052	mov	w0, #0x0                ; =0
0x5281c	c0035fd6	ret
0x52820	080040f9	ldr	x8, [x0]
0x52824	031d40f9	ldr	x3, [x8, #0x38]
0x52828	22008052	mov	w2, #0x1                ; =1
0x5282c	60001fd6	br	x3
0x52830	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x52834	f44f01a9	stp	x20, x19, [sp, #0x10]
0x52838	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x5283c	fd830091	add	x29, sp, #0x20
0x52840	5f040071	cmp	w2, #0x1
0x52844	6b020054	b.lt	0x52890 <_WeChatMain+0x39024>
0x52848	f50302aa	mov	x21, x2
0x5284c	f30301aa	mov	x19, x1
0x52850	f40300aa	mov	x20, x0
0x52854	00600091	add	x0, x0, #0x18
0x52858	27bbc395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x5285c	20020035	cbnz	w0, 0x528a0 <_WeChatMain+0x39034>
0x52860	803240f9	ldr	x0, [x20, #0x60]
0x52864	080040f9	ldr	x8, [x0]
0x52868	080940f9	ldr	x8, [x8, #0x10]
0x5286c	e10313aa	mov	x1, x19
0x52870	e20315aa	mov	x2, x21
0x52874	00013fd6	blr	x8
0x52878	80620091	add	x0, x20, #0x18
0x5287c	21bbc395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x52880	482605d0	adrp	x8, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x52884	08653091	add	x8, x8, #0xc19
0x52888	08014039	ldrb	w8, [x8]
0x5288c	08010037	tbnz	w8, #0x0, 0x528ac <_WeChatMain+0x39040>
0x52890	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x52894	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x52898	f657c3a8	ldp	x22, x21, [sp], #0x30
0x5289c	c0035fd6	ret
0x528a0	80620091	add	x0, x20, #0x18
0x528a4	f85e0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x528a8	eeffff17	b	0x52860 <_WeChatMain+0x38ff4>
0x528ac	e00314aa	mov	x0, x20
0x528b0	e10313aa	mov	x1, x19
0x528b4	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x528b8	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x528bc	f657c3a8	ldp	x22, x21, [sp], #0x30
0x528c0	26e3ff17	b	0x4b558 <_WeChatMain+0x31cec>
0x528c4	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x528c8	f44f01a9	stp	x20, x19, [sp, #0x10]
0x528cc	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x528d0	fd830091	add	x29, sp, #0x20
0x528d4	f50300aa	mov	x21, x0
0x528d8	f30308aa	mov	x19, x8
0x528dc	00068052	mov	w0, #0x30               ; =48
0x528e0	d4b5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x528e4	f40300aa	mov	x20, x0
0x528e8	f60315aa	mov	x22, x21
0x528ec	c88641f8	ldr	x8, [x22], #0x18
0x528f0	080d40f9	ldr	x8, [x8, #0x18]
0x528f4	e00315aa	mov	x0, x21
0x528f8	00013fd6	blr	x8
0x528fc	e10300aa	mov	x1, x0
0x52900	e00314aa	mov	x0, x20
0x52904	70f5ff97	bl	0x4fec4 <_WeChatMain+0x36658>
0x52908	e00316aa	mov	x0, x22
0x5290c	fabac395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x52910	20020035	cbnz	w0, 0x52954 <_WeChatMain+0x390e8>
0x52914	a13240f9	ldr	x1, [x21, #0x60]
0x52918	880240f9	ldr	x8, [x20]
0x5291c	081540f9	ldr	x8, [x8, #0x28]
0x52920	e00314aa	mov	x0, x20
0x52924	00013fd6	blr	x8
0x52928	a13640f9	ldr	x1, [x21, #0x68]
0x5292c	880240f9	ldr	x8, [x20]
0x52930	081540f9	ldr	x8, [x8, #0x28]
0x52934	e00314aa	mov	x0, x20
0x52938	00013fd6	blr	x8
0x5293c	740200f9	str	x20, [x19]
0x52940	e00316aa	mov	x0, x22
0x52944	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x52948	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x5294c	f657c3a8	ldp	x22, x21, [sp], #0x30
0x52950	ecbac315	b	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x52954	e00316aa	mov	x0, x22
0x52958	cb5e0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x5295c	eeffff17	b	0x52914 <_WeChatMain+0x390a8>
0x52960	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x52964	f44f01a9	stp	x20, x19, [sp, #0x10]
0x52968	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x5296c	fd830091	add	x29, sp, #0x20
0x52970	f50300aa	mov	x21, x0
0x52974	f30308aa	mov	x19, x8
0x52978	00068052	mov	w0, #0x30               ; =48
0x5297c	adb5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52980	f40300aa	mov	x20, x0
0x52984	f60315aa	mov	x22, x21
0x52988	c88641f8	ldr	x8, [x22], #0x18
0x5298c	080d40f9	ldr	x8, [x8, #0x18]
0x52990	e00315aa	mov	x0, x21
0x52994	00013fd6	blr	x8
0x52998	e10300aa	mov	x1, x0
0x5299c	e00314aa	mov	x0, x20
0x529a0	49f5ff97	bl	0x4fec4 <_WeChatMain+0x36658>
0x529a4	e00316aa	mov	x0, x22
0x529a8	d3bac395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x529ac	c0020035	cbnz	w0, 0x52a04 <_WeChatMain+0x39198>
0x529b0	a13240f9	ldr	x1, [x21, #0x60]
0x529b4	880240f9	ldr	x8, [x20]
0x529b8	081540f9	ldr	x8, [x8, #0x28]
0x529bc	e00314aa	mov	x0, x20
0x529c0	00013fd6	blr	x8
0x529c4	a03240f9	ldr	x0, [x21, #0x60]
0x529c8	080040f9	ldr	x8, [x0]
0x529cc	081d40f9	ldr	x8, [x8, #0x38]
0x529d0	e10314aa	mov	x1, x20
0x529d4	00013fd6	blr	x8
0x529d8	a03640f9	ldr	x0, [x21, #0x68]
0x529dc	080040f9	ldr	x8, [x0]
0x529e0	081540f9	ldr	x8, [x8, #0x28]
0x529e4	e10314aa	mov	x1, x20
0x529e8	00013fd6	blr	x8
0x529ec	740200f9	str	x20, [x19]
0x529f0	e00316aa	mov	x0, x22
0x529f4	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x529f8	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x529fc	f657c3a8	ldp	x22, x21, [sp], #0x30
0x52a00	c0bac315	b	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x52a04	e00316aa	mov	x0, x22
0x52a08	9f5e0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x52a0c	e9ffff17	b	0x529b0 <_WeChatMain+0x39144>
0x52a10	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x52a14	f44f01a9	stp	x20, x19, [sp, #0x10]
0x52a18	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x52a1c	fd830091	add	x29, sp, #0x20
0x52a20	f30300aa	mov	x19, x0
0x52a24	f40308aa	mov	x20, x8
0x52a28	28008052	mov	w8, #0x1                ; =1
0x52a2c	08600139	strb	w8, [x0, #0x58]
0x52a30	00068052	mov	w0, #0x30               ; =48
0x52a34	7fb5c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52a38	f50300aa	mov	x21, x0
0x52a3c	680240f9	ldr	x8, [x19]
0x52a40	080d40f9	ldr	x8, [x8, #0x18]
0x52a44	e00313aa	mov	x0, x19
0x52a48	00013fd6	blr	x8
0x52a4c	e10300aa	mov	x1, x0
0x52a50	e00315aa	mov	x0, x21
0x52a54	1cf5ff97	bl	0x4fec4 <_WeChatMain+0x36658>
0x52a58	60620091	add	x0, x19, #0x18
0x52a5c	a6bac395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x52a60	80010035	cbnz	w0, 0x52a90 <_WeChatMain+0x39224>
0x52a64	613240f9	ldr	x1, [x19, #0x60]
0x52a68	a80240f9	ldr	x8, [x21]
0x52a6c	081540f9	ldr	x8, [x8, #0x28]
0x52a70	e00315aa	mov	x0, x21
0x52a74	00013fd6	blr	x8
0x52a78	950200f9	str	x21, [x20]
0x52a7c	60620091	add	x0, x19, #0x18
0x52a80	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x52a84	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x52a88	f657c3a8	ldp	x22, x21, [sp], #0x30
0x52a8c	9dbac315	b	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x52a90	60620091	add	x0, x19, #0x18
0x52a94	7c5e0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x52a98	f3ffff17	b	0x52a64 <_WeChatMain+0x391f8>
0x52a9c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x52aa0	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x52aa4	fd430091	add	x29, sp, #0x10
0x52aa8	f40301aa	mov	x20, x1
0x52aac	f30300aa	mov	x19, x0
0x52ab0	00600091	add	x0, x0, #0x18
0x52ab4	90bac395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x52ab8	40010035	cbnz	w0, 0x52ae0 <_WeChatMain+0x39274>
0x52abc	603240f9	ldr	x0, [x19, #0x60]
0x52ac0	080040f9	ldr	x8, [x0]
0x52ac4	081540f9	ldr	x8, [x8, #0x28]
0x52ac8	e10314aa	mov	x1, x20
0x52acc	00013fd6	blr	x8
0x52ad0	60620091	add	x0, x19, #0x18
0x52ad4	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x52ad8	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x52adc	89bac315	b	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x52ae0	60620091	add	x0, x19, #0x18
0x52ae4	685e0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x52ae8	f5ffff17	b	0x52abc <_WeChatMain+0x39250>
0x52aec	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x52af0	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x52af4	fd430091	add	x29, sp, #0x10
0x52af8	f40301aa	mov	x20, x1
0x52afc	f30300aa	mov	x19, x0
0x52b00	00600091	add	x0, x0, #0x18
0x52b04	7cbac395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x52b08	a0010035	cbnz	w0, 0x52b3c <_WeChatMain+0x392d0>
0x52b0c	603240f9	ldr	x0, [x19, #0x60]
0x52b10	080040f9	ldr	x8, [x0]
0x52b14	081940f9	ldr	x8, [x8, #0x30]
0x52b18	e10314aa	mov	x1, x20
0x52b1c	00013fd6	blr	x8
0x52b20	f40300aa	mov	x20, x0
0x52b24	60620091	add	x0, x19, #0x18
0x52b28	76bac395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x52b2c	e00314aa	mov	x0, x20
0x52b30	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x52b34	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x52b38	c0035fd6	ret
0x52b3c	60620091	add	x0, x19, #0x18
0x52b40	515e0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x52b44	f2ffff17	b	0x52b0c <_WeChatMain+0x392a0>
0x52b48	ff0301d1	sub	sp, sp, #0x40
0x52b4c	f65701a9	stp	x22, x21, [sp, #0x10]
0x52b50	f44f02a9	stp	x20, x19, [sp, #0x20]
0x52b54	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x52b58	fdc30091	add	x29, sp, #0x30
0x52b5c	f40300aa	mov	x20, x0
0x52b60	f30308aa	mov	x19, x8
0x52b64	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x52b68	e80300f9	str	x8, [sp]
0x52b6c	080040f9	ldr	x8, [x0]
0x52b70	092d40f9	ldr	x9, [x8, #0x58]
0x52b74	e8030091	mov	x8, sp
0x52b78	20013fd6	blr	x9
0x52b7c	f50340f9	ldr	x21, [sp]
0x52b80	960640f9	ldr	x22, [x20, #0x8]
0x52b84	b60000b4	cbz	x22, 0x52b98 <_WeChatMain+0x3932c>
0x52b88	e00316aa	mov	x0, x22
0x52b8c	9bbbc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x52b90	e20300aa	mov	x2, x0
0x52b94	0b000014	b	0x52bc0 <_WeChatMain+0x39354>
0x52b98	40bf04d0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52b9c	00800791	add	x0, x0, #0x1e0
0x52ba0	42bf04d0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52ba4	42300991	add	x2, x2, #0x24c
0x52ba8	e8230091	add	x8, sp, #0x8
0x52bac	a10f8052	mov	w1, #0x7d               ; =125
0x52bb0	c53aff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x52bb4	e0230091	add	x0, sp, #0x8
0x52bb8	2d1fff97	bl	0x1a86c <_WeChatMain+0x1000>
0x52bbc	020080d2	mov	x2, #0x0                ; =0
0x52bc0	831240b9	ldr	w3, [x20, #0x10]
0x52bc4	e80313aa	mov	x8, x19
0x52bc8	e00315aa	mov	x0, x21
0x52bcc	e10316aa	mov	x1, x22
0x52bd0	71e6ff97	bl	0x4c594 <_WeChatMain+0x32d28>
0x52bd4	e00340f9	ldr	x0, [sp]
0x52bd8	ff0300f9	str	xzr, [sp]
0x52bdc	800000b4	cbz	x0, 0x52bec <_WeChatMain+0x39380>
0x52be0	080040f9	ldr	x8, [x0]
0x52be4	080540f9	ldr	x8, [x8, #0x8]
0x52be8	00013fd6	blr	x8
0x52bec	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x52bf0	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x52bf4	f65741a9	ldp	x22, x21, [sp, #0x10]
0x52bf8	ff030191	add	sp, sp, #0x40
0x52bfc	c0035fd6	ret
0x52c00	ff0301d1	sub	sp, sp, #0x40
0x52c04	f44f02a9	stp	x20, x19, [sp, #0x20]
0x52c08	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x52c0c	fdc30091	add	x29, sp, #0x30
0x52c10	f30301aa	mov	x19, x1
0x52c14	f40300aa	mov	x20, x0
0x52c18	000440f9	ldr	x0, [x0, #0x8]
0x52c1c	e00700f9	str	x0, [sp, #0x8]
0x52c20	800000b4	cbz	x0, 0x52c30 <_WeChatMain+0x393c4>
0x52c24	75bbc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x52c28	e00b00f9	str	x0, [sp, #0x10]
0x52c2c	0b000014	b	0x52c58 <_WeChatMain+0x393ec>
0x52c30	ff0b00f9	str	xzr, [sp, #0x10]
0x52c34	40bf04d0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52c38	00800791	add	x0, x0, #0x1e0
0x52c3c	42bf04d0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52c40	42300991	add	x2, x2, #0x24c
0x52c44	e8630091	add	x8, sp, #0x18
0x52c48	a10f8052	mov	w1, #0x7d               ; =125
0x52c4c	9e3aff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x52c50	e0630091	add	x0, sp, #0x18
0x52c54	061fff97	bl	0x1a86c <_WeChatMain+0x1000>
0x52c58	e1230091	add	x1, sp, #0x8
0x52c5c	e00313aa	mov	x0, x19
0x52c60	ef150094	bl	0x5841c <_WeChatMain+0x3ebb0>
0x52c64	881240b9	ldr	w8, [x20, #0x10]
0x52c68	e80b00b9	str	w8, [sp, #0x8]
0x52c6c	e1230091	add	x1, sp, #0x8
0x52c70	e00313aa	mov	x0, x19
0x52c74	25130094	bl	0x57908 <_WeChatMain+0x3e09c>
0x52c78	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x52c7c	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x52c80	ff030191	add	sp, sp, #0x40
0x52c84	c0035fd6	ret
0x52c88	ff0301d1	sub	sp, sp, #0x40
0x52c8c	f65701a9	stp	x22, x21, [sp, #0x10]
0x52c90	f44f02a9	stp	x20, x19, [sp, #0x20]
0x52c94	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x52c98	fdc30091	add	x29, sp, #0x30
0x52c9c	f40301aa	mov	x20, x1
0x52ca0	f30300aa	mov	x19, x0
0x52ca4	0ae2ff97	bl	0x4b4cc <_WeChatMain+0x31c60>
0x52ca8	28d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x52cac	08c11e91	add	x8, x8, #0x7b0
0x52cb0	088401f8	str	x8, [x0], #0x18
0x52cb4	ca5d0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x52cb8	7f620139	strb	wzr, [x19, #0x58]
0x52cbc	00068052	mov	w0, #0x30               ; =48
0x52cc0	dcb4c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52cc4	f50300aa	mov	x21, x0
0x52cc8	b40000b4	cbz	x20, 0x52cdc <_WeChatMain+0x39470>
0x52ccc	e00314aa	mov	x0, x20
0x52cd0	4abbc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x52cd4	e10300aa	mov	x1, x0
0x52cd8	0b000014	b	0x52d04 <_WeChatMain+0x39498>
0x52cdc	40bf04d0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52ce0	00800791	add	x0, x0, #0x1e0
0x52ce4	42bf04d0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52ce8	42300991	add	x2, x2, #0x24c
0x52cec	e8230091	add	x8, sp, #0x8
0x52cf0	a10f8052	mov	w1, #0x7d               ; =125
0x52cf4	743aff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x52cf8	e0230091	add	x0, sp, #0x8
0x52cfc	dc1eff97	bl	0x1a86c <_WeChatMain+0x1000>
0x52d00	010080d2	mov	x1, #0x0                ; =0
0x52d04	e00314aa	mov	x0, x20
0x52d08	46e9ff97	bl	0x4d220 <_WeChatMain+0x339b4>
0x52d0c	e10300aa	mov	x1, x0
0x52d10	e00315aa	mov	x0, x21
0x52d14	6cf4ff97	bl	0x4fec4 <_WeChatMain+0x36658>
0x52d18	753200f9	str	x21, [x19, #0x60]
0x52d1c	00068052	mov	w0, #0x30               ; =48
0x52d20	c4b4c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52d24	a80a40f9	ldr	x8, [x21, #0x10]
0x52d28	010140f9	ldr	x1, [x8]
0x52d2c	66f4ff97	bl	0x4fec4 <_WeChatMain+0x36658>
0x52d30	603600f9	str	x0, [x19, #0x68]
0x52d34	e00313aa	mov	x0, x19
0x52d38	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x52d3c	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x52d40	f65741a9	ldp	x22, x21, [sp, #0x10]
0x52d44	ff030191	add	sp, sp, #0x40
0x52d48	c0035fd6	ret
0x52d4c	ff4301d1	sub	sp, sp, #0x50
0x52d50	f85f01a9	stp	x24, x23, [sp, #0x10]
0x52d54	f65702a9	stp	x22, x21, [sp, #0x20]
0x52d58	f44f03a9	stp	x20, x19, [sp, #0x30]
0x52d5c	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x52d60	fd030191	add	x29, sp, #0x40
0x52d64	f40304aa	mov	x20, x4
0x52d68	f60303aa	mov	x22, x3
0x52d6c	f70302aa	mov	x23, x2
0x52d70	f50301aa	mov	x21, x1
0x52d74	f30300aa	mov	x19, x0
0x52d78	e10302aa	mov	x1, x2
0x52d7c	d4e1ff97	bl	0x4b4cc <_WeChatMain+0x31c60>
0x52d80	28d704f0	adrp	x8, 0x9b39000 <_wxam_enc_uninit_10+0x9b39000>
0x52d84	08c11e91	add	x8, x8, #0x7b0
0x52d88	088401f8	str	x8, [x0], #0x18
0x52d8c	945d0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x52d90	7f620139	strb	wzr, [x19, #0x58]
0x52d94	00088052	mov	w0, #0x40               ; =64
0x52d98	a6b4c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52d9c	f80300aa	mov	x24, x0
0x52da0	b70000b4	cbz	x23, 0x52db4 <_WeChatMain+0x39548>
0x52da4	e00317aa	mov	x0, x23
0x52da8	14bbc395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x52dac	e10300aa	mov	x1, x0
0x52db0	0b000014	b	0x52ddc <_WeChatMain+0x39570>
0x52db4	40bf04d0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52db8	00800791	add	x0, x0, #0x1e0
0x52dbc	42bf04d0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x52dc0	42300991	add	x2, x2, #0x24c
0x52dc4	e8230091	add	x8, sp, #0x8
0x52dc8	a10f8052	mov	w1, #0x7d               ; =125
0x52dcc	3e3aff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x52dd0	e0230091	add	x0, sp, #0x8
0x52dd4	a61eff97	bl	0x1a86c <_WeChatMain+0x1000>
0x52dd8	010080d2	mov	x1, #0x0                ; =0
0x52ddc	e00317aa	mov	x0, x23
0x52de0	10e9ff97	bl	0x4d220 <_WeChatMain+0x339b4>
0x52de4	e10300aa	mov	x1, x0
0x52de8	e00318aa	mov	x0, x24
0x52dec	e20315aa	mov	x2, x21
0x52df0	e30316aa	mov	x3, x22
0x52df4	e1f0ff97	bl	0x4f178 <_WeChatMain+0x3590c>
0x52df8	783200f9	str	x24, [x19, #0x60]
0x52dfc	00088052	mov	w0, #0x40               ; =64
0x52e00	8cb4c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x52e04	080b40f9	ldr	x8, [x24, #0x10]
0x52e08	080140f9	ldr	x8, [x8]
0x52e0c	01050091	add	x1, x8, #0x1
0x52e10	e20315aa	mov	x2, x21
0x52e14	e30314aa	mov	x3, x20
0x52e18	d8f0ff97	bl	0x4f178 <_WeChatMain+0x3590c>
0x52e1c	603600f9	str	x0, [x19, #0x68]
0x52e20	e00313aa	mov	x0, x19
0x52e24	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x52e28	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x52e2c	f65742a9	ldp	x22, x21, [sp, #0x20]
0x52e30	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x52e34	ff430191	add	sp, sp, #0x50
0x52e38	c0035fd6	ret
0x52e3c	ff4301d1	sub	sp, sp, #0x50
0x52e40	f65702a9	stp	x22, x21, [sp, #0x20]
0x52e44	f44f03a9	stp	x20, x19, [sp, #0x30]
0x52e48	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x52e4c	fd030191	add	x29, sp, #0x40
0x52e50	f40300aa	mov	x20, x0
0x52e54	f30308aa	mov	x19, x8
0x52e58	e8f301b2	mov	x8, #-0x5555555555555556 ; =-6148914691236517206
0x52e5c	68a200a9	stp	x8, x8, [x19, #0x8]
0x52e60	680200f9	str	x8, [x19]
0x52e64	e00313aa	mov	x0, x19
0x52e68	1661ff97	bl	0x2b2c0 <_WeChatMain+0x11a54>
0x52e6c	08100590	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x52e70	09a56339	ldrb	w9, [x8, #0x8e9]
0x52e74	29010037	tbnz	w9, #0x0, 0x52e98 <_WeChatMain+0x3962c>
0x52e78	a92104f0	adrp	x9, 0x8489000 <_wxam_enc_uninit_10+0x8489000>
0x52e7c	20c543fd	ldr	d0, [x9, #0x788]
0x52e80	09100590	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x52e84	29912391	add	x9, x9, #0x8e4
0x52e88	200100bd	str	s0, [x9]
0x52e8c	3f110039	strb	wzr, [x9, #0x4]
0x52e90	29008052	mov	w9, #0x1                ; =1
0x52e94	09a52339	strb	w9, [x8, #0x8e9]
0x52e98	15100590	adrp	x21, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x52e9c	b5922391	add	x21, x21, #0x8e4
0x52ea0	e00315aa	mov	x0, x21
0x52ea4	d5bac395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x52ea8	f60300aa	mov	x22, x0
0x52eac	880240f9	ldr	x8, [x20]
0x52eb0	081140f9	ldr	x8, [x8, #0x20]
0x52eb4	e00314aa	mov	x0, x20
0x52eb8	00013fd6	blr	x8
0x52ebc	e8230091	add	x8, sp, #0x8
0x52ec0	66e0ff97	bl	0x4b058 <_WeChatMain+0x317ec>
0x52ec4	e3230091	add	x3, sp, #0x8
0x52ec8	e00313aa	mov	x0, x19
0x52ecc	e10315aa	mov	x1, x21
0x52ed0	e20316aa	mov	x2, x22
0x52ed4	e6520194	bl	0xa7a6c <_WeChatMain+0x8e200>
0x52ed8	e87fc039	ldrsb	w8, [sp, #0x1f]
0x52edc	a800f836	tbz	w8, #0x1f, 0x52ef0 <_WeChatMain+0x39684>
0x52ee0	e00740f9	ldr	x0, [sp, #0x8]
0x52ee4	e80f40f9	ldr	x8, [sp, #0x18]
0x52ee8	01f94092	and	x1, x8, #0x7fffffffffffffff
0x52eec	48b4c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x52ef0	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x52ef4	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x52ef8	f65742a9	ldp	x22, x21, [sp, #0x20]
0x52efc	ff430191	add	sp, sp, #0x50
0x52f00	c0035fd6	ret
0x52f04	210040b9	ldr	w1, [x1]
0x52f08	cab2c315	b	0x713fa30 <_wxam_enc_uninit_10+0x713fa30>
0x52f0c	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x52f10	f65701a9	stp	x22, x21, [sp, #0x10]
0x52f14	f44f02a9	stp	x20, x19, [sp, #0x20]
0x52f18	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x52f1c	fdc30091	add	x29, sp, #0x30
0x52f20	130c40f9	ldr	x19, [x0, #0x18]
0x52f24	f30200b4	cbz	x19, 0x52f80 <_WeChatMain+0x39714>
0x52f28	f40300aa	mov	x20, x0
0x52f2c	e00313aa	mov	x0, x19
0x52f30	f50303aa	mov	x21, x3
0x52f34	f60302aa	mov	x22, x2
0x52f38	f70301aa	mov	x23, x1
0x52f3c	d851ff97	bl	0x2769c <_WeChatMain+0xde30>
0x52f40	800e40f9	ldr	x0, [x20, #0x18]
0x52f44	080440f9	ldr	x8, [x0, #0x8]
0x52f48	e10317aa	mov	x1, x23
0x52f4c	e20316aa	mov	x2, x22
0x52f50	e30315aa	mov	x3, x21
0x52f54	00013fd6	blr	x8
0x52f58	08008012	mov	w8, #-0x1               ; =-1
0x52f5c	6802e8b8	ldaddal	w8, w8, [x19]
0x52f60	1f050071	cmp	w8, #0x1
0x52f64	e1010054	b.ne	0x52fa0 <_WeChatMain+0x39734>
0x52f68	e00313aa	mov	x0, x19
0x52f6c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x52f70	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x52f74	f65741a9	ldp	x22, x21, [sp, #0x10]
0x52f78	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x52f7c	2f83ff17	b	0x33c38 <_WeChatMain+0x1a3cc>
0x52f80	08018052	mov	w8, #0x8                ; =8
0x52f84	040140f9	ldr	x4, [x8]
0x52f88	000080d2	mov	x0, #0x0                ; =0
0x52f8c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x52f90	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x52f94	f65741a9	ldp	x22, x21, [sp, #0x10]
0x52f98	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x52f9c	80001fd6	br	x4
0x52fa0	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x52fa4	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x52fa8	f65741a9	ldp	x22, x21, [sp, #0x10]
0x52fac	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x52fb0	c0035fd6	ret
0x52fb4	ff8301d1	sub	sp, sp, #0x60
0x52fb8	f65703a9	stp	x22, x21, [sp, #0x30]
0x52fbc	f44f04a9	stp	x20, x19, [sp, #0x40]
0x52fc0	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x52fc4	fd430191	add	x29, sp, #0x50
0x52fc8	f30300aa	mov	x19, x0
0x52fcc	562605d0	adrp	x22, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x52fd0	d6222f91	add	x22, x22, #0xbc8
0x52fd4	d4c2bff8	ldapr	x20, [x22]
0x52fd8	9f0600f1	cmp	x20, #0x1
0x52fdc	08020054	b.hi	0x5301c <_WeChatMain+0x397b0>
0x52fe0	552605d0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x52fe4	b5222f91	add	x21, x21, #0xbc8
0x52fe8	e00315aa	mov	x0, x21
0x52fec	26a1ff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x52ff0	40010034	cbz	w0, 0x53018 <_WeChatMain+0x397ac>
0x52ff4	b4220091	add	x20, x21, #0x8
0x52ff8	e00314aa	mov	x0, x20
0x52ffc	f85c0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53000	e00315aa	mov	x0, x21
0x53004	e10314aa	mov	x1, x20
0x53008	020080d2	mov	x2, #0x0                ; =0
0x5300c	e30315aa	mov	x3, x21
0x53010	41a1ff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53014	02000014	b	0x5301c <_WeChatMain+0x397b0>
0x53018	b4c2bff8	ldapr	x20, [x21]
0x5301c	e00314aa	mov	x0, x20
0x53020	35b9c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x53024	200a0035	cbnz	w0, 0x53168 <_WeChatMain+0x398fc>
0x53028	c8c2bff8	ldapr	x8, [x22]
0x5302c	1f0500f1	cmp	x8, #0x1
0x53030	e8010054	b.hi	0x5306c <_WeChatMain+0x39800>
0x53034	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53038	b5222f91	add	x21, x21, #0xbc8
0x5303c	e00315aa	mov	x0, x21
0x53040	11a1ff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53044	20010034	cbz	w0, 0x53068 <_WeChatMain+0x397fc>
0x53048	a0220091	add	x0, x21, #0x8
0x5304c	e45c0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53050	a1220091	add	x1, x21, #0x8
0x53054	e00315aa	mov	x0, x21
0x53058	020080d2	mov	x2, #0x0                ; =0
0x5305c	e30315aa	mov	x3, x21
0x53060	2da1ff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53064	02000014	b	0x5306c <_WeChatMain+0x39800>
0x53068	bfc2bff8	ldapr	xzr, [x21]
0x5306c	562605b0	adrp	x22, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53070	d50a46f9	ldr	x21, [x22, #0xc10]
0x53074	b50000b5	cbnz	x21, 0x53088 <_WeChatMain+0x3981c>
0x53078	00158052	mov	w0, #0xa8               ; =168
0x5307c	edb3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x53080	86040094	bl	0x54298 <_WeChatMain+0x3aa2c>
0x53084	d50a46f9	ldr	x21, [x22, #0xc10]
0x53088	600640f9	ldr	x0, [x19, #0x8]
0x5308c	e00f00f9	str	x0, [sp, #0x18]
0x53090	e00700f9	str	x0, [sp, #0x8]
0x53094	800000b4	cbz	x0, 0x530a4 <_WeChatMain+0x39838>
0x53098	58bac395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x5309c	e00b00f9	str	x0, [sp, #0x10]
0x530a0	0b000014	b	0x530cc <_WeChatMain+0x39860>
0x530a4	ff0b00f9	str	xzr, [sp, #0x10]
0x530a8	40bf04b0	adrp	x0, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x530ac	00800791	add	x0, x0, #0x1e0
0x530b0	42bf04b0	adrp	x2, 0x983c000 <_wxam_enc_uninit_10+0x983c000>
0x530b4	42300991	add	x2, x2, #0x24c
0x530b8	e8a30091	add	x8, sp, #0x28
0x530bc	a10f8052	mov	w1, #0x7d               ; =125
0x530c0	8139ff97	bl	0x216c4 <_WeChatMain+0x7e58>
0x530c4	e0a30091	add	x0, sp, #0x28
0x530c8	e91dff97	bl	0x1a86c <_WeChatMain+0x1000>
0x530cc	e8230091	add	x8, sp, #0x8
0x530d0	e81700f9	str	x8, [sp, #0x28]
0x530d4	225904f0	adrp	x2, 0x8b7a000 <_wxam_enc_uninit_10+0x8b7a000>
0x530d8	42e02291	add	x2, x2, #0x8b8
0x530dc	e1230091	add	x1, sp, #0x8
0x530e0	e3a30091	add	x3, sp, #0x28
0x530e4	e49f0091	add	x4, sp, #0x27
0x530e8	e00315aa	mov	x0, x21
0x530ec	9d0b0094	bl	0x55f60 <_WeChatMain+0x3c6f4>
0x530f0	151040f9	ldr	x21, [x0, #0x20]
0x530f4	950100b4	cbz	x21, 0x53124 <_WeChatMain+0x398b8>
0x530f8	bf0213eb	cmp	x21, x19
0x530fc	60020054	b.eq	0x53148 <_WeChatMain+0x398dc>
0x53100	e00314aa	mov	x0, x20
0x53104	ffb8c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x53108	b30000b4	cbz	x19, 0x5311c <_WeChatMain+0x398b0>
0x5310c	680240f9	ldr	x8, [x19]
0x53110	080540f9	ldr	x8, [x8, #0x8]
0x53114	e00313aa	mov	x0, x19
0x53118	00013fd6	blr	x8
0x5311c	f30315aa	mov	x19, x21
0x53120	0c000014	b	0x53150 <_WeChatMain+0x398e4>
0x53124	131000f9	str	x19, [x0, #0x20]
0x53128	c80a46f9	ldr	x8, [x22, #0xc10]
0x5312c	00a10091	add	x0, x8, #0x28
0x53130	e1630091	add	x1, sp, #0x18
0x53134	95040094	bl	0x54388 <_WeChatMain+0x3ab1c>
0x53138	80000034	cbz	w0, 0x53148 <_WeChatMain+0x398dc>
0x5313c	e00313aa	mov	x0, x19
0x53140	01048052	mov	w1, #0x20               ; =32
0x53144	eae0ff97	bl	0x4b4ec <_WeChatMain+0x31c80>
0x53148	e00314aa	mov	x0, x20
0x5314c	edb8c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x53150	e00313aa	mov	x0, x19
0x53154	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x53158	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x5315c	f65743a9	ldp	x22, x21, [sp, #0x30]
0x53160	ff830191	add	sp, sp, #0x60
0x53164	c0035fd6	ret
0x53168	e00314aa	mov	x0, x20
0x5316c	c65c0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x53170	aeffff17	b	0x53028 <_WeChatMain+0x397bc>
0x53174	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x53178	f44f01a9	stp	x20, x19, [sp, #0x10]
0x5317c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x53180	fd830091	add	x29, sp, #0x20
0x53184	f30300aa	mov	x19, x0
0x53188	562605b0	adrp	x22, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x5318c	d6222f91	add	x22, x22, #0xbc8
0x53190	d4c2bff8	ldapr	x20, [x22]
0x53194	9f0600f1	cmp	x20, #0x1
0x53198	08020054	b.hi	0x531d8 <_WeChatMain+0x3996c>
0x5319c	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x531a0	b5222f91	add	x21, x21, #0xbc8
0x531a4	e00315aa	mov	x0, x21
0x531a8	b7a0ff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x531ac	40010034	cbz	w0, 0x531d4 <_WeChatMain+0x39968>
0x531b0	b4220091	add	x20, x21, #0x8
0x531b4	e00314aa	mov	x0, x20
0x531b8	895c0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x531bc	e00315aa	mov	x0, x21
0x531c0	e10314aa	mov	x1, x20
0x531c4	020080d2	mov	x2, #0x0                ; =0
0x531c8	e30315aa	mov	x3, x21
0x531cc	d2a0ff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x531d0	02000014	b	0x531d8 <_WeChatMain+0x3996c>
0x531d4	b4c2bff8	ldapr	x20, [x21]
0x531d8	e00314aa	mov	x0, x20
0x531dc	c6b8c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x531e0	80040035	cbnz	w0, 0x53270 <_WeChatMain+0x39a04>
0x531e4	c8c2bff8	ldapr	x8, [x22]
0x531e8	1f0500f1	cmp	x8, #0x1
0x531ec	e8010054	b.hi	0x53228 <_WeChatMain+0x399bc>
0x531f0	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x531f4	b5222f91	add	x21, x21, #0xbc8
0x531f8	e00315aa	mov	x0, x21
0x531fc	a2a0ff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53200	20010034	cbz	w0, 0x53224 <_WeChatMain+0x399b8>
0x53204	a0220091	add	x0, x21, #0x8
0x53208	755c0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x5320c	a1220091	add	x1, x21, #0x8
0x53210	e00315aa	mov	x0, x21
0x53214	020080d2	mov	x2, #0x0                ; =0
0x53218	e30315aa	mov	x3, x21
0x5321c	bea0ff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53220	02000014	b	0x53228 <_WeChatMain+0x399bc>
0x53224	bfc2bff8	ldapr	xzr, [x21]
0x53228	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x5322c	a80a46f9	ldr	x8, [x21, #0xc10]
0x53230	a80000b5	cbnz	x8, 0x53244 <_WeChatMain+0x399d8>
0x53234	00158052	mov	w0, #0xa8               ; =168
0x53238	7eb3c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x5323c	17040094	bl	0x54298 <_WeChatMain+0x3aa2c>
0x53240	a80a46f9	ldr	x8, [x21, #0xc10]
0x53244	00a10191	add	x0, x8, #0x68
0x53248	e10313aa	mov	x1, x19
0x5324c	55f2ff97	bl	0x4fba0 <_WeChatMain+0x36334>
0x53250	f30300aa	mov	x19, x0
0x53254	e00314aa	mov	x0, x20
0x53258	aab8c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x5325c	e00313aa	mov	x0, x19
0x53260	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x53264	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x53268	f657c3a8	ldp	x22, x21, [sp], #0x30
0x5326c	c0035fd6	ret
0x53270	e00314aa	mov	x0, x20
0x53274	845c0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x53278	dbffff17	b	0x531e4 <_WeChatMain+0x39978>
0x5327c	ff0303d1	sub	sp, sp, #0xc0
0x53280	fc6f06a9	stp	x28, x27, [sp, #0x60]
0x53284	fa6707a9	stp	x26, x25, [sp, #0x70]
0x53288	f85f08a9	stp	x24, x23, [sp, #0x80]
0x5328c	f65709a9	stp	x22, x21, [sp, #0x90]
0x53290	f44f0aa9	stp	x20, x19, [sp, #0xa0]
0x53294	fd7b0ba9	stp	x29, x30, [sp, #0xb0]
0x53298	fdc30291	add	x29, sp, #0xb0
0x5329c	f90301aa	mov	x25, x1
0x532a0	f40300aa	mov	x20, x0
0x532a4	095cc039	ldrsb	w9, [x0, #0x17]
0x532a8	8900f837	tbnz	w9, #0x1f, 0x532b8 <_WeChatMain+0x39a4c>
0x532ac	e80314aa	mov	x8, x20
0x532b0	a9000035	cbnz	w9, 0x532c4 <_WeChatMain+0x39a58>
0x532b4	2a000014	b	0x5335c <_WeChatMain+0x39af0>
0x532b8	880640f9	ldr	x8, [x20, #0x8]
0x532bc	080500b4	cbz	x8, 0x5335c <_WeChatMain+0x39af0>
0x532c0	880240f9	ldr	x8, [x20]
0x532c4	e90f05f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x532c8	2a496439	ldrb	w10, [x9, #0x912]
0x532cc	ca030037	tbnz	w10, #0x0, 0x53344 <_WeChatMain+0x39ad8>
0x532d0	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x532d4	409144fd	ldr	d0, [x10, #0x920]
0x532d8	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x532dc	419544fd	ldr	d1, [x10, #0x928]
0x532e0	20040c6e	mov.s	v0[1], v1[0]
0x532e4	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x532e8	419944fd	ldr	d1, [x10, #0x930]
0x532ec	2004146e	mov.s	v0[2], v1[0]
0x532f0	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x532f4	419d44fd	ldr	d1, [x10, #0x938]
0x532f8	20041c6e	mov.s	v0[3], v1[0]
0x532fc	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53300	418940fd	ldr	d1, [x10, #0x110]
0x53304	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53308	428d40fd	ldr	d2, [x10, #0x118]
0x5330c	41040c6e	mov.s	v1[1], v2[0]
0x53310	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53314	42a144fd	ldr	d2, [x10, #0x940]
0x53318	4104146e	mov.s	v1[2], v2[0]
0x5331c	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53320	42a544fd	ldr	d2, [x10, #0x948]
0x53324	41041c6e	mov.s	v1[3], v2[0]
0x53328	ea0f05f0	adrp	x10, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5332c	4ac12391	add	x10, x10, #0x8f0
0x53330	400500ad	stp	q0, q1, [x10]
0x53334	4b018052	mov	w11, #0xa               ; =10
0x53338	4b410079	strh	w11, [x10, #0x20]
0x5333c	2a008052	mov	w10, #0x1               ; =1
0x53340	2a492439	strb	w10, [x9, #0x912]
0x53344	e80300f9	str	x8, [sp]
0x53348	e10f05f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5334c	21c02391	add	x1, x1, #0x8f0
0x53350	e00319aa	mov	x0, x25
0x53354	d1530094	bl	0x68298 <_WeChatMain+0x4ea2c>
0x53358	4b000014	b	0x53484 <_WeChatMain+0x39c18>
0x5335c	e80f05f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53360	09cd6439	ldrb	w9, [x8, #0x933]
0x53364	a9030037	tbnz	w9, #0x0, 0x533d8 <_WeChatMain+0x39b6c>
0x53368	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5336c	209144fd	ldr	d0, [x9, #0x920]
0x53370	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53374	219544fd	ldr	d1, [x9, #0x928]
0x53378	20040c6e	mov.s	v0[1], v1[0]
0x5337c	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53380	219944fd	ldr	d1, [x9, #0x930]
0x53384	2004146e	mov.s	v0[2], v1[0]
0x53388	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x5338c	21a944fd	ldr	d1, [x9, #0x950]
0x53390	20041c6e	mov.s	v0[3], v1[0]
0x53394	e90f05f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53398	29512491	add	x9, x9, #0x914
0x5339c	2001803d	str	q0, [x9]
0x533a0	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x533a4	40ad44fd	ldr	d0, [x10, #0x958]
0x533a8	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x533ac	418940fd	ldr	d1, [x10, #0x110]
0x533b0	20040c6e	mov.s	v0[1], v1[0]
0x533b4	200900fd	str	d0, [x9, #0x10]
0x533b8	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x533bc	408d40fd	ldr	d0, [x10, #0x118]
0x533c0	201900bd	str	s0, [x9, #0x18]
0x533c4	6a4e8152	mov	w10, #0xa73             ; =2675
0x533c8	2a390079	strh	w10, [x9, #0x1c]
0x533cc	3f790039	strb	wzr, [x9, #0x1e]
0x533d0	29008052	mov	w9, #0x1                ; =1
0x533d4	09cd2439	strb	w9, [x8, #0x933]
0x533d8	e00f05f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x533dc	00502491	add	x0, x0, #0x914
0x533e0	86b9c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x533e4	f50300aa	mov	x21, x0
0x533e8	285f8039	ldrsb	x8, [x25, #0x17]
0x533ec	8800f8b7	tbnz	x8, #0x3f, 0x533fc <_WeChatMain+0x39b90>
0x533f0	c1028052	mov	w1, #0x16               ; =22
0x533f4	f60308aa	mov	x22, x8
0x533f8	04000014	b	0x53408 <_WeChatMain+0x39b9c>
0x533fc	36a740a9	ldp	x22, x9, [x25, #0x8]
0x53400	29f94092	and	x9, x9, #0x7fffffffffffffff
0x53404	210500d1	sub	x1, x9, #0x1
0x53408	290016cb	sub	x9, x1, x22
0x5340c	3f0115eb	cmp	x9, x21
0x53410	82010054	b.hs	0x53440 <_WeChatMain+0x39bd4>
0x53414	a80201cb	sub	x8, x21, x1
0x53418	e70f05f0	adrp	x7, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x5341c	e7502491	add	x7, x7, #0x914
0x53420	0201168b	add	x2, x8, x22
0x53424	e00319aa	mov	x0, x25
0x53428	e30316aa	mov	x3, x22
0x5342c	e40316aa	mov	x4, x22
0x53430	050080d2	mov	x5, #0x0                ; =0
0x53434	e60315aa	mov	x6, x21
0x53438	dfb0c395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x5343c	12000014	b	0x53484 <_WeChatMain+0x39c18>
0x53440	350200b4	cbz	x21, 0x53484 <_WeChatMain+0x39c18>
0x53444	f70319aa	mov	x23, x25
0x53448	4800f836	tbz	w8, #0x1f, 0x53450 <_WeChatMain+0x39be4>
0x5344c	370340f9	ldr	x23, [x25]
0x53450	e10f05f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53454	21502491	add	x1, x1, #0x914
0x53458	e002168b	add	x0, x23, x22
0x5345c	e20315aa	mov	x2, x21
0x53460	8db6c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x53464	c802158b	add	x8, x22, x21
0x53468	295fc039	ldrsb	w9, [x25, #0x17]
0x5346c	8900f837	tbnz	w9, #0x1f, 0x5347c <_WeChatMain+0x39c10>
0x53470	09190012	and	w9, w8, #0x7f
0x53474	295f0039	strb	w9, [x25, #0x17]
0x53478	02000014	b	0x53480 <_WeChatMain+0x39c14>
0x5347c	280700f9	str	x8, [x25, #0x8]
0x53480	ff6a2838	strb	wzr, [x23, x8]
0x53484	e8830091	add	x8, sp, #0x20
0x53488	96000094	bl	0x536e0 <_WeChatMain+0x39e74>
0x5348c	885ec039	ldrsb	w8, [x20, #0x17]
0x53490	890240f9	ldr	x9, [x20]
0x53494	1f010071	cmp	w8, #0x0
0x53498	37b1949a	csel	x23, x9, x20, lt
0x5349c	f35342a9	ldp	x19, x20, [sp, #0x20]
0x534a0	f60313aa	mov	x22, x19
0x534a4	7f0214eb	cmp	x19, x20
0x534a8	60030054	b.eq	0x53514 <_WeChatMain+0x39ca8>
0x534ac	c80240f9	ldr	x8, [x22]
0x534b0	000540f9	ldr	x0, [x8, #0x8]
0x534b4	e10317aa	mov	x1, x23
0x534b8	6bb9c395	bl	0x7141a64 <_wxam_enc_uninit_10+0x7141a64>
0x534bc	a00000b4	cbz	x0, 0x534d0 <_WeChatMain+0x39c64>
0x534c0	d6220091	add	x22, x22, #0x8
0x534c4	df0214eb	cmp	x22, x20
0x534c8	21ffff54	b.ne	0x534ac <_WeChatMain+0x39c40>
0x534cc	1d000014	b	0x53540 <_WeChatMain+0x39cd4>
0x534d0	df0214eb	cmp	x22, x20
0x534d4	00020054	b.eq	0x53514 <_WeChatMain+0x39ca8>
0x534d8	d5220091	add	x21, x22, #0x8
0x534dc	bf0214eb	cmp	x21, x20
0x534e0	a1000054	b.ne	0x534f4 <_WeChatMain+0x39c88>
0x534e4	0c000014	b	0x53514 <_WeChatMain+0x39ca8>
0x534e8	b5220091	add	x21, x21, #0x8
0x534ec	bf0214eb	cmp	x21, x20
0x534f0	00010054	b.eq	0x53510 <_WeChatMain+0x39ca4>
0x534f4	b30240f9	ldr	x19, [x21]
0x534f8	600640f9	ldr	x0, [x19, #0x8]
0x534fc	e10317aa	mov	x1, x23
0x53500	59b9c395	bl	0x7141a64 <_wxam_enc_uninit_10+0x7141a64>
0x53504	20ffffb4	cbz	x0, 0x534e8 <_WeChatMain+0x39c7c>
0x53508	d38600f8	str	x19, [x22], #0x8
0x5350c	f7ffff17	b	0x534e8 <_WeChatMain+0x39c7c>
0x53510	f35342a9	ldp	x19, x20, [sp, #0x20]
0x53514	df0214eb	cmp	x22, x20
0x53518	40010054	b.eq	0x53540 <_WeChatMain+0x39cd4>
0x5351c	880216cb	sub	x8, x20, x22
0x53520	c102088b	add	x1, x22, x8
0x53524	940201eb	subs	x20, x20, x1
0x53528	a0000054	b.eq	0x5353c <_WeChatMain+0x39cd0>
0x5352c	e00316aa	mov	x0, x22
0x53530	e20314aa	mov	x2, x20
0x53534	58b6c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x53538	f31340f9	ldr	x19, [sp, #0x20]
0x5353c	d402148b	add	x20, x22, x20
0x53540	880213eb	subs	x8, x20, x19
0x53544	08fd4393	asr	x8, x8, #3
0x53548	0811c0da	clz	x8, x8
0x5354c	e91b40f9	ldr	x9, [sp, #0x30]
0x53550	e90b00f9	str	x9, [sp, #0x10]
0x53554	c90f8052	mov	w9, #0x7e               ; =126
0x53558	280508cb	sub	x8, x9, x8, lsl #1
0x5355c	ff7f02a9	stp	xzr, xzr, [sp, #0x20]
0x53560	090000b0	adrp	x9, 0x54000 <_WeChatMain+0x3a794>
0x53564	2be10991	add	x11, x9, #0x278
0x53568	e9430191	add	x9, sp, #0x50
0x5356c	aa4701d1	sub	x10, x29, #0x51
0x53570	ff2703a9	stp	xzr, x9, [sp, #0x30]
0x53574	ea2300f9	str	x10, [sp, #0x40]
0x53578	eaaf04a9	stp	x10, x11, [sp, #0x48]
0x5357c	9f0213eb	cmp	x20, x19
0x53580	e303889a	csel	x3, xzr, x8, eq
0x53584	e2e30091	add	x2, sp, #0x38
0x53588	e00313aa	mov	x0, x19
0x5358c	e10314aa	mov	x1, x20
0x53590	24008052	mov	w4, #0x1                ; =1
0x53594	2d050094	bl	0x54a48 <_WeChatMain+0x3b1dc>
0x53598	e01340f9	ldr	x0, [sp, #0x20]
0x5359c	a00000b4	cbz	x0, 0x535b0 <_WeChatMain+0x39d44>
0x535a0	e01700f9	str	x0, [sp, #0x28]
0x535a4	e81b40f9	ldr	x8, [sp, #0x30]
0x535a8	010100cb	sub	x1, x8, x0
0x535ac	98b2c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x535b0	f30f00f9	str	x19, [sp, #0x18]
0x535b4	9f0213eb	cmp	x20, x19
0x535b8	a0070054	b.eq	0x536ac <_WeChatMain+0x39e40>
0x535bc	fa0f05f0	adrp	x26, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x535c0	5b018052	mov	w27, #0xa               ; =10
0x535c4	3c008052	mov	w28, #0x1               ; =1
0x535c8	f50f40f9	ldr	x21, [sp, #0x18]
0x535cc	f60f05f0	adrp	x22, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x535d0	d6d22491	add	x22, x22, #0x934
0x535d4	0d000014	b	0x53608 <_WeChatMain+0x39d9c>
0x535d8	e80201cb	sub	x8, x23, x1
0x535dc	0201188b	add	x2, x8, x24
0x535e0	e00319aa	mov	x0, x25
0x535e4	e30318aa	mov	x3, x24
0x535e8	e40318aa	mov	x4, x24
0x535ec	050080d2	mov	x5, #0x0                ; =0
0x535f0	e60317aa	mov	x6, x23
0x535f4	e70316aa	mov	x7, x22
0x535f8	6fb0c395	bl	0x713f7b4 <_wxam_enc_uninit_10+0x713f7b4>
0x535fc	b5220091	add	x21, x21, #0x8
0x53600	bf0214eb	cmp	x21, x20
0x53604	40050054	b.eq	0x536ac <_WeChatMain+0x39e40>
0x53608	a00240f9	ldr	x0, [x21]
0x5360c	080040f9	ldr	x8, [x0]
0x53610	083940f9	ldr	x8, [x8, #0x70]
0x53614	e10319aa	mov	x1, x25
0x53618	00013fd6	blr	x8
0x5361c	48db6439	ldrb	w8, [x26, #0x936]
0x53620	68000037	tbnz	w8, #0x0, 0x5362c <_WeChatMain+0x39dc0>
0x53624	db020079	strh	w27, [x22]
0x53628	5cdb2439	strb	w28, [x26, #0x936]
0x5362c	e00316aa	mov	x0, x22
0x53630	f2b8c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x53634	f70300aa	mov	x23, x0
0x53638	285f8039	ldrsb	x8, [x25, #0x17]
0x5363c	8800f8b7	tbnz	x8, #0x3f, 0x5364c <_WeChatMain+0x39de0>
0x53640	c1028052	mov	w1, #0x16               ; =22
0x53644	f80308aa	mov	x24, x8
0x53648	04000014	b	0x53658 <_WeChatMain+0x39dec>
0x5364c	38a740a9	ldp	x24, x9, [x25, #0x8]
0x53650	29f94092	and	x9, x9, #0x7fffffffffffffff
0x53654	210500d1	sub	x1, x9, #0x1
0x53658	290018cb	sub	x9, x1, x24
0x5365c	3f0117eb	cmp	x9, x23
0x53660	c3fbff54	b.lo	0x535d8 <_WeChatMain+0x39d6c>
0x53664	d7fcffb4	cbz	x23, 0x535fc <_WeChatMain+0x39d90>
0x53668	f30319aa	mov	x19, x25
0x5366c	4800f836	tbz	w8, #0x1f, 0x53674 <_WeChatMain+0x39e08>
0x53670	330340f9	ldr	x19, [x25]
0x53674	6002188b	add	x0, x19, x24
0x53678	e10316aa	mov	x1, x22
0x5367c	e20317aa	mov	x2, x23
0x53680	05b6c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x53684	0803178b	add	x8, x24, x23
0x53688	295fc039	ldrsb	w9, [x25, #0x17]
0x5368c	a900f837	tbnz	w9, #0x1f, 0x536a0 <_WeChatMain+0x39e34>
0x53690	09190012	and	w9, w8, #0x7f
0x53694	295f0039	strb	w9, [x25, #0x17]
0x53698	7f6a2838	strb	wzr, [x19, x8]
0x5369c	d8ffff17	b	0x535fc <_WeChatMain+0x39d90>
0x536a0	280700f9	str	x8, [x25, #0x8]
0x536a4	7f6a2838	strb	wzr, [x19, x8]
0x536a8	d5ffff17	b	0x535fc <_WeChatMain+0x39d90>
0x536ac	e00f40f9	ldr	x0, [sp, #0x18]
0x536b0	800000b4	cbz	x0, 0x536c0 <_WeChatMain+0x39e54>
0x536b4	e80b40f9	ldr	x8, [sp, #0x10]
0x536b8	010100cb	sub	x1, x8, x0
0x536bc	54b2c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x536c0	fd7b4ba9	ldp	x29, x30, [sp, #0xb0]
0x536c4	f44f4aa9	ldp	x20, x19, [sp, #0xa0]
0x536c8	f65749a9	ldp	x22, x21, [sp, #0x90]
0x536cc	f85f48a9	ldp	x24, x23, [sp, #0x80]
0x536d0	fa6747a9	ldp	x26, x25, [sp, #0x70]
0x536d4	fc6f46a9	ldp	x28, x27, [sp, #0x60]
0x536d8	ff030391	add	sp, sp, #0xc0
0x536dc	c0035fd6	ret
0x536e0	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x536e4	f85f01a9	stp	x24, x23, [sp, #0x10]
0x536e8	f65702a9	stp	x22, x21, [sp, #0x20]
0x536ec	f44f03a9	stp	x20, x19, [sp, #0x30]
0x536f0	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x536f4	fd030191	add	x29, sp, #0x40
0x536f8	f30308aa	mov	x19, x8
0x536fc	88eaff97	bl	0x4e11c <_WeChatMain+0x348b0>
0x53700	400000b4	cbz	x0, 0x53708 <_WeChatMain+0x39e9c>
0x53704	8aeaff97	bl	0x4e12c <_WeChatMain+0x348c0>
0x53708	7f7e00a9	stp	xzr, xzr, [x19]
0x5370c	7f0a00f9	str	xzr, [x19, #0x10]
0x53710	562605b0	adrp	x22, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53714	d6222f91	add	x22, x22, #0xbc8
0x53718	d4c2bff8	ldapr	x20, [x22]
0x5371c	9f0600f1	cmp	x20, #0x1
0x53720	08020054	b.hi	0x53760 <_WeChatMain+0x39ef4>
0x53724	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53728	b5222f91	add	x21, x21, #0xbc8
0x5372c	e00315aa	mov	x0, x21
0x53730	559fff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53734	40010034	cbz	w0, 0x5375c <_WeChatMain+0x39ef0>
0x53738	b4220091	add	x20, x21, #0x8
0x5373c	e00314aa	mov	x0, x20
0x53740	275b0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53744	e00315aa	mov	x0, x21
0x53748	e10314aa	mov	x1, x20
0x5374c	020080d2	mov	x2, #0x0                ; =0
0x53750	e30315aa	mov	x3, x21
0x53754	709fff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53758	02000014	b	0x53760 <_WeChatMain+0x39ef4>
0x5375c	b4c2bff8	ldapr	x20, [x21]
0x53760	e00314aa	mov	x0, x20
0x53764	64b7c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x53768	c0150035	cbnz	w0, 0x53a20 <_WeChatMain+0x3a1b4>
0x5376c	c8c2bff8	ldapr	x8, [x22]
0x53770	1f0500f1	cmp	x8, #0x1
0x53774	e8010054	b.hi	0x537b0 <_WeChatMain+0x39f44>
0x53778	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x5377c	b5222f91	add	x21, x21, #0xbc8
0x53780	e00315aa	mov	x0, x21
0x53784	409fff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53788	20010034	cbz	w0, 0x537ac <_WeChatMain+0x39f40>
0x5378c	a0220091	add	x0, x21, #0x8
0x53790	135b0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53794	a1220091	add	x1, x21, #0x8
0x53798	e00315aa	mov	x0, x21
0x5379c	020080d2	mov	x2, #0x0                ; =0
0x537a0	e30315aa	mov	x3, x21
0x537a4	5c9fff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x537a8	02000014	b	0x537b0 <_WeChatMain+0x39f44>
0x537ac	bfc2bff8	ldapr	xzr, [x21]
0x537b0	582605b0	adrp	x24, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x537b4	190b46f9	ldr	x25, [x24, #0xc10]
0x537b8	b90000b5	cbnz	x25, 0x537cc <_WeChatMain+0x39f60>
0x537bc	00158052	mov	w0, #0xa8               ; =168
0x537c0	1cb2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x537c4	b5020094	bl	0x54298 <_WeChatMain+0x3aa2c>
0x537c8	190b46f9	ldr	x25, [x24, #0xc10]
0x537cc	280f40f9	ldr	x8, [x25, #0x18]
0x537d0	690a40f9	ldr	x9, [x19, #0x10]
0x537d4	750240f9	ldr	x21, [x19]
0x537d8	360115cb	sub	x22, x9, x21
0x537dc	1f0d96eb	cmp	x8, x22, asr #3
0x537e0	a9060054	b.ls	0x538b4 <_WeChatMain+0x3a048>
0x537e4	09fd7dd3	lsr	x9, x8, #61
0x537e8	291200b5	cbnz	x9, 0x53a2c <_WeChatMain+0x3a1c0>
0x537ec	7a0640f9	ldr	x26, [x19, #0x8]
0x537f0	17f17dd3	lsl	x23, x8, #3
0x537f4	e00317aa	mov	x0, x23
0x537f8	0eb2c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x537fc	4b0315eb	subs	x11, x26, x21
0x53800	08000b8b	add	x8, x0, x11
0x53804	0900178b	add	x9, x0, x23
0x53808	ea0308aa	mov	x10, x8
0x5380c	60040054	b.eq	0x53898 <_WeChatMain+0x3a02c>
0x53810	6b2100d1	sub	x11, x11, #0x8
0x53814	7fe100f1	cmp	x11, #0x38
0x53818	63030054	b.lo	0x53884 <_WeChatMain+0x3a018>
0x5381c	ac0200cb	sub	x12, x21, x0
0x53820	ea0308aa	mov	x10, x8
0x53824	9f0101f1	cmp	x12, #0x40
0x53828	03030054	b.lo	0x53888 <_WeChatMain+0x3a01c>
0x5382c	6afd43d3	lsr	x10, x11, #3
0x53830	4b050091	add	x11, x10, #0x1
0x53834	6ce97d92	and	x12, x11, #0x3ffffffffffffff8
0x53838	8af17dd3	lsl	x10, x12, #3
0x5383c	4d030acb	sub	x13, x26, x10
0x53840	0a010acb	sub	x10, x8, x10
0x53844	4e8300d1	sub	x14, x26, #0x20
0x53848	cf0115cb	sub	x15, x14, x21
0x5384c	0f000f8b	add	x15, x0, x15
0x53850	f0030caa	mov	x16, x12
0x53854	c10140ad	ldp	q1, q0, [x14]
0x53858	c3097fad	ldp	q3, q2, [x14, #-0x20]
0x5385c	e10100ad	stp	q1, q0, [x15]
0x53860	e3093fad	stp	q3, q2, [x15, #-0x20]
0x53864	ce0101d1	sub	x14, x14, #0x40
0x53868	ef0101d1	sub	x15, x15, #0x40
0x5386c	102200d1	sub	x16, x16, #0x8
0x53870	30ffffb5	cbnz	x16, 0x53854 <_WeChatMain+0x39fe8>
0x53874	fa030daa	mov	x26, x13
0x53878	7f010ceb	cmp	x11, x12
0x5387c	61000054	b.ne	0x53888 <_WeChatMain+0x3a01c>
0x53880	06000014	b	0x53898 <_WeChatMain+0x3a02c>
0x53884	ea0308aa	mov	x10, x8
0x53888	4b8f5ff8	ldr	x11, [x26, #-0x8]!
0x5388c	4b8d1ff8	str	x11, [x10, #-0x8]!
0x53890	5f0315eb	cmp	x26, x21
0x53894	a1ffff54	b.ne	0x53888 <_WeChatMain+0x3a01c>
0x53898	6a2200a9	stp	x10, x8, [x19]
0x5389c	690a00f9	str	x9, [x19, #0x10]
0x538a0	b50000b4	cbz	x21, 0x538b4 <_WeChatMain+0x3a048>
0x538a4	e00315aa	mov	x0, x21
0x538a8	e10316aa	mov	x1, x22
0x538ac	d8b1c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x538b0	190b46f9	ldr	x25, [x24, #0xc10]
0x538b4	350b40f9	ldr	x21, [x25, #0x10]
0x538b8	750a00b4	cbz	x21, 0x53a04 <_WeChatMain+0x3a198>
0x538bc	780640f9	ldr	x24, [x19, #0x8]
0x538c0	f6ef7db2	mov	x22, #0x7ffffffffffffff8 ; =9223372036854775800
0x538c4	1700fc92	mov	x23, #0x1fffffffffffffff ; =2305843009213693951
0x538c8	06000014	b	0x538e0 <_WeChatMain+0x3a074>
0x538cc	a81240f9	ldr	x8, [x21, #0x20]
0x538d0	088700f8	str	x8, [x24], #0x8
0x538d4	780600f9	str	x24, [x19, #0x8]
0x538d8	b50240f9	ldr	x21, [x21]
0x538dc	550900b4	cbz	x21, 0x53a04 <_WeChatMain+0x3a198>
0x538e0	680a40f9	ldr	x8, [x19, #0x10]
0x538e4	1f0308eb	cmp	x24, x8
0x538e8	23ffff54	b.lo	0x538cc <_WeChatMain+0x3a060>
0x538ec	690240f9	ldr	x9, [x19]
0x538f0	1a0309cb	sub	x26, x24, x9
0x538f4	58ff4393	asr	x24, x26, #3
0x538f8	0a070091	add	x10, x24, #0x1
0x538fc	4bfd7dd3	lsr	x11, x10, #61
0x53900	6b0900b5	cbnz	x11, 0x53a2c <_WeChatMain+0x3a1c0>
0x53904	080109cb	sub	x8, x8, x9
0x53908	09fd4293	asr	x9, x8, #2
0x5390c	3f010aeb	cmp	x9, x10
0x53910	29818a9a	csel	x9, x9, x10, hi
0x53914	1f0116eb	cmp	x8, x22
0x53918	3931979a	csel	x25, x9, x23, lo
0x5391c	d90000b4	cbz	x25, 0x53934 <_WeChatMain+0x3a0c8>
0x53920	28ff7dd3	lsr	x8, x25, #61
0x53924	880800b5	cbnz	x8, 0x53a34 <_WeChatMain+0x3a1c8>
0x53928	20f37dd3	lsl	x0, x25, #3
0x5392c	c1b1c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x53930	02000014	b	0x53938 <_WeChatMain+0x3a0cc>
0x53934	000080d2	mov	x0, #0x0                ; =0
0x53938	0a0c188b	add	x10, x0, x24, lsl #3
0x5393c	a81240f9	ldr	x8, [x21, #0x20]
0x53940	f8030aaa	mov	x24, x10
0x53944	088700f8	str	x8, [x24], #0x8
0x53948	682e40a9	ldp	x8, x11, [x19]
0x5394c	690108eb	subs	x9, x11, x8
0x53950	80040054	b.eq	0x539e0 <_WeChatMain+0x3a174>
0x53954	292100d1	sub	x9, x9, #0x8
0x53958	3fe100f1	cmp	x9, #0x38
0x5395c	43030054	b.lo	0x539c4 <_WeChatMain+0x3a158>
0x53960	6c0100cb	sub	x12, x11, x0
0x53964	8c011acb	sub	x12, x12, x26
0x53968	9f0101f1	cmp	x12, #0x40
0x5396c	c3020054	b.lo	0x539c4 <_WeChatMain+0x3a158>
0x53970	29fd43d3	lsr	x9, x9, #3
0x53974	2c050091	add	x12, x9, #0x1
0x53978	8de97d92	and	x13, x12, #0x3ffffffffffffff8
0x5397c	a9f17dd3	lsl	x9, x13, #3
0x53980	6e0109cb	sub	x14, x11, x9
0x53984	490109cb	sub	x9, x10, x9
0x53988	6b8100d1	sub	x11, x11, #0x20
0x5398c	4a8100d1	sub	x10, x10, #0x20
0x53990	ef030daa	mov	x15, x13
0x53994	610140ad	ldp	q1, q0, [x11]
0x53998	63097fad	ldp	q3, q2, [x11, #-0x20]
0x5399c	410100ad	stp	q1, q0, [x10]
0x539a0	43093fad	stp	q3, q2, [x10, #-0x20]
0x539a4	6b0101d1	sub	x11, x11, #0x40
0x539a8	4a0101d1	sub	x10, x10, #0x40
0x539ac	ef2100d1	sub	x15, x15, #0x8
0x539b0	2fffffb5	cbnz	x15, 0x53994 <_WeChatMain+0x3a128>
0x539b4	eb030eaa	mov	x11, x14
0x539b8	ea0309aa	mov	x10, x9
0x539bc	9f010deb	cmp	x12, x13
0x539c0	c0000054	b.eq	0x539d8 <_WeChatMain+0x3a16c>
0x539c4	e9030aaa	mov	x9, x10
0x539c8	6a8d5ff8	ldr	x10, [x11, #-0x8]!
0x539cc	2a8d1ff8	str	x10, [x9, #-0x8]!
0x539d0	7f0108eb	cmp	x11, x8
0x539d4	a1ffff54	b.ne	0x539c8 <_WeChatMain+0x3a15c>
0x539d8	680240f9	ldr	x8, [x19]
0x539dc	ea0309aa	mov	x10, x9
0x539e0	0b0c198b	add	x11, x0, x25, lsl #3
0x539e4	6a6200a9	stp	x10, x24, [x19]
0x539e8	690a40f9	ldr	x9, [x19, #0x10]
0x539ec	6b0a00f9	str	x11, [x19, #0x10]
0x539f0	28f7ffb4	cbz	x8, 0x538d4 <_WeChatMain+0x3a068>
0x539f4	210108cb	sub	x1, x9, x8
0x539f8	e00308aa	mov	x0, x8
0x539fc	84b1c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x53a00	b5ffff17	b	0x538d4 <_WeChatMain+0x3a068>
0x53a04	e00314aa	mov	x0, x20
0x53a08	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x53a0c	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x53a10	f65742a9	ldp	x22, x21, [sp, #0x20]
0x53a14	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x53a18	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x53a1c	b9b6c315	b	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x53a20	e00314aa	mov	x0, x20
0x53a24	985a0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x53a28	51ffff17	b	0x5376c <_WeChatMain+0x39f00>
0x53a2c	e00313aa	mov	x0, x19
0x53a30	fe030094	bl	0x54a28 <_WeChatMain+0x3b1bc>
0x53a34	4640ff97	bl	0x23b4c <_WeChatMain+0xa2e0>
0x53a38	ff0301d1	sub	sp, sp, #0x40
0x53a3c	f65701a9	stp	x22, x21, [sp, #0x10]
0x53a40	f44f02a9	stp	x20, x19, [sp, #0x20]
0x53a44	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x53a48	fdc30091	add	x29, sp, #0x30
0x53a4c	e00700a9	stp	x0, x1, [sp]
0x53a50	b3e9ff97	bl	0x4e11c <_WeChatMain+0x348b0>
0x53a54	400000b4	cbz	x0, 0x53a5c <_WeChatMain+0x3a1f0>
0x53a58	b5e9ff97	bl	0x4e12c <_WeChatMain+0x348c0>
0x53a5c	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53a60	b5222f91	add	x21, x21, #0xbc8
0x53a64	b3c2bff8	ldapr	x19, [x21]
0x53a68	7f0600f1	cmp	x19, #0x1
0x53a6c	08020054	b.hi	0x53aac <_WeChatMain+0x3a240>
0x53a70	542605b0	adrp	x20, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53a74	94222f91	add	x20, x20, #0xbc8
0x53a78	e00314aa	mov	x0, x20
0x53a7c	829eff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53a80	40010034	cbz	w0, 0x53aa8 <_WeChatMain+0x3a23c>
0x53a84	93220091	add	x19, x20, #0x8
0x53a88	e00313aa	mov	x0, x19
0x53a8c	545a0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53a90	e00314aa	mov	x0, x20
0x53a94	e10313aa	mov	x1, x19
0x53a98	020080d2	mov	x2, #0x0                ; =0
0x53a9c	e30314aa	mov	x3, x20
0x53aa0	9d9eff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53aa4	02000014	b	0x53aac <_WeChatMain+0x3a240>
0x53aa8	93c2bff8	ldapr	x19, [x20]
0x53aac	e00313aa	mov	x0, x19
0x53ab0	91b6c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x53ab4	e0040035	cbnz	w0, 0x53b50 <_WeChatMain+0x3a2e4>
0x53ab8	a8c2bff8	ldapr	x8, [x21]
0x53abc	1f0500f1	cmp	x8, #0x1
0x53ac0	e8010054	b.hi	0x53afc <_WeChatMain+0x3a290>
0x53ac4	542605b0	adrp	x20, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53ac8	94222f91	add	x20, x20, #0xbc8
0x53acc	e00314aa	mov	x0, x20
0x53ad0	6d9eff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53ad4	20010034	cbz	w0, 0x53af8 <_WeChatMain+0x3a28c>
0x53ad8	80220091	add	x0, x20, #0x8
0x53adc	405a0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53ae0	81220091	add	x1, x20, #0x8
0x53ae4	e00314aa	mov	x0, x20
0x53ae8	020080d2	mov	x2, #0x0                ; =0
0x53aec	e30314aa	mov	x3, x20
0x53af0	899eff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53af4	02000014	b	0x53afc <_WeChatMain+0x3a290>
0x53af8	9fc2bff8	ldapr	xzr, [x20]
0x53afc	542605b0	adrp	x20, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53b00	800a46f9	ldr	x0, [x20, #0xc10]
0x53b04	a00000b5	cbnz	x0, 0x53b18 <_WeChatMain+0x3a2ac>
0x53b08	00158052	mov	w0, #0xa8               ; =168
0x53b0c	49b1c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x53b10	e2010094	bl	0x54298 <_WeChatMain+0x3aa2c>
0x53b14	800a46f9	ldr	x0, [x20, #0xc10]
0x53b18	e1030091	mov	x1, sp
0x53b1c	d5090094	bl	0x56270 <_WeChatMain+0x3ca04>
0x53b20	600000b4	cbz	x0, 0x53b2c <_WeChatMain+0x3a2c0>
0x53b24	141040f9	ldr	x20, [x0, #0x20]
0x53b28	02000014	b	0x53b30 <_WeChatMain+0x3a2c4>
0x53b2c	140080d2	mov	x20, #0x0               ; =0
0x53b30	e00313aa	mov	x0, x19
0x53b34	73b6c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x53b38	e00314aa	mov	x0, x20
0x53b3c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x53b40	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x53b44	f65741a9	ldp	x22, x21, [sp, #0x10]
0x53b48	ff030191	add	sp, sp, #0x40
0x53b4c	c0035fd6	ret
0x53b50	e00313aa	mov	x0, x19
0x53b54	4c5a0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x53b58	d8ffff17	b	0x53ab8 <_WeChatMain+0x3a24c>
0x53b5c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x53b60	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x53b64	fd430091	add	x29, sp, #0x10
0x53b68	482605b0	adrp	x8, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53b6c	08212f91	add	x8, x8, #0xbc8
0x53b70	08c1bff8	ldapr	x8, [x8]
0x53b74	1f0500f1	cmp	x8, #0x1
0x53b78	e8010054	b.hi	0x53bb4 <_WeChatMain+0x3a348>
0x53b7c	532605b0	adrp	x19, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53b80	73222f91	add	x19, x19, #0xbc8
0x53b84	e00313aa	mov	x0, x19
0x53b88	3f9eff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53b8c	20010034	cbz	w0, 0x53bb0 <_WeChatMain+0x3a344>
0x53b90	60220091	add	x0, x19, #0x8
0x53b94	125a0094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53b98	61220091	add	x1, x19, #0x8
0x53b9c	e00313aa	mov	x0, x19
0x53ba0	020080d2	mov	x2, #0x0                ; =0
0x53ba4	e30313aa	mov	x3, x19
0x53ba8	5b9eff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53bac	02000014	b	0x53bb4 <_WeChatMain+0x3a348>
0x53bb0	7fc2bff8	ldapr	xzr, [x19]
0x53bb4	532605b0	adrp	x19, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53bb8	68627039	ldrb	w8, [x19, #0xc18]
0x53bbc	88050037	tbnz	w8, #0x0, 0x53c6c <_WeChatMain+0x3a400>
0x53bc0	e80f05f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53bc4	09696739	ldrb	w9, [x8, #0x9da]
0x53bc8	69030037	tbnz	w9, #0x0, 0x53c34 <_WeChatMain+0x3a3c8>
0x53bcc	090080d2	mov	x9, #0x0                ; =0
0x53bd0	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x53bd4	aa9999f2	movk	x10, #0xcccd
0x53bd8	6b028092	mov	x11, #-0x14             ; =-20
0x53bdc	ac2104f0	adrp	x12, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53be0	8c412691	add	x12, x12, #0x990
0x53be4	ed0f05f0	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53be8	ad992591	add	x13, x13, #0x966
0x53bec	2e7dca9b	umulh	x14, x9, x10
0x53bf0	cefd44d3	lsr	x14, x14, #4
0x53bf4	8f01098b	add	x15, x12, x9
0x53bf8	ce3d0b9b	madd	x14, x14, x11, x15
0x53bfc	ef550491	add	x15, x15, #0x115
0x53c00	ce050491	add	x14, x14, #0x101
0x53c04	e00140bd	ldr	s0, [x15]
0x53c08	00a4082f	ushll.8h	v0, v0, #0x0
0x53c0c	c10140bd	ldr	s1, [x14]
0x53c10	21a4082f	ushll.8h	v1, v1, #0x0
0x53c14	201c202e	eor.8b	v0, v1, v0
0x53c18	0018000e	uzp1.8b	v0, v0, v0
0x53c1c	a06929bc	str	s0, [x13, x9]
0x53c20	29110091	add	x9, x9, #0x4
0x53c24	3fd101f1	cmp	x9, #0x74
0x53c28	21feff54	b.ne	0x53bec <_WeChatMain+0x3a380>
0x53c2c	29008052	mov	w9, #0x1                ; =1
0x53c30	09692739	strb	w9, [x8, #0x9da]
0x53c34	e00f05f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53c38	00982591	add	x0, x0, #0x966
0x53c3c	810e8052	mov	w1, #0x74               ; =116
0x53c40	eba0ff97	bl	0x3bfec <_WeChatMain+0x22780>
0x53c44	1f040071	cmp	w0, #0x1
0x53c48	2b010054	b.lt	0x53c6c <_WeChatMain+0x3a400>
0x53c4c	28008052	mov	w8, #0x1                ; =1
0x53c50	68623039	strb	w8, [x19, #0xc18]
0x53c54	000000d0	adrp	x0, 0x55000 <_WeChatMain+0x3b794>
0x53c58	00b03691	add	x0, x0, #0xdac
0x53c5c	010080d2	mov	x1, #0x0                ; =0
0x53c60	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x53c64	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x53c68	e12dff17	b	0x1f3ec <_WeChatMain+0x5b80>
0x53c6c	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x53c70	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x53c74	c0035fd6	ret
0x53c78	ff0302d1	sub	sp, sp, #0x80
0x53c7c	f85f04a9	stp	x24, x23, [sp, #0x40]
0x53c80	f65705a9	stp	x22, x21, [sp, #0x50]
0x53c84	f44f06a9	stp	x20, x19, [sp, #0x60]
0x53c88	fd7b07a9	stp	x29, x30, [sp, #0x70]
0x53c8c	fdc30191	add	x29, sp, #0x70
0x53c90	e10303a9	stp	x1, x0, [sp, #0x30]
0x53c94	e22f00b9	str	w2, [sp, #0x2c]
0x53c98	552605b0	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53c9c	b5222f91	add	x21, x21, #0xbc8
0x53ca0	b3c2bff8	ldapr	x19, [x21]
0x53ca4	7f0600f1	cmp	x19, #0x1
0x53ca8	08020054	b.hi	0x53ce8 <_WeChatMain+0x3a47c>
0x53cac	542605b0	adrp	x20, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53cb0	94222f91	add	x20, x20, #0xbc8
0x53cb4	e00314aa	mov	x0, x20
0x53cb8	f39dff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53cbc	40010034	cbz	w0, 0x53ce4 <_WeChatMain+0x3a478>
0x53cc0	93220091	add	x19, x20, #0x8
0x53cc4	e00313aa	mov	x0, x19
0x53cc8	c5590094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53ccc	e00314aa	mov	x0, x20
0x53cd0	e10313aa	mov	x1, x19
0x53cd4	020080d2	mov	x2, #0x0                ; =0
0x53cd8	e30314aa	mov	x3, x20
0x53cdc	0e9eff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53ce0	02000014	b	0x53ce8 <_WeChatMain+0x3a47c>
0x53ce4	93c2bff8	ldapr	x19, [x20]
0x53ce8	e00313aa	mov	x0, x19
0x53cec	02b6c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x53cf0	60120035	cbnz	w0, 0x53f3c <_WeChatMain+0x3a6d0>
0x53cf4	a8c2bff8	ldapr	x8, [x21]
0x53cf8	1f0500f1	cmp	x8, #0x1
0x53cfc	e8010054	b.hi	0x53d38 <_WeChatMain+0x3a4cc>
0x53d00	542605b0	adrp	x20, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53d04	94222f91	add	x20, x20, #0xbc8
0x53d08	e00314aa	mov	x0, x20
0x53d0c	de9dff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x53d10	20010034	cbz	w0, 0x53d34 <_WeChatMain+0x3a4c8>
0x53d14	80220091	add	x0, x20, #0x8
0x53d18	b1590094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x53d1c	81220091	add	x1, x20, #0x8
0x53d20	e00314aa	mov	x0, x20
0x53d24	020080d2	mov	x2, #0x0                ; =0
0x53d28	e30314aa	mov	x3, x20
0x53d2c	fa9dff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x53d30	02000014	b	0x53d38 <_WeChatMain+0x3a4cc>
0x53d34	9fc2bff8	ldapr	xzr, [x20]
0x53d38	542605b0	adrp	x20, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x53d3c	980a46f9	ldr	x24, [x20, #0xc10]
0x53d40	b80000b5	cbnz	x24, 0x53d54 <_WeChatMain+0x3a4e8>
0x53d44	00158052	mov	w0, #0xa8               ; =168
0x53d48	bab0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x53d4c	53010094	bl	0x54298 <_WeChatMain+0x3aa2c>
0x53d50	980a46f9	ldr	x24, [x20, #0xc10]
0x53d54	f51f40f9	ldr	x21, [sp, #0x38]
0x53d58	e00315aa	mov	x0, x21
0x53d5c	27b7c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x53d60	e8ef7db2	mov	x8, #0x7ffffffffffffff8 ; =9223372036854775800
0x53d64	1f0008eb	cmp	x0, x8
0x53d68	020f0054	b.hs	0x53f48 <_WeChatMain+0x3a6dc>
0x53d6c	f40300aa	mov	x20, x0
0x53d70	1f5c00f1	cmp	x0, #0x17
0x53d74	a2000054	b.hs	0x53d88 <_WeChatMain+0x3a51c>
0x53d78	f47f0039	strb	w20, [sp, #0x1f]
0x53d7c	f6230091	add	x22, sp, #0x8
0x53d80	940100b5	cbnz	x20, 0x53db0 <_WeChatMain+0x3a544>
0x53d84	0f000014	b	0x53dc0 <_WeChatMain+0x3a554>
0x53d88	880a40b2	orr	x8, x20, #0x7
0x53d8c	1f5d00f1	cmp	x8, #0x17
0x53d90	29038052	mov	w9, #0x19               ; =25
0x53d94	3705889a	csinc	x23, x9, x8, eq
0x53d98	e00317aa	mov	x0, x23
0x53d9c	a5b0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x53da0	f60300aa	mov	x22, x0
0x53da4	e80241b2	orr	x8, x23, #0x8000000000000000
0x53da8	f42301a9	stp	x20, x8, [sp, #0x10]
0x53dac	e00700f9	str	x0, [sp, #0x8]
0x53db0	e00316aa	mov	x0, x22
0x53db4	e10315aa	mov	x1, x21
0x53db8	e20314aa	mov	x2, x20
0x53dbc	36b4c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x53dc0	df6a3438	strb	wzr, [x22, x20]
0x53dc4	00a30091	add	x0, x24, #0x28
0x53dc8	e1230091	add	x1, sp, #0x8
0x53dcc	74090094	bl	0x5639c <_WeChatMain+0x3cb30>
0x53dd0	f40300aa	mov	x20, x0
0x53dd4	e87fc039	ldrsb	w8, [sp, #0x1f]
0x53dd8	a800f836	tbz	w8, #0x1f, 0x53dec <_WeChatMain+0x3a580>
0x53ddc	e00740f9	ldr	x0, [sp, #0x8]
0x53de0	e80f40f9	ldr	x8, [sp, #0x18]
0x53de4	01f94092	and	x1, x8, #0x7fffffffffffffff
0x53de8	89b0c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x53dec	940900b4	cbz	x20, 0x53f1c <_WeChatMain+0x3a6b0>
0x53df0	941640f9	ldr	x20, [x20, #0x28]
0x53df4	e80f05f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53df8	09956539	ldrb	w9, [x8, #0x965]
0x53dfc	69030037	tbnz	w9, #0x0, 0x53e68 <_WeChatMain+0x3a5fc>
0x53e00	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e04	20b144fd	ldr	d0, [x9, #0x960]
0x53e08	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e0c	21b544fd	ldr	d1, [x9, #0x968]
0x53e10	20040c6e	mov.s	v0[1], v1[0]
0x53e14	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e18	21b944fd	ldr	d1, [x9, #0x970]
0x53e1c	2004146e	mov.s	v0[2], v1[0]
0x53e20	a92104f0	adrp	x9, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e24	216540fd	ldr	d1, [x9, #0xc8]
0x53e28	20041c6e	mov.s	v0[3], v1[0]
0x53e2c	e90f05f0	adrp	x9, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53e30	29212591	add	x9, x9, #0x948
0x53e34	2001803d	str	q0, [x9]
0x53e38	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e3c	40bd44fd	ldr	d0, [x10, #0x978]
0x53e40	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e44	41c144fd	ldr	d1, [x10, #0x980]
0x53e48	20040c6e	mov.s	v0[1], v1[0]
0x53e4c	200900fd	str	d0, [x9, #0x10]
0x53e50	aa2104f0	adrp	x10, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e54	40c544fd	ldr	d0, [x10, #0x988]
0x53e58	201900bd	str	s0, [x9, #0x18]
0x53e5c	3f710039	strb	wzr, [x9, #0x1c]
0x53e60	29008052	mov	w9, #0x1                ; =1
0x53e64	09952539	strb	w9, [x8, #0x965]
0x53e68	e80f05f0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53e6c	09696739	ldrb	w9, [x8, #0x9da]
0x53e70	69030037	tbnz	w9, #0x0, 0x53edc <_WeChatMain+0x3a670>
0x53e74	090080d2	mov	x9, #0x0                ; =0
0x53e78	eae702b2	mov	x10, #-0x3333333333333334 ; =-3689348814741910324
0x53e7c	aa9999f2	movk	x10, #0xcccd
0x53e80	6b028092	mov	x11, #-0x14             ; =-20
0x53e84	ac2104f0	adrp	x12, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x53e88	8c412691	add	x12, x12, #0x990
0x53e8c	ed0f05f0	adrp	x13, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53e90	ad992591	add	x13, x13, #0x966
0x53e94	2e7dca9b	umulh	x14, x9, x10
0x53e98	cefd44d3	lsr	x14, x14, #4
0x53e9c	8f01098b	add	x15, x12, x9
0x53ea0	ce3d0b9b	madd	x14, x14, x11, x15
0x53ea4	ef550491	add	x15, x15, #0x115
0x53ea8	ce050491	add	x14, x14, #0x101
0x53eac	e00140bd	ldr	s0, [x15]
0x53eb0	00a4082f	ushll.8h	v0, v0, #0x0
0x53eb4	c10140bd	ldr	s1, [x14]
0x53eb8	21a4082f	ushll.8h	v1, v1, #0x0
0x53ebc	201c202e	eor.8b	v0, v1, v0
0x53ec0	0018000e	uzp1.8b	v0, v0, v0
0x53ec4	a06929bc	str	s0, [x13, x9]
0x53ec8	29110091	add	x9, x9, #0x4
0x53ecc	3fd101f1	cmp	x9, #0x74
0x53ed0	21feff54	b.ne	0x53e94 <_WeChatMain+0x3a628>
0x53ed4	29008052	mov	w9, #0x1                ; =1
0x53ed8	09692739	strb	w9, [x8, #0x9da]
0x53edc	e00f05f0	adrp	x0, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53ee0	00202591	add	x0, x0, #0x948
0x53ee4	e10f05f0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x53ee8	21982591	add	x1, x1, #0x966
0x53eec	e8230091	add	x8, sp, #0x8
0x53ef0	a2258052	mov	w2, #0x12d              ; =301
0x53ef4	1e9fff97	bl	0x3bb6c <_WeChatMain+0x22300>
0x53ef8	e2fffff0	adrp	x2, 0x52000 <_WeChatMain+0x38794>
0x53efc	42303c91	add	x2, x2, #0xf0c
0x53f00	e1230091	add	x1, sp, #0x8
0x53f04	e4e30091	add	x4, sp, #0x38
0x53f08	e5c30091	add	x5, sp, #0x30
0x53f0c	e6b30091	add	x6, sp, #0x2c
0x53f10	e00314aa	mov	x0, x20
0x53f14	030080d2	mov	x3, #0x0                ; =0
0x53f18	0e000094	bl	0x53f50 <_WeChatMain+0x3a6e4>
0x53f1c	e00313aa	mov	x0, x19
0x53f20	78b5c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x53f24	fd7b47a9	ldp	x29, x30, [sp, #0x70]
0x53f28	f44f46a9	ldp	x20, x19, [sp, #0x60]
0x53f2c	f65745a9	ldp	x22, x21, [sp, #0x50]
0x53f30	f85f44a9	ldp	x24, x23, [sp, #0x40]
0x53f34	ff030291	add	sp, sp, #0x80
0x53f38	c0035fd6	ret
0x53f3c	e00313aa	mov	x0, x19
0x53f40	51590094	bl	0x6a484 <_WeChatMain+0x50c18>
0x53f44	6cffff17	b	0x53cf4 <_WeChatMain+0x3a488>
0x53f48	e0230091	add	x0, sp, #0x8
0x53f4c	4c1bff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x53f50	ffc302d1	sub	sp, sp, #0xb0
0x53f54	fc6f05a9	stp	x28, x27, [sp, #0x50]
0x53f58	fa6706a9	stp	x26, x25, [sp, #0x60]
0x53f5c	f85f07a9	stp	x24, x23, [sp, #0x70]
0x53f60	f65708a9	stp	x22, x21, [sp, #0x80]
0x53f64	f44f09a9	stp	x20, x19, [sp, #0x90]
0x53f68	fd7b0aa9	stp	x29, x30, [sp, #0xa0]
0x53f6c	fd830291	add	x29, sp, #0xa0
0x53f70	f50306aa	mov	x21, x6
0x53f74	f60305aa	mov	x22, x5
0x53f78	f80304aa	mov	x24, x4
0x53f7c	f90303aa	mov	x25, x3
0x53f80	fa0302aa	mov	x26, x2
0x53f84	f40301aa	mov	x20, x1
0x53f88	f30300aa	mov	x19, x0
0x53f8c	000a8052	mov	w0, #0x50               ; =80
0x53f90	28b0c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x53f94	f70300aa	mov	x23, x0
0x53f98	010000f0	adrp	x1, 0x56000 <_WeChatMain+0x3c794>
0x53f9c	21e02091	add	x1, x1, #0x838
0x53fa0	020000f0	adrp	x2, 0x56000 <_WeChatMain+0x3c794>
0x53fa4	42d02191	add	x2, x2, #0x874
0x53fa8	267fff97	bl	0x33c40 <_WeChatMain+0x1a3d4>
0x53fac	080000f0	adrp	x8, 0x56000 <_WeChatMain+0x3c794>
0x53fb0	08512091	add	x8, x8, #0x814
0x53fb4	086802a9	stp	x8, x26, [x0, #0x20]
0x53fb8	191800f9	str	x25, [x0, #0x30]
0x53fbc	180340f9	ldr	x24, [x24]
0x53fc0	08775e92	and	x8, x24, #0xfffffffc00000000
0x53fc4	3afd04f0	adrp	x26, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x53fc8	5a033b91	add	x26, x26, #0xec0
0x53fcc	490740f9	ldr	x9, [x26, #0x8]
0x53fd0	1f0109eb	cmp	x8, x9
0x53fd4	61000054	b.ne	0x53fe0 <_WeChatMain+0x3a774>
0x53fd8	e00318aa	mov	x0, x24
0x53fdc	1caeff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x53fe0	c80240f9	ldr	x8, [x22]
0x53fe4	f8a203a9	stp	x24, x8, [x23, #0x38]
0x53fe8	a80240b9	ldr	w8, [x21]
0x53fec	e84a00b9	str	w8, [x23, #0x48]
0x53ff0	f72700f9	str	x23, [sp, #0x48]
0x53ff4	60420091	add	x0, x19, #0x10
0x53ff8	3fb5c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x53ffc	c0080035	cbnz	w0, 0x54114 <_WeChatMain+0x3a8a8>
0x54000	7b3640f9	ldr	x27, [x19, #0x68]
0x54004	1b0900b4	cbz	x27, 0x54124 <_WeChatMain+0x3a8b8>
0x54008	7c765e92	and	x28, x19, #0xfffffffc00000000
0x5400c	f5230091	add	x21, sp, #0x8
0x54010	160000d0	adrp	x22, 0x56000 <_WeChatMain+0x3c794>
0x54014	d6a21491	add	x22, x22, #0x528
0x54018	03000014	b	0x54024 <_WeChatMain+0x3a7b8>
0x5401c	7b0340f9	ldr	x27, [x27]
0x54020	3b0800b4	cbz	x27, 0x54124 <_WeChatMain+0x3a8b8>
0x54024	785f41a9	ldp	x24, x23, [x27, #0x10]
0x54028	480740f9	ldr	x8, [x26, #0x8]
0x5402c	09775e92	and	x9, x24, #0xfffffffc00000000
0x54030	3f0108eb	cmp	x9, x8
0x54034	81000054	b.ne	0x54044 <_WeChatMain+0x3a7d8>
0x54038	e00318aa	mov	x0, x24
0x5403c	04aeff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x54040	480740f9	ldr	x8, [x26, #0x8]
0x54044	791340f9	ldr	x25, [x27, #0x20]
0x54048	9f0308eb	cmp	x28, x8
0x5404c	61000054	b.ne	0x54058 <_WeChatMain+0x3a7ec>
0x54050	e00313aa	mov	x0, x19
0x54054	feadff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x54058	f30700f9	str	x19, [sp, #0x8]
0x5405c	a0220091	add	x0, x21, #0x8
0x54060	e10314aa	mov	x1, x20
0x54064	589dff97	bl	0x3b5c4 <_WeChatMain+0x21d58>
0x54068	a0a20091	add	x0, x21, #0x28
0x5406c	e1230191	add	x1, sp, #0x48
0x54070	407fff97	bl	0x33d70 <_WeChatMain+0x1a504>
0x54074	f91f00f9	str	x25, [sp, #0x38]
0x54078	000f8052	mov	w0, #0x78               ; =120
0x5407c	edafc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x54080	f90300aa	mov	x25, x0
0x54084	010000d0	adrp	x1, 0x56000 <_WeChatMain+0x3c794>
0x54088	21501d91	add	x1, x1, #0x754
0x5408c	020000d0	adrp	x2, 0x56000 <_WeChatMain+0x3c794>
0x54090	42e01d91	add	x2, x2, #0x778
0x54094	eb7eff97	bl	0x33c40 <_WeChatMain+0x1a3d4>
0x54098	167c02a9	stp	x22, xzr, [x0, #0x20]
0x5409c	131800f9	str	x19, [x0, #0x30]
0x540a0	930000b4	cbz	x19, 0x540b0 <_WeChatMain+0x3a844>
0x540a4	68220091	add	x8, x19, #0x8
0x540a8	29008052	mov	w9, #0x1                ; =1
0x540ac	080129b8	ldadd	w9, w8, [x8]
0x540b0	e80740f9	ldr	x8, [sp, #0x8]
0x540b4	38a303a9	stp	x24, x8, [x25, #0x38]
0x540b8	ff0700f9	str	xzr, [sp, #0x8]
0x540bc	20230191	add	x0, x25, #0x48
0x540c0	a1220091	add	x1, x21, #0x8
0x540c4	409dff97	bl	0x3b5c4 <_WeChatMain+0x21d58>
0x540c8	e82743a9	ldp	x8, x9, [sp, #0x30]
0x540cc	ff1b00f9	str	xzr, [sp, #0x30]
0x540d0	28a706a9	stp	x8, x9, [x25, #0x68]
0x540d4	f92300f9	str	x25, [sp, #0x40]
0x540d8	e2030191	add	x2, sp, #0x40
0x540dc	e00317aa	mov	x0, x23
0x540e0	e10314aa	mov	x1, x20
0x540e4	61c70094	bl	0x85e68 <_WeChatMain+0x6c5fc>
0x540e8	e0030191	add	x0, sp, #0x40
0x540ec	107fff97	bl	0x33d2c <_WeChatMain+0x1a4c0>
0x540f0	a0a20091	add	x0, x21, #0x28
0x540f4	0e7fff97	bl	0x33d2c <_WeChatMain+0x1a4c0>
0x540f8	e00740f9	ldr	x0, [sp, #0x8]
0x540fc	08745e92	and	x8, x0, #0xfffffffc00000000
0x54100	490740f9	ldr	x9, [x26, #0x8]
0x54104	1f0109eb	cmp	x8, x9
0x54108	a1f8ff54	b.ne	0x5401c <_WeChatMain+0x3a7b0>
0x5410c	6daeff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x54110	c3ffff17	b	0x5401c <_WeChatMain+0x3a7b0>
0x54114	60420091	add	x0, x19, #0x10
0x54118	db580094	bl	0x6a484 <_WeChatMain+0x50c18>
0x5411c	7b3640f9	ldr	x27, [x19, #0x68]
0x54120	5bf7ffb5	cbnz	x27, 0x54008 <_WeChatMain+0x3a79c>
0x54124	60420091	add	x0, x19, #0x10
0x54128	f6b4c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x5412c	e0230191	add	x0, sp, #0x48
0x54130	ff7eff97	bl	0x33d2c <_WeChatMain+0x1a4c0>
0x54134	fd7b4aa9	ldp	x29, x30, [sp, #0xa0]
0x54138	f44f49a9	ldp	x20, x19, [sp, #0x90]
0x5413c	f65748a9	ldp	x22, x21, [sp, #0x80]
0x54140	f85f47a9	ldp	x24, x23, [sp, #0x70]
0x54144	fa6746a9	ldp	x26, x25, [sp, #0x60]
0x54148	fc6f45a9	ldp	x28, x27, [sp, #0x50]
0x5414c	ffc30291	add	sp, sp, #0xb0
0x54150	c0035fd6	ret
0x54154	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x54158	f44f01a9	stp	x20, x19, [sp, #0x10]
0x5415c	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x54160	fd830091	add	x29, sp, #0x20
0x54164	f30300aa	mov	x19, x0
0x54168	56260590	adrp	x22, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x5416c	d6222f91	add	x22, x22, #0xbc8
0x54170	d4c2bff8	ldapr	x20, [x22]
0x54174	9f0600f1	cmp	x20, #0x1
0x54178	08020054	b.hi	0x541b8 <_WeChatMain+0x3a94c>
0x5417c	55260590	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x54180	b5222f91	add	x21, x21, #0xbc8
0x54184	e00315aa	mov	x0, x21
0x54188	bf9cff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x5418c	40010034	cbz	w0, 0x541b4 <_WeChatMain+0x3a948>
0x54190	b4220091	add	x20, x21, #0x8
0x54194	e00314aa	mov	x0, x20
0x54198	91580094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x5419c	e00315aa	mov	x0, x21
0x541a0	e10314aa	mov	x1, x20
0x541a4	020080d2	mov	x2, #0x0                ; =0
0x541a8	e30315aa	mov	x3, x21
0x541ac	da9cff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x541b0	02000014	b	0x541b8 <_WeChatMain+0x3a94c>
0x541b4	b4c2bff8	ldapr	x20, [x21]
0x541b8	e00314aa	mov	x0, x20
0x541bc	ceb4c395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x541c0	60050035	cbnz	w0, 0x5426c <_WeChatMain+0x3aa00>
0x541c4	c8c2bff8	ldapr	x8, [x22]
0x541c8	1f0500f1	cmp	x8, #0x1
0x541cc	e8010054	b.hi	0x54208 <_WeChatMain+0x3a99c>
0x541d0	55260590	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x541d4	b5222f91	add	x21, x21, #0xbc8
0x541d8	e00315aa	mov	x0, x21
0x541dc	aa9cff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x541e0	20010034	cbz	w0, 0x54204 <_WeChatMain+0x3a998>
0x541e4	a0220091	add	x0, x21, #0x8
0x541e8	7d580094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x541ec	a1220091	add	x1, x21, #0x8
0x541f0	e00315aa	mov	x0, x21
0x541f4	020080d2	mov	x2, #0x0                ; =0
0x541f8	e30315aa	mov	x3, x21
0x541fc	c69cff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x54200	02000014	b	0x54208 <_WeChatMain+0x3a99c>
0x54204	bfc2bff8	ldapr	xzr, [x21]
0x54208	55260590	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x5420c	a80a46f9	ldr	x8, [x21, #0xc10]
0x54210	280100b4	cbz	x8, 0x54234 <_WeChatMain+0x3a9c8>
0x54214	004d40f9	ldr	x0, [x8, #0x98]
0x54218	a00100b4	cbz	x0, 0x5424c <_WeChatMain+0x3a9e0>
0x5421c	080040f9	ldr	x8, [x0]
0x54220	080940f9	ldr	x8, [x8, #0x10]
0x54224	e10313aa	mov	x1, x19
0x54228	00013fd6	blr	x8
0x5422c	f30300aa	mov	x19, x0
0x54230	08000014	b	0x54250 <_WeChatMain+0x3a9e4>
0x54234	00158052	mov	w0, #0xa8               ; =168
0x54238	7eafc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x5423c	17000094	bl	0x54298 <_WeChatMain+0x3aa2c>
0x54240	a80a46f9	ldr	x8, [x21, #0xc10]
0x54244	004d40f9	ldr	x0, [x8, #0x98]
0x54248	a0feffb5	cbnz	x0, 0x5421c <_WeChatMain+0x3a9b0>
0x5424c	33008052	mov	w19, #0x1               ; =1
0x54250	e00314aa	mov	x0, x20
0x54254	abb4c395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x54258	e00313aa	mov	x0, x19
0x5425c	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x54260	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x54264	f657c3a8	ldp	x22, x21, [sp], #0x30
0x54268	c0035fd6	ret
0x5426c	e00314aa	mov	x0, x20
0x54270	85580094	bl	0x6a484 <_WeChatMain+0x50c18>
0x54274	d4ffff17	b	0x541c4 <_WeChatMain+0x3a958>
0x54278	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x5427c	fd030091	mov	x29, sp
0x54280	000440f9	ldr	x0, [x0, #0x8]
0x54284	210440f9	ldr	x1, [x1, #0x8]
0x54288	c4b5c395	bl	0x7141998 <_wxam_enc_uninit_10+0x7141998>
0x5428c	007c1f53	lsr	w0, w0, #31
0x54290	fd7bc1a8	ldp	x29, x30, [sp], #0x10
0x54294	c0035fd6	ret
0x54298	f657bda9	stp	x22, x21, [sp, #-0x30]!
0x5429c	f44f01a9	stp	x20, x19, [sp, #0x10]
0x542a0	fd7b02a9	stp	x29, x30, [sp, #0x20]
0x542a4	fd830091	add	x29, sp, #0x20
0x542a8	f30300aa	mov	x19, x0
0x542ac	00e4006f	movi.2d	v0, #0000000000000000
0x542b0	000000ad	stp	q0, q0, [x0]
0x542b4	08f0a752	mov	w8, #0x3f800000         ; =1065353216
0x542b8	082000b9	str	w8, [x0, #0x20]
0x542bc	0080823c	stur	q0, [x0, #0x28]
0x542c0	0080833c	stur	q0, [x0, #0x38]
0x542c4	084800b9	str	w8, [x0, #0x48]
0x542c8	1ffc05a9	stp	xzr, xzr, [x0, #0x58]
0x542cc	1f2800f9	str	xzr, [x0, #0x50]
0x542d0	00a00191	add	x0, x0, #0x68
0x542d4	2deeff97	bl	0x4fb88 <_WeChatMain+0x3631c>
0x542d8	7ffe09a9	stp	xzr, xzr, [x19, #0x98]
0x542dc	48260590	adrp	x8, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x542e0	08212f91	add	x8, x8, #0xbc8
0x542e4	08c1bff8	ldapr	x8, [x8]
0x542e8	1f0500f1	cmp	x8, #0x1
0x542ec	e8010054	b.hi	0x54328 <_WeChatMain+0x3aabc>
0x542f0	54260590	adrp	x20, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x542f4	94222f91	add	x20, x20, #0xbc8
0x542f8	e00314aa	mov	x0, x20
0x542fc	629cff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x54300	20010034	cbz	w0, 0x54324 <_WeChatMain+0x3aab8>
0x54304	80220091	add	x0, x20, #0x8
0x54308	35580094	bl	0x6a3dc <_WeChatMain+0x50b70>
0x5430c	81220091	add	x1, x20, #0x8
0x54310	e00314aa	mov	x0, x20
0x54314	020080d2	mov	x2, #0x0                ; =0
0x54318	e30314aa	mov	x3, x20
0x5431c	7e9cff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x54320	02000014	b	0x54328 <_WeChatMain+0x3aabc>
0x54324	9fc2bff8	ldapr	xzr, [x20]
0x54328	55260590	adrp	x21, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x5432c	b40a46f9	ldr	x20, [x21, #0xc10]
0x54330	605240f9	ldr	x0, [x19, #0xa0]
0x54334	08745e92	and	x8, x0, #0xfffffffc00000000
0x54338	36fd04d0	adrp	x22, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x5433c	d6023b91	add	x22, x22, #0xec0
0x54340	c90640f9	ldr	x9, [x22, #0x8]
0x54344	1f0109eb	cmp	x8, x9
0x54348	41000054	b.ne	0x54350 <_WeChatMain+0x3aae4>
0x5434c	ddadff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x54350	88765e92	and	x8, x20, #0xfffffffc00000000
0x54354	c90640f9	ldr	x9, [x22, #0x8]
0x54358	1f0109eb	cmp	x8, x9
0x5435c	61000054	b.ne	0x54368 <_WeChatMain+0x3aafc>
0x54360	e00314aa	mov	x0, x20
0x54364	3aadff97	bl	0x3f84c <_WeChatMain+0x25fe0>
0x54368	745200f9	str	x20, [x19, #0xa0]
0x5436c	b30a06f9	str	x19, [x21, #0xc10]
0x54370	fbfdff97	bl	0x53b5c <_WeChatMain+0x3a2f0>
0x54374	e00313aa	mov	x0, x19
0x54378	fd7b42a9	ldp	x29, x30, [sp, #0x20]
0x5437c	f44f41a9	ldp	x20, x19, [sp, #0x10]
0x54380	f657c3a8	ldp	x22, x21, [sp], #0x30
0x54384	c0035fd6	ret
0x54388	ff8301d1	sub	sp, sp, #0x60
0x5438c	f85f02a9	stp	x24, x23, [sp, #0x20]
0x54390	f65703a9	stp	x22, x21, [sp, #0x30]
0x54394	f44f04a9	stp	x20, x19, [sp, #0x40]
0x54398	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x5439c	fd430191	add	x29, sp, #0x50
0x543a0	f30300aa	mov	x19, x0
0x543a4	350040f9	ldr	x21, [x1]
0x543a8	e00315aa	mov	x0, x21
0x543ac	93b5c395	bl	0x71419f8 <_wxam_enc_uninit_10+0x71419f8>
0x543b0	e8ef7db2	mov	x8, #0x7ffffffffffffff8 ; =9223372036854775800
0x543b4	1f0008eb	cmp	x0, x8
0x543b8	22050054	b.hs	0x5445c <_WeChatMain+0x3abf0>
0x543bc	f40300aa	mov	x20, x0
0x543c0	1f5c00f1	cmp	x0, #0x17
0x543c4	a2000054	b.hs	0x543d8 <_WeChatMain+0x3ab6c>
0x543c8	f47f0039	strb	w20, [sp, #0x1f]
0x543cc	f6230091	add	x22, sp, #0x8
0x543d0	940100b5	cbnz	x20, 0x54400 <_WeChatMain+0x3ab94>
0x543d4	0f000014	b	0x54410 <_WeChatMain+0x3aba4>
0x543d8	880a40b2	orr	x8, x20, #0x7
0x543dc	1f5d00f1	cmp	x8, #0x17
0x543e0	29038052	mov	w9, #0x19               ; =25
0x543e4	3705889a	csinc	x23, x9, x8, eq
0x543e8	e00317aa	mov	x0, x23
0x543ec	11afc395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x543f0	f60300aa	mov	x22, x0
0x543f4	e80241b2	orr	x8, x23, #0x8000000000000000
0x543f8	f42301a9	stp	x20, x8, [sp, #0x10]
0x543fc	e00700f9	str	x0, [sp, #0x8]
0x54400	e00316aa	mov	x0, x22
0x54404	e10315aa	mov	x1, x21
0x54408	e20314aa	mov	x2, x20
0x5440c	a2b2c395	bl	0x7140e94 <_wxam_enc_uninit_10+0x7140e94>
0x54410	df6a3438	strb	wzr, [x22, x20]
0x54414	e1230091	add	x1, sp, #0x8
0x54418	e00313aa	mov	x0, x19
0x5441c	12000094	bl	0x54464 <_WeChatMain+0x3abf8>
0x54420	f30300aa	mov	x19, x0
0x54424	e87fc039	ldrsb	w8, [sp, #0x1f]
0x54428	a800f836	tbz	w8, #0x1f, 0x5443c <_WeChatMain+0x3abd0>
0x5442c	e00740f9	ldr	x0, [sp, #0x8]
0x54430	e80f40f9	ldr	x8, [sp, #0x18]
0x54434	01f94092	and	x1, x8, #0x7fffffffffffffff
0x54438	f5aec395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x5443c	7f0200f1	cmp	x19, #0x0
0x54440	e0079f1a	cset	w0, ne
0x54444	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x54448	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x5444c	f65743a9	ldp	x22, x21, [sp, #0x30]
0x54450	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x54454	ff830191	add	sp, sp, #0x60
0x54458	c0035fd6	ret
0x5445c	e0230091	add	x0, sp, #0x8
0x54460	071aff97	bl	0x1ac7c <_WeChatMain+0x1410>
0x54464	ff8301d1	sub	sp, sp, #0x60
0x54468	fa6701a9	stp	x26, x25, [sp, #0x10]
0x5446c	f85f02a9	stp	x24, x23, [sp, #0x20]
0x54470	f65703a9	stp	x22, x21, [sp, #0x30]
0x54474	f44f04a9	stp	x20, x19, [sp, #0x40]
0x54478	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x5447c	fd430191	add	x29, sp, #0x50
0x54480	f40301aa	mov	x20, x1
0x54484	f30300aa	mov	x19, x0
0x54488	285c4039	ldrb	w8, [x1, #0x17]
0x5448c	091d0013	sxtb	w9, w8
0x54490	2a2c40a9	ldp	x10, x11, [x1]
0x54494	3f010071	cmp	w9, #0x0
0x54498	41b1819a	csel	x1, x10, x1, lt
0x5449c	62b1889a	csel	x2, x11, x8, lt
0x544a0	e03f0091	add	x0, sp, #0xf
0x544a4	53000094	bl	0x545f0 <_WeChatMain+0x3ad84>
0x544a8	750640f9	ldr	x21, [x19, #0x8]
0x544ac	150900b4	cbz	x21, 0x545cc <_WeChatMain+0x3ad60>
0x544b0	a002679e	fmov	d0, x21
0x544b4	0058200e	cnt.8b	v0, v0
0x544b8	0038302e	uaddlv.8b	h0, v0
0x544bc	1600261e	fmov	w22, s0
0x544c0	df0600f1	cmp	x22, #0x1
0x544c4	88000054	b.hi	0x544d4 <_WeChatMain+0x3ac68>
0x544c8	a80600d1	sub	x8, x21, #0x1
0x544cc	1701008a	and	x23, x8, x0
0x544d0	06000014	b	0x544e8 <_WeChatMain+0x3ac7c>
0x544d4	f70300aa	mov	x23, x0
0x544d8	1f0015eb	cmp	x0, x21
0x544dc	63000054	b.lo	0x544e8 <_WeChatMain+0x3ac7c>
0x544e0	0808d59a	udiv	x8, x0, x21
0x544e4	1781159b	msub	x23, x8, x21, x0
0x544e8	680240f9	ldr	x8, [x19]
0x544ec	087977f8	ldr	x8, [x8, x23, lsl #3]
0x544f0	e80600b4	cbz	x8, 0x545cc <_WeChatMain+0x3ad60>
0x544f4	130140f9	ldr	x19, [x8]
0x544f8	d30600b4	cbz	x19, 0x545d0 <_WeChatMain+0x3ad64>
0x544fc	b80600d1	sub	x24, x21, #0x1
0x54500	885e4039	ldrb	w8, [x20, #0x17]
0x54504	091d0013	sxtb	w9, w8
0x54508	3f010071	cmp	w9, #0x0
0x5450c	8a2640a9	ldp	x10, x9, [x20]
0x54510	39b1889a	csel	x25, x9, x8, lt
0x54514	54b1949a	csel	x20, x10, x20, lt
0x54518	06000014	b	0x54530 <_WeChatMain+0x3acc4>
0x5451c	0801188a	and	x8, x8, x24
0x54520	1f0117eb	cmp	x8, x23
0x54524	41050054	b.ne	0x545cc <_WeChatMain+0x3ad60>
0x54528	730240f9	ldr	x19, [x19]
0x5452c	330500b4	cbz	x19, 0x545d0 <_WeChatMain+0x3ad64>
0x54530	680640f9	ldr	x8, [x19, #0x8]
0x54534	1f0008eb	cmp	x0, x8
0x54538	a1020054	b.ne	0x5458c <_WeChatMain+0x3ad20>
0x5453c	689e4039	ldrb	w8, [x19, #0x27]
0x54540	091d0013	sxtb	w9, w8
0x54544	620e40f9	ldr	x2, [x19, #0x18]
0x54548	3f010071	cmp	w9, #0x0
0x5454c	49b0889a	csel	x9, x2, x8, lt
0x54550	3f0119eb	cmp	x9, x25
0x54554	a1feff54	b.ne	0x54528 <_WeChatMain+0x3acbc>
0x54558	69420091	add	x9, x19, #0x10
0x5455c	68023837	tbnz	w8, #0x7, 0x545a8 <_WeChatMain+0x3ad3c>
0x54560	88030034	cbz	w8, 0x545d0 <_WeChatMain+0x3ad64>
0x54564	ea0314aa	mov	x10, x20
0x54568	2b014039	ldrb	w11, [x9]
0x5456c	4c014039	ldrb	w12, [x10]
0x54570	7f010c6b	cmp	w11, w12
0x54574	a1fdff54	b.ne	0x54528 <_WeChatMain+0x3acbc>
0x54578	29050091	add	x9, x9, #0x1
0x5457c	4a050091	add	x10, x10, #0x1
0x54580	080500f1	subs	x8, x8, #0x1
0x54584	21ffff54	b.ne	0x54568 <_WeChatMain+0x3acfc>
0x54588	12000014	b	0x545d0 <_WeChatMain+0x3ad64>
0x5458c	df0600f1	cmp	x22, #0x1
0x54590	69fcff54	b.ls	0x5451c <_WeChatMain+0x3acb0>
0x54594	1f0115eb	cmp	x8, x21
0x54598	43fcff54	b.lo	0x54520 <_WeChatMain+0x3acb4>
0x5459c	0909d59a	udiv	x9, x8, x21
0x545a0	28a1159b	msub	x8, x9, x21, x8
0x545a4	dfffff17	b	0x54520 <_WeChatMain+0x3acb4>
0x545a8	280140f9	ldr	x8, [x9]
0x545ac	fa0300aa	mov	x26, x0
0x545b0	e00308aa	mov	x0, x8
0x545b4	e10314aa	mov	x1, x20
0x545b8	31b2c395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x545bc	e80300aa	mov	x8, x0
0x545c0	e0031aaa	mov	x0, x26
0x545c4	28fbff35	cbnz	w8, 0x54528 <_WeChatMain+0x3acbc>
0x545c8	02000014	b	0x545d0 <_WeChatMain+0x3ad64>
0x545cc	130080d2	mov	x19, #0x0               ; =0
0x545d0	e00313aa	mov	x0, x19
0x545d4	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x545d8	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x545dc	f65743a9	ldp	x22, x21, [sp, #0x30]
0x545e0	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x545e4	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x545e8	ff830191	add	sp, sp, #0x60
0x545ec	c0035fd6	ret
0x545f0	5f8000f1	cmp	x2, #0x20
0x545f4	e8020054	b.hi	0x54650 <_WeChatMain+0x3ade4>
0x545f8	5f4000f1	cmp	x2, #0x10
0x545fc	a8080054	b.hi	0x54710 <_WeChatMain+0x3aea4>
0x54600	5f2400f1	cmp	x2, #0x9
0x54604	631c0054	b.lo	0x54990 <_WeChatMain+0x3b124>
0x54608	280040f9	ldr	x8, [x1]
0x5460c	2900028b	add	x9, x1, x2
0x54610	29815ff8	ldur	x9, [x9, #-0x8]
0x54614	2a01028b	add	x10, x9, x2
0x54618	4a2dc29a	ror	x10, x10, x2
0x5461c	480108ca	eor	x8, x10, x8
0x54620	2bad85d2	mov	x11, #0x2d69            ; =11625
0x54624	0b67bdf2	movk	x11, #0xeb38, lsl #16
0x54628	0b41ddf2	movk	x11, #0xea08, lsl #32
0x5462c	ebbbf3f2	movk	x11, #0x9ddf, lsl #48
0x54630	087d0b9b	mul	x8, x8, x11
0x54634	4abd48ca	eor	x10, x10, x8, lsr #47
0x54638	480108ca	eor	x8, x10, x8
0x5463c	087d0b9b	mul	x8, x8, x11
0x54640	08bd48ca	eor	x8, x8, x8, lsr #47
0x54644	087d0b9b	mul	x8, x8, x11
0x54648	000109ca	eor	x0, x8, x9
0x5464c	c0035fd6	ret
0x54650	5f0001f1	cmp	x2, #0x40
0x54654	480b0054	b.hi	0x547bc <_WeChatMain+0x3af50>
0x54658	2800028b	add	x8, x1, x2
0x5465c	09297fa9	ldp	x9, x10, [x8, #-0x10]
0x54660	2b01028b	add	x11, x9, x2
0x54664	ec2486d2	mov	x12, #0x3127            ; =12583
0x54668	6cf9b2f2	movk	x12, #0x97cb, lsl #16
0x5466c	8c0bd9f2	movk	x12, #0xc85c, lsl #32
0x54670	ac74f8f2	movk	x12, #0xc3a5, lsl #48
0x54674	2d3840a9	ldp	x13, x14, [x1]
0x54678	6b350c9b	madd	x11, x11, x12, x13
0x5467c	2f3441a9	ldp	x15, x13, [x1, #0x10]
0x54680	70010d8b	add	x16, x11, x13
0x54684	10d2d093	ror	x16, x16, #0x34
0x54688	7195cb93	ror	x17, x11, #0x25
0x5468c	6b010e8b	add	x11, x11, x14
0x54690	6e010f8b	add	x14, x11, x15
0x54694	6b1dcb93	ror	x11, x11, #0x7
0x54698	c07dce93	ror	x0, x14, #0x1f
0x5469c	6b01118b	add	x11, x11, x17
0x546a0	6b01108b	add	x11, x11, x16
0x546a4	10217ea9	ldp	x16, x8, [x8, #-0x20]
0x546a8	0f020f8b	add	x15, x16, x15
0x546ac	08010f8b	add	x8, x8, x15
0x546b0	4a010d8b	add	x10, x10, x13
0x546b4	50010f8b	add	x16, x10, x15
0x546b8	10d2d093	ror	x16, x16, #0x34
0x546bc	ef95cf93	ror	x15, x15, #0x25
0x546c0	111dc893	ror	x17, x8, #0x7
0x546c4	0801098b	add	x8, x8, x9
0x546c8	09010a8b	add	x9, x8, x10
0x546cc	087dc893	ror	x8, x8, #0x1f
0x546d0	aa010f8b	add	x10, x13, x15
0x546d4	4a01118b	add	x10, x10, x17
0x546d8	4a01108b	add	x10, x10, x16
0x546dc	4801088b	add	x8, x10, x8
0x546e0	c801088b	add	x8, x14, x8
0x546e4	ea0988d2	mov	x10, #0x404f            ; =16463
0x546e8	0af2a5f2	movk	x10, #0x2f90, lsl #16
0x546ec	6a47cdf2	movk	x10, #0x6a3b, lsl #32
0x546f0	2a5cf3f2	movk	x10, #0x9ae1, lsl #48
0x546f4	6b01008b	add	x11, x11, x0
0x546f8	29010b8b	add	x9, x9, x11
0x546fc	297d0c9b	mul	x9, x9, x12
0x54700	08250a9b	madd	x8, x8, x10, x9
0x54704	08bd48ca	eor	x8, x8, x8, lsr #47
0x54708	082d0c9b	madd	x8, x8, x12, x11
0x5470c	29000014	b	0x547b0 <_WeChatMain+0x3af44>
0x54710	684e9ed2	mov	x8, #0xf273             ; =62067
0x54714	08d3b7f2	movk	x8, #0xbe98, lsl #16
0x54718	e8cdd6f2	movk	x8, #0xb66f, lsl #32
0x5471c	4892f6f2	movk	x8, #0xb492, lsl #48
0x54720	292840a9	ldp	x9, x10, [x1]
0x54724	287d089b	mul	x8, x9, x8
0x54728	2900028b	add	x9, x1, x2
0x5472c	eb0988d2	mov	x11, #0x404f            ; =16463
0x54730	0bf2a5f2	movk	x11, #0x2f90, lsl #16
0x54734	6b47cdf2	movk	x11, #0x6a3b, lsl #32
0x54738	2b5cf3f2	movk	x11, #0x9ae1, lsl #48
0x5473c	29317fa9	ldp	x9, x12, [x9, #-0x10]
0x54740	8b7d0b9b	mul	x11, x12, x11
0x54744	0c010acb	sub	x12, x8, x10
0x54748	8cadcc93	ror	x12, x12, #0x2b
0x5474c	6d79cb93	ror	x13, x11, #0x1e
0x54750	ee2486d2	mov	x14, #0x3127            ; =12583
0x54754	6ef9b2f2	movk	x14, #0x97cb, lsl #16
0x54758	8e0bd9f2	movk	x14, #0xc85c, lsl #32
0x5475c	ae74f8f2	movk	x14, #0xc3a5, lsl #48
0x54760	ac010c8b	add	x12, x13, x12
0x54764	edaa8cd2	mov	x13, #0x6557            ; =25943
0x54768	cd13aaf2	movk	x13, #0x509e, lsl #16
0x5476c	edf8daf2	movk	x13, #0xd7c7, lsl #32
0x54770	2d29f9f2	movk	x13, #0xc949, lsl #48
0x54774	4a010dca	eor	x10, x10, x13
0x54778	4a51ca93	ror	x10, x10, #0x14
0x5477c	29310e9b	madd	x9, x9, x14, x12
0x54780	4a000a8b	add	x10, x2, x10
0x54784	08010a8b	add	x8, x8, x10
0x54788	08010bcb	sub	x8, x8, x11
0x5478c	290108ca	eor	x9, x9, x8
0x54790	2aad85d2	mov	x10, #0x2d69            ; =11625
0x54794	0a67bdf2	movk	x10, #0xeb38, lsl #16
0x54798	0a41ddf2	movk	x10, #0xea08, lsl #32
0x5479c	eabbf3f2	movk	x10, #0x9ddf, lsl #48
0x547a0	297d0a9b	mul	x9, x9, x10
0x547a4	08bd49ca	eor	x8, x8, x9, lsr #47
0x547a8	080109ca	eor	x8, x8, x9
0x547ac	087d0a9b	mul	x8, x8, x10
0x547b0	08bd48ca	eor	x8, x8, x8, lsr #47
0x547b4	007d0a9b	mul	x0, x8, x10
0x547b8	c0035fd6	ret
0x547bc	694e9ed2	mov	x9, #0xf273             ; =62067
0x547c0	09d3b7f2	movk	x9, #0xbe98, lsl #16
0x547c4	e9cdd6f2	movk	x9, #0xb66f, lsl #32
0x547c8	4992f6f2	movk	x9, #0xb492, lsl #48
0x547cc	28ad85d2	mov	x8, #0x2d69             ; =11625
0x547d0	0867bdf2	movk	x8, #0xeb38, lsl #16
0x547d4	0841ddf2	movk	x8, #0xea08, lsl #32
0x547d8	e8bbf3f2	movk	x8, #0x9ddf, lsl #48
0x547dc	2b00028b	add	x11, x1, x2
0x547e0	6d317ca9	ldp	x13, x12, [x11, #-0x40]
0x547e4	6e3d7fa9	ldp	x14, x15, [x11, #-0x10]
0x547e8	8a010e8b	add	x10, x12, x14
0x547ec	60457da9	ldp	x0, x17, [x11, #-0x30]
0x547f0	640d7ea9	ldp	x4, x3, [x11, #-0x20]
0x547f4	0b00028b	add	x11, x0, x2
0x547f8	6b000bca	eor	x11, x3, x11
0x547fc	6b7d089b	mul	x11, x11, x8
0x54800	70bc4bca	eor	x16, x3, x11, lsr #47
0x54804	0b020bca	eor	x11, x16, x11
0x54808	6b7d089b	mul	x11, x11, x8
0x5480c	6bbd4bca	eor	x11, x11, x11, lsr #47
0x54810	707d089b	mul	x16, x11, x8
0x54814	ab01028b	add	x11, x13, x2
0x54818	2d020b8b	add	x13, x17, x11
0x5481c	ad01108b	add	x13, x13, x16
0x54820	ad55cd93	ror	x13, x13, #0x15
0x54824	8c01008b	add	x12, x12, x0
0x54828	6c010c8b	add	x12, x11, x12
0x5482c	80b1cc93	ror	x0, x12, #0x2c
0x54830	8c01118b	add	x12, x12, x17
0x54834	0b000b8b	add	x11, x0, x11
0x54838	6b010d8b	add	x11, x11, x13
0x5483c	8d00098b	add	x13, x4, x9
0x54840	4d010d8b	add	x13, x10, x13
0x54844	20020f8b	add	x0, x17, x15
0x54848	a001008b	add	x0, x13, x0
0x5484c	0054c093	ror	x0, x0, #0x15
0x54850	6e000e8b	add	x14, x3, x14
0x54854	ae010e8b	add	x14, x13, x14
0x54858	c3b1ce93	ror	x3, x14, #0x2c
0x5485c	cf010f8b	add	x15, x14, x15
0x54860	6d000d8b	add	x13, x3, x13
0x54864	ad01008b	add	x13, x13, x0
0x54868	2e0442f8	ldr	x14, [x1], #0x20
0x5486c	313a099b	madd	x17, x17, x9, x14
0x54870	4e0400d1	sub	x14, x2, #0x1
0x54874	cee57a92	and	x14, x14, #0xffffffffffffffc0
0x54878	ee030ecb	neg	x14, x14
0x5487c	31020c8b	add	x17, x17, x12
0x54880	31020a8b	add	x17, x17, x10
0x54884	23087ea9	ldp	x3, x2, [x1, #-0x20]
0x54888	3102028b	add	x17, x17, x2
0x5488c	3196d193	ror	x17, x17, #0x25
0x54890	241441a9	ldp	x4, x5, [x1, #0x10]
0x54894	4a010b8b	add	x10, x10, x11
0x54898	4a01048b	add	x10, x10, x4
0x5489c	4aa9ca93	ror	x10, x10, #0x2a
0x548a0	317e099b	mul	x17, x17, x9
0x548a4	20020dca	eor	x0, x17, x13
0x548a8	271840a9	ldp	x7, x6, [x1]
0x548ac	cc000c8b	add	x12, x6, x12
0x548b0	4a31099b	madd	x10, x10, x9, x12
0x548b4	0c020f8b	add	x12, x16, x15
0x548b8	8c85cc93	ror	x12, x12, #0x21
0x548bc	917d099b	mul	x17, x12, x9
0x548c0	6b0d099b	madd	x11, x11, x9, x3
0x548c4	30307fa9	ldp	x16, x12, [x1, #-0x10]
0x548c8	6f010f8b	add	x15, x11, x15
0x548cc	ef010c8b	add	x15, x15, x12
0x548d0	ef01008b	add	x15, x15, x0
0x548d4	ef55cf93	ror	x15, x15, #0x15
0x548d8	4200108b	add	x2, x2, x16
0x548dc	6201028b	add	x2, x11, x2
0x548e0	4c000c8b	add	x12, x2, x12
0x548e4	42b0c293	ror	x2, x2, #0x2c
0x548e8	4b000b8b	add	x11, x2, x11
0x548ec	6b010f8b	add	x11, x11, x15
0x548f0	ad01078b	add	x13, x13, x7
0x548f4	2d020d8b	add	x13, x17, x13
0x548f8	0f020d8b	add	x15, x16, x13
0x548fc	ef01058b	add	x15, x15, x5
0x54900	4f010f8b	add	x15, x10, x15
0x54904	f055cf93	ror	x16, x15, #0x15
0x54908	cf00048b	add	x15, x6, x4
0x5490c	af010f8b	add	x15, x13, x15
0x54910	e2b1cf93	ror	x2, x15, #0x2c
0x54914	ef01058b	add	x15, x15, x5
0x54918	4d000d8b	add	x13, x2, x13
0x5491c	ad01108b	add	x13, x13, x16
0x54920	21000191	add	x1, x1, #0x40
0x54924	f00300aa	mov	x16, x0
0x54928	ce0101b1	adds	x14, x14, #0x40
0x5492c	81faff54	b.ne	0x5487c <_WeChatMain+0x3b010>
0x54930	ec010cca	eor	x12, x15, x12
0x54934	8c7d089b	mul	x12, x12, x8
0x54938	eebd4cca	eor	x14, x15, x12, lsr #47
0x5493c	cc010cca	eor	x12, x14, x12
0x54940	8c7d089b	mul	x12, x12, x8
0x54944	8cbd4cca	eor	x12, x12, x12, lsr #47
0x54948	4abd4aca	eor	x10, x10, x10, lsr #47
0x5494c	4901099b	madd	x9, x10, x9, x0
0x54950	8925089b	madd	x9, x12, x8, x9
0x54954	aa010bca	eor	x10, x13, x11
0x54958	4a7d089b	mul	x10, x10, x8
0x5495c	abbd4aca	eor	x11, x13, x10, lsr #47
0x54960	6a010aca	eor	x10, x11, x10
0x54964	4a7d089b	mul	x10, x10, x8
0x54968	4abd4aca	eor	x10, x10, x10, lsr #47
0x5496c	4a45089b	madd	x10, x10, x8, x17
0x54970	490109ca	eor	x9, x10, x9
0x54974	297d089b	mul	x9, x9, x8
0x54978	4abd49ca	eor	x10, x10, x9, lsr #47
0x5497c	490109ca	eor	x9, x10, x9
0x54980	297d089b	mul	x9, x9, x8
0x54984	29bd49ca	eor	x9, x9, x9, lsr #47
0x54988	207d089b	mul	x0, x9, x8
0x5498c	c0035fd6	ret
0x54990	5f1000f1	cmp	x2, #0x4
0x54994	e3010054	b.lo	0x549d0 <_WeChatMain+0x3b164>
0x54998	280040b9	ldr	w8, [x1]
0x5499c	2900028b	add	x9, x1, x2
0x549a0	29c15fb8	ldur	w9, [x9, #-0x4]
0x549a4	08711d53	lsl	w8, w8, #3
0x549a8	0801028b	add	x8, x8, x2
0x549ac	080109ca	eor	x8, x8, x9
0x549b0	2aad85d2	mov	x10, #0x2d69            ; =11625
0x549b4	0a67bdf2	movk	x10, #0xeb38, lsl #16
0x549b8	0a41ddf2	movk	x10, #0xea08, lsl #32
0x549bc	eabbf3f2	movk	x10, #0x9ddf, lsl #48
0x549c0	087d0a9b	mul	x8, x8, x10
0x549c4	29bd48ca	eor	x9, x9, x8, lsr #47
0x549c8	280108ca	eor	x8, x9, x8
0x549cc	78ffff17	b	0x547ac <_WeChatMain+0x3af40>
0x549d0	e00988d2	mov	x0, #0x404f             ; =16463
0x549d4	00f2a5f2	movk	x0, #0x2f90, lsl #16
0x549d8	6047cdf2	movk	x0, #0x6a3b, lsl #32
0x549dc	205cf3f2	movk	x0, #0x9ae1, lsl #48
0x549e0	62fdffb4	cbz	x2, 0x5498c <_WeChatMain+0x3b120>
0x549e4	28004039	ldrb	w8, [x1]
0x549e8	49fc41d3	lsr	x9, x2, #1
0x549ec	29686938	ldrb	w9, [x1, x9]
0x549f0	2a00028b	add	x10, x1, x2
0x549f4	4af15f38	ldurb	w10, [x10, #-0x1]
0x549f8	082109aa	orr	x8, x8, x9, lsl #8
0x549fc	49080aaa	orr	x9, x2, x10, lsl #2
0x54a00	087d009b	mul	x8, x8, x0
0x54a04	eaaa8cd2	mov	x10, #0x6557            ; =25943
0x54a08	ca13aaf2	movk	x10, #0x509e, lsl #16
0x54a0c	eaf8daf2	movk	x10, #0xd7c7, lsl #32
0x54a10	2a29f9f2	movk	x10, #0xc949, lsl #48
0x54a14	297d0a9b	mul	x9, x9, x10
0x54a18	280108ca	eor	x8, x9, x8
0x54a1c	08bd48ca	eor	x8, x8, x8, lsr #47
0x54a20	007d009b	mul	x0, x8, x0
0x54a24	c0035fd6	ret
0x54a28	e80f05d0	adrp	x8, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x54a2c	09716739	ldrb	w9, [x8, #0x9dc]
0x54a30	69000037	tbnz	w9, #0x0, 0x54a3c <_WeChatMain+0x3b1d0>
0x54a34	29008052	mov	w9, #0x1                ; =1
0x54a38	09712739	strb	w9, [x8, #0x9dc]
0x54a3c	fd7bbfa9	stp	x29, x30, [sp, #-0x10]!
0x54a40	fd030091	mov	x29, sp
0x54a44	0baec395	bl	0x7140270 <_wxam_enc_uninit_10+0x7140270>
0x54a48	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x54a4c	fa6701a9	stp	x26, x25, [sp, #0x10]
0x54a50	f85f02a9	stp	x24, x23, [sp, #0x20]
0x54a54	f65703a9	stp	x22, x21, [sp, #0x30]
0x54a58	f44f04a9	stp	x20, x19, [sp, #0x40]
0x54a5c	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x54a60	fd430191	add	x29, sp, #0x50
0x54a64	f60304aa	mov	x22, x4
0x54a68	f40302aa	mov	x20, x2
0x54a6c	f30301aa	mov	x19, x1
0x54a70	f50300aa	mov	x21, x0
0x54a74	3a008052	mov	w26, #0x1               ; =1
0x54a78	f80315aa	mov	x24, x21
0x54a7c	480303cb	sub	x8, x26, x3
0x54a80	f50318aa	mov	x21, x24
0x54a84	fb0308aa	mov	x27, x8
0x54a88	680218cb	sub	x8, x19, x24
0x54a8c	08fd4393	asr	x8, x8, #3
0x54a90	1f0900f1	cmp	x8, #0x2
0x54a94	ac000054	b.gt	0x54aa8 <_WeChatMain+0x3b23c>
0x54a98	63380054	b.lo	0x551a4 <_WeChatMain+0x3b938>
0x54a9c	1f0900f1	cmp	x8, #0x2
0x54aa0	01010054	b.ne	0x54ac0 <_WeChatMain+0x3b254>
0x54aa4	47010014	b	0x54fc0 <_WeChatMain+0x3b754>
0x54aa8	1f0d00f1	cmp	x8, #0x3
0x54aac	e0240054	b.eq	0x54f48 <_WeChatMain+0x3b6dc>
0x54ab0	1f1100f1	cmp	x8, #0x4
0x54ab4	a0290054	b.eq	0x54fe8 <_WeChatMain+0x3b77c>
0x54ab8	1f1500f1	cmp	x8, #0x5
0x54abc	80260054	b.eq	0x54f8c <_WeChatMain+0x3b720>
0x54ac0	1f5d00f1	cmp	x8, #0x17
0x54ac4	ad2a0054	b.le	0x55018 <_WeChatMain+0x3b7ac>
0x54ac8	7f0700f1	cmp	x27, #0x1
0x54acc	002f0054	b.eq	0x550ac <_WeChatMain+0x3b840>
0x54ad0	18fd41d3	lsr	x24, x8, #1
0x54ad4	890240f9	ldr	x9, [x20]
0x54ad8	290140f9	ldr	x9, [x9]
0x54adc	1f0502f1	cmp	x8, #0x81
0x54ae0	23020054	b.lo	0x54b24 <_WeChatMain+0x3b2b8>
0x54ae4	a07a78f8	ldr	x0, [x21, x24, lsl #3]
0x54ae8	a10240f9	ldr	x1, [x21]
0x54aec	20013fd6	blr	x9
0x54af0	f70300aa	mov	x23, x0
0x54af4	880240f9	ldr	x8, [x20]
0x54af8	080140f9	ldr	x8, [x8]
0x54afc	60825ff8	ldur	x0, [x19, #-0x8]
0x54b00	a17a78f8	ldr	x1, [x21, x24, lsl #3]
0x54b04	00013fd6	blr	x8
0x54b08	17030036	tbz	w23, #0x0, 0x54b68 <_WeChatMain+0x3b2fc>
0x54b0c	a10240f9	ldr	x1, [x21]
0x54b10	e0060034	cbz	w0, 0x54bec <_WeChatMain+0x3b380>
0x54b14	68825ff8	ldur	x8, [x19, #-0x8]
0x54b18	a80200f9	str	x8, [x21]
0x54b1c	61821ff8	stur	x1, [x19, #-0x8]
0x54b20	3f000014	b	0x54c1c <_WeChatMain+0x3b3b0>
0x54b24	a00240f9	ldr	x0, [x21]
0x54b28	a17a78f8	ldr	x1, [x21, x24, lsl #3]
0x54b2c	20013fd6	blr	x9
0x54b30	f70300aa	mov	x23, x0
0x54b34	880240f9	ldr	x8, [x20]
0x54b38	080140f9	ldr	x8, [x8]
0x54b3c	60825ff8	ldur	x0, [x19, #-0x8]
0x54b40	a10240f9	ldr	x1, [x21]
0x54b44	00013fd6	blr	x8
0x54b48	17030036	tbz	w23, #0x0, 0x54ba8 <_WeChatMain+0x3b33c>
0x54b4c	a17a78f8	ldr	x1, [x21, x24, lsl #3]
0x54b50	c00a0034	cbz	w0, 0x54ca8 <_WeChatMain+0x3b43c>
0x54b54	68825ff8	ldur	x8, [x19, #-0x8]
0x54b58	a87a38f8	str	x8, [x21, x24, lsl #3]
0x54b5c	61821ff8	stur	x1, [x19, #-0x8]
0x54b60	d6190036	tbz	w22, #0x0, 0x54e98 <_WeChatMain+0x3b62c>
0x54b64	d2000014	b	0x54eac <_WeChatMain+0x3b640>
0x54b68	a0050034	cbz	w0, 0x54c1c <_WeChatMain+0x3b3b0>
0x54b6c	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54b70	69825ff8	ldur	x9, [x19, #-0x8]
0x54b74	a97a38f8	str	x9, [x21, x24, lsl #3]
0x54b78	68821ff8	stur	x8, [x19, #-0x8]
0x54b7c	880240f9	ldr	x8, [x20]
0x54b80	080140f9	ldr	x8, [x8]
0x54b84	a07a78f8	ldr	x0, [x21, x24, lsl #3]
0x54b88	a10240f9	ldr	x1, [x21]
0x54b8c	00013fd6	blr	x8
0x54b90	60040034	cbz	w0, 0x54c1c <_WeChatMain+0x3b3b0>
0x54b94	a80240f9	ldr	x8, [x21]
0x54b98	a97a78f8	ldr	x9, [x21, x24, lsl #3]
0x54b9c	a90200f9	str	x9, [x21]
0x54ba0	a87a38f8	str	x8, [x21, x24, lsl #3]
0x54ba4	1e000014	b	0x54c1c <_WeChatMain+0x3b3b0>
0x54ba8	80090034	cbz	w0, 0x54cd8 <_WeChatMain+0x3b46c>
0x54bac	a80240f9	ldr	x8, [x21]
0x54bb0	69825ff8	ldur	x9, [x19, #-0x8]
0x54bb4	a90200f9	str	x9, [x21]
0x54bb8	68821ff8	stur	x8, [x19, #-0x8]
0x54bbc	880240f9	ldr	x8, [x20]
0x54bc0	080140f9	ldr	x8, [x8]
0x54bc4	a00240f9	ldr	x0, [x21]
0x54bc8	a17a78f8	ldr	x1, [x21, x24, lsl #3]
0x54bcc	00013fd6	blr	x8
0x54bd0	40080034	cbz	w0, 0x54cd8 <_WeChatMain+0x3b46c>
0x54bd4	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54bd8	a90240f9	ldr	x9, [x21]
0x54bdc	a97a38f8	str	x9, [x21, x24, lsl #3]
0x54be0	a80200f9	str	x8, [x21]
0x54be4	b6150036	tbz	w22, #0x0, 0x54e98 <_WeChatMain+0x3b62c>
0x54be8	b1000014	b	0x54eac <_WeChatMain+0x3b640>
0x54bec	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54bf0	a80200f9	str	x8, [x21]
0x54bf4	a17a38f8	str	x1, [x21, x24, lsl #3]
0x54bf8	880240f9	ldr	x8, [x20]
0x54bfc	080140f9	ldr	x8, [x8]
0x54c00	60825ff8	ldur	x0, [x19, #-0x8]
0x54c04	00013fd6	blr	x8
0x54c08	a0000034	cbz	w0, 0x54c1c <_WeChatMain+0x3b3b0>
0x54c0c	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54c10	69825ff8	ldur	x9, [x19, #-0x8]
0x54c14	a97a38f8	str	x9, [x21, x24, lsl #3]
0x54c18	68821ff8	stur	x8, [x19, #-0x8]
0x54c1c	190700d1	sub	x25, x24, #0x1
0x54c20	880240f9	ldr	x8, [x20]
0x54c24	080140f9	ldr	x8, [x8]
0x54c28	a07a79f8	ldr	x0, [x21, x25, lsl #3]
0x54c2c	a10640f9	ldr	x1, [x21, #0x8]
0x54c30	00013fd6	blr	x8
0x54c34	f70300aa	mov	x23, x0
0x54c38	880240f9	ldr	x8, [x20]
0x54c3c	080140f9	ldr	x8, [x8]
0x54c40	60025ff8	ldur	x0, [x19, #-0x10]
0x54c44	a17a79f8	ldr	x1, [x21, x25, lsl #3]
0x54c48	00013fd6	blr	x8
0x54c4c	f7000036	tbz	w23, #0x0, 0x54c68 <_WeChatMain+0x3b3fc>
0x54c50	a10640f9	ldr	x1, [x21, #0x8]
0x54c54	60040034	cbz	w0, 0x54ce0 <_WeChatMain+0x3b474>
0x54c58	68025ff8	ldur	x8, [x19, #-0x10]
0x54c5c	a80600f9	str	x8, [x21, #0x8]
0x54c60	61021ff8	stur	x1, [x19, #-0x10]
0x54c64	2b000014	b	0x54d10 <_WeChatMain+0x3b4a4>
0x54c68	40050034	cbz	w0, 0x54d10 <_WeChatMain+0x3b4a4>
0x54c6c	a87a79f8	ldr	x8, [x21, x25, lsl #3]
0x54c70	69025ff8	ldur	x9, [x19, #-0x10]
0x54c74	a97a39f8	str	x9, [x21, x25, lsl #3]
0x54c78	68021ff8	stur	x8, [x19, #-0x10]
0x54c7c	880240f9	ldr	x8, [x20]
0x54c80	080140f9	ldr	x8, [x8]
0x54c84	a07a79f8	ldr	x0, [x21, x25, lsl #3]
0x54c88	a10640f9	ldr	x1, [x21, #0x8]
0x54c8c	00013fd6	blr	x8
0x54c90	00040034	cbz	w0, 0x54d10 <_WeChatMain+0x3b4a4>
0x54c94	a80640f9	ldr	x8, [x21, #0x8]
0x54c98	a97a79f8	ldr	x9, [x21, x25, lsl #3]
0x54c9c	a90600f9	str	x9, [x21, #0x8]
0x54ca0	a87a39f8	str	x8, [x21, x25, lsl #3]
0x54ca4	1b000014	b	0x54d10 <_WeChatMain+0x3b4a4>
0x54ca8	a80240f9	ldr	x8, [x21]
0x54cac	a87a38f8	str	x8, [x21, x24, lsl #3]
0x54cb0	a10200f9	str	x1, [x21]
0x54cb4	880240f9	ldr	x8, [x20]
0x54cb8	080140f9	ldr	x8, [x8]
0x54cbc	60825ff8	ldur	x0, [x19, #-0x8]
0x54cc0	00013fd6	blr	x8
0x54cc4	a0000034	cbz	w0, 0x54cd8 <_WeChatMain+0x3b46c>
0x54cc8	a80240f9	ldr	x8, [x21]
0x54ccc	69825ff8	ldur	x9, [x19, #-0x8]
0x54cd0	a90200f9	str	x9, [x21]
0x54cd4	68821ff8	stur	x8, [x19, #-0x8]
0x54cd8	160e0036	tbz	w22, #0x0, 0x54e98 <_WeChatMain+0x3b62c>
0x54cdc	74000014	b	0x54eac <_WeChatMain+0x3b640>
0x54ce0	a87a79f8	ldr	x8, [x21, x25, lsl #3]
0x54ce4	a80600f9	str	x8, [x21, #0x8]
0x54ce8	a17a39f8	str	x1, [x21, x25, lsl #3]
0x54cec	880240f9	ldr	x8, [x20]
0x54cf0	080140f9	ldr	x8, [x8]
0x54cf4	60025ff8	ldur	x0, [x19, #-0x10]
0x54cf8	00013fd6	blr	x8
0x54cfc	a0000034	cbz	w0, 0x54d10 <_WeChatMain+0x3b4a4>
0x54d00	a87a79f8	ldr	x8, [x21, x25, lsl #3]
0x54d04	69025ff8	ldur	x9, [x19, #-0x10]
0x54d08	a97a39f8	str	x9, [x21, x25, lsl #3]
0x54d0c	68021ff8	stur	x8, [x19, #-0x10]
0x54d10	1c070091	add	x28, x24, #0x1
0x54d14	880240f9	ldr	x8, [x20]
0x54d18	080140f9	ldr	x8, [x8]
0x54d1c	a07a7cf8	ldr	x0, [x21, x28, lsl #3]
0x54d20	a10a40f9	ldr	x1, [x21, #0x10]
0x54d24	00013fd6	blr	x8
0x54d28	f70300aa	mov	x23, x0
0x54d2c	880240f9	ldr	x8, [x20]
0x54d30	080140f9	ldr	x8, [x8]
0x54d34	60825ef8	ldur	x0, [x19, #-0x18]
0x54d38	a17a7cf8	ldr	x1, [x21, x28, lsl #3]
0x54d3c	00013fd6	blr	x8
0x54d40	f7000036	tbz	w23, #0x0, 0x54d5c <_WeChatMain+0x3b4f0>
0x54d44	a10a40f9	ldr	x1, [x21, #0x10]
0x54d48	a0020034	cbz	w0, 0x54d9c <_WeChatMain+0x3b530>
0x54d4c	68825ef8	ldur	x8, [x19, #-0x18]
0x54d50	a80a00f9	str	x8, [x21, #0x10]
0x54d54	61821ef8	stur	x1, [x19, #-0x18]
0x54d58	1d000014	b	0x54dcc <_WeChatMain+0x3b560>
0x54d5c	80030034	cbz	w0, 0x54dcc <_WeChatMain+0x3b560>
0x54d60	a87a7cf8	ldr	x8, [x21, x28, lsl #3]
0x54d64	69825ef8	ldur	x9, [x19, #-0x18]
0x54d68	a97a3cf8	str	x9, [x21, x28, lsl #3]
0x54d6c	68821ef8	stur	x8, [x19, #-0x18]
0x54d70	880240f9	ldr	x8, [x20]
0x54d74	080140f9	ldr	x8, [x8]
0x54d78	a07a7cf8	ldr	x0, [x21, x28, lsl #3]
0x54d7c	a10a40f9	ldr	x1, [x21, #0x10]
0x54d80	00013fd6	blr	x8
0x54d84	40020034	cbz	w0, 0x54dcc <_WeChatMain+0x3b560>
0x54d88	a80a40f9	ldr	x8, [x21, #0x10]
0x54d8c	a97a7cf8	ldr	x9, [x21, x28, lsl #3]
0x54d90	a90a00f9	str	x9, [x21, #0x10]
0x54d94	a87a3cf8	str	x8, [x21, x28, lsl #3]
0x54d98	0d000014	b	0x54dcc <_WeChatMain+0x3b560>
0x54d9c	a87a7cf8	ldr	x8, [x21, x28, lsl #3]
0x54da0	a80a00f9	str	x8, [x21, #0x10]
0x54da4	a17a3cf8	str	x1, [x21, x28, lsl #3]
0x54da8	880240f9	ldr	x8, [x20]
0x54dac	080140f9	ldr	x8, [x8]
0x54db0	60825ef8	ldur	x0, [x19, #-0x18]
0x54db4	00013fd6	blr	x8
0x54db8	a0000034	cbz	w0, 0x54dcc <_WeChatMain+0x3b560>
0x54dbc	a87a7cf8	ldr	x8, [x21, x28, lsl #3]
0x54dc0	69825ef8	ldur	x9, [x19, #-0x18]
0x54dc4	a97a3cf8	str	x9, [x21, x28, lsl #3]
0x54dc8	68821ef8	stur	x8, [x19, #-0x18]
0x54dcc	880240f9	ldr	x8, [x20]
0x54dd0	080140f9	ldr	x8, [x8]
0x54dd4	a07a78f8	ldr	x0, [x21, x24, lsl #3]
0x54dd8	a17a79f8	ldr	x1, [x21, x25, lsl #3]
0x54ddc	00013fd6	blr	x8
0x54de0	f70300aa	mov	x23, x0
0x54de4	880240f9	ldr	x8, [x20]
0x54de8	080140f9	ldr	x8, [x8]
0x54dec	a07a7cf8	ldr	x0, [x21, x28, lsl #3]
0x54df0	a17a78f8	ldr	x1, [x21, x24, lsl #3]
0x54df4	00013fd6	blr	x8
0x54df8	17010036	tbz	w23, #0x0, 0x54e18 <_WeChatMain+0x3b5ac>
0x54dfc	a17a79f8	ldr	x1, [x21, x25, lsl #3]
0x54e00	a0020034	cbz	w0, 0x54e54 <_WeChatMain+0x3b5e8>
0x54e04	a87a7cf8	ldr	x8, [x21, x28, lsl #3]
0x54e08	a87a39f8	str	x8, [x21, x25, lsl #3]
0x54e0c	a17a3cf8	str	x1, [x21, x28, lsl #3]
0x54e10	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54e14	1d000014	b	0x54e88 <_WeChatMain+0x3b61c>
0x54e18	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54e1c	60030034	cbz	w0, 0x54e88 <_WeChatMain+0x3b61c>
0x54e20	a07a7cf8	ldr	x0, [x21, x28, lsl #3]
0x54e24	a07a38f8	str	x0, [x21, x24, lsl #3]
0x54e28	a87a3cf8	str	x8, [x21, x28, lsl #3]
0x54e2c	880240f9	ldr	x8, [x20]
0x54e30	080140f9	ldr	x8, [x8]
0x54e34	a17a79f8	ldr	x1, [x21, x25, lsl #3]
0x54e38	00013fd6	blr	x8
0x54e3c	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54e40	40020034	cbz	w0, 0x54e88 <_WeChatMain+0x3b61c>
0x54e44	a97a79f8	ldr	x9, [x21, x25, lsl #3]
0x54e48	a87a39f8	str	x8, [x21, x25, lsl #3]
0x54e4c	a97a38f8	str	x9, [x21, x24, lsl #3]
0x54e50	0d000014	b	0x54e84 <_WeChatMain+0x3b618>
0x54e54	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54e58	a87a39f8	str	x8, [x21, x25, lsl #3]
0x54e5c	a17a38f8	str	x1, [x21, x24, lsl #3]
0x54e60	880240f9	ldr	x8, [x20]
0x54e64	080140f9	ldr	x8, [x8]
0x54e68	a07a7cf8	ldr	x0, [x21, x28, lsl #3]
0x54e6c	00013fd6	blr	x8
0x54e70	a87a78f8	ldr	x8, [x21, x24, lsl #3]
0x54e74	a0000034	cbz	w0, 0x54e88 <_WeChatMain+0x3b61c>
0x54e78	a97a7cf8	ldr	x9, [x21, x28, lsl #3]
0x54e7c	a97a38f8	str	x9, [x21, x24, lsl #3]
0x54e80	a87a3cf8	str	x8, [x21, x28, lsl #3]
0x54e84	e80309aa	mov	x8, x9
0x54e88	a90240f9	ldr	x9, [x21]
0x54e8c	a80200f9	str	x8, [x21]
0x54e90	a97a38f8	str	x9, [x21, x24, lsl #3]
0x54e94	d6000037	tbnz	w22, #0x0, 0x54eac <_WeChatMain+0x3b640>
0x54e98	880240f9	ldr	x8, [x20]
0x54e9c	080140f9	ldr	x8, [x8]
0x54ea0	a0867fa9	ldp	x0, x1, [x21, #-0x8]
0x54ea4	00013fd6	blr	x8
0x54ea8	80030036	tbz	w0, #0x0, 0x54f18 <_WeChatMain+0x3b6ac>
0x54eac	e00315aa	mov	x0, x21
0x54eb0	e10313aa	mov	x1, x19
0x54eb4	e20314aa	mov	x2, x20
0x54eb8	0b010094	bl	0x552e4 <_WeChatMain+0x3ba78>
0x54ebc	f70300aa	mov	x23, x0
0x54ec0	c1010036	tbz	w1, #0x0, 0x54ef8 <_WeChatMain+0x3b68c>
0x54ec4	e00315aa	mov	x0, x21
0x54ec8	e10317aa	mov	x1, x23
0x54ecc	e20314aa	mov	x2, x20
0x54ed0	50010094	bl	0x55410 <_WeChatMain+0x3bba4>
0x54ed4	f90300aa	mov	x25, x0
0x54ed8	f8220091	add	x24, x23, #0x8
0x54edc	e00318aa	mov	x0, x24
0x54ee0	e10313aa	mov	x1, x19
0x54ee4	e20314aa	mov	x2, x20
0x54ee8	4a010094	bl	0x55410 <_WeChatMain+0x3bba4>
0x54eec	60020035	cbnz	w0, 0x54f38 <_WeChatMain+0x3b6cc>
0x54ef0	68070091	add	x8, x27, #0x1
0x54ef4	79dc0737	tbnz	w25, #0x0, 0x54a80 <_WeChatMain+0x3b214>
0x54ef8	e3031bcb	neg	x3, x27
0x54efc	c4020012	and	w4, w22, #0x1
0x54f00	e00315aa	mov	x0, x21
0x54f04	e10317aa	mov	x1, x23
0x54f08	e20314aa	mov	x2, x20
0x54f0c	cffeff97	bl	0x54a48 <_WeChatMain+0x3b1dc>
0x54f10	f8220091	add	x24, x23, #0x8
0x54f14	06000014	b	0x54f2c <_WeChatMain+0x3b6c0>
0x54f18	e00315aa	mov	x0, x21
0x54f1c	e10313aa	mov	x1, x19
0x54f20	e20314aa	mov	x2, x20
0x54f24	a7000094	bl	0x551c0 <_WeChatMain+0x3b954>
0x54f28	f80300aa	mov	x24, x0
0x54f2c	16008052	mov	w22, #0x0               ; =0
0x54f30	e3031bcb	neg	x3, x27
0x54f34	d2feff17	b	0x54a7c <_WeChatMain+0x3b210>
0x54f38	e3031bcb	neg	x3, x27
0x54f3c	f30317aa	mov	x19, x23
0x54f40	d9d90736	tbz	w25, #0x0, 0x54a78 <_WeChatMain+0x3b20c>
0x54f44	98000014	b	0x551a4 <_WeChatMain+0x3b938>
0x54f48	880240f9	ldr	x8, [x20]
0x54f4c	080140f9	ldr	x8, [x8]
0x54f50	a10240a9	ldp	x1, x0, [x21]
0x54f54	00013fd6	blr	x8
0x54f58	f60300aa	mov	x22, x0
0x54f5c	880240f9	ldr	x8, [x20]
0x54f60	080140f9	ldr	x8, [x8]
0x54f64	60825ff8	ldur	x0, [x19, #-0x8]
0x54f68	a10640f9	ldr	x1, [x21, #0x8]
0x54f6c	00013fd6	blr	x8
0x54f70	960b0036	tbz	w22, #0x0, 0x550e0 <_WeChatMain+0x3b874>
0x54f74	a10240f9	ldr	x1, [x21]
0x54f78	00100034	cbz	w0, 0x55178 <_WeChatMain+0x3b90c>
0x54f7c	68825ff8	ldur	x8, [x19, #-0x8]
0x54f80	a80200f9	str	x8, [x21]
0x54f84	61821ff8	stur	x1, [x19, #-0x8]
0x54f88	87000014	b	0x551a4 <_WeChatMain+0x3b938>
0x54f8c	642200d1	sub	x4, x19, #0x8
0x54f90	a1220091	add	x1, x21, #0x8
0x54f94	a2420091	add	x2, x21, #0x10
0x54f98	a3620091	add	x3, x21, #0x18
0x54f9c	e00315aa	mov	x0, x21
0x54fa0	e50314aa	mov	x5, x20
0x54fa4	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x54fa8	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x54fac	f65743a9	ldp	x22, x21, [sp, #0x30]
0x54fb0	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x54fb4	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x54fb8	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x54fbc	25020014	b	0x55850 <_WeChatMain+0x3bfe4>
0x54fc0	880240f9	ldr	x8, [x20]
0x54fc4	080140f9	ldr	x8, [x8]
0x54fc8	60825ff8	ldur	x0, [x19, #-0x8]
0x54fcc	a10240f9	ldr	x1, [x21]
0x54fd0	00013fd6	blr	x8
0x54fd4	800e0034	cbz	w0, 0x551a4 <_WeChatMain+0x3b938>
0x54fd8	a80240f9	ldr	x8, [x21]
0x54fdc	69825ff8	ldur	x9, [x19, #-0x8]
0x54fe0	a90200f9	str	x9, [x21]
0x54fe4	6f000014	b	0x551a0 <_WeChatMain+0x3b934>
0x54fe8	632200d1	sub	x3, x19, #0x8
0x54fec	a1220091	add	x1, x21, #0x8
0x54ff0	a2420091	add	x2, x21, #0x10
0x54ff4	e00315aa	mov	x0, x21
0x54ff8	e40314aa	mov	x4, x20
0x54ffc	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x55000	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x55004	f65743a9	ldp	x22, x21, [sp, #0x30]
0x55008	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x5500c	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x55010	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x55014	b4010014	b	0x556e4 <_WeChatMain+0x3be78>
0x55018	bf0213eb	cmp	x21, x19
0x5501c	a8220091	add	x8, x21, #0x8
0x55020	041153fa	ccmp	x8, x19, #0x4, ne
0x55024	e9179f1a	cset	w9, eq
0x55028	96070036	tbz	w22, #0x0, 0x55118 <_WeChatMain+0x3b8ac>
0x5502c	c90b0037	tbnz	w9, #0x0, 0x551a4 <_WeChatMain+0x3b938>
0x55030	170080d2	mov	x23, #0x0               ; =0
0x55034	f80315aa	mov	x24, x21
0x55038	07000014	b	0x55054 <_WeChatMain+0x3b7e8>
0x5503c	e80315aa	mov	x8, x21
0x55040	160100f9	str	x22, [x8]
0x55044	08230091	add	x8, x24, #0x8
0x55048	f7220091	add	x23, x23, #0x8
0x5504c	1f0113eb	cmp	x8, x19
0x55050	a00a0054	b.eq	0x551a4 <_WeChatMain+0x3b938>
0x55054	010340a9	ldp	x1, x0, [x24]
0x55058	f80308aa	mov	x24, x8
0x5505c	880240f9	ldr	x8, [x20]
0x55060	080140f9	ldr	x8, [x8]
0x55064	00013fd6	blr	x8
0x55068	e0feff34	cbz	w0, 0x55044 <_WeChatMain+0x3b7d8>
0x5506c	160340f9	ldr	x22, [x24]
0x55070	f90317aa	mov	x25, x23
0x55074	a802198b	add	x8, x21, x25
0x55078	090140f9	ldr	x9, [x8]
0x5507c	090500f9	str	x9, [x8, #0x8]
0x55080	f9fdffb4	cbz	x25, 0x5503c <_WeChatMain+0x3b7d0>
0x55084	890240f9	ldr	x9, [x20]
0x55088	290140f9	ldr	x9, [x9]
0x5508c	01815ff8	ldur	x1, [x8, #-0x8]
0x55090	e00316aa	mov	x0, x22
0x55094	20013fd6	blr	x9
0x55098	392300d1	sub	x25, x25, #0x8
0x5509c	c0fe0737	tbnz	w0, #0x0, 0x55074 <_WeChatMain+0x3b808>
0x550a0	a802198b	add	x8, x21, x25
0x550a4	08210091	add	x8, x8, #0x8
0x550a8	e6ffff17	b	0x55040 <_WeChatMain+0x3b7d4>
0x550ac	bf0213eb	cmp	x21, x19
0x550b0	a0070054	b.eq	0x551a4 <_WeChatMain+0x3b938>
0x550b4	e00315aa	mov	x0, x21
0x550b8	e10313aa	mov	x1, x19
0x550bc	e20313aa	mov	x2, x19
0x550c0	e30314aa	mov	x3, x20
0x550c4	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x550c8	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x550cc	f65743a9	ldp	x22, x21, [sp, #0x30]
0x550d0	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x550d4	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x550d8	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x550dc	17020014	b	0x55938 <_WeChatMain+0x3c0cc>
0x550e0	20060034	cbz	w0, 0x551a4 <_WeChatMain+0x3b938>
0x550e4	a80640f9	ldr	x8, [x21, #0x8]
0x550e8	69825ff8	ldur	x9, [x19, #-0x8]
0x550ec	a90600f9	str	x9, [x21, #0x8]
0x550f0	68821ff8	stur	x8, [x19, #-0x8]
0x550f4	880240f9	ldr	x8, [x20]
0x550f8	080140f9	ldr	x8, [x8]
0x550fc	a10240a9	ldp	x1, x0, [x21]
0x55100	00013fd6	blr	x8
0x55104	00050034	cbz	w0, 0x551a4 <_WeChatMain+0x3b938>
0x55108	a002c03d	ldr	q0, [x21]
0x5510c	0040006e	ext.16b	v0, v0, v0, #0x8
0x55110	a002803d	str	q0, [x21]
0x55114	24000014	b	0x551a4 <_WeChatMain+0x3b938>
0x55118	a9000036	tbz	w9, #0x0, 0x5512c <_WeChatMain+0x3b8c0>
0x5511c	22000014	b	0x551a4 <_WeChatMain+0x3b938>
0x55120	a8220091	add	x8, x21, #0x8
0x55124	1f0113eb	cmp	x8, x19
0x55128	e0030054	b.eq	0x551a4 <_WeChatMain+0x3b938>
0x5512c	a10240a9	ldp	x1, x0, [x21]
0x55130	f50308aa	mov	x21, x8
0x55134	880240f9	ldr	x8, [x20]
0x55138	080140f9	ldr	x8, [x8]
0x5513c	00013fd6	blr	x8
0x55140	00ffff34	cbz	w0, 0x55120 <_WeChatMain+0x3b8b4>
0x55144	b60240f9	ldr	x22, [x21]
0x55148	f70315aa	mov	x23, x21
0x5514c	e80317aa	mov	x8, x23
0x55150	e98e5ff8	ldr	x9, [x23, #-0x8]!
0x55154	090100f9	str	x9, [x8]
0x55158	890240f9	ldr	x9, [x20]
0x5515c	290140f9	ldr	x9, [x9]
0x55160	01015ff8	ldur	x1, [x8, #-0x10]
0x55164	e00316aa	mov	x0, x22
0x55168	20013fd6	blr	x9
0x5516c	00ff0737	tbnz	w0, #0x0, 0x5514c <_WeChatMain+0x3b8e0>
0x55170	f60200f9	str	x22, [x23]
0x55174	ebffff17	b	0x55120 <_WeChatMain+0x3b8b4>
0x55178	a80640f9	ldr	x8, [x21, #0x8]
0x5517c	a80600a9	stp	x8, x1, [x21]
0x55180	880240f9	ldr	x8, [x20]
0x55184	080140f9	ldr	x8, [x8]
0x55188	60825ff8	ldur	x0, [x19, #-0x8]
0x5518c	00013fd6	blr	x8
0x55190	a0000034	cbz	w0, 0x551a4 <_WeChatMain+0x3b938>
0x55194	a80640f9	ldr	x8, [x21, #0x8]
0x55198	69825ff8	ldur	x9, [x19, #-0x8]
0x5519c	a90600f9	str	x9, [x21, #0x8]
0x551a0	68821ff8	stur	x8, [x19, #-0x8]
0x551a4	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x551a8	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x551ac	f65743a9	ldp	x22, x21, [sp, #0x30]
0x551b0	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x551b4	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x551b8	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x551bc	c0035fd6	ret
0x551c0	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x551c4	f65701a9	stp	x22, x21, [sp, #0x10]
0x551c8	f44f02a9	stp	x20, x19, [sp, #0x20]
0x551cc	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x551d0	fdc30091	add	x29, sp, #0x30
0x551d4	f50302aa	mov	x21, x2
0x551d8	f60301aa	mov	x22, x1
0x551dc	f40300aa	mov	x20, x0
0x551e0	130040f9	ldr	x19, [x0]
0x551e4	480040f9	ldr	x8, [x2]
0x551e8	080140f9	ldr	x8, [x8]
0x551ec	21805ff8	ldur	x1, [x1, #-0x8]
0x551f0	e00313aa	mov	x0, x19
0x551f4	00013fd6	blr	x8
0x551f8	20010036	tbz	w0, #0x0, 0x5521c <_WeChatMain+0x3b9b0>
0x551fc	f70314aa	mov	x23, x20
0x55200	e18e40f8	ldr	x1, [x23, #0x8]!
0x55204	a80240f9	ldr	x8, [x21]
0x55208	080140f9	ldr	x8, [x8]
0x5520c	e00313aa	mov	x0, x19
0x55210	00013fd6	blr	x8
0x55214	60ff0736	tbz	w0, #0x0, 0x55200 <_WeChatMain+0x3b994>
0x55218	0c000014	b	0x55248 <_WeChatMain+0x3b9dc>
0x5521c	98220091	add	x24, x20, #0x8
0x55220	f70318aa	mov	x23, x24
0x55224	1f0316eb	cmp	x24, x22
0x55228	02010054	b.hs	0x55248 <_WeChatMain+0x3b9dc>
0x5522c	a80240f9	ldr	x8, [x21]
0x55230	080140f9	ldr	x8, [x8]
0x55234	f80317aa	mov	x24, x23
0x55238	018740f8	ldr	x1, [x24], #0x8
0x5523c	e00313aa	mov	x0, x19
0x55240	00013fd6	blr	x8
0x55244	e0feff34	cbz	w0, 0x55220 <_WeChatMain+0x3b9b4>
0x55248	ff0216eb	cmp	x23, x22
0x5524c	02030054	b.hs	0x552ac <_WeChatMain+0x3ba40>
0x55250	c18e5ff8	ldr	x1, [x22, #-0x8]!
0x55254	a80240f9	ldr	x8, [x21]
0x55258	080140f9	ldr	x8, [x8]
0x5525c	e00313aa	mov	x0, x19
0x55260	00013fd6	blr	x8
0x55264	60ff0737	tbnz	w0, #0x0, 0x55250 <_WeChatMain+0x3b9e4>
0x55268	11000014	b	0x552ac <_WeChatMain+0x3ba40>
0x5526c	e80240f9	ldr	x8, [x23]
0x55270	c90240f9	ldr	x9, [x22]
0x55274	e90200f9	str	x9, [x23]
0x55278	c80200f9	str	x8, [x22]
0x5527c	e18e40f8	ldr	x1, [x23, #0x8]!
0x55280	a80240f9	ldr	x8, [x21]
0x55284	080140f9	ldr	x8, [x8]
0x55288	e00313aa	mov	x0, x19
0x5528c	00013fd6	blr	x8
0x55290	60ffff34	cbz	w0, 0x5527c <_WeChatMain+0x3ba10>
0x55294	c18e5ff8	ldr	x1, [x22, #-0x8]!
0x55298	a80240f9	ldr	x8, [x21]
0x5529c	080140f9	ldr	x8, [x8]
0x552a0	e00313aa	mov	x0, x19
0x552a4	00013fd6	blr	x8
0x552a8	60ff0737	tbnz	w0, #0x0, 0x55294 <_WeChatMain+0x3ba28>
0x552ac	ff0216eb	cmp	x23, x22
0x552b0	e3fdff54	b.lo	0x5526c <_WeChatMain+0x3ba00>
0x552b4	e82200d1	sub	x8, x23, #0x8
0x552b8	1f0114eb	cmp	x8, x20
0x552bc	60000054	b.eq	0x552c8 <_WeChatMain+0x3ba5c>
0x552c0	080140f9	ldr	x8, [x8]
0x552c4	880200f9	str	x8, [x20]
0x552c8	f3821ff8	stur	x19, [x23, #-0x8]
0x552cc	e00317aa	mov	x0, x23
0x552d0	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x552d4	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x552d8	f65741a9	ldp	x22, x21, [sp, #0x10]
0x552dc	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x552e0	c0035fd6	ret
0x552e4	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x552e8	f85f01a9	stp	x24, x23, [sp, #0x10]
0x552ec	f65702a9	stp	x22, x21, [sp, #0x20]
0x552f0	f44f03a9	stp	x20, x19, [sp, #0x30]
0x552f4	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x552f8	fd030191	add	x29, sp, #0x40
0x552fc	f60302aa	mov	x22, x2
0x55300	f30301aa	mov	x19, x1
0x55304	f50300aa	mov	x21, x0
0x55308	190080d2	mov	x25, #0x0               ; =0
0x5530c	140040f9	ldr	x20, [x0]
0x55310	a802198b	add	x8, x21, x25
0x55314	c90240f9	ldr	x9, [x22]
0x55318	290140f9	ldr	x9, [x9]
0x5531c	000540f9	ldr	x0, [x8, #0x8]
0x55320	e10314aa	mov	x1, x20
0x55324	20013fd6	blr	x9
0x55328	39230091	add	x25, x25, #0x8
0x5532c	20ff0737	tbnz	w0, #0x0, 0x55310 <_WeChatMain+0x3baa4>
0x55330	b802198b	add	x24, x21, x25
0x55334	172300d1	sub	x23, x24, #0x8
0x55338	3f2300f1	cmp	x25, #0x8
0x5533c	c0010054	b.eq	0x55374 <_WeChatMain+0x3bb08>
0x55340	608e5ff8	ldr	x0, [x19, #-0x8]!
0x55344	c80240f9	ldr	x8, [x22]
0x55348	080140f9	ldr	x8, [x8]
0x5534c	e10314aa	mov	x1, x20
0x55350	00013fd6	blr	x8
0x55354	60ffff34	cbz	w0, 0x55340 <_WeChatMain+0x3bad4>
0x55358	09000014	b	0x5537c <_WeChatMain+0x3bb10>
0x5535c	608e5ff8	ldr	x0, [x19, #-0x8]!
0x55360	c80240f9	ldr	x8, [x22]
0x55364	080140f9	ldr	x8, [x8]
0x55368	e10314aa	mov	x1, x20
0x5536c	00013fd6	blr	x8
0x55370	60000037	tbnz	w0, #0x0, 0x5537c <_WeChatMain+0x3bb10>
0x55374	1f0313eb	cmp	x24, x19
0x55378	23ffff54	b.lo	0x5535c <_WeChatMain+0x3baf0>
0x5537c	1f0313eb	cmp	x24, x19
0x55380	c2020054	b.hs	0x553d8 <_WeChatMain+0x3bb6c>
0x55384	f70318aa	mov	x23, x24
0x55388	f90313aa	mov	x25, x19
0x5538c	e80240f9	ldr	x8, [x23]
0x55390	290340f9	ldr	x9, [x25]
0x55394	e90200f9	str	x9, [x23]
0x55398	280300f9	str	x8, [x25]
0x5539c	e08e40f8	ldr	x0, [x23, #0x8]!
0x553a0	c80240f9	ldr	x8, [x22]
0x553a4	080140f9	ldr	x8, [x8]
0x553a8	e10314aa	mov	x1, x20
0x553ac	00013fd6	blr	x8
0x553b0	60ff0737	tbnz	w0, #0x0, 0x5539c <_WeChatMain+0x3bb30>
0x553b4	208f5ff8	ldr	x0, [x25, #-0x8]!
0x553b8	c80240f9	ldr	x8, [x22]
0x553bc	080140f9	ldr	x8, [x8]
0x553c0	e10314aa	mov	x1, x20
0x553c4	00013fd6	blr	x8
0x553c8	60ffff34	cbz	w0, 0x553b4 <_WeChatMain+0x3bb48>
0x553cc	ff0219eb	cmp	x23, x25
0x553d0	e3fdff54	b.lo	0x5538c <_WeChatMain+0x3bb20>
0x553d4	f72200d1	sub	x23, x23, #0x8
0x553d8	ff0215eb	cmp	x23, x21
0x553dc	60000054	b.eq	0x553e8 <_WeChatMain+0x3bb7c>
0x553e0	e80240f9	ldr	x8, [x23]
0x553e4	a80200f9	str	x8, [x21]
0x553e8	1f0313eb	cmp	x24, x19
0x553ec	e1379f1a	cset	w1, hs
0x553f0	f40200f9	str	x20, [x23]
0x553f4	e00317aa	mov	x0, x23
0x553f8	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x553fc	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x55400	f65742a9	ldp	x22, x21, [sp, #0x20]
0x55404	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x55408	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x5540c	c0035fd6	ret
0x55410	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x55414	f85f01a9	stp	x24, x23, [sp, #0x10]
0x55418	f65702a9	stp	x22, x21, [sp, #0x20]
0x5541c	f44f03a9	stp	x20, x19, [sp, #0x30]
0x55420	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x55424	fd030191	add	x29, sp, #0x40
0x55428	f50302aa	mov	x21, x2
0x5542c	f40301aa	mov	x20, x1
0x55430	f30300aa	mov	x19, x0
0x55434	280000cb	sub	x8, x1, x0
0x55438	08fd4393	asr	x8, x8, #3
0x5543c	1f0900f1	cmp	x8, #0x2
0x55440	ec010054	b.gt	0x5547c <_WeChatMain+0x3bc10>
0x55444	a3130054	b.lo	0x556b8 <_WeChatMain+0x3be4c>
0x55448	1f0900f1	cmp	x8, #0x2
0x5544c	61050054	b.ne	0x554f8 <_WeChatMain+0x3bc8c>
0x55450	a80240f9	ldr	x8, [x21]
0x55454	080140f9	ldr	x8, [x8]
0x55458	80825ff8	ldur	x0, [x20, #-0x8]
0x5545c	610240f9	ldr	x1, [x19]
0x55460	00013fd6	blr	x8
0x55464	a0120034	cbz	w0, 0x556b8 <_WeChatMain+0x3be4c>
0x55468	680240f9	ldr	x8, [x19]
0x5546c	89825ff8	ldur	x9, [x20, #-0x8]
0x55470	690200f9	str	x9, [x19]
0x55474	88821ff8	stur	x8, [x20, #-0x8]
0x55478	90000014	b	0x556b8 <_WeChatMain+0x3be4c>
0x5547c	1f0d00f1	cmp	x8, #0x3
0x55480	a0010054	b.eq	0x554b4 <_WeChatMain+0x3bc48>
0x55484	1f1100f1	cmp	x8, #0x4
0x55488	c0050054	b.eq	0x55540 <_WeChatMain+0x3bcd4>
0x5548c	1f1500f1	cmp	x8, #0x5
0x55490	41030054	b.ne	0x554f8 <_WeChatMain+0x3bc8c>
0x55494	842200d1	sub	x4, x20, #0x8
0x55498	61220091	add	x1, x19, #0x8
0x5549c	62420091	add	x2, x19, #0x10
0x554a0	63620091	add	x3, x19, #0x18
0x554a4	e00313aa	mov	x0, x19
0x554a8	e50315aa	mov	x5, x21
0x554ac	e9000094	bl	0x55850 <_WeChatMain+0x3bfe4>
0x554b0	82000014	b	0x556b8 <_WeChatMain+0x3be4c>
0x554b4	a80240f9	ldr	x8, [x21]
0x554b8	080140f9	ldr	x8, [x8]
0x554bc	610240a9	ldp	x1, x0, [x19]
0x554c0	00013fd6	blr	x8
0x554c4	f60300aa	mov	x22, x0
0x554c8	a80240f9	ldr	x8, [x21]
0x554cc	080140f9	ldr	x8, [x8]
0x554d0	80825ff8	ldur	x0, [x20, #-0x8]
0x554d4	610640f9	ldr	x1, [x19, #0x8]
0x554d8	00013fd6	blr	x8
0x554dc	16040036	tbz	w22, #0x0, 0x5555c <_WeChatMain+0x3bcf0>
0x554e0	610240f9	ldr	x1, [x19]
0x554e4	00070034	cbz	w0, 0x555c4 <_WeChatMain+0x3bd58>
0x554e8	88825ff8	ldur	x8, [x20, #-0x8]
0x554ec	680200f9	str	x8, [x19]
0x554f0	81821ff8	stur	x1, [x20, #-0x8]
0x554f4	71000014	b	0x556b8 <_WeChatMain+0x3be4c>
0x554f8	a80240f9	ldr	x8, [x21]
0x554fc	080140f9	ldr	x8, [x8]
0x55500	610240a9	ldp	x1, x0, [x19]
0x55504	00013fd6	blr	x8
0x55508	f60300aa	mov	x22, x0
0x5550c	f70313aa	mov	x23, x19
0x55510	e00e41f8	ldr	x0, [x23, #0x10]!
0x55514	a80240f9	ldr	x8, [x21]
0x55518	080140f9	ldr	x8, [x8]
0x5551c	610640f9	ldr	x1, [x19, #0x8]
0x55520	00013fd6	blr	x8
0x55524	96030036	tbz	w22, #0x0, 0x55594 <_WeChatMain+0x3bd28>
0x55528	610240f9	ldr	x1, [x19]
0x5552c	40060034	cbz	w0, 0x555f4 <_WeChatMain+0x3bd88>
0x55530	680a40f9	ldr	x8, [x19, #0x10]
0x55534	680200f9	str	x8, [x19]
0x55538	610a00f9	str	x1, [x19, #0x10]
0x5553c	37000014	b	0x55618 <_WeChatMain+0x3bdac>
0x55540	832200d1	sub	x3, x20, #0x8
0x55544	61220091	add	x1, x19, #0x8
0x55548	62420091	add	x2, x19, #0x10
0x5554c	e00313aa	mov	x0, x19
0x55550	e40315aa	mov	x4, x21
0x55554	64000094	bl	0x556e4 <_WeChatMain+0x3be78>
0x55558	58000014	b	0x556b8 <_WeChatMain+0x3be4c>
0x5555c	e00a0034	cbz	w0, 0x556b8 <_WeChatMain+0x3be4c>
0x55560	680640f9	ldr	x8, [x19, #0x8]
0x55564	89825ff8	ldur	x9, [x20, #-0x8]
0x55568	690600f9	str	x9, [x19, #0x8]
0x5556c	88821ff8	stur	x8, [x20, #-0x8]
0x55570	a80240f9	ldr	x8, [x21]
0x55574	080140f9	ldr	x8, [x8]
0x55578	610240a9	ldp	x1, x0, [x19]
0x5557c	00013fd6	blr	x8
0x55580	c0090034	cbz	w0, 0x556b8 <_WeChatMain+0x3be4c>
0x55584	6002c03d	ldr	q0, [x19]
0x55588	0040006e	ext.16b	v0, v0, v0, #0x8
0x5558c	6002803d	str	q0, [x19]
0x55590	4a000014	b	0x556b8 <_WeChatMain+0x3be4c>
0x55594	20040034	cbz	w0, 0x55618 <_WeChatMain+0x3bdac>
0x55598	688240a9	ldp	x8, x0, [x19, #0x8]
0x5559c	610240f9	ldr	x1, [x19]
0x555a0	60a200a9	stp	x0, x8, [x19, #0x8]
0x555a4	a80240f9	ldr	x8, [x21]
0x555a8	080140f9	ldr	x8, [x8]
0x555ac	00013fd6	blr	x8
0x555b0	40030034	cbz	w0, 0x55618 <_WeChatMain+0x3bdac>
0x555b4	6002c03d	ldr	q0, [x19]
0x555b8	0040006e	ext.16b	v0, v0, v0, #0x8
0x555bc	6002803d	str	q0, [x19]
0x555c0	16000014	b	0x55618 <_WeChatMain+0x3bdac>
0x555c4	680640f9	ldr	x8, [x19, #0x8]
0x555c8	680600a9	stp	x8, x1, [x19]
0x555cc	a80240f9	ldr	x8, [x21]
0x555d0	080140f9	ldr	x8, [x8]
0x555d4	80825ff8	ldur	x0, [x20, #-0x8]
0x555d8	00013fd6	blr	x8
0x555dc	e0060034	cbz	w0, 0x556b8 <_WeChatMain+0x3be4c>
0x555e0	680640f9	ldr	x8, [x19, #0x8]
0x555e4	89825ff8	ldur	x9, [x20, #-0x8]
0x555e8	690600f9	str	x9, [x19, #0x8]
0x555ec	88821ff8	stur	x8, [x20, #-0x8]
0x555f0	32000014	b	0x556b8 <_WeChatMain+0x3be4c>
0x555f4	688240a9	ldp	x8, x0, [x19, #0x8]
0x555f8	680600a9	stp	x8, x1, [x19]
0x555fc	a80240f9	ldr	x8, [x21]
0x55600	080140f9	ldr	x8, [x8]
0x55604	00013fd6	blr	x8
0x55608	80000034	cbz	w0, 0x55618 <_WeChatMain+0x3bdac>
0x5560c	6082c03c	ldur	q0, [x19, #0x8]
0x55610	0040006e	ext.16b	v0, v0, v0, #0x8
0x55614	6082803c	stur	q0, [x19, #0x8]
0x55618	78620091	add	x24, x19, #0x18
0x5561c	1f0314eb	cmp	x24, x20
0x55620	c0040054	b.eq	0x556b8 <_WeChatMain+0x3be4c>
0x55624	190080d2	mov	x25, #0x0               ; =0
0x55628	1a008052	mov	w26, #0x0               ; =0
0x5562c	0c000014	b	0x5565c <_WeChatMain+0x3bdf0>
0x55630	e80313aa	mov	x8, x19
0x55634	160100f9	str	x22, [x8]
0x55638	5a070011	add	w26, w26, #0x1
0x5563c	5f230071	cmp	w26, #0x8
0x55640	a0040054	b.eq	0x556d4 <_WeChatMain+0x3be68>
0x55644	f70318aa	mov	x23, x24
0x55648	08230091	add	x8, x24, #0x8
0x5564c	39230091	add	x25, x25, #0x8
0x55650	f80308aa	mov	x24, x8
0x55654	1f0114eb	cmp	x8, x20
0x55658	00030054	b.eq	0x556b8 <_WeChatMain+0x3be4c>
0x5565c	a80240f9	ldr	x8, [x21]
0x55660	080140f9	ldr	x8, [x8]
0x55664	000340f9	ldr	x0, [x24]
0x55668	e10240f9	ldr	x1, [x23]
0x5566c	00013fd6	blr	x8
0x55670	a0feff34	cbz	w0, 0x55644 <_WeChatMain+0x3bdd8>
0x55674	160340f9	ldr	x22, [x24]
0x55678	f70319aa	mov	x23, x25
0x5567c	6802178b	add	x8, x19, x23
0x55680	090940f9	ldr	x9, [x8, #0x10]
0x55684	090d00f9	str	x9, [x8, #0x18]
0x55688	ff4200b1	cmn	x23, #0x10
0x5568c	20fdff54	b.eq	0x55630 <_WeChatMain+0x3bdc4>
0x55690	a90240f9	ldr	x9, [x21]
0x55694	290140f9	ldr	x9, [x9]
0x55698	010540f9	ldr	x1, [x8, #0x8]
0x5569c	e00316aa	mov	x0, x22
0x556a0	20013fd6	blr	x9
0x556a4	f72200d1	sub	x23, x23, #0x8
0x556a8	a0fe0737	tbnz	w0, #0x0, 0x5567c <_WeChatMain+0x3be10>
0x556ac	6802178b	add	x8, x19, x23
0x556b0	08610091	add	x8, x8, #0x18
0x556b4	e0ffff17	b	0x55634 <_WeChatMain+0x3bdc8>
0x556b8	20008052	mov	w0, #0x1                ; =1
0x556bc	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x556c0	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x556c4	f65742a9	ldp	x22, x21, [sp, #0x20]
0x556c8	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x556cc	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x556d0	c0035fd6	ret
0x556d4	08230091	add	x8, x24, #0x8
0x556d8	1f0114eb	cmp	x8, x20
0x556dc	e0179f1a	cset	w0, eq
0x556e0	f7ffff17	b	0x556bc <_WeChatMain+0x3be50>
0x556e4	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x556e8	f65701a9	stp	x22, x21, [sp, #0x10]
0x556ec	f44f02a9	stp	x20, x19, [sp, #0x20]
0x556f0	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x556f4	fdc30091	add	x29, sp, #0x30
0x556f8	f50304aa	mov	x21, x4
0x556fc	f70303aa	mov	x23, x3
0x55700	f60302aa	mov	x22, x2
0x55704	f30301aa	mov	x19, x1
0x55708	f40300aa	mov	x20, x0
0x5570c	880040f9	ldr	x8, [x4]
0x55710	080140f9	ldr	x8, [x8]
0x55714	200040f9	ldr	x0, [x1]
0x55718	810240f9	ldr	x1, [x20]
0x5571c	00013fd6	blr	x8
0x55720	f80300aa	mov	x24, x0
0x55724	a80240f9	ldr	x8, [x21]
0x55728	080140f9	ldr	x8, [x8]
0x5572c	c00240f9	ldr	x0, [x22]
0x55730	610240f9	ldr	x1, [x19]
0x55734	00013fd6	blr	x8
0x55738	f8000036	tbz	w24, #0x0, 0x55754 <_WeChatMain+0x3bee8>
0x5573c	810240f9	ldr	x1, [x20]
0x55740	a0020034	cbz	w0, 0x55794 <_WeChatMain+0x3bf28>
0x55744	c80240f9	ldr	x8, [x22]
0x55748	880200f9	str	x8, [x20]
0x5574c	c10200f9	str	x1, [x22]
0x55750	1d000014	b	0x557c4 <_WeChatMain+0x3bf58>
0x55754	80030034	cbz	w0, 0x557c4 <_WeChatMain+0x3bf58>
0x55758	680240f9	ldr	x8, [x19]
0x5575c	c90240f9	ldr	x9, [x22]
0x55760	690200f9	str	x9, [x19]
0x55764	c80200f9	str	x8, [x22]
0x55768	a80240f9	ldr	x8, [x21]
0x5576c	080140f9	ldr	x8, [x8]
0x55770	600240f9	ldr	x0, [x19]
0x55774	810240f9	ldr	x1, [x20]
0x55778	00013fd6	blr	x8
0x5577c	40020034	cbz	w0, 0x557c4 <_WeChatMain+0x3bf58>
0x55780	880240f9	ldr	x8, [x20]
0x55784	690240f9	ldr	x9, [x19]
0x55788	890200f9	str	x9, [x20]
0x5578c	680200f9	str	x8, [x19]
0x55790	0d000014	b	0x557c4 <_WeChatMain+0x3bf58>
0x55794	680240f9	ldr	x8, [x19]
0x55798	880200f9	str	x8, [x20]
0x5579c	610200f9	str	x1, [x19]
0x557a0	a80240f9	ldr	x8, [x21]
0x557a4	080140f9	ldr	x8, [x8]
0x557a8	c00240f9	ldr	x0, [x22]
0x557ac	00013fd6	blr	x8
0x557b0	a0000034	cbz	w0, 0x557c4 <_WeChatMain+0x3bf58>
0x557b4	680240f9	ldr	x8, [x19]
0x557b8	c90240f9	ldr	x9, [x22]
0x557bc	690200f9	str	x9, [x19]
0x557c0	c80200f9	str	x8, [x22]
0x557c4	a80240f9	ldr	x8, [x21]
0x557c8	080140f9	ldr	x8, [x8]
0x557cc	e00240f9	ldr	x0, [x23]
0x557d0	c10240f9	ldr	x1, [x22]
0x557d4	00013fd6	blr	x8
0x557d8	20030034	cbz	w0, 0x5583c <_WeChatMain+0x3bfd0>
0x557dc	c80240f9	ldr	x8, [x22]
0x557e0	e90240f9	ldr	x9, [x23]
0x557e4	c90200f9	str	x9, [x22]
0x557e8	e80200f9	str	x8, [x23]
0x557ec	a80240f9	ldr	x8, [x21]
0x557f0	080140f9	ldr	x8, [x8]
0x557f4	c00240f9	ldr	x0, [x22]
0x557f8	610240f9	ldr	x1, [x19]
0x557fc	00013fd6	blr	x8
0x55800	e0010034	cbz	w0, 0x5583c <_WeChatMain+0x3bfd0>
0x55804	680240f9	ldr	x8, [x19]
0x55808	c90240f9	ldr	x9, [x22]
0x5580c	690200f9	str	x9, [x19]
0x55810	c80200f9	str	x8, [x22]
0x55814	a80240f9	ldr	x8, [x21]
0x55818	080140f9	ldr	x8, [x8]
0x5581c	600240f9	ldr	x0, [x19]
0x55820	810240f9	ldr	x1, [x20]
0x55824	00013fd6	blr	x8
0x55828	a0000034	cbz	w0, 0x5583c <_WeChatMain+0x3bfd0>
0x5582c	880240f9	ldr	x8, [x20]
0x55830	690240f9	ldr	x9, [x19]
0x55834	890200f9	str	x9, [x20]
0x55838	680200f9	str	x8, [x19]
0x5583c	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x55840	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x55844	f65741a9	ldp	x22, x21, [sp, #0x10]
0x55848	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x5584c	c0035fd6	ret
0x55850	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x55854	f65701a9	stp	x22, x21, [sp, #0x10]
0x55858	f44f02a9	stp	x20, x19, [sp, #0x20]
0x5585c	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x55860	fdc30091	add	x29, sp, #0x30
0x55864	f50305aa	mov	x21, x5
0x55868	f80304aa	mov	x24, x4
0x5586c	f70303aa	mov	x23, x3
0x55870	f60302aa	mov	x22, x2
0x55874	f30301aa	mov	x19, x1
0x55878	f40300aa	mov	x20, x0
0x5587c	e40305aa	mov	x4, x5
0x55880	99ffff97	bl	0x556e4 <_WeChatMain+0x3be78>
0x55884	a80240f9	ldr	x8, [x21]
0x55888	080140f9	ldr	x8, [x8]
0x5588c	000340f9	ldr	x0, [x24]
0x55890	e10240f9	ldr	x1, [x23]
0x55894	00013fd6	blr	x8
0x55898	60040034	cbz	w0, 0x55924 <_WeChatMain+0x3c0b8>
0x5589c	e80240f9	ldr	x8, [x23]
0x558a0	090340f9	ldr	x9, [x24]
0x558a4	e90200f9	str	x9, [x23]
0x558a8	080300f9	str	x8, [x24]
0x558ac	a80240f9	ldr	x8, [x21]
0x558b0	080140f9	ldr	x8, [x8]
0x558b4	e00240f9	ldr	x0, [x23]
0x558b8	c10240f9	ldr	x1, [x22]
0x558bc	00013fd6	blr	x8
0x558c0	20030034	cbz	w0, 0x55924 <_WeChatMain+0x3c0b8>
0x558c4	c80240f9	ldr	x8, [x22]
0x558c8	e90240f9	ldr	x9, [x23]
0x558cc	c90200f9	str	x9, [x22]
0x558d0	e80200f9	str	x8, [x23]
0x558d4	a80240f9	ldr	x8, [x21]
0x558d8	080140f9	ldr	x8, [x8]
0x558dc	c00240f9	ldr	x0, [x22]
0x558e0	610240f9	ldr	x1, [x19]
0x558e4	00013fd6	blr	x8
0x558e8	e0010034	cbz	w0, 0x55924 <_WeChatMain+0x3c0b8>
0x558ec	680240f9	ldr	x8, [x19]
0x558f0	c90240f9	ldr	x9, [x22]
0x558f4	690200f9	str	x9, [x19]
0x558f8	c80200f9	str	x8, [x22]
0x558fc	a80240f9	ldr	x8, [x21]
0x55900	080140f9	ldr	x8, [x8]
0x55904	600240f9	ldr	x0, [x19]
0x55908	810240f9	ldr	x1, [x20]
0x5590c	00013fd6	blr	x8
0x55910	a0000034	cbz	w0, 0x55924 <_WeChatMain+0x3c0b8>
0x55914	880240f9	ldr	x8, [x20]
0x55918	690240f9	ldr	x9, [x19]
0x5591c	890200f9	str	x9, [x20]
0x55920	680200f9	str	x8, [x19]
0x55924	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x55928	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x5592c	f65741a9	ldp	x22, x21, [sp, #0x10]
0x55930	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x55934	c0035fd6	ret
0x55938	ff4302d1	sub	sp, sp, #0x90
0x5593c	fc6f03a9	stp	x28, x27, [sp, #0x30]
0x55940	fa6704a9	stp	x26, x25, [sp, #0x40]
0x55944	f85f05a9	stp	x24, x23, [sp, #0x50]
0x55948	f65706a9	stp	x22, x21, [sp, #0x60]
0x5594c	f44f07a9	stp	x20, x19, [sp, #0x70]
0x55950	fd7b08a9	stp	x29, x30, [sp, #0x80]
0x55954	fd030291	add	x29, sp, #0x80
0x55958	fc0302aa	mov	x28, x2
0x5595c	1f0001eb	cmp	x0, x1
0x55960	200e0054	b.eq	0x55b24 <_WeChatMain+0x3c2b8>
0x55964	f30303aa	mov	x19, x3
0x55968	fa0301aa	mov	x26, x1
0x5596c	f50300aa	mov	x21, x0
0x55970	280000cb	sub	x8, x1, x0
0x55974	e81300f9	str	x8, [sp, #0x20]
0x55978	16fd4393	asr	x22, x8, #3
0x5597c	d40a00f1	subs	x20, x22, #0x2
0x55980	8b010054	b.lt	0x559b0 <_WeChatMain+0x3c144>
0x55984	88fe41d3	lsr	x8, x20, #1
0x55988	17050091	add	x23, x8, #0x1
0x5598c	b80e088b	add	x24, x21, x8, lsl #3
0x55990	e00315aa	mov	x0, x21
0x55994	e10313aa	mov	x1, x19
0x55998	e20316aa	mov	x2, x22
0x5599c	e30318aa	mov	x3, x24
0x559a0	b5000094	bl	0x55c74 <_WeChatMain+0x3c408>
0x559a4	182300d1	sub	x24, x24, #0x8
0x559a8	f70600d1	sub	x23, x23, #0x1
0x559ac	37ffffb5	cbnz	x23, 0x55990 <_WeChatMain+0x3c124>
0x559b0	f9031aaa	mov	x25, x26
0x559b4	fa1700f9	str	x26, [sp, #0x28]
0x559b8	5f031ceb	cmp	x26, x28
0x559bc	e00a0054	b.eq	0x55b18 <_WeChatMain+0x3c2ac>
0x559c0	9afe41d3	lsr	x26, x20, #1
0x559c4	b4220091	add	x20, x21, #0x8
0x559c8	a8420091	add	x8, x21, #0x10
0x559cc	e85300a9	stp	x8, x20, [sp]
0x559d0	f91740f9	ldr	x25, [sp, #0x28]
0x559d4	fc0b00f9	str	x28, [sp, #0x10]
0x559d8	07000014	b	0x559f4 <_WeChatMain+0x3c188>
0x559dc	980300f9	str	x24, [x28]
0x559e0	f4f340a9	ldp	x20, x28, [sp, #0x8]
0x559e4	f90f40f9	ldr	x25, [sp, #0x18]
0x559e8	39230091	add	x25, x25, #0x8
0x559ec	3f031ceb	cmp	x25, x28
0x559f0	40090054	b.eq	0x55b18 <_WeChatMain+0x3c2ac>
0x559f4	680240f9	ldr	x8, [x19]
0x559f8	080140f9	ldr	x8, [x8]
0x559fc	200340f9	ldr	x0, [x25]
0x55a00	a10240f9	ldr	x1, [x21]
0x55a04	00013fd6	blr	x8
0x55a08	00ffff34	cbz	w0, 0x559e8 <_WeChatMain+0x3c17c>
0x55a0c	210340f9	ldr	x1, [x25]
0x55a10	a80240f9	ldr	x8, [x21]
0x55a14	280300f9	str	x8, [x25]
0x55a18	a10200f9	str	x1, [x21]
0x55a1c	df0a00f1	cmp	x22, #0x2
0x55a20	4bfeff54	b.lt	0x559e8 <_WeChatMain+0x3c17c>
0x55a24	e81340f9	ldr	x8, [sp, #0x20]
0x55a28	1f4100f1	cmp	x8, #0x10
0x55a2c	81000054	b.ne	0x55a3c <_WeChatMain+0x3c1d0>
0x55a30	fb0314aa	mov	x27, x20
0x55a34	37008052	mov	w23, #0x1               ; =1
0x55a38	0b000014	b	0x55a64 <_WeChatMain+0x3c1f8>
0x55a3c	680240f9	ldr	x8, [x19]
0x55a40	080140f9	ldr	x8, [x8]
0x55a44	a08640a9	ldp	x0, x1, [x21, #0x8]
0x55a48	00013fd6	blr	x8
0x55a4c	1f000071	cmp	w0, #0x0
0x55a50	e80340f9	ldr	x8, [sp]
0x55a54	1b11949a	csel	x27, x8, x20, ne
0x55a58	28008052	mov	w8, #0x1                ; =1
0x55a5c	1705889a	cinc	x23, x8, ne
0x55a60	a10240f9	ldr	x1, [x21]
0x55a64	680240f9	ldr	x8, [x19]
0x55a68	080140f9	ldr	x8, [x8]
0x55a6c	600340f9	ldr	x0, [x27]
0x55a70	00013fd6	blr	x8
0x55a74	a0fb0737	tbnz	w0, #0x0, 0x559e8 <_WeChatMain+0x3c17c>
0x55a78	f90f00f9	str	x25, [sp, #0x18]
0x55a7c	b80240f9	ldr	x24, [x21]
0x55a80	fc0315aa	mov	x28, x21
0x55a84	08000014	b	0x55aa4 <_WeChatMain+0x3c238>
0x55a88	680240f9	ldr	x8, [x19]
0x55a8c	080140f9	ldr	x8, [x8]
0x55a90	600340f9	ldr	x0, [x27]
0x55a94	e10318aa	mov	x1, x24
0x55a98	00013fd6	blr	x8
0x55a9c	f70314aa	mov	x23, x20
0x55aa0	e0f9ff35	cbnz	w0, 0x559dc <_WeChatMain+0x3c170>
0x55aa4	e8031caa	mov	x8, x28
0x55aa8	fc031baa	mov	x28, x27
0x55aac	690340f9	ldr	x9, [x27]
0x55ab0	090100f9	str	x9, [x8]
0x55ab4	5f0317eb	cmp	x26, x23
0x55ab8	2bf9ff54	b.lt	0x559dc <_WeChatMain+0x3c170>
0x55abc	e8fa7fd3	lsl	x8, x23, #1
0x55ac0	34008052	mov	w20, #0x1               ; =1
0x55ac4	f4fa7fb3	bfi	x20, x23, #1, #63
0x55ac8	bb0e148b	add	x27, x21, x20, lsl #3
0x55acc	17090091	add	x23, x8, #0x2
0x55ad0	ff0216eb	cmp	x23, x22
0x55ad4	aafdff54	b.ge	0x55a88 <_WeChatMain+0x3c21c>
0x55ad8	680240f9	ldr	x8, [x19]
0x55adc	080140f9	ldr	x8, [x8]
0x55ae0	600340f9	ldr	x0, [x27]
0x55ae4	f90315aa	mov	x25, x21
0x55ae8	f50318aa	mov	x21, x24
0x55aec	f8031aaa	mov	x24, x26
0x55af0	fa031baa	mov	x26, x27
0x55af4	418f40f8	ldr	x1, [x26, #0x8]!
0x55af8	00013fd6	blr	x8
0x55afc	1f000071	cmp	w0, #0x0
0x55b00	5b139b9a	csel	x27, x26, x27, ne
0x55b04	fa0318aa	mov	x26, x24
0x55b08	f80315aa	mov	x24, x21
0x55b0c	f50319aa	mov	x21, x25
0x55b10	f412949a	csel	x20, x23, x20, ne
0x55b14	ddffff17	b	0x55a88 <_WeChatMain+0x3c21c>
0x55b18	df0a00f1	cmp	x22, #0x2
0x55b1c	4a020054	b.ge	0x55b64 <_WeChatMain+0x3c2f8>
0x55b20	fc0319aa	mov	x28, x25
0x55b24	e0031caa	mov	x0, x28
0x55b28	fd7b48a9	ldp	x29, x30, [sp, #0x80]
0x55b2c	f44f47a9	ldp	x20, x19, [sp, #0x70]
0x55b30	f65746a9	ldp	x22, x21, [sp, #0x60]
0x55b34	f85f45a9	ldp	x24, x23, [sp, #0x50]
0x55b38	fa6744a9	ldp	x26, x25, [sp, #0x40]
0x55b3c	fc6f43a9	ldp	x28, x27, [sp, #0x30]
0x55b40	ff430291	add	sp, sp, #0x90
0x55b44	c0035fd6	ret
0x55b48	e81340f9	ldr	x8, [sp, #0x20]
0x55b4c	080300f9	str	x8, [x24]
0x55b50	fb1700f9	str	x27, [sp, #0x28]
0x55b54	c80600d1	sub	x8, x22, #0x1
0x55b58	df0a00f1	cmp	x22, #0x2
0x55b5c	f60308aa	mov	x22, x8
0x55b60	0dfeff54	b.le	0x55b20 <_WeChatMain+0x3c2b4>
0x55b64	080080d2	mov	x8, #0x0                ; =0
0x55b68	a90240f9	ldr	x9, [x21]
0x55b6c	e91300f9	str	x9, [sp, #0x20]
0x55b70	c90a00d1	sub	x9, x22, #0x2
0x55b74	3afd41d3	lsr	x26, x9, #1
0x55b78	fb0315aa	mov	x27, x21
0x55b7c	0e000014	b	0x55bb4 <_WeChatMain+0x3c348>
0x55b80	680240f9	ldr	x8, [x19]
0x55b84	080140f9	ldr	x8, [x8]
0x55b88	810f41f8	ldr	x1, [x28, #0x10]!
0x55b8c	80835ff8	ldur	x0, [x28, #-0x8]
0x55b90	00013fd6	blr	x8
0x55b94	1f000071	cmp	w0, #0x0
0x55b98	9813989a	csel	x24, x28, x24, ne
0x55b9c	e812949a	csel	x8, x23, x20, ne
0x55ba0	090340f9	ldr	x9, [x24]
0x55ba4	690300f9	str	x9, [x27]
0x55ba8	fb0318aa	mov	x27, x24
0x55bac	1f011aeb	cmp	x8, x26
0x55bb0	6c010054	b.gt	0x55bdc <_WeChatMain+0x3c370>
0x55bb4	7c0f088b	add	x28, x27, x8, lsl #3
0x55bb8	98230091	add	x24, x28, #0x8
0x55bbc	09f97fd3	lsl	x9, x8, #1
0x55bc0	34008052	mov	w20, #0x1               ; =1
0x55bc4	14f97fb3	bfi	x20, x8, #1, #63
0x55bc8	37090091	add	x23, x9, #0x2
0x55bcc	ff0216eb	cmp	x23, x22
0x55bd0	8bfdff54	b.lt	0x55b80 <_WeChatMain+0x3c314>
0x55bd4	e80314aa	mov	x8, x20
0x55bd8	f2ffff17	b	0x55ba0 <_WeChatMain+0x3c334>
0x55bdc	fb1740f9	ldr	x27, [sp, #0x28]
0x55be0	7b2300d1	sub	x27, x27, #0x8
0x55be4	1f031beb	cmp	x24, x27
0x55be8	00fbff54	b.eq	0x55b48 <_WeChatMain+0x3c2dc>
0x55bec	680340f9	ldr	x8, [x27]
0x55bf0	080300f9	str	x8, [x24]
0x55bf4	e81340f9	ldr	x8, [sp, #0x20]
0x55bf8	680300f9	str	x8, [x27]
0x55bfc	080315cb	sub	x8, x24, x21
0x55c00	08210091	add	x8, x8, #0x8
0x55c04	08fd4393	asr	x8, x8, #3
0x55c08	080900f1	subs	x8, x8, #0x2
0x55c0c	2bfaff54	b.lt	0x55b50 <_WeChatMain+0x3c2e4>
0x55c10	1afd41d3	lsr	x26, x8, #1
0x55c14	b40e1a8b	add	x20, x21, x26, lsl #3
0x55c18	680240f9	ldr	x8, [x19]
0x55c1c	080140f9	ldr	x8, [x8]
0x55c20	800240f9	ldr	x0, [x20]
0x55c24	010340f9	ldr	x1, [x24]
0x55c28	00013fd6	blr	x8
0x55c2c	20f9ff34	cbz	w0, 0x55b50 <_WeChatMain+0x3c2e4>
0x55c30	170340f9	ldr	x23, [x24]
0x55c34	e80318aa	mov	x8, x24
0x55c38	f80314aa	mov	x24, x20
0x55c3c	890240f9	ldr	x9, [x20]
0x55c40	090100f9	str	x9, [x8]
0x55c44	5a0100b4	cbz	x26, 0x55c6c <_WeChatMain+0x3c400>
0x55c48	480700d1	sub	x8, x26, #0x1
0x55c4c	1afd41d3	lsr	x26, x8, #1
0x55c50	b40e1a8b	add	x20, x21, x26, lsl #3
0x55c54	680240f9	ldr	x8, [x19]
0x55c58	080140f9	ldr	x8, [x8]
0x55c5c	800240f9	ldr	x0, [x20]
0x55c60	e10317aa	mov	x1, x23
0x55c64	00013fd6	blr	x8
0x55c68	60fe0737	tbnz	w0, #0x0, 0x55c34 <_WeChatMain+0x3c3c8>
0x55c6c	170300f9	str	x23, [x24]
0x55c70	b8ffff17	b	0x55b50 <_WeChatMain+0x3c2e4>
0x55c74	490800f1	subs	x9, x2, #0x2
0x55c78	8b090054	b.lt	0x55da8 <_WeChatMain+0x3c53c>
0x55c7c	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x55c80	fa6701a9	stp	x26, x25, [sp, #0x10]
0x55c84	f85f02a9	stp	x24, x23, [sp, #0x20]
0x55c88	f65703a9	stp	x22, x21, [sp, #0x30]
0x55c8c	f44f04a9	stp	x20, x19, [sp, #0x40]
0x55c90	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x55c94	fd430191	add	x29, sp, #0x50
0x55c98	f30303aa	mov	x19, x3
0x55c9c	f60300aa	mov	x22, x0
0x55ca0	680000cb	sub	x8, x3, x0
0x55ca4	38fd41d3	lsr	x24, x9, #1
0x55ca8	1f0f88eb	cmp	x24, x8, asr #3
0x55cac	2b070054	b.lt	0x55d90 <_WeChatMain+0x3c524>
0x55cb0	f40302aa	mov	x20, x2
0x55cb4	f50301aa	mov	x21, x1
0x55cb8	08fd4293	asr	x8, x8, #2
0x55cbc	1a050091	add	x26, x8, #0x1
0x55cc0	d90e1a8b	add	x25, x22, x26, lsl #3
0x55cc4	17090091	add	x23, x8, #0x2
0x55cc8	ff0202eb	cmp	x23, x2
0x55ccc	4a010054	b.ge	0x55cf4 <_WeChatMain+0x3c488>
0x55cd0	a80240f9	ldr	x8, [x21]
0x55cd4	080140f9	ldr	x8, [x8]
0x55cd8	200340f9	ldr	x0, [x25]
0x55cdc	fb0319aa	mov	x27, x25
0x55ce0	618f40f8	ldr	x1, [x27, #0x8]!
0x55ce4	00013fd6	blr	x8
0x55ce8	1f000071	cmp	w0, #0x0
0x55cec	7913999a	csel	x25, x27, x25, ne
0x55cf0	fa129a9a	csel	x26, x23, x26, ne
0x55cf4	a80240f9	ldr	x8, [x21]
0x55cf8	080140f9	ldr	x8, [x8]
0x55cfc	200340f9	ldr	x0, [x25]
0x55d00	610240f9	ldr	x1, [x19]
0x55d04	00013fd6	blr	x8
0x55d08	40040037	tbnz	w0, #0x0, 0x55d90 <_WeChatMain+0x3c524>
0x55d0c	770240f9	ldr	x23, [x19]
0x55d10	08000014	b	0x55d30 <_WeChatMain+0x3c4c4>
0x55d14	a80240f9	ldr	x8, [x21]
0x55d18	080140f9	ldr	x8, [x8]
0x55d1c	200340f9	ldr	x0, [x25]
0x55d20	e10317aa	mov	x1, x23
0x55d24	00013fd6	blr	x8
0x55d28	fa031baa	mov	x26, x27
0x55d2c	00030035	cbnz	w0, 0x55d8c <_WeChatMain+0x3c520>
0x55d30	e80313aa	mov	x8, x19
0x55d34	f30319aa	mov	x19, x25
0x55d38	290340f9	ldr	x9, [x25]
0x55d3c	090100f9	str	x9, [x8]
0x55d40	1f031aeb	cmp	x24, x26
0x55d44	4b020054	b.lt	0x55d8c <_WeChatMain+0x3c520>
0x55d48	48fb7fd3	lsl	x8, x26, #1
0x55d4c	3b008052	mov	w27, #0x1               ; =1
0x55d50	5bfb7fb3	bfi	x27, x26, #1, #63
0x55d54	d90e1b8b	add	x25, x22, x27, lsl #3
0x55d58	1a090091	add	x26, x8, #0x2
0x55d5c	5f0314eb	cmp	x26, x20
0x55d60	aafdff54	b.ge	0x55d14 <_WeChatMain+0x3c4a8>
0x55d64	a80240f9	ldr	x8, [x21]
0x55d68	080140f9	ldr	x8, [x8]
0x55d6c	200340f9	ldr	x0, [x25]
0x55d70	fc0319aa	mov	x28, x25
0x55d74	818f40f8	ldr	x1, [x28, #0x8]!
0x55d78	00013fd6	blr	x8
0x55d7c	1f000071	cmp	w0, #0x0
0x55d80	9913999a	csel	x25, x28, x25, ne
0x55d84	5b139b9a	csel	x27, x26, x27, ne
0x55d88	e3ffff17	b	0x55d14 <_WeChatMain+0x3c4a8>
0x55d8c	770200f9	str	x23, [x19]
0x55d90	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x55d94	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x55d98	f65743a9	ldp	x22, x21, [sp, #0x30]
0x55d9c	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x55da0	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x55da4	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x55da8	c0035fd6	ret
0x55dac	ff0306d1	sub	sp, sp, #0x180
0x55db0	fc6f15a9	stp	x28, x27, [sp, #0x150]
0x55db4	f44f16a9	stp	x20, x19, [sp, #0x160]
0x55db8	fd7b17a9	stp	x29, x30, [sp, #0x170]
0x55dbc	fdc30591	add	x29, sp, #0x170
0x55dc0	bfff3ca9	stp	xzr, xzr, [x29, #-0x38]
0x55dc4	bf831df8	stur	xzr, [x29, #-0x28]
0x55dc8	ff7f0039	strb	wzr, [sp, #0x1f]
0x55dcc	ff230039	strb	wzr, [sp, #0x8]
0x55dd0	e0230091	add	x0, sp, #0x8
0x55dd4	a1e300d1	sub	x1, x29, #0x38
0x55dd8	29f5ff97	bl	0x5327c <_WeChatMain+0x39a10>
0x55ddc	e87fc039	ldrsb	w8, [sp, #0x1f]
0x55de0	a800f836	tbz	w8, #0x1f, 0x55df4 <_WeChatMain+0x3c588>
0x55de4	e00740f9	ldr	x0, [sp, #0x8]
0x55de8	e80f40f9	ldr	x8, [sp, #0x18]
0x55dec	01f94092	and	x1, x8, #0x7fffffffffffffff
0x55df0	87a8c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x55df4	f40f05b0	adrp	x20, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x55df8	886a6739	ldrb	w8, [x20, #0x9da]
0x55dfc	68030037	tbnz	w8, #0x0, 0x55e68 <_WeChatMain+0x3c5fc>
0x55e00	080080d2	mov	x8, #0x0                ; =0
0x55e04	e9e702b2	mov	x9, #-0x3333333333333334 ; =-3689348814741910324
0x55e08	a99999f2	movk	x9, #0xcccd
0x55e0c	6a028092	mov	x10, #-0x14             ; =-20
0x55e10	ab2104b0	adrp	x11, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x55e14	6b412691	add	x11, x11, #0x990
0x55e18	ec0f05b0	adrp	x12, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x55e1c	8c992591	add	x12, x12, #0x966
0x55e20	0d7dc99b	umulh	x13, x8, x9
0x55e24	adfd44d3	lsr	x13, x13, #4
0x55e28	6e01088b	add	x14, x11, x8
0x55e2c	ad390a9b	madd	x13, x13, x10, x14
0x55e30	ce550491	add	x14, x14, #0x115
0x55e34	ad050491	add	x13, x13, #0x101
0x55e38	c00140bd	ldr	s0, [x14]
0x55e3c	00a4082f	ushll.8h	v0, v0, #0x0
0x55e40	a10140bd	ldr	s1, [x13]
0x55e44	21a4082f	ushll.8h	v1, v1, #0x0
0x55e48	201c202e	eor.8b	v0, v1, v0
0x55e4c	0018000e	uzp1.8b	v0, v0, v0
0x55e50	806928bc	str	s0, [x12, x8]
0x55e54	08110091	add	x8, x8, #0x4
0x55e58	1fd101f1	cmp	x8, #0x74
0x55e5c	21feff54	b.ne	0x55e20 <_WeChatMain+0x3c5b4>
0x55e60	28008052	mov	w8, #0x1                ; =1
0x55e64	886a2739	strb	w8, [x20, #0x9da]
0x55e68	f30f05b0	adrp	x19, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x55e6c	739a2591	add	x19, x19, #0x966
0x55e70	e00313aa	mov	x0, x19
0x55e74	810e8052	mov	w1, #0x74               ; =116
0x55e78	5d98ff97	bl	0x3bfec <_WeChatMain+0x22780>
0x55e7c	1f040071	cmp	w0, #0x1
0x55e80	ab050054	b.lt	0x55f34 <_WeChatMain+0x3c6c8>
0x55e84	886a6739	ldrb	w8, [x20, #0x9da]
0x55e88	28030037	tbnz	w8, #0x0, 0x55eec <_WeChatMain+0x3c680>
0x55e8c	080080d2	mov	x8, #0x0                ; =0
0x55e90	e9e702b2	mov	x9, #-0x3333333333333334 ; =-3689348814741910324
0x55e94	a99999f2	movk	x9, #0xcccd
0x55e98	6a028092	mov	x10, #-0x14             ; =-20
0x55e9c	ab2104b0	adrp	x11, 0x848a000 <_wxam_enc_uninit_10+0x848a000>
0x55ea0	6b412691	add	x11, x11, #0x990
0x55ea4	0c7dc99b	umulh	x12, x8, x9
0x55ea8	8cfd44d3	lsr	x12, x12, #4
0x55eac	6d01088b	add	x13, x11, x8
0x55eb0	8c350a9b	madd	x12, x12, x10, x13
0x55eb4	ad550491	add	x13, x13, #0x115
0x55eb8	8c050491	add	x12, x12, #0x101
0x55ebc	a00140bd	ldr	s0, [x13]
0x55ec0	00a4082f	ushll.8h	v0, v0, #0x0
0x55ec4	810140bd	ldr	s1, [x12]
0x55ec8	21a4082f	ushll.8h	v1, v1, #0x0
0x55ecc	201c202e	eor.8b	v0, v1, v0
0x55ed0	0018000e	uzp1.8b	v0, v0, v0
0x55ed4	606a28bc	str	s0, [x19, x8]
0x55ed8	08110091	add	x8, x8, #0x4
0x55edc	1fd101f1	cmp	x8, #0x74
0x55ee0	21feff54	b.ne	0x55ea4 <_WeChatMain+0x3c638>
0x55ee4	28008052	mov	w8, #0x1                ; =1
0x55ee8	886a2739	strb	w8, [x20, #0x9da]
0x55eec	e10f05b0	adrp	x1, 0xa252000 <_wxam_enc_uninit_10+0xa252000>
0x55ef0	21982591	add	x1, x1, #0x966
0x55ef4	f3230091	add	x19, sp, #0x8
0x55ef8	e0230091	add	x0, sp, #0x8
0x55efc	82388052	mov	w2, #0x1c4              ; =452
0x55f00	03008012	mov	w3, #-0x1               ; =-1
0x55f04	4b98ff97	bl	0x3c030 <_WeChatMain+0x227c4>
0x55f08	a8f35d38	ldurb	w8, [x29, #-0x21]
0x55f0c	091d0013	sxtb	w9, w8
0x55f10	aaaf7ca9	ldp	x10, x11, [x29, #-0x38]
0x55f14	3f010071	cmp	w9, #0x0
0x55f18	a9e300d1	sub	x9, x29, #0x38
0x55f1c	41b1899a	csel	x1, x10, x9, lt
0x55f20	62b1889a	csel	x2, x11, x8, lt
0x55f24	60420091	add	x0, x19, #0x10
0x55f28	a912ff97	bl	0x1a9cc <_WeChatMain+0x1160>
0x55f2c	e0230091	add	x0, sp, #0x8
0x55f30	749dff97	bl	0x3d500 <_WeChatMain+0x23c94>
0x55f34	a8f3dd38	ldursb	w8, [x29, #-0x21]
0x55f38	a800f836	tbz	w8, #0x1f, 0x55f4c <_WeChatMain+0x3c6e0>
0x55f3c	a0835cf8	ldur	x0, [x29, #-0x38]
0x55f40	a8835df8	ldur	x8, [x29, #-0x28]
0x55f44	01f94092	and	x1, x8, #0x7fffffffffffffff
0x55f48	31a8c395	bl	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x55f4c	fd7b57a9	ldp	x29, x30, [sp, #0x170]
0x55f50	f44f56a9	ldp	x20, x19, [sp, #0x160]
0x55f54	fc6f55a9	ldp	x28, x27, [sp, #0x150]
0x55f58	ff030691	add	sp, sp, #0x180
0x55f5c	c0035fd6	ret
0x55f60	fc6fbaa9	stp	x28, x27, [sp, #-0x60]!
0x55f64	fa6701a9	stp	x26, x25, [sp, #0x10]
0x55f68	f85f02a9	stp	x24, x23, [sp, #0x20]
0x55f6c	f65703a9	stp	x22, x21, [sp, #0x30]
0x55f70	f44f04a9	stp	x20, x19, [sp, #0x40]
0x55f74	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x55f78	fd430191	add	x29, sp, #0x50
0x55f7c	f50303aa	mov	x21, x3
0x55f80	f30300aa	mov	x19, x0
0x55f84	365c40a9	ldp	x22, x23, [x1]
0x55f88	970200b4	cbz	x23, 0x55fd8 <_WeChatMain+0x3c76c>
0x55f8c	180080d2	mov	x24, #0x0               ; =0
0x55f90	68108052	mov	w8, #0x83               ; =131
0x55f94	e90317aa	mov	x9, x23
0x55f98	ea0316aa	mov	x10, x22
0x55f9c	4b158038	ldrsb	x11, [x10], #0x1
0x55fa0	182f089b	madd	x24, x24, x8, x11
0x55fa4	290500f1	subs	x9, x9, #0x1
0x55fa8	a1ffff54	b.ne	0x55f9c <_WeChatMain+0x3c730>
0x55fac	790640f9	ldr	x25, [x19, #0x8]
0x55fb0	b90100b4	cbz	x25, 0x55fe4 <_WeChatMain+0x3c778>
0x55fb4	2003679e	fmov	d0, x25
0x55fb8	0058200e	cnt.8b	v0, v0
0x55fbc	0038302e	uaddlv.8b	h0, v0
0x55fc0	1b00261e	fmov	w27, s0
0x55fc4	7f0700f1	cmp	x27, #0x1
0x55fc8	28010054	b.hi	0x55fec <_WeChatMain+0x3c780>
0x55fcc	280700d1	sub	x8, x25, #0x1
0x55fd0	1a01188a	and	x26, x8, x24
0x55fd4	0b000014	b	0x56000 <_WeChatMain+0x3c794>
0x55fd8	180080d2	mov	x24, #0x0               ; =0
0x55fdc	790640f9	ldr	x25, [x19, #0x8]
0x55fe0	b9feffb5	cbnz	x25, 0x55fb4 <_WeChatMain+0x3c748>
0x55fe4	faf301b2	mov	x26, #-0x5555555555555556 ; =-6148914691236517206
0x55fe8	25000014	b	0x5607c <_WeChatMain+0x3c810>
0x55fec	fa0318aa	mov	x26, x24
0x55ff0	1f0319eb	cmp	x24, x25
0x55ff4	63000054	b.lo	0x56000 <_WeChatMain+0x3c794>
0x55ff8	080bd99a	udiv	x8, x24, x25
0x55ffc	1ae1199b	msub	x26, x8, x25, x24
0x56000	680240f9	ldr	x8, [x19]
0x56004	08797af8	ldr	x8, [x8, x26, lsl #3]
0x56008	a80300b4	cbz	x8, 0x5607c <_WeChatMain+0x3c810>
0x5600c	140140f9	ldr	x20, [x8]
0x56010	740300b4	cbz	x20, 0x5607c <_WeChatMain+0x3c810>
0x56014	3c0700d1	sub	x28, x25, #0x1
0x56018	06000014	b	0x56030 <_WeChatMain+0x3c7c4>
0x5601c	08011c8a	and	x8, x8, x28
0x56020	1f011aeb	cmp	x8, x26
0x56024	c1020054	b.ne	0x5607c <_WeChatMain+0x3c810>
0x56028	940240f9	ldr	x20, [x20]
0x5602c	940200b4	cbz	x20, 0x5607c <_WeChatMain+0x3c810>
0x56030	880640f9	ldr	x8, [x20, #0x8]
0x56034	1f0118eb	cmp	x8, x24
0x56038	41010054	b.ne	0x56060 <_WeChatMain+0x3c7f4>
0x5603c	880e40f9	ldr	x8, [x20, #0x18]
0x56040	1f0117eb	cmp	x8, x23
0x56044	21ffff54	b.ne	0x56028 <_WeChatMain+0x3c7bc>
0x56048	800a40f9	ldr	x0, [x20, #0x10]
0x5604c	e10316aa	mov	x1, x22
0x56050	e20317aa	mov	x2, x23
0x56054	8aabc395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x56058	80feff35	cbnz	w0, 0x56028 <_WeChatMain+0x3c7bc>
0x5605c	83000014	b	0x56268 <_WeChatMain+0x3c9fc>
0x56060	7f0700f1	cmp	x27, #0x1
0x56064	c9fdff54	b.ls	0x5601c <_WeChatMain+0x3c7b0>
0x56068	1f0119eb	cmp	x8, x25
0x5606c	a3fdff54	b.lo	0x56020 <_WeChatMain+0x3c7b4>
0x56070	0909d99a	udiv	x9, x8, x25
0x56074	28a1199b	msub	x8, x9, x25, x8
0x56078	eaffff17	b	0x56020 <_WeChatMain+0x3c7b4>
0x5607c	00058052	mov	w0, #0x28               ; =40
0x56080	eca7c395	bl	0x7140030 <_wxam_enc_uninit_10+0x7140030>
0x56084	f40300aa	mov	x20, x0
0x56088	1f6000a9	stp	xzr, x24, [x0]
0x5608c	a80240f9	ldr	x8, [x21]
0x56090	0001c03d	ldr	q0, [x8]
0x56094	0004803d	str	q0, [x0, #0x10]
0x56098	1f1000f9	str	xzr, [x0, #0x20]
0x5609c	680e40f9	ldr	x8, [x19, #0x18]
0x560a0	08050091	add	x8, x8, #0x1
0x560a4	0001239e	ucvtf	s0, x8
0x560a8	612240bd	ldr	s1, [x19, #0x20]
0x560ac	b90000b4	cbz	x25, 0x560c0 <_WeChatMain+0x3c854>
0x560b0	2203239e	ucvtf	s2, x25
0x560b4	2208221e	fmul	s2, s1, s2
0x560b8	4020201e	fcmp	s2, s0
0x560bc	a5080054	b.pl	0x561d0 <_WeChatMain+0x3c964>
0x560c0	28fb7fd3	lsl	x8, x25, #1
0x560c4	29008052	mov	w9, #0x1                ; =1
0x560c8	2a0700d1	sub	x10, x25, #0x1
0x560cc	3f030aea	tst	x25, x10
0x560d0	ea079f1a	cset	w10, ne
0x560d4	3f0f00f1	cmp	x25, #0x3
0x560d8	29318a9a	csel	x9, x9, x10, lo
0x560dc	280108aa	orr	x8, x9, x8
0x560e0	0018211e	fdiv	s0, s0, s1
0x560e4	0900299e	fcvtpu	x9, s0
0x560e8	1f0109eb	cmp	x8, x9
0x560ec	0181899a	csel	x1, x8, x9, hi
0x560f0	280400f1	subs	x8, x1, #0x1
0x560f4	61000054	b.ne	0x56100 <_WeChatMain+0x3c894>
0x560f8	41008052	mov	w1, #0x2                ; =2
0x560fc	07000014	b	0x56118 <_WeChatMain+0x3c8ac>
0x56100	3f0008ea	tst	x1, x8
0x56104	a0000054	b.eq	0x56118 <_WeChatMain+0x3c8ac>
0x56108	e00301aa	mov	x0, x1
0x5610c	a7a5c395	bl	0x713f7a8 <_wxam_enc_uninit_10+0x713f7a8>
0x56110	e10300aa	mov	x1, x0
0x56114	790640f9	ldr	x25, [x19, #0x8]
0x56118	3f0019eb	cmp	x1, x25
0x5611c	89000054	b.ls	0x5612c <_WeChatMain+0x3c8c0>
0x56120	e00313aa	mov	x0, x19
0x56124	d051ff97	bl	0x2a864 <_WeChatMain+0x10ff8>
0x56128	1e000014	b	0x561a0 <_WeChatMain+0x3c934>
0x5612c	a2030054	b.hs	0x561a0 <_WeChatMain+0x3c934>
0x56130	680e40f9	ldr	x8, [x19, #0x18]
0x56134	0001239e	ucvtf	s0, x8
0x56138	612240bd	ldr	s1, [x19, #0x20]
0x5613c	0018211e	fdiv	s0, s0, s1
0x56140	0000299e	fcvtpu	x0, s0
0x56144	3f0f00f1	cmp	x25, #0x3
0x56148	e3010054	b.lo	0x56184 <_WeChatMain+0x3c918>
0x5614c	2003679e	fmov	d0, x25
0x56150	0058200e	cnt.8b	v0, v0
0x56154	0038302e	uaddlv.8b	h0, v0
0x56158	0800261e	fmov	w8, s0
0x5615c	1f0500f1	cmp	x8, #0x1
0x56160	28010054	b.hi	0x56184 <_WeChatMain+0x3c918>
0x56164	080400d1	sub	x8, x0, #0x1
0x56168	0811c0da	clz	x8, x8
0x5616c	e80308cb	neg	x8, x8
0x56170	29008052	mov	w9, #0x1                ; =1
0x56174	2821c89a	lsl	x8, x9, x8
0x56178	1f0800f1	cmp	x0, #0x2
0x5617c	0030889a	csel	x0, x0, x8, lo
0x56180	04000014	b	0x56190 <_WeChatMain+0x3c924>
0x56184	f50301aa	mov	x21, x1
0x56188	88a5c395	bl	0x713f7a8 <_wxam_enc_uninit_10+0x713f7a8>
0x5618c	e10315aa	mov	x1, x21
0x56190	3f0000eb	cmp	x1, x0
0x56194	2180809a	csel	x1, x1, x0, hi
0x56198	3f0019eb	cmp	x1, x25
0x5619c	23fcff54	b.lo	0x56120 <_WeChatMain+0x3c8b4>
0x561a0	790640f9	ldr	x25, [x19, #0x8]
0x561a4	280700d1	sub	x8, x25, #0x1
0x561a8	3f0308ea	tst	x25, x8
0x561ac	61000054	b.ne	0x561b8 <_WeChatMain+0x3c94c>
0x561b0	1a01188a	and	x26, x8, x24
0x561b4	07000014	b	0x561d0 <_WeChatMain+0x3c964>
0x561b8	1f0319eb	cmp	x24, x25
0x561bc	62000054	b.hs	0x561c8 <_WeChatMain+0x3c95c>
0x561c0	fa0318aa	mov	x26, x24
0x561c4	03000014	b	0x561d0 <_WeChatMain+0x3c964>
0x561c8	080bd99a	udiv	x8, x24, x25
0x561cc	1ae1199b	msub	x26, x8, x25, x24
0x561d0	690240f9	ldr	x9, [x19]
0x561d4	28797af8	ldr	x8, [x9, x26, lsl #3]
0x561d8	880000b4	cbz	x8, 0x561e8 <_WeChatMain+0x3c97c>
0x561dc	090140f9	ldr	x9, [x8]
0x561e0	890200f9	str	x9, [x20]
0x561e4	14000014	b	0x56234 <_WeChatMain+0x3c9c8>
0x561e8	e80313aa	mov	x8, x19
0x561ec	0a0d41f8	ldr	x10, [x8, #0x10]!
0x561f0	8a0200f9	str	x10, [x20]
0x561f4	140100f9	str	x20, [x8]
0x561f8	28793af8	str	x8, [x9, x26, lsl #3]
0x561fc	880240f9	ldr	x8, [x20]
0x56200	c80100b4	cbz	x8, 0x56238 <_WeChatMain+0x3c9cc>
0x56204	080540f9	ldr	x8, [x8, #0x8]
0x56208	290700d1	sub	x9, x25, #0x1
0x5620c	3f0309ea	tst	x25, x9
0x56210	61000054	b.ne	0x5621c <_WeChatMain+0x3c9b0>
0x56214	0801098a	and	x8, x8, x9
0x56218	05000014	b	0x5622c <_WeChatMain+0x3c9c0>
0x5621c	1f0119eb	cmp	x8, x25
0x56220	63000054	b.lo	0x5622c <_WeChatMain+0x3c9c0>
0x56224	0909d99a	udiv	x9, x8, x25
0x56228	28a1199b	msub	x8, x9, x25, x8
0x5622c	690240f9	ldr	x9, [x19]
0x56230	280d088b	add	x8, x9, x8, lsl #3
0x56234	140100f9	str	x20, [x8]
0x56238	680e40f9	ldr	x8, [x19, #0x18]
0x5623c	08050091	add	x8, x8, #0x1
0x56240	680e00f9	str	x8, [x19, #0x18]
0x56244	21008052	mov	w1, #0x1                ; =1
0x56248	e00314aa	mov	x0, x20
0x5624c	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x56250	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x56254	f65743a9	ldp	x22, x21, [sp, #0x30]
0x56258	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x5625c	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x56260	fc6fc6a8	ldp	x28, x27, [sp], #0x60
0x56264	c0035fd6	ret
0x56268	010080d2	mov	x1, #0x0                ; =0
0x5626c	f7ffff17	b	0x56248 <_WeChatMain+0x3c9dc>
0x56270	fa67bba9	stp	x26, x25, [sp, #-0x50]!
0x56274	f85f01a9	stp	x24, x23, [sp, #0x10]
0x56278	f65702a9	stp	x22, x21, [sp, #0x20]
0x5627c	f44f03a9	stp	x20, x19, [sp, #0x30]
0x56280	fd7b04a9	stp	x29, x30, [sp, #0x40]
0x56284	fd030191	add	x29, sp, #0x40
0x56288	335040a9	ldp	x19, x20, [x1]
0x5628c	940100b4	cbz	x20, 0x562bc <_WeChatMain+0x3ca50>
0x56290	160080d2	mov	x22, #0x0               ; =0
0x56294	68108052	mov	w8, #0x83               ; =131
0x56298	e90314aa	mov	x9, x20
0x5629c	ea0313aa	mov	x10, x19
0x562a0	4b158038	ldrsb	x11, [x10], #0x1
0x562a4	d62e089b	madd	x22, x22, x8, x11
0x562a8	290500f1	subs	x9, x9, #0x1
0x562ac	a1ffff54	b.ne	0x562a0 <_WeChatMain+0x3ca34>
0x562b0	170440f9	ldr	x23, [x0, #0x8]
0x562b4	b70000b5	cbnz	x23, 0x562c8 <_WeChatMain+0x3ca5c>
0x562b8	31000014	b	0x5637c <_WeChatMain+0x3cb10>
0x562bc	160080d2	mov	x22, #0x0               ; =0
0x562c0	170440f9	ldr	x23, [x0, #0x8]
0x562c4	d70500b4	cbz	x23, 0x5637c <_WeChatMain+0x3cb10>
0x562c8	e002679e	fmov	d0, x23
0x562cc	0058200e	cnt.8b	v0, v0
0x562d0	0038302e	uaddlv.8b	h0, v0
0x562d4	1800261e	fmov	w24, s0
0x562d8	1f0700f1	cmp	x24, #0x1
0x562dc	88000054	b.hi	0x562ec <_WeChatMain+0x3ca80>
0x562e0	e80600d1	sub	x8, x23, #0x1
0x562e4	1901168a	and	x25, x8, x22
0x562e8	06000014	b	0x56300 <_WeChatMain+0x3ca94>
0x562ec	f90316aa	mov	x25, x22
0x562f0	df0217eb	cmp	x22, x23
0x562f4	63000054	b.lo	0x56300 <_WeChatMain+0x3ca94>
0x562f8	c80ad79a	udiv	x8, x22, x23
0x562fc	19d9179b	msub	x25, x8, x23, x22
0x56300	080040f9	ldr	x8, [x0]
0x56304	087979f8	ldr	x8, [x8, x25, lsl #3]
0x56308	a80300b4	cbz	x8, 0x5637c <_WeChatMain+0x3cb10>
0x5630c	150140f9	ldr	x21, [x8]
0x56310	950300b4	cbz	x21, 0x56380 <_WeChatMain+0x3cb14>
0x56314	fa0600d1	sub	x26, x23, #0x1
0x56318	06000014	b	0x56330 <_WeChatMain+0x3cac4>
0x5631c	08011a8a	and	x8, x8, x26
0x56320	1f0119eb	cmp	x8, x25
0x56324	c1020054	b.ne	0x5637c <_WeChatMain+0x3cb10>
0x56328	b50240f9	ldr	x21, [x21]
0x5632c	b50200b4	cbz	x21, 0x56380 <_WeChatMain+0x3cb14>
0x56330	a80640f9	ldr	x8, [x21, #0x8]
0x56334	1f0116eb	cmp	x8, x22
0x56338	41010054	b.ne	0x56360 <_WeChatMain+0x3caf4>
0x5633c	a80e40f9	ldr	x8, [x21, #0x18]
0x56340	1f0114eb	cmp	x8, x20
0x56344	21ffff54	b.ne	0x56328 <_WeChatMain+0x3cabc>
0x56348	a00a40f9	ldr	x0, [x21, #0x10]
0x5634c	e10313aa	mov	x1, x19
0x56350	e20314aa	mov	x2, x20
0x56354	caaac395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x56358	80feff35	cbnz	w0, 0x56328 <_WeChatMain+0x3cabc>
0x5635c	09000014	b	0x56380 <_WeChatMain+0x3cb14>
0x56360	1f0700f1	cmp	x24, #0x1
0x56364	c9fdff54	b.ls	0x5631c <_WeChatMain+0x3cab0>
0x56368	1f0117eb	cmp	x8, x23
0x5636c	a3fdff54	b.lo	0x56320 <_WeChatMain+0x3cab4>
0x56370	0909d79a	udiv	x9, x8, x23
0x56374	28a1179b	msub	x8, x9, x23, x8
0x56378	eaffff17	b	0x56320 <_WeChatMain+0x3cab4>
0x5637c	150080d2	mov	x21, #0x0               ; =0
0x56380	e00315aa	mov	x0, x21
0x56384	fd7b44a9	ldp	x29, x30, [sp, #0x40]
0x56388	f44f43a9	ldp	x20, x19, [sp, #0x30]
0x5638c	f65742a9	ldp	x22, x21, [sp, #0x20]
0x56390	f85f41a9	ldp	x24, x23, [sp, #0x10]
0x56394	fa67c5a8	ldp	x26, x25, [sp], #0x50
0x56398	c0035fd6	ret
0x5639c	ff8301d1	sub	sp, sp, #0x60
0x563a0	fa6701a9	stp	x26, x25, [sp, #0x10]
0x563a4	f85f02a9	stp	x24, x23, [sp, #0x20]
0x563a8	f65703a9	stp	x22, x21, [sp, #0x30]
0x563ac	f44f04a9	stp	x20, x19, [sp, #0x40]
0x563b0	fd7b05a9	stp	x29, x30, [sp, #0x50]
0x563b4	fd430191	add	x29, sp, #0x50
0x563b8	f40301aa	mov	x20, x1
0x563bc	f30300aa	mov	x19, x0
0x563c0	285c4039	ldrb	w8, [x1, #0x17]
0x563c4	091d0013	sxtb	w9, w8
0x563c8	2a2c40a9	ldp	x10, x11, [x1]
0x563cc	3f010071	cmp	w9, #0x0
0x563d0	41b1819a	csel	x1, x10, x1, lt
0x563d4	62b1889a	csel	x2, x11, x8, lt
0x563d8	e03f0091	add	x0, sp, #0xf
0x563dc	85f8ff97	bl	0x545f0 <_WeChatMain+0x3ad84>
0x563e0	750640f9	ldr	x21, [x19, #0x8]
0x563e4	150900b4	cbz	x21, 0x56504 <_WeChatMain+0x3cc98>
0x563e8	a002679e	fmov	d0, x21
0x563ec	0058200e	cnt.8b	v0, v0
0x563f0	0038302e	uaddlv.8b	h0, v0
0x563f4	1600261e	fmov	w22, s0
0x563f8	df0600f1	cmp	x22, #0x1
0x563fc	88000054	b.hi	0x5640c <_WeChatMain+0x3cba0>
0x56400	a80600d1	sub	x8, x21, #0x1
0x56404	1701008a	and	x23, x8, x0
0x56408	06000014	b	0x56420 <_WeChatMain+0x3cbb4>
0x5640c	f70300aa	mov	x23, x0
0x56410	1f0015eb	cmp	x0, x21
0x56414	63000054	b.lo	0x56420 <_WeChatMain+0x3cbb4>
0x56418	0808d59a	udiv	x8, x0, x21
0x5641c	1781159b	msub	x23, x8, x21, x0
0x56420	680240f9	ldr	x8, [x19]
0x56424	087977f8	ldr	x8, [x8, x23, lsl #3]
0x56428	e80600b4	cbz	x8, 0x56504 <_WeChatMain+0x3cc98>
0x5642c	130140f9	ldr	x19, [x8]
0x56430	d30600b4	cbz	x19, 0x56508 <_WeChatMain+0x3cc9c>
0x56434	b80600d1	sub	x24, x21, #0x1
0x56438	885e4039	ldrb	w8, [x20, #0x17]
0x5643c	091d0013	sxtb	w9, w8
0x56440	3f010071	cmp	w9, #0x0
0x56444	8a2640a9	ldp	x10, x9, [x20]
0x56448	39b1889a	csel	x25, x9, x8, lt
0x5644c	54b1949a	csel	x20, x10, x20, lt
0x56450	06000014	b	0x56468 <_WeChatMain+0x3cbfc>
0x56454	0801188a	and	x8, x8, x24
0x56458	1f0117eb	cmp	x8, x23
0x5645c	41050054	b.ne	0x56504 <_WeChatMain+0x3cc98>
0x56460	730240f9	ldr	x19, [x19]
0x56464	330500b4	cbz	x19, 0x56508 <_WeChatMain+0x3cc9c>
0x56468	680640f9	ldr	x8, [x19, #0x8]
0x5646c	1f0100eb	cmp	x8, x0
0x56470	a1020054	b.ne	0x564c4 <_WeChatMain+0x3cc58>
0x56474	689e4039	ldrb	w8, [x19, #0x27]
0x56478	091d0013	sxtb	w9, w8
0x5647c	620e40f9	ldr	x2, [x19, #0x18]
0x56480	3f010071	cmp	w9, #0x0
0x56484	49b0889a	csel	x9, x2, x8, lt
0x56488	3f0119eb	cmp	x9, x25
0x5648c	a1feff54	b.ne	0x56460 <_WeChatMain+0x3cbf4>
0x56490	69420091	add	x9, x19, #0x10
0x56494	68023837	tbnz	w8, #0x7, 0x564e0 <_WeChatMain+0x3cc74>
0x56498	88030034	cbz	w8, 0x56508 <_WeChatMain+0x3cc9c>
0x5649c	ea0314aa	mov	x10, x20
0x564a0	2b014039	ldrb	w11, [x9]
0x564a4	4c014039	ldrb	w12, [x10]
0x564a8	7f010c6b	cmp	w11, w12
0x564ac	a1fdff54	b.ne	0x56460 <_WeChatMain+0x3cbf4>
0x564b0	29050091	add	x9, x9, #0x1
0x564b4	4a050091	add	x10, x10, #0x1
0x564b8	080500f1	subs	x8, x8, #0x1
0x564bc	21ffff54	b.ne	0x564a0 <_WeChatMain+0x3cc34>
0x564c0	12000014	b	0x56508 <_WeChatMain+0x3cc9c>
0x564c4	df0600f1	cmp	x22, #0x1
0x564c8	69fcff54	b.ls	0x56454 <_WeChatMain+0x3cbe8>
0x564cc	1f0115eb	cmp	x8, x21
0x564d0	43fcff54	b.lo	0x56458 <_WeChatMain+0x3cbec>
0x564d4	0909d59a	udiv	x9, x8, x21
0x564d8	28a1159b	msub	x8, x9, x21, x8
0x564dc	dfffff17	b	0x56458 <_WeChatMain+0x3cbec>
0x564e0	280140f9	ldr	x8, [x9]
0x564e4	fa0300aa	mov	x26, x0
0x564e8	e00308aa	mov	x0, x8
0x564ec	e10314aa	mov	x1, x20
0x564f0	63aac395	bl	0x7140e7c <_wxam_enc_uninit_10+0x7140e7c>
0x564f4	e80300aa	mov	x8, x0
0x564f8	e0031aaa	mov	x0, x26
0x564fc	28fbff35	cbnz	w8, 0x56460 <_WeChatMain+0x3cbf4>
0x56500	02000014	b	0x56508 <_WeChatMain+0x3cc9c>
0x56504	130080d2	mov	x19, #0x0               ; =0
0x56508	e00313aa	mov	x0, x19
0x5650c	fd7b45a9	ldp	x29, x30, [sp, #0x50]
0x56510	f44f44a9	ldp	x20, x19, [sp, #0x40]
0x56514	f65743a9	ldp	x22, x21, [sp, #0x30]
0x56518	f85f42a9	ldp	x24, x23, [sp, #0x20]
0x5651c	fa6741a9	ldp	x26, x25, [sp, #0x10]
0x56520	ff830191	add	sp, sp, #0x60
0x56524	c0035fd6	ret
0x56528	f85fbca9	stp	x24, x23, [sp, #-0x40]!
0x5652c	f65701a9	stp	x22, x21, [sp, #0x10]
0x56530	f44f02a9	stp	x20, x19, [sp, #0x20]
0x56534	fd7b03a9	stp	x29, x30, [sp, #0x30]
0x56538	fdc30091	add	x29, sp, #0x30
0x5653c	f40302aa	mov	x20, x2
0x56540	f30301aa	mov	x19, x1
0x56544	f50300aa	mov	x21, x0
0x56548	00400091	add	x0, x0, #0x10
0x5654c	eaabc395	bl	0x71414f4 <_wxam_enc_uninit_10+0x71414f4>
0x56550	e00e0035	cbnz	w0, 0x5672c <_WeChatMain+0x3cec0>
0x56554	a83240f9	ldr	x8, [x21, #0x60]
0x56558	280f00b4	cbz	x8, 0x5673c <_WeChatMain+0x3ced0>
0x5655c	69fe60d3	lsr	x9, x19, #32
0x56560	6a727dd3	ubfiz	x10, x19, #3, #29
0x56564	4a210091	add	x10, x10, #0x8
0x56568	4a0109ca	eor	x10, x10, x9
0x5656c	2bad85d2	mov	x11, #0x2d69            ; =11625
0x56570	0b67bdf2	movk	x11, #0xeb38, lsl #16
0x56574	0b41ddf2	movk	x11, #0xea08, lsl #32
0x56578	ebbbf3f2	movk	x11, #0x9ddf, lsl #48
0x5657c	4a7d0b9b	mul	x10, x10, x11
0x56580	29bd4aca	eor	x9, x9, x10, lsr #47
0x56584	29010aca	eor	x9, x9, x10
0x56588	297d0b9b	mul	x9, x9, x11
0x5658c	29bd49ca	eor	x9, x9, x9, lsr #47
0x56590	297d0b9b	mul	x9, x9, x11
0x56594	0001679e	fmov	d0, x8
0x56598	0058200e	cnt.8b	v0, v0
0x5659c	0038302e	uaddlv.8b	h0, v0
0x565a0	0a00261e	fmov	w10, s0
0x565a4	5f0500f1	cmp	x10, #0x1
0x565a8	88000054	b.hi	0x565b8 <_WeChatMain+0x3cd4c>
0x565ac	0b0500d1	sub	x11, x8, #0x1
0x565b0	6b01098a	and	x11, x11, x9
0x565b4	06000014	b	0x565cc <_WeChatMain+0x3cd60>
0x565b8	eb0309aa	mov	x11, x9
0x565bc	3f0108eb	cmp	x9, x8
0x565c0	63000054	b.lo	0x565cc <_WeChatMain+0x3cd60>
0x565c4	2b09c89a	udiv	x11, x9, x8
0x565c8	6ba5089b	msub	x11, x11, x8, x9
0x565cc	ac2e40f9	ldr	x12, [x21, #0x58]
0x565d0	8c796bf8	ldr	x12, [x12, x11, lsl #3]
0x565d4	4c0b00b4	cbz	x12, 0x5673c <_WeChatMain+0x3ced0>
0x565d8	8c0140f9	ldr	x12, [x12]
0x565dc	0c0b00b4	cbz	x12, 0x5673c <_WeChatMain+0x3ced0>
0x565e0	0d0500d1	sub	x13, x8, #0x1
0x565e4	06000014	b	0x565fc <_WeChatMain+0x3cd90>
0x565e8	8e0940f9	ldr	x14, [x12, #0x10]
0x565ec	df0113eb	cmp	x14, x19
0x565f0	20020054	b.eq	0x56634 <_WeChatMain+0x3cdc8>
0x565f4	8c0140f9	ldr	x12, [x12]
0x565f8	2c0a00b4	cbz	x12, 0x5673c <_WeChatMain+0x3ced0>
0x565fc	8e0540f9	ldr	x14, [x12, #0x8]
0x56600	df0109eb	cmp	x14, x9
0x56604	20ffff54	b.eq	0x565e8 <_WeChatMain+0x3cd7c>
0x56608	5f0500f1	cmp	x10, #0x1
0x5660c	68000054	b.hi	0x56618 <_WeChatMain+0x3cdac>
0x56610	ce010d8a	and	x14, x14, x13
0x56614	05000014	b	0x56628 <_WeChatMain+0x3cdbc>
0x56618	df0108eb	cmp	x14, x8
0x5661c	63000054	b.lo	0x56628 <_WeChatMain+0x3cdbc>
0x56620	cf09c89a	udiv	x15, x14, x8
0x56624	eeb9089b	msub	x14, x15, x8, x14
0x56628	df010beb	cmp	x14, x11
0x5662c	40feff54	b.eq	0x565f4 <_WeChatMain+0x3cd88>
0x56630	43000014	b	0x5673c <_WeChatMain+0x3ced0>
0x56634	881140f9	ldr	x8, [x12, #0x20]
0x56638	891a40f9	ldr	x9, [x20, #0x30]
0x5663c	1f0109eb	cmp	x8, x9
0x56640	e1070054	b.ne	0x5673c <_WeChatMain+0x3ced0>
0x56644	a0420091	add	x0, x21, #0x10
0x56648	aeabc395	bl	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x5664c	282605d0	adrp	x8, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x56650	08a13091	add	x8, x8, #0xc28
0x56654	15c1bff8	ldapr	x21, [x8]
0x56658	bf0600f1	cmp	x21, #0x1
0x5665c	68020054	b.hi	0x566a8 <_WeChatMain+0x3ce3c>
0x56660	362605d0	adrp	x22, 0xa51c000 <_wxam_enc_uninit_10+0xa51c000>
0x56664	d6a23091	add	x22, x22, #0xc28
0x56668	e00316aa	mov	x0, x22
0x5666c	8693ff97	bl	0x3b484 <_WeChatMain+0x21c18>
0x56670	a0010034	cbz	w0, 0x566a4 <_WeChatMain+0x3ce38>
0x56674	df0a00f9	str	xzr, [x22, #0x10]
0x56678	f50316aa	mov	x21, x22
0x5667c	bf8e00f8	str	xzr, [x21, #0x8]!
0x56680	e00315aa	mov	x0, x21
0x56684	010080d2	mov	x1, #0x0                ; =0
0x56688	e7370194	bl	0xa4624 <_WeChatMain+0x8adb8>
0x5668c	e00316aa	mov	x0, x22
0x56690	e10315aa	mov	x1, x21
0x56694	020080d2	mov	x2, #0x0                ; =0
0x56698	e30316aa	mov	x3, x22
0x5669c	9e93ff97	bl	0x3b514 <_WeChatMain+0x21ca8>
0x566a0	02000014	b	0x566a8 <_WeChatMain+0x3ce3c>
0x566a4	d5c2bff8	ldapr	x21, [x22]
0x566a8	e00315aa	mov	x0, x21
0x566ac	5a370194	bl	0xa4414 <_WeChatMain+0x8aba8>
0x566b0	f60300aa	mov	x22, x0
0x566b4	e00315aa	mov	x0, x21
0x566b8	e10314aa	mov	x1, x20
0x566bc	97370194	bl	0xa4518 <_WeChatMain+0x8acac>
0x566c0	971640f9	ldr	x23, [x20, #0x28]
0x566c4	d70100b4	cbz	x23, 0x566fc <_WeChatMain+0x3ce90>
0x566c8	e00317aa	mov	x0, x23
0x566cc	f443ff97	bl	0x2769c <_WeChatMain+0xde30>
0x566d0	801640f9	ldr	x0, [x20, #0x28]
0x566d4	080440f9	ldr	x8, [x0, #0x8]
0x566d8	e10313aa	mov	x1, x19
0x566dc	00013fd6	blr	x8
0x566e0	08008012	mov	w8, #-0x1               ; =-1
0x566e4	e802e8b8	ldaddal	w8, w8, [x23]
0x566e8	1f050071	cmp	w8, #0x1
0x566ec	21010054	b.ne	0x56710 <_WeChatMain+0x3cea4>
0x566f0	e00317aa	mov	x0, x23
0x566f4	5175ff97	bl	0x33c38 <_WeChatMain+0x1a3cc>
0x566f8	06000014	b	0x56710 <_WeChatMain+0x3cea4>
0x566fc	08018052	mov	w8, #0x8                ; =8
0x56700	080140f9	ldr	x8, [x8]
0x56704	000080d2	mov	x0, #0x0                ; =0
0x56708	e10313aa	mov	x1, x19
0x5670c	00013fd6	blr	x8
0x56710	e00315aa	mov	x0, x21
0x56714	e10316aa	mov	x1, x22
0x56718	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x5671c	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x56720	f65741a9	ldp	x22, x21, [sp, #0x10]
0x56724	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x56728	7c370114	b	0xa4518 <_WeChatMain+0x8acac>
0x5672c	a0420091	add	x0, x21, #0x10
0x56730	554f0094	bl	0x6a484 <_WeChatMain+0x50c18>
0x56734	a83240f9	ldr	x8, [x21, #0x60]
0x56738	28f1ffb5	cbnz	x8, 0x5655c <_WeChatMain+0x3ccf0>
0x5673c	a0420091	add	x0, x21, #0x10
0x56740	fd7b43a9	ldp	x29, x30, [sp, #0x30]
0x56744	f44f42a9	ldp	x20, x19, [sp, #0x20]
0x56748	f65741a9	ldp	x22, x21, [sp, #0x10]
0x5674c	f85fc4a8	ldp	x24, x23, [sp], #0x40
0x56750	6cabc315	b	0x7141500 <_wxam_enc_uninit_10+0x7141500>
0x56754	032442a9	ldp	x3, x9, [x0, #0x20]
0x56758	080443a9	ldp	x8, x1, [x0, #0x30]
0x5675c	0805898b	add	x8, x8, x9, asr #1
0x56760	69000036	tbz	w9, #0x0, 0x5676c <_WeChatMain+0x3cf00>
0x56764	090140f9	ldr	x9, [x8]
0x56768	234963f8	ldr	x3, [x9, w3, uxtw]
0x5676c	02000191	add	x2, x0, #0x40
0x56770	e00308aa	mov	x0, x8
0x56774	60001fd6	br	x3
0x56778	c00400b4	cbz	x0, 0x56810 <_WeChatMain+0x3cfa4>
0x5677c	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x56780	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x56784	fd430091	add	x29, sp, #0x10
0x56788	f30300aa	mov	x19, x0
0x5678c	00a00191	add	x0, x0, #0x68
0x56790	6775ff97	bl	0x33d2c <_WeChatMain+0x1a4c0>
0x56794	602240f9	ldr	x0, [x19, #0x40]
0x56798	08745e92	and	x8, x0, #0xfffffffc00000000
0x5679c	34fd0490	adrp	x20, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x567a0	94023b91	add	x20, x20, #0xec0
0x567a4	890640f9	ldr	x9, [x20, #0x8]
0x567a8	1f0109eb	cmp	x8, x9
0x567ac	41000054	b.ne	0x567b4 <_WeChatMain+0x3cf48>
0x567b0	c4a4ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x567b4	7f2200f9	str	xzr, [x19, #0x40]
0x567b8	601e40f9	ldr	x0, [x19, #0x38]
0x567bc	08745e92	and	x8, x0, #0xfffffffc00000000
0x567c0	890640f9	ldr	x9, [x20, #0x8]
0x567c4	1f0109eb	cmp	x8, x9
0x567c8	41000054	b.ne	0x567d0 <_WeChatMain+0x3cf64>
0x567cc	bda4ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x567d0	7f1e00f9	str	xzr, [x19, #0x38]
0x567d4	601a40f9	ldr	x0, [x19, #0x30]
0x567d8	200100b4	cbz	x0, 0x567fc <_WeChatMain+0x3cf90>
0x567dc	08200091	add	x8, x0, #0x8
0x567e0	09008012	mov	w9, #-0x1               ; =-1
0x567e4	0801e9b8	ldaddal	w9, w8, [x8]
0x567e8	1f050071	cmp	w8, #0x1
0x567ec	81000054	b.ne	0x567fc <_WeChatMain+0x3cf90>
0x567f0	080040f9	ldr	x8, [x0]
0x567f4	080540f9	ldr	x8, [x8, #0x8]
0x567f8	00013fd6	blr	x8
0x567fc	e00313aa	mov	x0, x19
0x56800	010f8052	mov	w1, #0x78               ; =120
0x56804	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x56808	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x5680c	00a6c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x56810	c0035fd6	ret
0x56814	e60300aa	mov	x6, x0
0x56818	a004818b	add	x0, x5, x1, asr #1
0x5681c	61000036	tbz	w1, #0x0, 0x56828 <_WeChatMain+0x3cfbc>
0x56820	080040f9	ldr	x8, [x0]
0x56824	064966f8	ldr	x6, [x8, w6, uxtw]
0x56828	e10302aa	mov	x1, x2
0x5682c	e20303aa	mov	x2, x3
0x56830	e30304aa	mov	x3, x4
0x56834	c0001fd6	br	x6
0x56838	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x5683c	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x56840	fd430091	add	x29, sp, #0x10
0x56844	f30301aa	mov	x19, x1
0x56848	f40300aa	mov	x20, x0
0x5684c	001c40f9	ldr	x0, [x0, #0x38]
0x56850	62a6ff97	bl	0x401d8 <_WeChatMain+0x2696c>
0x56854	860242a9	ldp	x6, x0, [x20, #0x20]
0x56858	810a43a9	ldp	x1, x2, [x20, #0x30]
0x5685c	832240f9	ldr	x3, [x20, #0x40]
0x56860	844a40b9	ldr	w4, [x20, #0x48]
0x56864	e50313aa	mov	x5, x19
0x56868	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x5686c	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x56870	c0001fd6	br	x6
0x56874	600200b4	cbz	x0, 0x568c0 <_WeChatMain+0x3d054>
0x56878	081c40f9	ldr	x8, [x0, #0x38]
0x5687c	09755e92	and	x9, x8, #0xfffffffc00000000
0x56880	2afd0490	adrp	x10, 0x9ffa000 <_wxam_enc_uninit_10+0x9ffa000>
0x56884	4a013b91	add	x10, x10, #0xec0
0x56888	4a0540f9	ldr	x10, [x10, #0x8]
0x5688c	3f010aeb	cmp	x9, x10
0x56890	41010054	b.ne	0x568b8 <_WeChatMain+0x3d04c>
0x56894	f44fbea9	stp	x20, x19, [sp, #-0x20]!
0x56898	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x5689c	fd430091	add	x29, sp, #0x10
0x568a0	f30300aa	mov	x19, x0
0x568a4	e00308aa	mov	x0, x8
0x568a8	86a4ff97	bl	0x3fac0 <_WeChatMain+0x26254>
0x568ac	e00313aa	mov	x0, x19
0x568b0	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x568b4	f44fc2a8	ldp	x20, x19, [sp], #0x20
0x568b8	010a8052	mov	w1, #0x50               ; =80
0x568bc	d4a5c315	b	0x714000c <_wxam_enc_uninit_10+0x714000c>
0x568c0	c0035fd6	ret
0x568c4	ff8300d1	sub	sp, sp, #0x20
0x568c8	fd7b01a9	stp	x29, x30, [sp, #0x10]
0x568cc	fd430091	add	x29, sp, #0x10
0x568d0	e20301aa	mov	x2, x1
0x568d4	bff31f38	sturb	wzr, [x29, #-0x1]
0x568d8	a10700d1	sub	x1, x29, #0x1
0x568dc	04000094	bl	0x568ec <_WeChatMain+0x3d080>
0x568e0	fd7b41a9	ldp	x29, x30, [sp, #0x10]
0x568e4	ff830091	add	sp, sp, #0x20
0x568e8	c0035fd6	ret
