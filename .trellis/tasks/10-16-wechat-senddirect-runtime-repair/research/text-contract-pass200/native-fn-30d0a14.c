// Ghidra inferred pseudocode; requested=0x30d0a14
// entry=030d0a14 end=030d0e5b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d0a14(long param_1,long param_2,undefined8 param_3)

{
  uint3 uVar1;
  long lVar2;
  ulong uVar3;
  long *plVar4;
  code *pcVar5;
  long *plVar6;
  long *plVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  long local_468;
  long local_460;
  long lStack_458;
  long lStack_450;
  long lStack_448;
  long local_440;
  long lStack_438;
  long lStack_430;
  long lStack_428;
  long local_420;
  long *local_418;
  long local_410;
  long lStack_408;
  undefined1 auStack_400 [632];
  undefined8 local_188;
  undefined8 local_180;
  undefined1 *local_178;
  long alStack_170 [3];
  long *local_158;
  undefined8 *local_150;
  undefined8 *local_148;
  undefined1 *local_140;
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
      if ((DAT_0a3d94fd & 1) == 0) {
        DAT_0a3d94f8 = (undefined4)ram0x08782918;
        DAT_0a3d94fc = 0;
        DAT_0a3d94fd = 1;
      }
      if ((DAT_0a3d94b3 & 1) == 0) {
        DAT_0a3d94a8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a3d94a8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a3d94a8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a3d94a8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a3d94a8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a3d94a8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a3d94a8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a3d94a8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a3d94b0 = 0x2928;
        DAT_0a3d94b2 = 0;
        DAT_0a3d94b3 = 1;
      }
      if ((DAT_0a3d950d & 1) == 0) {
        DAT_0a3d9500._0_1_ = s_signalslot_h_08782920[0];
        DAT_0a3d9500._1_1_ = s_signalslot_h_08782920[1];
        DAT_0a3d9500._2_1_ = s_signalslot_h_08782920[2];
        DAT_0a3d9500._3_1_ = s_signalslot_h_08782920[3];
        DAT_0a3d9500._4_1_ = s_signalslot_h_08782920[4];
        DAT_0a3d9500._5_1_ = s_signalslot_h_08782920[5];
        DAT_0a3d9500._6_1_ = s_signalslot_h_08782920[6];
        DAT_0a3d9500._7_1_ = s_signalslot_h_08782920[7];
        DAT_0a3d9508 = (undefined4)ram0x08782928;
        DAT_0a3d950c = 0;
        DAT_0a3d950d = 1;
      }
      FUN_0668db5c(&local_150,&DAT_0a3d94f8,&DAT_0a3d94a8,&DAT_0a3d9500,0xe500008800);
      if ((DAT_0a3d954f & 1) == 0) {
        uVar3 = 0;
        do {
          uVar8 = *(undefined4 *)((long)&DAT_088afe70 + uVar3);
          uVar1 = CONCAT12((char)((uint)uVar8 >> 8),(short)uVar8) & 0xff00ff;
          uVar9 = *(undefined4 *)((long)&DAT_088afe5c + uVar3 % 0x14);
          *(uint *)((long)&DAT_0a3d950e + uVar3) =
               CONCAT13((char)((uint)uVar8 >> 0x18) + 0x8aU ^ (byte)((uint)uVar9 >> 0x18),
                        CONCAT12((char)((uint)uVar8 >> 0x10) + 0x8aU ^ (byte)((uint)uVar9 >> 0x10),
                                 CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar9 >> 8),
                                          (char)uVar1 + 0x8aU ^ (byte)uVar9)));
          uVar3 = uVar3 + 4;
        } while (uVar3 != 0x40);
        DAT_0a3d954e = 0;
        DAT_0a3d954f = 1;
      }
      plVar4 = local_150 + 0xd;
      if (*(char *)((long)local_150 + 0x7f) < '\0') {
        plVar4 = (long *)*plVar4;
      }
      local_78 = (long **)0xaaaaaaaa00000006;
      local_80 = (long *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_150 + 7,&DAT_0a3d950e,plVar4,&local_80,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(&local_150);
    }
  }
  else {
    local_188 = *(undefined8 *)(param_1 + 8);
    local_140 = &SUB_aaaaaaaaaaaaaaaa;
    local_150 = &local_180;
    local_148 = &local_188;
    local_78 = &local_80;
    local_80 = (long *)0x0;
    FUN_0668688c(param_1,&local_80);
    if (local_80 != (long *)0x0) {
      plVar4 = local_80;
      do {
        plVar7 = (long *)*plVar4;
        plVar6 = (long *)plVar4[8];
        if (plVar6 == (long *)0x0) {
          local_468 = param_2;
          (*(code *)plVar4[2])(plVar4[1],plVar4 + 3,&local_468,param_3);
        }
        else {
          lStack_458 = plVar4[2];
          local_460 = plVar4[1];
          lStack_448 = plVar4[4];
          lStack_450 = plVar4[3];
          lStack_438 = plVar4[6];
          local_440 = plVar4[5];
          lStack_428 = plVar4[8];
          lStack_430 = plVar4[7];
          local_420 = plVar4[9];
          local_418 = (long *)plVar4[10];
          if (local_418 != (long *)0x0) {
            local_418[1] = local_418[1] + 1;
          }
          local_410 = plVar4[0xb];
          lStack_408 = param_2;
          FUN_00f57630(auStack_400,param_3);
          local_158 = (long *)0x0;
          plVar4 = (long *)__Znwm(0x2e0);
          *plVar4 = (long)&PTR_FUN_09de8920;
          plVar4[2] = lStack_458;
          plVar4[1] = local_460;
          plVar4[4] = lStack_448;
          plVar4[3] = lStack_450;
          plVar4[6] = lStack_438;
          plVar4[5] = local_440;
          plVar4[8] = lStack_428;
          plVar4[7] = lStack_430;
          plVar4[9] = local_420;
          plVar4[10] = (long)local_418;
          if (local_418 != (long *)0x0) {
            local_418[1] = local_418[1] + 1;
          }
          plVar4[0xb] = local_410;
          plVar4[0xc] = lStack_408;
          FUN_02a0cf30(plVar4 + 0xd,auStack_400);
          local_158 = plVar4;
          (**(code **)(*plVar6 + 0x10))(plVar6,alStack_170);
          if (local_158 == alStack_170) {
            pcVar5 = *(code **)(*local_158 + 0x20);
LAB_030d0bd0:
            (*pcVar5)();
          }
          else if (local_158 != (long *)0x0) {
            pcVar5 = *(code **)(*local_158 + 0x28);
            goto LAB_030d0bd0;
          }
          FUN_00ac6290(auStack_400);
          plVar4 = local_418;
          if (local_418 != (long *)0x0) {
            LOAcquire();
            lVar2 = local_418[1];
            local_418[1] = lVar2 + -1;
            LORelease();
            if (lVar2 == 0) {
              (**(code **)(*local_418 + 0x10))(local_418);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
            }
          }
        }
        plVar4 = plVar7;
        plVar6 = local_80;
      } while (plVar7 != (long *)0x0);
      while (plVar6 != (long *)0x0) {
        plVar7 = (long *)*plVar6;
        plVar4 = (long *)plVar6[10];
        if (plVar4 != (long *)0x0) {
          LOAcquire();
          lVar2 = plVar4[1];
          plVar4[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*plVar4 + 0x10))(plVar4);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
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


