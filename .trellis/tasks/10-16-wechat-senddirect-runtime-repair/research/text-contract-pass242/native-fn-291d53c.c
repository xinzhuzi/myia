// Ghidra inferred pseudocode; requested=0x291d53c
// entry=0291d53c end=0291da27

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0291d53c(undefined8 param_1,undefined8 param_2,long ****param_3,undefined8 *param_4)

{
  long ****pppplVar1;
  undefined8 ****ppppuVar2;
  int iVar3;
  undefined8 uVar4;
  undefined8 local_230;
  undefined8 ***local_228 [2];
  undefined7 local_218;
  char cStack_211;
  undefined1 auStack_210 [144];
  long ***local_180;
  undefined1 local_178;
  undefined7 local_170;
  char cStack_169;
  long ***local_130;
  undefined1 *puStack_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *local_110;
  undefined1 *puStack_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  undefined1 *puStack_f0;
  undefined1 *local_e8;
  long ***local_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
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
  uVar4 = thunk_FUN_05e1d97c(2);
  if ((int)uVar4 != 0) {
    FUN_0488143c(&local_180);
    pppplVar1 = (long ****)local_180;
    if (-1 < cStack_169) {
      pppplVar1 = &local_180;
    }
    if ((DAT_0a3a556a & 1) == 0) {
      _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
      uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
      _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
      uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
      DAT_0a3a5564 = (undefined4)DAT_084ccd80;
      DAT_0a3a5568 = 99;
      DAT_0a3a556a = 1;
    }
    if ((DAT_0a3a5578 & 1) == 0) {
      DAT_0a3a5570[0] = s_Execute_08781cc8[0];
      DAT_0a3a5570[1] = s_Execute_08781cc8[1];
      DAT_0a3a5570[2] = s_Execute_08781cc8[2];
      DAT_0a3a5570[3] = s_Execute_08781cc8[3];
      DAT_0a3a5570[4] = s_Execute_08781cc8[4];
      DAT_0a3a5570[5] = s_Execute_08781cc8[5];
      DAT_0a3a5570[6] = s_Execute_08781cc8[6];
      DAT_0a3a5570[7] = s_Execute_08781cc8[7];
      DAT_0a3a5578 = 1;
    }
    FUN_05e1d050(auStack_210,2,pppplVar1,&DAT_0a3a5544,DAT_0a3a5570,0xbc,0,0);
    local_130 = *param_3;
    if (-1 < *(char *)((long)param_3 + 0x17)) {
      local_130 = (long ***)param_3;
    }
    puStack_128 = (undefined1 *)((ulong)puStack_128 & 0xffffffffffffff00);
    if ((DAT_0a3a5595 & 1) == 0) {
      _DAT_0a3a557c = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
      uRam000000000a3a5584 = CONCAT44((int)DAT_08781cb0,(int)ram0x087713c8);
      DAT_0a3a558c = CONCAT44((int)DAT_08492cc0,(int)DAT_084e0fd0);
      DAT_0a3a5594 = 0;
      DAT_0a3a5595 = 1;
    }
    uStack_c8 = 0;
    local_d0 = 0;
    local_d8 = (long ***)&local_130;
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
    FUN_05e1d31c(auStack_210,&DAT_0a3a557c,&local_d8);
    uVar4 = thunk_FUN_05e1d0bc(auStack_210);
    if (cStack_169 < '\0') {
      uVar4 = __ZdlPvm(local_180,CONCAT17(cStack_169,local_170) & 0x7fffffffffffffff);
    }
  }
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  local_e8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  local_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  local_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
  local_130 = (long ***)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0291dab8(&local_130,uVar4,param_2,param_4);
  if ((char)local_e8 == '\x01') {
    iVar3 = thunk_FUN_05e1d97c(2);
    if (iVar3 != 0) {
      FUN_0488143c(local_228);
      ppppuVar2 = (undefined8 ****)local_228[0];
      if (-1 < cStack_211) {
        ppppuVar2 = local_228;
      }
      if ((DAT_0a3a556a & 1) == 0) {
        _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
        uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
        _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
        uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
        DAT_0a3a5564 = (undefined4)DAT_084ccd80;
        DAT_0a3a5568 = 99;
        DAT_0a3a556a = 1;
      }
      if ((DAT_0a3a5578 & 1) == 0) {
        DAT_0a3a5570[0] = s_Execute_08781cc8[0];
        DAT_0a3a5570[1] = s_Execute_08781cc8[1];
        DAT_0a3a5570[2] = s_Execute_08781cc8[2];
        DAT_0a3a5570[3] = s_Execute_08781cc8[3];
        DAT_0a3a5570[4] = s_Execute_08781cc8[4];
        DAT_0a3a5570[5] = s_Execute_08781cc8[5];
        DAT_0a3a5570[6] = s_Execute_08781cc8[6];
        DAT_0a3a5570[7] = s_Execute_08781cc8[7];
        DAT_0a3a5578 = 1;
      }
      FUN_05e1d050(auStack_210,2,ppppuVar2,&DAT_0a3a5544,DAT_0a3a5570,0xc5,0,0);
      local_180 = *param_3;
      if (-1 < *(char *)((long)param_3 + 0x17)) {
        local_180 = (long ***)param_3;
      }
      local_178 = 0;
      if ((DAT_0a3a55b4 & 1) == 0) {
        _DAT_0a3a5598 = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
        uRam000000000a3a55a0 = CONCAT44((int)DAT_0880ab18,(int)ram0x087715b0);
        DAT_0a3a55a8 = CONCAT44((int)DAT_0880ab20,(int)DAT_084d4b58);
        DAT_0a3a55b0 = (undefined4)DAT_085028c8;
        DAT_0a3a55b4 = 1;
      }
      uStack_c8 = 0;
      local_d0 = 0;
      local_d8 = (long ***)&local_180;
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
      FUN_05e1d31c(auStack_210,&DAT_0a3a5598,&local_d8);
      thunk_FUN_05e1d0bc(auStack_210);
      if (cStack_211 < '\0') {
        __ZdlPvm(local_228[0],CONCAT17(cStack_211,local_218) & 0x7fffffffffffffff);
      }
    }
    if (((ulong)local_e8 & 1) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_004d04d4();
    }
    local_230 = *param_4;
    *param_4 = 0;
    FUN_0291fb70(param_1,&local_130,param_3,&local_230);
    FUN_00033d2c(&local_230);
    if (((ulong)local_e8 & 1) == 0) goto LAB_0291d9c0;
  }
  else if ((char)local_e8 == '\0') goto LAB_0291d9c0;
  if ((long)local_100 < 0) {
    __ZdlPvm(local_110,(ulong)local_100 & 0x7fffffffffffffff);
  }
  if ((long)local_120 < 0) {
    __ZdlPvm(local_130,(ulong)local_120 & 0x7fffffffffffffff);
  }
LAB_0291d9c0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


