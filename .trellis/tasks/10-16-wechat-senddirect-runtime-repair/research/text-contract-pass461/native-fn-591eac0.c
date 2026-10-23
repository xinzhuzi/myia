// Ghidra inferred pseudocode; requested=0x591eac0
// entry=0591eac0 end=0591ebab

undefined8
FUN_0591eac0(long *param_1,int param_2,long param_3,undefined8 param_4,code *param_5,
            undefined8 param_6)

{
  undefined8 uVar1;
  long lVar2;
  
  uVar1 = FUN_0591ec10();
  if ((int)uVar1 == 0) {
    if (param_3 == 0) {
      uVar1 = 0;
    }
    else {
      lVar2 = param_1[0x10] + (long)param_2 * 0x38 + -0x38;
      uVar1 = FUN_0592720c(lVar2,param_3,param_4,param_6,param_5);
      if (((int)param_6 != 0) && ((int)uVar1 == 0)) {
        uVar1 = FUN_059262c0(lVar2,*(undefined1 *)(*param_1 + 0x5e));
      }
      if ((int)uVar1 != 0) {
        FUN_0591472c(*param_1,uVar1);
        uVar1 = FUN_058e0ccc(*param_1,uVar1);
      }
    }
    FUN_058e17a4(*(undefined8 *)(*param_1 + 0x18));
  }
  else if ((code *)((long)&MACH_HEADER.magic + 1) < param_5 + 1) {
    (*param_5)(param_3);
  }
  return uVar1;
}


