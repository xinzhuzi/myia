// Ghidra inferred pseudocode; requested=0x667fd04
// entry=0667fd04 end=066800df

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0667fd04(long param_1,long param_2)

{
  long *plVar1;
  long lVar2;
  ulong uVar3;
  code *pcVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  long lVar8;
  long local_1f8;
  long local_1f0;
  long lStack_1e8;
  long lStack_1e0;
  long lStack_1d8;
  long local_1d0;
  long lStack_1c8;
  long lStack_1c0;
  long lStack_1b8;
  long local_1b0;
  long *plStack_1a8;
  long local_1a0;
  long lStack_198;
  undefined8 local_188;
  undefined8 local_180;
  undefined1 *local_178;
  long alStack_170 [3];
  long *local_158;
  undefined8 *local_150;
  undefined8 *local_148;
  undefined1 *puStack_140;
  long *local_80;
  long **local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_178 = &SUB_aaaaaaaaaaaaaaaa;
  local_180 = FUN_00e39f68(*(undefined8 *)(param_1 + 8));
  local_178 = (undefined1 *)CONCAT71(local_178._1_7_,1);
  __ZNSt3__115recursive_mutex4lockEv();
  uVar3 = FUN_06686644(*(undefined8 *)(param_1 + 8));
  if ((uVar3 & 1) == 0) {
    uVar3 = FUN_0668dad0(4);
    if ((uVar3 & 1) != 0) {
      if ((DAT_0a5181e5 & 1) == 0) {
        DAT_0a5181e0 = (undefined4)ram0x08782918;
        DAT_0a5181e4 = 0;
        DAT_0a5181e5 = 1;
      }
      if ((DAT_0a51827b & 1) == 0) {
        DAT_0a518270._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a518270._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a518270._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a518270._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a518270._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a518270._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a518270._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a518270._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a518278 = 0x2928;
        DAT_0a51827a = 0;
        DAT_0a51827b = 1;
      }
      if ((DAT_0a51828d & 1) == 0) {
        DAT_0a518280._0_1_ = s_signalslot_h_08782920[0];
        DAT_0a518280._1_1_ = s_signalslot_h_08782920[1];
        DAT_0a518280._2_1_ = s_signalslot_h_08782920[2];
        DAT_0a518280._3_1_ = s_signalslot_h_08782920[3];
        DAT_0a518280._4_1_ = s_signalslot_h_08782920[4];
        DAT_0a518280._5_1_ = s_signalslot_h_08782920[5];
        DAT_0a518280._6_1_ = s_signalslot_h_08782920[6];
        DAT_0a518280._7_1_ = s_signalslot_h_08782920[7];
        DAT_0a518288 = (undefined4)ram0x08782928;
        DAT_0a51828c = 0;
        DAT_0a51828d = 1;
      }
      FUN_0668db5c(&local_150,&DAT_0a5181e0,&DAT_0a518270,&DAT_0a518280,0xe500008800);
      if ((DAT_0a5182cf & 1) == 0) {
        uVar3 = 0;
        do {
          (&DAT_0a51828e)[uVar3] = (&DAT_09685e92)[uVar3 & 0xf] ^ (&DAT_09685ea2)[uVar3];
          uVar3 = uVar3 + 1;
        } while (uVar3 != 0x41);
        DAT_0a5182cf = 1;
      }
      plVar5 = local_150 + 0xd;
      if (*(char *)((long)local_150 + 0x7f) < '\0') {
        plVar5 = (long *)*plVar5;
      }
      local_78 = (long **)0xaaaaaaaa00000006;
      local_80 = (long *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_150 + 7,&DAT_0a51828e,plVar5,&local_80,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(&local_150);
    }
  }
  else {
    local_188 = *(undefined8 *)(param_1 + 8);
    local_150 = &local_180;
    local_148 = &local_188;
    puStack_140 = &SUB_aaaaaaaaaaaaaaaa;
    local_78 = &local_80;
    local_80 = (long *)0x0;
    FUN_0668688c(param_1,&local_80);
    if (local_80 != (long *)0x0) {
      plVar5 = local_80;
      do {
        plVar7 = (long *)*plVar5;
        plVar6 = (long *)plVar5[8];
        if (plVar6 == (long *)0x0) {
          local_1f8 = param_2;
          (*(code *)plVar5[2])(plVar5[1],plVar5 + 3,&local_1f8);
        }
        else {
          lStack_1e8 = plVar5[2];
          local_1f0 = plVar5[1];
          lStack_1d8 = plVar5[4];
          lStack_1e0 = plVar5[3];
          lStack_1c8 = plVar5[6];
          local_1d0 = plVar5[5];
          lStack_1b8 = plVar5[8];
          lStack_1c0 = plVar5[7];
          lVar2 = plVar5[9];
          plVar1 = (long *)plVar5[10];
          if (plVar1 != (long *)0x0) {
            plVar1[1] = plVar1[1] + 1;
          }
          lVar8 = plVar5[0xb];
          local_158 = (long *)0x0;
          local_1b0 = lVar2;
          plStack_1a8 = plVar1;
          local_1a0 = lVar8;
          lStack_198 = param_2;
          local_158 = (long *)__Znwm(0x68);
          *local_158 = (long)&PTR_FUN_09fb2df8;
          local_158[2] = lStack_1e8;
          local_158[1] = local_1f0;
          local_158[4] = lStack_1d8;
          local_158[3] = lStack_1e0;
          local_158[6] = lStack_1c8;
          local_158[5] = local_1d0;
          local_158[8] = lStack_1b8;
          local_158[7] = lStack_1c0;
          local_158[9] = lVar2;
          local_158[10] = (long)plVar1;
          if (plVar1 != (long *)0x0) {
            plVar1[1] = plVar1[1] + 1;
          }
          local_158[0xb] = lVar8;
          local_158[0xc] = param_2;
          (**(code **)(*plVar6 + 0x10))(plVar6,alStack_170);
          if (local_158 == alStack_170) {
            pcVar4 = *(code **)(*local_158 + 0x20);
LAB_0667fe8c:
            (*pcVar4)();
          }
          else if (local_158 != (long *)0x0) {
            pcVar4 = *(code **)(*local_158 + 0x28);
            goto LAB_0667fe8c;
          }
          if (plVar1 != (long *)0x0) {
            LOAcquire();
            lVar2 = plVar1[1];
            plVar1[1] = lVar2 + -1;
            LORelease();
            if (lVar2 == 0) {
              (**(code **)(*plVar1 + 0x10))(plVar1);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
            }
          }
        }
        plVar5 = plVar7;
        plVar6 = local_80;
      } while (plVar7 != (long *)0x0);
      while (plVar6 != (long *)0x0) {
        plVar7 = (long *)*plVar6;
        plVar5 = (long *)plVar6[10];
        if (plVar5 != (long *)0x0) {
          LOAcquire();
          lVar2 = plVar5[1];
          plVar5[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*plVar5 + 0x10))(plVar5);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
        __ZdlPvm(plVar6,0x60);
        plVar6 = plVar7;
      }
    }
    FUN_06686680(local_150,*local_148);
  }
  if ((char)local_178 == '\x01') {
    __ZNSt3__115recursive_mutex6unlockEv(local_180);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_70) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


