// Ghidra inferred pseudocode; requested=0x32979e0
// entry=032979e0 end=03297abb

ulong FUN_032979e0(long param_1,long param_2,long *param_3)

{
  undefined8 uVar1;
  long lVar2;
  ulong uVar3;
  
  FUN_056f4e0c(*(undefined8 *)(param_1 + 8));
  lVar2 = *(long *)(param_1 + 0xa8);
  if (lVar2 != param_1 + 0xa0) {
    uVar3 = 0;
    do {
      if (((param_3[1] == 0) ||
          ((*(ulong *)(*param_3 + (uVar3 >> 3 & 0x1ffffffffffffff8)) >> (uVar3 & 0x3f) & 1) == 0))
         || ((*(byte *)(param_2 + 0x218) & 1) == 0)) {
        FUN_030265e8(*(undefined8 *)(param_1 + 8),param_2,lVar2 + 0x10,(int)uVar3 + 1);
      }
      else {
        FUN_056f4f6c(*(undefined8 *)(param_1 + 8),(int)uVar3 + 1);
      }
      lVar2 = *(long *)(lVar2 + 8);
      uVar3 = uVar3 + 1;
    } while (lVar2 != param_1 + 0xa0);
  }
  uVar3 = FUN_056f4db0(*(undefined8 *)(param_1 + 8));
  if ((uVar3 & 1) != 0) {
    uVar1 = FUN_056f90e0(*(undefined8 *)(param_1 + 8));
    **(undefined8 **)(param_2 + 0x208) = uVar1;
  }
  return uVar3;
}


