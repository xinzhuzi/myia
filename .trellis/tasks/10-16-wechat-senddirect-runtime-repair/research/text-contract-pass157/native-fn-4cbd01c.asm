0x4cbd01c	ff0302d1	sub sp,sp,#0x80
0x4cbd020	fc6f02a9	stp x28,x27,[sp, #0x20]
0x4cbd024	fa6703a9	stp x26,x25,[sp, #0x30]
0x4cbd028	f85f04a9	stp x24,x23,[sp, #0x40]
0x4cbd02c	f65705a9	stp x22,x21,[sp, #0x50]
0x4cbd030	f44f06a9	stp x20,x19,[sp, #0x60]
0x4cbd034	fd7b07a9	stp x29,x30,[sp, #0x70]
0x4cbd038	fdc30191	add x29,sp,#0x70
0x4cbd03c	fa0303aa	mov x26,x3
0x4cbd040	f80302aa	mov x24,x2
0x4cbd044	f90301aa	mov x25,x1
0x4cbd048	f30300aa	mov x19,x0
0x4cbd04c	888f02f0	adrp x8,0x9eb0000
0x4cbd050	08c11391	add x8,x8,#0x4f0
0x4cbd054	087c00a9	stp x8,xzr,[x0]
0x4cbd058	1f1000b9	str wzr,[x0, #0x10]
0x4cbd05c	00e4006f	movi v0.2D,#0x0
0x4cbd060	fc0300aa	mov x28,x0
0x4cbd064	808f813c	str q0,[x28, #0x18]!
0x4cbd068	00808a3c	stur q0,[x0, #0xa8]
0x4cbd06c	f40300aa	mov x20,x0
0x4cbd070	808e893c	str q0,[x20, #0x98]!
0x4cbd074	0080823c	stur q0,[x0, #0x28]
0x4cbd078	0080833c	stur q0,[x0, #0x38]
0x4cbd07c	0080843c	stur q0,[x0, #0x48]
0x4cbd080	0080853c	stur q0,[x0, #0x58]
0x4cbd084	0080863c	stur q0,[x0, #0x68]
0x4cbd088	0080873c	stur q0,[x0, #0x78]
0x4cbd08c	0020883c	stur q0,[x0, #0x82]
0x4cbd090	08f0a752	mov w8,#0x3f800000
0x4cbd094	08b800b9	str w8,[x0, #0xb8]
0x4cbd098	008006ad	stp q0,q0,[x0, #0xd0]
0x4cbd09c	1fe00179	strh wzr,[x0, #0xf0]
0x4cbd0a0	f50300aa	mov x21,x0
0x4cbd0a4	a00e8c3c	str q0,[x21, #0xc0]!
0x4cbd0a8	f60300aa	mov x22,x0
0x4cbd0ac	c04e8f3c	str q0,[x22, #0xf4]!
0x4cbd0b0	c0ce863c	str q0,[x22, #0x6c]!
0x4cbd0b4	fb0316aa	mov x27,x22
0x4cbd0b8	600f9d3c	str q0,[x27, #-0x30]!
0x4cbd0bc	df421cf8	stur xzr,[x22, #-0x3c]
0x4cbd0c0	c0429b3c	stur q0,[x22, #-0x4c]
0x4cbd0c4	c0429a3c	stur q0,[x22, #-0x5c]
0x4cbd0c8	c0023fad	stp q0,q0,[x22, #-0x20]
0x4cbd0cc	c08200ad	stp q0,q0,[x22, #0x10]
0x4cbd0d0	c0c20091	add x0,x22,#0x30
0x4cbd0d4	b3a60794	bl 0x04ea6ba0
0x4cbd0d8	00048052	mov w0,#0x20
0x4cbd0dc	d50b9294	bl 0x07140030
0x4cbd0e0	00e4006f	movi v0.2D,#0x0
0x4cbd0e4	0080803c	stur q0,[x0, #0x8]
0x4cbd0e8	487a02f0	adrp x8,0x9c08000
0x4cbd0ec	08611091	add x8,x8,#0x418
0x4cbd0f0	08410091	add x8,x8,#0x10
0x4cbd0f4	080000f9	str x8,[x0]
0x4cbd0f8	e80300aa	mov x8,x0
0x4cbd0fc	1f8d01f8	str xzr,[x8, #0x18]!
0x4cbd100	680601f9	str x8,[x19, #0x208]
0x4cbd104	600a01f9	str x0,[x19, #0x210]
0x4cbd108	7f620839	strb wzr,[x19, #0x218]
0x4cbd10c	77820891	add x23,x19,#0x220
0x4cbd110	600211ad	stp q0,q0,[x19, #0x220]
0x4cbd114	28008052	mov w8,#0x1
0x4cbd118	68020939	strb w8,[x19, #0x240]
0x4cbd11c	68220991	add x8,x19,#0x248
0x4cbd120	69820991	add x9,x19,#0x260
0x4cbd124	7f3201f9	str xzr,[x19, #0x260]
0x4cbd128	2081803c	stur q0,[x9, #0x8]
0x4cbd12c	7f620939	strb wzr,[x19, #0x258]
0x4cbd130	0001803d	str q0,[x8]
0x4cbd134	283b40f9	ldr x8,[x25, #0x70]
0x4cbd138	687e00f9	str x8,[x19, #0xf8]
0x4cbd13c	282b40f9	ldr x8,[x25, #0x50]
0x4cbd140	08fd43d3	lsr x8,x8,#0x3
0x4cbd144	e9f99ed2	mov x9,#0xf7cf
0x4cbd148	696abcf2	movk x9,#0xe353, LSL #16
0x4cbd14c	a974d3f2	movk x9,#0x9ba5, LSL #32
0x4cbd150	8918e4f2	movk x9,#0x20c4, LSL #48
0x4cbd154	087dc99b	umulh x8,x8,x9
0x4cbd158	09fd44d3	lsr x9,x8,#0x4
0x4cbd15c	691601b9	str w9,[x19, #0x114]
0x4cbd160	088d44d3	ubfx x8,x8,#0x4,#0x20
0x4cbd164	097d8052	mov w9,#0x3e8
0x4cbd168	087da99b	umull x8,w8,w9
0x4cbd16c	688200f9	str x8,[x19, #0x100]
0x4cbd170	283f40f9	ldr x8,[x25, #0x78]
0x4cbd174	682601b9	str w8,[x19, #0x124]
0x4cbd178	21230091	add x1,x25,#0x8
0x4cbd17c	e0031caa	mov x0,x28
0x4cbd180	d8099294	bl 0x0713f8e0
0x4cbd184	c0c204d1	sub x0,x22,#0x130
0x4cbd188	21830091	add x1,x25,#0x20
0x4cbd18c	d5099294	bl 0x0713f8e0
0x4cbd190	280340b9	ldr w8,[x25]
0x4cbd194	1fc50071	cmp w8,#0x31
0x4cbd198	c1000054	b.ne 0x04cbd1b0
0x4cbd19c	20e30091	add x0,x25,#0x38
0x4cbd1a0	f6410094	bl 0x04ccd978
0x4cbd1a4	fc0300aa	mov x28,x0
0x4cbd1a8	280340b9	ldr w8,[x25]
0x4cbd1ac	02000014	b 0x04cbd1b4
0x4cbd1b0	1c008052	mov w28,#0x0
0x4cbd1b4	e803082a	mov w8,w8
0x4cbd1b8	08811caa	orr x8,x8,x28, LSL #0x20
0x4cbd1bc	e80f00f9	str x8,[sp, #0x18]
0x4cbd1c0	7f620939	strb wzr,[x19, #0x258]
0x4cbd1c4	21e30091	add x1,x25,#0x38
0x4cbd1c8	e0031baa	mov x0,x27
0x4cbd1cc	c5099294	bl 0x0713f8e0
0x4cbd1d0	e0630091	add x0,sp,#0x18
0x4cbd1d4	d9bcef97	bl 0x048ac538
0x4cbd1d8	40010036	tbz w0,#0x0,0x04cbd200
0x4cbd1dc	21630191	add x1,x25,#0x58
0x4cbd1e0	e00316aa	mov x0,x22
0x4cbd1e4	bf099294	bl 0x0713f8e0
0x4cbd1e8	280340b9	ldr w8,[x25]
0x4cbd1ec	49e28452	mov w9,#0x2712
0x4cbd1f0	0ae28452	mov w10,#0x2710
0x4cbd1f4	1f01096b	cmp w8,w9
0x4cbd1f8	4101881a	csel w1,w10,w8,eq
0x4cbd1fc	0a000014	b 0x04cbd224
0x4cbd200	280340b9	ldr w8,[x25]
0x4cbd204	49e28452	mov w9,#0x2712
0x4cbd208	1f01096b	cmp w8,w9
0x4cbd20c	a1000054	b.ne 0x04cbd220
0x4cbd210	20e30091	add x0,x25,#0x38
0x4cbd214	e1031aaa	mov x1,x26
0x4cbd218	f0c8ef97	bl 0x048af5d8
0x4cbd21c	00feff35	cbnz w0,0x04cbd1dc
0x4cbd220	015f8552	mov w1,#0x2af8
0x4cbd224	e00313aa	mov x0,x19
0x4cbd228	befaff97	bl 0x04cbbd20
0x4cbd22c	7c1200b9	str w28,[x19, #0x10]
0x4cbd230	68c240f8	ldur x8,[x19, #0xc]
0x4cbd234	688600f9	str x8,[x19, #0x108]
0x4cbd238	681241f9	ldr x8,[x19, #0x220]
0x4cbd23c	c80000b4	cbz x8,0x04cbd254
0x4cbd240	e00313aa	mov x0,x19
0x4cbd244	d0b2f597	bl 0x04a29d84
0x4cbd248	60000034	cbz w0,0x04cbd254
0x4cbd24c	e80240f9	ldr x8,[x23]
0x4cbd250	1c0d00b9	str w28,[x8, #0xc]
0x4cbd254	1f030071	cmp w24,#0x0
0x4cbd258	a8008052	mov w8,#0x5
0x4cbd25c	0805881a	cinc w8,w8,ne
0x4cbd260	682a01b9	str w8,[x19, #0x128]
0x4cbd264	e00313aa	mov x0,x19
0x4cbd268	38010094	bl 0x04cbd748
0x4cbd26c	88008052	mov w8,#0x4
0x4cbd270	49008052	mov w9,#0x2
0x4cbd274	1f000071	cmp w0,#0x0
0x4cbd278	2811881a	csel w8,w9,w8,ne
0x4cbd27c	681a01b9	str w8,[x19, #0x118]
0x4cbd280	e00313aa	mov x0,x19
0x4cbd284	90aff597	bl 0x04a290c4
0x4cbd288	a0010037	tbnz w0,#0x0,0x04cbd2bc
0x4cbd28c	e00313aa	mov x0,x19
0x4cbd290	0faff597	bl 0x04a28ecc
0x4cbd294	40010037	tbnz w0,#0x0,0x04cbd2bc
0x4cbd298	e00313aa	mov x0,x19
0x4cbd29c	9baff597	bl 0x04a29108
0x4cbd2a0	e0000037	tbnz w0,#0x0,0x04cbd2bc
0x4cbd2a4	e00313aa	mov x0,x19
0x4cbd2a8	caaff597	bl 0x04a291d0
0x4cbd2ac	80000037	tbnz w0,#0x0,0x04cbd2bc
0x4cbd2b0	e00313aa	mov x0,x19
0x4cbd2b4	11aff597	bl 0x04a28ef8
0x4cbd2b8	80000034	cbz w0,0x04cbd2c8
0x4cbd2bc	e00313aa	mov x0,x19
0x4cbd2c0	21008052	mov w1,#0x1
0x4cbd2c4	3afcff97	bl 0x04cbc3ac
0x4cbd2c8	e8030091	mov x8,sp
0x4cbd2cc	e00313aa	mov x0,x19
0x4cbd2d0	6efaff97	bl 0x04cbbc88
0x4cbd2d4	e1030091	mov x1,sp
0x4cbd2d8	e00313aa	mov x0,x19
0x4cbd2dc	13f9ff97	bl 0x04cbb728
0x4cbd2e0	e85fc039	ldrsb w8,[sp, #0x17]
0x4cbd2e4	a800f836	tbz w8,#0x1f,0x04cbd2f8
0x4cbd2e8	e00340f9	ldr x0,[sp]
0x4cbd2ec	e80b40f9	ldr x8,[sp, #0x10]
0x4cbd2f0	01f94092	and x1,x8,#0x7fffffffffffffff
0x4cbd2f4	460b9294	bl 0x0714000c
0x4cbd2f8	680e40b9	ldr w8,[x19, #0xc]
0x4cbd2fc	095f8552	mov w9,#0x2af8
0x4cbd300	1f01096b	cmp w8,w9
0x4cbd304	a1060054	b.ne 0x04cbd3d8
0x4cbd308	e00313aa	mov x0,x19
0x4cbd30c	0f010094	bl 0x04cbd748
0x4cbd310	20050037	tbnz w0,#0x0,0x04cbd3b4
0x4cbd314	687e8139	ldrsb x8,[x19, #0x5f]
0x4cbd318	6800f8b7	tbnz x8,#0x3f,0x04cbd324
0x4cbd31c	c80400b5	cbnz x8,0x04cbd3b4
0x4cbd320	03000014	b 0x04cbd32c
0x4cbd324	682a40f9	ldr x8,[x19, #0x50]
0x4cbd328	680400b5	cbnz x8,0x04cbd3b4
0x4cbd32c	681240b9	ldr w8,[x19, #0x10]
0x4cbd330	1ff10171	cmp w8,#0x7c
0x4cbd334	01040054	b.ne 0x04cbd3b4
0x4cbd338	00018152	mov w0,#0x808
0x4cbd33c	3d0b9294	bl 0x07140030
0x4cbd340	f90300aa	mov x25,x0
0x4cbd344	fa0300aa	mov x26,x0
0x4cbd348	5f8f00f8	str xzr,[x26, #0x8]!
0x4cbd34c	1f0800f9	str xzr,[x0, #0x10]
0x4cbd350	687d0290	adrp x8,0x9c69000
0x4cbd354	08012491	add x8,x8,#0x900
0x4cbd358	080000f9	str x8,[x0]
0x4cbd35c	18600091	add x24,x0,#0x18
0x4cbd360	e00318aa	mov x0,x24
0x4cbd364	01fe8052	mov w1,#0x7f0
0x4cbd368	0a0c9294	bl 0x07140390
0x4cbd36c	e00318aa	mov x0,x24
0x4cbd370	d566f896	bl 0x00ad6ec4
0x4cbd374	f86700a9	stp x24,x25,[sp]
0x4cbd378	280f40f9	ldr x8,[x25, #0x18]
0x4cbd37c	080d40f9	ldr x8,[x8, #0x18]
0x4cbd380	e00318aa	mov x0,x24
0x4cbd384	e10313aa	mov x1,x19
0x4cbd388	00013fd6	blr x8
0x4cbd38c	590100b4	cbz x25,0x04cbd3b4
0x4cbd390	08008092	mov x8,#-0x1
0x4cbd394	4803e8f8	ldaddal x8,x8,[x26]
0x4cbd398	e80000b5	cbnz x8,0x04cbd3b4
0x4cbd39c	280340f9	ldr x8,[x25]
0x4cbd3a0	080940f9	ldr x8,[x8, #0x10]
0x4cbd3a4	e00319aa	mov x0,x25
0x4cbd3a8	00013fd6	blr x8
0x4cbd3ac	e00319aa	mov x0,x25
0x4cbd3b0	1b0a9294	bl 0x0713fc1c
0x4cbd3b4	7f620939	strb wzr,[x19, #0x258]
0x4cbd3b8	681ec539	ldrsb w8,[x19, #0x147]
0x4cbd3bc	a800f836	tbz w8,#0x1f,0x04cbd3d0
0x4cbd3c0	609a40f9	ldr x0,[x19, #0x130]
0x4cbd3c4	68a240f9	ldr x8,[x19, #0x140]
0x4cbd3c8	01f94092	and x1,x8,#0x7fffffffffffffff
0x4cbd3cc	100b9294	bl 0x0714000c
0x4cbd3d0	7fc20439	strb wzr,[x19, #0x130]
0x4cbd3d4	7f1e0539	strb wzr,[x19, #0x147]
0x4cbd3d8	7f020939	strb wzr,[x19, #0x240]
0x4cbd3dc	e00313aa	mov x0,x19
0x4cbd3e0	01008052	mov w1,#0x0
0x4cbd3e4	37fcff97	bl 0x04cbc4c0
0x4cbd3e8	e00313aa	mov x0,x19
0x4cbd3ec	fd7b47a9	ldp x29,x30,[sp, #0x70]
0x4cbd3f0	f44f46a9	ldp x20,x19,[sp, #0x60]
0x4cbd3f4	f65745a9	ldp x22,x21,[sp, #0x50]
0x4cbd3f8	f85f44a9	ldp x24,x23,[sp, #0x40]
0x4cbd3fc	fa6743a9	ldp x26,x25,[sp, #0x30]
0x4cbd400	fc6f42a9	ldp x28,x27,[sp, #0x20]
0x4cbd404	ff030291	add sp,sp,#0x80
0x4cbd408	c0035fd6	ret
