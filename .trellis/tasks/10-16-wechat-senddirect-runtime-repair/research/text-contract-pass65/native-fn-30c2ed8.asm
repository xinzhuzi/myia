0x30c2ed8	ff0301d1	sub sp,sp,#0x40
0x30c2edc	f44f02a9	stp x20,x19,[sp, #0x20]
0x30c2ee0	fd7b03a9	stp x29,x30,[sp, #0x30]
0x30c2ee4	fdc30091	add x29,sp,#0x30
0x30c2ee8	f30301aa	mov x19,x1
0x30c2eec	7f000039	strb wzr,[x3]
0x30c2ef0	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x30c2ef4	e82301a9	stp x8,x8,[sp, #0x10]
0x30c2ef8	e80700f9	str x8,[sp, #0x8]
0x30c2efc	f4230091	add x20,sp,#0x8
0x30c2f00	e8230091	add x8,sp,#0x8
0x30c2f04	00e00191	add x0,x0,#0x78
0x30c2f08	48c4a794	bl 0x05ab4028
0x30c2f0c	e87fc039	ldrsb w8,[sp, #0x1f]
0x30c2f10	e90740f9	ldr x9,[sp, #0x8]
0x30c2f14	ea1340b9	ldr w10,[sp, #0x10]
0x30c2f18	0b1d0012	and w11,w8,#0xff
0x30c2f1c	1f010071	cmp w8,#0x0
0x30c2f20	42b18b1a	csel w2,w10,w11,lt
0x30c2f24	21b1949a	csel x1,x9,x20,lt
0x30c2f28	e00313aa	mov x0,x19
0x30c2f2c	fb5b5694	bl 0x04659f18
0x30c2f30	e87fc039	ldrsb w8,[sp, #0x1f]
0x30c2f34	a800f836	tbz w8,#0x1f,0x030c2f48
0x30c2f38	e00740f9	ldr x0,[sp, #0x8]
0x30c2f3c	e80f40f9	ldr x8,[sp, #0x18]
0x30c2f40	01f94092	and x1,x8,#0x7fffffffffffffff
0x30c2f44	32f40195	bl 0x0714000c
0x30c2f48	20008052	mov w0,#0x1
0x30c2f4c	fd7b43a9	ldp x29,x30,[sp, #0x30]
0x30c2f50	f44f42a9	ldp x20,x19,[sp, #0x20]
0x30c2f54	ff030191	add sp,sp,#0x40
0x30c2f58	c0035fd6	ret
