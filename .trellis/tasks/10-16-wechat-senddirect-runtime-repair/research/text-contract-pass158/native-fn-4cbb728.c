// Ghidra inferred pseudocode; requested=0x4cbb728
// entry=04cbb728 end=04cbbc4b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04cbb728(long param_1,undefined8 *param_2)

{
  bool bVar1;
  undefined1 **ppuVar2;
  undefined1 uVar3;
  undefined4 uVar4;
  uint3 uVar5;
  long lVar6;
  int iVar7;
  size_t sVar8;
  undefined8 *puVar9;
  ulong uVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  long lVar13;
  uint uVar14;
  undefined1 *puVar15;
  ulong uVar16;
  undefined4 uVar17;
  undefined1 *local_250 [2];
  undefined7 local_240;
  char cStack_239;
  undefined8 local_238;
  undefined8 uStack_230;
  undefined8 local_228;
  undefined1 *local_1a8;
  undefined1 local_1a0 [72];
  undefined1 *local_158;
  undefined1 local_150 [72];
  undefined1 *local_108;
  undefined1 local_100 [72];
  undefined1 **local_b8;
  undefined1 **ppuStack_b0;
  undefined1 **local_a8;
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
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((DAT_0a4adb55 & 1) == 0) {
    DAT_0a4adb50 = (undefined4)DAT_08486088;
    DAT_0a4adb54 = 0;
    DAT_0a4adb55 = 1;
  }
  sVar8 = _strlen((char *)&DAT_0a4adb50);
  if ((long)*(char *)((long)param_2 + 0x17) < 0) {
    if (sVar8 == param_2[1]) {
      if (sVar8 == 0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0(param_2);
      }
      puVar9 = (undefined8 *)*param_2;
      goto LAB_04cbb7c0;
    }
  }
  else {
    puVar9 = param_2;
    if (sVar8 == (long)*(char *)((long)param_2 + 0x17)) {
LAB_04cbb7c0:
      iVar7 = _memcmp(puVar9,&DAT_0a4adb50,sVar8);
      if (iVar7 == 0) {
        iVar7 = thunk_FUN_05e1d97c(2);
        if (iVar7 != 0) {
          FUN_0488143c(local_250);
          ppuVar2 = (undefined1 **)local_250[0];
          if (-1 < cStack_239) {
            ppuVar2 = local_250;
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
          if ((DAT_0a4adb66 & 1) == 0) {
            DAT_0a4adb58._0_1_ = s_message_SetSendeSetType_08ad4560[8];
            DAT_0a4adb58._1_1_ = s_message_SetSendeSetType_08ad4560[9];
            DAT_0a4adb58._2_1_ = s_message_SetSendeSetType_08ad4560[10];
            DAT_0a4adb58._3_1_ = s_message_SetSendeSetType_08ad4560[0xb];
            DAT_0a4adb58._4_1_ = s_message_SetSendeSetType_08ad4560[0xc];
            DAT_0a4adb58._5_1_ = s_message_SetSendeSetType_08ad4560[0xd];
            DAT_0a4adb58._6_1_ = s_message_SetSendeSetType_08ad4560[0xe];
            DAT_0a4adb58._7_1_ = s_message_SetSendeSetType_08ad4560[0xf];
            DAT_0a4adb60 = (undefined4)DAT_0878f988;
            DAT_0a4adb64 = 0x65;
            DAT_0a4adb66 = 1;
          }
          FUN_05e1d050(&local_238,2,ppuVar2,&DAT_0a4ad970,&DAT_0a4adb58,0x256,0,0);
          uVar10 = *(ulong *)(param_1 + 0xf8);
          local_108 = (undefined1 *)0x0;
          if ((DAT_0a4adbd0 & 1) == 0) {
            uVar16 = 0;
            do {
              uVar17 = *(undefined4 *)((long)&DAT_08ad519e + uVar16);
              uVar5 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
              uVar4 = *(undefined4 *)((long)&DAT_08ad518a + uVar16 % 0x14);
              *(uint *)((long)&DAT_0a4adb88 + uVar16) =
                   CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar4 >> 0x18),
                            CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar4 >> 0x10),
                                     CONCAT11((char)(uVar5 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar4 >> 8),
                                              (char)uVar5 + 0x8aU ^ (byte)uVar4)));
              uVar16 = uVar16 + 4;
            } while (uVar16 != 0x48);
            DAT_0a4adbd0 = 1;
          }
          lVar6 = 0;
          do {
            lVar13 = lVar6;
            local_100[lVar13] = *(undefined1 *)(uVar10 % 10 + 0xa4adbab);
            bVar1 = 9 < uVar10;
            uVar10 = uVar10 / 10;
            lVar6 = lVar13 + 1;
          } while (bVar1);
          local_100[lVar13 + 1] = 0;
          if (8 < lVar13 + 8U) {
            puVar15 = local_100;
            puVar11 = local_100 + lVar13;
            do {
              puVar15 = puVar15 + 1;
              uVar3 = *puVar11;
              puVar12 = puVar11 + -1;
              *puVar11 = puVar15[-1];
              puVar15[-1] = uVar3;
              puVar11 = puVar12;
            } while (puVar15 < puVar12);
          }
          local_108 = local_100;
          local_158 = (undefined1 *)0x0;
          lVar6 = 0;
          uVar10 = (ulong)*(uint *)(param_1 + 0xc);
          do {
            lVar13 = lVar6;
            uVar14 = (uint)uVar10;
            local_150[lVar13] =
                 *(undefined1 *)
                  ((long)&DAT_0a4adb88 + (ulong)(uVar14 + (int)(uVar10 / 10) * -10 + 0x23));
            lVar6 = lVar13 + 1;
            uVar10 = uVar10 / 10;
          } while (9 < uVar14);
          local_150[lVar13 + 1] = 0;
          if (8 < lVar13 + 8U) {
            puVar15 = local_150;
            puVar11 = local_150 + lVar13;
            do {
              puVar15 = puVar15 + 1;
              uVar3 = *puVar11;
              puVar12 = puVar11 + -1;
              *puVar11 = puVar15[-1];
              puVar15[-1] = uVar3;
              puVar11 = puVar12;
            } while (puVar15 < puVar12);
          }
          local_158 = local_150;
          local_1a8 = local_1a0;
          lVar6 = 0;
          uVar10 = (ulong)*(uint *)(param_1 + 0x10);
          do {
            lVar13 = lVar6;
            uVar14 = (uint)uVar10;
            local_1a0[lVar13] =
                 *(undefined1 *)
                  ((long)&DAT_0a4adb88 + (ulong)(uVar14 + (int)(uVar10 / 10) * -10 + 0x23));
            lVar6 = lVar13 + 1;
            uVar10 = uVar10 / 10;
          } while (9 < uVar14);
          local_1a0[lVar13 + 1] = 0;
          if (8 < lVar13 + 8U) {
            puVar15 = local_1a0;
            puVar11 = local_1a0 + lVar13;
            do {
              puVar15 = puVar15 + 1;
              uVar3 = *puVar11;
              puVar12 = puVar11 + -1;
              *puVar11 = puVar15[-1];
              puVar15[-1] = uVar3;
              puVar11 = puVar12;
            } while (puVar15 < puVar12);
          }
          if ((DAT_0a4adb84 & 1) == 0) {
            _DAT_0a4adb68 = CONCAT44((int)DAT_084de688,(int)ram0x08507778);
            uRam000000000a4adb70 = CONCAT44((int)DAT_084ceed0,(int)DAT_084ce700);
            DAT_0a4adb78 = CONCAT44((int)DAT_08489788,(int)DAT_0866e2c8);
            DAT_0a4adb80 = (undefined4)ram0x084c9468;
            DAT_0a4adb84 = 1;
          }
          local_b8 = &local_108;
          ppuStack_b0 = &local_158;
          local_a8 = &local_1a8;
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
          uStack_48 = 0;
          local_50 = 0;
          local_40 = 0;
          FUN_05e1d31c(&local_238,&DAT_0a4adb68,&local_b8);
          thunk_FUN_05e1d0bc(&local_238);
          if (cStack_239 < '\0') {
            __ZdlPvm(local_250[0],CONCAT17(cStack_239,local_240) & 0x7fffffffffffffff);
          }
        }
        goto LAB_04cbb84c;
      }
    }
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0x48,param_2);
  if (*(char *)(param_1 + 0x5f) < '\0') {
    if (*(long *)(param_1 + 0x50) != 0) goto LAB_04cbb7f4;
  }
  else if (*(char *)(param_1 + 0x5f) != '\0') {
LAB_04cbb7f4:
    uVar10 = FUN_04bb3974(param_1 + 0x48);
    if ((((uVar10 & 1) == 0) && (uVar10 = FUN_04bb3a88(param_1 + 0x48), (uVar10 & 1) == 0)) &&
       (iVar7 = FUN_04bb4c9c(param_1 + 0x48), iVar7 == 0)) goto LAB_04cbb84c;
  }
  FUN_04cbbc88(&local_238,param_1);
  if (*(char *)(param_1 + 0x5f) < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x48),*(ulong *)(param_1 + 0x58) & 0x7fffffffffffffff);
  }
  *(undefined8 *)(param_1 + 0x50) = uStack_230;
  *(undefined8 *)(param_1 + 0x48) = local_238;
  *(undefined8 *)(param_1 + 0x58) = local_228;
LAB_04cbb84c:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


