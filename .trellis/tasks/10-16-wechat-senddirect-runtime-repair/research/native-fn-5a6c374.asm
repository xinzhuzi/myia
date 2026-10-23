0x5a6c374	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x5a6c378	fd7b01a9	stp x29,x30,[sp, #0x10]
0x5a6c37c	fd430091	add x29,sp,#0x10
0x5a6c380	f30300aa	mov x19,x0
0x5a6c384	c8550290	adrp x8,0xa524000
0x5a6c388	08412b91	add x8,x8,#0xad0
0x5a6c38c	492602b0	adrp x9,0x9f35000
0x5a6c390	29211291	add x9,x9,#0x488
0x5a6c394	092000a9	stp x9,x8,[x0]
0x5a6c398	087c01a9	stp x8,xzr,[x0, #0x10]
0x5a6c39c	1f1000f9	str xzr,[x0, #0x20]
0x5a6c3a0	a3ffff97	bl 0x05a6c22c
0x5a6c3a4	e00313aa	mov x0,x19
0x5a6c3a8	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x5a6c3ac	f44fc2a8	ldp x20,x19,[sp], #0x20
0x5a6c3b0	c0035fd6	ret
