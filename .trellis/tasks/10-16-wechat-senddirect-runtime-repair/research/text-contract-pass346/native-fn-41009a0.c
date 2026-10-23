// Ghidra inferred pseudocode; requested=0x41009a0
// entry=041009a0 end=04100c33

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_041009a0(undefined8 param_1,undefined8 param_2,undefined8 *param_3,undefined8 *param_4)

{
  undefined8 ****ppppuVar1;
  int iVar2;
  undefined8 ***local_188 [2];
  undefined7 local_178;
  char cStack_171;
  undefined4 local_170 [2];
  undefined8 local_168;
  undefined8 uStack_160;
  ulong local_158;
  undefined8 local_150;
  undefined8 local_148;
  undefined8 uStack_140;
  ulong local_138;
  undefined8 local_130;
  undefined8 uStack_128;
  ulong local_120;
  undefined8 uStack_118;
  undefined8 uStack_110;
  ulong local_108;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
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
  iVar2 = thunk_FUN_05e1d97c(2);
  if (iVar2 != 0) {
    FUN_0488143c(local_188);
    ppppuVar1 = (undefined8 ****)local_188[0];
    if (-1 < cStack_171) {
      ppppuVar1 = local_188;
    }
    if ((DAT_0a43e621 & 1) == 0) {
      uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
      uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
      uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
      uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
      uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
      uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
      uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
      uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
      DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
      DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
      DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
      DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
      DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
      DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
      DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
      DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
      DAT_0a43e620 = 0;
      DAT_0a43e621 = 1;
    }
    if ((DAT_0a43e723 & 1) == 0) {
      DAT_0a43e718 = DAT_0889c418;
      DAT_0a43e720 = 0x6874;
      DAT_0a43e722 = 0;
      DAT_0a43e723 = 1;
    }
    FUN_05e1d050(local_170,2,ppppuVar1,&DAT_0a43e610,&DAT_0a43e718,0x174,0,0);
    if ((DAT_0a43e723 & 1) == 0) {
      DAT_0a43e718 = DAT_0889c418;
      DAT_0a43e720 = 0x6874;
      DAT_0a43e722 = 0;
      DAT_0a43e723 = 1;
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
    uStack_d0 = 0;
    FUN_05e1d31c(local_170,&DAT_0a43e718,&local_e0);
    thunk_FUN_05e1d0bc(local_170);
    if (cStack_171 < '\0') {
      __ZdlPvm(local_188[0],CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
    }
  }
  local_170[0] = 0;
  if (*(char *)((long)param_3 + 0x17) < '\0') {
    FUN_00018d20(&local_168,*param_3,param_3[1]);
  }
  else {
    uStack_160 = param_3[1];
    local_168 = *param_3;
    local_158 = param_3[2];
  }
  local_150 = 0;
  if (*(char *)((long)param_4 + 0x17) < '\0') {
    FUN_00018d20(&local_148,*param_4,param_4[1]);
  }
  else {
    uStack_140 = param_4[1];
    local_148 = *param_4;
    local_138 = param_4[2];
  }
  uStack_118 = 0;
  local_120 = 0;
  local_108 = 0;
  uStack_110 = 0;
  uStack_128 = 0;
  local_130 = 0;
  FUN_04100c94(param_1,param_2,local_170);
  if ((long)local_108 < 0) {
    __ZdlPvm(uStack_118,local_108 & 0x7fffffffffffffff);
  }
  if ((long)local_120 < 0) {
    __ZdlPvm(local_130,local_120 & 0x7fffffffffffffff);
  }
  if ((long)local_138 < 0) {
    __ZdlPvm(local_148,local_138 & 0x7fffffffffffffff);
  }
  if ((long)local_158 < 0) {
    __ZdlPvm(local_168,local_158 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


