// Ghidra inferred pseudocode; requested=0x4a292e4
// entry=04a292e4 end=04a29617

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04a292e4(long param_1)

{
  undefined8 *****pppppuVar1;
  size_t sVar2;
  size_t sVar3;
  byte bVar4;
  byte bVar5;
  bool bVar6;
  int iVar7;
  char *pcVar8;
  char *pcVar9;
  ulong uVar10;
  char *pcVar11;
  undefined8 ****local_168 [2];
  undefined7 local_158;
  char cStack_151;
  undefined1 auStack_150 [144];
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  pcVar11 = (char *)(param_1 + 0x18);
  pcVar8 = (char *)FUN_04bb4e7c();
  bVar4 = *(byte *)(param_1 + 0x2f);
  uVar10 = (ulong)bVar4;
  sVar2 = *(size_t *)(param_1 + 0x20);
  if (-1 < (char)bVar4) {
    sVar2 = uVar10;
  }
  bVar5 = pcVar8[0x17];
  sVar3 = *(size_t *)(pcVar8 + 8);
  if (-1 < (char)bVar5) {
    sVar3 = (ulong)bVar5;
  }
  if (sVar2 == sVar3) {
    pcVar9 = *(char **)pcVar8;
    if (-1 < (char)bVar5) {
      pcVar9 = pcVar8;
    }
    if ((char)bVar4 < '\0') {
      iVar7 = _memcmp(*(void **)(param_1 + 0x18),pcVar9,*(size_t *)(param_1 + 0x20));
      if (iVar7 != 0 || *(int *)(param_1 + 0xc) == 1) goto LAB_04a29558;
    }
    else {
      pcVar8 = pcVar11;
      if (bVar4 != 0) {
        do {
          if (*pcVar8 != *pcVar9) goto LAB_04a29558;
          pcVar9 = pcVar9 + 1;
          uVar10 = uVar10 - 1;
          pcVar8 = pcVar8 + 1;
        } while (uVar10 != 0);
      }
      if (*(int *)(param_1 + 0xc) == 1) goto LAB_04a29558;
    }
    iVar7 = thunk_FUN_05e1d97c(4);
    if (iVar7 != 0) {
      FUN_0488143c(local_168);
      pppppuVar1 = (undefined8 *****)local_168[0];
      if (-1 < cStack_151) {
        pppppuVar1 = local_168;
      }
      if ((DAT_0a49254a & 1) == 0) {
        _DAT_0a492530 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
        uRam000000000a492538 = CONCAT44((int)DAT_085213d0,(int)DAT_08596720);
        DAT_0a492540 = CONCAT44((int)ram0x084e0b50,(int)DAT_084e3330);
        DAT_0a492548 = 99;
        DAT_0a49254a = 1;
      }
      if ((DAT_0a4927c2 & 1) == 0) {
        uRam000000000a4927b8._0_1_ = s_IsMmreaderMessag__08a9b150[8];
        uRam000000000a4927b8._1_1_ = s_IsMmreaderMessag__08a9b150[9];
        uRam000000000a4927b8._2_1_ = s_IsMmreaderMessag__08a9b150[10];
        uRam000000000a4927b8._3_1_ = s_IsMmreaderMessag__08a9b150[0xb];
        uRam000000000a4927b8._4_1_ = s_IsMmreaderMessag__08a9b150[0xc];
        uRam000000000a4927b8._5_1_ = s_IsMmreaderMessag__08a9b150[0xd];
        uRam000000000a4927b8._6_1_ = s_IsMmreaderMessag__08a9b150[0xe];
        uRam000000000a4927b8._7_1_ = s_IsMmreaderMessag__08a9b150[0xf];
        DAT_0a4927b0 = s_IsMmreaderMessag__08a9b150[0];
        DAT_0a4927b0_1._0_1_ = s_IsMmreaderMessag__08a9b150[1];
        DAT_0a4927b0_1._1_1_ = s_IsMmreaderMessag__08a9b150[2];
        DAT_0a4927b0_1._2_1_ = s_IsMmreaderMessag__08a9b150[3];
        DAT_0a4927b0_1._3_1_ = s_IsMmreaderMessag__08a9b150[4];
        DAT_0a4927b0_1._4_1_ = s_IsMmreaderMessag__08a9b150[5];
        DAT_0a4927b0_1._5_1_ = s_IsMmreaderMessag__08a9b150[6];
        DAT_0a4927b0_1._6_1_ = s_IsMmreaderMessag__08a9b150[7];
        DAT_0a4927c0 = 0x65;
        DAT_0a4927c2 = 1;
      }
      FUN_05e1d050(auStack_150,4,pppppuVar1,&DAT_0a492530,&DAT_0a4927b0,0x261,0,0);
      if ((DAT_0a4927e5 & 1) == 0) {
        _DAT_0a4927c4 = CONCAT44((int)DAT_085c9268,(int)DAT_08486a48);
        uRam000000000a4927cc = CONCAT44((int)DAT_084cadd8,(int)DAT_08489788);
        _DAT_0a4927d4 = CONCAT44((int)DAT_08a9b1e0,(int)DAT_084c7770);
        uRam000000000a4927dc = CONCAT44((int)DAT_08a9b1e8,(int)DAT_08655330);
        DAT_0a4927e4 = 0;
        DAT_0a4927e5 = 1;
      }
      uStack_58 = 0;
      local_60 = 0;
      uStack_48 = 0;
      uStack_50 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      uStack_b0 = 0;
      FUN_05e1d31c(auStack_150,&DAT_0a4927c4,&local_c0);
      thunk_FUN_05e1d0bc(auStack_150);
      if (cStack_151 < '\0') {
        __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
      }
    }
  }
LAB_04a29558:
  pcVar8 = (char *)FUN_04bb4e7c();
  bVar4 = *(byte *)(param_1 + 0x2f);
  uVar10 = (ulong)bVar4;
  sVar2 = *(size_t *)(param_1 + 0x20);
  if (-1 < (char)bVar4) {
    sVar2 = uVar10;
  }
  bVar5 = pcVar8[0x17];
  sVar3 = *(size_t *)(pcVar8 + 8);
  if (-1 < (char)bVar5) {
    sVar3 = (ulong)bVar5;
  }
  if (sVar2 == sVar3) {
    pcVar9 = *(char **)pcVar8;
    if (-1 < (char)bVar5) {
      pcVar9 = pcVar8;
    }
    if ((char)bVar4 < '\0') {
      iVar7 = _memcmp(*(void **)pcVar11,pcVar9,*(size_t *)(param_1 + 0x20));
      bVar6 = iVar7 == 0;
    }
    else if (bVar4 == 0) {
      bVar6 = true;
    }
    else {
      do {
        uVar10 = uVar10 - 1;
        bVar6 = *pcVar11 == *pcVar9;
        if (!bVar6) break;
        pcVar9 = pcVar9 + 1;
        pcVar11 = pcVar11 + 1;
      } while (uVar10 != 0);
    }
  }
  else {
    bVar6 = false;
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(bVar6);
}


