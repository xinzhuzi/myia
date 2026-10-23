0x4eaeeb8	ffc301d1	sub sp, sp, #0x70
0x4eaeebc	fc6f01a9	stp x28, x27, [sp, #0x10]
0x4eaeec0	fa6702a9	stp x26, x25, [sp, #0x20]
0x4eaeec4	f85f03a9	stp x24, x23, [sp, #0x30]
0x4eaeec8	f65704a9	stp x22, x21, [sp, #0x40]
0x4eaeecc	f44f05a9	stp x20, x19, [sp, #0x50]
0x4eaeed0	fd7b06a9	stp x29, x30, [sp, #0x60]
0x4eaeed4	fd830191	add x29, sp, #0x60
0x4eaeed8	f30301aa	mov x19, x1
0x4eaeedc	f40300aa	mov x20, x0
0x4eaeee0	17e201f0	adrp x23, 0x8af1000
0x4eaeee4	f7023191	add x23, x23, #0xc40
0x4eaeee8	f9f30132	mov w25, #-0x55555556
0x4eaeeec	bab302d0	adrp x26, 0xa524000
0x4eaeef0	5a432b91	add x26, x26, #0xad0
0x4eaeef4	bc8002d0	adrp x28, 0x9ec4000
0x4eaeef8	9c030391	add x28, x28, #0xc0
0x4eaeefc	b88002d0	adrp x24, 0x9ec4000
0x4eaef00	18e30491	add x24, x24, #0x138
0x4eaef04	bb8002d0	adrp x27, 0x9ec4000
0x4eaef08	7bc30691	add x27, x27, #0x1b0
0x4eaef0c	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaef10	1f0109eb	cmp x8, x9
0x4eaef14	02010054	b.hs 0x4eaef34
0x4eaef18	0101c039	ldrsb w1, [x8]
0x4eaef1c	c100f837	tbnz w1, #0x1f, 0x4eaef34
0x4eaef20	612200b9	str w1, [x19, #0x20]
0x4eaef24	08050091	add x8, x8, #0x1
0x4eaef28	680600f9	str x8, [x19, #0x8]
0x4eaef2c	e1000035	cbnz w1, 0x4eaef48
0x4eaef30	1a030014	b 0x4eafb98
0x4eaef34	e00313aa	mov x0, x19
0x4eaef38	41103094	bl 0x5ab303c
0x4eaef3c	e10300aa	mov x1, x0
0x4eaef40	602200b9	str w0, [x19, #0x20]
0x4eaef44	a1620034	cbz w1, 0x4eafb98
0x4eaef48	297c0353	lsr w9, w1, #3
0x4eaef4c	28080012	and w8, w1, #0x7
0x4eaef50	29050051	sub w9, w9, #0x1
0x4eaef54	3f350071	cmp w9, #0xd
0x4eaef58	68070054	b.hi 0x4eaf044
0x4eaef5c	8a000010	adr x10, 0x4eaef6c
0x4eaef60	eb6a6938	ldrb w11, [x23, x9]
0x4eaef64	4a090b8b	add x10, x10, x11, lsl #2
0x4eaef68	40011fd6	br x10
0x4eaef6c	c8060035	cbnz w8, 0x4eaf044
0x4eaef70	69a240a9	ldp x9, x8, [x19, #0x8]
0x4eaef74	3f0108eb	cmp x9, x8
0x4eaef78	22070054	b.hs 0x4eaf05c
0x4eaef7c	2a01c039	ldrsb w10, [x9]
0x4eaef80	ea06f837	tbnz w10, #0x1f, 0x4eaf05c
0x4eaef84	8a8200b8	stur w10, [x20, #0x8]
0x4eaef88	29050091	add x9, x9, #0x1
0x4eaef8c	690600f9	str x9, [x19, #0x8]
0x4eaef90	38000014	b 0x4eaf070
0x4eaef94	1f090071	cmp w8, #0x2
0x4eaef98	61050054	b.ne 0x4eaf044
0x4eaef9c	8a7640b9	ldr w10, [x20, #0x74]
0x4eaefa0	4b020014	b 0x4eaf8cc
0x4eaefa4	1f090071	cmp w8, #0x2
0x4eaefa8	e1040054	b.ne 0x4eaf044
0x4eaefac	cc000014	b 0x4eaf2dc
0x4eaefb0	1f090071	cmp w8, #0x2
0x4eaefb4	81040054	b.ne 0x4eaf044
0x4eaefb8	7f020014	b 0x4eaf9b4
0x4eaefbc	1f090071	cmp w8, #0x2
0x4eaefc0	21040054	b.ne 0x4eaf044
0x4eaefc4	f1010014	b 0x4eaf788
0x4eaefc8	1f090071	cmp w8, #0x2
0x4eaefcc	c1030054	b.ne 0x4eaf044
0x4eaefd0	8a7640b9	ldr w10, [x20, #0x74]
0x4eaefd4	48000014	b 0x4eaf0f4
0x4eaefd8	1f090071	cmp w8, #0x2
0x4eaefdc	41030054	b.ne 0x4eaf044
0x4eaefe0	81000014	b 0x4eaf1e4
0x4eaefe4	1f090071	cmp w8, #0x2
0x4eaefe8	e1020054	b.ne 0x4eaf044
0x4eaefec	70010014	b 0x4eaf5ac
0x4eaeff0	a8020035	cbnz w8, 0x4eaf044
0x4eaeff4	69a240a9	ldp x9, x8, [x19, #0x8]
0x4eaeff8	3f0108eb	cmp x9, x8
0x4eaeffc	23050054	b.lo 0x4eaf0a0
0x4eaf000	2e000014	b 0x4eaf0b8
0x4eaf004	1f090071	cmp w8, #0x2
0x4eaf008	e1010054	b.ne 0x4eaf044
0x4eaf00c	ef000014	b 0x4eaf3c8
0x4eaf010	1f090071	cmp w8, #0x2
0x4eaf014	81010054	b.ne 0x4eaf044
0x4eaf018	a0020014	b 0x4eafa98
0x4eaf01c	1f090071	cmp w8, #0x2
0x4eaf020	21010054	b.ne 0x4eaf044
0x4eaf024	25010014	b 0x4eaf4b8
0x4eaf028	e8000035	cbnz w8, 0x4eaf044
0x4eaf02c	69a240a9	ldp x9, x8, [x19, #0x8]
0x4eaf030	3f0108eb	cmp x9, x8
0x4eaf034	23420054	b.lo 0x4eaf878
0x4eaf038	16020014	b 0x4eaf890
0x4eaf03c	1f090071	cmp w8, #0x2
0x4eaf040	00330054	b.eq 0x4eaf6a0
0x4eaf044	1f110071	cmp w8, #0x4
0x4eaf048	805a0054	b.eq 0x4eafb98
0x4eaf04c	e00313aa	mov x0, x19
0x4eaf050	97163094	bl 0x5ab4aac
0x4eaf054	c0f50737	tbnz w0, #0x0, 0x4eaef0c
0x4eaf058	ce020014	b 0x4eafb90
0x4eaf05c	81220091	add x1, x20, #0x8
0x4eaf060	e00313aa	mov x0, x19
0x4eaf064	8f0f3094	bl 0x5ab2ea0
0x4eaf068	a0590034	cbz w0, 0x4eafb9c
0x4eaf06c	69a240a9	ldp x9, x8, [x19, #0x8]
0x4eaf070	8a7640b9	ldr w10, [x20, #0x74]
0x4eaf074	4a010032	orr w10, w10, #0x1
0x4eaf078	8a7600b9	str w10, [x20, #0x74]
0x4eaf07c	3f0108eb	cmp x9, x8
0x4eaf080	62f4ff54	b.hs 0x4eaef0c
0x4eaf084	2a014039	ldrb w10, [x9]
0x4eaf088	5f410071	cmp w10, #0x10
0x4eaf08c	01f4ff54	b.ne 0x4eaef0c
0x4eaf090	29050091	add x9, x9, #0x1
0x4eaf094	690600f9	str x9, [x19, #0x8]
0x4eaf098	3f0108eb	cmp x9, x8
0x4eaf09c	e2000054	b.hs 0x4eaf0b8
0x4eaf0a0	2a01c039	ldrsb w10, [x9]
0x4eaf0a4	aa00f837	tbnz w10, #0x1f, 0x4eaf0b8
0x4eaf0a8	8ac200b8	stur w10, [x20, #0xc]
0x4eaf0ac	29050091	add x9, x9, #0x1
0x4eaf0b0	690600f9	str x9, [x19, #0x8]
0x4eaf0b4	06000014	b 0x4eaf0cc
0x4eaf0b8	81320091	add x1, x20, #0xc
0x4eaf0bc	e00313aa	mov x0, x19
0x4eaf0c0	780f3094	bl 0x5ab2ea0
0x4eaf0c4	c0560034	cbz w0, 0x4eafb9c
0x4eaf0c8	69a240a9	ldp x9, x8, [x19, #0x8]
0x4eaf0cc	8a7640b9	ldr w10, [x20, #0x74]
0x4eaf0d0	4a011f32	orr w10, w10, #0x2
0x4eaf0d4	8a7600b9	str w10, [x20, #0x74]
0x4eaf0d8	3f0108eb	cmp x9, x8
0x4eaf0dc	82f1ff54	b.hs 0x4eaef0c
0x4eaf0e0	28014039	ldrb w8, [x9]
0x4eaf0e4	1f690071	cmp w8, #0x1a
0x4eaf0e8	21f1ff54	b.ne 0x4eaef0c
0x4eaf0ec	28050091	add x8, x9, #0x1
0x4eaf0f0	680600f9	str x8, [x19, #0x8]
0x4eaf0f4	48011e32	orr w8, w10, #0x4
0x4eaf0f8	887600b9	str w8, [x20, #0x74]
0x4eaf0fc	950a40f9	ldr x21, [x20, #0x10]
0x4eaf100	950100b5	cbnz x21, 0x4eaf130
0x4eaf104	00058052	mov w0, #0x28
0x4eaf108	ca438a94	bl 0x7140030
0x4eaf10c	f50300aa	mov x21, x0
0x4eaf110	a8800290	adrp x8, 0x9ec3000
0x4eaf114	08612e91	add x8, x8, #0xb98
0x4eaf118	080000f9	str x8, [x0]
0x4eaf11c	00e4006f	movi.2d v0, #0000000000000000
0x4eaf120	000400fd	str d0, [x0, #0x8]
0x4eaf124	1a6801a9	stp x26, x26, [x0, #0x10]
0x4eaf128	001000fd	str d0, [x0, #0x20]
0x4eaf12c	800a00f9	str x0, [x20, #0x10]
0x4eaf130	f90f00b9	str w25, [sp, #0xc]
0x4eaf134	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf138	1f0109eb	cmp x8, x9
0x4eaf13c	e2000054	b.hs 0x4eaf158
0x4eaf140	0901c039	ldrsb w9, [x8]
0x4eaf144	a900f837	tbnz w9, #0x1f, 0x4eaf158
0x4eaf148	e90f00b9	str w9, [sp, #0xc]
0x4eaf14c	08050091	add x8, x8, #0x1
0x4eaf150	680600f9	str x8, [x19, #0x8]
0x4eaf154	05000014	b 0x4eaf168
0x4eaf158	e1330091	add x1, sp, #0xc
0x4eaf15c	e00313aa	mov x0, x19
0x4eaf160	500f3094	bl 0x5ab2ea0
0x4eaf164	60510034	cbz w0, 0x4eafb90
0x4eaf168	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf16c	0a050011	add w10, w8, #0x1
0x4eaf170	6a3a00b9	str w10, [x19, #0x38]
0x4eaf174	1f01096b	cmp w8, w9
0x4eaf178	ca500054	b.ge 0x4eafb90
0x4eaf17c	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf180	e00313aa	mov x0, x19
0x4eaf184	5b0d3094	bl 0x5ab26f0
0x4eaf188	f60300aa	mov x22, x0
0x4eaf18c	e00315aa	mov x0, x21
0x4eaf190	e10313aa	mov x1, x19
0x4eaf194	dbdfff97	bl 0x4ea7100
0x4eaf198	c04f0034	cbz w0, 0x4eafb90
0x4eaf19c	68924039	ldrb w8, [x19, #0x24]
0x4eaf1a0	1f050071	cmp w8, #0x1
0x4eaf1a4	614f0054	b.ne 0x4eafb90
0x4eaf1a8	e00313aa	mov x0, x19
0x4eaf1ac	e10316aa	mov x1, x22
0x4eaf1b0	6f0d3094	bl 0x5ab276c
0x4eaf1b4	683a40b9	ldr w8, [x19, #0x38]
0x4eaf1b8	08050071	subs w8, w8, #0x1
0x4eaf1bc	4b000054	b.lt 0x4eaf1c4
0x4eaf1c0	683a00b9	str w8, [x19, #0x38]
0x4eaf1c4	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf1c8	1f0109eb	cmp x8, x9
0x4eaf1cc	02eaff54	b.hs 0x4eaef0c
0x4eaf1d0	09014039	ldrb w9, [x8]
0x4eaf1d4	3f890071	cmp w9, #0x22
0x4eaf1d8	a1e9ff54	b.ne 0x4eaef0c
0x4eaf1dc	08050091	add x8, x8, #0x1
0x4eaf1e0	680600f9	str x8, [x19, #0x8]
0x4eaf1e4	887640b9	ldr w8, [x20, #0x74]
0x4eaf1e8	08011d32	orr w8, w8, #0x8
0x4eaf1ec	887600b9	str w8, [x20, #0x74]
0x4eaf1f0	950e40f9	ldr x21, [x20, #0x18]
0x4eaf1f4	b50100b5	cbnz x21, 0x4eaf228
0x4eaf1f8	00088052	mov w0, #0x40
0x4eaf1fc	8d438a94	bl 0x7140030
0x4eaf200	f50300aa	mov x21, x0
0x4eaf204	1ffc00a9	stp xzr, xzr, [x0, #0x8]
0x4eaf208	a8800290	adrp x8, 0x9ec3000
0x4eaf20c	08413091	add x8, x8, #0xc10
0x4eaf210	080000f9	str x8, [x0]
0x4eaf214	1f5001f8	stur xzr, [x0, #0x15]
0x4eaf218	1a6802a9	stp x26, x26, [x0, #0x20]
0x4eaf21c	1f1800f9	str xzr, [x0, #0x30]
0x4eaf220	1f3800b9	str wzr, [x0, #0x38]
0x4eaf224	800e00f9	str x0, [x20, #0x18]
0x4eaf228	f90f00b9	str w25, [sp, #0xc]
0x4eaf22c	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf230	1f0109eb	cmp x8, x9
0x4eaf234	e2000054	b.hs 0x4eaf250
0x4eaf238	0901c039	ldrsb w9, [x8]
0x4eaf23c	a900f837	tbnz w9, #0x1f, 0x4eaf250
0x4eaf240	e90f00b9	str w9, [sp, #0xc]
0x4eaf244	08050091	add x8, x8, #0x1
0x4eaf248	680600f9	str x8, [x19, #0x8]
0x4eaf24c	05000014	b 0x4eaf260
0x4eaf250	e1330091	add x1, sp, #0xc
0x4eaf254	e00313aa	mov x0, x19
0x4eaf258	120f3094	bl 0x5ab2ea0
0x4eaf25c	a0490034	cbz w0, 0x4eafb90
0x4eaf260	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf264	0a050011	add w10, w8, #0x1
0x4eaf268	6a3a00b9	str w10, [x19, #0x38]
0x4eaf26c	1f01096b	cmp w8, w9
0x4eaf270	0a490054	b.ge 0x4eafb90
0x4eaf274	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf278	e00313aa	mov x0, x19
0x4eaf27c	1d0d3094	bl 0x5ab26f0
0x4eaf280	f60300aa	mov x22, x0
0x4eaf284	e00315aa	mov x0, x21
0x4eaf288	e10313aa	mov x1, x19
0x4eaf28c	07e2ff97	bl 0x4ea7aa8
0x4eaf290	00480034	cbz w0, 0x4eafb90
0x4eaf294	68924039	ldrb w8, [x19, #0x24]
0x4eaf298	1f050071	cmp w8, #0x1
0x4eaf29c	a1470054	b.ne 0x4eafb90
0x4eaf2a0	e00313aa	mov x0, x19
0x4eaf2a4	e10316aa	mov x1, x22
0x4eaf2a8	310d3094	bl 0x5ab276c
0x4eaf2ac	683a40b9	ldr w8, [x19, #0x38]
0x4eaf2b0	08050071	subs w8, w8, #0x1
0x4eaf2b4	4b000054	b.lt 0x4eaf2bc
0x4eaf2b8	683a00b9	str w8, [x19, #0x38]
0x4eaf2bc	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf2c0	1f0109eb	cmp x8, x9
0x4eaf2c4	42e2ff54	b.hs 0x4eaef0c
0x4eaf2c8	09014039	ldrb w9, [x8]
0x4eaf2cc	3fa90071	cmp w9, #0x2a
0x4eaf2d0	e1e1ff54	b.ne 0x4eaef0c
0x4eaf2d4	08050091	add x8, x8, #0x1
0x4eaf2d8	680600f9	str x8, [x19, #0x8]
0x4eaf2dc	887640b9	ldr w8, [x20, #0x74]
0x4eaf2e0	08011c32	orr w8, w8, #0x10
0x4eaf2e4	887600b9	str w8, [x20, #0x74]
0x4eaf2e8	951240f9	ldr x21, [x20, #0x20]
0x4eaf2ec	550100b5	cbnz x21, 0x4eaf314
0x4eaf2f0	00048052	mov w0, #0x20
0x4eaf2f4	4f438a94	bl 0x7140030
0x4eaf2f8	f50300aa	mov x21, x0
0x4eaf2fc	1afc00a9	stp x26, xzr, [x0, #0x8]
0x4eaf300	a8800290	adrp x8, 0x9ec3000
0x4eaf304	08e13591	add x8, x8, #0xd78
0x4eaf308	080000f9	str x8, [x0]
0x4eaf30c	1f1800b9	str wzr, [x0, #0x18]
0x4eaf310	801200f9	str x0, [x20, #0x20]
0x4eaf314	f90f00b9	str w25, [sp, #0xc]
0x4eaf318	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf31c	1f0109eb	cmp x8, x9
0x4eaf320	e2000054	b.hs 0x4eaf33c
0x4eaf324	0901c039	ldrsb w9, [x8]
0x4eaf328	a900f837	tbnz w9, #0x1f, 0x4eaf33c
0x4eaf32c	e90f00b9	str w9, [sp, #0xc]
0x4eaf330	08050091	add x8, x8, #0x1
0x4eaf334	680600f9	str x8, [x19, #0x8]
0x4eaf338	05000014	b 0x4eaf34c
0x4eaf33c	e1330091	add x1, sp, #0xc
0x4eaf340	e00313aa	mov x0, x19
0x4eaf344	d70e3094	bl 0x5ab2ea0
0x4eaf348	40420034	cbz w0, 0x4eafb90
0x4eaf34c	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf350	0a050011	add w10, w8, #0x1
0x4eaf354	6a3a00b9	str w10, [x19, #0x38]
0x4eaf358	1f01096b	cmp w8, w9
0x4eaf35c	aa410054	b.ge 0x4eafb90
0x4eaf360	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf364	e00313aa	mov x0, x19
0x4eaf368	e20c3094	bl 0x5ab26f0
0x4eaf36c	f60300aa	mov x22, x0
0x4eaf370	e00315aa	mov x0, x21
0x4eaf374	e10313aa	mov x1, x19
0x4eaf378	6fe9ff97	bl 0x4ea9934
0x4eaf37c	a0400034	cbz w0, 0x4eafb90
0x4eaf380	68924039	ldrb w8, [x19, #0x24]
0x4eaf384	1f050071	cmp w8, #0x1
0x4eaf388	41400054	b.ne 0x4eafb90
0x4eaf38c	e00313aa	mov x0, x19
0x4eaf390	e10316aa	mov x1, x22
0x4eaf394	f60c3094	bl 0x5ab276c
0x4eaf398	683a40b9	ldr w8, [x19, #0x38]
0x4eaf39c	08050071	subs w8, w8, #0x1
0x4eaf3a0	4b000054	b.lt 0x4eaf3a8
0x4eaf3a4	683a00b9	str w8, [x19, #0x38]
0x4eaf3a8	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf3ac	1f0109eb	cmp x8, x9
0x4eaf3b0	e2daff54	b.hs 0x4eaef0c
0x4eaf3b4	09014039	ldrb w9, [x8]
0x4eaf3b8	3fc90071	cmp w9, #0x32
0x4eaf3bc	81daff54	b.ne 0x4eaef0c
0x4eaf3c0	08050091	add x8, x8, #0x1
0x4eaf3c4	680600f9	str x8, [x19, #0x8]
0x4eaf3c8	887640b9	ldr w8, [x20, #0x74]
0x4eaf3cc	08011b32	orr w8, w8, #0x20
0x4eaf3d0	887600b9	str w8, [x20, #0x74]
0x4eaf3d4	951640f9	ldr x21, [x20, #0x28]
0x4eaf3d8	750100b5	cbnz x21, 0x4eaf404
0x4eaf3dc	00078052	mov w0, #0x38
0x4eaf3e0	14438a94	bl 0x7140030
0x4eaf3e4	f50300aa	mov x21, x0
0x4eaf3e8	1a7c02a9	stp x26, xzr, [x0, #0x20]
0x4eaf3ec	a8800290	adrp x8, 0x9ec3000
0x4eaf3f0	08c13791	add x8, x8, #0xdf0
0x4eaf3f4	086800a9	stp x8, x26, [x0]
0x4eaf3f8	1a6801a9	stp x26, x26, [x0, #0x10]
0x4eaf3fc	1f3000b9	str wzr, [x0, #0x30]
0x4eaf400	801600f9	str x0, [x20, #0x28]
0x4eaf404	f90f00b9	str w25, [sp, #0xc]
0x4eaf408	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf40c	1f0109eb	cmp x8, x9
0x4eaf410	e2000054	b.hs 0x4eaf42c
0x4eaf414	0901c039	ldrsb w9, [x8]
0x4eaf418	a900f837	tbnz w9, #0x1f, 0x4eaf42c
0x4eaf41c	e90f00b9	str w9, [sp, #0xc]
0x4eaf420	08050091	add x8, x8, #0x1
0x4eaf424	680600f9	str x8, [x19, #0x8]
0x4eaf428	05000014	b 0x4eaf43c
0x4eaf42c	e1330091	add x1, sp, #0xc
0x4eaf430	e00313aa	mov x0, x19
0x4eaf434	9b0e3094	bl 0x5ab2ea0
0x4eaf438	c03a0034	cbz w0, 0x4eafb90
0x4eaf43c	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf440	0a050011	add w10, w8, #0x1
0x4eaf444	6a3a00b9	str w10, [x19, #0x38]
0x4eaf448	1f01096b	cmp w8, w9
0x4eaf44c	2a3a0054	b.ge 0x4eafb90
0x4eaf450	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf454	e00313aa	mov x0, x19
0x4eaf458	a60c3094	bl 0x5ab26f0
0x4eaf45c	f60300aa	mov x22, x0
0x4eaf460	e00315aa	mov x0, x21
0x4eaf464	e10313aa	mov x1, x19
0x4eaf468	85ebff97	bl 0x4eaa27c
0x4eaf46c	20390034	cbz w0, 0x4eafb90
0x4eaf470	68924039	ldrb w8, [x19, #0x24]
0x4eaf474	1f050071	cmp w8, #0x1
0x4eaf478	c1380054	b.ne 0x4eafb90
0x4eaf47c	e00313aa	mov x0, x19
0x4eaf480	e10316aa	mov x1, x22
0x4eaf484	ba0c3094	bl 0x5ab276c
0x4eaf488	683a40b9	ldr w8, [x19, #0x38]
0x4eaf48c	08050071	subs w8, w8, #0x1
0x4eaf490	4b000054	b.lt 0x4eaf498
0x4eaf494	683a00b9	str w8, [x19, #0x38]
0x4eaf498	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf49c	1f0109eb	cmp x8, x9
0x4eaf4a0	62d3ff54	b.hs 0x4eaef0c
0x4eaf4a4	09014039	ldrb w9, [x8]
0x4eaf4a8	3fe90071	cmp w9, #0x3a
0x4eaf4ac	01d3ff54	b.ne 0x4eaef0c
0x4eaf4b0	08050091	add x8, x8, #0x1
0x4eaf4b4	680600f9	str x8, [x19, #0x8]
0x4eaf4b8	887640b9	ldr w8, [x20, #0x74]
0x4eaf4bc	08011a32	orr w8, w8, #0x40
0x4eaf4c0	887600b9	str w8, [x20, #0x74]
0x4eaf4c4	951a40f9	ldr x21, [x20, #0x30]
0x4eaf4c8	950100b5	cbnz x21, 0x4eaf4f8
0x4eaf4cc	00078052	mov w0, #0x38
0x4eaf4d0	d8428a94	bl 0x7140030
0x4eaf4d4	f50300aa	mov x21, x0
0x4eaf4d8	1ffc00a9	stp xzr, xzr, [x0, #0x8]
0x4eaf4dc	a8800290	adrp x8, 0x9ec3000
0x4eaf4e0	08013491	add x8, x8, #0xd00
0x4eaf4e4	080000f9	str x8, [x0]
0x4eaf4e8	1f1800b9	str wzr, [x0, #0x18]
0x4eaf4ec	1a7c02a9	stp x26, xzr, [x0, #0x20]
0x4eaf4f0	1f3000b9	str wzr, [x0, #0x30]
0x4eaf4f4	801a00f9	str x0, [x20, #0x30]
0x4eaf4f8	f90f00b9	str w25, [sp, #0xc]
0x4eaf4fc	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf500	1f0109eb	cmp x8, x9
0x4eaf504	e2000054	b.hs 0x4eaf520
0x4eaf508	0901c039	ldrsb w9, [x8]
0x4eaf50c	a900f837	tbnz w9, #0x1f, 0x4eaf520
0x4eaf510	e90f00b9	str w9, [sp, #0xc]
0x4eaf514	08050091	add x8, x8, #0x1
0x4eaf518	680600f9	str x8, [x19, #0x8]
0x4eaf51c	05000014	b 0x4eaf530
0x4eaf520	e1330091	add x1, sp, #0xc
0x4eaf524	e00313aa	mov x0, x19
0x4eaf528	5e0e3094	bl 0x5ab2ea0
0x4eaf52c	20330034	cbz w0, 0x4eafb90
0x4eaf530	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf534	0a050011	add w10, w8, #0x1
0x4eaf538	6a3a00b9	str w10, [x19, #0x38]
0x4eaf53c	1f01096b	cmp w8, w9
0x4eaf540	8a320054	b.ge 0x4eafb90
0x4eaf544	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf548	e00313aa	mov x0, x19
0x4eaf54c	690c3094	bl 0x5ab26f0
0x4eaf550	f60300aa	mov x22, x0
0x4eaf554	e00315aa	mov x0, x21
0x4eaf558	e10313aa	mov x1, x19
0x4eaf55c	8ae6ff97	bl 0x4ea8f84
0x4eaf560	80310034	cbz w0, 0x4eafb90
0x4eaf564	68924039	ldrb w8, [x19, #0x24]
0x4eaf568	1f050071	cmp w8, #0x1
0x4eaf56c	21310054	b.ne 0x4eafb90
0x4eaf570	e00313aa	mov x0, x19
0x4eaf574	e10316aa	mov x1, x22
0x4eaf578	7d0c3094	bl 0x5ab276c
0x4eaf57c	683a40b9	ldr w8, [x19, #0x38]
0x4eaf580	08050071	subs w8, w8, #0x1
0x4eaf584	4b000054	b.lt 0x4eaf58c
0x4eaf588	683a00b9	str w8, [x19, #0x38]
0x4eaf58c	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf590	1f0109eb	cmp x8, x9
0x4eaf594	c2cbff54	b.hs 0x4eaef0c
0x4eaf598	09014039	ldrb w9, [x8]
0x4eaf59c	3f090171	cmp w9, #0x42
0x4eaf5a0	61cbff54	b.ne 0x4eaef0c
0x4eaf5a4	08050091	add x8, x8, #0x1
0x4eaf5a8	680600f9	str x8, [x19, #0x8]
0x4eaf5ac	887640b9	ldr w8, [x20, #0x74]
0x4eaf5b0	08011932	orr w8, w8, #0x80
0x4eaf5b4	887600b9	str w8, [x20, #0x74]
0x4eaf5b8	951e40f9	ldr x21, [x20, #0x38]
0x4eaf5bc	950100b5	cbnz x21, 0x4eaf5ec
0x4eaf5c0	00088052	mov w0, #0x40
0x4eaf5c4	9b428a94	bl 0x7140030
0x4eaf5c8	f50300aa	mov x21, x0
0x4eaf5cc	a8800290	adrp x8, 0x9ec3000
0x4eaf5d0	08a13991	add x8, x8, #0xe68
0x4eaf5d4	087c00a9	stp x8, xzr, [x0]
0x4eaf5d8	1f6801a9	stp xzr, x26, [x0, #0x10]
0x4eaf5dc	1a7c02a9	stp x26, xzr, [x0, #0x20]
0x4eaf5e0	1f1800f9	str xzr, [x0, #0x30]
0x4eaf5e4	1f3800b9	str wzr, [x0, #0x38]
0x4eaf5e8	801e00f9	str x0, [x20, #0x38]
0x4eaf5ec	f90f00b9	str w25, [sp, #0xc]
0x4eaf5f0	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf5f4	1f0109eb	cmp x8, x9
0x4eaf5f8	e2000054	b.hs 0x4eaf614
0x4eaf5fc	0901c039	ldrsb w9, [x8]
0x4eaf600	a900f837	tbnz w9, #0x1f, 0x4eaf614
0x4eaf604	e90f00b9	str w9, [sp, #0xc]
0x4eaf608	08050091	add x8, x8, #0x1
0x4eaf60c	680600f9	str x8, [x19, #0x8]
0x4eaf610	05000014	b 0x4eaf624
0x4eaf614	e1330091	add x1, sp, #0xc
0x4eaf618	e00313aa	mov x0, x19
0x4eaf61c	210e3094	bl 0x5ab2ea0
0x4eaf620	802b0034	cbz w0, 0x4eafb90
0x4eaf624	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf628	0a050011	add w10, w8, #0x1
0x4eaf62c	6a3a00b9	str w10, [x19, #0x38]
0x4eaf630	1f01096b	cmp w8, w9
0x4eaf634	ea2a0054	b.ge 0x4eafb90
0x4eaf638	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf63c	e00313aa	mov x0, x19
0x4eaf640	2c0c3094	bl 0x5ab26f0
0x4eaf644	f60300aa	mov x22, x0
0x4eaf648	e00315aa	mov x0, x21
0x4eaf64c	e10313aa	mov x1, x19
0x4eaf650	d6edff97	bl 0x4eaada8
0x4eaf654	e0290034	cbz w0, 0x4eafb90
0x4eaf658	68924039	ldrb w8, [x19, #0x24]
0x4eaf65c	1f050071	cmp w8, #0x1
0x4eaf660	81290054	b.ne 0x4eafb90
0x4eaf664	e00313aa	mov x0, x19
0x4eaf668	e10316aa	mov x1, x22
0x4eaf66c	400c3094	bl 0x5ab276c
0x4eaf670	683a40b9	ldr w8, [x19, #0x38]
0x4eaf674	08050071	subs w8, w8, #0x1
0x4eaf678	4b000054	b.lt 0x4eaf680
0x4eaf67c	683a00b9	str w8, [x19, #0x38]
0x4eaf680	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf684	1f0109eb	cmp x8, x9
0x4eaf688	22c4ff54	b.hs 0x4eaef0c
0x4eaf68c	09014039	ldrb w9, [x8]
0x4eaf690	3f290171	cmp w9, #0x4a
0x4eaf694	c1c3ff54	b.ne 0x4eaef0c
0x4eaf698	08050091	add x8, x8, #0x1
0x4eaf69c	680600f9	str x8, [x19, #0x8]
0x4eaf6a0	887640b9	ldr w8, [x20, #0x74]
0x4eaf6a4	08011832	orr w8, w8, #0x100
0x4eaf6a8	887600b9	str w8, [x20, #0x74]
0x4eaf6ac	952240f9	ldr x21, [x20, #0x40]
0x4eaf6b0	350100b5	cbnz x21, 0x4eaf6d4
0x4eaf6b4	00038052	mov w0, #0x18
0x4eaf6b8	5e428a94	bl 0x7140030
0x4eaf6bc	f50300aa	mov x21, x0
0x4eaf6c0	a8800290	adrp x8, 0x9ec3000
0x4eaf6c4	08813b91	add x8, x8, #0xee0
0x4eaf6c8	086800a9	stp x8, x26, [x0]
0x4eaf6cc	1f0800f9	str xzr, [x0, #0x10]
0x4eaf6d0	802200f9	str x0, [x20, #0x40]
0x4eaf6d4	f90f00b9	str w25, [sp, #0xc]
0x4eaf6d8	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf6dc	1f0109eb	cmp x8, x9
0x4eaf6e0	e2000054	b.hs 0x4eaf6fc
0x4eaf6e4	0901c039	ldrsb w9, [x8]
0x4eaf6e8	a900f837	tbnz w9, #0x1f, 0x4eaf6fc
0x4eaf6ec	e90f00b9	str w9, [sp, #0xc]
0x4eaf6f0	08050091	add x8, x8, #0x1
0x4eaf6f4	680600f9	str x8, [x19, #0x8]
0x4eaf6f8	05000014	b 0x4eaf70c
0x4eaf6fc	e1330091	add x1, sp, #0xc
0x4eaf700	e00313aa	mov x0, x19
0x4eaf704	e70d3094	bl 0x5ab2ea0
0x4eaf708	40240034	cbz w0, 0x4eafb90
0x4eaf70c	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf710	0a050011	add w10, w8, #0x1
0x4eaf714	6a3a00b9	str w10, [x19, #0x38]
0x4eaf718	1f01096b	cmp w8, w9
0x4eaf71c	aa230054	b.ge 0x4eafb90
0x4eaf720	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf724	e00313aa	mov x0, x19
0x4eaf728	f20b3094	bl 0x5ab26f0
0x4eaf72c	f60300aa	mov x22, x0
0x4eaf730	e00315aa	mov x0, x21
0x4eaf734	e10313aa	mov x1, x19
0x4eaf738	e0f0ff97	bl 0x4eabab8
0x4eaf73c	a0220034	cbz w0, 0x4eafb90
0x4eaf740	68924039	ldrb w8, [x19, #0x24]
0x4eaf744	1f050071	cmp w8, #0x1
0x4eaf748	41220054	b.ne 0x4eafb90
0x4eaf74c	e00313aa	mov x0, x19
0x4eaf750	e10316aa	mov x1, x22
0x4eaf754	060c3094	bl 0x5ab276c
0x4eaf758	683a40b9	ldr w8, [x19, #0x38]
0x4eaf75c	08050071	subs w8, w8, #0x1
0x4eaf760	4b000054	b.lt 0x4eaf768
0x4eaf764	683a00b9	str w8, [x19, #0x38]
0x4eaf768	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf76c	1f0109eb	cmp x8, x9
0x4eaf770	e2bcff54	b.hs 0x4eaef0c
0x4eaf774	09014039	ldrb w9, [x8]
0x4eaf778	3f490171	cmp w9, #0x52
0x4eaf77c	81bcff54	b.ne 0x4eaef0c
0x4eaf780	08050091	add x8, x8, #0x1
0x4eaf784	680600f9	str x8, [x19, #0x8]
0x4eaf788	887640b9	ldr w8, [x20, #0x74]
0x4eaf78c	08011732	orr w8, w8, #0x200
0x4eaf790	887600b9	str w8, [x20, #0x74]
0x4eaf794	952640f9	ldr x21, [x20, #0x48]
0x4eaf798	350100b5	cbnz x21, 0x4eaf7bc
0x4eaf79c	00038052	mov w0, #0x18
0x4eaf7a0	24428a94	bl 0x7140030
0x4eaf7a4	f50300aa	mov x21, x0
0x4eaf7a8	a8800290	adrp x8, 0x9ec3000
0x4eaf7ac	08613d91	add x8, x8, #0xf58
0x4eaf7b0	087c00a9	stp x8, xzr, [x0]
0x4eaf7b4	1f1000b9	str wzr, [x0, #0x10]
0x4eaf7b8	802600f9	str x0, [x20, #0x48]
0x4eaf7bc	f90f00b9	str w25, [sp, #0xc]
0x4eaf7c0	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf7c4	1f0109eb	cmp x8, x9
0x4eaf7c8	e2000054	b.hs 0x4eaf7e4
0x4eaf7cc	0901c039	ldrsb w9, [x8]
0x4eaf7d0	a900f837	tbnz w9, #0x1f, 0x4eaf7e4
0x4eaf7d4	e90f00b9	str w9, [sp, #0xc]
0x4eaf7d8	08050091	add x8, x8, #0x1
0x4eaf7dc	680600f9	str x8, [x19, #0x8]
0x4eaf7e0	05000014	b 0x4eaf7f4
0x4eaf7e4	e1330091	add x1, sp, #0xc
0x4eaf7e8	e00313aa	mov x0, x19
0x4eaf7ec	ad0d3094	bl 0x5ab2ea0
0x4eaf7f0	001d0034	cbz w0, 0x4eafb90
0x4eaf7f4	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf7f8	0a050011	add w10, w8, #0x1
0x4eaf7fc	6a3a00b9	str w10, [x19, #0x38]
0x4eaf800	1f01096b	cmp w8, w9
0x4eaf804	6a1c0054	b.ge 0x4eafb90
0x4eaf808	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf80c	e00313aa	mov x0, x19
0x4eaf810	b80b3094	bl 0x5ab26f0
0x4eaf814	f60300aa	mov x22, x0
0x4eaf818	e00315aa	mov x0, x21
0x4eaf81c	e10313aa	mov x1, x19
0x4eaf820	e3f1ff97	bl 0x4eabfac
0x4eaf824	601b0034	cbz w0, 0x4eafb90
0x4eaf828	68924039	ldrb w8, [x19, #0x24]
0x4eaf82c	1f050071	cmp w8, #0x1
0x4eaf830	011b0054	b.ne 0x4eafb90
0x4eaf834	e00313aa	mov x0, x19
0x4eaf838	e10316aa	mov x1, x22
0x4eaf83c	cc0b3094	bl 0x5ab276c
0x4eaf840	683a40b9	ldr w8, [x19, #0x38]
0x4eaf844	08050071	subs w8, w8, #0x1
0x4eaf848	4b000054	b.lt 0x4eaf850
0x4eaf84c	683a00b9	str w8, [x19, #0x38]
0x4eaf850	69a240a9	ldp x9, x8, [x19, #0x8]
0x4eaf854	3f0108eb	cmp x9, x8
0x4eaf858	a2b5ff54	b.hs 0x4eaef0c
0x4eaf85c	2a014039	ldrb w10, [x9]
0x4eaf860	5f610171	cmp w10, #0x58
0x4eaf864	41b5ff54	b.ne 0x4eaef0c
0x4eaf868	29050091	add x9, x9, #0x1
0x4eaf86c	690600f9	str x9, [x19, #0x8]
0x4eaf870	3f0108eb	cmp x9, x8
0x4eaf874	e2000054	b.hs 0x4eaf890
0x4eaf878	2a018039	ldrsb x10, [x9]
0x4eaf87c	aa00f8b7	tbnz x10, #0x3f, 0x4eaf890
0x4eaf880	8a0205f8	stur x10, [x20, #0x50]
0x4eaf884	29050091	add x9, x9, #0x1
0x4eaf888	690600f9	str x9, [x19, #0x8]
0x4eaf88c	06000014	b 0x4eaf8a4
0x4eaf890	81420191	add x1, x20, #0x50
0x4eaf894	e00313aa	mov x0, x19
0x4eaf898	300d3094	bl 0x5ab2d58
0x4eaf89c	00180034	cbz w0, 0x4eafb9c
0x4eaf8a0	69a240a9	ldp x9, x8, [x19, #0x8]
0x4eaf8a4	8a7640b9	ldr w10, [x20, #0x74]
0x4eaf8a8	4a011632	orr w10, w10, #0x400
0x4eaf8ac	8a7600b9	str w10, [x20, #0x74]
0x4eaf8b0	3f0108eb	cmp x9, x8
0x4eaf8b4	c2b2ff54	b.hs 0x4eaef0c
0x4eaf8b8	28014039	ldrb w8, [x9]
0x4eaf8bc	1f890171	cmp w8, #0x62
0x4eaf8c0	61b2ff54	b.ne 0x4eaef0c
0x4eaf8c4	28050091	add x8, x9, #0x1
0x4eaf8c8	680600f9	str x8, [x19, #0x8]
0x4eaf8cc	48011532	orr w8, w10, #0x800
0x4eaf8d0	887600b9	str w8, [x20, #0x74]
0x4eaf8d4	952e40f9	ldr x21, [x20, #0x58]
0x4eaf8d8	550100b5	cbnz x21, 0x4eaf900
0x4eaf8dc	00068052	mov w0, #0x30
0x4eaf8e0	d4418a94	bl 0x7140030
0x4eaf8e4	f50300aa	mov x21, x0
0x4eaf8e8	1f1000b9	str wzr, [x0, #0x10]
0x4eaf8ec	1c7c00a9	stp x28, xzr, [x0]
0x4eaf8f0	1f500039	strb wzr, [x0, #0x14]
0x4eaf8f4	1f7c02a9	stp xzr, xzr, [x0, #0x20]
0x4eaf8f8	1f0c00f9	str xzr, [x0, #0x18]
0x4eaf8fc	802e00f9	str x0, [x20, #0x58]
0x4eaf900	f90f00b9	str w25, [sp, #0xc]
0x4eaf904	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf908	1f0109eb	cmp x8, x9
0x4eaf90c	e2000054	b.hs 0x4eaf928
0x4eaf910	0901c039	ldrsb w9, [x8]
0x4eaf914	a900f837	tbnz w9, #0x1f, 0x4eaf928
0x4eaf918	e90f00b9	str w9, [sp, #0xc]
0x4eaf91c	08050091	add x8, x8, #0x1
0x4eaf920	680600f9	str x8, [x19, #0x8]
0x4eaf924	05000014	b 0x4eaf938
0x4eaf928	e1330091	add x1, sp, #0xc
0x4eaf92c	e00313aa	mov x0, x19
0x4eaf930	5c0d3094	bl 0x5ab2ea0
0x4eaf934	e0120034	cbz w0, 0x4eafb90
0x4eaf938	68264729	ldp w8, w9, [x19, #0x38]
0x4eaf93c	0a050011	add w10, w8, #0x1
0x4eaf940	6a3a00b9	str w10, [x19, #0x38]
0x4eaf944	1f01096b	cmp w8, w9
0x4eaf948	4a120054	b.ge 0x4eafb90
0x4eaf94c	e10f40b9	ldr w1, [sp, #0xc]
0x4eaf950	e00313aa	mov x0, x19
0x4eaf954	670b3094	bl 0x5ab26f0
0x4eaf958	f60300aa	mov x22, x0
0x4eaf95c	e00315aa	mov x0, x21
0x4eaf960	e10313aa	mov x1, x19
0x4eaf964	a0f5ff97	bl 0x4eacfe4
0x4eaf968	40110034	cbz w0, 0x4eafb90
0x4eaf96c	68924039	ldrb w8, [x19, #0x24]
0x4eaf970	1f050071	cmp w8, #0x1
0x4eaf974	e1100054	b.ne 0x4eafb90
0x4eaf978	e00313aa	mov x0, x19
0x4eaf97c	e10316aa	mov x1, x22
0x4eaf980	7b0b3094	bl 0x5ab276c
0x4eaf984	683a40b9	ldr w8, [x19, #0x38]
0x4eaf988	08050071	subs w8, w8, #0x1
0x4eaf98c	4b000054	b.lt 0x4eaf994
0x4eaf990	683a00b9	str w8, [x19, #0x38]
0x4eaf994	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf998	1f0109eb	cmp x8, x9
0x4eaf99c	82abff54	b.hs 0x4eaef0c
0x4eaf9a0	09014039	ldrb w9, [x8]
0x4eaf9a4	3fa90171	cmp w9, #0x6a
0x4eaf9a8	21abff54	b.ne 0x4eaef0c
0x4eaf9ac	08050091	add x8, x8, #0x1
0x4eaf9b0	680600f9	str x8, [x19, #0x8]
0x4eaf9b4	887640b9	ldr w8, [x20, #0x74]
0x4eaf9b8	08011432	orr w8, w8, #0x1000
0x4eaf9bc	887600b9	str w8, [x20, #0x74]
0x4eaf9c0	953240f9	ldr x21, [x20, #0x60]
0x4eaf9c4	150100b5	cbnz x21, 0x4eaf9e4
0x4eaf9c8	00038052	mov w0, #0x18
0x4eaf9cc	99418a94	bl 0x7140030
0x4eaf9d0	f50300aa	mov x21, x0
0x4eaf9d4	180000f9	str x24, [x0]
0x4eaf9d8	1fc000f8	stur xzr, [x0, #0xc]
0x4eaf9dc	1f100079	strh wzr, [x0, #0x8]
0x4eaf9e0	803200f9	str x0, [x20, #0x60]
0x4eaf9e4	f90f00b9	str w25, [sp, #0xc]
0x4eaf9e8	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eaf9ec	1f0109eb	cmp x8, x9
0x4eaf9f0	e2000054	b.hs 0x4eafa0c
0x4eaf9f4	0901c039	ldrsb w9, [x8]
0x4eaf9f8	a900f837	tbnz w9, #0x1f, 0x4eafa0c
0x4eaf9fc	e90f00b9	str w9, [sp, #0xc]
0x4eafa00	08050091	add x8, x8, #0x1
0x4eafa04	680600f9	str x8, [x19, #0x8]
0x4eafa08	05000014	b 0x4eafa1c
0x4eafa0c	e1330091	add x1, sp, #0xc
0x4eafa10	e00313aa	mov x0, x19
0x4eafa14	230d3094	bl 0x5ab2ea0
0x4eafa18	c00b0034	cbz w0, 0x4eafb90
0x4eafa1c	68264729	ldp w8, w9, [x19, #0x38]
0x4eafa20	0a050011	add w10, w8, #0x1
0x4eafa24	6a3a00b9	str w10, [x19, #0x38]
0x4eafa28	1f01096b	cmp w8, w9
0x4eafa2c	2a0b0054	b.ge 0x4eafb90
0x4eafa30	e10f40b9	ldr w1, [sp, #0xc]
0x4eafa34	e00313aa	mov x0, x19
0x4eafa38	2e0b3094	bl 0x5ab26f0
0x4eafa3c	f60300aa	mov x22, x0
0x4eafa40	e00315aa	mov x0, x21
0x4eafa44	e10313aa	mov x1, x19
0x4eafa48	e4f7ff97	bl 0x4ead9d8
0x4eafa4c	200a0034	cbz w0, 0x4eafb90
0x4eafa50	68924039	ldrb w8, [x19, #0x24]
0x4eafa54	1f050071	cmp w8, #0x1
0x4eafa58	c1090054	b.ne 0x4eafb90
0x4eafa5c	e00313aa	mov x0, x19
0x4eafa60	e10316aa	mov x1, x22
0x4eafa64	420b3094	bl 0x5ab276c
0x4eafa68	683a40b9	ldr w8, [x19, #0x38]
0x4eafa6c	08050071	subs w8, w8, #0x1
0x4eafa70	4b000054	b.lt 0x4eafa78
0x4eafa74	683a00b9	str w8, [x19, #0x38]
0x4eafa78	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eafa7c	1f0109eb	cmp x8, x9
0x4eafa80	62a4ff54	b.hs 0x4eaef0c
0x4eafa84	09014039	ldrb w9, [x8]
0x4eafa88	3fc90171	cmp w9, #0x72
0x4eafa8c	01a4ff54	b.ne 0x4eaef0c
0x4eafa90	08050091	add x8, x8, #0x1
0x4eafa94	680600f9	str x8, [x19, #0x8]
0x4eafa98	887640b9	ldr w8, [x20, #0x74]
0x4eafa9c	08011332	orr w8, w8, #0x2000
0x4eafaa0	887600b9	str w8, [x20, #0x74]
0x4eafaa4	953640f9	ldr x21, [x20, #0x68]
0x4eafaa8	150100b5	cbnz x21, 0x4eafac8
0x4eafaac	00038052	mov w0, #0x18
0x4eafab0	60418a94	bl 0x7140030
0x4eafab4	f50300aa	mov x21, x0
0x4eafab8	1b0000f9	str x27, [x0]
0x4eafabc	1fc000f8	stur xzr, [x0, #0xc]
0x4eafac0	1f200039	strb wzr, [x0, #0x8]
0x4eafac4	803600f9	str x0, [x20, #0x68]
0x4eafac8	f90f00b9	str w25, [sp, #0xc]
0x4eafacc	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eafad0	1f0109eb	cmp x8, x9
0x4eafad4	e2000054	b.hs 0x4eafaf0
0x4eafad8	0901c039	ldrsb w9, [x8]
0x4eafadc	a900f837	tbnz w9, #0x1f, 0x4eafaf0
0x4eafae0	e90f00b9	str w9, [sp, #0xc]
0x4eafae4	08050091	add x8, x8, #0x1
0x4eafae8	680600f9	str x8, [x19, #0x8]
0x4eafaec	05000014	b 0x4eafb00
0x4eafaf0	e1330091	add x1, sp, #0xc
0x4eafaf4	e00313aa	mov x0, x19
0x4eafaf8	ea0c3094	bl 0x5ab2ea0
0x4eafafc	a0040034	cbz w0, 0x4eafb90
0x4eafb00	68264729	ldp w8, w9, [x19, #0x38]
0x4eafb04	0a050011	add w10, w8, #0x1
0x4eafb08	6a3a00b9	str w10, [x19, #0x38]
0x4eafb0c	1f01096b	cmp w8, w9
0x4eafb10	0a040054	b.ge 0x4eafb90
0x4eafb14	e10f40b9	ldr w1, [sp, #0xc]
0x4eafb18	e00313aa	mov x0, x19
0x4eafb1c	f50a3094	bl 0x5ab26f0
0x4eafb20	f60300aa	mov x22, x0
0x4eafb24	e00315aa	mov x0, x21
0x4eafb28	e10313aa	mov x1, x19
0x4eafb2c	05f9ff97	bl 0x4eadf40
0x4eafb30	00030034	cbz w0, 0x4eafb90
0x4eafb34	68924039	ldrb w8, [x19, #0x24]
0x4eafb38	1f050071	cmp w8, #0x1
0x4eafb3c	a1020054	b.ne 0x4eafb90
0x4eafb40	e00313aa	mov x0, x19
0x4eafb44	e10316aa	mov x1, x22
0x4eafb48	090b3094	bl 0x5ab276c
0x4eafb4c	683a40b9	ldr w8, [x19, #0x38]
0x4eafb50	08050071	subs w8, w8, #0x1
0x4eafb54	4b000054	b.lt 0x4eafb5c
0x4eafb58	683a00b9	str w8, [x19, #0x38]
0x4eafb5c	68a640a9	ldp x8, x9, [x19, #0x8]
0x4eafb60	1f0109eb	cmp x8, x9
0x4eafb64	419dff54	b.ne 0x4eaef0c
0x4eafb68	682e40b9	ldr w8, [x19, #0x2c]
0x4eafb6c	a8000035	cbnz w8, 0x4eafb80
0x4eafb70	681a40b9	ldr w8, [x19, #0x18]
0x4eafb74	692a40b9	ldr w9, [x19, #0x28]
0x4eafb78	1f01096b	cmp w8, w9
0x4eafb7c	819cff54	b.ne 0x4eaef0c
0x4eafb80	7f2200b9	str wzr, [x19, #0x20]
0x4eafb84	20008052	mov w0, #0x1
0x4eafb88	60920039	strb w0, [x19, #0x24]
0x4eafb8c	04000014	b 0x4eafb9c
0x4eafb90	00008052	mov w0, #0x0
0x4eafb94	02000014	b 0x4eafb9c
0x4eafb98	20008052	mov w0, #0x1
0x4eafb9c	fd7b46a9	ldp x29, x30, [sp, #0x60]
0x4eafba0	f44f45a9	ldp x20, x19, [sp, #0x50]
0x4eafba4	f65744a9	ldp x22, x21, [sp, #0x40]
0x4eafba8	f85f43a9	ldp x24, x23, [sp, #0x30]
0x4eafbac	fa6742a9	ldp x26, x25, [sp, #0x20]
0x4eafbb0	fc6f41a9	ldp x28, x27, [sp, #0x10]
0x4eafbb4	ffc30191	add sp, sp, #0x70
0x4eafbb8	c0035fd6	ret
