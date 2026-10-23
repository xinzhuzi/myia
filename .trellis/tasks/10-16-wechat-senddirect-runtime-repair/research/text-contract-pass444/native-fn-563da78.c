// Ghidra inferred pseudocode; requested=0x563da78
// entry=0563da78 end=0563e19b

void FUN_0563da78(undefined8 param_1,long *param_2,undefined8 param_3,undefined8 param_4,int param_5
                 )

{
  segment_command *psVar1;
  uint uVar2;
  undefined1 *puVar3;
  segment_command *psVar4;
  long lVar5;
  ulong uVar6;
  long *plVar7;
  undefined8 *puVar8;
  undefined8 uVar9;
  uint uVar10;
  long *plVar11;
  long *plVar12;
  long *plVar13;
  undefined1 *local_120;
  segment_command *psStack_118;
  undefined1 *local_110;
  undefined1 *puStack_108;
  undefined1 *puStack_100;
  undefined1 *local_f8;
  undefined1 *local_f0;
  undefined1 *local_e8 [3];
  undefined1 *local_d0;
  segment_command *apsStack_c8 [2];
  undefined1 **local_b8;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar5 = FUN_0563e2b0(param_2 + 0x7f);
  uVar10 = (uint)param_3;
  uVar2 = uVar10 >> 8 & 0xff;
  if (8 < uVar2) {
    if ((DAT_0a4d659a & 1) == 0) {
      DAT_0a4d6590._0_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[8];
      DAT_0a4d6590._1_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[9];
      DAT_0a4d6590._2_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[10];
      DAT_0a4d6590._3_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[0xb];
      DAT_0a4d6590._4_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[0xc];
      DAT_0a4d6590._5_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[0xd];
      DAT_0a4d6590._6_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[0xe];
      DAT_0a4d6590._7_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[0xf];
      DAT_0a4d6598 = 0x74;
      DAT_0a4d659a = 1;
    }
                    /* WARNING: Subroutine does not return */
    FUN_0020ee1c(&DAT_0a4d6590);
  }
  plVar11 = (long *)(lVar5 + (ulong)uVar2 * 0x18);
  if (*plVar11 != 0) {
    *(int *)(plVar11 + 2) = (int)plVar11[2] + 1;
    local_b8 = (undefined1 **)__Znwm(0x28);
    *local_b8 = (undefined1 *)&PTR_FUN_09f182c0;
    local_b8[1] = FUN_0563e384;
    local_b8[2] = (undefined1 *)0x0;
    local_b8[3] = (undefined1 *)param_2;
    *(uint *)(local_b8 + 4) = uVar10;
    FUN_05646510(param_1,plVar11,&local_d0);
    if (local_b8 == &local_d0) {
      (**(code **)(*local_b8 + 0x20))();
    }
    else if (local_b8 != (undefined1 **)0x0) {
      (**(code **)(*local_b8 + 0x28))();
    }
    goto LAB_0563e124;
  }
  if (param_5 != 0) {
    local_d0 = (undefined1 *)0x0;
    FUN_056463e4(param_1,&local_d0);
    goto LAB_0563e124;
  }
  uVar6 = FUN_0563cb5c(param_2 + 100,param_3,param_4);
  if ((uVar6 & 1) == 0) {
    local_f0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
    local_110 = &SUB_aaaaaaaaaaaaaaaa;
    local_f8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_100 = &SUB_aaaaaaaaaaaaaaaa;
    psStack_118 = (segment_command *)&SUB_aaaaaaaaaaaaaaaa;
    local_120 = &SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4d655b & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a4d651e)[uVar6] = (&DAT_08b2cf48)[uVar6 & 0xf] ^ (&DAT_08b2cf58)[uVar6];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x3d);
      DAT_0a4d655b = 1;
    }
    FUN_0562fcc8(&local_d0,&DAT_0a4d651e);
    FUN_05632e9c(&local_120,0x12,5,&local_d0);
    FUN_0562fd84(&local_d0);
    if ((DAT_0a4d656b & 1) == 0) {
      DAT_0a4d6560._0_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[0];
      DAT_0a4d6560._1_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[1];
      DAT_0a4d6560._2_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[2];
      DAT_0a4d6560._3_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[3];
      DAT_0a4d6560._4_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[4];
      DAT_0a4d6560._5_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[5];
      DAT_0a4d6560._6_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[6];
      DAT_0a4d6560._7_1_ = s_MaxAllowarray__a_90e63183_08b2ce70[7];
      DAT_0a4d6568 = 0x6465;
      DAT_0a4d656a = 0;
      DAT_0a4d656b = 1;
    }
    FUN_0562fcc8(local_e8,&DAT_0a4d6560);
    local_d0._0_1_ = 1;
    apsStack_c8[0] = &segment_command_00000020;
    FUN_05626090(&puStack_100,local_e8,&local_d0);
    FUN_056caefc(&local_d0);
    FUN_0562fd84(local_e8);
    local_d0 = (undefined1 *)CONCAT71(local_d0._1_7_,3);
    FUN_056c9128(local_e8,param_2 + 9);
    FUN_056309f0(apsStack_c8,local_e8);
    FUN_0562fd84(local_e8);
    FUN_05626090(&puStack_100,&DAT_0a524300,&local_d0);
    FUN_056caefc(&local_d0);
    uVar9 = FUN_0562c050();
    FUN_0562c85c(uVar9,&local_120);
    FUN_05627b10(param_2,&local_120);
    local_d0 = (undefined1 *)0x0;
    FUN_056463e4(param_1,&local_d0);
    FUN_03b35c00(&puStack_100,local_f8);
    FUN_0562fd84((ulong)&local_120 | 8);
    goto LAB_0563e124;
  }
  local_e8[0] = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0562b77c(local_e8,param_2 + 0xc);
  local_120 = (undefined1 *)0x0;
  psStack_118 = (segment_command *)0x0;
  local_d0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0562b720(&local_d0,param_2 + 0x29);
  psVar4 = psStack_118;
  uVar2 = uVar10 & 0xff;
  if (param_2[(ulong)uVar2 * 3 + 0x57] != 0) {
    lVar5 = param_2[(ulong)uVar2 * 3 + 0x55];
    local_120 = *(undefined1 **)(lVar5 + 0x10);
    psVar1 = *(segment_command **)(lVar5 + 0x18);
    if (psVar1 != (segment_command *)0x0) {
      *(long *)psVar1->segname = *(long *)psVar1->segname + 1;
    }
    if (psStack_118 != (segment_command *)0x0) {
      LOAcquire();
      lVar5 = *(long *)psStack_118->segname;
      *(long *)psStack_118->segname = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        lVar5 = *(long *)psStack_118;
        psStack_118 = psVar1;
        (**(code **)(lVar5 + 0x10))(psVar4);
        __ZNSt3__119__shared_weak_count14__release_weakEv(psVar4);
        psVar1 = psStack_118;
      }
    }
    psStack_118 = psVar1;
    plVar7 = (long *)param_2[(ulong)uVar2 * 3 + 0x55];
    lVar5 = *plVar7;
    plVar12 = (long *)plVar7[1];
    *(long **)(lVar5 + 8) = plVar12;
    *plVar12 = lVar5;
    param_2[(ulong)uVar2 * 3 + 0x57] = param_2[(ulong)uVar2 * 3 + 0x57] + -1;
    plVar12 = (long *)plVar7[3];
    if (plVar12 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar12[1];
      plVar12[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar12 + 0x10))(plVar12);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
      }
    }
    __ZdlPvm(plVar7,0x20);
  }
  FUN_0562b74c(&local_d0);
  if (local_120 == (undefined1 *)0x0) {
    (**(code **)(*param_2 + 0x18))(&local_d0,param_2,param_3);
    psVar1 = apsStack_c8[0];
    local_120 = local_d0;
    psVar4 = psStack_118;
    local_d0 = (undefined1 *)0x0;
    apsStack_c8[0] = (segment_command *)0x0;
    psStack_118 = psVar1;
    if (psVar4 != (segment_command *)0x0) {
      LOAcquire();
      lVar5 = *(long *)psVar4->segname;
      *(long *)psVar4->segname = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*(long *)psVar4 + 0x10))(psVar4);
        __ZNSt3__119__shared_weak_count14__release_weakEv(psVar4);
      }
    }
    psVar4 = apsStack_c8[0];
    if (apsStack_c8[0] != (segment_command *)0x0) {
      LOAcquire();
      lVar5 = *(long *)apsStack_c8[0]->segname;
      *(long *)apsStack_c8[0]->segname = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*(long *)apsStack_c8[0] + 0x10))(apsStack_c8[0]);
        __ZNSt3__119__shared_weak_count14__release_weakEv(psVar4);
      }
    }
    if (local_120 != (undefined1 *)0x0) {
      local_d0 = &SUB_aaaaaaaaaaaaaaaa;
      FUN_0562b720(&local_d0,param_2 + 0x29);
      puVar3 = local_120;
      plVar12 = (long *)param_2[(ulong)uVar2 * 3 + 0x47];
      if ((long *)param_2[(ulong)uVar2 * 3 + 0x47] == (long *)0x0) {
        plVar7 = param_2 + (ulong)uVar2 * 3 + 0x47;
        plVar13 = plVar7;
      }
      else {
        do {
          while (plVar7 = plVar12, (undefined1 *)plVar7[4] <= local_120) {
            if (local_120 <= (undefined1 *)plVar7[4]) goto LAB_0563dfcc;
            plVar12 = (long *)plVar7[1];
            if ((long *)plVar7[1] == (long *)0x0) {
              plVar13 = plVar7 + 1;
              goto LAB_0563df70;
            }
          }
          plVar12 = (long *)*plVar7;
          plVar13 = plVar7;
        } while ((long *)*plVar7 != (long *)0x0);
      }
LAB_0563df70:
      puVar8 = (undefined8 *)__Znwm(0x30);
      puVar8[4] = puVar3;
      puVar8[5] = psStack_118;
      if (psStack_118 != (segment_command *)0x0) {
        *(long *)psStack_118->segname = *(long *)psStack_118->segname + 1;
      }
      *puVar8 = 0;
      puVar8[1] = 0;
      puVar8[2] = plVar7;
      *plVar13 = (long)puVar8;
      lVar5 = *(long *)param_2[(ulong)uVar2 * 3 + 0x46];
      if (lVar5 != 0) {
        param_2[(ulong)uVar2 * 3 + 0x46] = lVar5;
        puVar8 = (undefined8 *)*plVar13;
      }
      FUN_0002413c(param_2[(ulong)uVar2 * 3 + 0x47],puVar8);
      param_2[(ulong)uVar2 * 3 + 0x48] = param_2[(ulong)uVar2 * 3 + 0x48] + 1;
LAB_0563dfcc:
      uVar6 = FUN_0563d4b8(param_2);
      if (0x20 < uVar6) {
        FUN_0563d7d0(param_2);
      }
      FUN_0562b74c(&local_d0);
      goto LAB_0563dfec;
    }
    FUN_0563cd90(param_2 + 100,param_4);
    local_d0 = (undefined1 *)0x0;
    FUN_056463e4(param_1,&local_d0);
  }
  else {
    uVar6 = (**(code **)(*param_2 + 0x20))(param_2,param_3);
    if ((uVar6 & 1) == 0) {
      FUN_05645da4(local_120);
      local_d0 = &SUB_aaaaaaaaaaaaaaaa;
      FUN_0562b720(&local_d0,param_2 + 0x29);
      FUN_00da458c(param_2 + (ulong)uVar2 * 3 + 0x46,&local_120);
      FUN_0562b74c(&local_d0);
      FUN_0563cd90(param_2 + 100,param_4);
      local_d0 = (undefined1 *)0x0;
      FUN_056463e4(param_1,&local_d0);
    }
    else {
LAB_0563dfec:
      FUN_056459b4(local_120,param_4);
      puVar3 = local_120;
      uVar9 = FUN_05631510();
      FUN_0117f910(puVar3,uVar9);
      FUN_0562aeec(param_2 + 0xc);
      if (psStack_118 != (segment_command *)0x0) {
        *(long *)psStack_118->segname = *(long *)psStack_118->segname + 1;
      }
      plVar12 = (long *)plVar11[1];
      *plVar11 = (long)local_120;
      plVar11[1] = (long)psStack_118;
      if (plVar12 != (long *)0x0) {
        LOAcquire();
        lVar5 = plVar12[1];
        plVar12[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*plVar12 + 0x10))(plVar12);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
        }
      }
      *(undefined4 *)(plVar11 + 2) = 1;
      local_b8 = (undefined1 **)__Znwm(0x28);
      *local_b8 = (undefined1 *)&PTR_FUN_09f182c0;
      local_b8[1] = FUN_0563e384;
      local_b8[2] = (undefined1 *)0x0;
      local_b8[3] = (undefined1 *)param_2;
      *(uint *)(local_b8 + 4) = uVar10;
      FUN_05646510(param_1,&local_120,&local_d0);
      if (local_b8 == &local_d0) {
        (**(code **)(*local_b8 + 0x20))();
      }
      else if (local_b8 != (undefined1 **)0x0) {
        (**(code **)(*local_b8 + 0x28))();
      }
    }
  }
  psVar4 = psStack_118;
  if (psStack_118 != (segment_command *)0x0) {
    LOAcquire();
    lVar5 = *(long *)psStack_118->segname;
    *(long *)psStack_118->segname = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*(long *)psStack_118 + 0x10))(psStack_118);
      __ZNSt3__119__shared_weak_count14__release_weakEv(psVar4);
    }
  }
  FUN_0562b7a8(local_e8);
LAB_0563e124:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


