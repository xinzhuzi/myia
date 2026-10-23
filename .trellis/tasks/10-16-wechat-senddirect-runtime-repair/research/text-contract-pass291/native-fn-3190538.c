// Ghidra inferred pseudocode; requested=0x3190538
// entry=03190538 end=03190c73

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03190538(undefined1 *param_1,long param_2,long *******param_3,ulong param_4,ulong param_5)

{
  undefined8 *******pppppppuVar1;
  undefined1 **ppuVar2;
  undefined1 uVar3;
  uint3 uVar4;
  long *plVar5;
  bool bVar6;
  long lVar7;
  long lVar8;
  int iVar9;
  undefined1 *puVar10;
  ulong uVar11;
  undefined1 *puVar12;
  long *plVar13;
  uint uVar14;
  undefined4 uVar15;
  undefined4 uVar16;
  undefined1 *local_280 [2];
  undefined7 local_270;
  char cStack_269;
  long *local_268;
  long *local_260;
  long local_258;
  long *local_1d8;
  long *local_1d0;
  long *******local_1c8;
  undefined8 local_1c0;
  undefined7 local_1b8;
  char cStack_1b1;
  undefined8 *******local_178;
  undefined8 local_170;
  undefined7 local_168;
  char cStack_161;
  long *******local_128;
  undefined1 local_120;
  long *******local_d8;
  undefined8 *******local_d0;
  long *******ppppppplStack_c8;
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
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_1d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_032f26b8(&local_1d8,*(undefined8 *)(param_2 + 0xb78));
  local_268 = local_1d8;
  local_260 = local_1d0;
  lVar7 = 0;
  if (local_1d0 != (long *)0x0) {
    lVar7 = local_1d0[1];
    local_1d0[1] = lVar7 + 1;
  }
  local_258 = 0;
  FUN_066856fc(lVar7,&local_268);
  lVar7 = FUN_0303fe7c(&local_268);
  plVar13 = local_260;
  if (local_260 != (long *)0x0) {
    LOAcquire();
    lVar8 = local_260[1];
    local_260[1] = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*local_260 + 0x10))(local_260);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  if ((*(byte *)(lVar7 + 0x278) & 1) == 0) {
    iVar9 = thunk_FUN_05e1d97c(3);
    if (iVar9 != 0) {
      FUN_0488143c(local_280);
      ppuVar2 = (undefined1 **)local_280[0];
      if (-1 < cStack_269) {
        ppuVar2 = local_280;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar11 = 0;
        do {
          (&DAT_0a3dd350)[uVar11] = (&DAT_088bce97)[uVar11] + 0x8a ^ (&DAT_088bce87)[uVar11 & 0xf];
          uVar11 = uVar11 + 1;
        } while (uVar11 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3df0a4 & 1) == 0) {
        uRam000000000a3df098._0_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x38];
        uRam000000000a3df098._1_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x39];
        uRam000000000a3df098._2_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3a];
        uRam000000000a3df098._3_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3b];
        uRam000000000a3df098._4_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3c];
        uRam000000000a3df098._5_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3d];
        uRam000000000a3df098._6_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3e];
        uRam000000000a3df098._7_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3f];
        DAT_0a3df090 = s_AsyncCheckStoragCancelCheckStora_088bb440[0x30];
        DAT_0a3df090_1._0_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x31];
        DAT_0a3df090_1._1_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x32];
        DAT_0a3df090_1._2_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x33];
        DAT_0a3df090_1._3_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x34];
        DAT_0a3df090_1._4_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x35];
        DAT_0a3df090_1._5_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x36];
        DAT_0a3df090_1._6_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x37];
        DAT_0a3df0a0 = (undefined4)DAT_088baa50;
        DAT_0a3df0a4 = 1;
      }
      FUN_05e1d050(&local_268,3,ppuVar2,&DAT_0a3dd350,&DAT_0a3df090,0xbd8,0,0);
      local_128 = (long *******)*param_3;
      if (-1 < *(char *)((long)param_3 + 0x17)) {
        local_128 = param_3;
      }
      local_120 = 0;
      local_178 = (undefined8 *******)0x0;
      if ((DAT_0a3e2eba & 1) == 0) {
        uVar11 = 0;
        do {
          uVar15 = *(undefined4 *)((long)&DAT_088c56c9 + uVar11);
          uVar4 = CONCAT12((char)((uint)uVar15 >> 8),(short)uVar15) & 0xff00ff;
          uVar16 = *(undefined4 *)((long)&DAT_088c56b5 + uVar11 % 0x14);
          *(uint *)((long)&DAT_0a3e2e72 + uVar11) =
               CONCAT13((char)((uint)uVar15 >> 0x18) + 0x69U ^ (byte)((uint)uVar16 >> 0x18),
                        CONCAT12((char)((uint)uVar15 >> 0x10) + 0x69U ^ (byte)((uint)uVar16 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar16 >> 8)
                                           ,(char)uVar4 + 0x69U ^ (byte)uVar16)));
          uVar11 = uVar11 + 4;
        } while (uVar11 != 0x48);
        DAT_0a3e2eba = 1;
      }
      lVar7 = 0;
      do {
        lVar8 = lVar7;
        uVar14 = (uint)param_4;
        *(undefined1 *)((long)&local_170 + lVar8) =
             *(undefined1 *)
              ((long)&DAT_0a3e2e72 +
              (ulong)(uVar14 + (int)((param_4 & 0xffffffff) / 10) * -10 + 0x23));
        lVar7 = lVar8 + 1;
        param_4 = (param_4 & 0xffffffff) / 10;
      } while (9 < uVar14);
      *(undefined1 *)((long)&local_170 + lVar8 + 1) = 0;
      if (8 < lVar8 + 8U) {
        puVar10 = (undefined1 *)((long)&local_170 + lVar8);
        puVar12 = (undefined1 *)((long)&local_170 + 1);
        do {
          uVar3 = *puVar10;
          *puVar10 = puVar12[-1];
          puVar12[-1] = uVar3;
          bVar6 = puVar12 < puVar10 + -1;
          puVar10 = puVar10 + -1;
          puVar12 = puVar12 + 1;
        } while (bVar6);
      }
      local_178 = (undefined8 *******)&local_170;
      local_1c8 = (long *******)&local_1c0;
      lVar7 = 0;
      do {
        lVar8 = lVar7;
        uVar14 = (uint)param_5;
        *(undefined1 *)((long)&local_1c0 + lVar8) =
             *(undefined1 *)
              ((long)&DAT_0a3e2e72 +
              (ulong)(uVar14 + (int)((param_5 & 0xffffffff) / 10) * -10 + 0x23));
        lVar7 = lVar8 + 1;
        param_5 = (param_5 & 0xffffffff) / 10;
      } while (9 < uVar14);
      *(undefined1 *)((long)&local_1c0 + lVar8 + 1) = 0;
      if (8 < lVar8 + 8U) {
        puVar10 = (undefined1 *)((long)&local_1c0 + lVar8);
        puVar12 = (undefined1 *)((long)&local_1c0 + 1);
        do {
          uVar3 = *puVar10;
          *puVar10 = puVar12[-1];
          puVar12[-1] = uVar3;
          bVar6 = puVar12 < puVar10 + -1;
          puVar10 = puVar10 + -1;
          puVar12 = puVar12 + 1;
        } while (bVar6);
      }
      if ((DAT_0a3df0d5 & 1) == 0) {
        _DAT_0a3df0a8 = CONCAT44((int)DAT_0848f630,(int)DAT_08485378);
        uRam000000000a3df0b0 = CONCAT44((int)DAT_0848a170,(int)DAT_086bf770);
        _DAT_0a3df0b8 = CONCAT44((int)DAT_084d00e0,(int)DAT_087fe760);
        uRam000000000a3df0c0 = CONCAT44((int)DAT_0848f630,(int)ram0x08648e50);
        DAT_0a3df0c8 = CONCAT44((int)DAT_08504b78,(int)DAT_085b0708);
        DAT_0a3df0d0 = (undefined4)DAT_08504b70;
        DAT_0a3df0d4 = 0;
        DAT_0a3df0d5 = 1;
      }
      local_d8 = (long *******)&local_128;
      local_d0 = &local_178;
      ppppppplStack_c8 = (long *******)&local_1c8;
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
      local_60 = 0;
      FUN_05e1d31c(&local_268,&DAT_0a3df0a8,&local_d8);
      thunk_FUN_05e1d0bc(&local_268);
      if (cStack_269 < '\0') {
        __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[0x278] = 0;
  }
  else {
    iVar9 = thunk_FUN_05e1d97c(2);
    if (iVar9 != 0) {
      FUN_0488143c(&local_178);
      pppppppuVar1 = local_178;
      if (-1 < cStack_161) {
        pppppppuVar1 = &local_178;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar11 = 0;
        do {
          (&DAT_0a3dd350)[uVar11] = (&DAT_088bce97)[uVar11] + 0x8a ^ (&DAT_088bce87)[uVar11 & 0xf];
          uVar11 = uVar11 + 1;
        } while (uVar11 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3df0a4 & 1) == 0) {
        uRam000000000a3df098._0_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x38];
        uRam000000000a3df098._1_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x39];
        uRam000000000a3df098._2_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3a];
        uRam000000000a3df098._3_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3b];
        uRam000000000a3df098._4_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3c];
        uRam000000000a3df098._5_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3d];
        uRam000000000a3df098._6_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3e];
        uRam000000000a3df098._7_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x3f];
        DAT_0a3df090 = s_AsyncCheckStoragCancelCheckStora_088bb440[0x30];
        DAT_0a3df090_1._0_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x31];
        DAT_0a3df090_1._1_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x32];
        DAT_0a3df090_1._2_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x33];
        DAT_0a3df090_1._3_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x34];
        DAT_0a3df090_1._4_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x35];
        DAT_0a3df090_1._5_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x36];
        DAT_0a3df090_1._6_1_ = s_AsyncCheckStoragCancelCheckStora_088bb440[0x37];
        DAT_0a3df0a0 = (undefined4)DAT_088baa50;
        DAT_0a3df0a4 = 1;
      }
      FUN_05e1d050(&local_268,2,pppppppuVar1,&DAT_0a3dd350,&DAT_0a3df090,0xbdd,0,0);
      FUN_04cbe4cc(&local_1c8,lVar7);
      local_128 = local_1c8;
      if (-1 < cStack_1b1) {
        local_128 = (long *******)&local_1c8;
      }
      local_120 = 0;
      if ((DAT_0a3df0fc & 1) == 0) {
        _DAT_0a3df0d8 = CONCAT44((int)DAT_0848f630,(int)DAT_08485378);
        uRam000000000a3df0e0 = CONCAT44((int)DAT_0848a170,(int)DAT_086bf770);
        _DAT_0a3df0e8 = CONCAT44((int)DAT_084d00e0,(int)DAT_087fe760);
        uRam000000000a3df0f0 = CONCAT44((int)DAT_08480ab8,(int)DAT_08486a48);
        DAT_0a3df0f8 = (undefined4)DAT_084d1ec0;
        DAT_0a3df0fc = 1;
      }
      ppppppplStack_c8 = (long *******)0x0;
      local_d0 = (undefined8 *******)0x0;
      local_d8 = (long *******)&local_128;
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
      local_60 = 0;
      FUN_05e1d31c(&local_268,&DAT_0a3df0d8,&local_d8);
      if (cStack_1b1 < '\0') {
        __ZdlPvm(local_1c8,CONCAT17(cStack_1b1,local_1b8) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_268);
      if (cStack_161 < '\0') {
        __ZdlPvm(local_178,CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
      }
    }
    local_268 = (long *)0x0;
    local_260 = (long *)0x0;
    local_258 = 0;
    local_260 = (long *)FUN_03025b60(&local_268,lVar7);
    FUN_031b5470(param_2,param_3,&local_268);
    FUN_02a0cf30(param_1,local_268);
    plVar5 = local_268;
    param_1[0x278] = 1;
    plVar13 = local_260;
    if (local_268 != (long *)0x0) {
      while (plVar13 != plVar5) {
        plVar13 = plVar13 + -0x4f;
        (**(code **)*plVar13)(plVar13);
      }
      local_260 = plVar5;
      __ZdlPvm(local_268,local_258 - (long)local_268);
    }
  }
  plVar13 = local_1d0;
  if (local_1d0 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_1d0[1];
    local_1d0[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_1d0 + 0x10))(local_1d0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


