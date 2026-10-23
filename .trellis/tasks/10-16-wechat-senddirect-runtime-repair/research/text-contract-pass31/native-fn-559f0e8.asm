0x559f0e8	884b02b0	adrp x8,0x9f10000
0x559f0ec	08213391	add x8,x8,#0xcc8
0x559f0f0	1ffc02a9	stp xzr,xzr,[x0, #0x28]
0x559f0f4	1f3800b9	str wzr,[x0, #0x38]
0x559f0f8	1f7c04a9	stp xzr,xzr,[x0, #0x40]
0x559f0fc	1f5000b9	str wzr,[x0, #0x50]
0x559f100	1ffc06a9	stp xzr,xzr,[x0, #0x68]
0x559f104	1ffc05a9	stp xzr,xzr,[x0, #0x58]
0x559f108	087c00a9	stp x8,xzr,[x0]
0x559f10c	1f7c01a9	stp xzr,xzr,[x0, #0x10]
0x559f110	1f2000b9	str wzr,[x0, #0x20]
0x559f114	287c02b0	adrp x8,0xa524000
0x559f118	08412b91	add x8,x8,#0xad0
0x559f11c	083c00f9	str x8,[x0, #0x78]
0x559f120	00e4006f	movi v0.2D,#0x0
0x559f124	008004ad	stp q0,q0,[x0, #0x90]
0x559f128	0020803d	str q0,[x0, #0x80]
0x559f12c	1f200ba9	stp xzr,x8,[x0, #0xb0]
0x559f130	087c0ca9	stp x8,xzr,[x0, #0xc0]
0x559f134	08200da9	stp x8,x8,[x0, #0xd0]
0x559f138	1f200ea9	stp xzr,x8,[x0, #0xe0]
0x559f13c	08200fa9	stp x8,x8,[x0, #0xf0]
0x559f140	082010a9	stp x8,x8,[x0, #0x100]
0x559f144	087c11a9	stp x8,xzr,[x0, #0x110]
0x559f148	082012a9	stp x8,x8,[x0, #0x120]
0x559f14c	e0e5002f	movi d0,#0xffffffff
0x559f150	00a000fd	str d0,[x0, #0x140]
0x559f154	1f2013a9	stp xzr,x8,[x0, #0x130]
0x559f158	1fa400f9	str xzr,[x0, #0x148]
0x559f15c	c0035fd6	ret
