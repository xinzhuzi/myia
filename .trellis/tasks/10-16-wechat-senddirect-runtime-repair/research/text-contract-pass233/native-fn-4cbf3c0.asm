0x4cbf3c0	f657bda9	stp x22,x21,[sp, #-0x30]!
0x4cbf3c4	f44f01a9	stp x20,x19,[sp, #0x10]
0x4cbf3c8	fd7b02a9	stp x29,x30,[sp, #0x20]
0x4cbf3cc	fd830091	add x29,sp,#0x20
0x4cbf3d0	f40308aa	mov x20,x8
0x4cbf3d4	00388052	mov w0,#0x1c0
0x4cbf3d8	16039294	bl 0x07140030
0x4cbf3dc	f30300aa	mov x19,x0
0x4cbf3e0	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x4cbf3e4	888f02b0	adrp x8,0x9eb0000
0x4cbf3e8	08412e91	add x8,x8,#0xb90
0x4cbf3ec	080000f9	str x8,[x0]
0x4cbf3f0	00e4006f	movi v0.2D,#0x0
0x4cbf3f4	000001ad	stp q0,q0,[x0, #0x20]
0x4cbf3f8	000002ad	stp q0,q0,[x0, #0x40]
0x4cbf3fc	000003ad	stp q0,q0,[x0, #0x60]
0x4cbf400	000004ad	stp q0,q0,[x0, #0x80]
0x4cbf404	000005ad	stp q0,q0,[x0, #0xa0]
0x4cbf408	000006ad	stp q0,q0,[x0, #0xc0]
0x4cbf40c	000007ad	stp q0,q0,[x0, #0xe0]
0x4cbf410	000008ad	stp q0,q0,[x0, #0x100]
0x4cbf414	000009ad	stp q0,q0,[x0, #0x120]
0x4cbf418	00000aad	stp q0,q0,[x0, #0x140]
0x4cbf41c	00000bad	stp q0,q0,[x0, #0x160]
0x4cbf420	00000cad	stp q0,q0,[x0, #0x180]
0x4cbf424	00000dad	stp q0,q0,[x0, #0x1a0]
0x4cbf428	888f02b0	adrp x8,0x9eb0000
0x4cbf42c	08613f91	add x8,x8,#0xfd8
0x4cbf430	08410091	add x8,x8,#0x10
0x4cbf434	f50300aa	mov x21,x0
0x4cbf438	a88e01f8	str x8,[x21, #0x18]!
0x4cbf43c	28008052	mov w8,#0x1
0x4cbf440	08800039	strb w8,[x0, #0x20]
0x4cbf444	00a00091	add x0,x0,#0x28
0x4cbf448	7762e096	bl 0x004d7e24
0x4cbf44c	7f7e11a9	stp xzr,xzr,[x19, #0x110]
0x4cbf450	7f2a01b9	str wzr,[x19, #0x128]
0x4cbf454	7f9200f9	str xzr,[x19, #0x120]
0x4cbf458	7f3201b9	str wzr,[x19, #0x130]
0x4cbf45c	7f9e00f9	str xzr,[x19, #0x138]
0x4cbf460	7f4201b9	str wzr,[x19, #0x140]
0x4cbf464	68220591	add x8,x19,#0x148
0x4cbf468	00e4006f	movi v0.2D,#0x0
0x4cbf46c	000100ad	stp q0,q0,[x8]
0x4cbf470	7ffe0fa9	stp xzr,xzr,[x19, #0xf8]
0x4cbf474	7f7a00f9	str xzr,[x19, #0xf0]
0x4cbf478	7f0a01b9	str wzr,[x19, #0x108]
0x4cbf47c	08f0a752	mov w8,#0x3f800000
0x4cbf480	686a01b9	str w8,[x19, #0x168]
0x4cbf484	7f7201b9	str wzr,[x19, #0x170]
0x4cbf488	68e20591	add x8,x19,#0x178
0x4cbf48c	7fde00f9	str xzr,[x19, #0x1b8]
0x4cbf490	000101ad	stp q0,q0,[x8, #0x20]
0x4cbf494	000100ad	stp q0,q0,[x8]
0x4cbf498	954e00a9	stp x21,x19,[x20]
0x4cbf49c	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x4cbf4a0	f44f41a9	ldp x20,x19,[sp, #0x10]
0x4cbf4a4	f657c3a8	ldp x22,x21,[sp], #0x30
0x4cbf4a8	c0035fd6	ret
