0x4c6b5b8	ff8304d1	sub sp,sp,#0x120
0x4c6b5bc	fc6f0ca9	stp x28,x27,[sp, #0xc0]
0x4c6b5c0	fa670da9	stp x26,x25,[sp, #0xd0]
0x4c6b5c4	f85f0ea9	stp x24,x23,[sp, #0xe0]
0x4c6b5c8	f6570fa9	stp x22,x21,[sp, #0xf0]
0x4c6b5cc	f44f10a9	stp x20,x19,[sp, #0x100]
0x4c6b5d0	fd7b11a9	stp x29,x30,[sp, #0x110]
0x4c6b5d4	fd430491	add x29,sp,#0x110
0x4c6b5d8	f50301aa	mov x21,x1
0x4c6b5dc	f40300aa	mov x20,x0
0x4c6b5e0	f30308aa	mov x19,x8
0x4c6b5e4	f8f301b2	orr x24,xzr,#-0x5555555555555556
0x4c6b5e8	186100a9	stp x24,x24,[x8]
0x4c6b5ec	00cf8052	mov w0,#0x678
0x4c6b5f0	90529394	bl 0x07140030
0x4c6b5f4	f60300aa	mov x22,x0
0x4c6b5f8	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x4c6b5fc	288202b0	adrp x8,0x9cb0000
0x4c6b600	08e11a91	add x8,x8,#0x6b8
0x4c6b604	080000f9	str x8,[x0]
0x4c6b608	17600091	add x23,x0,#0x18
0x4c6b60c	e00317aa	mov x0,x23
0x4c6b610	01cc8052	mov w1,#0x660
0x4c6b614	5f539394	bl 0x07140390
0x4c6b618	e00317aa	mov x0,x23
0x4c6b61c	8dc00d97	bl 0x00fdb850
0x4c6b620	689202f0	adrp x8,0x9eba000
0x4c6b624	08410591	add x8,x8,#0x150
0x4c6b628	08410091	add x8,x8,#0x10
0x4c6b62c	c80e00f9	str x8,[x22, #0x18]
0x4c6b630	c8621691	add x8,x22,#0x598
0x4c6b634	c9fe1791	add x9,x22,#0x5ff
0x4c6b638	cabe1891	add x10,x22,#0x62f
0x4c6b63c	5f010079	strh wzr,[x10]
0x4c6b640	ca1e1991	add x10,x22,#0x647
0x4c6b644	5f010079	strh wzr,[x10]
0x4c6b648	df7e1939	strb wzr,[x22, #0x65f]
0x4c6b64c	df6206b9	str wzr,[x22, #0x660]
0x4c6b650	df3603f9	str xzr,[x22, #0x668]
0x4c6b654	df7206b9	str wzr,[x22, #0x670]
0x4c6b658	dfa21739	strb wzr,[x22, #0x5e8]
0x4c6b65c	00e4006f	movi v0.2D,#0x0
0x4c6b660	000100ad	stp q0,q0,[x8]
0x4c6b664	000101ad	stp q0,q0,[x8, #0x20]
0x4c6b668	0011803d	str q0,[x8, #0x40]
0x4c6b66c	3ffd00a9	stp xzr,xzr,[x9, #0x8]
0x4c6b670	3f0100f9	str xzr,[x9]
0x4c6b674	3f310079	strh wzr,[x9, #0x18]
0x4c6b678	775a00a9	stp x23,x22,[x19]
0x4c6b67c	b8633aa9	stp x24,x24,[x29, #-0x60]
0x4c6b680	a00240f9	ldr x0,[x21]
0x4c6b684	a88301d1	sub x8,x29,#0x60
0x4c6b688	d70bb697	bl 0x039ee5e4
0x4c6b68c	bfff38a9	stp xzr,xzr,[x29, #-0x78]
0x4c6b690	bf8319f8	stur xzr,[x29, #-0x68]
0x4c6b694	982241a9	ldp x24,x8,[x20, #0x10]
0x4c6b698	190118eb	subs x25,x8,x24
0x4c6b69c	c0010054	b.eq 0x04c6b6d4
0x4c6b6a0	d945f8b7	tbnz x25,#0x3f,0x04c6bf58
0x4c6b6a4	e00319aa	mov x0,x25
0x4c6b6a8	62529394	bl 0x07140030
0x4c6b6ac	f70300aa	mov x23,x0
0x4c6b6b0	1a00198b	add x26,x0,x25
0x4c6b6b4	a08318f8	stur x0,[x29, #-0x78]
0x4c6b6b8	ba8319f8	stur x26,[x29, #-0x68]
0x4c6b6bc	e10318aa	mov x1,x24
0x4c6b6c0	e20319aa	mov x2,x25
0x4c6b6c4	f1559394	bl 0x07140e88
0x4c6b6c8	e2031aaa	mov x2,x26
0x4c6b6cc	ba0319f8	stur x26,[x29, #-0x70]
0x4c6b6d0	03000014	b 0x04c6b6dc
0x4c6b6d4	020080d2	mov x2,#0x0
0x4c6b6d8	170080d2	mov x23,#0x0
0x4c6b6dc	480017cb	sub x8,x2,x23
0x4c6b6e0	03fd4293	asr x3,x8,#0x2
0x4c6b6e4	c0e21691	add x0,x22,#0x5b8
0x4c6b6e8	e10317aa	mov x1,x23
0x4c6b6ec	8a442397	bl 0x0153c914
0x4c6b6f0	a08358f8	ldur x0,[x29, #-0x78]
0x4c6b6f4	a00000b4	cbz x0,0x04c6b708
0x4c6b6f8	a00319f8	stur x0,[x29, #-0x70]
0x4c6b6fc	a88359f8	ldur x8,[x29, #-0x68]
0x4c6b700	010100cb	sub x1,x8,x0
0x4c6b704	42529394	bl 0x0714000c
0x4c6b708	760240f9	ldr x22,[x19]
0x4c6b70c	a80240f9	ldr x8,[x21]
0x4c6b710	09a940b9	ldr w9,[x8, #0xa8]
0x4c6b714	c9c605b9	str w9,[x22, #0x5c4]
0x4c6b718	097540b9	ldr w9,[x8, #0x74]
0x4c6b71c	c9c205b9	str w9,[x22, #0x5c0]
0x4c6b720	c0421791	add x0,x22,#0x5d0
0x4c6b724	01610191	add x1,x8,#0x58
0x4c6b728	6e509394	bl 0x0713f8e0
0x4c6b72c	a80240f9	ldr x8,[x21]
0x4c6b730	093dc739	ldrsb w9,[x8, #0x1cf]
0x4c6b734	e900f837	tbnz w9,#0x1f,0x04c6b750
0x4c6b738	08e10691	add x8,x8,#0x1b8
0x4c6b73c	0001c03d	ldr q0,[x8]
0x4c6b740	e023803d	str q0,[sp, #0x80]
0x4c6b744	080940f9	ldr x8,[x8, #0x10]
0x4c6b748	e84b00f9	str x8,[sp, #0x90]
0x4c6b74c	04000014	b 0x04c6b75c
0x4c6b750	01895ba9	ldp x1,x2,[x8, #0x1b8]
0x4c6b754	e0030291	add x0,sp,#0x80
0x4c6b758	72b5ce96	bl 0x00018d20
0x4c6b75c	c0a21791	add x0,x22,#0x5e8
0x4c6b760	e1030291	add x1,sp,#0x80
0x4c6b764	5f509394	bl 0x0713f8e0
0x4c6b768	e85fc239	ldrsb w8,[sp, #0x97]
0x4c6b76c	a800f836	tbz w8,#0x1f,0x04c6b780
0x4c6b770	e04340f9	ldr x0,[sp, #0x80]
0x4c6b774	e84b40f9	ldr x8,[sp, #0x90]
0x4c6b778	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6b77c	24529394	bl 0x0714000c
0x4c6b780	a80240f9	ldr x8,[x21]
0x4c6b784	000940b9	ldr w0,[x8, #0x8]
0x4c6b788	1fc40071	cmp w0,#0x31
0x4c6b78c	81000054	b.ne 0x04c6b79c
0x4c6b790	080d40b9	ldr w8,[x8, #0xc]
0x4c6b794	29068052	mov w9,#0x31
0x4c6b798	208108aa	orr x0,x9,x8, LSL #0x20
0x4c6b79c	dc5cf897	bl 0x04a82b0c
0x4c6b7a0	c00a00b9	str w0,[x22, #0x8]
0x4c6b7a4	a00240f9	ldr x0,[x21]
0x4c6b7a8	080840b9	ldr w8,[x0, #0x8]
0x4c6b7ac	1fc50071	cmp w8,#0x31
0x4c6b7b0	e1040054	b.ne 0x04c6b84c
0x4c6b7b4	080c41f9	ldr x8,[x0, #0x218]
0x4c6b7b8	480200b4	cbz x8,0x04c6b800
0x4c6b7bc	219202d0	adrp x1,0x9eb1000
0x4c6b7c0	21000191	add x1,x1,#0x40
0x4c6b7c4	229202b0	adrp x2,0x9eb0000
0x4c6b7c8	42003391	add x2,x2,#0xcc0
0x4c6b7cc	f70300aa	mov x23,x0
0x4c6b7d0	e00308aa	mov x0,x8
0x4c6b7d4	030080d2	mov x3,#0x0
0x4c6b7d8	55529394	bl 0x0714012c
0x4c6b7dc	200100b4	cbz x0,0x04c6b800
0x4c6b7e0	e80300aa	mov x8,x0
0x4c6b7e4	e91241f9	ldr x9,[x23, #0x220]
0x4c6b7e8	e02708a9	stp x0,x9,[sp, #0x80]
0x4c6b7ec	e90000b4	cbz x9,0x04c6b808
0x4c6b7f0	29210091	add x9,x9,#0x8
0x4c6b7f4	2a008052	mov w10,#0x1
0x4c6b7f8	29012af8	ldadd x10,x9,[x9]
0x4c6b7fc	03000014	b 0x04c6b808
0x4c6b800	080080d2	mov x8,#0x0
0x4c6b804	ff7f08a9	stp xzr,xzr,[sp, #0x80]
0x4c6b808	c0c20191	add x0,x22,#0x70
0x4c6b80c	01811191	add x1,x8,#0x460
0x4c6b810	34509394	bl 0x0713f8e0
0x4c6b814	f64740f9	ldr x22,[sp, #0x88]
0x4c6b818	760100b4	cbz x22,0x04c6b844
0x4c6b81c	c8220091	add x8,x22,#0x8
0x4c6b820	09008092	mov x9,#-0x1
0x4c6b824	0801e9f8	ldaddal x9,x8,[x8]
0x4c6b828	e80000b5	cbnz x8,0x04c6b844
0x4c6b82c	c80240f9	ldr x8,[x22]
0x4c6b830	080940f9	ldr x8,[x8, #0x10]
0x4c6b834	e00316aa	mov x0,x22
0x4c6b838	00013fd6	blr x8
0x4c6b83c	e00316aa	mov x0,x22
0x4c6b840	f7509394	bl 0x0713fc1c
0x4c6b844	760240f9	ldr x22,[x19]
0x4c6b848	a00240f9	ldr x0,[x21]
0x4c6b84c	e8030291	add x8,sp,#0x80
0x4c6b850	a570f897	bl 0x04a87ae4
0x4c6b854	c0e20291	add x0,x22,#0xb8
0x4c6b858	e1030291	add x1,sp,#0x80
0x4c6b85c	21509394	bl 0x0713f8e0
0x4c6b860	e85fc239	ldrsb w8,[sp, #0x97]
0x4c6b864	a800f836	tbz w8,#0x1f,0x04c6b878
0x4c6b868	e04340f9	ldr x0,[sp, #0x80]
0x4c6b86c	e84b40f9	ldr x8,[sp, #0x90]
0x4c6b870	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6b874	e6519394	bl 0x0714000c
0x4c6b878	760240f9	ldr x22,[x19]
0x4c6b87c	a80240f9	ldr x8,[x21]
0x4c6b880	c0c20c91	add x0,x22,#0x330
0x4c6b884	01610191	add x1,x8,#0x58
0x4c6b888	16509394	bl 0x0713f8e0
0x4c6b88c	a80240f9	ldr x8,[x21]
0x4c6b890	01a940b9	ldr w1,[x8, #0xa8]
0x4c6b894	e1000034	cbz w1,0x04c6b8b0
0x4c6b898	e8030291	add x8,sp,#0x80
0x4c6b89c	40020094	bl 0x04c6c19c
0x4c6b8a0	c0620491	add x0,x22,#0x118
0x4c6b8a4	e1030291	add x1,sp,#0x80
0x4c6b8a8	0e509394	bl 0x0713f8e0
0x4c6b8ac	0b000014	b 0x04c6b8d8
0x4c6b8b0	b1f7e797	bl 0x04669774
0x4c6b8b4	080040f9	ldr x8,[x0]
0x4c6b8b8	082940f9	ldr x8,[x8, #0x50]
0x4c6b8bc	00013fd6	blr x8
0x4c6b8c0	e8030291	add x8,sp,#0x80
0x4c6b8c4	e10300aa	mov x1,x0
0x4c6b8c8	35020094	bl 0x04c6c19c
0x4c6b8cc	c0620491	add x0,x22,#0x118
0x4c6b8d0	e1030291	add x1,sp,#0x80
0x4c6b8d4	03509394	bl 0x0713f8e0
0x4c6b8d8	e85fc239	ldrsb w8,[sp, #0x97]
0x4c6b8dc	a800f836	tbz w8,#0x1f,0x04c6b8f0
0x4c6b8e0	e04340f9	ldr x0,[sp, #0x80]
0x4c6b8e4	e84b40f9	ldr x8,[sp, #0x90]
0x4c6b8e8	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6b8ec	c8519394	bl 0x0714000c
0x4c6b8f0	a00240f9	ldr x0,[x21]
0x4c6b8f4	e8030291	add x8,sp,#0x80
0x4c6b8f8	cb3f0394	bl 0x04d3b824
0x4c6b8fc	c0a20391	add x0,x22,#0xe8
0x4c6b900	e1030291	add x1,sp,#0x80
0x4c6b904	f74f9394	bl 0x0713f8e0
0x4c6b908	e85fc239	ldrsb w8,[sp, #0x97]
0x4c6b90c	a800f836	tbz w8,#0x1f,0x04c6b920
0x4c6b910	e04340f9	ldr x0,[sp, #0x80]
0x4c6b914	e84b40f9	ldr x8,[sp, #0x90]
0x4c6b918	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6b91c	bc519394	bl 0x0714000c
0x4c6b920	a00240f9	ldr x0,[x21]
0x4c6b924	087440b9	ldr w8,[x0, #0x74]
0x4c6b928	c84a03b9	str w8,[x22, #0x348]
0x4c6b92c	085040f9	ldr x8,[x0, #0xa0]
0x4c6b930	c8de02f9	str x8,[x22, #0x5b8]
0x4c6b934	08a840b9	ldr w8,[x0, #0xa8]
0x4c6b938	c84e03b9	str w8,[x22, #0x34c]
0x4c6b93c	763c0394	bl 0x04d3ab14
0x4c6b940	c0a20f39	strb w0,[x22, #0x3e8]
0x4c6b944	a00240f9	ldr x0,[x21]
0x4c6b948	283c0394	bl 0x04d3a9e8
0x4c6b94c	c0a60f39	strb w0,[x22, #0x3e9]
0x4c6b950	a00240f9	ldr x0,[x21]
0x4c6b954	d9df4a97	bl 0x01f238b8
0x4c6b958	c03a04b9	str w0,[x22, #0x438]
0x4c6b95c	a00240f9	ldr x0,[x21]
0x4c6b960	0aa3e397	bl 0x04554588
0x4c6b964	e10300aa	mov x1,x0
0x4c6b968	c0c20f91	add x0,x22,#0x3f0
0x4c6b96c	dd4f9394	bl 0x0713f8e0
0x4c6b970	a80240f9	ldr x8,[x21]
0x4c6b974	084940f9	ldr x8,[x8, #0x90]
0x4c6b978	c8b601f9	str x8,[x22, #0x368]
0x4c6b97c	680640f9	ldr x8,[x19, #0x8]
0x4c6b980	f62307a9	stp x22,x8,[sp, #0x70]
0x4c6b984	880000b4	cbz x8,0x04c6b994
0x4c6b988	08210091	add x8,x8,#0x8
0x4c6b98c	29008052	mov w9,#0x1
0x4c6b990	080129f8	ldadd x9,x8,[x8]
0x4c6b994	c8d642f9	ldr x8,[x22, #0x5a8]
0x4c6b998	01c15fb8	ldur w1,[x8, #-0x4]
0x4c6b99c	e8030291	add x8,sp,#0x80
0x4c6b9a0	e0c30191	add x0,sp,#0x70
0x4c6b9a4	7f6cf897	bl 0x04a86ba0
0x4c6b9a8	c0420091	add x0,x22,#0x10
0x4c6b9ac	e1030291	add x1,sp,#0x80
0x4c6b9b0	cc4f9394	bl 0x0713f8e0
0x4c6b9b4	e85fc239	ldrsb w8,[sp, #0x97]
0x4c6b9b8	a800f836	tbz w8,#0x1f,0x04c6b9cc
0x4c6b9bc	e04340f9	ldr x0,[sp, #0x80]
0x4c6b9c0	e84b40f9	ldr x8,[sp, #0x90]
0x4c6b9c4	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6b9c8	91519394	bl 0x0714000c
0x4c6b9cc	f63f40f9	ldr x22,[sp, #0x78]
0x4c6b9d0	760100b4	cbz x22,0x04c6b9fc
0x4c6b9d4	c8220091	add x8,x22,#0x8
0x4c6b9d8	09008092	mov x9,#-0x1
0x4c6b9dc	0801e9f8	ldaddal x9,x8,[x8]
0x4c6b9e0	e80000b5	cbnz x8,0x04c6b9fc
0x4c6b9e4	c80240f9	ldr x8,[x22]
0x4c6b9e8	080940f9	ldr x8,[x8, #0x10]
0x4c6b9ec	e00316aa	mov x0,x22
0x4c6b9f0	00013fd6	blr x8
0x4c6b9f4	e00316aa	mov x0,x22
0x4c6b9f8	89509394	bl 0x0713fc1c
0x4c6b9fc	760240f9	ldr x22,[x19]
0x4c6ba00	c0020191	add x0,x22,#0x40
0x4c6ba04	c1420091	add x1,x22,#0x10
0x4c6ba08	b64f9394	bl 0x0713f8e0
0x4c6ba0c	a80240f9	ldr x8,[x21]
0x4c6ba10	c0021891	add x0,x22,#0x600
0x4c6ba14	01410091	add x1,x8,#0x10
0x4c6ba18	b24f9394	bl 0x0713f8e0
0x4c6ba1c	a80240f9	ldr x8,[x21]
0x4c6ba20	c0621891	add x0,x22,#0x618
0x4c6ba24	01a10091	add x1,x8,#0x28
0x4c6ba28	ae4f9394	bl 0x0713f8e0
0x4c6ba2c	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x4c6ba30	e8a308a9	stp x8,x8,[sp, #0x88]
0x4c6ba34	e84300f9	str x8,[sp, #0x80]
0x4c6ba38	a80240f9	ldr x8,[x21]
0x4c6ba3c	095dc139	ldrsb w9,[x8, #0x57]
0x4c6ba40	c900f837	tbnz w9,#0x1f,0x04c6ba58
0x4c6ba44	0001c43c	ldur q0,[x8, #0x40]
0x4c6ba48	e023803d	str q0,[sp, #0x80]
0x4c6ba4c	080145f8	ldur x8,[x8, #0x50]
0x4c6ba50	e84b00f9	str x8,[sp, #0x90]
0x4c6ba54	04000014	b 0x04c6ba64
0x4c6ba58	010944a9	ldp x1,x2,[x8, #0x40]
0x4c6ba5c	e0030291	add x0,sp,#0x80
0x4c6ba60	b0b4ce96	bl 0x00018d20
0x4c6ba64	e85f4239	ldrb w8,[sp, #0x97]
0x4c6ba68	091d0013	sxtb w9,w8
0x4c6ba6c	ea4740f9	ldr x10,[sp, #0x88]
0x4c6ba70	3f010071	cmp w9,#0x0
0x4c6ba74	48b1889a	csel x8,x10,x8,lt
0x4c6ba78	a80000b5	cbnz x8,0x04c6ba8c
0x4c6ba7c	a80240f9	ldr x8,[x21]
0x4c6ba80	e0030291	add x0,sp,#0x80
0x4c6ba84	01410091	add x1,x8,#0x10
0x4c6ba88	964f9394	bl 0x0713f8e0
0x4c6ba8c	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x4c6ba90	e82306a9	stp x8,x8,[sp, #0x60]
0x4c6ba94	e82f00f9	str x8,[sp, #0x58]
0x4c6ba98	e8030091	mov x8,sp
0x4c6ba9c	83fce797	bl 0x0466aca8
0x4c6baa0	e00340f9	ldr x0,[sp]
0x4c6baa4	e8a30091	add x8,sp,#0x28
0x4c6baa8	26671697	bl 0x01205740
0x4c6baac	e01740f9	ldr x0,[sp, #0x28]
0x4c6bab0	e8030191	add x8,sp,#0x40
0x4c6bab4	56515a97	bl 0x0230000c
0x4c6bab8	e02340f9	ldr x0,[sp, #0x40]
0x4c6babc	e8630191	add x8,sp,#0x58
0x4c6bac0	e1030291	add x1,sp,#0x80
0x4c6bac4	d04a7997	bl 0x02abe604
0x4c6bac8	f62740f9	ldr x22,[sp, #0x48]
0x4c6bacc	760100b4	cbz x22,0x04c6baf8
0x4c6bad0	c8220091	add x8,x22,#0x8
0x4c6bad4	09008092	mov x9,#-0x1
0x4c6bad8	0801e9f8	ldaddal x9,x8,[x8]
0x4c6badc	e80000b5	cbnz x8,0x04c6baf8
0x4c6bae0	c80240f9	ldr x8,[x22]
0x4c6bae4	080940f9	ldr x8,[x8, #0x10]
0x4c6bae8	e00316aa	mov x0,x22
0x4c6baec	00013fd6	blr x8
0x4c6baf0	e00316aa	mov x0,x22
0x4c6baf4	4a509394	bl 0x0713fc1c
0x4c6baf8	f61b40f9	ldr x22,[sp, #0x30]
0x4c6bafc	760100b4	cbz x22,0x04c6bb28
0x4c6bb00	c8220091	add x8,x22,#0x8
0x4c6bb04	09008092	mov x9,#-0x1
0x4c6bb08	0801e9f8	ldaddal x9,x8,[x8]
0x4c6bb0c	e80000b5	cbnz x8,0x04c6bb28
0x4c6bb10	c80240f9	ldr x8,[x22]
0x4c6bb14	080940f9	ldr x8,[x8, #0x10]
0x4c6bb18	e00316aa	mov x0,x22
0x4c6bb1c	00013fd6	blr x8
0x4c6bb20	e00316aa	mov x0,x22
0x4c6bb24	3e509394	bl 0x0713fc1c
0x4c6bb28	f60740f9	ldr x22,[sp, #0x8]
0x4c6bb2c	760100b4	cbz x22,0x04c6bb58
0x4c6bb30	c8220091	add x8,x22,#0x8
0x4c6bb34	09008092	mov x9,#-0x1
0x4c6bb38	0801e9f8	ldaddal x9,x8,[x8]
0x4c6bb3c	e80000b5	cbnz x8,0x04c6bb58
0x4c6bb40	c80240f9	ldr x8,[x22]
0x4c6bb44	080940f9	ldr x8,[x8, #0x10]
0x4c6bb48	e00316aa	mov x0,x22
0x4c6bb4c	00013fd6	blr x8
0x4c6bb50	e00316aa	mov x0,x22
0x4c6bb54	32509394	bl 0x0713fc1c
0x4c6bb58	790240f9	ldr x25,[x19]
0x4c6bb5c	e82f40f9	ldr x8,[sp, #0x58]
0x4c6bb60	20030491	add x0,x25,#0x100
0x4c6bb64	01210491	add x1,x8,#0x108
0x4c6bb68	5e4f9394	bl 0x0713f8e0
0x4c6bb6c	000c8052	mov w0,#0x60
0x4c6bb70	30519394	bl 0x07140030
0x4c6bb74	f60300aa	mov x22,x0
0x4c6bb78	f80300aa	mov x24,x0
0x4c6bb7c	1f8f00f8	str xzr,[x24, #0x8]!
0x4c6bb80	288102d0	adrp x8,0x9c91000
0x4c6bb84	08813b91	add x8,x8,#0xee0
0x4c6bb88	1f0800f9	str xzr,[x0, #0x10]
0x4c6bb8c	080000f9	str x8,[x0]
0x4c6bb90	00e4006f	movi v0.2D,#0x0
0x4c6bb94	f70300aa	mov x23,x0
0x4c6bb98	e08e813c	str q0,[x23, #0x18]!
0x4c6bb9c	0080823c	stur q0,[x0, #0x28]
0x4c6bba0	0080833c	stur q0,[x0, #0x38]
0x4c6bba4	0080843c	stur q0,[x0, #0x48]
0x4c6bba8	1f2c00f9	str xzr,[x0, #0x58]
0x4c6bbac	f78302a9	stp x23,x0,[sp, #0x28]
0x4c6bbb0	e8030191	add x8,sp,#0x40
0x4c6bbb4	e0030291	add x0,sp,#0x80
0x4c6bbb8	892cfd97	bl 0x04bb6ddc
0x4c6bbbc	c0220191	add x0,x22,#0x48
0x4c6bbc0	e1030191	add x1,sp,#0x40
0x4c6bbc4	474f9394	bl 0x0713f8e0
0x4c6bbc8	e85fc139	ldrsb w8,[sp, #0x57]
0x4c6bbcc	a800f836	tbz w8,#0x1f,0x04c6bbe0
0x4c6bbd0	e02340f9	ldr x0,[sp, #0x40]
0x4c6bbd4	e82b40f9	ldr x8,[sp, #0x50]
0x4c6bbd8	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6bbdc	0c519394	bl 0x0714000c
0x4c6bbe0	e0030291	add x0,sp,#0x80
0x4c6bbe4	ec26fd97	bl 0x04bb5794
0x4c6bbe8	80000034	cbz w0,0x04c6bbf8
0x4c6bbec	e1030291	add x1,sp,#0x80
0x4c6bbf0	e00317aa	mov x0,x23
0x4c6bbf4	3b4f9394	bl 0x0713f8e0
0x4c6bbf8	b60000b4	cbz x22,0x04c6bc0c
0x4c6bbfc	28008052	mov w8,#0x1
0x4c6bc00	090328f8	ldadd x8,x9,[x24]
0x4c6bc04	090328f8	ldadd x8,x9,[x24]
0x4c6bc08	080328f8	ldadd x8,x8,[x24]
0x4c6bc0c	372302f9	str x23,[x25, #0x440]
0x4c6bc10	372742f9	ldr x23,[x25, #0x448]
0x4c6bc14	362702f9	str x22,[x25, #0x448]
0x4c6bc18	b70000b4	cbz x23,0x04c6bc2c
0x4c6bc1c	e8220091	add x8,x23,#0x8
0x4c6bc20	09008092	mov x9,#-0x1
0x4c6bc24	0801e9f8	ldaddal x9,x8,[x8]
0x4c6bc28	280100b4	cbz x8,0x04c6bc4c
0x4c6bc2c	160300b4	cbz x22,0x04c6bc8c
0x4c6bc30	c8220091	add x8,x22,#0x8
0x4c6bc34	17008092	mov x23,#-0x1
0x4c6bc38	0801f7f8	ldaddal x23,x8,[x8]
0x4c6bc3c	880100b4	cbz x8,0x04c6bc6c
0x4c6bc40	0803f7f8	ldaddal x23,x8,[x24]
0x4c6bc44	480200b5	cbnz x8,0x04c6bc8c
0x4c6bc48	1e000014	b 0x04c6bcc0
0x4c6bc4c	e80240f9	ldr x8,[x23]
0x4c6bc50	080940f9	ldr x8,[x8, #0x10]
0x4c6bc54	e00317aa	mov x0,x23
0x4c6bc58	00013fd6	blr x8
0x4c6bc5c	e00317aa	mov x0,x23
0x4c6bc60	ef4f9394	bl 0x0713fc1c
0x4c6bc64	76feffb5	cbnz x22,0x04c6bc30
0x4c6bc68	09000014	b 0x04c6bc8c
0x4c6bc6c	c80240f9	ldr x8,[x22]
0x4c6bc70	080940f9	ldr x8,[x8, #0x10]
0x4c6bc74	e00316aa	mov x0,x22
0x4c6bc78	00013fd6	blr x8
0x4c6bc7c	e00316aa	mov x0,x22
0x4c6bc80	e74f9394	bl 0x0713fc1c
0x4c6bc84	0803f7f8	ldaddal x23,x8,[x24]
0x4c6bc88	c80100b4	cbz x8,0x04c6bcc0
0x4c6bc8c	f61b40f9	ldr x22,[sp, #0x30]
0x4c6bc90	960200b4	cbz x22,0x04c6bce0
0x4c6bc94	c8220091	add x8,x22,#0x8
0x4c6bc98	09008092	mov x9,#-0x1
0x4c6bc9c	0801e9f8	ldaddal x9,x8,[x8]
0x4c6bca0	080200b5	cbnz x8,0x04c6bce0
0x4c6bca4	c80240f9	ldr x8,[x22]
0x4c6bca8	080940f9	ldr x8,[x8, #0x10]
0x4c6bcac	e00316aa	mov x0,x22
0x4c6bcb0	00013fd6	blr x8
0x4c6bcb4	e00316aa	mov x0,x22
0x4c6bcb8	d94f9394	bl 0x0713fc1c
0x4c6bcbc	09000014	b 0x04c6bce0
0x4c6bcc0	c80240f9	ldr x8,[x22]
0x4c6bcc4	080940f9	ldr x8,[x8, #0x10]
0x4c6bcc8	e00316aa	mov x0,x22
0x4c6bccc	00013fd6	blr x8
0x4c6bcd0	e00316aa	mov x0,x22
0x4c6bcd4	d24f9394	bl 0x0713fc1c
0x4c6bcd8	f61b40f9	ldr x22,[sp, #0x30]
0x4c6bcdc	d6fdffb5	cbnz x22,0x04c6bc94
0x4c6bce0	ff7f04a9	stp xzr,xzr,[sp, #0x40]
0x4c6bce4	ff2b00f9	str xzr,[sp, #0x50]
0x4c6bce8	ffff02a9	stp xzr,xzr,[sp, #0x28]
0x4c6bcec	ff1f00f9	str xzr,[sp, #0x38]
0x4c6bcf0	a00240f9	ldr x0,[x21]
0x4c6bcf4	e1030191	add x1,sp,#0x40
0x4c6bcf8	e2a30091	add x2,sp,#0x28
0x4c6bcfc	77936b97	bl 0x02750ad8
0x4c6bd00	40040034	cbz w0,0x04c6bd88
0x4c6bd04	e85f4139	ldrb w8,[sp, #0x57]
0x4c6bd08	091d0013	sxtb w9,w8
0x4c6bd0c	ea2740f9	ldr x10,[sp, #0x48]
0x4c6bd10	3f010071	cmp w9,#0x0
0x4c6bd14	48b1889a	csel x8,x10,x8,lt
0x4c6bd18	760240f9	ldr x22,[x19]
0x4c6bd1c	880000b4	cbz x8,0x04c6bd2c
0x4c6bd20	c0e20291	add x0,x22,#0xb8
0x4c6bd24	e1030191	add x1,sp,#0x40
0x4c6bd28	ee4e9394	bl 0x0713f8e0
0x4c6bd2c	c0020491	add x0,x22,#0x100
0x4c6bd30	e1a30091	add x1,sp,#0x28
0x4c6bd34	eb4e9394	bl 0x0713f8e0
0x4c6bd38	c82242f9	ldr x8,[x22, #0x440]
0x4c6bd3c	d62642f9	ldr x22,[x22, #0x448]
0x4c6bd40	e8db01a9	stp x8,x22,[sp, #0x18]
0x4c6bd44	960000b4	cbz x22,0x04c6bd54
0x4c6bd48	c9220091	add x9,x22,#0x8
0x4c6bd4c	2a008052	mov w10,#0x1
0x4c6bd50	29012af8	ldadd x10,x9,[x9]
0x4c6bd54	080100b4	cbz x8,0x04c6bd74
0x4c6bd58	ff5f0039	strb wzr,[sp, #0x17]
0x4c6bd5c	ff030039	strb wzr,[sp]
0x4c6bd60	00c10091	add x0,x8,#0x30
0x4c6bd64	e1030091	mov x1,sp
0x4c6bd68	de4e9394	bl 0x0713f8e0
0x4c6bd6c	e85fc039	ldrsb w8,[sp, #0x17]
0x4c6bd70	880ef837	tbnz w8,#0x1f,0x04c6bf40
0x4c6bd74	b60000b4	cbz x22,0x04c6bd88
0x4c6bd78	c8220091	add x8,x22,#0x8
0x4c6bd7c	09008092	mov x9,#-0x1
0x4c6bd80	0801e9f8	ldaddal x9,x8,[x8]
0x4c6bd84	880b00b4	cbz x8,0x04c6bef4
0x4c6bd88	e8ffc039	ldrsb w8,[sp, #0x3f]
0x4c6bd8c	480cf837	tbnz w8,#0x1f,0x04c6bf14
0x4c6bd90	e85fc139	ldrsb w8,[sp, #0x57]
0x4c6bd94	c80cf837	tbnz w8,#0x1f,0x04c6bf2c
0x4c6bd98	a90240f9	ldr x9,[x21]
0x4c6bd9c	281541f9	ldr x8,[x9, #0x228]
0x4c6bda0	351941f9	ldr x21,[x9, #0x230]
0x4c6bda4	e85704a9	stp x8,x21,[sp, #0x40]
0x4c6bda8	950000b4	cbz x21,0x04c6bdb8
0x4c6bdac	a9220091	add x9,x21,#0x8
0x4c6bdb0	2a008052	mov w10,#0x1
0x4c6bdb4	29012af8	ldadd x10,x9,[x9]
0x4c6bdb8	e80200b4	cbz x8,0x04c6be14
0x4c6bdbc	01d545a9	ldp x1,x21,[x8, #0x58]
0x4c6bdc0	e1d702a9	stp x1,x21,[sp, #0x28]
0x4c6bdc4	950000b4	cbz x21,0x04c6bdd4
0x4c6bdc8	a8220091	add x8,x21,#0x8
0x4c6bdcc	29008052	mov w9,#0x1
0x4c6bdd0	080129f8	ldadd x9,x8,[x8]
0x4c6bdd4	810000b4	cbz x1,0x04c6bde4
0x4c6bdd8	680240f9	ldr x8,[x19]
0x4c6bddc	00410d91	add x0,x8,#0x350
0x4c6bde0	c04e9394	bl 0x0713f8e0
0x4c6bde4	750100b4	cbz x21,0x04c6be10
0x4c6bde8	a8220091	add x8,x21,#0x8
0x4c6bdec	09008092	mov x9,#-0x1
0x4c6bdf0	0801e9f8	ldaddal x9,x8,[x8]
0x4c6bdf4	e80000b5	cbnz x8,0x04c6be10
0x4c6bdf8	a80240f9	ldr x8,[x21]
0x4c6bdfc	080940f9	ldr x8,[x8, #0x10]
0x4c6be00	e00315aa	mov x0,x21
0x4c6be04	00013fd6	blr x8
0x4c6be08	e00315aa	mov x0,x21
0x4c6be0c	844f9394	bl 0x0713fc1c
0x4c6be10	f52740f9	ldr x21,[sp, #0x48]
0x4c6be14	750100b4	cbz x21,0x04c6be40
0x4c6be18	a8220091	add x8,x21,#0x8
0x4c6be1c	09008092	mov x9,#-0x1
0x4c6be20	0801e9f8	ldaddal x9,x8,[x8]
0x4c6be24	e80000b5	cbnz x8,0x04c6be40
0x4c6be28	a80240f9	ldr x8,[x21]
0x4c6be2c	080940f9	ldr x8,[x8, #0x10]
0x4c6be30	e00315aa	mov x0,x21
0x4c6be34	00013fd6	blr x8
0x4c6be38	e00315aa	mov x0,x21
0x4c6be3c	784f9394	bl 0x0713fc1c
0x4c6be40	680240f9	ldr x8,[x19]
0x4c6be44	00c11891	add x0,x8,#0x630
0x4c6be48	81a20091	add x1,x20,#0x28
0x4c6be4c	a54e9394	bl 0x0713f8e0
0x4c6be50	f33340f9	ldr x19,[sp, #0x60]
0x4c6be54	b30000b4	cbz x19,0x04c6be68
0x4c6be58	68220091	add x8,x19,#0x8
0x4c6be5c	09008092	mov x9,#-0x1
0x4c6be60	0801e9f8	ldaddal x9,x8,[x8]
0x4c6be64	680300b4	cbz x8,0x04c6bed0
0x4c6be68	e85fc239	ldrsb w8,[sp, #0x97]
0x4c6be6c	a800f836	tbz w8,#0x1f,0x04c6be80
0x4c6be70	e04340f9	ldr x0,[sp, #0x80]
0x4c6be74	e84b40f9	ldr x8,[sp, #0x90]
0x4c6be78	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6be7c	64509394	bl 0x0714000c
0x4c6be80	b3835af8	ldur x19,[x29, #-0x58]
0x4c6be84	730100b4	cbz x19,0x04c6beb0
0x4c6be88	68220091	add x8,x19,#0x8
0x4c6be8c	09008092	mov x9,#-0x1
0x4c6be90	0801e9f8	ldaddal x9,x8,[x8]
0x4c6be94	e80000b5	cbnz x8,0x04c6beb0
0x4c6be98	680240f9	ldr x8,[x19]
0x4c6be9c	080940f9	ldr x8,[x8, #0x10]
0x4c6bea0	e00313aa	mov x0,x19
0x4c6bea4	00013fd6	blr x8
0x4c6bea8	e00313aa	mov x0,x19
0x4c6beac	5c4f9394	bl 0x0713fc1c
0x4c6beb0	fd7b51a9	ldp x29,x30,[sp, #0x110]
0x4c6beb4	f44f50a9	ldp x20,x19,[sp, #0x100]
0x4c6beb8	f6574fa9	ldp x22,x21,[sp, #0xf0]
0x4c6bebc	f85f4ea9	ldp x24,x23,[sp, #0xe0]
0x4c6bec0	fa674da9	ldp x26,x25,[sp, #0xd0]
0x4c6bec4	fc6f4ca9	ldp x28,x27,[sp, #0xc0]
0x4c6bec8	ff830491	add sp,sp,#0x120
0x4c6becc	c0035fd6	ret
0x4c6bed0	680240f9	ldr x8,[x19]
0x4c6bed4	080940f9	ldr x8,[x8, #0x10]
0x4c6bed8	e00313aa	mov x0,x19
0x4c6bedc	00013fd6	blr x8
0x4c6bee0	e00313aa	mov x0,x19
0x4c6bee4	4e4f9394	bl 0x0713fc1c
0x4c6bee8	e85fc239	ldrsb w8,[sp, #0x97]
0x4c6beec	a8fcff36	tbz w8,#0x1f,0x04c6be80
0x4c6bef0	e0ffff17	b 0x04c6be70
0x4c6bef4	c80240f9	ldr x8,[x22]
0x4c6bef8	080940f9	ldr x8,[x8, #0x10]
0x4c6befc	e00316aa	mov x0,x22
0x4c6bf00	00013fd6	blr x8
0x4c6bf04	e00316aa	mov x0,x22
0x4c6bf08	454f9394	bl 0x0713fc1c
0x4c6bf0c	e8ffc039	ldrsb w8,[sp, #0x3f]
0x4c6bf10	08f4ff36	tbz w8,#0x1f,0x04c6bd90
0x4c6bf14	e01740f9	ldr x0,[sp, #0x28]
0x4c6bf18	e81f40f9	ldr x8,[sp, #0x38]
0x4c6bf1c	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6bf20	3b509394	bl 0x0714000c
0x4c6bf24	e85fc139	ldrsb w8,[sp, #0x57]
0x4c6bf28	88f3ff36	tbz w8,#0x1f,0x04c6bd98
0x4c6bf2c	e02340f9	ldr x0,[sp, #0x40]
0x4c6bf30	e82b40f9	ldr x8,[sp, #0x50]
0x4c6bf34	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6bf38	35509394	bl 0x0714000c
0x4c6bf3c	97ffff17	b 0x04c6bd98
0x4c6bf40	e00340f9	ldr x0,[sp]
0x4c6bf44	e80b40f9	ldr x8,[sp, #0x10]
0x4c6bf48	01f94092	and x1,x8,#0x7fffffffffffffff
0x4c6bf4c	30509394	bl 0x0714000c
0x4c6bf50	56f1ffb5	cbnz x22,0x04c6bd78
0x4c6bf54	8dffff17	b 0x04c6bd88
0x4c6bf58	a0e301d1	sub x0,x29,#0x78
0x4c6bf5c	9857ee96	bl 0x00801dbc
0x4c6bf60	200020d4	brk #0x1
