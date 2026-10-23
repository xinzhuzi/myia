// Ghidra inferred pseudocode; requested=0x319eef8
// entry=0319eef8 end=0319f39b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0319eef8(long param_1,long *param_2)

{
  long *plVar1;
  uint3 uVar2;
  undefined8 *puVar3;
  long lVar4;
  ulong uVar5;
  long lVar6;
  code *pcVar7;
  long *plVar8;
  long *plVar9;
  undefined8 *puVar10;
  long *plVar11;
  long lVar12;
  long lVar13;
  undefined4 uVar14;
  long lVar15;
  long lVar16;
  undefined4 uVar17;
  long lVar18;
  long lVar19;
  long lVar20;
  long lVar21;
  undefined8 *puStack_1a8;
  undefined8 *local_1a0;
  long local_198;
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
  uVar5 = FUN_06686644(*(undefined8 *)(param_1 + 8));
  if ((uVar5 & 1) == 0) {
    uVar5 = FUN_0668dad0(4);
    if ((uVar5 & 1) != 0) {
      if ((DAT_0a3e3209 & 1) == 0) {
        DAT_0a3e3204 = (undefined4)ram0x08782918;
        DAT_0a3e3208 = 0;
        DAT_0a3e3209 = 1;
      }
      if ((DAT_0a3e2ee3 & 1) == 0) {
        DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a3e2ee0 = 0x2928;
        DAT_0a3e2ee2 = 0;
        DAT_0a3e2ee3 = 1;
      }
      if ((DAT_0a3e321d & 1) == 0) {
        DAT_0a3e3210._0_1_ = s_signalslot_h_08782920[0];
        DAT_0a3e3210._1_1_ = s_signalslot_h_08782920[1];
        DAT_0a3e3210._2_1_ = s_signalslot_h_08782920[2];
        DAT_0a3e3210._3_1_ = s_signalslot_h_08782920[3];
        DAT_0a3e3210._4_1_ = s_signalslot_h_08782920[4];
        DAT_0a3e3210._5_1_ = s_signalslot_h_08782920[5];
        DAT_0a3e3210._6_1_ = s_signalslot_h_08782920[6];
        DAT_0a3e3210._7_1_ = s_signalslot_h_08782920[7];
        DAT_0a3e3218 = (undefined4)ram0x08782928;
        DAT_0a3e321c = 0;
        DAT_0a3e321d = 1;
      }
      FUN_0668db5c(&local_150,&DAT_0a3e3204,0xa3e2ed8,&DAT_0a3e3210,0xe500008800);
      if ((DAT_0a3e325f & 1) == 0) {
        uVar5 = 0;
        do {
          uVar14 = *(undefined4 *)((long)&DAT_088c60b7 + uVar5);
          uVar2 = CONCAT12((char)((uint)uVar14 >> 8),(short)uVar14) & 0xff00ff;
          uVar17 = *(undefined4 *)((long)&DAT_088c60a3 + uVar5 % 0x14);
          *(uint *)((long)&DAT_0a3e321e + uVar5) =
               CONCAT13((char)((uint)uVar14 >> 0x18) + 0x69U ^ (byte)((uint)uVar17 >> 0x18),
                        CONCAT12((char)((uint)uVar14 >> 0x10) + 0x69U ^ (byte)((uint)uVar17 >> 0x10)
                                 ,CONCAT11((char)(uVar2 >> 0x10) + 0x69U ^ (byte)((uint)uVar17 >> 8)
                                           ,(char)uVar2 + 0x69U ^ (byte)uVar17)));
          uVar5 = uVar5 + 4;
        } while (uVar5 != 0x40);
        DAT_0a3e325e = 0;
        DAT_0a3e325f = 1;
      }
      plVar8 = local_150 + 0xd;
      if (*(char *)((long)local_150 + 0x7f) < '\0') {
        plVar8 = (long *)*plVar8;
      }
      local_78 = (long **)0xaaaaaaaa00000006;
      local_80 = (long *)&DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_150 + 7,&DAT_0a3e321e,plVar8,&local_80,0);
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
      plVar8 = local_80;
      do {
        plVar11 = (long *)*plVar8;
        plVar9 = (long *)plVar8[8];
        if (plVar9 == (long *)0x0) {
          (*(code *)plVar8[2])(plVar8[1],plVar8 + 3,param_2);
        }
        else {
          lVar13 = plVar8[2];
          lVar12 = plVar8[1];
          lVar16 = plVar8[4];
          lVar15 = plVar8[3];
          lVar19 = plVar8[6];
          lVar18 = plVar8[5];
          lVar21 = plVar8[8];
          lVar20 = plVar8[7];
          lVar4 = plVar8[9];
          plVar1 = (long *)plVar8[10];
          if (plVar1 != (long *)0x0) {
            plVar1[1] = plVar1[1] + 1;
          }
          lVar6 = plVar8[0xb];
          local_1a0 = (undefined8 *)0x0;
          local_198 = 0;
          puStack_1a8 = (undefined8 *)0x0;
          FUN_03214ae4(&puStack_1a8,*param_2,param_2[1],
                       (param_2[1] - *param_2 >> 3) * -0x6474a8819ec8e951);
          local_158 = (long *)0x0;
          local_158 = (long *)__Znwm(0x78);
          *local_158 = (long)&PTR_FUN_09deeda0;
          local_158[2] = lVar13;
          local_158[1] = lVar12;
          local_158[4] = lVar16;
          local_158[3] = lVar15;
          local_158[6] = lVar19;
          local_158[5] = lVar18;
          local_158[8] = lVar21;
          local_158[7] = lVar20;
          local_158[9] = lVar4;
          local_158[10] = (long)plVar1;
          if (plVar1 != (long *)0x0) {
            plVar1[1] = plVar1[1] + 1;
          }
          local_158[0xc] = (long)puStack_1a8;
          local_158[0xb] = lVar6;
          local_158[0xe] = local_198;
          local_158[0xd] = (long)local_1a0;
          local_1a0 = (undefined8 *)0x0;
          local_198 = 0;
          puStack_1a8 = (undefined8 *)0x0;
          (**(code **)(*plVar9 + 0x10))(plVar9,alStack_170);
          if (local_158 == alStack_170) {
            pcVar7 = *(code **)(*local_158 + 0x20);
LAB_0319f0c4:
            (*pcVar7)();
          }
          else if (local_158 != (long *)0x0) {
            pcVar7 = *(code **)(*local_158 + 0x28);
            goto LAB_0319f0c4;
          }
          puVar3 = puStack_1a8;
          puVar10 = local_1a0;
          if (puStack_1a8 != (undefined8 *)0x0) {
            while (puVar10 != puVar3) {
              puVar10 = puVar10 + -0x4f;
              (**(code **)*puVar10)(puVar10);
            }
            local_1a0 = puVar3;
            __ZdlPvm(puStack_1a8,local_198 - (long)puStack_1a8);
          }
          if (plVar1 != (long *)0x0) {
            LOAcquire();
            lVar4 = plVar1[1];
            plVar1[1] = lVar4 + -1;
            LORelease();
            if (lVar4 == 0) {
              (**(code **)(*plVar1 + 0x10))(plVar1);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
            }
          }
        }
        plVar8 = plVar11;
        plVar9 = local_80;
      } while (plVar11 != (long *)0x0);
      while (plVar9 != (long *)0x0) {
        plVar11 = (long *)*plVar9;
        plVar8 = (long *)plVar9[10];
        if (plVar8 != (long *)0x0) {
          LOAcquire();
          lVar4 = plVar8[1];
          plVar8[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*plVar8 + 0x10))(plVar8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
          }
        }
        __ZdlPvm(plVar9,0x60);
        plVar9 = plVar11;
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


