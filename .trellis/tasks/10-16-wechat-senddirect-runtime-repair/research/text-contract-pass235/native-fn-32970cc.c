// Ghidra inferred pseudocode; requested=0x32970cc
// entry=032970cc end=0329725b

undefined8 FUN_032970cc(long param_1)

{
  byte bVar1;
  ulong uVar2;
  undefined8 uVar3;
  long lVar4;
  undefined **local_58;
  long lStack_50;
  undefined ***local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  bVar1 = *(byte *)(param_1 + 0xb8);
  uVar3 = 1;
  if (bVar1 < 3) {
    if (bVar1 == 1) {
      uVar2 = FUN_056f5578(param_1,1);
      if ((uVar2 & 1) == 0) {
LAB_032971fc:
        uVar3 = 0;
        goto LAB_03297200;
      }
LAB_032971d8:
      uVar3 = FUN_032973c8(param_1);
LAB_032971e4:
      FUN_056f5598(param_1,uVar3);
    }
    else if (bVar1 == 2) {
      lVar4 = ((*(long **)(param_1 + 0xc0))[1] - **(long **)(param_1 + 0xc0) >> 3) *
              -0x6474a8819ec8e951;
joined_r0x03297164:
      if (lVar4 != 0) goto LAB_03297168;
LAB_0329713c:
      uVar3 = 1;
    }
  }
  else {
    if (bVar1 == 3) {
      lVar4 = (*(long **)(param_1 + 0xc0))[1] - **(long **)(param_1 + 0xc0) >> 3;
      if (lVar4 == 0) goto LAB_0329713c;
LAB_03297168:
      uVar2 = FUN_056f5578(param_1,1);
      if ((uVar2 & 1) == 0) goto LAB_032971fc;
      if (lVar4 == 1) goto LAB_032971d8;
      local_58 = &PTR_FUN_09df1c38;
      lStack_50 = param_1;
      local_40 = &local_58;
      uVar3 = FUN_056f412c(*(long *)(param_1 + 8) + 8,&local_58);
      if (local_40 == &local_58) {
        (*(code *)(*local_40)[4])();
      }
      else if (local_40 != (undefined ***)0x0) {
        (*(code *)(*local_40)[5])();
      }
      goto LAB_032971e4;
    }
    if (bVar1 == 4) {
      lVar4 = (*(long **)(param_1 + 0xc0))[1] - **(long **)(param_1 + 0xc0) >> 4;
      goto joined_r0x03297164;
    }
  }
  FUN_056f8d28(*(undefined8 *)(param_1 + 8));
LAB_03297200:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return uVar3;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


