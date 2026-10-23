// Ghidra inferred pseudocode; requested=0x563f1a8
// entry=0563f1a8 end=0563f35f

void FUN_0563f1a8(undefined8 *param_1,long param_2,undefined8 param_3,undefined8 param_4)

{
  undefined1 *puVar1;
  long *plVar2;
  long lVar3;
  ulong uVar4;
  undefined1 **ppuVar5;
  code *pcVar6;
  long *plVar7;
  undefined1 *local_68;
  undefined1 *local_60;
  long *plStack_58;
  undefined1 **local_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*(char *)(param_2 + 0x988) != '\x01') {
    local_60 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0563f89c(&local_60,param_2);
    uVar4 = FUN_009ce478(&local_60);
    if ((uVar4 & 1) == 0) {
      local_68 = (undefined1 *)0x0;
      FUN_056463e4(param_1,&local_68);
    }
    else {
      param_1[7] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[6] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[9] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[8] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
      *param_1 = &SUB_aaaaaaaaaaaaaaaa;
      FUN_0563da78(param_1,param_2,0,param_3,param_4);
    }
    ppuVar5 = &local_60;
    goto LAB_0563f32c;
  }
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0563f89c(&local_68,param_2);
  if (*(long *)(param_2 + 0x990) == 0) {
    FUN_0563fe60(&local_60,param_2,0);
    plVar2 = plStack_58;
    puVar1 = local_60;
    local_60 = (undefined1 *)0x0;
    plStack_58 = (long *)0x0;
    plVar7 = *(long **)(param_2 + 0x998);
    *(long **)(param_2 + 0x998) = plVar2;
    *(undefined1 **)(param_2 + 0x990) = puVar1;
    if (plVar7 != (long *)0x0) {
      LOAcquire();
      lVar3 = plVar7[1];
      plVar7[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar7 + 0x10))(plVar7);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    plVar2 = plStack_58;
    if (plStack_58 != (long *)0x0) {
      LOAcquire();
      lVar3 = plStack_58[1];
      plStack_58[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plStack_58 + 0x10))(plStack_58);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
  }
  local_48 = (undefined1 **)0x0;
  FUN_05646510(param_1,param_2 + 0x990,&local_60);
  if (local_48 == &local_60) {
    pcVar6 = *(code **)(*local_48 + 0x20);
LAB_0563f324:
    (*pcVar6)();
  }
  else if (local_48 != (undefined1 **)0x0) {
    pcVar6 = *(code **)(*local_48 + 0x28);
    goto LAB_0563f324;
  }
  ppuVar5 = &local_68;
LAB_0563f32c:
  FUN_0562b7a8(ppuVar5);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


