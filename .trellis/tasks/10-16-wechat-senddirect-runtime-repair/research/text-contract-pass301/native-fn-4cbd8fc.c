// Ghidra inferred pseudocode; requested=0x4cbd8fc
// entry=04cbd8fc end=04cbde23

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04cbd8fc(undefined8 *param_1,long param_2)

{
  undefined8 ****ppppuVar1;
  char cVar2;
  char cVar3;
  int iVar4;
  int iVar5;
  ulong uVar6;
  size_t sVar7;
  void *pvVar8;
  void *pvVar9;
  undefined8 *puVar10;
  ulong uVar11;
  void *pvVar12;
  void *pvVar13;
  void *pvVar14;
  undefined8 ***local_200 [2];
  undefined7 local_1f0;
  char cStack_1e9;
  undefined8 ***local_1e8 [2];
  undefined7 local_1d8;
  char cStack_1d1;
  undefined1 auStack_1d0 [144];
  undefined8 ***local_140;
  undefined1 local_138;
  undefined8 ***local_f0;
  undefined8 local_e8;
  undefined8 uStack_e0;
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
  uVar6 = FUN_04bb3974(param_2 + 0x18);
  if ((((((uVar6 & 1) != 0) || (uVar6 = FUN_04bb3974(param_2 + 0x30), (uVar6 & 1) != 0)) ||
       (uVar6 = FUN_04bb3a88(param_2 + 0x18), (uVar6 & 1) != 0)) ||
      (uVar6 = FUN_04bb3a88(param_2 + 0x30), (uVar6 & 1) != 0)) &&
     (iVar5 = *(int *)(param_2 + 0xc), iVar5 != 10000)) {
    pvVar14 = (void *)(param_2 + 0x130);
    if ((DAT_0a4ad9a3 & 1) == 0) {
      _DAT_0a4ad9a0 = 0xa3a;
      DAT_0a4ad9a2 = 0;
      DAT_0a4ad9a3 = 1;
    }
    cVar2 = *(char *)(param_2 + 0x147);
    uVar6 = (ulong)cVar2;
    uVar11 = uVar6;
    pvVar12 = pvVar14;
    if ((long)uVar6 < 0) {
      uVar11 = *(ulong *)(param_2 + 0x138);
      pvVar12 = *(void **)(param_2 + 0x130);
    }
    sVar7 = _strlen(&DAT_0a4ad9a0);
    if (sVar7 == 0) {
      uVar11 = 0;
    }
    else {
      pvVar9 = (void *)((long)pvVar12 + uVar11);
      pvVar13 = pvVar9;
      if ((long)sVar7 <= (long)uVar11) {
        cVar3 = DAT_0a4ad9a0;
        pvVar8 = pvVar12;
        do {
          pvVar13 = pvVar9;
          if (((0xfffffffffffffffe < uVar11 - sVar7) ||
              (pvVar8 = _memchr(pvVar8,(int)cVar3,(uVar11 - sVar7) + 1), pvVar8 == (void *)0x0)) ||
             (iVar4 = _memcmp(pvVar8,&DAT_0a4ad9a0,sVar7), pvVar13 = pvVar8, iVar4 == 0)) break;
          pvVar8 = (void *)((long)pvVar8 + 1);
          uVar11 = (long)pvVar9 - (long)pvVar8;
          pvVar13 = pvVar9;
        } while ((long)sVar7 <= (long)uVar11);
      }
      uVar11 = (long)pvVar13 - (long)pvVar12;
      if (pvVar13 == pvVar9) {
        uVar11 = 0xffffffffffffffff;
      }
    }
    if ((iVar5 == 11000) && (*(int *)(param_2 + 0x10) == 0x7c)) {
      if ((DAT_0a4ada13 & 1) == 0) {
        DAT_0a4ada10 = 0x203a;
        DAT_0a4ada12 = 0;
        DAT_0a4ada13 = 1;
      }
      pvVar12 = pvVar14;
      uVar11 = uVar6;
      if (cVar2 < '\0') {
        pvVar12 = *(void **)(param_2 + 0x130);
        uVar11 = *(ulong *)(param_2 + 0x138);
      }
      sVar7 = _strlen((char *)&DAT_0a4ada10);
      if (sVar7 == 0) {
        uVar11 = 0;
        goto LAB_04cbdb3c;
      }
      if ((long)sVar7 <= (long)uVar11) {
        pvVar13 = (void *)((long)pvVar12 + uVar11);
        cVar3 = (char)DAT_0a4ada10;
        pvVar9 = pvVar12;
        do {
          if ((0xfffffffffffffffe < uVar11 - sVar7) ||
             (pvVar9 = _memchr(pvVar9,(int)cVar3,(uVar11 - sVar7) + 1), pvVar9 == (void *)0x0))
          break;
          iVar5 = _memcmp(pvVar9,&DAT_0a4ada10,sVar7);
          if (iVar5 == 0) {
            if (pvVar9 != pvVar13) {
              uVar11 = (long)pvVar9 - (long)pvVar12;
              goto LAB_04cbdb34;
            }
            break;
          }
          pvVar9 = (void *)((long)pvVar9 + 1);
          uVar11 = (long)pvVar13 - (long)pvVar9;
        } while ((long)sVar7 <= (long)uVar11);
      }
    }
    else {
LAB_04cbdb34:
      if (uVar11 != 0xffffffffffffffff) {
LAB_04cbdb3c:
        if (cVar2 < '\0') {
          pvVar14 = *(void **)(param_2 + 0x130);
          uVar6 = *(ulong *)(param_2 + 0x138);
        }
        if (uVar11 <= uVar6) {
          uVar6 = uVar11;
        }
        if (0x7ffffffffffffff7 < uVar6) {
                    /* WARNING: Subroutine does not return */
          FUN_00018d9c(param_1);
        }
        if (uVar6 < 0x17) {
          *(char *)((long)param_1 + 0x17) = (char)uVar6;
          puVar10 = param_1;
          if (uVar6 != 0) goto LAB_04cbddc8;
        }
        else {
          uVar11 = 0x19;
          if ((uVar6 | 7) != 0x17) {
            uVar11 = (uVar6 | 7) + 1;
          }
          puVar10 = (undefined8 *)__Znwm(uVar11);
          param_1[1] = uVar6;
          param_1[2] = uVar11 | 0x8000000000000000;
          *param_1 = puVar10;
LAB_04cbddc8:
          _memmove(puVar10,pvVar14,uVar6);
          param_1 = puVar10;
        }
        param_1 = (undefined8 *)((long)param_1 + uVar6);
        goto LAB_04cbdddc;
      }
    }
    if ((*(char *)(param_2 + 600) == '\x01') && (iVar5 = thunk_FUN_05e1d97c(4), iVar5 != 0)) {
      FUN_0488143c(local_1e8);
      ppppuVar1 = (undefined8 ****)local_1e8[0];
      if (-1 < cStack_1d1) {
        ppppuVar1 = local_1e8;
      }
      if ((DAT_0a4ad97b & 1) == 0) {
        DAT_0a4ad970._0_1_ = s_message_SetSendeSetType_08ad4560[0];
        DAT_0a4ad970._1_1_ = s_message_SetSendeSetType_08ad4560[1];
        DAT_0a4ad970._2_1_ = s_message_SetSendeSetType_08ad4560[2];
        DAT_0a4ad970._3_1_ = s_message_SetSendeSetType_08ad4560[3];
        DAT_0a4ad970._4_1_ = s_message_SetSendeSetType_08ad4560[4];
        DAT_0a4ad970._5_1_ = s_message_SetSendeSetType_08ad4560[5];
        DAT_0a4ad970._6_1_ = s_message_SetSendeSetType_08ad4560[6];
        DAT_0a4ad970._7_1_ = s_message_SetSendeSetType_08ad4560[7];
        DAT_0a4ad978 = 0x6363;
        DAT_0a4ad97a = 0;
        DAT_0a4ad97b = 1;
      }
      if ((DAT_0a4ada2e & 1) == 0) {
        _DAT_0a4ada14 = CONCAT44((int)DAT_084fdd10,(int)DAT_084b0388);
        uRam000000000a4ada1c = CONCAT44((int)DAT_084b0678,(int)DAT_084b0670);
        DAT_0a4ada24 = CONCAT44((int)DAT_0878f988,(int)DAT_084aeae0);
        DAT_0a4ada2c = 0x65;
        DAT_0a4ada2e = 1;
      }
      FUN_05e1d050(auStack_1d0,4,ppppuVar1,&DAT_0a4ad970,&DAT_0a4ada14,0x1c8,0,0);
      FUN_04cbde70(local_200,param_2);
      local_140 = local_200[0];
      if (-1 < cStack_1e9) {
        local_140 = local_200;
      }
      local_138 = 0;
      if ((DAT_0a4ada54 & 1) == 0) {
        _DAT_0a4ada30 = CONCAT44((int)DAT_084c7770,(int)ram0x084caf40);
        uRam000000000a4ada38 = CONCAT44((int)DAT_0848a1c0,(int)DAT_084a04e8);
        _DAT_0a4ada40 = CONCAT44((int)DAT_08531fb0,(int)DAT_08850808);
        uRam000000000a4ada48 = CONCAT44((int)DAT_0852a9d0,(int)DAT_086071c8);
        DAT_0a4ada50 = (undefined4)ram0x084c9468;
        DAT_0a4ada54 = 1;
      }
      uStack_e0 = 0;
      local_e8 = 0;
      local_f0 = &local_140;
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
      FUN_05e1d31c(auStack_1d0,&DAT_0a4ada30,&local_f0);
      if (cStack_1e9 < '\0') {
        __ZdlPvm(local_200[0],CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(auStack_1d0);
      if (cStack_1d1 < '\0') {
        __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
      }
    }
  }
  *(undefined1 *)((long)param_1 + 0x17) = 0;
LAB_04cbdddc:
  *(undefined1 *)param_1 = 0;
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_70) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


