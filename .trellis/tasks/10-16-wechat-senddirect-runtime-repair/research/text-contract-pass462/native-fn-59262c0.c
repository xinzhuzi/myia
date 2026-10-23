// Ghidra inferred pseudocode; requested=0x59262c0
// entry=059262c0 end=059262e3

undefined8 FUN_059262c0(long param_1,uint param_2)

{
  undefined8 uVar1;
  
  if (((*(ushort *)(param_1 + 8) >> 1 & 1) != 0) && (*(byte *)(param_1 + 10) != param_2)) {
    uVar1 = FUN_05913fb8(param_1,param_2 & 0xff);
    return uVar1;
  }
  return 0;
}


