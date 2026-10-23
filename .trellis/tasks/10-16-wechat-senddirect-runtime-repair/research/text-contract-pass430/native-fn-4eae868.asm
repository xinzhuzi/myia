0x4eae868	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4eae86c	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4eae870	fd430091	add x29,sp,#0x10
0x4eae874	f30300aa	mov x19,x0
0x4eae878	a88002d0	adrp x8,0x9ec4000
0x4eae87c	08a10891	add x8,x8,#0x228
0x4eae880	080000f9	str x8,[x0]
0x4eae884	00e4006f	movi v0.2D,#0x0
0x4eae888	0080803c	stur q0,[x0, #0x8]
0x4eae88c	0080813c	stur q0,[x0, #0x18]
0x4eae890	0080823c	stur q0,[x0, #0x28]
0x4eae894	0080833c	stur q0,[x0, #0x38]
0x4eae898	0080843c	stur q0,[x0, #0x48]
0x4eae89c	0080853c	stur q0,[x0, #0x58]
0x4eae8a0	0080863c	stur q0,[x0, #0x68]
0x4eae8a4	45feff97	bl 0x04eae1b8
0x4eae8a8	e00313aa	mov x0,x19
0x4eae8ac	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4eae8b0	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4eae8b4	c0035fd6	ret
