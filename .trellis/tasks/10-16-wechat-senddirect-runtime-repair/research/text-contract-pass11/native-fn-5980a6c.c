// Ghidra inferred pseudocode; requested=0x5980a6c
// entry=05980a6c end=05980d73

void FUN_05980a6c(undefined8 *param_1,ulong param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5)

{
  char cVar1;
  ulong uVar2;
  long lVar3;
  int iVar4;
  int iVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  char *pcVar8;
  char *pcVar9;
  ulong uVar10;
  char *pcVar11;
  uint uVar12;
  undefined1 auStack_1b8 [144];
  long *local_128;
  long *local_120;
  undefined8 local_118;
  char local_110 [72];
  undefined8 *local_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_05980d74(&local_128);
  if (local_128 != (long *)0x0) {
    iVar4 = thunk_FUN_05e1d97c(2);
    if (iVar4 != 0) {
      FUN_05e1d050(auStack_1b8,2,"mars::mmext","actiontask_mgr.cc","Req2Buf",0xdc,0,0);
      local_118 = (char *)0x0;
      uVar2 = 8;
      do {
        uVar10 = uVar2;
        uVar12 = (uint)param_2;
        local_110[uVar10 - 8] =
             "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             [uVar12 + (int)((param_2 & 0xffffffff) / 10) * -10 + 0x23];
        uVar2 = uVar10 + 1;
        param_2 = (param_2 & 0xffffffff) / 10;
      } while (9 < uVar12);
      *(undefined1 *)((long)&local_118 + uVar10 + 1) = 0;
      local_118 = local_110;
      if (8 < uVar10) {
        pcVar11 = local_110;
        pcVar8 = local_110 + (uVar10 - 8);
        do {
          pcVar11 = pcVar11 + 1;
          cVar1 = *pcVar8;
          pcVar9 = pcVar8 + -1;
          *pcVar8 = pcVar11[-1];
          pcVar11[-1] = cVar1;
          pcVar8 = pcVar9;
        } while (pcVar11 < pcVar9);
      }
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      local_60 = 0;
      local_50 = 0;
      local_c8 = &local_118;
      FUN_05e1d31c(auStack_1b8,"req2buf taskid:%_",&local_c8);
      thunk_FUN_05e1d0bc(auStack_1b8);
    }
    FUN_05a6c374(&local_c8,local_128 + 1);
    if (((uStack_a8._4_1_ >> 3 & 1) == 0) && (iVar4 = thunk_FUN_05e1d97c(5), iVar4 != 0)) {
      FUN_05e1d050(auStack_1b8,5,"mars::mmext","actiontask_mgr.cc","Req2Buf",0xde,0,0);
      FUN_05e1d244(auStack_1b8,"ack.has_error()");
      thunk_FUN_05e1d0bc(auStack_1b8);
    }
    if ((((uStack_a8._4_1_ >> 1 & 1) != 0) &&
        (iVar4 = (int)local_b0, iVar5 = (**(code **)(*local_128 + 0x10))(local_128), iVar4 != iVar5)
        ) && (iVar4 = thunk_FUN_05e1d97c(5), iVar4 != 0)) {
      FUN_05e1d050(auStack_1b8,5,"mars::mmext","actiontask_mgr.cc","Req2Buf",0xdf,0,0);
      FUN_05e1d244(auStack_1b8,
                   "!ack.has_action_code() || ack.action_code() == sptask->GetActionCode()");
      thunk_FUN_05e1d0bc(auStack_1b8);
    }
    iVar4 = FUN_05a6c868(&local_c8);
    FUN_05ded378(param_5,(long)iVar4,1);
    uVar6 = FUN_056300b4(param_5,0);
    uVar7 = FUN_05a6c868(&local_c8);
    thunk_FUN_05ab3f9c(&local_c8,uVar6,uVar7);
    uVar6 = FUN_0594c390(*param_1);
    FUN_0597e100(uVar6,0x11,0x26,1,0);
    FUN_05a6c43c(&local_c8);
  }
  if (local_120 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_120[1];
    local_120[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_120 + 0x10))(local_120);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_120);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(local_128 != (long *)0x0);
}


