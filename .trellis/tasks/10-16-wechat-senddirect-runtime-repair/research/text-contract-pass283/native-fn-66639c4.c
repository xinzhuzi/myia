// Ghidra inferred pseudocode; requested=0x66639c4
// entry=066639c4 end=06663a5f

void FUN_066639c4(long param_1,ulong param_2)

{
  long lVar1;
  
  __ZNSt3__15mutex4lockEv(param_1 + 8);
  if ((((param_2 >> 0x20 != 0) &&
       ((uint)(param_2 >> 0x20) <
        (uint)((ulong)(*(long *)(param_1 + 0xa0) - *(long *)(param_1 + 0x98)) >> 3))) &&
      (lVar1 = *(long *)(*(long *)(param_1 + 0x98) + (param_2 >> 0x20) * 8), lVar1 != 0)) &&
     (*(int *)(lVar1 + 0xc) == (int)param_2)) {
    if ((*(short *)(lVar1 + 4) == 2) && ((*(ushort *)(lVar1 + 6) & 1) != 0)) {
      *(ushort *)(lVar1 + 6) = *(ushort *)(lVar1 + 6) | 2;
    }
    else if (*(long **)(lVar1 + 0x10) != (long *)0x0) {
      (**(code **)(**(long **)(lVar1 + 0x10) + 8))();
      *(undefined8 *)(lVar1 + 0x10) = 0;
    }
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 8);
  return;
}


