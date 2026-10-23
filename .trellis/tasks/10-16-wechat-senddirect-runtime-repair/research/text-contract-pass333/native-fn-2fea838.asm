0x2fea838	f44fbea9	stp x20,x19,[sp, #-0x20]!
0x2fea83c	fd7b01a9	stp x29,x30,[sp, #0x10]
0x2fea840	fd430091	add x29,sp,#0x10
0x2fea844	f40300aa	mov x20,x0
0x2fea848	00198052	mov w0,#0xc8
0x2fea84c	f9550595	bl 0x07140030
0x2fea850	f30300aa	mov x19,x0
0x2fea854	a86f03d0	adrp x8,0x9de0000
0x2fea858	08012c91	add x8,x8,#0xb00
0x2fea85c	088400f8	str x8,[x0], #0x8
0x2fea860	81220091	add x1,x20,#0x8
0x2fea864	54030094	bl 0x02feb5b4
0x2fea868	e00313aa	mov x0,x19
0x2fea86c	fd7b41a9	ldp x29,x30,[sp, #0x10]
0x2fea870	f44fc2a8	ldp x20,x19,[sp], #0x20
0x2fea874	c0035fd6	ret
