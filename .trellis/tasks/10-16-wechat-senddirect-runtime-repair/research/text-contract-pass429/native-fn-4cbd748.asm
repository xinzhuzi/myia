0x4cbd748	080c40b9	ldr w8,[x0, #0xc]
0x4cbd74c	09e28452	mov w9,#0x2710
0x4cbd750	1f01096b	cmp w8,w9
0x4cbd754	60050054	b.eq 0x04cbd800
0x4cbd758	08bc4039	ldrb w8,[x0, #0x2f]
0x4cbd75c	091d0013	sxtb w9,w8
0x4cbd760	0a1040f9	ldr x10,[x0, #0x20]
0x4cbd764	3f010071	cmp w9,#0x0
0x4cbd768	48b1889a	csel x8,x10,x8,lt
0x4cbd76c	a80400b4	cbz x8,0x04cbd800
0x4cbd770	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4cbd774	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4cbd778	fd430091	add x29,sp,#0x10
0x4cbd77c	f30300aa	mov x19,x0
0x4cbd780	fdafe697	bl 0x04669774
0x4cbd784	080040f9	ldr x8,[x0]
0x4cbd788	081540f9	ldr x8,[x8, #0x28]
0x4cbd78c	00013fd6	blr x8
0x4cbd790	69be4039	ldrb w9,[x19, #0x2f]
0x4cbd794	2a1d0013	sxtb w10,w9
0x4cbd798	621240f9	ldr x2,[x19, #0x20]
0x4cbd79c	5f010071	cmp w10,#0x0
0x4cbd7a0	4bb0899a	csel x11,x2,x9,lt
0x4cbd7a4	0c5c4039	ldrb w12,[x0, #0x17]
0x4cbd7a8	8a1d0013	sxtb w10,w12
0x4cbd7ac	0d0440f9	ldr x13,[x0, #0x8]
0x4cbd7b0	5f010071	cmp w10,#0x0
0x4cbd7b4	acb18c9a	csel x12,x13,x12,lt
0x4cbd7b8	7f010ceb	cmp x11,x12
0x4cbd7bc	61020054	b.ne 0x04cbd808
0x4cbd7c0	68620091	add x8,x19,#0x18
0x4cbd7c4	0b0040f9	ldr x11,[x0]
0x4cbd7c8	5f010071	cmp w10,#0x0
0x4cbd7cc	61b1809a	csel x1,x11,x0,lt
0x4cbd7d0	09023837	tbnz w9,#0x7,0x04cbd810
0x4cbd7d4	89020034	cbz w9,0x04cbd824
0x4cbd7d8	290500d1	sub x9,x9,#0x1
0x4cbd7dc	0b154038	ldrb w11,[x8], #0x1
0x4cbd7e0	2c144038	ldrb w12,[x1], #0x1
0x4cbd7e4	290500f1	subs x9,x9,#0x1
0x4cbd7e8	ea379f1a	cset w10,cs
0x4cbd7ec	7f010c6b	cmp w11,w12
0x4cbd7f0	e0179f1a	cset w0,eq
0x4cbd7f4	a1010054	b.ne 0x04cbd828
0x4cbd7f8	2aff0737	tbnz w10,#0x0,0x04cbd7dc
0x4cbd7fc	0b000014	b 0x04cbd828
0x4cbd800	00008052	mov w0,#0x0
0x4cbd804	c0035fd6	ret
0x4cbd808	00008052	mov w0,#0x0
0x4cbd80c	07000014	b 0x04cbd828
0x4cbd810	000140f9	ldr x0,[x8]
0x4cbd814	9a0d9294	bl 0x07140e7c
0x4cbd818	1f000071	cmp w0,#0x0
0x4cbd81c	e0179f1a	cset w0,eq
0x4cbd820	02000014	b 0x04cbd828
0x4cbd824	20008052	mov w0,#0x1
0x4cbd828	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4cbd82c	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4cbd830	c0035fd6	ret
