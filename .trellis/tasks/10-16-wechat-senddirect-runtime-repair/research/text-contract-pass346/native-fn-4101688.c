// Ghidra inferred pseudocode; requested=0x4101688
// entry=04101688 end=04101953

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04101688(undefined8 param_1,undefined8 param_2,undefined8 *param_3,undefined8 param_4,
                 undefined8 *param_5,undefined8 *param_6)

{
  undefined8 ****ppppuVar1;
  int iVar2;
  undefined8 ***local_198 [2];
  undefined7 local_188;
  char cStack_181;
  undefined4 local_180 [2];
  undefined8 local_178;
  undefined8 uStack_170;
  ulong local_168;
  undefined8 local_160;
  undefined8 local_158;
  undefined8 local_150;
  ulong local_148;
  undefined8 local_140;
  undefined8 uStack_138;
  ulong local_130;
  undefined8 local_128;
  undefined8 uStack_120;
  ulong local_118;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 uStack_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar2 = thunk_FUN_05e1d97c(2);
  if (iVar2 != 0) {
    FUN_0488143c(local_198);
    ppppuVar1 = (undefined8 ****)local_198[0];
    if (-1 < cStack_181) {
      ppppuVar1 = local_198;
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
    if ((DAT_0a43e774 & 1) == 0) {
      DAT_0a43e768._0_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[8];
      DAT_0a43e768._1_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[9];
      DAT_0a43e768._2_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[10];
      DAT_0a43e768._3_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xb];
      DAT_0a43e768._4_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xc];
      DAT_0a43e768._5_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xd];
      DAT_0a43e768._6_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xe];
      DAT_0a43e768._7_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xf];
      DAT_0a43e770 = (undefined4)DAT_087d3a00;
      DAT_0a43e774 = 1;
    }
    FUN_05e1d050(local_180,2,ppppuVar1,&DAT_0a43e610,&DAT_0a43e768,0x25b,0,0);
    if ((DAT_0a43e774 & 1) == 0) {
      DAT_0a43e768._0_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[8];
      DAT_0a43e768._1_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[9];
      DAT_0a43e768._2_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[10];
      DAT_0a43e768._3_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xb];
      DAT_0a43e768._4_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xc];
      DAT_0a43e768._5_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xd];
      DAT_0a43e768._6_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xe];
      DAT_0a43e768._7_1_ = s_BeforeAuSilenceAManualLoManual_l_089be570[0xf];
      DAT_0a43e770 = (undefined4)DAT_087d3a00;
      DAT_0a43e774 = 1;
    }
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    uStack_a0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    uStack_c0 = 0;
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(local_180,&DAT_0a43e768,&local_f0);
    thunk_FUN_05e1d0bc(local_180);
    if (cStack_181 < '\0') {
      __ZdlPvm(local_198[0],CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
    }
  }
  local_180[0] = 1;
  if (*(char *)((long)param_3 + 0x17) < '\0') {
    FUN_00018d20(&local_178,*param_3,param_3[1]);
  }
  else {
    uStack_170 = param_3[1];
    local_178 = *param_3;
    local_168 = param_3[2];
  }
  local_158 = 0;
  local_150 = 0;
  local_148 = 0;
  local_160 = param_4;
  if (*(char *)((long)param_5 + 0x17) < '\0') {
    FUN_00018d20(&local_140,*param_5,param_5[1]);
  }
  else {
    uStack_138 = param_5[1];
    local_140 = *param_5;
    local_130 = param_5[2];
  }
  if (*(char *)((long)param_6 + 0x17) < '\0') {
    FUN_00018d20(&local_128,*param_6,param_6[1]);
  }
  else {
    uStack_120 = param_6[1];
    local_128 = *param_6;
    local_118 = param_6[2];
  }
  FUN_04100c94(param_1,param_2,local_180);
  if ((long)local_118 < 0) {
    __ZdlPvm(local_128,local_118 & 0x7fffffffffffffff);
  }
  if ((long)local_130 < 0) {
    __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
  }
  if ((long)local_148 < 0) {
    __ZdlPvm(local_158,local_148 & 0x7fffffffffffffff);
  }
  if ((long)local_168 < 0) {
    __ZdlPvm(local_178,local_168 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


