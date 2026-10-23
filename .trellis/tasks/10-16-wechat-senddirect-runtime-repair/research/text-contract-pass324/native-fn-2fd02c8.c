// Ghidra inferred pseudocode; requested=0x2fd02c8
// entry=02fd02c8 end=02fd0673

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02fd02c8(undefined8 *param_1,long param_2,undefined8 param_3)

{
  undefined1 *puVar1;
  ulong uVar2;
  int iVar3;
  ulong uVar4;
  undefined8 *puVar5;
  char *pcVar6;
  size_t sVar7;
  undefined8 *******pppppppuVar8;
  undefined1 local_188;
  undefined7 uStack_187;
  undefined7 local_178;
  char cStack_171;
  undefined8 *******local_170;
  size_t local_168;
  undefined8 local_160;
  undefined4 local_158;
  ulong local_150;
  undefined8 local_148;
  ulong local_140;
  undefined1 auStack_138 [88];
  ulong local_e0;
  undefined8 uStack_d8;
  ulong local_d0;
  undefined8 uStack_c8;
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
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar3 = thunk_FUN_05e1d97c(2);
  if (iVar3 != 0) {
    FUN_0488143c(&local_188);
    puVar1 = (undefined1 *)CONCAT71(uStack_187,local_188);
    if (-1 < cStack_171) {
      puVar1 = &local_188;
    }
    if ((DAT_0a3d2361 & 1) == 0) {
      uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
      uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
      uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
      uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
      uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
      uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
      uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
      uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
      DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
      DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
      DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
      DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
      DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
      DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
      DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
      DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
      DAT_0a3d2360 = 0;
      DAT_0a3d2361 = 1;
    }
    if ((DAT_0a3d2a23 & 1) == 0) {
      DAT_0a3d2a18 = DAT_0889c418;
      DAT_0a3d2a20 = 0x6874;
      DAT_0a3d2a22 = 0;
      DAT_0a3d2a23 = 1;
    }
    FUN_05e1d050(&local_170,2,puVar1,&DAT_0a3d2350,&DAT_0a3d2a18,0x2e2,0,0);
    if ((DAT_0a3d2a23 & 1) == 0) {
      DAT_0a3d2a18 = DAT_0889c418;
      DAT_0a3d2a20 = 0x6874;
      DAT_0a3d2a22 = 0;
      DAT_0a3d2a23 = 1;
    }
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
    uStack_d8 = 0;
    local_e0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    FUN_05e1d31c(&local_170,&DAT_0a3d2a18,&local_e0);
    thunk_FUN_05e1d0bc(&local_170);
    if (cStack_171 < '\0') {
      __ZdlPvm(CONCAT71(uStack_187,local_188),CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
    }
  }
  uVar4 = FUN_0473def4(param_2 + 0x168);
  if ((uVar4 & 1) != 0) {
    local_160 = local_160 & 0xffffffffffffff;
    local_170 = (undefined8 *******)((ulong)local_170 & 0xffffffffffffff00);
    local_d0 = local_d0 & 0xffffffffffffff;
    local_e0 = local_e0 & 0xffffffffffffff00;
    cStack_171 = '\0';
    local_188 = 0;
    FUN_02fd0768(param_1,param_2,param_3,param_2 + 0x168,param_2 + 0x180,&local_170,&local_e0,
                 &local_188,0);
    uVar4 = local_e0;
    uVar2 = local_d0;
    if (cStack_171 < '\0') {
      __ZdlPvm(CONCAT71(uStack_187,local_188),CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
      uVar4 = local_e0;
      uVar2 = local_d0;
    }
    goto joined_r0x02fd05e4;
  }
  param_1[5] = 0;
  param_1[4] = 0;
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  puVar5 = (undefined8 *)__Znwm(0x270);
  puVar5[2] = 0;
  puVar5[1] = 0;
  *puVar5 = &PTR_FUN_09de0f80;
  _bzero(puVar5 + 3,0x228);
  *(undefined4 *)(puVar5 + 3) = 1;
  puVar5[0x40] = 0;
  puVar5[0x42] = 0;
  puVar5[0x41] = 0;
  *(undefined1 *)(puVar5 + 0x43) = 0;
  puVar5[0x11] = 0;
  puVar5[0x10] = 0;
  puVar5[0x13] = 0;
  puVar5[0x12] = 0;
  puVar5[0x15] = 0;
  puVar5[0x14] = 0;
  puVar5[0x17] = 0;
  puVar5[0x16] = 0;
  puVar5[0x19] = 0;
  puVar5[0x18] = 0;
  puVar5[0x1b] = 0;
  puVar5[0x1a] = 0;
  puVar5[0x1d] = 0;
  puVar5[0x1c] = 0;
  puVar5[0x1f] = 0;
  puVar5[0x1e] = 0;
  puVar5[0x21] = 0;
  puVar5[0x20] = 0;
  puVar5[0x23] = 0;
  puVar5[0x22] = 0;
  puVar5[0x25] = 0;
  puVar5[0x24] = 0;
  puVar5[0x27] = 0;
  puVar5[0x26] = 0;
  puVar5[0x29] = 0;
  puVar5[0x28] = 0;
  puVar5[0x2b] = 0;
  puVar5[0x2a] = 0;
  puVar5[0x2d] = 0;
  puVar5[0x2c] = 0;
  puVar5[0x2f] = 0;
  puVar5[0x2e] = 0;
  puVar5[0x31] = 0;
  puVar5[0x30] = 0;
  puVar5[0x33] = 0;
  puVar5[0x32] = 0;
  puVar5[0x35] = 0;
  puVar5[0x34] = 0;
  puVar5[0x37] = 0;
  puVar5[0x36] = 0;
  puVar5[0x39] = 0;
  puVar5[0x38] = 0;
  puVar5[0x3b] = 0;
  puVar5[0x3a] = 0;
  puVar5[0x3d] = 0;
  puVar5[0x3c] = 0;
  *(undefined8 *)((long)puVar5 + 0x1f1) = 0;
  *(undefined8 *)((long)puVar5 + 0x1e9) = 0;
  *(undefined2 *)(puVar5 + 0x47) = 0;
  puVar5[0x46] = 0;
  puVar5[0x45] = 0;
  puVar5[0x44] = 0;
  puVar5[0x49] = 0;
  puVar5[0x48] = 0;
  puVar5[0x4b] = 0;
  puVar5[0x4a] = 0;
  puVar5[0x4d] = 0;
  puVar5[0x4c] = 0;
  param_1[4] = puVar5 + 3;
  param_1[5] = puVar5;
  *param_1 = DAT_0889c420;
  pcVar6 = (char *)FUN_04e044e8();
  sVar7 = _strlen(pcVar6);
  if (0x7ffffffffffffff7 < sVar7) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_170);
  }
  if (sVar7 < 0x17) {
    local_160 = CONCAT17((char)sVar7,(undefined7)local_160);
    pppppppuVar8 = &local_170;
    if (sVar7 != 0) goto LAB_02fd059c;
  }
  else {
    uVar4 = 0x19;
    if ((sVar7 | 7) != 0x17) {
      uVar4 = (sVar7 | 7) + 1;
    }
    pppppppuVar8 = (undefined8 *******)__Znwm(uVar4);
    local_160 = uVar4 | 0x8000000000000000;
    local_170 = pppppppuVar8;
    local_168 = sVar7;
LAB_02fd059c:
    _memmove(pppppppuVar8,pcVar6,sVar7);
  }
  *(undefined1 *)((long)pppppppuVar8 + sVar7) = 0;
  local_158 = 0;
  local_148 = 0;
  local_140 = 0;
  local_150 = 0;
  FUN_0002b2c0(auStack_138);
  FUN_02fc4f04(param_1[4] + 0x10,&local_170);
  FUN_0002b440(auStack_138);
  uVar4 = local_150;
  uVar2 = local_140;
joined_r0x02fd05e4:
  if ((long)uVar2 < 0) {
    __ZdlPvm(uVar4,uVar2 & 0x7fffffffffffffff);
  }
  if ((long)local_160 < 0) {
    __ZdlPvm(local_170,local_160 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


