0x4cbf170	f657bda9	stp x22,x21,[sp, #-0x30]!
0x4cbf174	f44f01a9	stp x20,x19,[sp, #0x10]
0x4cbf178	fd7b02a9	stp x29,x30,[sp, #0x20]
0x4cbf17c	fd830091	add x29,sp,#0x20
0x4cbf180	f40308aa	mov x20,x8
0x4cbf184	003a8052	mov w0,#0x1d0
0x4cbf188	aa039294	bl 0x07140030
0x4cbf18c	f30300aa	mov x19,x0
0x4cbf190	1ffc00a9	stp xzr,xzr,[x0, #0x8]
0x4cbf194	888f02b0	adrp x8,0x9eb0000
0x4cbf198	08c12b91	add x8,x8,#0xaf0
0x4cbf19c	080000f9	str x8,[x0]
0x4cbf1a0	00e4006f	movi v0.2D,#0x0
0x4cbf1a4	000001ad	stp q0,q0,[x0, #0x20]
0x4cbf1a8	000002ad	stp q0,q0,[x0, #0x40]
0x4cbf1ac	000003ad	stp q0,q0,[x0, #0x60]
0x4cbf1b0	000004ad	stp q0,q0,[x0, #0x80]
0x4cbf1b4	000005ad	stp q0,q0,[x0, #0xa0]
0x4cbf1b8	000006ad	stp q0,q0,[x0, #0xc0]
0x4cbf1bc	000007ad	stp q0,q0,[x0, #0xe0]
0x4cbf1c0	000008ad	stp q0,q0,[x0, #0x100]
0x4cbf1c4	000009ad	stp q0,q0,[x0, #0x120]
0x4cbf1c8	00000aad	stp q0,q0,[x0, #0x140]
0x4cbf1cc	00000bad	stp q0,q0,[x0, #0x160]
0x4cbf1d0	00000cad	stp q0,q0,[x0, #0x180]
0x4cbf1d4	00000dad	stp q0,q0,[x0, #0x1a0]
0x4cbf1d8	0070803d	str q0,[x0, #0x1c0]
0x4cbf1dc	888f02b0	adrp x8,0x9eb0000
0x4cbf1e0	08613f91	add x8,x8,#0xfd8
0x4cbf1e4	08410091	add x8,x8,#0x10
0x4cbf1e8	f50300aa	mov x21,x0
0x4cbf1ec	a88e01f8	str x8,[x21, #0x18]!
0x4cbf1f0	28008052	mov w8,#0x1
0x4cbf1f4	08800039	strb w8,[x0, #0x20]
0x4cbf1f8	00a00091	add x0,x0,#0x28
0x4cbf1fc	0a63e096	bl 0x004d7e24
0x4cbf200	7f7e11a9	stp xzr,xzr,[x19, #0x110]
0x4cbf204	7f2a01b9	str wzr,[x19, #0x128]
0x4cbf208	7f9200f9	str xzr,[x19, #0x120]
0x4cbf20c	7f3201b9	str wzr,[x19, #0x130]
0x4cbf210	7f9e00f9	str xzr,[x19, #0x138]
0x4cbf214	7f4201b9	str wzr,[x19, #0x140]
0x4cbf218	68220591	add x8,x19,#0x148
0x4cbf21c	00e4006f	movi v0.2D,#0x0
0x4cbf220	000100ad	stp q0,q0,[x8]
0x4cbf224	7ffe0fa9	stp xzr,xzr,[x19, #0xf8]
0x4cbf228	7f7a00f9	str xzr,[x19, #0xf0]
0x4cbf22c	7f0a01b9	str wzr,[x19, #0x108]
0x4cbf230	08f0a752	mov w8,#0x3f800000
0x4cbf234	686a01b9	str w8,[x19, #0x168]
0x4cbf238	7f7201b9	str wzr,[x19, #0x170]
0x4cbf23c	68e20591	add x8,x19,#0x178
0x4cbf240	000101ad	stp q0,q0,[x8, #0x20]
0x4cbf244	000100ad	stp q0,q0,[x8]
0x4cbf248	888f02d0	adrp x8,0x9eb1000
0x4cbf24c	08011991	add x8,x8,#0x640
0x4cbf250	08410091	add x8,x8,#0x10
0x4cbf254	680e00f9	str x8,[x19, #0x18]
0x4cbf258	7f7e1ca9	stp xzr,xzr,[x19, #0x1c0]
0x4cbf25c	7fde00f9	str xzr,[x19, #0x1b8]
0x4cbf260	954e00a9	stp x21,x19,[x20]
0x4cbf264	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x4cbf268	f44f41a9	ldp x20,x19,[sp, #0x10]
0x4cbf26c	f657c3a8	ldp x22,x21,[sp], #0x30
0x4cbf270	c0035fd6	ret
