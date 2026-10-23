0x2fc361c	fc6fbaa9	stp x28, x27, [sp, #-0x60]!
0x2fc3620	fa6701a9	stp x26, x25, [sp, #0x10]
0x2fc3624	f85f02a9	stp x24, x23, [sp, #0x20]
0x2fc3628	f65703a9	stp x22, x21, [sp, #0x30]
0x2fc362c	f44f04a9	stp x20, x19, [sp, #0x40]
0x2fc3630	fd7b05a9	stp x29, x30, [sp, #0x50]
0x2fc3634	fd430191	add x29, sp, #0x50
0x2fc3638	ff030ed1	sub sp, sp, #0x380
0x2fc363c	f50301aa	mov x21, x1
0x2fc3640	f40300aa	mov x20, x0
0x2fc3644	f30308aa	mov x19, x8
0x2fc3648	885b03f0	adrp x8, 0x9b36000
0x2fc364c	084d46f9	ldr x8, [x8, #0xc98]
0x2fc3650	080140f9	ldr x8, [x8]
0x2fc3654	a8831af8	stur x8, [x29, #-0x58]
0x2fc3658	e8f301b2	mov x8, #-0x5555555555555556
0x2fc365c	e8a311a9	stp x8, x8, [sp, #0x118]
0x2fc3660	e88b00f9	str x8, [sp, #0x110]
0x2fc3664	287cc039	ldrsb w8, [x1, #0x1f]
0x2fc3668	c800f837	tbnz w8, #0x1f, 0x2fc3680
0x2fc366c	a082c03c	ldur q0, [x21, #0x8]
0x2fc3670	e047803d	str q0, [sp, #0x110]
0x2fc3674	a88241f8	ldur x8, [x21, #0x18]
0x2fc3678	e89300f9	str x8, [sp, #0x120]
0x2fc367c	04000014	b 0x2fc368c
0x2fc3680	a18a40a9	ldp x1, x2, [x21, #0x8]
0x2fc3684	e0430491	add x0, sp, #0x110
0x2fc3688	a6554197	bl 0x18d20
0x2fc368c	e8f301b2	mov x8, #-0x5555555555555556
0x2fc3690	e8a30fa9	stp x8, x8, [sp, #0xf8]
0x2fc3694	e87b00f9	str x8, [sp, #0xf0]
0x2fc3698	a8fec039	ldrsb w8, [x21, #0x3f]
0x2fc369c	c800f837	tbnz w8, #0x1f, 0x2fc36b4
0x2fc36a0	a082c23c	ldur q0, [x21, #0x28]
0x2fc36a4	e03f803d	str q0, [sp, #0xf0]
0x2fc36a8	a88243f8	ldur x8, [x21, #0x38]
0x2fc36ac	e88300f9	str x8, [sp, #0x100]
0x2fc36b0	04000014	b 0x2fc36c0
0x2fc36b4	a18a42a9	ldp x1, x2, [x21, #0x28]
0x2fc36b8	e0c30391	add x0, sp, #0xf0
0x2fc36bc	99554197	bl 0x18d20
0x2fc36c0	e89f4439	ldrb w8, [sp, #0x127]
0x2fc36c4	091d0013	sxtb w9, w8
0x2fc36c8	ea8f40f9	ldr x10, [sp, #0x118]
0x2fc36cc	3f010071	cmp w9, #0x0
0x2fc36d0	48b1889a	csel x8, x10, x8, lt
0x2fc36d4	880000b4	cbz x8, 0x2fc36e4
0x2fc36d8	80a20591	add x0, x20, #0x168
0x2fc36dc	e1430491	add x1, sp, #0x110
0x2fc36e0	80f00595	bl 0x713f8e0
0x2fc36e4	ff7f1aa9	stp xzr, xzr, [sp, #0x1a0]
0x2fc36e8	ffdb00f9	str xzr, [sp, #0x1b0]
0x2fc36ec	80a20591	add x0, x20, #0x168
0x2fc36f0	e1830691	add x1, sp, #0x1a0
0x2fc36f4	3bdb6a94	bl 0x4a7a3e0
0x2fc36f8	f60300aa	mov x22, x0
0x2fc36fc	f7d340f9	ldr x23, [sp, #0x1a0]
0x2fc3700	b70200b4	cbz x23, 0x2fc3754
0x2fc3704	f8d740f9	ldr x24, [sp, #0x1a8]
0x2fc3708	e00317aa	mov x0, x23
0x2fc370c	1f0317eb	cmp x24, x23
0x2fc3710	a1000054	b.ne 0x2fc3724
0x2fc3714	0c000014	b 0x2fc3744
0x2fc3718	186300d1	sub x24, x24, #0x18
0x2fc371c	1f0317eb	cmp x24, x23
0x2fc3720	00010054	b.eq 0x2fc3740
0x2fc3724	08f3df38	ldursb w8, [x24, #-0x1]
0x2fc3728	88ffff36	tbz w8, #0x1f, 0x2fc3718
0x2fc372c	00835ef8	ldur x0, [x24, #-0x18]
0x2fc3730	08835ff8	ldur x8, [x24, #-0x8]
0x2fc3734	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc3738	35f20595	bl 0x714000c
0x2fc373c	f7ffff17	b 0x2fc3718
0x2fc3740	e0d340f9	ldr x0, [sp, #0x1a0]
0x2fc3744	f7d700f9	str x23, [sp, #0x1a8]
0x2fc3748	e8db40f9	ldr x8, [sp, #0x1b0]
0x2fc374c	010100cb	sub x1, x8, x0
0x2fc3750	2ff20595	bl 0x714000c
0x2fc3754	f8c30991	add x24, sp, #0x270
0x2fc3758	960e0036	tbz w22, #0x0, 0x2fc3928
0x2fc375c	e00314aa	mov x0, x20
0x2fc3760	21008052	mov w1, #0x1
0x2fc3764	3d060094	bl 0x2fc5058
0x2fc3768	03985a94	bl 0x4669774
0x2fc376c	f7a30491	add x23, sp, #0x128
0x2fc3770	08000391	add x8, x0, #0xc0
0x2fc3774	08fddf08	ldarb w8, [x8]
0x2fc3778	68210036	tbz w8, #0x0, 0x2fc3ba4
0x2fc377c	60008052	mov w0, #0x3
0x2fc3780	7e68b994	bl 0x5e1d978
0x2fc3784	e00b0034	cbz w0, 0x2fc3900
0x2fc3788	f4030091	mov x20, sp
0x2fc378c	e8030091	mov x8, sp
0x2fc3790	2bf76294	bl 0x488143c
0x2fc3794	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc3798	e90340f9	ldr x9, [sp]
0x2fc379c	1f010071	cmp w8, #0x0
0x2fc37a0	22b1949a	csel x2, x9, x20, lt
0x2fc37a4	68a003f0	adrp x8, 0xa3d2000
0x2fc37a8	09854d39	ldrb w9, [x8, #0x361]
0x2fc37ac	29010037	tbnz w9, #0x0, 0x2fc37d0
0x2fc37b0	c9c602b0	adrp x9, 0x889c000
0x2fc37b4	2011c03d	ldr q0, [x9, #0x40]
0x2fc37b8	69a003f0	adrp x9, 0xa3d2000
0x2fc37bc	29410d91	add x9, x9, #0x350
0x2fc37c0	2001803d	str q0, [x9]
0x2fc37c4	3f410039	strb wzr, [x9, #0x10]
0x2fc37c8	29008052	mov w9, #0x1
0x2fc37cc	09850d39	strb w9, [x8, #0x361]
0x2fc37d0	68a003f0	adrp x8, 0xa3d2000
0x2fc37d4	09f95039	ldrb w9, [x8, #0x43e]
0x2fc37d8	a9010037	tbnz w9, #0x0, 0x2fc380c
0x2fc37dc	49a60290	adrp x9, 0x848b000
0x2fc37e0	202945fd	ldr d0, [x9, #0xa50]
0x2fc37e4	69a003f0	adrp x9, 0xa3d2000
0x2fc37e8	29c11091	add x9, x9, #0x430
0x2fc37ec	200100fd	str d0, [x9]
0x2fc37f0	6aaf0290	adrp x10, 0x85af000
0x2fc37f4	409547fd	ldr d0, [x10, #0xf28]
0x2fc37f8	200900bd	str s0, [x9, #0x8]
0x2fc37fc	ca0d8052	mov w10, #0x6e
0x2fc3800	2a190079	strh w10, [x9, #0xc]
0x2fc3804	29008052	mov w9, #0x1
0x2fc3808	09f91039	strb w9, [x8, #0x43e]
0x2fc380c	63a003f0	adrp x3, 0xa3d2000
0x2fc3810	63400d91	add x3, x3, #0x350
0x2fc3814	64a003f0	adrp x4, 0xa3d2000
0x2fc3818	84c01091	add x4, x4, #0x430
0x2fc381c	e0830691	add x0, sp, #0x1a0
0x2fc3820	61008052	mov w1, #0x3
0x2fc3824	051c8052	mov w5, #0xe0
0x2fc3828	06008052	mov w6, #0x0
0x2fc382c	070080d2	mov x7, #0x0
0x2fc3830	0866b994	bl 0x5e1d050
0x2fc3834	68a003f0	adrp x8, 0xa3d2000
0x2fc3838	09915239	ldrb w9, [x8, #0x4a4]
0x2fc383c	e9030037	tbnz w9, #0x0, 0x2fc38b8
0x2fc3840	c9c602b0	adrp x9, 0x889c000
0x2fc3844	202541fd	ldr d0, [x9, #0x248]
0x2fc3848	a9a802b0	adrp x9, 0x84d8000
0x2fc384c	211943fd	ldr d1, [x9, #0x630]
0x2fc3850	20040c6e	mov.s v0[1], v1[0]
0x2fc3854	c9c602b0	adrp x9, 0x889c000
0x2fc3858	214941fd	ldr d1, [x9, #0x290]
0x2fc385c	2004146e	mov.s v0[2], v1[0]
0x2fc3860	e9bd02f0	adrp x9, 0x8782000
0x2fc3864	210d44fd	ldr d1, [x9, #0x818]
0x2fc3868	20041c6e	mov.s v0[3], v1[0]
0x2fc386c	e9a602f0	adrp x9, 0x84a2000
0x2fc3870	216542fd	ldr d1, [x9, #0x4c8]
0x2fc3874	c9c602b0	adrp x9, 0x889c000
0x2fc3878	224d41fd	ldr d2, [x9, #0x298]
0x2fc387c	41040c6e	mov.s v1[1], v2[0]
0x2fc3880	c9c602b0	adrp x9, 0x889c000
0x2fc3884	225141fd	ldr d2, [x9, #0x2a0]
0x2fc3888	4104146e	mov.s v1[2], v2[0]
0x2fc388c	c9c602b0	adrp x9, 0x889c000
0x2fc3890	225541fd	ldr d2, [x9, #0x2a8]
0x2fc3894	41041c6e	mov.s v1[3], v2[0]
0x2fc3898	69a003f0	adrp x9, 0xa3d2000
0x2fc389c	29011291	add x9, x9, #0x480
0x2fc38a0	200500ad	stp q0, q1, [x9]
0x2fc38a4	eaa602f0	adrp x10, 0x84a2000
0x2fc38a8	409d47fd	ldr d0, [x10, #0xf38]
0x2fc38ac	202100bd	str s0, [x9, #0x20]
0x2fc38b0	29008052	mov w9, #0x1
0x2fc38b4	09911239	strb w9, [x8, #0x4a4]
0x2fc38b8	00e4006f	movi.2d v0, #0000000000000000
0x2fc38bc	e08316ad	stp q0, q0, [sp, #0x2d0]
0x2fc38c0	e08315ad	stp q0, q0, [sp, #0x2b0]
0x2fc38c4	e08314ad	stp q0, q0, [sp, #0x290]
0x2fc38c8	e08313ad	stp q0, q0, [sp, #0x270]
0x2fc38cc	61a003f0	adrp x1, 0xa3d2000
0x2fc38d0	21001291	add x1, x1, #0x480
0x2fc38d4	e0830691	add x0, sp, #0x1a0
0x2fc38d8	e2c30991	add x2, sp, #0x270
0x2fc38dc	9066b994	bl 0x5e1d31c
0x2fc38e0	e0830691	add x0, sp, #0x1a0
0x2fc38e4	2e66b994	bl 0x5e1d19c
0x2fc38e8	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc38ec	a800f836	tbz w8, #0x1f, 0x2fc3900
0x2fc38f0	e00340f9	ldr x0, [sp]
0x2fc38f4	e80b40f9	ldr x8, [sp, #0x10]
0x2fc38f8	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc38fc	c4f10595	bl 0x714000c
0x2fc3900	c8c602b0	adrp x8, 0x889c000
0x2fc3904	005941fd	ldr d0, [x8, #0x2b0]
0x2fc3908	e0d300fd	str d0, [sp, #0x1a0]
0x2fc390c	f5830691	add x21, sp, #0x1a0
0x2fc3910	00e4006f	movi.2d v0, #0000000000000000
0x2fc3914	e00204ad	stp q0, q0, [x23, #0x80]
0x2fc3918	ffe700f9	str xzr, [sp, #0x1c8]
0x2fc391c	004e8052	mov w0, #0x270
0x2fc3920	c4f10595	bl 0x7140030
0x2fc3924	0b010014	b 0x2fc3d50
0x2fc3928	60008052	mov w0, #0x3
0x2fc392c	1368b994	bl 0x5e1d978
0x2fc3930	000c0034	cbz w0, 0x2fc3ab0
0x2fc3934	f4030091	mov x20, sp
0x2fc3938	e8030091	mov x8, sp
0x2fc393c	c0f66294	bl 0x488143c
0x2fc3940	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc3944	e90340f9	ldr x9, [sp]
0x2fc3948	1f010071	cmp w8, #0x0
0x2fc394c	22b1949a	csel x2, x9, x20, lt
0x2fc3950	68a003f0	adrp x8, 0xa3d2000
0x2fc3954	09854d39	ldrb w9, [x8, #0x361]
0x2fc3958	29010037	tbnz w9, #0x0, 0x2fc397c
0x2fc395c	c9c602b0	adrp x9, 0x889c000
0x2fc3960	2011c03d	ldr q0, [x9, #0x40]
0x2fc3964	69a003f0	adrp x9, 0xa3d2000
0x2fc3968	29410d91	add x9, x9, #0x350
0x2fc396c	2001803d	str q0, [x9]
0x2fc3970	3f410039	strb wzr, [x9, #0x10]
0x2fc3974	29008052	mov w9, #0x1
0x2fc3978	09850d39	strb w9, [x8, #0x361]
0x2fc397c	68a003f0	adrp x8, 0xa3d2000
0x2fc3980	09f95039	ldrb w9, [x8, #0x43e]
0x2fc3984	a9010037	tbnz w9, #0x0, 0x2fc39b8
0x2fc3988	49a60290	adrp x9, 0x848b000
0x2fc398c	202945fd	ldr d0, [x9, #0xa50]
0x2fc3990	69a003f0	adrp x9, 0xa3d2000
0x2fc3994	29c11091	add x9, x9, #0x430
0x2fc3998	200100fd	str d0, [x9]
0x2fc399c	6aaf0290	adrp x10, 0x85af000
0x2fc39a0	409547fd	ldr d0, [x10, #0xf28]
0x2fc39a4	200900bd	str s0, [x9, #0x8]
0x2fc39a8	ca0d8052	mov w10, #0x6e
0x2fc39ac	2a190079	strh w10, [x9, #0xc]
0x2fc39b0	29008052	mov w9, #0x1
0x2fc39b4	09f91039	strb w9, [x8, #0x43e]
0x2fc39b8	63a003f0	adrp x3, 0xa3d2000
0x2fc39bc	63400d91	add x3, x3, #0x350
0x2fc39c0	64a003f0	adrp x4, 0xa3d2000
0x2fc39c4	84c01091	add x4, x4, #0x430
0x2fc39c8	e0830691	add x0, sp, #0x1a0
0x2fc39cc	61008052	mov w1, #0x3
0x2fc39d0	a51a8052	mov w5, #0xd5
0x2fc39d4	06008052	mov w6, #0x0
0x2fc39d8	070080d2	mov x7, #0x0
0x2fc39dc	9d65b994	bl 0x5e1d050
0x2fc39e0	68a003f0	adrp x8, 0xa3d2000
0x2fc39e4	09f55139	ldrb w9, [x8, #0x47d]
0x2fc39e8	09040037	tbnz w9, #0x0, 0x2fc3a68
0x2fc39ec	090080d2	mov x9, #0x0
0x2fc39f0	eae702b2	mov x10, #-0x3333333333333334
0x2fc39f4	aa9999f2	movk x10, #0xcccd
0x2fc39f8	6b028092	mov x11, #-0x14
0x2fc39fc	ccc602d0	adrp x12, 0x889d000
0x2fc3a00	8c010691	add x12, x12, #0x180
0x2fc3a04	4085040f	movi.4h v0, #0x8a
0x2fc3a08	6da003f0	adrp x13, 0xa3d2000
0x2fc3a0c	adfd1091	add x13, x13, #0x43f
0x2fc3a10	2e7dca9b	umulh x14, x9, x10
0x2fc3a14	cefd44d3	lsr x14, x14, #4
0x2fc3a18	8f01098b	add x15, x12, x9
0x2fc3a1c	ce3d0b9b	madd x14, x14, x11, x15
0x2fc3a20	efe50591	add x15, x15, #0x179
0x2fc3a24	ce950591	add x14, x14, #0x165
0x2fc3a28	e10140bd	ldr s1, [x15]
0x2fc3a2c	0110212e	uaddw.8h v1, v0, v1
0x2fc3a30	c20140bd	ldr s2, [x14]
0x2fc3a34	42a4082f	ushll.8h v2, v2, #0x0
0x2fc3a38	211c222e	eor.8b v1, v1, v2
0x2fc3a3c	2118000e	uzp1.8b v1, v1, v0
0x2fc3a40	a16929bc	str s1, [x13, x9]
0x2fc3a44	29110091	add x9, x9, #0x4
0x2fc3a48	3ff100f1	cmp x9, #0x3c
0x2fc3a4c	21feff54	b.ne 0x2fc3a10
0x2fc3a50	69a003f0	adrp x9, 0xa3d2000
0x2fc3a54	29ed1191	add x9, x9, #0x47b
0x2fc3a58	ca058052	mov w10, #0x2e
0x2fc3a5c	2a010079	strh w10, [x9]
0x2fc3a60	29008052	mov w9, #0x1
0x2fc3a64	09f51139	strb w9, [x8, #0x47d]
0x2fc3a68	00e4006f	movi.2d v0, #0000000000000000
0x2fc3a6c	e08316ad	stp q0, q0, [sp, #0x2d0]
0x2fc3a70	e08315ad	stp q0, q0, [sp, #0x2b0]
0x2fc3a74	e08314ad	stp q0, q0, [sp, #0x290]
0x2fc3a78	e08313ad	stp q0, q0, [sp, #0x270]
0x2fc3a7c	61a003f0	adrp x1, 0xa3d2000
0x2fc3a80	21fc1091	add x1, x1, #0x43f
0x2fc3a84	e0830691	add x0, sp, #0x1a0
0x2fc3a88	e2c30991	add x2, sp, #0x270
0x2fc3a8c	2466b994	bl 0x5e1d31c
0x2fc3a90	e0830691	add x0, sp, #0x1a0
0x2fc3a94	c265b994	bl 0x5e1d19c
0x2fc3a98	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc3a9c	a800f836	tbz w8, #0x1f, 0x2fc3ab0
0x2fc3aa0	e00340f9	ldr x0, [sp]
0x2fc3aa4	e80b40f9	ldr x8, [sp, #0x10]
0x2fc3aa8	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc3aac	58f10595	bl 0x714000c
0x2fc3ab0	c8c602b0	adrp x8, 0x889c000
0x2fc3ab4	002141fd	ldr d0, [x8, #0x240]
0x2fc3ab8	e03b01fd	str d0, [sp, #0x270]
0x2fc3abc	f9c30991	add x25, sp, #0x270
0x2fc3ac0	00e4006f	movi.2d v0, #0000000000000000
0x2fc3ac4	0083803c	stur q0, [x24, #0x8]
0x2fc3ac8	0083813c	stur q0, [x24, #0x18]
0x2fc3acc	ff4f01f9	str xzr, [sp, #0x298]
0x2fc3ad0	004e8052	mov w0, #0x270
0x2fc3ad4	57f10595	bl 0x7140030
0x2fc3ad8	f40300aa	mov x20, x0
0x2fc3adc	00e4006f	movi.2d v0, #0000000000000000
0x2fc3ae0	0080803c	stur q0, [x0, #0x8]
0x2fc3ae4	e87003b0	adrp x8, 0x9de0000
0x2fc3ae8	08013e91	add x8, x8, #0xf80
0x2fc3aec	080000f9	str x8, [x0]
0x2fc3af0	15600091	add x21, x0, #0x18
0x2fc3af4	e00315aa	mov x0, x21
0x2fc3af8	01458052	mov w1, #0x228
0x2fc3afc	25f20595	bl 0x7140390
0x2fc3b00	28008052	mov w8, #0x1
0x2fc3b04	881a00b9	str w8, [x20, #0x18]
0x2fc3b08	88020891	add x8, x20, #0x200
0x2fc3b0c	9f0201f9	str xzr, [x20, #0x200]
0x2fc3b10	00e4006f	movi.2d v0, #0000000000000000
0x2fc3b14	0081803c	stur q0, [x8, #0x8]
0x2fc3b18	9f620839	strb wzr, [x20, #0x218]
0x2fc3b1c	800204ad	stp q0, q0, [x20, #0x80]
0x2fc3b20	800205ad	stp q0, q0, [x20, #0xa0]
0x2fc3b24	800206ad	stp q0, q0, [x20, #0xc0]
0x2fc3b28	800207ad	stp q0, q0, [x20, #0xe0]
0x2fc3b2c	800208ad	stp q0, q0, [x20, #0x100]
0x2fc3b30	800209ad	stp q0, q0, [x20, #0x120]
0x2fc3b34	80020aad	stp q0, q0, [x20, #0x140]
0x2fc3b38	80020bad	stp q0, q0, [x20, #0x160]
0x2fc3b3c	80020cad	stp q0, q0, [x20, #0x180]
0x2fc3b40	80020dad	stp q0, q0, [x20, #0x1a0]
0x2fc3b44	80020ead	stp q0, q0, [x20, #0x1c0]
0x2fc3b48	807a803d	str q0, [x20, #0x1e0]
0x2fc3b4c	88a60791	add x8, x20, #0x1e9
0x2fc3b50	0001803d	str q0, [x8]
0x2fc3b54	9f720479	strh wzr, [x20, #0x238]
0x2fc3b58	9f1a01f9	str xzr, [x20, #0x230]
0x2fc3b5c	808a803d	str q0, [x20, #0x220]
0x2fc3b60	800212ad	stp q0, q0, [x20, #0x240]
0x2fc3b64	809a803d	str q0, [x20, #0x260]
0x2fc3b68	f54b01f9	str x21, [sp, #0x290]
0x2fc3b6c	f44f01f9	str x20, [sp, #0x298]
0x2fc3b70	46027994	bl 0x4e04488
0x2fc3b74	f50300aa	mov x21, x0
0x2fc3b78	a0f70595	bl 0x71419f8
0x2fc3b7c	e8ef7db2	mov x8, #0x7ffffffffffffff8
0x2fc3b80	1f0008eb	cmp x0, x8
0x2fc3b84	c2770054	b.hs 0x2fc4a7c
0x2fc3b88	f40300aa	mov x20, x0
0x2fc3b8c	1f5c00f1	cmp x0, #0x17
0x2fc3b90	a2150054	b.hs 0x2fc3e44
0x2fc3b94	f4df0639	strb w20, [sp, #0x1b7]
0x2fc3b98	f6830691	add x22, sp, #0x1a0
0x2fc3b9c	941600b5	cbnz x20, 0x2fc3e6c
0x2fc3ba0	b7000014	b 0x2fc3e7c
0x2fc3ba4	f4965a94	bl 0x4669774
0x2fc3ba8	08c00a91	add x8, x0, #0x2b0
0x2fc3bac	08fddf88	ldar w8, [x8]
0x2fc3bb0	08090051	sub w8, w8, #0x2
0x2fc3bb4	1f090071	cmp w8, #0x2
0x2fc3bb8	48270054	b.hi 0x2fc40a0
0x2fc3bbc	80008052	mov w0, #0x4
0x2fc3bc0	6e67b994	bl 0x5e1d978
0x2fc3bc4	400b0034	cbz w0, 0x2fc3d2c
0x2fc3bc8	f4030091	mov x20, sp
0x2fc3bcc	e8030091	mov x8, sp
0x2fc3bd0	1bf66294	bl 0x488143c
0x2fc3bd4	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc3bd8	e90340f9	ldr x9, [sp]
0x2fc3bdc	1f010071	cmp w8, #0x0
0x2fc3be0	22b1949a	csel x2, x9, x20, lt
0x2fc3be4	68a003f0	adrp x8, 0xa3d2000
0x2fc3be8	09854d39	ldrb w9, [x8, #0x361]
0x2fc3bec	29010037	tbnz w9, #0x0, 0x2fc3c10
0x2fc3bf0	c9c602b0	adrp x9, 0x889c000
0x2fc3bf4	2011c03d	ldr q0, [x9, #0x40]
0x2fc3bf8	69a003f0	adrp x9, 0xa3d2000
0x2fc3bfc	29410d91	add x9, x9, #0x350
0x2fc3c00	2001803d	str q0, [x9]
0x2fc3c04	3f410039	strb wzr, [x9, #0x10]
0x2fc3c08	29008052	mov w9, #0x1
0x2fc3c0c	09850d39	strb w9, [x8, #0x361]
0x2fc3c10	68a003f0	adrp x8, 0xa3d2000
0x2fc3c14	09f95039	ldrb w9, [x8, #0x43e]
0x2fc3c18	a9010037	tbnz w9, #0x0, 0x2fc3c4c
0x2fc3c1c	49a60290	adrp x9, 0x848b000
0x2fc3c20	202945fd	ldr d0, [x9, #0xa50]
0x2fc3c24	69a003f0	adrp x9, 0xa3d2000
0x2fc3c28	29c11091	add x9, x9, #0x430
0x2fc3c2c	200100fd	str d0, [x9]
0x2fc3c30	6aaf0290	adrp x10, 0x85af000
0x2fc3c34	409547fd	ldr d0, [x10, #0xf28]
0x2fc3c38	200900bd	str s0, [x9, #0x8]
0x2fc3c3c	ca0d8052	mov w10, #0x6e
0x2fc3c40	2a190079	strh w10, [x9, #0xc]
0x2fc3c44	29008052	mov w9, #0x1
0x2fc3c48	09f91039	strb w9, [x8, #0x43e]
0x2fc3c4c	63a003f0	adrp x3, 0xa3d2000
0x2fc3c50	63400d91	add x3, x3, #0x350
0x2fc3c54	64a003f0	adrp x4, 0xa3d2000
0x2fc3c58	84c01091	add x4, x4, #0x430
0x2fc3c5c	e0830691	add x0, sp, #0x1a0
0x2fc3c60	81008052	mov w1, #0x4
0x2fc3c64	451d8052	mov w5, #0xea
0x2fc3c68	06008052	mov w6, #0x0
0x2fc3c6c	070080d2	mov x7, #0x0
0x2fc3c70	f864b994	bl 0x5e1d050
0x2fc3c74	68a003f0	adrp x8, 0xa3d2000
0x2fc3c78	090d5339	ldrb w9, [x8, #0x4c3]
0x2fc3c7c	49030037	tbnz w9, #0x0, 0x2fc3ce4
0x2fc3c80	c9c602b0	adrp x9, 0x889c000
0x2fc3c84	202541fd	ldr d0, [x9, #0x248]
0x2fc3c88	a9a802b0	adrp x9, 0x84d8000
0x2fc3c8c	211943fd	ldr d1, [x9, #0x630]
0x2fc3c90	20040c6e	mov.s v0[1], v1[0]
0x2fc3c94	c9c602b0	adrp x9, 0x889c000
0x2fc3c98	213d41fd	ldr d1, [x9, #0x278]
0x2fc3c9c	2004146e	mov.s v0[2], v1[0]
0x2fc3ca0	c9c602b0	adrp x9, 0x889c000
0x2fc3ca4	214141fd	ldr d1, [x9, #0x280]
0x2fc3ca8	20041c6e	mov.s v0[3], v1[0]
0x2fc3cac	69a003f0	adrp x9, 0xa3d2000
0x2fc3cb0	29a11291	add x9, x9, #0x4a8
0x2fc3cb4	2001803d	str q0, [x9]
0x2fc3cb8	2aa802f0	adrp x10, 0x84ca000
0x2fc3cbc	40e541fd	ldr d0, [x10, #0x3c8]
0x2fc3cc0	aaa802b0	adrp x10, 0x84d8000
0x2fc3cc4	414d41fd	ldr d1, [x10, #0x298]
0x2fc3cc8	20040c6e	mov.s v0[1], v1[0]
0x2fc3ccc	200900fd	str d0, [x9, #0x10]
0x2fc3cd0	2acd8d52	mov w10, #0x6e69
0x2fc3cd4	2a310079	strh w10, [x9, #0x18]
0x2fc3cd8	3f690039	strb wzr, [x9, #0x1a]
0x2fc3cdc	29008052	mov w9, #0x1
0x2fc3ce0	090d1339	strb w9, [x8, #0x4c3]
0x2fc3ce4	00e4006f	movi.2d v0, #0000000000000000
0x2fc3ce8	e08316ad	stp q0, q0, [sp, #0x2d0]
0x2fc3cec	e08315ad	stp q0, q0, [sp, #0x2b0]
0x2fc3cf0	e08314ad	stp q0, q0, [sp, #0x290]
0x2fc3cf4	e08313ad	stp q0, q0, [sp, #0x270]
0x2fc3cf8	61a003f0	adrp x1, 0xa3d2000
0x2fc3cfc	21a01291	add x1, x1, #0x4a8
0x2fc3d00	e0830691	add x0, sp, #0x1a0
0x2fc3d04	e2c30991	add x2, sp, #0x270
0x2fc3d08	8565b994	bl 0x5e1d31c
0x2fc3d0c	e0830691	add x0, sp, #0x1a0
0x2fc3d10	2365b994	bl 0x5e1d19c
0x2fc3d14	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc3d18	a800f836	tbz w8, #0x1f, 0x2fc3d2c
0x2fc3d1c	e00340f9	ldr x0, [sp]
0x2fc3d20	e80b40f9	ldr x8, [sp, #0x10]
0x2fc3d24	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc3d28	b9f00595	bl 0x714000c
0x2fc3d2c	c8c602b0	adrp x8, 0x889c000
0x2fc3d30	004541fd	ldr d0, [x8, #0x288]
0x2fc3d34	e0d300fd	str d0, [sp, #0x1a0]
0x2fc3d38	f5830691	add x21, sp, #0x1a0
0x2fc3d3c	00e4006f	movi.2d v0, #0000000000000000
0x2fc3d40	e00204ad	stp q0, q0, [x23, #0x80]
0x2fc3d44	ffe700f9	str xzr, [sp, #0x1c8]
0x2fc3d48	004e8052	mov w0, #0x270
0x2fc3d4c	b9f00595	bl 0x7140030
0x2fc3d50	f40300aa	mov x20, x0
0x2fc3d54	f60300aa	mov x22, x0
0x2fc3d58	00e4006f	movi.2d v0, #0000000000000000
0x2fc3d5c	c08e803c	str q0, [x22, #0x8]!
0x2fc3d60	e87003b0	adrp x8, 0x9de0000
0x2fc3d64	08013e91	add x8, x8, #0xf80
0x2fc3d68	080000f9	str x8, [x0]
0x2fc3d6c	15600091	add x21, x0, #0x18
0x2fc3d70	e00315aa	mov x0, x21
0x2fc3d74	01458052	mov w1, #0x228
0x2fc3d78	86f10595	bl 0x7140390
0x2fc3d7c	28008052	mov w8, #0x1
0x2fc3d80	881a00b9	str w8, [x20, #0x18]
0x2fc3d84	88020891	add x8, x20, #0x200
0x2fc3d88	9f0201f9	str xzr, [x20, #0x200]
0x2fc3d8c	00e4006f	movi.2d v0, #0000000000000000
0x2fc3d90	0081803c	stur q0, [x8, #0x8]
0x2fc3d94	9f620839	strb wzr, [x20, #0x218]
0x2fc3d98	800204ad	stp q0, q0, [x20, #0x80]
0x2fc3d9c	800205ad	stp q0, q0, [x20, #0xa0]
0x2fc3da0	800206ad	stp q0, q0, [x20, #0xc0]
0x2fc3da4	800207ad	stp q0, q0, [x20, #0xe0]
0x2fc3da8	800208ad	stp q0, q0, [x20, #0x100]
0x2fc3dac	800209ad	stp q0, q0, [x20, #0x120]
0x2fc3db0	80020aad	stp q0, q0, [x20, #0x140]
0x2fc3db4	80020bad	stp q0, q0, [x20, #0x160]
0x2fc3db8	80020cad	stp q0, q0, [x20, #0x180]
0x2fc3dbc	80020dad	stp q0, q0, [x20, #0x1a0]
0x2fc3dc0	80020ead	stp q0, q0, [x20, #0x1c0]
0x2fc3dc4	807a803d	str q0, [x20, #0x1e0]
0x2fc3dc8	88a60791	add x8, x20, #0x1e9
0x2fc3dcc	0001803d	str q0, [x8]
0x2fc3dd0	9f720479	strh wzr, [x20, #0x238]
0x2fc3dd4	9f1a01f9	str xzr, [x20, #0x230]
0x2fc3dd8	808a803d	str q0, [x20, #0x220]
0x2fc3ddc	800212ad	stp q0, q0, [x20, #0x240]
0x2fc3de0	809a803d	str q0, [x20, #0x260]
0x2fc3de4	f5531ca9	stp x21, x20, [sp, #0x1c0]
0x2fc3de8	e8d340f9	ldr x8, [sp, #0x1a0]
0x2fc3dec	687e00a9	stp x8, xzr, [x19]
0x2fc3df0	7f7e01a9	stp xzr, xzr, [x19, #0x10]
0x2fc3df4	755202a9	stp x21, x20, [x19, #0x20]
0x2fc3df8	741000b4	cbz x20, 0x2fc4004
0x2fc3dfc	28008052	mov w8, #0x1
0x2fc3e00	c80228f8	ldadd x8, x8, [x22]
0x2fc3e04	7fd20039	strb wzr, [x19, #0x34]
0x2fc3e08	7f3200b9	str wzr, [x19, #0x30]
0x2fc3e0c	7fe20039	strb wzr, [x19, #0x38]
0x2fc3e10	7fa20139	strb wzr, [x19, #0x68]
0x2fc3e14	08008092	mov x8, #-0x1
0x2fc3e18	c802e8f8	ldaddal x8, x8, [x22]
0x2fc3e1c	e80000b5	cbnz x8, 0x2fc3e38
0x2fc3e20	880240f9	ldr x8, [x20]
0x2fc3e24	080940f9	ldr x8, [x8, #0x10]
0x2fc3e28	e00314aa	mov x0, x20
0x2fc3e2c	00013fd6	blr x8
0x2fc3e30	e00314aa	mov x0, x20
0x2fc3e34	7aef0595	bl 0x713fc1c
0x2fc3e38	e8ffc639	ldrsb w8, [sp, #0x1bf]
0x2fc3e3c	880ff836	tbz w8, #0x1f, 0x2fc402c
0x2fc3e40	77000014	b 0x2fc401c
0x2fc3e44	880a40b2	orr x8, x20, #0x7
0x2fc3e48	1f5d00f1	cmp x8, #0x17
0x2fc3e4c	29038052	mov w9, #0x19
0x2fc3e50	3705889a	csinc x23, x9, x8, eq
0x2fc3e54	e00317aa	mov x0, x23
0x2fc3e58	76f00595	bl 0x7140030
0x2fc3e5c	f60300aa	mov x22, x0
0x2fc3e60	e80241b2	orr x8, x23, #0x8000000000000000
0x2fc3e64	f4a31aa9	stp x20, x8, [sp, #0x1a8]
0x2fc3e68	e0d300f9	str x0, [sp, #0x1a0]
0x2fc3e6c	e00316aa	mov x0, x22
0x2fc3e70	e10315aa	mov x1, x21
0x2fc3e74	e20314aa	mov x2, x20
0x2fc3e78	07f40595	bl 0x7140e94
0x2fc3e7c	df6a3438	strb wzr, [x22, x20]
0x2fc3e80	ffbb01b9	str wzr, [sp, #0x1b8]
0x2fc3e84	ffff1ca9	stp xzr, xzr, [sp, #0x1c8]
0x2fc3e88	f4830691	add x20, sp, #0x1a0
0x2fc3e8c	ffe300f9	str xzr, [sp, #0x1c0]
0x2fc3e90	80e20091	add x0, x20, #0x38
0x2fc3e94	0b9d4197	bl 0x2b2c0
0x2fc3e98	e84b41f9	ldr x8, [sp, #0x290]
0x2fc3e9c	00410091	add x0, x8, #0x10
0x2fc3ea0	e1830691	add x1, sp, #0x1a0
0x2fc3ea4	18040094	bl 0x2fc4f04
0x2fc3ea8	80e20091	add x0, x20, #0x38
0x2fc3eac	659d4197	bl 0x2b440
0x2fc3eb0	e85fc739	ldrsb w8, [sp, #0x1d7]
0x2fc3eb4	2802f837	tbnz w8, #0x1f, 0x2fc3ef8
0x2fc3eb8	e8dfc639	ldrsb w8, [sp, #0x1b7]
0x2fc3ebc	a802f837	tbnz w8, #0x1f, 0x2fc3f10
0x2fc3ec0	ffa301b9	str wzr, [sp, #0x1a0]
0x2fc3ec4	ff930639	strb wzr, [sp, #0x1a4]
0x2fc3ec8	ffa30639	strb wzr, [sp, #0x1a8]
0x2fc3ecc	ff630739	strb wzr, [sp, #0x1d8]
0x2fc3ed0	e83b41f9	ldr x8, [sp, #0x270]
0x2fc3ed4	e00313aa	mov x0, x19
0x2fc3ed8	088400f8	str x8, [x0], #0x8
0x2fc3edc	e83fca39	ldrsb w8, [sp, #0x28f]
0x2fc3ee0	2802f837	tbnz w8, #0x1f, 0x2fc3f24
0x2fc3ee4	2083c03c	ldur q0, [x25, #0x8]
0x2fc3ee8	0000803d	str q0, [x0]
0x2fc3eec	288341f8	ldur x8, [x25, #0x18]
0x2fc3ef0	080800f9	str x8, [x0, #0x10]
0x2fc3ef4	0f000014	b 0x2fc3f30
0x2fc3ef8	e0e340f9	ldr x0, [sp, #0x1c0]
0x2fc3efc	e8eb40f9	ldr x8, [sp, #0x1d0]
0x2fc3f00	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc3f04	42f00595	bl 0x714000c
0x2fc3f08	e8dfc639	ldrsb w8, [sp, #0x1b7]
0x2fc3f0c	a8fdff36	tbz w8, #0x1f, 0x2fc3ec0
0x2fc3f10	e0d340f9	ldr x0, [sp, #0x1a0]
0x2fc3f14	e8db40f9	ldr x8, [sp, #0x1b0]
0x2fc3f18	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc3f1c	3cf00595	bl 0x714000c
0x2fc3f20	e8ffff17	b 0x2fc3ec0
0x2fc3f24	e13f41f9	ldr x1, [sp, #0x278]
0x2fc3f28	e24341f9	ldr x2, [sp, #0x280]
0x2fc3f2c	7d534197	bl 0x18d20
0x2fc3f30	e94b41f9	ldr x9, [sp, #0x290]
0x2fc3f34	e84f41f9	ldr x8, [sp, #0x298]
0x2fc3f38	692202a9	stp x9, x8, [x19, #0x20]
0x2fc3f3c	880000b4	cbz x8, 0x2fc3f4c
0x2fc3f40	08210091	add x8, x8, #0x8
0x2fc3f44	29008052	mov w9, #0x1
0x2fc3f48	080129f8	ldadd x9, x8, [x8]
0x2fc3f4c	e8a341b9	ldr w8, [sp, #0x1a0]
0x2fc3f50	f50313aa	mov x21, x19
0x2fc3f54	bf8e0338	strb wzr, [x21, #0x38]!
0x2fc3f58	a8821fb8	stur w8, [x21, #-0x8]
0x2fc3f5c	e8934639	ldrb w8, [sp, #0x1a4]
0x2fc3f60	a8c21f38	sturb w8, [x21, #-0x4]
0x2fc3f64	bfc20039	strb wzr, [x21, #0x30]
0x2fc3f68	e8634739	ldrb w8, [sp, #0x1d8]
0x2fc3f6c	1f050071	cmp w8, #0x1
0x2fc3f70	81010054	b.ne 0x2fc3fa0
0x2fc3f74	e8ab41b9	ldr w8, [sp, #0x1a8]
0x2fc3f78	683a00b9	str w8, [x19, #0x38]
0x2fc3f7c	e8830691	add x8, sp, #0x1a0
0x2fc3f80	60020191	add x0, x19, #0x40
0x2fc3f84	01410091	add x1, x8, #0x10
0x2fc3f88	e2980094	bl 0x2fea310
0x2fc3f8c	28008052	mov w8, #0x1
0x2fc3f90	68a20139	strb w8, [x19, #0x68]
0x2fc3f94	e8634739	ldrb w8, [sp, #0x1d8]
0x2fc3f98	68000037	tbnz w8, #0x0, 0x2fc3fa4
0x2fc3f9c	0f000014	b 0x2fc3fd8
0x2fc3fa0	c8010034	cbz w8, 0x2fc3fd8
0x2fc3fa4	e0e340f9	ldr x0, [sp, #0x1c0]
0x2fc3fa8	c00000b4	cbz x0, 0x2fc3fc0
0x2fc3fac	130040f9	ldr x19, [x0]
0x2fc3fb0	01038052	mov w1, #0x18
0x2fc3fb4	16f00595	bl 0x714000c
0x2fc3fb8	e00313aa	mov x0, x19
0x2fc3fbc	93ffffb5	cbnz x19, 0x2fc3fac
0x2fc3fc0	e0db40f9	ldr x0, [sp, #0x1b0]
0x2fc3fc4	ffdb00f9	str xzr, [sp, #0x1b0]
0x2fc3fc8	800000b4	cbz x0, 0x2fc3fd8
0x2fc3fcc	e8df40f9	ldr x8, [sp, #0x1b8]
0x2fc3fd0	01f17dd3	lsl x1, x8, #3
0x2fc3fd4	0ef00595	bl 0x714000c
0x2fc3fd8	f34f41f9	ldr x19, [sp, #0x298]
0x2fc3fdc	b30000b4	cbz x19, 0x2fc3ff0
0x2fc3fe0	68220091	add x8, x19, #0x8
0x2fc3fe4	09008092	mov x9, #-0x1
0x2fc3fe8	0801e9f8	ldaddal x9, x8, [x8]
0x2fc3fec	481b00b4	cbz x8, 0x2fc4354
0x2fc3ff0	e83fca39	ldrsb w8, [sp, #0x28f]
0x2fc3ff4	c801f836	tbz w8, #0x1f, 0x2fc402c
0x2fc3ff8	e03f41f9	ldr x0, [sp, #0x278]
0x2fc3ffc	e84741f9	ldr x8, [sp, #0x288]
0x2fc4000	09000014	b 0x2fc4024
0x2fc4004	7fd20039	strb wzr, [x19, #0x34]
0x2fc4008	7f3200b9	str wzr, [x19, #0x30]
0x2fc400c	7fe20039	strb wzr, [x19, #0x38]
0x2fc4010	7fa20139	strb wzr, [x19, #0x68]
0x2fc4014	e8ffc639	ldrsb w8, [sp, #0x1bf]
0x2fc4018	a800f836	tbz w8, #0x1f, 0x2fc402c
0x2fc401c	e0d740f9	ldr x0, [sp, #0x1a8]
0x2fc4020	e8df40f9	ldr x8, [sp, #0x1b8]
0x2fc4024	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4028	f9ef0595	bl 0x714000c
0x2fc402c	e81fc439	ldrsb w8, [sp, #0x107]
0x2fc4030	2802f837	tbnz w8, #0x1f, 0x2fc4074
0x2fc4034	e89fc439	ldrsb w8, [sp, #0x127]
0x2fc4038	a802f837	tbnz w8, #0x1f, 0x2fc408c
0x2fc403c	a8835af8	ldur x8, [x29, #-0x58]
0x2fc4040	895b03d0	adrp x9, 0x9b36000
0x2fc4044	294d46f9	ldr x9, [x9, #0xc98]
0x2fc4048	290140f9	ldr x9, [x9]
0x2fc404c	3f0108eb	cmp x9, x8
0x2fc4050	41510054	b.ne 0x2fc4a78
0x2fc4054	ff030e91	add sp, sp, #0x380
0x2fc4058	fd7b45a9	ldp x29, x30, [sp, #0x50]
0x2fc405c	f44f44a9	ldp x20, x19, [sp, #0x40]
0x2fc4060	f65743a9	ldp x22, x21, [sp, #0x30]
0x2fc4064	f85f42a9	ldp x24, x23, [sp, #0x20]
0x2fc4068	fa6741a9	ldp x26, x25, [sp, #0x10]
0x2fc406c	fc6fc6a8	ldp x28, x27, [sp], #0x60
0x2fc4070	c0035fd6	ret
0x2fc4074	e07b40f9	ldr x0, [sp, #0xf0]
0x2fc4078	e88340f9	ldr x8, [sp, #0x100]
0x2fc407c	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4080	e3ef0595	bl 0x714000c
0x2fc4084	e89fc439	ldrsb w8, [sp, #0x127]
0x2fc4088	a8fdff36	tbz w8, #0x1f, 0x2fc403c
0x2fc408c	e08b40f9	ldr x0, [sp, #0x110]
0x2fc4090	e89340f9	ldr x8, [sp, #0x120]
0x2fc4094	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4098	ddef0595	bl 0x714000c
0x2fc409c	e8ffff17	b 0x2fc403c
0x2fc40a0	40008052	mov w0, #0x2
0x2fc40a4	3566b994	bl 0x5e1d978
0x2fc40a8	800b0034	cbz w0, 0x2fc4218
0x2fc40ac	f6030091	mov x22, sp
0x2fc40b0	e8030091	mov x8, sp
0x2fc40b4	e2f46294	bl 0x488143c
0x2fc40b8	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc40bc	e90340f9	ldr x9, [sp]
0x2fc40c0	1f010071	cmp w8, #0x0
0x2fc40c4	22b1969a	csel x2, x9, x22, lt
0x2fc40c8	68a003d0	adrp x8, 0xa3d2000
0x2fc40cc	09854d39	ldrb w9, [x8, #0x361]
0x2fc40d0	29010037	tbnz w9, #0x0, 0x2fc40f4
0x2fc40d4	c9c60290	adrp x9, 0x889c000
0x2fc40d8	2011c03d	ldr q0, [x9, #0x40]
0x2fc40dc	69a003d0	adrp x9, 0xa3d2000
0x2fc40e0	29410d91	add x9, x9, #0x350
0x2fc40e4	2001803d	str q0, [x9]
0x2fc40e8	3f410039	strb wzr, [x9, #0x10]
0x2fc40ec	29008052	mov w9, #0x1
0x2fc40f0	09850d39	strb w9, [x8, #0x361]
0x2fc40f4	68a003d0	adrp x8, 0xa3d2000
0x2fc40f8	09f95039	ldrb w9, [x8, #0x43e]
0x2fc40fc	a9010037	tbnz w9, #0x0, 0x2fc4130
0x2fc4100	29a602f0	adrp x9, 0x848b000
0x2fc4104	202945fd	ldr d0, [x9, #0xa50]
0x2fc4108	69a003d0	adrp x9, 0xa3d2000
0x2fc410c	29c11091	add x9, x9, #0x430
0x2fc4110	200100fd	str d0, [x9]
0x2fc4114	4aaf02f0	adrp x10, 0x85af000
0x2fc4118	409547fd	ldr d0, [x10, #0xf28]
0x2fc411c	200900bd	str s0, [x9, #0x8]
0x2fc4120	ca0d8052	mov w10, #0x6e
0x2fc4124	2a190079	strh w10, [x9, #0xc]
0x2fc4128	29008052	mov w9, #0x1
0x2fc412c	09f91039	strb w9, [x8, #0x43e]
0x2fc4130	63a003d0	adrp x3, 0xa3d2000
0x2fc4134	63400d91	add x3, x3, #0x350
0x2fc4138	64a003d0	adrp x4, 0xa3d2000
0x2fc413c	84c01091	add x4, x4, #0x430
0x2fc4140	e0830691	add x0, sp, #0x1a0
0x2fc4144	41008052	mov w1, #0x2
0x2fc4148	051e8052	mov w5, #0xf0
0x2fc414c	06008052	mov w6, #0x0
0x2fc4150	070080d2	mov x7, #0x0
0x2fc4154	bf63b994	bl 0x5e1d050
0x2fc4158	68a003d0	adrp x8, 0xa3d2000
0x2fc415c	09915339	ldrb w9, [x8, #0x4e4]
0x2fc4160	89030037	tbnz w9, #0x0, 0x2fc41d0
0x2fc4164	c9c60290	adrp x9, 0x889c000
0x2fc4168	202541fd	ldr d0, [x9, #0x248]
0x2fc416c	a9a80290	adrp x9, 0x84d8000
0x2fc4170	211943fd	ldr d1, [x9, #0x630]
0x2fc4174	20040c6e	mov.s v0[1], v1[0]
0x2fc4178	c9c60290	adrp x9, 0x889c000
0x2fc417c	212941fd	ldr d1, [x9, #0x250]
0x2fc4180	2004146e	mov.s v0[2], v1[0]
0x2fc4184	09a802f0	adrp x9, 0x84c7000
0x2fc4188	21b543fd	ldr d1, [x9, #0x768]
0x2fc418c	20041c6e	mov.s v0[3], v1[0]
0x2fc4190	c9c60290	adrp x9, 0x889c000
0x2fc4194	212d41fd	ldr d1, [x9, #0x258]
0x2fc4198	e9c102b0	adrp x9, 0x8801000
0x2fc419c	223940fd	ldr d2, [x9, #0x70]
0x2fc41a0	41040c6e	mov.s v1[1], v2[0]
0x2fc41a4	09b902f0	adrp x9, 0x86e7000
0x2fc41a8	22a944fd	ldr d2, [x9, #0x950]
0x2fc41ac	4104146e	mov.s v1[2], v2[0]
0x2fc41b0	c9c60290	adrp x9, 0x889c000
0x2fc41b4	223141fd	ldr d2, [x9, #0x260]
0x2fc41b8	41041c6e	mov.s v1[3], v2[0]
0x2fc41bc	69a003d0	adrp x9, 0xa3d2000
0x2fc41c0	29111391	add x9, x9, #0x4c4
0x2fc41c4	200500ad	stp q0, q1, [x9]
0x2fc41c8	29008052	mov w9, #0x1
0x2fc41cc	09911339	strb w9, [x8, #0x4e4]
0x2fc41d0	00e4006f	movi.2d v0, #0000000000000000
0x2fc41d4	e08316ad	stp q0, q0, [sp, #0x2d0]
0x2fc41d8	e08315ad	stp q0, q0, [sp, #0x2b0]
0x2fc41dc	e08314ad	stp q0, q0, [sp, #0x290]
0x2fc41e0	e08313ad	stp q0, q0, [sp, #0x270]
0x2fc41e4	61a003d0	adrp x1, 0xa3d2000
0x2fc41e8	21101391	add x1, x1, #0x4c4
0x2fc41ec	e0830691	add x0, sp, #0x1a0
0x2fc41f0	e2c30991	add x2, sp, #0x270
0x2fc41f4	4a64b994	bl 0x5e1d31c
0x2fc41f8	e0830691	add x0, sp, #0x1a0
0x2fc41fc	e863b994	bl 0x5e1d19c
0x2fc4200	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc4204	a800f836	tbz w8, #0x1f, 0x2fc4218
0x2fc4208	e00340f9	ldr x0, [sp]
0x2fc420c	e80b40f9	ldr x8, [sp, #0x10]
0x2fc4210	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4214	7eef0595	bl 0x714000c
0x2fc4218	88824439	ldrb w8, [x20, #0x120]
0x2fc421c	88300037	tbnz w8, #0x0, 0x2fc482c
0x2fc4220	e8f301b2	mov x8, #-0x5555555555555556
0x2fc4224	e8230ea9	stp x8, x8, [sp, #0xe0]
0x2fc4228	e8830391	add x8, sp, #0xe0
0x2fc422c	e00314aa	mov x0, x20
0x2fc4230	2d060094	bl 0x2fc5ae4
0x2fc4234	50955a94	bl 0x4669774
0x2fc4238	e8430391	add x8, sp, #0xd0
0x2fc423c	ce9a5a94	bl 0x466ad74
0x2fc4240	68a003d0	adrp x8, 0xa3d2000
0x2fc4244	09f95039	ldrb w9, [x8, #0x43e]
0x2fc4248	a9010037	tbnz w9, #0x0, 0x2fc427c
0x2fc424c	29a602f0	adrp x9, 0x848b000
0x2fc4250	202945fd	ldr d0, [x9, #0xa50]
0x2fc4254	69a003d0	adrp x9, 0xa3d2000
0x2fc4258	29c11091	add x9, x9, #0x430
0x2fc425c	200100fd	str d0, [x9]
0x2fc4260	4aaf02f0	adrp x10, 0x85af000
0x2fc4264	409547fd	ldr d0, [x10, #0xf28]
0x2fc4268	200900bd	str s0, [x9, #0x8]
0x2fc426c	ca0d8052	mov w10, #0x6e
0x2fc4270	2a190079	strh w10, [x9, #0xc]
0x2fc4274	29008052	mov w9, #0x1
0x2fc4278	09f91039	strb w9, [x8, #0x43e]
0x2fc427c	68a003d0	adrp x8, 0xa3d2000
0x2fc4280	09195539	ldrb w9, [x8, #0x546]
0x2fc4284	c9030037	tbnz w9, #0x0, 0x2fc42fc
0x2fc4288	090080d2	mov x9, #0x0
0x2fc428c	eae702b2	mov x10, #-0x3333333333333334
0x2fc4290	aa9999f2	movk x10, #0xcccd
0x2fc4294	6b028092	mov x11, #-0x14
0x2fc4298	ccc602b0	adrp x12, 0x889d000
0x2fc429c	8c010691	add x12, x12, #0x180
0x2fc42a0	4085040f	movi.4h v0, #0x8a
0x2fc42a4	6da003d0	adrp x13, 0xa3d2000
0x2fc42a8	ad951391	add x13, x13, #0x4e5
0x2fc42ac	2e7dca9b	umulh x14, x9, x10
0x2fc42b0	cefd44d3	lsr x14, x14, #4
0x2fc42b4	8f01098b	add x15, x12, x9
0x2fc42b8	ce3d0b9b	madd x14, x14, x11, x15
0x2fc42bc	ef990991	add x15, x15, #0x266
0x2fc42c0	ce490991	add x14, x14, #0x252
0x2fc42c4	e10140bd	ldr s1, [x15]
0x2fc42c8	0110212e	uaddw.8h v1, v0, v1
0x2fc42cc	c20140bd	ldr s2, [x14]
0x2fc42d0	42a4082f	ushll.8h v2, v2, #0x0
0x2fc42d4	211c222e	eor.8b v1, v1, v2
0x2fc42d8	2118000e	uzp1.8b v1, v1, v0
0x2fc42dc	a16929bc	str s1, [x13, x9]
0x2fc42e0	29110091	add x9, x9, #0x4
0x2fc42e4	3f8101f1	cmp x9, #0x60
0x2fc42e8	21feff54	b.ne 0x2fc42ac
0x2fc42ec	69a003d0	adrp x9, 0xa3d2000
0x2fc42f0	3f151539	strb wzr, [x9, #0x545]
0x2fc42f4	29008052	mov w9, #0x1
0x2fc42f8	09191539	strb w9, [x8, #0x546]
0x2fc42fc	f96b40f9	ldr x25, [sp, #0xd0]
0x2fc4300	60a003d0	adrp x0, 0xa3d2000
0x2fc4304	00c01091	add x0, x0, #0x430
0x2fc4308	61a003d0	adrp x1, 0xa3d2000
0x2fc430c	21941391	add x1, x1, #0x4e5
0x2fc4310	e8c30291	add x8, sp, #0xb0
0x2fc4314	621e8052	mov w2, #0xf3
0x2fc4318	15de4197	bl 0x3bb6c
0x2fc431c	e9234ea9	ldp x9, x8, [sp, #0xe0]
0x2fc4320	e92300a9	stp x9, x8, [sp]
0x2fc4324	880000b4	cbz x8, 0x2fc4334
0x2fc4328	08410091	add x8, x8, #0x10
0x2fc432c	29008052	mov w9, #0x1
0x2fc4330	080129f8	ldadd x9, x8, [x8]
0x2fc4334	f6030091	mov x22, sp
0x2fc4338	e89fc439	ldrsb w8, [sp, #0x127]
0x2fc433c	e801f837	tbnz w8, #0x1f, 0x2fc4378
0x2fc4340	e047c03d	ldr q0, [sp, #0x110]
0x2fc4344	c002813c	stur q0, [x22, #0x10]
0x2fc4348	e89340f9	ldr x8, [sp, #0x120]
0x2fc434c	c80202f8	stur x8, [x22, #0x20]
0x2fc4350	0d000014	b 0x2fc4384
0x2fc4354	680240f9	ldr x8, [x19]
0x2fc4358	080940f9	ldr x8, [x8, #0x10]
0x2fc435c	e00313aa	mov x0, x19
0x2fc4360	00013fd6	blr x8
0x2fc4364	e00313aa	mov x0, x19
0x2fc4368	2dee0595	bl 0x713fc1c
0x2fc436c	e83fca39	ldrsb w8, [sp, #0x28f]
0x2fc4370	e8e5ff36	tbz w8, #0x1f, 0x2fc402c
0x2fc4374	21ffff17	b 0x2fc3ff8
0x2fc4378	e10b51a9	ldp x1, x2, [sp, #0x110]
0x2fc437c	c0420091	add x0, x22, #0x10
0x2fc4380	68524197	bl 0x18d20
0x2fc4384	fa030091	mov x26, sp
0x2fc4388	e81fc439	ldrsb w8, [sp, #0x107]
0x2fc438c	c800f837	tbnz w8, #0x1f, 0x2fc43a4
0x2fc4390	e03fc03d	ldr q0, [sp, #0xf0]
0x2fc4394	4083823c	stur q0, [x26, #0x28]
0x2fc4398	e88340f9	ldr x8, [sp, #0x100]
0x2fc439c	488303f8	stur x8, [x26, #0x38]
0x2fc43a0	04000014	b 0x2fc43b0
0x2fc43a4	e10b4fa9	ldp x1, x2, [sp, #0xf0]
0x2fc43a8	40a30091	add x0, x26, #0x28
0x2fc43ac	5d524197	bl 0x18d20
0x2fc43b0	fb030091	mov x27, sp
0x2fc43b4	60030191	add x0, x27, #0x40
0x2fc43b8	e10315aa	mov x1, x21
0x2fc43bc	169f0094	bl 0x2fec014
0x2fc43c0	350740f9	ldr x21, [x25, #0x8]
0x2fc43c4	e8a30491	add x8, sp, #0x128
0x2fc43c8	e0c30291	add x0, sp, #0xb0
0x2fc43cc	cde45594	bl 0x453d700
0x2fc43d0	e8ffc439	ldrsb w8, [sp, #0x13f]
0x2fc43d4	c800f837	tbnz w8, #0x1f, 0x2fc43ec
0x2fc43d8	e002c03d	ldr q0, [x23]
0x2fc43dc	e053803d	str q0, [sp, #0x140]
0x2fc43e0	e89f40f9	ldr x8, [sp, #0x138]
0x2fc43e4	e8ab00f9	str x8, [sp, #0x150]
0x2fc43e8	04000014	b 0x2fc43f8
0x2fc43ec	e18b52a9	ldp x1, x2, [sp, #0x128]
0x2fc43f0	e0030591	add x0, sp, #0x140
0x2fc43f4	4b524197	bl 0x18d20
0x2fc43f8	e003679e	fmov d0, xzr
0x2fc43fc	ffb700f9	str xzr, [sp, #0x168]
0x2fc4400	0004186e	mov.d v0[1], v0[0]
0x2fc4404	e002833c	stur q0, [x23, #0x30]
0x2fc4408	e0e5002f	movi d0, #0x000000ffffffff
0x2fc440c	0040611e	fneg d0, d0
0x2fc4410	e0bb00fd	str d0, [sp, #0x170]
0x2fc4414	e8030591	add x8, sp, #0x140
0x2fc4418	f9c30991	add x25, sp, #0x270
0x2fc441c	e003c03d	ldr q0, [sp]
0x2fc4420	0083803c	stur q0, [x24, #0x8]
0x2fc4424	ff7f00a9	stp xzr, xzr, [sp]
0x2fc4428	c002c13c	ldur q0, [x22, #0x10]
0x2fc442c	0083813c	stur q0, [x24, #0x18]
0x2fc4430	c90242f8	ldur x9, [x22, #0x20]
0x2fc4434	e83b01f9	str x8, [sp, #0x270]
0x2fc4438	e94f01f9	str x9, [sp, #0x298]
0x2fc443c	df7e01a9	stp xzr, xzr, [x22, #0x10]
0x2fc4440	df0202f8	stur xzr, [x22, #0x20]
0x2fc4444	4083c23c	ldur q0, [x26, #0x28]
0x2fc4448	e0ab803d	str q0, [sp, #0x2a0]
0x2fc444c	488343f8	ldur x8, [x26, #0x38]
0x2fc4450	e85b01f9	str x8, [sp, #0x2b0]
0x2fc4454	5f7f03a9	stp xzr, xzr, [x26, #0x30]
0x2fc4458	5f8302f8	stur xzr, [x26, #0x28]
0x2fc445c	20230191	add x0, x25, #0x48
0x2fc4460	61030191	add x1, x27, #0x40
0x2fc4464	ec9e0094	bl 0x2fec014
0x2fc4468	f59701f9	str x21, [sp, #0x328]
0x2fc446c	e8f301b2	mov x8, #-0x5555555555555556
0x2fc4470	e82319a9	stp x8, x8, [sp, #0x190]
0x2fc4474	e8430691	add x8, sp, #0x190
0x2fc4478	e0830691	add x0, sp, #0x1a0
0x2fc447c	9dadc897	bl 0x21efaf0
0x2fc4480	fb6b59a9	ldp x27, x26, [sp, #0x190]
0x2fc4484	fb6b18a9	stp x27, x26, [sp, #0x180]
0x2fc4488	9a0000b4	cbz x26, 0x2fc4498
0x2fc448c	48230091	add x8, x26, #0x8
0x2fc4490	29008052	mov w9, #0x1
0x2fc4494	080129f8	ldadd x9, x8, [x8]
0x2fc4498	e8f301b2	mov x8, #-0x5555555555555556
0x2fc449c	e83701f9	str x8, [sp, #0x268]
0x2fc44a0	e83301f9	str x8, [sp, #0x260]
0x2fc44a4	f59741f9	ldr x21, [sp, #0x328]
0x2fc44a8	f63b41f9	ldr x22, [sp, #0x270]
0x2fc44ac	0083c03c	ldur q0, [x24, #0x8]
0x2fc44b0	3fff00a9	stp xzr, xzr, [x25, #0x8]
0x2fc44b4	f8830691	add x24, sp, #0x1a0
0x2fc44b8	2183c13c	ldur q1, [x25, #0x18]
0x2fc44bc	e0070dad	stp q0, q1, [sp, #0x1a0]
0x2fc44c0	288342f8	ldur x8, [x25, #0x28]
0x2fc44c4	3fff01a9	stp xzr, xzr, [x25, #0x18]
0x2fc44c8	2003c33c	ldur q0, [x25, #0x30]
0x2fc44cc	290344f8	ldur x9, [x25, #0x40]
0x2fc44d0	e8e300f9	str x8, [sp, #0x1c0]
0x2fc44d4	e9ef00f9	str x9, [sp, #0x1d8]
0x2fc44d8	e0028a3c	stur q0, [x23, #0xa0]
0x2fc44dc	3fff02a9	stp xzr, xzr, [x25, #0x28]
0x2fc44e0	3fff03a9	stp xzr, xzr, [x25, #0x38]
0x2fc44e4	00030191	add x0, x24, #0x40
0x2fc44e8	21230191	add x1, x25, #0x48
0x2fc44ec	ca9e0094	bl 0x2fec014
0x2fc44f0	fb2b01f9	str x27, [sp, #0x250]
0x2fc44f4	fa2f01f9	str x26, [sp, #0x258]
0x2fc44f8	9a0000b4	cbz x26, 0x2fc4508
0x2fc44fc	48230091	add x8, x26, #0x8
0x2fc4500	29008052	mov w9, #0x1
0x2fc4504	080129f8	ldadd x9, x8, [x8]
0x2fc4508	bf0318f8	stur xzr, [x29, #-0x80]
0x2fc450c	00198052	mov w0, #0xc8
0x2fc4510	c8ee0595	bl 0x7140030
0x2fc4514	f70300aa	mov x23, x0
0x2fc4518	e8700390	adrp x8, 0x9de0000
0x2fc451c	08012c91	add x8, x8, #0xb00
0x2fc4520	080000f9	str x8, [x0]
0x2fc4524	e06bc03d	ldr q0, [sp, #0x1a0]
0x2fc4528	0080803c	stur q0, [x0, #0x8]
0x2fc452c	ff7f1aa9	stp xzr, xzr, [sp, #0x1a0]
0x2fc4530	0003c13c	ldur q0, [x24, #0x10]
0x2fc4534	0080813c	stur q0, [x0, #0x18]
0x2fc4538	080342f8	ldur x8, [x24, #0x20]
0x2fc453c	081400f9	str x8, [x0, #0x28]
0x2fc4540	1f7f01a9	stp xzr, xzr, [x24, #0x10]
0x2fc4544	0083c23c	ldur q0, [x24, #0x28]
0x2fc4548	000c803d	str q0, [x0, #0x30]
0x2fc454c	088343f8	ldur x8, [x24, #0x38]
0x2fc4550	082000f9	str x8, [x0, #0x40]
0x2fc4554	1f7f02a9	stp xzr, xzr, [x24, #0x20]
0x2fc4558	1f7f03a9	stp xzr, xzr, [x24, #0x30]
0x2fc455c	00200191	add x0, x0, #0x48
0x2fc4560	01030191	add x1, x24, #0x40
0x2fc4564	ac9e0094	bl 0x2fec014
0x2fc4568	e92b41f9	ldr x9, [sp, #0x250]
0x2fc456c	e82f41f9	ldr x8, [sp, #0x258]
0x2fc4570	e9a20ba9	stp x9, x8, [x23, #0xb8]
0x2fc4574	880000b4	cbz x8, 0x2fc4584
0x2fc4578	08210091	add x8, x8, #0x8
0x2fc457c	29008052	mov w9, #0x1
0x2fc4580	080129f8	ldadd x9, x8, [x8]
0x2fc4584	b70318f8	stur x23, [x29, #-0x80]
0x2fc4588	b76302d1	sub x23, x29, #0x98
0x2fc458c	e8830991	add x8, sp, #0x260
0x2fc4590	a26302d1	sub x2, x29, #0x98
0x2fc4594	e00315aa	mov x0, x21
0x2fc4598	e10316aa	mov x1, x22
0x2fc459c	7c01db94	bl 0x6684b8c
0x2fc45a0	a00358f8	ldur x0, [x29, #-0x80]
0x2fc45a4	1f0017eb	cmp x0, x23
0x2fc45a8	a0000054	b.eq 0x2fc45bc
0x2fc45ac	e00000b4	cbz x0, 0x2fc45c8
0x2fc45b0	080040f9	ldr x8, [x0]
0x2fc45b4	081540f9	ldr x8, [x8, #0x28]
0x2fc45b8	03000014	b 0x2fc45c4
0x2fc45bc	080040f9	ldr x8, [x0]
0x2fc45c0	081140f9	ldr x8, [x8, #0x20]
0x2fc45c4	00013fd6	blr x8
0x2fc45c8	f52f41f9	ldr x21, [sp, #0x258]
0x2fc45cc	750100b4	cbz x21, 0x2fc45f8
0x2fc45d0	a8220091	add x8, x21, #0x8
0x2fc45d4	09008092	mov x9, #-0x1
0x2fc45d8	0801e9f8	ldaddal x9, x8, [x8]
0x2fc45dc	e80000b5	cbnz x8, 0x2fc45f8
0x2fc45e0	a80240f9	ldr x8, [x21]
0x2fc45e4	080940f9	ldr x8, [x8, #0x10]
0x2fc45e8	e00315aa	mov x0, x21
0x2fc45ec	00013fd6	blr x8
0x2fc45f0	e00315aa	mov x0, x21
0x2fc45f4	8aed0595	bl 0x713fc1c
0x2fc45f8	e0830691	add x0, sp, #0x1a0
0x2fc45fc	72050094	bl 0x2fc5bc4
0x2fc4600	e83341f9	ldr x8, [sp, #0x260]
0x2fc4604	f53741f9	ldr x21, [sp, #0x268]
0x2fc4608	b50000b4	cbz x21, 0x2fc461c
0x2fc460c	a9420091	add x9, x21, #0x10
0x2fc4610	2a008052	mov w10, #0x1
0x2fc4614	2b012af8	ldadd x10, x11, [x9]
0x2fc4618	29012af8	ldadd x10, x9, [x9]
0x2fc461c	e9700390	adrp x9, 0x9de0000
0x2fc4620	29013091	add x9, x9, #0xc00
0x2fc4624	e0c340f9	ldr x0, [sp, #0x180]
0x2fc4628	a9a338a9	stp x9, x8, [x29, #-0x78]
0x2fc462c	b6e301d1	sub x22, x29, #0x78
0x2fc4630	b5db39a9	stp x21, x22, [x29, #-0x68]
0x2fc4634	a1e301d1	sub x1, x29, #0x78
0x2fc4638	8391da94	bl 0x6668c44
0x2fc463c	a0035af8	ldur x0, [x29, #-0x60]
0x2fc4640	1f0016eb	cmp x0, x22
0x2fc4644	a0000054	b.eq 0x2fc4658
0x2fc4648	e00000b4	cbz x0, 0x2fc4664
0x2fc464c	080040f9	ldr x8, [x0]
0x2fc4650	081540f9	ldr x8, [x8, #0x28]
0x2fc4654	03000014	b 0x2fc4660
0x2fc4658	080040f9	ldr x8, [x0]
0x2fc465c	081140f9	ldr x8, [x8, #0x20]
0x2fc4660	00013fd6	blr x8
0x2fc4664	750000b4	cbz x21, 0x2fc4670
0x2fc4668	e00315aa	mov x0, x21
0x2fc466c	6ced0595	bl 0x713fc1c
0x2fc4670	f53741f9	ldr x21, [sp, #0x268]
0x2fc4674	750100b4	cbz x21, 0x2fc46a0
0x2fc4678	a8220091	add x8, x21, #0x8
0x2fc467c	09008092	mov x9, #-0x1
0x2fc4680	0801e9f8	ldaddal x9, x8, [x8]
0x2fc4684	e80000b5	cbnz x8, 0x2fc46a0
0x2fc4688	a80240f9	ldr x8, [x21]
0x2fc468c	080940f9	ldr x8, [x8, #0x10]
0x2fc4690	e00315aa	mov x0, x21
0x2fc4694	00013fd6	blr x8
0x2fc4698	e00315aa	mov x0, x21
0x2fc469c	60ed0595	bl 0x713fc1c
0x2fc46a0	f5c740f9	ldr x21, [sp, #0x188]
0x2fc46a4	750100b4	cbz x21, 0x2fc46d0
0x2fc46a8	a8220091	add x8, x21, #0x8
0x2fc46ac	09008092	mov x9, #-0x1
0x2fc46b0	0801e9f8	ldaddal x9, x8, [x8]
0x2fc46b4	e80000b5	cbnz x8, 0x2fc46d0
0x2fc46b8	a80240f9	ldr x8, [x21]
0x2fc46bc	080940f9	ldr x8, [x8, #0x10]
0x2fc46c0	e00315aa	mov x0, x21
0x2fc46c4	00013fd6	blr x8
0x2fc46c8	e00315aa	mov x0, x21
0x2fc46cc	54ed0595	bl 0x713fc1c
0x2fc46d0	f75759a9	ldp x23, x21, [sp, #0x190]
0x2fc46d4	150200b4	cbz x21, 0x2fc4714
0x2fc46d8	a8220091	add x8, x21, #0x8
0x2fc46dc	29008052	mov w9, #0x1
0x2fc46e0	080129f8	ldadd x9, x8, [x8]
0x2fc46e4	f6cf40f9	ldr x22, [sp, #0x198]
0x2fc46e8	760100b4	cbz x22, 0x2fc4714
0x2fc46ec	c8220091	add x8, x22, #0x8
0x2fc46f0	09008092	mov x9, #-0x1
0x2fc46f4	0801e9f8	ldaddal x9, x8, [x8]
0x2fc46f8	e80000b5	cbnz x8, 0x2fc4714
0x2fc46fc	c80240f9	ldr x8, [x22]
0x2fc4700	080940f9	ldr x8, [x8, #0x10]
0x2fc4704	e00316aa	mov x0, x22
0x2fc4708	00013fd6	blr x8
0x2fc470c	e00316aa	mov x0, x22
0x2fc4710	43ed0595	bl 0x713fc1c
0x2fc4714	20230091	add x0, x25, #0x8
0x2fc4718	2b050094	bl 0x2fc5bc4
0x2fc471c	e85fc539	ldrsb w8, [sp, #0x157]
0x2fc4720	a800f836	tbz w8, #0x1f, 0x2fc4734
0x2fc4724	e0a340f9	ldr x0, [sp, #0x140]
0x2fc4728	e8ab40f9	ldr x8, [sp, #0x150]
0x2fc472c	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4730	37ee0595	bl 0x714000c
0x2fc4734	e8ffc439	ldrsb w8, [sp, #0x13f]
0x2fc4738	a800f836	tbz w8, #0x1f, 0x2fc474c
0x2fc473c	e09740f9	ldr x0, [sp, #0x128]
0x2fc4740	e89f40f9	ldr x8, [sp, #0x138]
0x2fc4744	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4748	31ee0595	bl 0x714000c
0x2fc474c	88824439	ldrb w8, [x20, #0x120]
0x2fc4750	1f050071	cmp w8, #0x1
0x2fc4754	61020054	b.ne 0x2fc47a0
0x2fc4758	950000b4	cbz x21, 0x2fc4768
0x2fc475c	a8220091	add x8, x21, #0x8
0x2fc4760	29008052	mov w9, #0x1
0x2fc4764	080129f8	ldadd x9, x8, [x8]
0x2fc4768	968e40f9	ldr x22, [x20, #0x118]
0x2fc476c	975611a9	stp x23, x21, [x20, #0x110]
0x2fc4770	760200b4	cbz x22, 0x2fc47bc
0x2fc4774	c8220091	add x8, x22, #0x8
0x2fc4778	09008092	mov x9, #-0x1
0x2fc477c	0801e9f8	ldaddal x9, x8, [x8]
0x2fc4780	e80100b5	cbnz x8, 0x2fc47bc
0x2fc4784	c80240f9	ldr x8, [x22]
0x2fc4788	080940f9	ldr x8, [x8, #0x10]
0x2fc478c	e00316aa	mov x0, x22
0x2fc4790	00013fd6	blr x8
0x2fc4794	e00316aa	mov x0, x22
0x2fc4798	21ed0595	bl 0x713fc1c
0x2fc479c	08000014	b 0x2fc47bc
0x2fc47a0	975611a9	stp x23, x21, [x20, #0x110]
0x2fc47a4	950000b4	cbz x21, 0x2fc47b4
0x2fc47a8	a8220091	add x8, x21, #0x8
0x2fc47ac	29008052	mov w9, #0x1
0x2fc47b0	080129f8	ldadd x9, x8, [x8]
0x2fc47b4	28008052	mov w8, #0x1
0x2fc47b8	88820439	strb w8, [x20, #0x120]
0x2fc47bc	750100b4	cbz x21, 0x2fc47e8
0x2fc47c0	a8220091	add x8, x21, #0x8
0x2fc47c4	09008092	mov x9, #-0x1
0x2fc47c8	0801e9f8	ldaddal x9, x8, [x8]
0x2fc47cc	e80000b5	cbnz x8, 0x2fc47e8
0x2fc47d0	a80240f9	ldr x8, [x21]
0x2fc47d4	080940f9	ldr x8, [x8, #0x10]
0x2fc47d8	e00315aa	mov x0, x21
0x2fc47dc	00013fd6	blr x8
0x2fc47e0	e00315aa	mov x0, x21
0x2fc47e4	0eed0595	bl 0x713fc1c
0x2fc47e8	e0030091	mov x0, sp
0x2fc47ec	f6040094	bl 0x2fc5bc4
0x2fc47f0	f56f40f9	ldr x21, [sp, #0xd8]
0x2fc47f4	750100b4	cbz x21, 0x2fc4820
0x2fc47f8	a8220091	add x8, x21, #0x8
0x2fc47fc	09008092	mov x9, #-0x1
0x2fc4800	0801e9f8	ldaddal x9, x8, [x8]
0x2fc4804	e80000b5	cbnz x8, 0x2fc4820
0x2fc4808	a80240f9	ldr x8, [x21]
0x2fc480c	080940f9	ldr x8, [x8, #0x10]
0x2fc4810	e00315aa	mov x0, x21
0x2fc4814	00013fd6	blr x8
0x2fc4818	e00315aa	mov x0, x21
0x2fc481c	00ed0595	bl 0x713fc1c
0x2fc4820	e07740f9	ldr x0, [sp, #0xe8]
0x2fc4824	400000b4	cbz x0, 0x2fc482c
0x2fc4828	fdec0595	bl 0x713fc1c
0x2fc482c	c8c60290	adrp x8, 0x889c000
0x2fc4830	08a12891	add x8, x8, #0xa28
0x2fc4834	000542ad	ldp q0, q1, [x8, #0x40]
0x2fc4838	600602ad	stp q0, q1, [x19, #0x40]
0x2fc483c	0019c03d	ldr q0, [x8, #0x60]
0x2fc4840	601a803d	str q0, [x19, #0x60]
0x2fc4844	000540ad	ldp q0, q1, [x8]
0x2fc4848	600600ad	stp q0, q1, [x19]
0x2fc484c	010141ad	ldp q1, q0, [x8, #0x20]
0x2fc4850	610201ad	stp q1, q0, [x19, #0x20]
0x2fc4854	892251a9	ldp x9, x8, [x20, #0x110]
0x2fc4858	e9231aa9	stp x9, x8, [sp, #0x1a0]
0x2fc485c	880000b4	cbz x8, 0x2fc486c
0x2fc4860	08210091	add x8, x8, #0x8
0x2fc4864	29008052	mov w9, #0x1
0x2fc4868	080129f8	ldadd x9, x8, [x8]
0x2fc486c	ffdb00f9	str xzr, [sp, #0x1b0]
0x2fc4870	e0830691	add x0, sp, #0x1a0
0x2fc4874	a203db94	bl 0x66856fc
0x2fc4878	e0830691	add x0, sp, #0x1a0
0x2fc487c	3d9e0094	bl 0x2fec170
0x2fc4880	f50300aa	mov x21, x0
0x2fc4884	f6d740f9	ldr x22, [sp, #0x1a8]
0x2fc4888	760100b4	cbz x22, 0x2fc48b4
0x2fc488c	c8220091	add x8, x22, #0x8
0x2fc4890	09008092	mov x9, #-0x1
0x2fc4894	0801e9f8	ldaddal x9, x8, [x8]
0x2fc4898	e80000b5	cbnz x8, 0x2fc48b4
0x2fc489c	c80240f9	ldr x8, [x22]
0x2fc48a0	080940f9	ldr x8, [x8, #0x10]
0x2fc48a4	e00316aa	mov x0, x22
0x2fc48a8	00013fd6	blr x8
0x2fc48ac	e00316aa	mov x0, x22
0x2fc48b0	dbec0595	bl 0x713fc1c
0x2fc48b4	e00313aa	mov x0, x19
0x2fc48b8	e10315aa	mov x1, x21
0x2fc48bc	549e0094	bl 0x2fec20c
0x2fc48c0	40008052	mov w0, #0x2
0x2fc48c4	2d64b994	bl 0x5e1d978
0x2fc48c8	600b0034	cbz w0, 0x2fc4a34
0x2fc48cc	f5030091	mov x21, sp
0x2fc48d0	e8030091	mov x8, sp
0x2fc48d4	daf26294	bl 0x488143c
0x2fc48d8	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc48dc	e90340f9	ldr x9, [sp]
0x2fc48e0	1f010071	cmp w8, #0x0
0x2fc48e4	22b1959a	csel x2, x9, x21, lt
0x2fc48e8	68a003d0	adrp x8, 0xa3d2000
0x2fc48ec	09854d39	ldrb w9, [x8, #0x361]
0x2fc48f0	29010037	tbnz w9, #0x0, 0x2fc4914
0x2fc48f4	c9c60290	adrp x9, 0x889c000
0x2fc48f8	2011c03d	ldr q0, [x9, #0x40]
0x2fc48fc	69a003d0	adrp x9, 0xa3d2000
0x2fc4900	29410d91	add x9, x9, #0x350
0x2fc4904	2001803d	str q0, [x9]
0x2fc4908	3f410039	strb wzr, [x9, #0x10]
0x2fc490c	29008052	mov w9, #0x1
0x2fc4910	09850d39	strb w9, [x8, #0x361]
0x2fc4914	68a003d0	adrp x8, 0xa3d2000
0x2fc4918	09f95039	ldrb w9, [x8, #0x43e]
0x2fc491c	a9010037	tbnz w9, #0x0, 0x2fc4950
0x2fc4920	29a602f0	adrp x9, 0x848b000
0x2fc4924	202945fd	ldr d0, [x9, #0xa50]
0x2fc4928	69a003d0	adrp x9, 0xa3d2000
0x2fc492c	29c11091	add x9, x9, #0x430
0x2fc4930	200100fd	str d0, [x9]
0x2fc4934	4aaf02f0	adrp x10, 0x85af000
0x2fc4938	409547fd	ldr d0, [x10, #0xf28]
0x2fc493c	200900bd	str s0, [x9, #0x8]
0x2fc4940	ca0d8052	mov w10, #0x6e
0x2fc4944	2a190079	strh w10, [x9, #0xc]
0x2fc4948	29008052	mov w9, #0x1
0x2fc494c	09f91039	strb w9, [x8, #0x43e]
0x2fc4950	63a003d0	adrp x3, 0xa3d2000
0x2fc4954	63400d91	add x3, x3, #0x350
0x2fc4958	64a003d0	adrp x4, 0xa3d2000
0x2fc495c	84c01091	add x4, x4, #0x430
0x2fc4960	e0830691	add x0, sp, #0x1a0
0x2fc4964	41008052	mov w1, #0x2
0x2fc4968	45278052	mov w5, #0x13a
0x2fc496c	06008052	mov w6, #0x0
0x2fc4970	070080d2	mov x7, #0x0
0x2fc4974	b761b994	bl 0x5e1d050
0x2fc4978	68a003d0	adrp x8, 0xa3d2000
0x2fc497c	09955539	ldrb w9, [x8, #0x565]
0x2fc4980	69030037	tbnz w9, #0x0, 0x2fc49ec
0x2fc4984	c9c60290	adrp x9, 0x889c000
0x2fc4988	202541fd	ldr d0, [x9, #0x248]
0x2fc498c	a9a80290	adrp x9, 0x84d8000
0x2fc4990	211943fd	ldr d1, [x9, #0x630]
0x2fc4994	20040c6e	mov.s v0[1], v1[0]
0x2fc4998	c9c60290	adrp x9, 0x889c000
0x2fc499c	213541fd	ldr d1, [x9, #0x268]
0x2fc49a0	2004146e	mov.s v0[2], v1[0]
0x2fc49a4	e9c102b0	adrp x9, 0x8801000
0x2fc49a8	213940fd	ldr d1, [x9, #0x70]
0x2fc49ac	20041c6e	mov.s v0[3], v1[0]
0x2fc49b0	69a003d0	adrp x9, 0xa3d2000
0x2fc49b4	29211591	add x9, x9, #0x548
0x2fc49b8	2001803d	str q0, [x9]
0x2fc49bc	0ab902f0	adrp x10, 0x86e7000
0x2fc49c0	40a944fd	ldr d0, [x10, #0x950]
0x2fc49c4	aab802f0	adrp x10, 0x86db000
0x2fc49c8	416942fd	ldr d1, [x10, #0x4d0]
0x2fc49cc	20040c6e	mov.s v0[1], v1[0]
0x2fc49d0	200900fd	str d0, [x9, #0x10]
0x2fc49d4	cac60290	adrp x10, 0x889c000
0x2fc49d8	403941fd	ldr d0, [x10, #0x270]
0x2fc49dc	201900bd	str s0, [x9, #0x18]
0x2fc49e0	3f710039	strb wzr, [x9, #0x1c]
0x2fc49e4	29008052	mov w9, #0x1
0x2fc49e8	09951539	strb w9, [x8, #0x565]
0x2fc49ec	00e4006f	movi.2d v0, #0000000000000000
0x2fc49f0	e08316ad	stp q0, q0, [sp, #0x2d0]
0x2fc49f4	e08315ad	stp q0, q0, [sp, #0x2b0]
0x2fc49f8	e08314ad	stp q0, q0, [sp, #0x290]
0x2fc49fc	e08313ad	stp q0, q0, [sp, #0x270]
0x2fc4a00	61a003d0	adrp x1, 0xa3d2000
0x2fc4a04	21201591	add x1, x1, #0x548
0x2fc4a08	e0830691	add x0, sp, #0x1a0
0x2fc4a0c	e2c30991	add x2, sp, #0x270
0x2fc4a10	4362b994	bl 0x5e1d31c
0x2fc4a14	e0830691	add x0, sp, #0x1a0
0x2fc4a18	e161b994	bl 0x5e1d19c
0x2fc4a1c	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc4a20	a800f836	tbz w8, #0x1f, 0x2fc4a34
0x2fc4a24	e00340f9	ldr x0, [sp]
0x2fc4a28	e80b40f9	ldr x8, [sp, #0x10]
0x2fc4a2c	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4a30	77ed0595	bl 0x714000c
0x2fc4a34	88824439	ldrb w8, [x20, #0x120]
0x2fc4a38	1f050071	cmp w8, #0x1
0x2fc4a3c	81afff54	b.ne 0x2fc402c
0x2fc4a40	938e40f9	ldr x19, [x20, #0x118]
0x2fc4a44	730100b4	cbz x19, 0x2fc4a70
0x2fc4a48	68220091	add x8, x19, #0x8
0x2fc4a4c	09008092	mov x9, #-0x1
0x2fc4a50	0801e9f8	ldaddal x9, x8, [x8]
0x2fc4a54	e80000b5	cbnz x8, 0x2fc4a70
0x2fc4a58	680240f9	ldr x8, [x19]
0x2fc4a5c	080940f9	ldr x8, [x8, #0x10]
0x2fc4a60	e00313aa	mov x0, x19
0x2fc4a64	00013fd6	blr x8
0x2fc4a68	e00313aa	mov x0, x19
0x2fc4a6c	6cec0595	bl 0x713fc1c
0x2fc4a70	9f820439	strb wzr, [x20, #0x120]
0x2fc4a74	6efdff17	b 0x2fc402c
0x2fc4a78	cbed0595	bl 0x71401a4
0x2fc4a7c	e0830691	add x0, sp, #0x1a0
0x2fc4a80	c7504197	bl 0x18d9c
0x2fc4a84	200020d4	brk #0x1
0x2fc4a88	f40300aa	mov x20, x0
0x2fc4a8c	e8ffc439	ldrsb w8, [sp, #0x13f]
0x2fc4a90	6809f837	tbnz w8, #0x1f, 0x2fc4bbc
0x2fc4a94	7e000014	b 0x2fc4c8c
0x2fc4a98	f40300aa	mov x20, x0
0x2fc4a9c	e89fc039	ldrsb w8, [sp, #0x27]
0x2fc4aa0	8811f836	tbz w8, #0x1f, 0x2fc4cd0
0x2fc4aa4	90000014	b 0x2fc4ce4
0x2fc4aa8	f40300aa	mov x20, x0
0x2fc4aac	e00740f9	ldr x0, [sp, #0x8]
0x2fc4ab0	200f00b4	cbz x0, 0x2fc4c94
0x2fc4ab4	92000014	b 0x2fc4cfc
0x2fc4ab8	f40300aa	mov x20, x0
0x2fc4abc	a0035af8	ldur x0, [x29, #-0x60]
0x2fc4ac0	1f0016eb	cmp x0, x22
0x2fc4ac4	00010054	b.eq 0x2fc4ae4
0x2fc4ac8	5d3a0495	bl 0x70d343c
0x2fc4acc	750000b4	cbz x21, 0x2fc4ad8
0x2fc4ad0	e00315aa	mov x0, x21
0x2fc4ad4	52ec0595	bl 0x713fc1c
0x2fc4ad8	e0830991	add x0, sp, #0x260
0x2fc4adc	711dc797	bl 0x218c0a0
0x2fc4ae0	26000014	b 0x2fc4b78
0x2fc4ae4	080040f9	ldr x8, [x0]
0x2fc4ae8	081140f9	ldr x8, [x8, #0x20]
0x2fc4aec	00013fd6	blr x8
0x2fc4af0	15ffffb5	cbnz x21, 0x2fc4ad0
0x2fc4af4	f9ffff17	b 0x2fc4ad8
0x2fc4af8	f40300aa	mov x20, x0
0x2fc4afc	a00358f8	ldur x0, [x29, #-0x80]
0x2fc4b00	1f0017eb	cmp x0, x23
0x2fc4b04	81000054	b.ne 0x2fc4b14
0x2fc4b08	080040f9	ldr x8, [x0]
0x2fc4b0c	081140f9	ldr x8, [x8, #0x20]
0x2fc4b10	04000014	b 0x2fc4b20
0x2fc4b14	e00200b4	cbz x0, 0x2fc4b70
0x2fc4b18	080040f9	ldr x8, [x0]
0x2fc4b1c	081540f9	ldr x8, [x8, #0x28]
0x2fc4b20	00013fd6	blr x8
0x2fc4b24	13000014	b 0x2fc4b70
0x2fc4b28	f30301aa	mov x19, x1
0x2fc4b2c	f40300aa	mov x20, x0
0x2fc4b30	e81ec139	ldrsb w8, [x23, #0x47]
0x2fc4b34	a800f836	tbz w8, #0x1f, 0x2fc4b48
0x2fc4b38	e01a40f9	ldr x0, [x23, #0x30]
0x2fc4b3c	e82240f9	ldr x8, [x23, #0x40]
0x2fc4b40	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4b44	32ed0595	bl 0x714000c
0x2fc4b48	e1620091	add x1, x23, #0x18
0x2fc4b4c	e2420091	add x2, x23, #0x10
0x2fc4b50	a5e301d1	sub x5, x29, #0x78
0x2fc4b54	e00317aa	mov x0, x23
0x2fc4b58	e30314aa	mov x3, x20
0x2fc4b5c	e40313aa	mov x4, x19
0x2fc4b60	163e0595	bl 0x71143b8
0x2fc4b64	b48358f8	ldur x20, [x29, #-0x78]
0x2fc4b68	02000014	b 0x2fc4b70
0x2fc4b6c	f40300aa	mov x20, x0
0x2fc4b70	e0830691	add x0, sp, #0x1a0
0x2fc4b74	e6960094	bl 0x2fea70c
0x2fc4b78	e0030691	add x0, sp, #0x180
0x2fc4b7c	fb944597	bl 0x129f68
0x2fc4b80	e0430691	add x0, sp, #0x190
0x2fc4b84	f9944597	bl 0x129f68
0x2fc4b88	20230091	add x0, x25, #0x8
0x2fc4b8c	0e040094	bl 0x2fc5bc4
0x2fc4b90	e85fc539	ldrsb w8, [sp, #0x157]
0x2fc4b94	0801f836	tbz w8, #0x1f, 0x2fc4bb4
0x2fc4b98	e0a340f9	ldr x0, [sp, #0x140]
0x2fc4b9c	e8ab40f9	ldr x8, [sp, #0x150]
0x2fc4ba0	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4ba4	1aed0595	bl 0x714000c
0x2fc4ba8	e8ffc439	ldrsb w8, [sp, #0x13f]
0x2fc4bac	0807f836	tbz w8, #0x1f, 0x2fc4c8c
0x2fc4bb0	03000014	b 0x2fc4bbc
0x2fc4bb4	e8ffc439	ldrsb w8, [sp, #0x13f]
0x2fc4bb8	a806f836	tbz w8, #0x1f, 0x2fc4c8c
0x2fc4bbc	e09740f9	ldr x0, [sp, #0x128]
0x2fc4bc0	e89f40f9	ldr x8, [sp, #0x138]
0x2fc4bc4	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4bc8	11ed0595	bl 0x714000c
0x2fc4bcc	30000014	b 0x2fc4c8c
0x2fc4bd0	f40300aa	mov x20, x0
0x2fc4bd4	e87fc739	ldrsb w8, [sp, #0x1df]
0x2fc4bd8	4801f836	tbz w8, #0x1f, 0x2fc4c00
0x2fc4bdc	e0e740f9	ldr x0, [sp, #0x1c8]
0x2fc4be0	e8ef40f9	ldr x8, [sp, #0x1d8]
0x2fc4be4	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4be8	09ed0595	bl 0x714000c
0x2fc4bec	e81fc739	ldrsb w8, [sp, #0x1c7]
0x2fc4bf0	c800f837	tbnz w8, #0x1f, 0x2fc4c08
0x2fc4bf4	e0d740f9	ldr x0, [sp, #0x1a8]
0x2fc4bf8	00fcffb4	cbz x0, 0x2fc4b78
0x2fc4bfc	09000014	b 0x2fc4c20
0x2fc4c00	e81fc739	ldrsb w8, [sp, #0x1c7]
0x2fc4c04	88ffff36	tbz w8, #0x1f, 0x2fc4bf4
0x2fc4c08	e0db40f9	ldr x0, [sp, #0x1b0]
0x2fc4c0c	e8e340f9	ldr x8, [sp, #0x1c0]
0x2fc4c10	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4c14	feec0595	bl 0x714000c
0x2fc4c18	e0d740f9	ldr x0, [sp, #0x1a8]
0x2fc4c1c	e0faffb4	cbz x0, 0x2fc4b78
0x2fc4c20	ffeb0595	bl 0x713fc1c
0x2fc4c24	d5ffff17	b 0x2fc4b78
0x2fc4c28	f40300aa	mov x20, x0
0x2fc4c2c	d7ffff17	b 0x2fc4b88
0x2fc4c30	f40300aa	mov x20, x0
0x2fc4c34	e8dfca39	ldrsb w8, [sp, #0x2b7]
0x2fc4c38	4801f836	tbz w8, #0x1f, 0x2fc4c60
0x2fc4c3c	e05341f9	ldr x0, [sp, #0x2a0]
0x2fc4c40	e85b41f9	ldr x8, [sp, #0x2b0]
0x2fc4c44	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4c48	f1ec0595	bl 0x714000c
0x2fc4c4c	e87fca39	ldrsb w8, [sp, #0x29f]
0x2fc4c50	c800f837	tbnz w8, #0x1f, 0x2fc4c68
0x2fc4c54	e04341f9	ldr x0, [sp, #0x280]
0x2fc4c58	c0f9ffb4	cbz x0, 0x2fc4b90
0x2fc4c5c	09000014	b 0x2fc4c80
0x2fc4c60	e87fca39	ldrsb w8, [sp, #0x29f]
0x2fc4c64	88ffff36	tbz w8, #0x1f, 0x2fc4c54
0x2fc4c68	e04741f9	ldr x0, [sp, #0x288]
0x2fc4c6c	e84f41f9	ldr x8, [sp, #0x298]
0x2fc4c70	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4c74	e6ec0595	bl 0x714000c
0x2fc4c78	e04341f9	ldr x0, [sp, #0x280]
0x2fc4c7c	a0f8ffb4	cbz x0, 0x2fc4b90
0x2fc4c80	e7eb0595	bl 0x713fc1c
0x2fc4c84	c3ffff17	b 0x2fc4b90
0x2fc4c88	f40300aa	mov x20, x0
0x2fc4c8c	e0030091	mov x0, sp
0x2fc4c90	cd030094	bl 0x2fc5bc4
0x2fc4c94	e0430391	add x0, sp, #0xd0
0x2fc4c98	b4944597	bl 0x129f68
0x2fc4c9c	e07740f9	ldr x0, [sp, #0xe8]
0x2fc4ca0	e01000b4	cbz x0, 0x2fc4ebc
0x2fc4ca4	deeb0595	bl 0x713fc1c
0x2fc4ca8	85000014	b 0x2fc4ebc
0x2fc4cac	f40300aa	mov x20, x0
0x2fc4cb0	e8ffc039	ldrsb w8, [sp, #0x3f]
0x2fc4cb4	4801f836	tbz w8, #0x1f, 0x2fc4cdc
0x2fc4cb8	e01740f9	ldr x0, [sp, #0x28]
0x2fc4cbc	e81f40f9	ldr x8, [sp, #0x38]
0x2fc4cc0	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4cc4	d2ec0595	bl 0x714000c
0x2fc4cc8	e89fc039	ldrsb w8, [sp, #0x27]
0x2fc4ccc	c800f837	tbnz w8, #0x1f, 0x2fc4ce4
0x2fc4cd0	e00740f9	ldr x0, [sp, #0x8]
0x2fc4cd4	00feffb4	cbz x0, 0x2fc4c94
0x2fc4cd8	09000014	b 0x2fc4cfc
0x2fc4cdc	e89fc039	ldrsb w8, [sp, #0x27]
0x2fc4ce0	88ffff36	tbz w8, #0x1f, 0x2fc4cd0
0x2fc4ce4	e00b40f9	ldr x0, [sp, #0x10]
0x2fc4ce8	e81340f9	ldr x8, [sp, #0x20]
0x2fc4cec	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4cf0	c7ec0595	bl 0x714000c
0x2fc4cf4	e00740f9	ldr x0, [sp, #0x8]
0x2fc4cf8	e0fcffb4	cbz x0, 0x2fc4c94
0x2fc4cfc	c8eb0595	bl 0x713fc1c
0x2fc4d00	e5ffff17	b 0x2fc4c94
0x2fc4d04	f40300aa	mov x20, x0
0x2fc4d08	e3ffff17	b 0x2fc4c94
0x2fc4d0c	6b000014	b 0x2fc4eb8
0x2fc4d10	f40300aa	mov x20, x0
0x2fc4d14	e0830691	add x0, sp, #0x1a0
0x2fc4d18	2161b994	bl 0x5e1d19c
0x2fc4d1c	02000014	b 0x2fc4d24
0x2fc4d20	f40300aa	mov x20, x0
0x2fc4d24	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc4d28	c801f836	tbz w8, #0x1f, 0x2fc4d60
0x2fc4d2c	e00340f9	ldr x0, [sp]
0x2fc4d30	e80b40f9	ldr x8, [sp, #0x10]
0x2fc4d34	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4d38	b5ec0595	bl 0x714000c
0x2fc4d3c	09000014	b 0x2fc4d60
0x2fc4d40	07000014	b 0x2fc4d5c
0x2fc4d44	29000014	b 0x2fc4de8
0x2fc4d48	28000014	b 0x2fc4de8
0x2fc4d4c	2b000014	b 0x2fc4df8
0x2fc4d50	2a000014	b 0x2fc4df8
0x2fc4d54	59000014	b 0x2fc4eb8
0x2fc4d58	58000014	b 0x2fc4eb8
0x2fc4d5c	f40300aa	mov x20, x0
0x2fc4d60	e00313aa	mov x0, x19
0x2fc4d64	d4030094	bl 0x2fc5cb4
0x2fc4d68	55000014	b 0x2fc4ebc
0x2fc4d6c	53000014	b 0x2fc4eb8
0x2fc4d70	f40300aa	mov x20, x0
0x2fc4d74	e07740f9	ldr x0, [sp, #0xe8]
0x2fc4d78	60f9ffb5	cbnz x0, 0x2fc4ca4
0x2fc4d7c	50000014	b 0x2fc4ebc
0x2fc4d80	12000014	b 0x2fc4dc8
0x2fc4d84	19000014	b 0x2fc4de8
0x2fc4d88	1c000014	b 0x2fc4df8
0x2fc4d8c	4b000014	b 0x2fc4eb8
0x2fc4d90	f40300aa	mov x20, x0
0x2fc4d94	0a000014	b 0x2fc4dbc
0x2fc4d98	f40300aa	mov x20, x0
0x2fc4d9c	e0830691	add x0, sp, #0x1a0
0x2fc4da0	72944597	bl 0x129f68
0x2fc4da4	46000014	b 0x2fc4ebc
0x2fc4da8	f40300aa	mov x20, x0
0x2fc4dac	e00315aa	mov x0, x21
0x2fc4db0	cd900094	bl 0x2fe90e4
0x2fc4db4	e00313aa	mov x0, x19
0x2fc4db8	9b4a4a97	bl 0x257824
0x2fc4dbc	e0830691	add x0, sp, #0x1a0
0x2fc4dc0	8e000094	bl 0x2fc4ff8
0x2fc4dc4	3a000014	b 0x2fc4eac
0x2fc4dc8	f40300aa	mov x20, x0
0x2fc4dcc	a0820091	add x0, x21, #0x20
0x2fc4dd0	66944597	bl 0x129f68
0x2fc4dd4	e8ffc639	ldrsb w8, [sp, #0x1bf]
0x2fc4dd8	2807f836	tbz w8, #0x1f, 0x2fc4ebc
0x2fc4ddc	e0d740f9	ldr x0, [sp, #0x1a8]
0x2fc4de0	e8df40f9	ldr x8, [sp, #0x1b8]
0x2fc4de4	29000014	b 0x2fc4e88
0x2fc4de8	f40300aa	mov x20, x0
0x2fc4dec	e0830691	add x0, sp, #0x1a0
0x2fc4df0	eb60b994	bl 0x5e1d19c
0x2fc4df4	02000014	b 0x2fc4dfc
0x2fc4df8	f40300aa	mov x20, x0
0x2fc4dfc	e85fc039	ldrsb w8, [sp, #0x17]
0x2fc4e00	e805f836	tbz w8, #0x1f, 0x2fc4ebc
0x2fc4e04	e00340f9	ldr x0, [sp]
0x2fc4e08	e80b40f9	ldr x8, [sp, #0x10]
0x2fc4e0c	1f000014	b 0x2fc4e88
0x2fc4e10	2a000014	b 0x2fc4eb8
0x2fc4e14	f40300aa	mov x20, x0
0x2fc4e18	e89fc439	ldrsb w8, [sp, #0x127]
0x2fc4e1c	0806f836	tbz w8, #0x1f, 0x2fc4edc
0x2fc4e20	33000014	b 0x2fc4eec
0x2fc4e24	f40300aa	mov x20, x0
0x2fc4e28	e0830691	add x0, sp, #0x1a0
0x2fc4e2c	2ddc8797	bl 0x11bbee0
0x2fc4e30	1f000014	b 0x2fc4eac
0x2fc4e34	f40300aa	mov x20, x0
0x2fc4e38	e85fc739	ldrsb w8, [sp, #0x1d7]
0x2fc4e3c	a800f836	tbz w8, #0x1f, 0x2fc4e50
0x2fc4e40	e0e340f9	ldr x0, [sp, #0x1c0]
0x2fc4e44	e8eb40f9	ldr x8, [sp, #0x1d0]
0x2fc4e48	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4e4c	70ec0595	bl 0x714000c
0x2fc4e50	e8dfc639	ldrsb w8, [sp, #0x1b7]
0x2fc4e54	c802f836	tbz w8, #0x1f, 0x2fc4eac
0x2fc4e58	e0d340f9	ldr x0, [sp, #0x1a0]
0x2fc4e5c	e8db40f9	ldr x8, [sp, #0x1b0]
0x2fc4e60	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4e64	6aec0595	bl 0x714000c
0x2fc4e68	11000014	b 0x2fc4eac
0x2fc4e6c	f40300aa	mov x20, x0
0x2fc4e70	20830091	add x0, x25, #0x20
0x2fc4e74	3d944597	bl 0x129f68
0x2fc4e78	e83fca39	ldrsb w8, [sp, #0x28f]
0x2fc4e7c	0802f836	tbz w8, #0x1f, 0x2fc4ebc
0x2fc4e80	e03f41f9	ldr x0, [sp, #0x278]
0x2fc4e84	e84741f9	ldr x8, [sp, #0x288]
0x2fc4e88	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4e8c	60ec0595	bl 0x714000c
0x2fc4e90	0b000014	b 0x2fc4ebc
0x2fc4e94	09000014	b 0x2fc4eb8
0x2fc4e98	f40300aa	mov x20, x0
0x2fc4e9c	e0830691	add x0, sp, #0x1a0
0x2fc4ea0	a5974897	bl 0x1ead34
0x2fc4ea4	06000014	b 0x2fc4ebc
0x2fc4ea8	f40300aa	mov x20, x0
0x2fc4eac	e0c30991	add x0, sp, #0x270
0x2fc4eb0	5d4a4a97	bl 0x257824
0x2fc4eb4	02000014	b 0x2fc4ebc
0x2fc4eb8	f40300aa	mov x20, x0
0x2fc4ebc	e81fc439	ldrsb w8, [sp, #0x107]
0x2fc4ec0	2801f836	tbz w8, #0x1f, 0x2fc4ee4
0x2fc4ec4	e07b40f9	ldr x0, [sp, #0xf0]
0x2fc4ec8	e88340f9	ldr x8, [sp, #0x100]
0x2fc4ecc	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4ed0	4fec0595	bl 0x714000c
0x2fc4ed4	e89fc439	ldrsb w8, [sp, #0x127]
0x2fc4ed8	a800f837	tbnz w8, #0x1f, 0x2fc4eec
0x2fc4edc	e00314aa	mov x0, x20
0x2fc4ee0	bee80595	bl 0x713f1d8
0x2fc4ee4	e89fc439	ldrsb w8, [sp, #0x127]
0x2fc4ee8	a8ffff36	tbz w8, #0x1f, 0x2fc4edc
0x2fc4eec	e08b40f9	ldr x0, [sp, #0x110]
0x2fc4ef0	e89340f9	ldr x8, [sp, #0x120]
0x2fc4ef4	01f94092	and x1, x8, #0x7fffffffffffffff
0x2fc4ef8	45ec0595	bl 0x714000c
0x2fc4efc	e00314aa	mov x0, x20
0x2fc4f00	b6e80595	bl 0x713f1d8
