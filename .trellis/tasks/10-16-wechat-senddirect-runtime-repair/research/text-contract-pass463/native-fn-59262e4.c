// Ghidra inferred pseudocode; requested=0x59262e4
// entry=059262e4 end=0592640b

undefined8 FUN_059262e4(long param_1,int param_2,int param_3)

{
  ushort uVar1;
  bool bVar2;
  undefined4 uVar3;
  long lVar4;
  undefined8 uVar5;
  
  if (param_2 < 0x21) {
    param_2 = 0x20;
  }
  if ((param_3 == 0) || (*(int *)(param_1 + 0x20) < 1)) {
    if (0 < *(int *)(param_1 + 0x20)) {
      lVar4 = *(long *)(param_1 + 0x18);
      goto LAB_0592636c;
    }
  }
  else {
    lVar4 = *(long *)(param_1 + 0x18);
    if (*(long *)(param_1 + 0x10) == lVar4) {
      lVar4 = FUN_058e0924(*(undefined8 *)(param_1 + 0x28),*(long *)(param_1 + 0x10),param_2);
      *(long *)(param_1 + 0x10) = lVar4;
      *(long *)(param_1 + 0x18) = lVar4;
      bVar2 = true;
      goto joined_r0x05926390;
    }
LAB_0592636c:
    FUN_058e00b4(*(undefined8 *)(param_1 + 0x28),lVar4);
  }
  lVar4 = FUN_058e05b0(*(undefined8 *)(param_1 + 0x28),param_2);
  *(long *)(param_1 + 0x18) = lVar4;
  bVar2 = param_3 == 0;
joined_r0x05926390:
  if (lVar4 == 0) {
    if ((*(ushort *)(param_1 + 8) & 0x2400) == 0) {
      *(undefined2 *)(param_1 + 8) = 1;
    }
    else {
      FUN_05926da4(param_1);
    }
    *(undefined8 *)(param_1 + 0x10) = 0;
    *(undefined4 *)(param_1 + 0x20) = 0;
    uVar5 = 7;
  }
  else {
    uVar3 = FUN_058dffb4(*(undefined8 *)(param_1 + 0x28));
    *(undefined4 *)(param_1 + 0x20) = uVar3;
    if ((!bVar2) && (*(void **)(param_1 + 0x10) != (void *)0x0)) {
      _memcpy(*(void **)(param_1 + 0x18),*(void **)(param_1 + 0x10),(long)*(int *)(param_1 + 0xc));
    }
    uVar1 = *(ushort *)(param_1 + 8);
    if ((uVar1 >> 10 & 1) != 0) {
      (**(code **)(param_1 + 0x30))(*(undefined8 *)(param_1 + 0x10));
      uVar1 = *(ushort *)(param_1 + 8);
    }
    uVar5 = 0;
    *(undefined8 *)(param_1 + 0x10) = *(undefined8 *)(param_1 + 0x18);
    *(ushort *)(param_1 + 8) = uVar1 & 0xe3ff;
  }
  return uVar5;
}


