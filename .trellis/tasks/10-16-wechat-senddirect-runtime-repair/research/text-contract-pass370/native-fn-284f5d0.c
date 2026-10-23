// Ghidra inferred pseudocode; requested=0x284f5d0
// entry=0284f5d0 end=0284f923

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0284f5d0(undefined8 param_1,long param_2)

{
  undefined8 ***pppuVar1;
  int iVar2;
  undefined8 **local_168 [2];
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
  iVar2 = thunk_FUN_05e1d97c(2);
  if (iVar2 != 0) {
    FUN_0488143c(local_168);
    pppuVar1 = (undefined8 ***)local_168[0];
    if (-1 < cStack_151) {
      pppuVar1 = local_168;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39e023 & 1) == 0) {
      DAT_0a39e018._0_1_ = s_OnInitSyger__087e2c30[0];
      DAT_0a39e018._1_1_ = s_OnInitSyger__087e2c30[1];
      DAT_0a39e018._2_1_ = s_OnInitSyger__087e2c30[2];
      DAT_0a39e018._3_1_ = s_OnInitSyger__087e2c30[3];
      DAT_0a39e018._4_1_ = s_OnInitSyger__087e2c30[4];
      DAT_0a39e018._5_1_ = s_OnInitSyger__087e2c30[5];
      DAT_0a39e018._6_1_ = s_OnInitSyger__087e2c30[6];
      DAT_0a39e018._7_1_ = s_OnInitSyger__087e2c30[7];
      DAT_0a39e020 = 0x636e;
      DAT_0a39e022 = 0;
      DAT_0a39e023 = 1;
    }
    FUN_05e1d050(auStack_150,2,pppuVar1,&DAT_0a39dff8,&DAT_0a39e018,0xb3,0,0);
    if ((DAT_0a39e044 & 1) == 0) {
      _DAT_0a39e024 = CONCAT44((int)DAT_08482f20,(int)DAT_087e2fa8);
      uRam000000000a39e02c = CONCAT44((int)DAT_084d82d8,(int)DAT_08484c30);
      _DAT_0a39e034 = CONCAT44((int)DAT_08805040,(int)DAT_087d7b18);
      uRam000000000a39e03c = CONCAT44((int)DAT_084e0fd8,(int)DAT_087e2c48);
      DAT_0a39e044 = 1;
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
    FUN_05e1d31c(auStack_150,&DAT_0a39e024,&local_c0);
    thunk_FUN_05e1d0bc(auStack_150);
    if (cStack_151 < '\0') {
      __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
    }
  }
  *(undefined1 *)(param_2 + 0x60) = 1;
  FUN_0284f958(param_2);
  FUN_0284fc28(param_2);
  FUN_0284ff04(param_2);
  FUN_028501d4(param_2);
  FUN_028504b0(param_2);
  FUN_02850794(param_2);
  FUN_02850a70(param_2);
  FUN_02850d58(param_2);
  FUN_02851034(param_2);
  FUN_02851304(param_2);
  FUN_028515d4(param_2);
  FUN_028518b0(param_2);
  FUN_02851b88(param_2);
  FUN_02851e78(param_2);
  FUN_02852148(param_2);
  FUN_02852418(param_2);
  FUN_028526a4(param_2);
  FUN_02852980(param_2);
  FUN_0287cab4(param_2);
  FUN_02852c58(param_2);
  FUN_02852f38(param_2);
  FUN_028531fc(param_2);
  FUN_02853490(param_2);
  FUN_0285372c(param_2);
  FUN_028539f4(param_2);
  FUN_02853cb8(param_2);
  FUN_02853f8c(param_2);
  FUN_02854220(param_2);
  FUN_028544e4(param_2);
  FUN_028547a4(param_2);
  FUN_02854a74(param_2);
  FUN_02854d08(param_2);
  FUN_02854fcc(param_2);
  FUN_02855298(param_2);
  FUN_02855560(param_2);
  FUN_02855844(param_2);
  FUN_02855aec(param_2);
  FUN_02855d8c(param_2);
  FUN_02856018(param_2);
  FUN_02322b5c(param_1);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


