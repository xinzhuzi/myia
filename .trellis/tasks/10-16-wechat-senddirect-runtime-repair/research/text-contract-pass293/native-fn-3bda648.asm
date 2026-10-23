0x3bda648	ffc300d1	sub sp,sp,#0x30
0x3bda64c	f44f01a9	stp x20,x19,[sp, #0x10]
0x3bda650	fd7b02a9	stp x29,x30,[sp, #0x20]
0x3bda654	fd830091	add x29,sp,#0x20
0x3bda658	f30308aa	mov x19,x8
0x3bda65c	e8f301b2	orr x8,xzr,#-0x5555555555555556
0x3bda660	e82300a9	stp x8,x8,[sp]
0x3bda664	3f040071	cmp w1,#0x1
0x3bda668	c0010054	b.eq 0x03bda6a0
0x3bda66c	3f080071	cmp w1,#0x2
0x3bda670	c1040054	b.ne 0x03bda708
0x3bda674	f40300aa	mov x20,x0
0x3bda678	e10302aa	mov x1,x2
0x3bda67c	02008052	mov w2,#0x0
0x3bda680	c3d4dd97	bl 0x0334f98c
0x3bda684	e10300aa	mov x1,x0
0x3bda688	e8030091	mov x8,sp
0x3bda68c	e00314aa	mov x0,x20
0x3bda690	80eadd97	bl 0x03355090
0x3bda694	f40340f9	ldr x20,[sp]
0x3bda698	940100b5	cbnz x20,0x03bda6c8
0x3bda69c	1c000014	b 0x03bda70c
0x3bda6a0	f40300aa	mov x20,x0
0x3bda6a4	e10302aa	mov x1,x2
0x3bda6a8	02008052	mov w2,#0x0
0x3bda6ac	b5a3dd97	bl 0x03343580
0x3bda6b0	e10300aa	mov x1,x0
0x3bda6b4	e8030091	mov x8,sp
0x3bda6b8	e00314aa	mov x0,x20
0x3bda6bc	2ec0dd97	bl 0x0334a774
0x3bda6c0	f40340f9	ldr x20,[sp]
0x3bda6c4	540200b4	cbz x20,0x03bda70c
0x3bda6c8	800640f9	ldr x0,[x20, #0x8]
0x3bda6cc	000200b4	cbz x0,0x03bda70c
0x3bda6d0	41120390	adrp x1,0x9e22000
0x3bda6d4	21801e91	add x1,x1,#0x7a0
0x3bda6d8	a21003f0	adrp x2,0x9df1000
0x3bda6dc	42001391	add x2,x2,#0x4c0
0x3bda6e0	030080d2	mov x3,#0x0
0x3bda6e4	9296d594	bl 0x0714012c
0x3bda6e8	200100b4	cbz x0,0x03bda70c
0x3bda6ec	880a40f9	ldr x8,[x20, #0x10]
0x3bda6f0	602200a9	stp x0,x8,[x19]
0x3bda6f4	e80000b4	cbz x8,0x03bda710
0x3bda6f8	08210091	add x8,x8,#0x8
0x3bda6fc	29008052	mov w9,#0x1
0x3bda700	080129f8	ldadd x9,x8,[x8]
0x3bda704	03000014	b 0x03bda710
0x3bda708	ff7f00a9	stp xzr,xzr,[sp]
0x3bda70c	7f7e00a9	stp xzr,xzr,[x19]
0x3bda710	f30740f9	ldr x19,[sp, #0x8]
0x3bda714	730100b4	cbz x19,0x03bda740
0x3bda718	68220091	add x8,x19,#0x8
0x3bda71c	09008092	mov x9,#-0x1
0x3bda720	0801e9f8	ldaddal x9,x8,[x8]
0x3bda724	e80000b5	cbnz x8,0x03bda740
0x3bda728	680240f9	ldr x8,[x19]
0x3bda72c	080940f9	ldr x8,[x8, #0x10]
0x3bda730	e00313aa	mov x0,x19
0x3bda734	00013fd6	blr x8
0x3bda738	e00313aa	mov x0,x19
0x3bda73c	3895d594	bl 0x0713fc1c
0x3bda740	fd7b42a9	ldp x29,x30,[sp, #0x20]
0x3bda744	f44f41a9	ldp x20,x19,[sp, #0x10]
0x3bda748	ffc30091	add sp,sp,#0x30
0x3bda74c	c0035fd6	ret
