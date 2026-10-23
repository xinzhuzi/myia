// Ghidra inferred pseudocode; requested=0x30265e8
// entry=030265e8 end=030267db

void FUN_030265e8(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  byte bVar1;
  long *plVar2;
  ulong uVar3;
  undefined8 local_98 [12];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar2 = (long *)FUN_056fa6f4(param_3);
  bVar1 = (**(code **)(*plVar2 + 0x10))();
  if (bVar1 < 3) {
    if (bVar1 == 1) {
      uVar3 = (**(code **)(*plVar2 + 0x18))(plVar2,param_2);
      if ((uVar3 & 1) != 0) {
LAB_03026748:
        if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
          FUN_056f4f6c(param_1,param_4);
          return;
        }
        goto LAB_030267d8;
      }
      local_98[0] = (**(code **)(*plVar2 + 0x30))(plVar2,param_2);
      FUN_056f4e3c(param_1,local_98,param_4);
    }
    else if (bVar1 == 2) {
      uVar3 = (**(code **)(*plVar2 + 0x18))(plVar2,param_2);
      if ((uVar3 & 1) != 0) goto LAB_03026748;
      local_98[0] = (**(code **)(*plVar2 + 0x30))(plVar2,param_2);
      FUN_056f4e88(param_1,local_98,param_4);
    }
  }
  else if (bVar1 == 3) {
    uVar3 = (**(code **)(*plVar2 + 0x18))(plVar2,param_2);
    if ((uVar3 & 1) != 0) goto LAB_03026748;
    (**(code **)(*plVar2 + 0x30))(local_98,plVar2,param_2);
    FUN_056f4ed4(param_1,local_98,param_4);
    FUN_0562fd84(local_98);
  }
  else if (bVar1 == 4) {
    uVar3 = (**(code **)(*plVar2 + 0x18))(plVar2,param_2);
    if ((uVar3 & 1) != 0) goto LAB_03026748;
    (**(code **)(*plVar2 + 0x30))(local_98,plVar2,param_2);
    FUN_056f4f20(param_1,local_98,param_4);
    FUN_0563255c(local_98);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
LAB_030267d8:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


