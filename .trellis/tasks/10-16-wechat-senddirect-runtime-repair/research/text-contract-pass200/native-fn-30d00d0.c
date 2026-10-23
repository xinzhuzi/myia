// Ghidra inferred pseudocode; requested=0x30d00d0
// entry=030d00d0 end=030d050b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d00d0(long param_1,undefined8 param_2)

{
  long *plVar1;
  uint3 uVar2;
  long lVar3;
  ulong uVar4;
  long *plVar5;
  long lVar6;
  code *pcVar7;
  long *plVar8;
  long *plVar9;
  long lVar10;
  long lVar11;
  undefined4 uVar12;
  long lVar13;
  long lVar14;
  undefined4 uVar15;
  long lVar16;
  long lVar17;
  long lVar18;
  long lVar19;
  undefined1 auStack_3f8 [632];
  undefined8 local_180;
  undefined8 local_178;
  undefined1 *local_170;
  long alStack_168 [3];
  long *local_150;
  undefined8 *local_148;
  undefined8 *local_140;
  undefined1 *local_138;
  long *local_78;
  long **local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  local_178 = FUN_00e39f68(*(undefined8 *)(param_1 + 8));
  local_170 = (undefined1 *)CONCAT71(local_170._1_7_,1);
  __ZNSt3__115recursive_mutex4lockEv();
  uVar4 = FUN_06686644(*(undefined8 *)(param_1 + 8));
  if ((uVar4 & 1) == 0) {
    uVar4 = FUN_0668dad0(4);
    if ((uVar4 & 1) != 0) {
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
      FUN_0668db5c(&local_148,&DAT_0a3d94f8,&DAT_0a3d94a8,&DAT_0a3d9500,0xe500008800);
      if ((DAT_0a3d954f & 1) == 0) {
        uVar4 = 0;
        do {
          uVar12 = *(undefined4 *)((long)&DAT_088afe70 + uVar4);
          uVar2 = CONCAT12((char)((uint)uVar12 >> 8),(short)uVar12) & 0xff00ff;
          uVar15 = *(undefined4 *)((long)&DAT_088afe5c + uVar4 % 0x14);
          *(uint *)((long)&DAT_0a3d950e + uVar4) =
               CONCAT13((char)((uint)uVar12 >> 0x18) + 0x8aU ^ (byte)((uint)uVar15 >> 0x18),
                        CONCAT12((char)((uint)uVar12 >> 0x10) + 0x8aU ^ (byte)((uint)uVar15 >> 0x10)
                                 ,CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar15 >> 8)
                                           ,(char)uVar2 + 0x8aU ^ (byte)uVar15)));
          uVar4 = uVar4 + 4;
        } while (uVar4 != 0x40);
        DAT_0a3d954e = 0;
        DAT_0a3d954f = 1;
      }
      plVar5 = local_148 + 0xd;
      if (*(char *)((long)local_148 + 0x7f) < '\0') {
        plVar5 = (long *)*plVar5;
      }
      local_70 = (long **)0xaaaaaaaa00000006;
      local_78 = (long *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_148 + 7,&DAT_0a3d950e,plVar5,&local_78,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(&local_148);
    }
  }
  else {
    local_180 = *(undefined8 *)(param_1 + 8);
    local_138 = &SUB_aaaaaaaaaaaaaaaa;
    local_148 = &local_178;
    local_140 = &local_180;
    local_70 = &local_78;
    local_78 = (long *)0x0;
    FUN_0668688c(param_1,&local_78);
    if (local_78 != (long *)0x0) {
      plVar5 = local_78;
      do {
        plVar9 = (long *)*plVar5;
        plVar8 = (long *)plVar5[8];
        if (plVar8 == (long *)0x0) {
          (*(code *)plVar5[2])(plVar5[1],plVar5 + 3,param_2);
        }
        else {
          lVar11 = plVar5[2];
          lVar10 = plVar5[1];
          lVar14 = plVar5[4];
          lVar13 = plVar5[3];
          lVar17 = plVar5[6];
          lVar16 = plVar5[5];
          lVar19 = plVar5[8];
          lVar18 = plVar5[7];
          lVar3 = plVar5[9];
          plVar1 = (long *)plVar5[10];
          if (plVar1 != (long *)0x0) {
            plVar1[1] = plVar1[1] + 1;
          }
          lVar6 = plVar5[0xb];
          FUN_00f57630(auStack_3f8,param_2);
          local_150 = (long *)0x0;
          plVar5 = (long *)__Znwm(0x2d8);
          *plVar5 = (long)&PTR_FUN_09de88a0;
          plVar5[2] = lVar11;
          plVar5[1] = lVar10;
          plVar5[4] = lVar14;
          plVar5[3] = lVar13;
          plVar5[6] = lVar17;
          plVar5[5] = lVar16;
          plVar5[8] = lVar19;
          plVar5[7] = lVar18;
          plVar5[9] = lVar3;
          plVar5[10] = (long)plVar1;
          if (plVar1 != (long *)0x0) {
            plVar1[1] = plVar1[1] + 1;
          }
          plVar5[0xb] = lVar6;
          FUN_02a0cf30(plVar5 + 0xc,auStack_3f8);
          local_150 = plVar5;
          (**(code **)(*plVar8 + 0x10))(plVar8,alStack_168);
          if (local_150 == alStack_168) {
            pcVar7 = *(code **)(*local_150 + 0x20);
LAB_030d0280:
            (*pcVar7)();
          }
          else if (local_150 != (long *)0x0) {
            pcVar7 = *(code **)(*local_150 + 0x28);
            goto LAB_030d0280;
          }
          FUN_00ac6290(auStack_3f8);
          if (plVar1 != (long *)0x0) {
            LOAcquire();
            lVar3 = plVar1[1];
            plVar1[1] = lVar3 + -1;
            LORelease();
            if (lVar3 == 0) {
              (**(code **)(*plVar1 + 0x10))(plVar1);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
            }
          }
        }
        plVar5 = plVar9;
        plVar8 = local_78;
      } while (plVar9 != (long *)0x0);
      while (plVar8 != (long *)0x0) {
        plVar9 = (long *)*plVar8;
        plVar5 = (long *)plVar8[10];
        if (plVar5 != (long *)0x0) {
          LOAcquire();
          lVar3 = plVar5[1];
          plVar5[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*plVar5 + 0x10))(plVar5);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
        __ZdlPvm(plVar8,0x60);
        plVar8 = plVar9;
      }
    }
    FUN_06686680(local_148,*local_140);
  }
  if ((char)local_170 == '\x01') {
    __ZNSt3__115recursive_mutex6unlockEv(local_178);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


