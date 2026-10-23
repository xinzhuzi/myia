// Ghidra inferred pseudocode; requested=0x2673a80
// entry=02673a80 end=02673b9b

void FUN_02673a80(undefined8 param_1,long param_2,undefined8 param_3,long param_4)

{
  ulong uVar1;
  undefined8 *puVar2;
  long lVar3;
  
  uVar1 = *(ulong *)(param_4 + 8);
  if (-1 < (char)*(byte *)(param_4 + 0x17)) {
    uVar1 = (ulong)*(byte *)(param_4 + 0x17);
  }
  if ((uVar1 != 0) || (*(char *)(param_4 + 0x18) == '\x01')) {
    *(uint *)(param_2 + 0x14c) = *(uint *)(param_2 + 0x14c) | 4;
    lVar3 = *(long *)(param_2 + 0x130);
    if (lVar3 == 0) {
      lVar3 = __Znwm(0x28);
      FUN_0559f1c0();
      *(long *)(param_2 + 0x130) = lVar3;
    }
    *(uint *)(lVar3 + 0x20) = *(uint *)(lVar3 + 0x20) | 1;
    puVar2 = *(undefined8 **)(lVar3 + 8);
    if (puVar2 == &DAT_0a524ad0) {
      puVar2 = (undefined8 *)__Znwm(0x18);
      puVar2[1] = 0;
      puVar2[2] = 0;
      *puVar2 = 0;
      *(undefined8 **)(lVar3 + 8) = puVar2;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar2,param_3);
    uVar1 = *(ulong *)(param_4 + 8);
    if (-1 < (char)*(byte *)(param_4 + 0x17)) {
      uVar1 = (ulong)*(byte *)(param_4 + 0x17);
    }
    if (uVar1 != 0) {
      *(uint *)(lVar3 + 0x20) = *(uint *)(lVar3 + 0x20) | 2;
      puVar2 = *(undefined8 **)(lVar3 + 0x10);
      if (puVar2 == &DAT_0a524ad0) {
        puVar2 = (undefined8 *)__Znwm(0x18);
        puVar2[1] = 0;
        puVar2[2] = 0;
        *puVar2 = 0;
        *(undefined8 **)(lVar3 + 0x10) = puVar2;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar2,param_4);
      return;
    }
    *(uint *)(lVar3 + 0x20) = *(uint *)(lVar3 + 0x20) | 4;
    *(undefined1 *)(lVar3 + 0x18) = 1;
  }
  return;
}


