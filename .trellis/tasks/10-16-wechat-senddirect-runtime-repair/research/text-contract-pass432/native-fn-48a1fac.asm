0x48a1fac	28008052	mov w8,#0x1
0x48a1fb0	09e28452	mov w9,#0x2710
0x48a1fb4	1f00096b	cmp w0,w9
0x48a1fb8	09019f1a	csel w9,w8,wzr,eq
0x48a1fbc	1fac0071	cmp w0,#0x2b
0x48a1fc0	0901891a	csel w9,w8,w9,eq
0x48a1fc4	1f0c0071	cmp w0,#0x3
0x48a1fc8	0001891a	csel w0,w8,w9,eq
0x48a1fcc	c0035fd6	ret
