// Ghidra inferred pseudocode; requested=0x318d680
// entry=0318d680 end=0318dca7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0318d680(long *param_1,undefined8 param_2,long *param_3)

{
  undefined1 **ppuVar1;
  undefined8 ******ppppppuVar2;
  undefined1 uVar3;
  undefined4 uVar4;
  uint3 uVar5;
  long *plVar6;
  bool bVar7;
  long lVar8;
  uint uVar9;
  uint uVar10;
  int iVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  ulong uVar14;
  undefined1 *puVar15;
  long lVar16;
  undefined4 uVar17;
  undefined1 *local_230 [2];
  undefined7 local_220;
  char cStack_219;
  uint local_218;
  uint local_214;
  undefined1 auStack_210 [144];
  long *local_180;
  long *local_178;
  undefined1 *local_170;
  undefined1 local_168 [72];
  undefined8 *****local_120;
  undefined8 local_118;
  undefined7 local_110;
  char cStack_109;
  undefined8 *****local_d0;
  undefined1 **ppuStack_c8;
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
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_180 = *(long **)(*param_3 + 8);
  if (local_180 == (long *)0x0) {
    local_180 = (long *)0x0;
    local_178 = (long *)0x0;
    iVar11 = thunk_FUN_05e1d97c(4);
    if (iVar11 != 0) {
      FUN_0488143c(&local_120);
      ppppppuVar2 = (undefined8 ******)local_120;
      if (-1 < cStack_109) {
        ppppppuVar2 = &local_120;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3de31b & 1) == 0) {
        DAT_0a3de310._0_1_ = s_GetHandlonTh_08854480[0];
        DAT_0a3de310._1_1_ = s_GetHandlonTh_08854480[1];
        DAT_0a3de310._2_1_ = s_GetHandlonTh_08854480[2];
        DAT_0a3de310._3_1_ = s_GetHandlonTh_08854480[3];
        DAT_0a3de310._4_1_ = s_GetHandlonTh_08854480[4];
        DAT_0a3de310._5_1_ = s_GetHandlonTh_08854480[5];
        DAT_0a3de310._6_1_ = s_GetHandlonTh_08854480[6];
        DAT_0a3de310._7_1_ = s_GetHandlonTh_08854480[7];
        DAT_0a3de318 = 0x7265;
        DAT_0a3de31a = 0;
        DAT_0a3de31b = 1;
      }
      FUN_05e1d050(auStack_210,4,ppppppuVar2,&DAT_0a3dd350,&DAT_0a3de310,
                   "rameworks/AppKit.framework/Versions/C/AppKit",0,0);
      if ((DAT_0a3e0750 & 1) == 0) {
        _DAT_0a3e0734 = CONCAT44((int)DAT_08557bc8,(int)DAT_08480908);
        uRam000000000a3e073c = CONCAT44((int)ram0x08491928,(int)DAT_085e8930);
        DAT_0a3e0744 = CONCAT44((int)DAT_08486088,(int)DAT_084cadd8);
        DAT_0a3e074c = (undefined4)DAT_084eadc8;
        DAT_0a3e0750 = 1;
      }
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      local_60 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      ppuStack_c8 = (undefined1 **)0x0;
      local_d0 = (undefined8 ******)0x0;
      uStack_b8 = 0;
      local_c0 = 0;
      FUN_05e1d31c(auStack_210,&DAT_0a3e0734,&local_d0);
      thunk_FUN_05e1d0bc(auStack_210);
      if (cStack_109 < '\0') {
        __ZdlPvm(local_120,CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    local_178 = *(long **)(*param_3 + 0x10);
    if (local_178 != (long *)0x0) {
      local_178[1] = local_178[1] + 1;
    }
    uVar9 = (**(code **)(*local_180 + 0x10))();
    plVar6 = local_180;
    local_214 = uVar9;
    uVar10 = (**(code **)(*local_180 + 0x18))(local_180);
    local_218 = uVar10;
    iVar11 = (**(code **)(*plVar6 + 0x20))(plVar6);
    if ((uVar9 == 0x31 && iVar11 == 2) &&
       ((uVar10 - 0x35 < 0x23 && (1L << ((ulong)(uVar10 - 0x35) & 0x3f) & 0x400000011U) != 0 ||
        (uVar10 == 0x8b)))) {
      local_214 = 1;
    }
    *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
    param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
    FUN_0319a6a8(param_1,param_2,&local_214,&local_218);
    if ((*param_1 == 0) && (iVar11 = thunk_FUN_05e1d97c(4), iVar11 != 0)) {
      FUN_0488143c(local_230);
      ppuVar1 = (undefined1 **)local_230[0];
      if (-1 < cStack_219) {
        ppuVar1 = local_230;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3de31b & 1) == 0) {
        DAT_0a3de310._0_1_ = s_GetHandlonTh_08854480[0];
        DAT_0a3de310._1_1_ = s_GetHandlonTh_08854480[1];
        DAT_0a3de310._2_1_ = s_GetHandlonTh_08854480[2];
        DAT_0a3de310._3_1_ = s_GetHandlonTh_08854480[3];
        DAT_0a3de310._4_1_ = s_GetHandlonTh_08854480[4];
        DAT_0a3de310._5_1_ = s_GetHandlonTh_08854480[5];
        DAT_0a3de310._6_1_ = s_GetHandlonTh_08854480[6];
        DAT_0a3de310._7_1_ = s_GetHandlonTh_08854480[7];
        DAT_0a3de318 = 0x7265;
        DAT_0a3de31a = 0;
        DAT_0a3de31b = 1;
      }
      FUN_05e1d050(auStack_210,4,ppuVar1,&DAT_0a3dd350,&DAT_0a3de310,
                   "/AppKit.framework/Versions/C/AppKit",0,0);
      local_120 = (undefined8 *****)0x0;
      if ((DAT_0a3e2eba & 1) == 0) {
        uVar14 = 0;
        do {
          uVar17 = *(undefined4 *)((long)&DAT_088c56c9 + uVar14);
          uVar5 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
          uVar4 = *(undefined4 *)((long)&DAT_088c56b5 + uVar14 % 0x14);
          *(uint *)((long)&DAT_0a3e2e72 + uVar14) =
               CONCAT13((char)((uint)uVar17 >> 0x18) + 0x69U ^ (byte)((uint)uVar4 >> 0x18),
                        CONCAT12((char)((uint)uVar17 >> 0x10) + 0x69U ^ (byte)((uint)uVar4 >> 0x10),
                                 CONCAT11((char)(uVar5 >> 0x10) + 0x69U ^ (byte)((uint)uVar4 >> 8),
                                          (char)uVar5 + 0x69U ^ (byte)uVar4)));
          uVar14 = uVar14 + 4;
        } while (uVar14 != 0x48);
        DAT_0a3e2eba = 1;
      }
      uVar14 = (ulong)local_214;
      lVar8 = 0;
      do {
        lVar16 = lVar8;
        uVar9 = (uint)uVar14;
        *(undefined1 *)((long)&local_118 + lVar16) =
             *(undefined1 *)((long)&DAT_0a3e2e72 + (ulong)(uVar9 + (int)(uVar14 / 10) * -10 + 0x23))
        ;
        uVar14 = uVar14 / 10;
        lVar8 = lVar16 + 1;
      } while (9 < uVar9);
      *(undefined1 *)((long)&local_118 + lVar16 + 1) = 0;
      if (8 < lVar16 + 8U) {
        puVar15 = (undefined1 *)((long)&local_118 + lVar16);
        puVar12 = (undefined1 *)((long)&local_118 + 1);
        do {
          uVar3 = *puVar15;
          *puVar15 = puVar12[-1];
          puVar12[-1] = uVar3;
          bVar7 = puVar12 < puVar15 + -1;
          puVar15 = puVar15 + -1;
          puVar12 = puVar12 + 1;
        } while (bVar7);
      }
      local_120 = (undefined8 *****)&local_118;
      local_170 = local_168;
      lVar8 = 0;
      uVar14 = (ulong)local_218;
      do {
        lVar16 = lVar8;
        uVar9 = (uint)uVar14;
        local_168[lVar16] =
             *(undefined1 *)((long)&DAT_0a3e2e72 + (ulong)(uVar9 + (int)(uVar14 / 10) * -10 + 0x23))
        ;
        lVar8 = lVar16 + 1;
        uVar14 = uVar14 / 10;
      } while (9 < uVar9);
      local_168[lVar16 + 1] = 0;
      if (8 < lVar16 + 8U) {
        puVar15 = local_168;
        puVar12 = local_168 + lVar16;
        do {
          puVar15 = puVar15 + 1;
          uVar3 = *puVar12;
          puVar13 = puVar12 + -1;
          *puVar12 = puVar15[-1];
          puVar15[-1] = uVar3;
          puVar12 = puVar13;
        } while (puVar15 < puVar13);
      }
      if ((DAT_0a3e0770 & 1) == 0) {
        _DAT_0a3e0754 = CONCAT44((int)DAT_084c7778,(int)DAT_084c7770);
        uRam000000000a3e075c = CONCAT44((int)DAT_08480588,(int)DAT_084c7780);
        DAT_0a3e0764 = CONCAT44((int)DAT_084cf930,(int)ram0x088baa20);
        DAT_0a3e076c = (undefined4)ram0x084c9468;
        DAT_0a3e0770 = 1;
      }
      local_d0 = &local_120;
      ppuStack_c8 = &local_170;
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
      FUN_05e1d31c(auStack_210,&DAT_0a3e0754,&local_d0);
      thunk_FUN_05e1d0bc(auStack_210);
      if (cStack_219 < '\0') {
        __ZdlPvm(local_230[0],CONCAT17(cStack_219,local_220) & 0x7fffffffffffffff);
      }
    }
  }
  plVar6 = local_178;
  if (local_178 != (long *)0x0) {
    LOAcquire();
    lVar8 = local_178[1];
    local_178[1] = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*local_178 + 0x10))(local_178);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


