// Ghidra inferred pseudocode; requested=0x667a760
// entry=0667a760 end=0667ac03

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0667a760(long param_1,long param_2,long *param_3,undefined4 param_4)

{
  uint3 uVar1;
  long lVar2;
  ulong uVar3;
  code *pcVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined4 local_21c;
  long local_218;
  long local_210;
  long lStack_208;
  long lStack_200;
  long lStack_1f8;
  long local_1f0;
  long lStack_1e8;
  long lStack_1e0;
  long lStack_1d8;
  long local_1d0;
  long *local_1c8;
  long local_1c0;
  long lStack_1b8;
  long local_1b0;
  long lStack_1a8;
  ulong local_1a0;
  undefined4 local_198;
  undefined8 local_190;
  undefined8 local_188;
  undefined1 *local_180;
  long alStack_178 [3];
  long *local_160;
  undefined8 *local_158;
  undefined8 *local_150;
  undefined1 *puStack_148;
  long *local_88;
  long **local_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_180 = &SUB_aaaaaaaaaaaaaaaa;
  local_188 = FUN_00e39f68(*(undefined8 *)(param_1 + 8));
  local_180 = (undefined1 *)CONCAT71(local_180._1_7_,1);
  __ZNSt3__115recursive_mutex4lockEv();
  uVar3 = FUN_06686644(*(undefined8 *)(param_1 + 8));
  if ((uVar3 & 1) == 0) {
    uVar3 = FUN_0668dad0(4);
    if ((uVar3 & 1) != 0) {
      if ((DAT_0a517add & 1) == 0) {
        DAT_0a517ad8 = (undefined4)ram0x08782918;
        DAT_0a517adc = 0;
        DAT_0a517add = 1;
      }
      if ((DAT_0a517c53 & 1) == 0) {
        DAT_0a517c48._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a517c48._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a517c48._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a517c48._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a517c48._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a517c48._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a517c48._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a517c48._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a517c50 = 0x2928;
        DAT_0a517c52 = 0;
        DAT_0a517c53 = 1;
      }
      if ((DAT_0a517c65 & 1) == 0) {
        DAT_0a517c58._0_1_ = s_signalslot_h_08782920[0];
        DAT_0a517c58._1_1_ = s_signalslot_h_08782920[1];
        DAT_0a517c58._2_1_ = s_signalslot_h_08782920[2];
        DAT_0a517c58._3_1_ = s_signalslot_h_08782920[3];
        DAT_0a517c58._4_1_ = s_signalslot_h_08782920[4];
        DAT_0a517c58._5_1_ = s_signalslot_h_08782920[5];
        DAT_0a517c58._6_1_ = s_signalslot_h_08782920[6];
        DAT_0a517c58._7_1_ = s_signalslot_h_08782920[7];
        DAT_0a517c60 = (undefined4)ram0x08782928;
        DAT_0a517c64 = 0;
        DAT_0a517c65 = 1;
      }
      FUN_0668db5c(&local_158,&DAT_0a517ad8,&DAT_0a517c48,&DAT_0a517c58,0xe500008800);
      if ((DAT_0a517ca7 & 1) == 0) {
        uVar3 = 0;
        do {
          uVar8 = *(undefined4 *)((long)&DAT_096852a1 + uVar3);
          uVar1 = CONCAT12((char)((uint)uVar8 >> 8),(short)uVar8) & 0xff00ff;
          uVar9 = *(undefined4 *)((long)&DAT_0968528d + uVar3 % 0x14);
          *(uint *)((long)&DAT_0a517c66 + uVar3) =
               CONCAT13((char)((uint)uVar8 >> 0x18) + 0x8aU ^ (byte)((uint)uVar9 >> 0x18),
                        CONCAT12((char)((uint)uVar8 >> 0x10) + 0x8aU ^ (byte)((uint)uVar9 >> 0x10),
                                 CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar9 >> 8),
                                          (char)uVar1 + 0x8aU ^ (byte)uVar9)));
          uVar3 = uVar3 + 4;
        } while (uVar3 != 0x40);
        DAT_0a517ca6 = 0;
        DAT_0a517ca7 = 1;
      }
      plVar5 = local_158 + 0xd;
      if (*(char *)((long)local_158 + 0x7f) < '\0') {
        plVar5 = (long *)*plVar5;
      }
      local_80 = (long **)0xaaaaaaaa00000006;
      local_88 = (long *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_158 + 7,&DAT_0a517c66,plVar5,&local_88,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(&local_158);
    }
  }
  else {
    local_190 = *(undefined8 *)(param_1 + 8);
    puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
    local_158 = &local_188;
    local_80 = &local_88;
    local_88 = (long *)0x0;
    local_150 = &local_190;
    FUN_0668688c(param_1,&local_88);
    if (local_88 != (long *)0x0) {
      plVar5 = local_88;
      do {
        plVar7 = (long *)*plVar5;
        plVar6 = (long *)plVar5[8];
        if (plVar6 == (long *)0x0) {
          local_21c = param_4;
          local_218 = param_2;
          (*(code *)plVar5[2])(plVar5[1],plVar5 + 3,&local_218,param_3,&local_21c);
        }
        else {
          lStack_208 = plVar5[2];
          local_210 = plVar5[1];
          lStack_1f8 = plVar5[4];
          lStack_200 = plVar5[3];
          lStack_1e8 = plVar5[6];
          local_1f0 = plVar5[5];
          lStack_1d8 = plVar5[8];
          lStack_1e0 = plVar5[7];
          local_1d0 = plVar5[9];
          local_1c8 = (long *)plVar5[10];
          if (local_1c8 != (long *)0x0) {
            local_1c8[1] = local_1c8[1] + 1;
          }
          local_1c0 = plVar5[0xb];
          lStack_1b8 = param_2;
          if (*(char *)((long)param_3 + 0x17) < '\0') {
            FUN_00018d20(&local_1b0,*param_3,param_3[1]);
          }
          else {
            lStack_1a8 = param_3[1];
            local_1b0 = *param_3;
            local_1a0 = param_3[2];
          }
          local_160 = (long *)0x0;
          local_198 = param_4;
          local_160 = (long *)__Znwm(0x88);
          *local_160 = (long)&PTR_FUN_09fb2770;
          local_160[2] = lStack_208;
          local_160[1] = local_210;
          local_160[4] = lStack_1f8;
          local_160[3] = lStack_200;
          local_160[6] = lStack_1e8;
          local_160[5] = local_1f0;
          local_160[8] = lStack_1d8;
          local_160[7] = lStack_1e0;
          local_160[9] = local_1d0;
          local_160[10] = (long)local_1c8;
          uVar8 = param_4;
          if (local_1c8 != (long *)0x0) {
            local_1c8[1] = local_1c8[1] + 1;
            uVar8 = local_198;
          }
          local_160[0xb] = local_1c0;
          local_160[0xc] = lStack_1b8;
          local_160[0xe] = lStack_1a8;
          local_160[0xd] = local_1b0;
          local_160[0xf] = local_1a0;
          lStack_1a8 = 0;
          local_1a0 = 0;
          local_1b0 = 0;
          *(undefined4 *)(local_160 + 0x10) = uVar8;
          (**(code **)(*plVar6 + 0x10))(plVar6,alStack_178);
          if (local_160 == alStack_178) {
            pcVar4 = *(code **)(*local_160 + 0x20);
LAB_0667a954:
            (*pcVar4)();
          }
          else if (local_160 != (long *)0x0) {
            pcVar4 = *(code **)(*local_160 + 0x28);
            goto LAB_0667a954;
          }
          plVar5 = local_1c8;
          if ((long)local_1a0 < 0) {
            __ZdlPvm(local_1b0,local_1a0 & 0x7fffffffffffffff);
            plVar5 = local_1c8;
          }
          local_1c8 = plVar5;
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
        }
        plVar5 = plVar7;
        plVar6 = local_88;
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
    FUN_06686680(local_158,*local_150);
  }
  if ((char)local_180 == '\x01') {
    __ZNSt3__115recursive_mutex6unlockEv(local_188);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


