0x4cbfafc	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4cbfb00	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4cbfb04	fd430091	add x29,sp,#0x10
0x4cbfb08	01a057a9	ldp x1,x8,[x0, #0x178]
0x4cbfb0c	3f0008eb	cmp x1,x8
0x4cbfb10	e0010054	b.eq 0x04cbfb4c
0x4cbfb14	f30300aa	mov x19,x0
0x4cbfb18	0201014b	sub w2,w8,w1
0x4cbfb1c	00400691	add x0,x0,#0x190
0x4cbfb20	e6cf3794	bl 0x05ab3ab8
0x4cbfb24	40010034	cbz w0,0x04cbfb4c
0x4cbfb28	60be40f9	ldr x0,[x19, #0x178]
0x4cbfb2c	7ffe17a9	stp xzr,xzr,[x19, #0x178]
0x4cbfb30	68c640f9	ldr x8,[x19, #0x188]
0x4cbfb34	7fc600f9	str xzr,[x19, #0x188]
0x4cbfb38	a00000b4	cbz x0,0x04cbfb4c
0x4cbfb3c	010100cb	sub x1,x8,x0
0x4cbfb40	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4cbfb44	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4cbfb48	31019214	b 0x0714000c
0x4cbfb4c	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4cbfb50	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4cbfb54	c0035fd6	ret
