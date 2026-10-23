// Ghidra inferred pseudocode; requested=0x453bd60
// entry=0453bd60 end=0453c15b

/* WARNING: Removing unreachable block (ram,0x0453c06c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0453bd60(undefined8 *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4)

{
  ulong uVar1;
  int iVar2;
  size_t sVar3;
  undefined8 ****ppppuVar4;
  code *pcVar5;
  undefined8 **local_210 [2];
  undefined7 local_200;
  char cStack_1f9;
  undefined8 ***local_1f8 [2];
  undefined7 local_1e8;
  char cStack_1e1;
  undefined8 ***local_1e0;
  undefined1 *puStack_1d8;
  undefined1 *local_1d0;
  undefined1 *puStack_1c8;
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *local_1b0;
  undefined **local_148 [3];
  undefined ***local_130;
  undefined8 **local_128;
  undefined1 local_120;
  undefined8 ***local_d8;
  size_t sStack_d0;
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
  iVar2 = thunk_FUN_05e1d97c(4);
  if (iVar2 != 0) {
    FUN_0488143c(local_1f8);
    ppppuVar4 = (undefined8 ****)local_1f8[0];
    if (-1 < cStack_1e1) {
      ppppuVar4 = local_1f8;
    }
    if ((DAT_0a455765 & 1) == 0) {
      DAT_0a455758._0_1_ = s_coroutinCoAsync_087e2ce0[0];
      DAT_0a455758._1_1_ = s_coroutinCoAsync_087e2ce0[1];
      DAT_0a455758._2_1_ = s_coroutinCoAsync_087e2ce0[2];
      DAT_0a455758._3_1_ = s_coroutinCoAsync_087e2ce0[3];
      DAT_0a455758._4_1_ = s_coroutinCoAsync_087e2ce0[4];
      DAT_0a455758._5_1_ = s_coroutinCoAsync_087e2ce0[5];
      DAT_0a455758._6_1_ = s_coroutinCoAsync_087e2ce0[6];
      DAT_0a455758._7_1_ = s_coroutinCoAsync_087e2ce0[7];
      DAT_0a455760 = (undefined4)DAT_084c8598;
      DAT_0a455764 = 0;
      DAT_0a455765 = 1;
    }
    if ((DAT_0a455877 & 1) == 0) {
      DAT_0a455868._0_1_ = s_DoCreateDummyJ_089feb76[2];
      DAT_0a455868._1_1_ = s_DoCreateDummyJ_089feb76[3];
      DAT_0a455868._2_1_ = s_DoCreateDummyJ_089feb76[4];
      DAT_0a455868._3_1_ = s_DoCreateDummyJ_089feb76[5];
      DAT_0a455868._4_1_ = s_DoCreateDummyJ_089feb76[6];
      DAT_0a455868._5_1_ = s_DoCreateDummyJ_089feb76[7];
      DAT_0a455868._6_1_ = s_DoCreateDummyJ_089feb76[8];
      DAT_0a455868._7_1_ = s_DoCreateDummyJ_089feb76[9];
      DAT_0a455870 = (undefined4)ram0x089feb80;
      DAT_0a455874 = 0x626f;
      DAT_0a455876 = 0;
      DAT_0a455877 = 1;
    }
    FUN_05e1d050(&local_1e0,4,ppppuVar4,&DAT_0a455758,&DAT_0a455868,0x3e,0,0);
    FUN_0453dd8c(local_210,param_3,param_4);
    local_128 = local_210[0];
    if (-1 < cStack_1f9) {
      local_128 = local_210;
    }
    local_120 = 0;
    if ((DAT_0a455897 & 1) == 0) {
      _DAT_0a455878 = CONCAT44((int)DAT_085312b0,(int)DAT_08487570);
      uRam000000000a455880 = CONCAT44((int)DAT_084d77b8,(int)DAT_084d8738);
      DAT_0a455888 = CONCAT44((int)DAT_084cae88,(int)DAT_087716f0);
      DAT_0a455890 = (undefined4)DAT_08562ac0;
      DAT_0a455894 = 0x5f25;
      DAT_0a455896 = 0;
      DAT_0a455897 = 1;
    }
    uStack_c8 = 0;
    sStack_d0 = 0;
    local_d8 = &local_128;
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
    FUN_05e1d31c(&local_1e0,&DAT_0a455878,&local_d8);
    if (cStack_1f9 < '\0') {
      __ZdlPvm(local_210[0],CONCAT17(cStack_1f9,local_200) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_1e0);
    if (cStack_1e1 < '\0') {
      __ZdlPvm(local_1f8[0],CONCAT17(cStack_1e1,local_1e8) & 0x7fffffffffffffff);
    }
  }
  local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e0 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a4558a2 & 1) == 0) {
    DAT_0a455898._0_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0];
    DAT_0a455898._1_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[1];
    DAT_0a455898._2_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[2];
    DAT_0a455898._3_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[3];
    DAT_0a455898._4_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[4];
    DAT_0a455898._5_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[5];
    DAT_0a455898._6_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[6];
    DAT_0a455898._7_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[7];
    DAT_0a4558a0 = 0x62;
    DAT_0a4558a2 = 1;
  }
  sVar3 = _strlen((char *)&DAT_0a455898);
  if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_d8);
  }
  if (sVar3 < 0x17) {
    uStack_c8 = CONCAT17((char)sVar3,(undefined7)uStack_c8);
    ppppuVar4 = &local_d8;
    if (sVar3 != 0) goto LAB_0453c028;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    ppppuVar4 = (undefined8 ****)__Znwm(uVar1);
    uStack_c8 = uVar1 | 0x8000000000000000;
    local_d8 = ppppuVar4;
    sStack_d0 = sVar3;
LAB_0453c028:
    _memcpy(ppppuVar4,&DAT_0a455898,sVar3);
  }
  *(undefined1 *)((long)ppppuVar4 + sVar3) = 0;
  puStack_1d8 = (undefined1 *)sStack_d0;
  local_1e0 = local_d8;
  local_1d0 = (undefined1 *)uStack_c8;
  local_1c0 = (undefined1 *)0x0;
  puStack_1b8 = (undefined1 *)0x0;
  local_1b0 = (undefined1 *)0x80000000ffffffff;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  local_148[0] = &PTR_FUN_09e86d78;
  puStack_1c8 = (undefined1 *)param_2;
  local_130 = local_148;
  FUN_0667ddb0(param_1,&local_1e0,local_148);
  if (local_130 == local_148) {
    pcVar5 = (code *)(*local_130)[4];
  }
  else {
    if (local_130 == (undefined ***)0x0) goto LAB_0453c0f4;
    pcVar5 = (code *)(*local_130)[5];
  }
  (*pcVar5)();
LAB_0453c0f4:
  (**(code **)(*(long *)*param_1 + 0x18))();
  if ((long)local_1d0 < 0) {
    __ZdlPvm(local_1e0,(ulong)local_1d0 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


