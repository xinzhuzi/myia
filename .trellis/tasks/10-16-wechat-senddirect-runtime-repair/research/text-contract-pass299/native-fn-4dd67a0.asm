0x4dd67a0	f657bda9	stp x22,x21,[sp, #-0x30]!
0x4dd67a4	f44f01a9	stp x20,x19,[sp, #0x10]
0x4dd67a8	fd7b02a9	stp x29,x30,[sp, #0x20]
0x4dd67ac	fd830091	add x29,sp,#0x20
0x4dd67b0	ff8307d1	sub sp,sp,#0x1e0
0x4dd67b4	086b0290	adrp x8,0x9b36000
0x4dd67b8	084d46f9	ldr x8,[x8, #0xc98]
0x4dd67bc	080140f9	ldr x8,[x8]
0x4dd67c0	a8831df8	stur x8,[x29, #-0x28]
0x4dd67c4	15b70290	adrp x21,0xa4b6000
0x4dd67c8	b39e46f9	ldr x19,[x21, #0xd38]
0x4dd67cc	405302d0	adrp x0,0x9840000
0x4dd67d0	00042391	add x0,x0,#0x8c1
0x4dd67d4	e8030091	mov x8,sp
0x4dd67d8	546a2194	bl 0x05631128
0x4dd67dc	00028052	mov w0,#0x10
0x4dd67e0	14a68d94	bl 0x07140030
0x4dd67e4	f40300aa	mov x20,x0
0x4dd67e8	778c2494	bl 0x056f99c4
0x4dd67ec	48870290	adrp x8,0x9ebe000
0x4dd67f0	08c10291	add x8,x8,#0xb0
0x4dd67f4	887e00a9	stp x8,xzr,[x20]
0x4dd67f8	e2030091	mov x2,sp
0x4dd67fc	e00313aa	mov x0,x19
0x4dd6800	010080d2	mov x1,#0x0
0x4dd6804	e30314aa	mov x3,x20
0x4dd6808	e58c2494	bl 0x056f9b9c
0x4dd680c	e0030091	mov x0,sp
0x4dd6810	5d652194	bl 0x0562fd84
0x4dd6814	40e5054f	movi v0.16B,#0xaa
0x4dd6818	e0830dad	stp q0,q0,[sp, #0x1b0]
0x4dd681c	e0830cad	stp q0,q0,[sp, #0x190]
0x4dd6820	e0830bad	stp q0,q0,[sp, #0x170]
0x4dd6824	e0830aad	stp q0,q0,[sp, #0x150]
0x4dd6828	e08309ad	stp q0,q0,[sp, #0x130]
0x4dd682c	e08308ad	stp q0,q0,[sp, #0x110]
0x4dd6830	e08307ad	stp q0,q0,[sp, #0xf0]
0x4dd6834	e08306ad	stp q0,q0,[sp, #0xd0]
0x4dd6838	e08305ad	stp q0,q0,[sp, #0xb0]
0x4dd683c	e08304ad	stp q0,q0,[sp, #0x90]
0x4dd6840	e08303ad	stp q0,q0,[sp, #0x70]
0x4dd6844	e08302ad	stp q0,q0,[sp, #0x50]
0x4dd6848	e08301ad	stp q0,q0,[sp, #0x30]
0x4dd684c	e08300ad	stp q0,q0,[sp, #0x10]
0x4dd6850	e003803d	str q0,[sp]
0x4dd6854	e0030091	mov x0,sp
0x4dd6858	5cd82394	bl 0x056cc9c8
0x4dd685c	e0030091	mov x0,sp
0x4dd6860	a0d82394	bl 0x056ccae0
0x4dd6864	a09e46f9	ldr x0,[x21, #0xd38]
0x4dd6868	010080d2	mov x1,#0x0
0x4dd686c	c08d2494	bl 0x056f9f6c
0x4dd6870	e1030091	mov x1,sp
0x4dd6874	bada2394	bl 0x056cd35c
0x4dd6878	e0030091	mov x0,sp
0x4dd687c	7fd82394	bl 0x056cca78
0x4dd6880	a8835df8	ldur x8,[x29, #-0x28]
0x4dd6884	096b0290	adrp x9,0x9b36000
0x4dd6888	294d46f9	ldr x9,[x9, #0xc98]
0x4dd688c	290140f9	ldr x9,[x9]
0x4dd6890	3f0108eb	cmp x9,x8
0x4dd6894	c1000054	b.ne 0x04dd68ac
0x4dd6898	ff830791	add sp,sp,#0x1e0
0x4dd689c	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x4dd68a0	f44f41a9	ldp x20,x19,[sp, #0x10]
0x4dd68a4	f657c3a8	ldp x22,x21,[sp], #0x30
0x4dd68a8	c0035fd6	ret
0x4dd68ac	3ea68d94	bl 0x071401a4
