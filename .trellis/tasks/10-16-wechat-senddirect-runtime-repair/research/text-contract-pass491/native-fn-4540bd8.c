// Ghidra inferred pseudocode; requested=0x4540bd8
// entry=04540bd8 end=04540e07

/* WARNING: Type propagation algorithm not settling */

void FUN_04540bd8(undefined8 *param_1,long param_2,long *param_3)

{
  ulong uVar1;
  char *pcVar2;
  long *plVar3;
  undefined8 *******pppppppuVar4;
  long lVar5;
  undefined8 *puVar6;
  code *pcVar7;
  undefined8 local_a0;
  long *local_98;
  undefined8 *******local_90;
  long *local_88;
  undefined8 local_80;
  long alStack_78 [3];
  long *local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  pcVar2 = (char *)(**(code **)(*param_3 + 0x10))(param_3);
  plVar3 = (long *)_strlen(pcVar2);
  if ((long *)0x7ffffffffffffff7 < plVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_90);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar3) {
    uVar1 = 0x19;
    if (((ulong)plVar3 | 7) != 0x17) {
      uVar1 = ((ulong)plVar3 | 7) + 1;
    }
    pppppppuVar4 = (undefined8 *******)__Znwm(uVar1);
    local_80 = (undefined1 *)(uVar1 | 0x8000000000000000);
    local_90 = pppppppuVar4;
    local_88 = plVar3;
LAB_04540c78:
    _memmove(pppppppuVar4,pcVar2,(size_t)plVar3);
  }
  else {
    local_80 = (undefined1 *)CONCAT17((char)plVar3,(undefined7)local_80);
    pppppppuVar4 = &local_90;
    if (plVar3 != (long *)0x0) goto LAB_04540c78;
  }
  *(undefined1 *)((long)pppppppuVar4 + (long)plVar3) = 0;
  lVar5 = FUN_04541d70(param_2,&local_90);
  if ((long)local_80 < 0) {
    __ZdlPvm(local_90,(ulong)local_80 & 0x7fffffffffffffff);
  }
  if (lVar5 != 0) {
    *param_1 = &SUB_aaaaaaaaaaaaaaaa;
    param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
    local_a0 = *(undefined8 *)(lVar5 + 0x28);
    local_98 = *(long **)(lVar5 + 0x30);
    if (local_98 != (long *)0x0) {
      local_98[1] = local_98[1] + 1;
    }
    (**(code **)(*param_3 + 0x20))(param_1,param_3,&local_a0);
    plVar3 = local_98;
    goto joined_r0x04540ce0;
  }
  local_88 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_90 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  local_60 = (long *)__Znwm(0x20);
  *local_60 = (long)&PTR_FUN_09e870a8;
  local_60[1] = param_2;
  local_60[2] = (long)pcVar2;
  local_60[3] = (long)param_3;
  FUN_0666ab58(&local_90,alStack_78);
  if (local_60 == alStack_78) {
    pcVar7 = *(code **)(*local_60 + 0x20);
LAB_04540d64:
    (*pcVar7)();
  }
  else if (local_60 != (long *)0x0) {
    pcVar7 = *(code **)(*local_60 + 0x28);
    goto LAB_04540d64;
  }
  FUN_066856fc(&local_90);
  puVar6 = (undefined8 *)FUN_021b3684(&local_90);
  *param_1 = *puVar6;
  lVar5 = puVar6[1];
  param_1[1] = lVar5;
  plVar3 = local_88;
  if (lVar5 != 0) {
    *(long *)(lVar5 + 8) = *(long *)(lVar5 + 8) + 1;
  }
joined_r0x04540ce0:
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar3[1];
    plVar3[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


