0x5ded3c4	080c40f9	ldr x8,[x0, #0x18]
0x5ded3c8	1f0101eb	cmp x8,x1
0x5ded3cc	e2080054	b.cs 0x05ded4e8
0x5ded3d0	ff4301d1	sub sp,sp,#0x50
0x5ded3d4	f65702a9	stp x22,x21,[sp, #0x20]
0x5ded3d8	f44f03a9	stp x20,x19,[sp, #0x30]
0x5ded3dc	fd7b04a9	stp x29,x30,[sp, #0x40]
0x5ded3e0	fd030191	add x29,sp,#0x40
0x5ded3e4	f50301aa	mov x21,x1
0x5ded3e8	f30300aa	mov x19,x0
0x5ded3ec	081040f9	ldr x8,[x0, #0x20]
0x5ded3f0	2900088b	add x9,x1,x8
0x5ded3f4	290500d1	sub x9,x9,#0x1
0x5ded3f8	2909c89a	udiv x9,x9,x8
0x5ded3fc	347d089b	mul x20,x9,x8
0x5ded400	000040f9	ldr x0,[x0]
0x5ded404	e10314aa	mov x1,x20
0x5ded408	c2504d94	bl 0x07141710
0x5ded40c	200400b4	cbz x0,0x05ded490
0x5ded410	600200f9	str x0,[x19]
0x5ded414	28008052	mov w8,#0x1
0x5ded418	0864a072	movk w8,#0x320, LSL #16
0x5ded41c	bf0208eb	cmp x21,x8
0x5ded420	e3020054	b.cc 0x05ded47c
0x5ded424	80d601d0	adrp x0,0x98bf000
0x5ded428	00f01691	add x0,x0,#0x5bc
0x5ded42c	82d601d0	adrp x2,0x98bf000
0x5ded430	423c1991	add x2,x2,#0x64f
0x5ded434	83d601d0	adrp x3,0x98bf000
0x5ded438	637c1a91	add x3,x3,#0x69f
0x5ded43c	84d201b0	adrp x4,0x983e000
0x5ded440	84ac0c91	add x4,x4,#0x32b
0x5ded444	f50300f9	str x21,[sp]
0x5ded448	01268052	mov w1,#0x130
0x5ded44c	41ffff97	bl 0x05ded150
0x5ded450	600240f9	ldr x0,[x19]
0x5ded454	400100b5	cbnz x0,0x05ded47c
0x5ded458	80d601d0	adrp x0,0x98bf000
0x5ded45c	00f01691	add x0,x0,#0x5bc
0x5ded460	82d601d0	adrp x2,0x98bf000
0x5ded464	423c1991	add x2,x2,#0x64f
0x5ded468	83d601d0	adrp x3,0x98bf000
0x5ded46c	63e01a91	add x3,x3,#0x6b8
0x5ded470	21268052	mov w1,#0x131
0x5ded474	95feff97	bl 0x05decec8
0x5ded478	600240f9	ldr x0,[x19]
0x5ded47c	680e40f9	ldr x8,[x19, #0x18]
0x5ded480	810208cb	sub x1,x20,x8
0x5ded484	0000088b	add x0,x0,x8
0x5ded488	c24b4d94	bl 0x07140390
0x5ded48c	12000014	b 0x05ded4d4
0x5ded490	69a241a9	ldp x9,x8,[x19, #0x18]
0x5ded494	80d601d0	adrp x0,0x98bf000
0x5ded498	00f01691	add x0,x0,#0x5bc
0x5ded49c	82d601d0	adrp x2,0x98bf000
0x5ded4a0	423c1991	add x2,x2,#0x64f
0x5ded4a4	f42701a9	stp x20,x9,[sp, #0x10]
0x5ded4a8	63d201f0	adrp x3,0x983c000
0x5ded4ac	63dc3d91	add x3,x3,#0xf77
0x5ded4b0	84d601d0	adrp x4,0x98bf000
0x5ded4b4	84641991	add x4,x4,#0x659
0x5ded4b8	f52300a9	stp x21,x8,[sp]
0x5ded4bc	c1248052	mov w1,#0x126
0x5ded4c0	24ffff97	bl 0x05ded150
0x5ded4c4	600240f9	ldr x0,[x19]
0x5ded4c8	054d4d94	bl 0x071408dc
0x5ded4cc	140080d2	mov x20,#0x0
0x5ded4d0	7f0200f9	str xzr,[x19]
0x5ded4d4	740e00f9	str x20,[x19, #0x18]
0x5ded4d8	fd7b44a9	ldp x29,x30,[sp, #0x40]
0x5ded4dc	f44f43a9	ldp x20,x19,[sp, #0x30]
0x5ded4e0	f65742a9	ldp x22,x21,[sp, #0x20]
0x5ded4e4	ff430191	add sp,sp,#0x50
0x5ded4e8	c0035fd6	ret
