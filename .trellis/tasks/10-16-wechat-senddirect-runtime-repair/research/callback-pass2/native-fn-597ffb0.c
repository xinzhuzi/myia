// Ghidra inferred pseudocode; requested=0x597ffb0
// entry=0597ffb0 end=059809ff

ulong FUN_0597ffb0(undefined8 *param_1,long param_2,int param_3,undefined8 param_4,
                  undefined8 param_5)

{
  char cVar1;
  undefined1 uVar2;
  ulong uVar3;
  bool bVar4;
  long lVar5;
  int iVar6;
  int iVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  ulong uVar11;
  long *plVar12;
  long *plVar13;
  uint uVar14;
  undefined1 *puVar15;
  ulong uVar16;
  char *pcVar17;
  char *pcVar18;
  undefined1 *puVar19;
  char *pcVar20;
  ulong uVar21;
  long *plVar22;
  long *local_680;
  long *local_678;
  long *local_670;
  long *local_668;
  undefined8 *local_660;
  undefined8 *apuStack_658 [67];
  long *local_440;
  long *local_438;
  undefined1 auStack_430 [40];
  undefined4 local_408;
  byte local_400;
  undefined1 *local_3f8;
  undefined1 auStack_3f0 [72];
  undefined8 local_3a8;
  undefined8 local_3a0;
  undefined8 local_358;
  char local_350 [72];
  undefined8 local_308;
  undefined8 local_300;
  undefined8 uStack_2f8;
  undefined8 local_2f0;
  undefined8 uStack_2e8;
  undefined8 local_2e0;
  undefined8 uStack_2d8;
  undefined8 local_2d0;
  undefined8 uStack_2c8;
  undefined8 local_2c0;
  undefined8 uStack_2b8;
  undefined8 local_2b0;
  undefined8 uStack_2a8;
  undefined8 *****local_2a0;
  undefined8 uStack_298;
  long local_290;
  undefined8 **local_f0;
  undefined8 *local_e8;
  undefined1 **ppuStack_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar11 = *(ulong *)(param_2 + 8);
  if (-1 < (char)*(byte *)(param_2 + 0x17)) {
    uVar11 = (ulong)*(byte *)(param_2 + 0x17);
  }
  if ((uVar11 == 0) && (iVar6 = thunk_FUN_05e1d97c(5), iVar6 != 0)) {
    FUN_05e1d050(&local_660,5,"mars::mmext","actiontask_mgr.cc","OnPush",0x88,0,0);
    FUN_05e1d244(&local_660,"!_channel_id.empty()");
    thunk_FUN_05e1d0bc(&local_660);
  }
  if (param_3 == 0x164) {
    uVar8 = FUN_0594c390(*param_1);
    FUN_0597e100(uVar8,0x11,0x20,1,0);
    FUN_05a6b83c(auStack_430);
    uVar9 = FUN_056300b4(param_5,0);
    uVar10 = FUN_009ce4a8(param_5);
    uVar11 = FUN_05ab3ab8(auStack_430,uVar9,uVar10);
    if ((uVar11 & 1) == 0) {
      iVar6 = thunk_FUN_05e1d97c(3);
      if (iVar6 != 0) {
        FUN_05e1d050(&local_660,3,"mars::mmext","actiontask_mgr.cc","OnPush",0x92,0,0);
        local_308 = &local_f0;
        local_f0 = &local_e8;
        local_e8 = (undefined8 *)CONCAT44(local_e8._4_4_,(int)DAT_08b7d390);
        uStack_2f8 = 0;
        local_300 = 0;
        uStack_2e8 = 0;
        local_2f0 = 0;
        uStack_2d8 = 0;
        local_2e0 = 0;
        uStack_2c8 = 0;
        local_2d0 = 0;
        uStack_2b8 = 0;
        local_2c0 = 0;
        uStack_2a8 = 0;
        local_2b0 = 0;
        uStack_298 = 0;
        local_2a0 = (undefined8 ******)0x0;
        local_290 = 0;
        FUN_05e1d31c(&local_660,"parse failed. cmdid %_",&local_308);
        thunk_FUN_05e1d0bc(&local_660);
      }
    }
    else {
      local_660 = param_1;
      if ((local_400 >> 1 & 1) == 0) {
        uVar8 = FUN_0594c390(*param_1);
        FUN_0597e100(uVar8,0x11,0x21,1,0);
        FUN_0597fc08(&local_308,param_1,param_2);
        plVar12 = (long *)__Znwm(0x50);
        plVar22 = plVar12 + 1;
        *plVar22 = 0;
        plVar12[2] = 0;
        *plVar12 = (long)&PTR_FUN_09f2e7c0;
        plVar13 = plVar12 + 3;
        *plVar13 = (long)&PTR_FUN_09f2e6d8;
        FUN_05a6b860(plVar12 + 4);
        *plVar13 = (long)&PTR_FUN_09f2e810;
        *(undefined4 *)(plVar12 + 9) = 2;
        FUN_05981abc(plVar13,*param_1,auStack_430,&local_308);
        *(uint *)((long)plVar12 + 0x44) = *(uint *)((long)plVar12 + 0x44) | 8;
        *(int *)((long)plVar12 + 0x3c) = (int)plVar12[9];
        thunk_FUN_05daa3c8(apuStack_658,&local_308);
        lVar5 = *plVar22;
        *plVar22 = lVar5 + 1;
        local_440 = plVar13;
        local_438 = plVar12;
        __ZNSt3__15mutex4lockEv(lVar5,param_1 + 1);
        local_f0 = apuStack_658;
        lVar5 = FUN_05981638(local_660 + 0xe,apuStack_658,&DAT_08b7a8b8,&local_f0,&local_358);
        FUN_059815d0(lVar5 + 0x18,&local_440);
        __ZNSt3__15mutex6unlockEv(param_1 + 1);
        plVar13 = local_438;
        if (local_438 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_438[1];
          local_438[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_438 + 0x10))(local_438);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
          }
        }
        FUN_046364ec(apuStack_658);
        iVar6 = thunk_FUN_05e1d97c(3);
        if (iVar6 != 0) {
          FUN_05e1d050(&local_660,3,"mars::mmext","actiontask_mgr.cc","OnPush",0xa3,0,0);
          local_358 = (char *)0x0;
          uVar16 = (ulong)local_308 & 0xffffffff;
          uVar3 = 8;
          do {
            uVar21 = uVar3;
            uVar14 = (uint)uVar16;
            local_350[uVar21 - 8] =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar14 + (int)(uVar16 / 10) * -10 + 0x23];
            uVar16 = uVar16 / 10;
            uVar3 = uVar21 + 1;
          } while (9 < uVar14);
          *(undefined1 *)((long)&local_358 + uVar21 + 1) = 0;
          local_358 = local_350;
          if (8 < uVar21) {
            pcVar20 = local_350;
            pcVar18 = local_350 + (uVar21 - 8);
            do {
              pcVar20 = pcVar20 + 1;
              cVar1 = *pcVar18;
              pcVar17 = pcVar18 + -1;
              *pcVar18 = pcVar20[-1];
              pcVar20[-1] = cVar1;
              pcVar18 = pcVar17;
            } while (pcVar20 < pcVar17);
          }
          ppuStack_e0 = (undefined1 **)0x0;
          local_e8 = (undefined8 *)0x0;
          uStack_d0 = 0;
          local_d8 = 0;
          uStack_c0 = 0;
          local_c8 = 0;
          uStack_b0 = 0;
          local_b8 = 0;
          uStack_a0 = 0;
          local_a8 = 0;
          uStack_90 = 0;
          local_98 = 0;
          uStack_80 = 0;
          local_88 = 0;
          local_78 = 0;
          local_f0 = (undefined8 **)&local_358;
          FUN_05e1d31c(&local_660,"no accode, ack taskid:%_",&local_f0);
          thunk_FUN_05e1d0bc(&local_660);
        }
        if (((local_308._4_4_ == 0) || ((int)local_308 == 0)) &&
           (iVar6 = thunk_FUN_05e1d97c(5), iVar6 != 0)) {
          FUN_05e1d050(&local_660,5,"mars::mmext","actiontask_mgr.cc","OnPush",0xa4,0,0);
          FUN_05e1d244(&local_660,"ack.cmdid != 0 && ack.taskid != 0");
          thunk_FUN_05e1d0bc(&local_660);
        }
        FUN_0597eda0(uVar8,&local_308);
        LOAcquire();
        lVar5 = *plVar22;
        *plVar22 = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*plVar12 + 0x10))(plVar12);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
        }
        FUN_046364ec(&local_308);
      }
      else {
        FUN_05980a00(&local_670,param_1,local_408);
        plVar13 = local_668;
        if (local_670 == (long *)0x0) {
          plVar13 = (long *)__Znwm(0x48);
          plVar13[2] = 0;
          *plVar13 = (long)&PTR_FUN_09f2e720;
          plVar13[1] = 0;
          plVar22 = plVar13 + 3;
          *plVar22 = (long)&PTR_FUN_09f2e6d8;
          FUN_05a6b860(plVar13 + 4);
          plVar12 = local_668;
          *plVar22 = (long)&PTR_FUN_09f2e770;
          local_670 = plVar22;
          if (local_668 != (long *)0x0) {
            LOAcquire();
            lVar5 = local_668[1];
            local_668[1] = lVar5 + -1;
            LORelease();
            if (lVar5 == 0) {
              lVar5 = *local_668;
              local_668 = plVar13;
              (**(code **)(lVar5 + 0x10))(plVar12);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
              plVar13 = local_668;
            }
          }
        }
        local_668 = plVar13;
        FUN_0597fc08(&local_308,param_1,param_2);
        (**(code **)(*local_670 + 0x20))(&local_680);
        iVar6 = (**(code **)(*local_680 + 0x18))(local_680,*param_1,auStack_430,&local_308);
        thunk_FUN_05daa3c8(apuStack_658,&local_308);
        local_440 = local_680;
        local_438 = local_678;
        lVar5 = 0;
        if (local_678 != (long *)0x0) {
          lVar5 = local_678[1];
          local_678[1] = lVar5 + 1;
        }
        __ZNSt3__15mutex4lockEv(lVar5,param_1 + 1);
        local_f0 = apuStack_658;
        lVar5 = FUN_05981638(local_660 + 0xe,apuStack_658,&DAT_08b7a8b8,&local_f0,&local_358);
        FUN_059815d0(lVar5 + 0x18,&local_440);
        __ZNSt3__15mutex6unlockEv(param_1 + 1);
        plVar13 = local_438;
        if (local_438 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_438[1];
          local_438[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_438 + 0x10))(local_438);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
          }
        }
        FUN_046364ec(apuStack_658);
        iVar7 = thunk_FUN_05e1d97c(2);
        if (iVar7 != 0) {
          FUN_05e1d050(&local_660,2,"mars::mmext","actiontask_mgr.cc","OnPush",0xbb,0,0);
          local_f0 = (undefined8 **)CONCAT44(local_f0._4_4_,local_408);
          local_358 = (char *)0x0;
          FUN_003eccb4(&local_f0,local_350,10,1);
          local_358 = local_350;
          local_3a8 = (undefined8 ******)0x0;
          uVar16 = (ulong)local_308 & 0xffffffff;
          uVar3 = 8;
          do {
            uVar21 = uVar3;
            uVar14 = (uint)uVar16;
            *(char *)((long)&local_3a8 + uVar21) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar14 + (int)(uVar16 / 10) * -10 + 0x23];
            uVar16 = uVar16 / 10;
            uVar3 = uVar21 + 1;
          } while (9 < uVar14);
          *(undefined1 *)((long)&local_3a8 + uVar21 + 1) = 0;
          local_3a8 = (undefined8 ******)&local_3a0;
          if (8 < uVar21) {
            puVar15 = (undefined1 *)((long)&local_3a8 + uVar21);
            puVar19 = (undefined1 *)((long)&local_3a0 + 1);
            do {
              uVar2 = *puVar15;
              *puVar15 = puVar19[-1];
              puVar19[-1] = uVar2;
              bVar4 = puVar19 < puVar15 + -1;
              puVar15 = puVar15 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar4);
          }
          local_f0 = (undefined8 **)CONCAT44(local_f0._4_4_,iVar6);
          local_3f8 = (undefined1 *)0x0;
          FUN_003eccb4(&local_f0,auStack_3f0,10,1);
          local_f0 = (undefined8 **)&local_358;
          uStack_d0 = 0;
          local_d8 = 0;
          uStack_c0 = 0;
          local_c8 = 0;
          uStack_b0 = 0;
          local_b8 = 0;
          uStack_a0 = 0;
          local_a8 = 0;
          uStack_90 = 0;
          local_98 = 0;
          uStack_80 = 0;
          local_88 = 0;
          local_78 = 0;
          local_3f8 = auStack_3f0;
          local_e8 = &local_3a8;
          ppuStack_e0 = &local_3f8;
          FUN_05e1d31c(&local_660,"accode %_ ack taskid:%_ retcode %_",&local_f0);
          thunk_FUN_05e1d0bc(&local_660);
        }
        if (((local_308._4_4_ == 0) || ((int)local_308 == 0)) &&
           (iVar7 = thunk_FUN_05e1d97c(5), iVar7 != 0)) {
          FUN_05e1d050(&local_660,5,"mars::mmext","actiontask_mgr.cc","OnPush",0xbe,0,0);
          FUN_05e1d244(&local_660,"ack.cmdid != 0 && ack.taskid != 0");
          thunk_FUN_05e1d0bc(&local_660);
        }
        if (iVar6 == -100) {
          __ZNSt3__15mutex4lockEv(param_1 + 1);
          local_660 = &local_308;
          lVar5 = FUN_059821cc(param_1 + 0x13,&local_308,&DAT_08b7a8b8,&local_660,&local_f0);
          FUN_05daa700(lVar5 + 0x18,&local_308);
          __ZNSt3__15mutex6unlockEv(param_1 + 1);
        }
        else {
          iVar6 = thunk_FUN_05e1d97c(2);
          if (iVar6 != 0) {
            FUN_05e1d050(&local_660,2,"mars::mmext","actiontask_mgr.cc","OnPush",0xc2,0,0);
            local_358 = (char *)0x0;
            uVar16 = (ulong)local_308 & 0xffffffff;
            uVar3 = 8;
            do {
              uVar21 = uVar3;
              uVar14 = (uint)uVar16;
              local_350[uVar21 - 8] =
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   [uVar14 + (int)(uVar16 / 10) * -10 + 0x23];
              uVar16 = uVar16 / 10;
              uVar3 = uVar21 + 1;
            } while (9 < uVar14);
            *(undefined1 *)((long)&local_358 + uVar21 + 1) = 0;
            local_358 = local_350;
            if (8 < uVar21) {
              pcVar20 = local_350;
              pcVar18 = local_350 + (uVar21 - 8);
              do {
                pcVar20 = pcVar20 + 1;
                cVar1 = *pcVar18;
                pcVar17 = pcVar18 + -1;
                *pcVar18 = pcVar20[-1];
                pcVar20[-1] = cVar1;
                pcVar18 = pcVar17;
              } while (pcVar20 < pcVar17);
            }
            local_3a8 = (undefined8 ******)local_2a0;
            if (-1 < local_290) {
              local_3a8 = &local_2a0;
            }
            local_3a0._0_1_ = 0;
            local_e8 = &local_3a8;
            local_d8 = 0;
            ppuStack_e0 = (undefined1 **)0x0;
            local_c8 = 0;
            uStack_d0 = 0;
            local_b8 = 0;
            uStack_c0 = 0;
            local_a8 = 0;
            uStack_b0 = 0;
            local_98 = 0;
            uStack_a0 = 0;
            local_88 = 0;
            uStack_90 = 0;
            local_78 = 0;
            uStack_80 = 0;
            local_f0 = (undefined8 **)&local_358;
            FUN_05e1d31c(&local_660,"start notifyack task %_ ch.name %_",&local_f0);
            thunk_FUN_05e1d0bc(&local_660);
          }
          FUN_0597eda0(uVar8,&local_308);
        }
        if (local_678 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_678[1];
          local_678[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_678 + 0x10))(local_678);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_678);
          }
        }
        FUN_046364ec(&local_308);
        plVar13 = local_668;
        if (local_668 != (long *)0x0) {
          LOAcquire();
          lVar5 = local_668[1];
          local_668[1] = lVar5 + -1;
          LORelease();
          if (lVar5 == 0) {
            (**(code **)(*local_668 + 0x10))(local_668);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
          }
        }
      }
    }
    FUN_05a6bb28(auStack_430);
  }
  else {
    uVar11 = 0;
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_70) {
    return uVar11;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


