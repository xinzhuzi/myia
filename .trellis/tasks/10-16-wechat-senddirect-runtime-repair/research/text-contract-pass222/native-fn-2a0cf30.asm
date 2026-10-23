0x2a0cf30	f657bda9	stp x22,x21,[sp, #-0x30]!
0x2a0cf34	f44f01a9	stp x20,x19,[sp, #0x10]
0x2a0cf38	fd7b02a9	stp x29,x30,[sp, #0x20]
0x2a0cf3c	fd830091	add x29,sp,#0x20
0x2a0cf40	f40301aa	mov x20,x1
0x2a0cf44	f30300aa	mov x19,x0
0x2a0cf48	28a50390	adrp x8,0x9eb0000
0x2a0cf4c	08811391	add x8,x8,#0x4e0
0x2a0cf50	08410091	add x8,x8,#0x10
0x2a0cf54	080000f9	str x8,[x0]
0x2a0cf58	280440f9	ldr x8,[x1, #0x8]
0x2a0cf5c	291040b9	ldr w9,[x1, #0x10]
0x2a0cf60	091000b9	str w9,[x0, #0x10]
0x2a0cf64	080400f9	str x8,[x0, #0x8]
0x2a0cf68	2080c13c	ldur q0,[x1, #0x18]
0x2a0cf6c	281440f9	ldr x8,[x1, #0x28]
0x2a0cf70	081400f9	str x8,[x0, #0x28]
0x2a0cf74	0080813c	stur q0,[x0, #0x18]
0x2a0cf78	3f7c02a9	stp xzr,xzr,[x1, #0x20]
0x2a0cf7c	3f0c00f9	str xzr,[x1, #0x18]
0x2a0cf80	200cc03d	ldr q0,[x1, #0x30]
0x2a0cf84	282040f9	ldr x8,[x1, #0x40]
0x2a0cf88	082000f9	str x8,[x0, #0x40]
0x2a0cf8c	000c803d	str q0,[x0, #0x30]
0x2a0cf90	3ffc03a9	stp xzr,xzr,[x1, #0x38]
0x2a0cf94	3f1800f9	str xzr,[x1, #0x30]
0x2a0cf98	2080c43c	ldur q0,[x1, #0x48]
0x2a0cf9c	282c40f9	ldr x8,[x1, #0x58]
0x2a0cfa0	082c00f9	str x8,[x0, #0x58]
0x2a0cfa4	0080843c	stur q0,[x0, #0x48]
0x2a0cfa8	3ffc04a9	stp xzr,xzr,[x1, #0x48]
0x2a0cfac	3f2c00f9	str xzr,[x1, #0x58]
0x2a0cfb0	2018c03d	ldr q0,[x1, #0x60]
0x2a0cfb4	283840f9	ldr x8,[x1, #0x70]
0x2a0cfb8	083800f9	str x8,[x0, #0x70]
0x2a0cfbc	0018803d	str q0,[x0, #0x60]
0x2a0cfc0	3f7c06a9	stp xzr,xzr,[x1, #0x60]
0x2a0cfc4	3f3800f9	str xzr,[x1, #0x70]
0x2a0cfc8	2080c73c	ldur q0,[x1, #0x78]
0x2a0cfcc	284440f9	ldr x8,[x1, #0x88]
0x2a0cfd0	084400f9	str x8,[x0, #0x88]
0x2a0cfd4	0080873c	stur q0,[x0, #0x78]
0x2a0cfd8	3ffc07a9	stp xzr,xzr,[x1, #0x78]
0x2a0cfdc	3f4400f9	str xzr,[x1, #0x88]
0x2a0cfe0	28204179	ldrh w8,[x1, #0x90]
0x2a0cfe4	08200179	strh w8,[x0, #0x90]
0x2a0cfe8	284c40f9	ldr x8,[x1, #0x98]
0x2a0cfec	3f4c00f9	str xzr,[x1, #0x98]
0x2a0cff0	f50300aa	mov x21,x0
0x2a0cff4	a88e09f8	str x8,[x21, #0x98]!
0x2a0cff8	295040f9	ldr x9,[x1, #0xa0]
0x2a0cffc	095000f9	str x9,[x0, #0xa0]
0x2a0d000	3f5000f9	str xzr,[x1, #0xa0]
0x2a0d004	e90301aa	mov x9,x1
0x2a0d008	2b8d4af8	ldr x11,[x9, #0xa8]!
0x2a0d00c	ea0300aa	mov x10,x0
0x2a0d010	4b8d0af8	str x11,[x10, #0xa8]!
0x2a0d014	2c0540f9	ldr x12,[x9, #0x8]
0x2a0d018	4c0500f9	str x12,[x10, #0x8]
0x2a0d01c	2d1140b9	ldr w13,[x9, #0x10]
0x2a0d020	4d1100b9	str w13,[x10, #0x10]
0x2a0d024	cc0100b4	cbz x12,0x02a0d05c
0x2a0d028	6b0540f9	ldr x11,[x11, #0x8]
0x2a0d02c	6c5240f9	ldr x12,[x19, #0xa0]
0x2a0d030	8d0500d1	sub x13,x12,#0x1
0x2a0d034	9f010dea	tst x12,x13
0x2a0d038	61000054	b.ne 0x02a0d044
0x2a0d03c	ab010b8a	and x11,x13,x11
0x2a0d040	05000014	b 0x02a0d054
0x2a0d044	7f010ceb	cmp x11,x12
0x2a0d048	63000054	b.cc 0x02a0d054
0x2a0d04c	6d09cc9a	udiv x13,x11,x12
0x2a0d050	abad0c9b	msub x11,x13,x12,x11
0x2a0d054	0a792bf8	str x10,[x8, x11, LSL #0x3]
0x2a0d058	3f7d00a9	stp xzr,xzr,[x9]
0x2a0d05c	8032c03d	ldr q0,[x20, #0xc0]
0x2a0d060	886a40f9	ldr x8,[x20, #0xd0]
0x2a0d064	686a00f9	str x8,[x19, #0xd0]
0x2a0d068	6032803d	str q0,[x19, #0xc0]
0x2a0d06c	9ffe0ca9	stp xzr,xzr,[x20, #0xc8]
0x2a0d070	9f6200f9	str xzr,[x20, #0xc0]
0x2a0d074	8082cd3c	ldur q0,[x20, #0xd8]
0x2a0d078	887640f9	ldr x8,[x20, #0xe8]
0x2a0d07c	687600f9	str x8,[x19, #0xe8]
0x2a0d080	60828d3c	stur q0,[x19, #0xd8]
0x2a0d084	9f7e0ea9	stp xzr,xzr,[x20, #0xe0]
0x2a0d088	9f6e00f9	str xzr,[x20, #0xd8]
0x2a0d08c	68c20391	add x8,x19,#0xf0
0x2a0d090	89c20391	add x9,x20,#0xf0
0x2a0d094	808647ad	ldp q0,q1,[x20, #0xf0]
0x2a0d098	8246c03d	ldr q2,[x20, #0x110]
0x2a0d09c	23c1c23c	ldur q3,[x9, #0x2c]
0x2a0d0a0	03c1823c	stur q3,[x8, #0x2c]
0x2a0d0a4	610a08ad	stp q1,q2,[x19, #0x100]
0x2a0d0a8	603e803d	str q0,[x19, #0xf0]
0x2a0d0ac	804ec03d	ldr q0,[x20, #0x130]
0x2a0d0b0	88a240f9	ldr x8,[x20, #0x140]
0x2a0d0b4	68a200f9	str x8,[x19, #0x140]
0x2a0d0b8	604e803d	str q0,[x19, #0x130]
0x2a0d0bc	9f7e13a9	stp xzr,xzr,[x20, #0x130]
0x2a0d0c0	9fa200f9	str xzr,[x20, #0x140]
0x2a0d0c4	68220591	add x8,x19,#0x148
0x2a0d0c8	89220591	add x9,x20,#0x148
0x2a0d0cc	2001c03d	ldr q0,[x9]
0x2a0d0d0	89ae40f9	ldr x9,[x20, #0x158]
0x2a0d0d4	69ae00f9	str x9,[x19, #0x158]
0x2a0d0d8	0001803d	str q0,[x8]
0x2a0d0dc	9ffe14a9	stp xzr,xzr,[x20, #0x148]
0x2a0d0e0	9fae00f9	str xzr,[x20, #0x158]
0x2a0d0e4	805ac03d	ldr q0,[x20, #0x160]
0x2a0d0e8	88ba40f9	ldr x8,[x20, #0x170]
0x2a0d0ec	68ba00f9	str x8,[x19, #0x170]
0x2a0d0f0	605a803d	str q0,[x19, #0x160]
0x2a0d0f4	9f7e16a9	stp xzr,xzr,[x20, #0x160]
0x2a0d0f8	9fba00f9	str xzr,[x20, #0x170]
0x2a0d0fc	76e20591	add x22,x19,#0x178
0x2a0d100	88e20591	add x8,x20,#0x178
0x2a0d104	7ffe17a9	stp xzr,xzr,[x19, #0x178]
0x2a0d108	7fc600f9	str xzr,[x19, #0x188]
0x2a0d10c	0001c03d	ldr q0,[x8]
0x2a0d110	c002803d	str q0,[x22]
0x2a0d114	88c640f9	ldr x8,[x20, #0x188]
0x2a0d118	68c600f9	str x8,[x19, #0x188]
0x2a0d11c	9ffe17a9	stp xzr,xzr,[x20, #0x178]
0x2a0d120	9fc600f9	str xzr,[x20, #0x188]
0x2a0d124	60420691	add x0,x19,#0x190
0x2a0d128	81420691	add x1,x20,#0x190
0x2a0d12c	cf859294	bl 0x04eae868
0x2a0d130	88220891	add x8,x20,#0x208
0x2a0d134	890641f9	ldr x9,[x20, #0x208]
0x2a0d138	690601f9	str x9,[x19, #0x208]
0x2a0d13c	890a41f9	ldr x9,[x20, #0x210]
0x2a0d140	690a01f9	str x9,[x19, #0x210]
0x2a0d144	00e4006f	movi v0.2D,#0x0
0x2a0d148	0001803d	str q0,[x8]
0x2a0d14c	88624839	ldrb w8,[x20, #0x218]
0x2a0d150	68620839	strb w8,[x19, #0x218]
0x2a0d154	818ac03d	ldr q1,[x20, #0x220]
0x2a0d158	618a803d	str q1,[x19, #0x220]
0x2a0d15c	808a803d	str q0,[x20, #0x220]
0x2a0d160	818ec03d	ldr q1,[x20, #0x230]
0x2a0d164	618e803d	str q1,[x19, #0x230]
0x2a0d168	808e803d	str q0,[x20, #0x230]
0x2a0d16c	88024939	ldrb w8,[x20, #0x240]
0x2a0d170	68020939	strb w8,[x19, #0x240]
0x2a0d174	88220991	add x8,x20,#0x248
0x2a0d178	892641f9	ldr x9,[x20, #0x248]
0x2a0d17c	692601f9	str x9,[x19, #0x248]
0x2a0d180	892a41f9	ldr x9,[x20, #0x250]
0x2a0d184	692a01f9	str x9,[x19, #0x250]
0x2a0d188	0001803d	str q0,[x8]
0x2a0d18c	88624939	ldrb w8,[x20, #0x258]
0x2a0d190	68620939	strb w8,[x19, #0x258]
0x2a0d194	809ac03d	ldr q0,[x20, #0x260]
0x2a0d198	883a41f9	ldr x8,[x20, #0x270]
0x2a0d19c	683a01f9	str x8,[x19, #0x270]
0x2a0d1a0	609a803d	str q0,[x19, #0x260]
0x2a0d1a4	9f3a01f9	str xzr,[x20, #0x270]
0x2a0d1a8	9f3601f9	str xzr,[x20, #0x268]
0x2a0d1ac	9f3201f9	str xzr,[x20, #0x260]
0x2a0d1b0	e00313aa	mov x0,x19
0x2a0d1b4	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x2a0d1b8	f44f41a9	ldp x20,x19,[sp, #0x10]
0x2a0d1bc	f657c3a8	ldp x22,x21,[sp], #0x30
0x2a0d1c0	c0035fd6	ret
