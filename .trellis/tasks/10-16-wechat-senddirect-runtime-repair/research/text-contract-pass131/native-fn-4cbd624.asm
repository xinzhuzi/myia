0x4cbd624	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4cbd628	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4cbd62c	fd430091	add x29,sp,#0x10
0x4cbd630	f30300aa	mov x19,x0
0x4cbd634	080c40b9	ldr w8,[x0, #0xc]
0x4cbd638	09e28452	mov w9,#0x2710
0x4cbd63c	1f01096b	cmp w8,w9
0x4cbd640	61040054	b.ne 0x04cbd6cc
0x4cbd644	4cb0e697	bl 0x04669774
0x4cbd648	080040f9	ldr x8,[x0]
0x4cbd64c	081540f9	ldr x8,[x8, #0x28]
0x4cbd650	00013fd6	blr x8
0x4cbd654	e80300aa	mov x8,x0
0x4cbd658	60620091	add x0,x19,#0x18
0x4cbd65c	69be4039	ldrb w9,[x19, #0x2f]
0x4cbd660	2a1d0013	sxtb w10,w9
0x4cbd664	621240f9	ldr x2,[x19, #0x20]
0x4cbd668	5f010071	cmp w10,#0x0
0x4cbd66c	4bb0899a	csel x11,x2,x9,lt
0x4cbd670	0c5d4039	ldrb w12,[x8, #0x17]
0x4cbd674	8a1d0013	sxtb w10,w12
0x4cbd678	0d0540f9	ldr x13,[x8, #0x8]
0x4cbd67c	5f010071	cmp w10,#0x0
0x4cbd680	acb18c9a	csel x12,x13,x12,lt
0x4cbd684	7f010ceb	cmp x11,x12
0x4cbd688	01030054	b.ne 0x04cbd6e8
0x4cbd68c	0b0140f9	ldr x11,[x8]
0x4cbd690	5f010071	cmp w10,#0x0
0x4cbd694	61b1889a	csel x1,x11,x8,lt
0x4cbd698	e9023837	tbnz w9,#0x7,0x04cbd6f4
0x4cbd69c	49010034	cbz w9,0x04cbd6c4
0x4cbd6a0	e80300aa	mov x8,x0
0x4cbd6a4	0a014039	ldrb w10,[x8]
0x4cbd6a8	2b004039	ldrb w11,[x1]
0x4cbd6ac	5f010b6b	cmp w10,w11
0x4cbd6b0	c1010054	b.ne 0x04cbd6e8
0x4cbd6b4	08050091	add x8,x8,#0x1
0x4cbd6b8	21040091	add x1,x1,#0x1
0x4cbd6bc	290500f1	subs x9,x9,#0x1
0x4cbd6c0	21ffff54	b.ne 0x04cbd6a4
0x4cbd6c4	60c20091	add x0,x19,#0x30
0x4cbd6c8	08000014	b 0x04cbd6e8
0x4cbd6cc	e00313aa	mov x0,x19
0x4cbd6d0	1e000094	bl 0x04cbd748
0x4cbd6d4	1f000071	cmp w0,#0x0
0x4cbd6d8	08038052	mov w8,#0x18
0x4cbd6dc	09068052	mov w9,#0x30
0x4cbd6e0	2811889a	csel x8,x9,x8,ne
0x4cbd6e4	6002088b	add x0,x19,x8
0x4cbd6e8	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4cbd6ec	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4cbd6f0	c0035fd6	ret
0x4cbd6f4	680e40f9	ldr x8,[x19, #0x18]
0x4cbd6f8	f40300aa	mov x20,x0
0x4cbd6fc	e00308aa	mov x0,x8
0x4cbd700	df0d9294	bl 0x07140e7c
0x4cbd704	69c20091	add x9,x19,#0x30
0x4cbd708	1f000071	cmp w0,#0x0
0x4cbd70c	2001949a	csel x0,x9,x20,eq
0x4cbd710	f6ffff17	b 0x04cbd6e8
