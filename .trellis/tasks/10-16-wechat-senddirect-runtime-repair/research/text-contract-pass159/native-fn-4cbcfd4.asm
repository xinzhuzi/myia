0x4cbcfd4	011000b9	str w1,[x0, #0x10]
0x4cbcfd8	08c040f8	ldur x8,[x0, #0xc]
0x4cbcfdc	088400f9	str x8,[x0, #0x108]
0x4cbcfe0	081041f9	ldr x8,[x0, #0x220]
0x4cbcfe4	880100b4	cbz x8,0x04cbd014
0x4cbcfe8	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x4cbcfec	fd7b01a9	stp x29,x30,[sp, #0x10]
0x4cbcff0	fd430091	add x29,sp,#0x10
0x4cbcff4	f30301aa	mov x19,x1
0x4cbcff8	f40300aa	mov x20,x0
0x4cbcffc	62b3f597	bl 0x04a29d84
0x4cbd000	60000034	cbz w0,0x04cbd00c
0x4cbd004	881241f9	ldr x8,[x20, #0x220]
0x4cbd008	130d00b9	str w19,[x8, #0xc]
0x4cbd00c	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x4cbd010	f44fc2a8	ldp x20,x19,[sp], #0x20
0x4cbd014	c0035fd6	ret
