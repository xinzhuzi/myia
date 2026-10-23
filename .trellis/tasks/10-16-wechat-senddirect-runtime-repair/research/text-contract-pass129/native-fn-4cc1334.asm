0x4cc1334	ffc301d1	sub sp,sp,#0x70
0x4cc1338	f65704a9	stp x22,x21,[sp, #0x40]
0x4cc133c	f44f05a9	stp x20,x19,[sp, #0x50]
0x4cc1340	fd7b06a9	stp x29,x30,[sp, #0x60]
0x4cc1344	fd830191	add x29,sp,#0x60
0x4cc1348	f30303aa	mov x19,x3
0x4cc134c	f40302aa	mov x20,x2
0x4cc1350	f50301aa	mov x21,x1
0x4cc1354	e10300aa	mov x1,x0
0x4cc1358	f60308aa	mov x22,x8
0x4cc135c	e0030091	mov x0,sp
0x4cc1360	84bf0194	bl 0x04d31170
0x4cc1364	e0030091	mov x0,sp
0x4cc1368	e80316aa	mov x8,x22
0x4cc136c	e10315aa	mov x1,x21
0x4cc1370	e20314aa	mov x2,x20
0x4cc1374	e30313aa	mov x3,x19
0x4cc1378	43a21197	bl 0x01129c84
0x4cc137c	e8ffc039	ldrsb w8,[sp, #0x3f]
0x4cc1380	0801f837	tbnz w8,#0x1f,0x04cc13a0
0x4cc1384	e85fc039	ldrsb w8,[sp, #0x17]
0x4cc1388	8801f837	tbnz w8,#0x1f,0x04cc13b8
0x4cc138c	fd7b46a9	ldp x29,x30,[sp, #0x60]
0x4cc1390	f44f45a9	ldp x20,x19,[sp, #0x50]
0x4cc1394	f65744a9	ldp x22,x21,[sp, #0x40]
0x4cc1398	ffc30191	add sp,sp,#0x70
0x4cc139c	c0035fd6	ret
0x4cc13a0	e01740f9	ldr x0,[sp, #0x28]
0x4cc13a4	e81f40f9	ldr x8,[sp, #0x38]
0x4cc13a8	01f94092	and x1,x8,#0x7fffffffffffffff
0x4cc13ac	18fb9194	bl 0x0714000c
0x4cc13b0	e85fc039	ldrsb w8,[sp, #0x17]
0x4cc13b4	c8feff36	tbz w8,#0x1f,0x04cc138c
0x4cc13b8	e00340f9	ldr x0,[sp]
0x4cc13bc	e80b40f9	ldr x8,[sp, #0x10]
0x4cc13c0	01f94092	and x1,x8,#0x7fffffffffffffff
0x4cc13c4	12fb9194	bl 0x0714000c
0x4cc13c8	f1ffff17	b 0x04cc138c
